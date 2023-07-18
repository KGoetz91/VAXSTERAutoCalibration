# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:39:11 2023

@author: klaus
"""

import pyFAI,fabio
from PIL import Image
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from numbers import Number
from scipy.optimize import curve_fit

from matplotlib.colors import LogNorm

import os
from os.path import isfile

import hdf5plugin
import h5py

def linear_function(x, m, b):
    return m*x+b

def gaussian(x,x0,sigma,area,const):
    
    prefactor = area/np.sqrt(2*np.pi*sigma*sigma)
    exponent = -0.5*np.power(((x-x0)/sigma),2)
    gaussian = prefactor*np.exp(exponent)+const
    
    return gaussian

def lin_interpolate(x1,y1,e1,x2,y2,e2,x_det):
  a = (y2-y1)/(x2-x1)
  ea = np.sqrt((e1*e1)+(e2*e2))
  eb = np.sqrt((e1*e1)+(e2*e2)+(ea*ea))
  b = 0.5*(y2+y1-a*(x1+x2))
  ydet = a*x_det+b
  edet = np.sqrt((x_det*x_det*ea*ea)+(eb*eb))
  return x_det,ydet,edet

def spline_data(x0, data):
  x1 = np.array(data[0])
  y1 = np.array(data[1])
  e1 = np.array(data[2])

  y2 = []
  e2 = []

  for x in x0:
    eps = x*1e-4
    diff = np.abs(np.subtract(x1,x))
    if diff.min() < eps:
      eq_ind = np.argmin(diff)
      y2.append(y1[eq_ind])
      e2.append(e1[eq_ind])
    else:
      min_ind = np.where(x1<x)[0]
      max_ind = np.where(x1>x)[0]
      if len(min_ind) == 0:
        xx1 = x1[max_ind[0]]
        xx2 = x1[max_ind[1]]
        yy1 = y1[max_ind[0]]
        yy2 = y1[max_ind[1]]
        ee1 = e1[max_ind[0]]
        ee2 = e1[max_ind[1]]
        xdet, ydet, edet = lin_interpolate(xx1,yy1,ee1,xx2,yy2,ee2,x)
      elif len(max_ind) == 0:
        xx1 = x1[min_ind[-1]]
        xx2 = x1[min_ind[-2]]
        yy1 = y1[min_ind[-1]]
        yy2 = y1[min_ind[-2]]
        ee1 = e1[min_ind[-1]]
        ee2 = e1[min_ind[-2]]
        xdet, ydet, edet = lin_interpolate(xx1,yy1,ee1,xx2,yy2,ee2,x)
      else:
        xx1 = x1[max_ind[0]]
        yy1 = y1[max_ind[0]]
        ee1 = e1[max_ind[0]]
        xx2 = x1[min_ind[-1]]
        yy2 = y1[min_ind[-1]]
        ee2 = e1[min_ind[-1]]
        xdet, ydet, edet = lin_interpolate(xx1,yy1,ee1,xx2,yy2,ee2,x)

      y2.append(ydet)
      e2.append(edet)
    
  return x0,y2,e2

class BaseOneDDataSet:
    
    def __mul__(self,value):
        if isinstance(value,Number):
            new_header = self._header+"#Arithmetic operation multiplication: {}*{}\n".format(self.name, value)
            new_y = np.multiply(self.y,value)
            new_error = np.multiply(self.error,value)
            return BaseOneDDataSet(np.array(self.x), new_y,error=new_error,name=self.name,header=new_header)
        else:
            raise ValueError('Only numbers are possible.')

    def __truediv__(self,value):
        if isinstance(value,Number):
            new_header = self._header+"#Arithmetic operation multiplication: {}*{}\n".format(self.name, value)
            new_y = np.divide(self.y,value)
            new_error = np.divide(self.error,value)
            return BaseOneDDataSet(np.array(self.x), new_y,error=new_error,name=self.name,header=new_header)
        else:
            raise ValueError('Only numbers are possible.')
    
    def spline(self,x1,y1,e1,x2,y2,e2):
        
        x_min = max(min(x1),min(x2))
        x_max = min(max(x1),max(x2))
        
        y1_new = np.where(x1 >= x_min, y1, None)
        y1_new = np.where(x1 <= x_max, y1_new, None)
        y1_new = y1_new[y1_new != None]
        e1_new = e1[x1>=x_min]
        x1_new = x1[x1>=x_min]
        e1_new = e1_new[x1_new<=x_max]
        x1_new = x1_new[x1_new<=x_max]
        
        y_spline = []
        
        x_spline, y_spline, e_spline = spline_data(x1_new,[x2,y2,e2])
        
        return x_spline,y1_new,y_spline,e1_new,e_spline

    def make_linear(self, x_min=(-1)*np.inf, x_max=np.inf):
        min_limit = x_min if x_min > min(self.x) else min(self.x)
        max_limit = x_max if x_max < max(self.x) else max(self.x)
        
        y0 = self.y[self.x<min_limit]
        y1 = self.y[self.x>min_limit]
        x1 = self.x[self.x>min_limit]
        y1 = y1[x1<max_limit]
        x1 = x1[x1<max_limit]
        y2 = self.y[self.x>max_limit]
        x0 = self.x[self.x<min_limit]
        x2 = self.x[self.x>max_limit]

        m_0 = y1[-1]-y1[0]
        b_0 = y1[0]-m_0*x1[0]
        p_0 = [m_0, b_0]
        p_best, cov = curve_fit(linear_function, x1, y1, p0=p_0)
        y1 = linear_function(x1, *p_best)
        
        self.x = np.array(list(x0)+list(x1)+list(x2))
        self.y = np.array(list(y0)+list(y1)+list(y2))
    
    def make_horizontal(self, value, x_min=(-1)*np.inf, x_max=np.inf):
        min_limit = x_min if x_min > min(self.x) else min(self.x)
        max_limit = x_max if x_max < max(self.x) else max(self.x)
        
        y0 = self.y[self.x<min_limit]
        y1 = self.y[self.x>min_limit]
        x1 = self.x[self.x>min_limit]
        y1 = y1[x1<max_limit]
        x1 = x1[x1<max_limit]
        y2 = self.y[self.x>max_limit]
        x0 = self.x[self.x<min_limit]
        x2 = self.x[self.x>max_limit]

        y1 = [value for i in y1]
        
        self.x = np.array(list(x0)+list(x1)+list(x2))
        self.y = np.array(list(y0)+list(y1)+list(y2))
    
    def interpolate(self, x_min=(-1)*np.inf, x_max=np.inf):
        min_limit = x_min if x_min > min(self.x) else min(self.x)
        max_limit = x_max if x_max < max(self.x) else max(self.x)
        
        y0 = self.y[self.x<min_limit]
        y1 = self.y[self.x>min_limit]
        x1 = self.x[self.x>min_limit]
        y1 = y1[x1<max_limit]
        x1 = x1[x1<max_limit]
        y2 = self.y[self.x>max_limit]
        x0 = self.x[self.x<min_limit]
        x2 = self.x[self.x>max_limit]
        
        m0 = (y1[-1]-y1[0])/(x1[-1]-x1[0])
        b0 = 0.5*(y1[-1]+y1[0]-m0*(x1[-1]+x1[0]))
        p0 = [m0, b0]
        
        p_opt, pcov = curve_fit(linear_function,x1,y1,p0)
        y_opt = linear_function(x1, *p_opt)
        self.x = np.array(list(x0)+list(x1)+list(x2))
        self.y = np.array(list(y0)+list(y_opt)+list(y2))
        
    def __sub__(self,secondDataset):
        if issubclass(type(secondDataset),BaseOneDDataSet):
            new_header = self._header + "#Arithmetic operation subtraction: {}-{}\n".format(self.name, secondDataset.name)
            x1 = np.array(self.x)
            y1 = np.array(self.y)
            e1 = np.array(self.error)
            
            x2 = np.array(secondDataset.x)
            y2 = np.array(secondDataset.y)
            e2 = np.array(secondDataset.error)
            
            xspline,y3,y4,e3,e4 = self.spline(x1,y1,e1,x2,y2,e2)
            new_y = np.subtract(y3,y4)
            new_e = np.sqrt(np.power(e3,2)+np.power(e4,2))
            new_x = xspline
            
        elif isinstance(secondDataset, Number):
            new_header = self._header + "#Arithmetic operation subtraction: {}-{}\n".format(self.name, secondDataset)
            new_y = np.subtract(self.y,secondDataset)
            new_x = np.array(self.x)
            new_e = np.array(self.e)
        else:
            raise ValueError('Subtraction only defined for numbers and other 1D-Datasets')
        return BaseOneDDataSet(new_x, new_y,error=new_e,name=self.name,header=new_header)
    
    def __add__(self,secondDataset):
        if issubclass(type(secondDataset),BaseOneDDataSet):
            new_header = self._header + "#Arithmetic operation subtraction: {}-{}\n".format(self.name, secondDataset.name)
            x1 = np.array(self.x)
            y1 = np.array(self.y)
            e1 = np.array(self.error)
            
            x2 = np.array(secondDataset.x)
            y2 = np.array(secondDataset.y)
            e2 = np.array(secondDataset.error)
            
            xspline,y3,y4,e3,e4 = self.spline(x1,y1,e1,x2,y2,e2)
                
            new_y = np.add(y3,y4)
            new_e = np.sqrt(np.power(e3,2)+np.power(e4,2))
            new_x = xspline
            
        elif isinstance(secondDataset, Number):
            new_header = self._header + "#Arithmetic operation subtraction: {}-{}\n".format(self.name, secondDataset)
            new_y = np.add(self.y,secondDataset)
            new_x = np.array(self.x)
            new_e = np.array(self.e)
        else:
            raise ValueError('Subtraction only defined for numbers and other 1D-Datasets')
        return BaseOneDDataSet(new_x, new_y,error=new_e,name=self.name,header=new_header)

    def __init__(self,x,y,name = '', header='', error=None):
        self.x = x
        self.y = y
        if type(error) == type(None):
            self.error = np.sqrt(y)
        else:
            if len(error) == len(x):
                self.error = error
            else:
                self.error = np.sqrt(y)
        self._header=header
        self.name = name

    def write_data_nm(self, filename):
        
        data = zip(self.x,self.y,self.error)
        
        with open(filename,'w') as outputfile:
            outputfile.write(self._header)
            outputfile.write('#Created: {}\n'.format(datetime.now()))
            outputfile.write('#Q[nm^-1]\tIntensity[cm^-1]\tError\n')
            
            for line in data:
                for point in line:
                    outputfile.write("{}\t".format(point))
                outputfile.write("\n")

    def write_data_AA(self, filename):
        
        data = zip(self.x/10,self.y,self.error)
        
        with open(filename,'w') as outputfile:
            outputfile.write(self._header)
            outputfile.write('#Created: {}\n'.format(datetime.now()))
            outputfile.write('#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
            
            for line in data:
                for point in line:
                    outputfile.write("{}\t".format(point))
                outputfile.write("\n")

    def plot_data(self):
        plt.clf()
        plt.plot(self.x,self.y,label=self.name)
        plt.legend()
        plt.show()

class OneDLoader(BaseOneDDataSet):
    def __init__(self,filename):
        x,y,error,name,header = self.load_data(filename)
        header += '#Reloaded from file: {}\n'.format(filename)
        super().__init__(x,y,name=name,header=header,error=error)
        
    def load_data(self,filename):
        
        header = ''
        name = ''
        x = []
        y = []
        e = []
        with open(filename,'r') as inputfile:
            for line in inputfile:
                if line.startswith('#'):
                    header += line
                    if line.startswith('#Sample:'):
                        namelist = list(line.strip().split())[1:]
                        for part in namelist:
                            name += "{} ".format(part)
                else:
                    try:
                        data = list(line.strip().split())
                        x.append(float(data[0]))
                        y.append(float(data[1]))
                        e.append(float(data[2]))
                    except:
                        header += "#{}".format(line)
        return np.array(x),np.array(y),np.array(e),name, header

    def write_data(self, outputfilename, column_names):
        data = zip(self.x,self.y,self.error)
        
        with open(outputfilename,'w') as outputfile:
            outputfile.write(self._header)
            outputfile.write('#Created: {}\n'.format(datetime.now()))
            outputfile.write(column_names)
            
            for line in data:
                for point in line:
                    outputfile.write("{}\t".format(point))
                outputfile.write("\n")

class CapillaryScan(BaseOneDDataSet):
    
    def __init__(self,scannumber,scanfile):
        self.scan_command = ''
        name = ''
        x,y,error = self.get_scan_from_file(scannumber,scanfile)
        for i in self.scan_command:
            name += "{} ".format(i)
        super().__init__(x,y,error=error,name=name)

    def cap_thickness(self):
        
        x0_guess=self.x[np.argmin(self.y)]
        sigma_guess=0.25
        const_guess = np.max(self.y)
        area_guess = np.min(self.y)-np.max(self.y)
        start_params = [x0_guess,sigma_guess,
                        area_guess,const_guess]
        
        
        y_gauss_start = gaussian(self.x, *start_params)
        params, covarianz = curve_fit(gaussian, self.x, self.y, p0=start_params)
        print(params)
        plt.clf()
        plt.plot(self.x,self.y,label="{}".format(self.name))
        plt.plot(self.x, y_gauss_start, label='Start values')
        plt.plot(self.x, gaussian(self.x,*params),label="Fit")
        plt.legend()
        plt.show()
        return 2*params[1]

    def get_scan_from_file(self,scannumber,scanfile):
        
        x = []
        y = []
        error = []
        
        scan_found = False
        with open(scanfile, 'r') as inputfile:
            for line in inputfile:
                if scan_found == False:
                    if line.startswith('#S {}'.format(scannumber)):
                        scan_found = True
                        self.scan_command = list(line.split())[2:]
                else:
                    if (not line.startswith('#')) and (len(line.strip())>0):
                        data = list(line.strip().split())
                        x.append(float(data[0]))
                        y.append(float(data[-1]))
                        error.append(np.sqrt(float(data[-1])))
                    elif line.startswith('#S'):
                        break

        return np.array(x),np.array(y),np.array(error)
                
class Transmission:
    
    def __init__(self,DB,data,mask,poni):
        self.DBImage = TwoDDataset(DB, poni,mask)
        if type(data)==TwoDDataset:
            self.transmissionImage = data
        else:
            self.transmissionImage = TwoDDataset(data, poni,mask)
    
    def tm_counts(self):
        return self.transmissionImage.calculateSum()
    
    def db_counts(self):
        return self.DBImage.calculateSum()
    
    def transmission(self):
        return self.transmissionImage.calculateSum()/self.DBImage.calculateSum()

class TwoDDataset:
    
    def _load_data(self):
        im = Image.open(self.inputfile)
        return np.array(im)
    
    def _init_parameters(self):
        self.inputfile = ""
        self.imageData = None
        self.errorData = None
        self.integrator = None
        self.mask = None
        self.shape = None
    
    def _load_mask(self, mask):
        img = fabio.open(mask)
        return img.data
    
    def add(self,secondDataset,error=None):
        if (type(secondDataset) == TwoDDataset) and (self.shape == secondDataset.shape):
            newImage = np.add(self.imageData, secondDataset.imageData)
            newError = np.sqrt(np.add(np.power(self.errorData,2),np.power(secondDataset.errorData,2)))
        elif isinstance(secondDataset,Number):
            newImage = np.add(self.imageData, secondDataset)
            if error == None:
                newError = self.errorData
            else:
                newError = np.sqrt(np.add(np.power(self.errorData,2),np.power(error,2)))
        else:
            raise TypeError('Operator only defined for two 2D-Datasets of same size or number values.')
        self.imageData = newImage
        self.errorData = newError
        return self
    
    def sub(self,secondDataset,error=None):
        if (type(secondDataset) == TwoDDataset) and (self.shape == secondDataset.shape):
            newImage = np.subtract(self.imageData, secondDataset.imageData)
            newError = np.sqrt(np.add(np.power(self.errorData,2),np.power(secondDataset.errorData,2)))
        elif isinstance(secondDataset,Number):
            newImage = np.subtract(self.imageData, secondDataset)
            if error == None:
                newError = self.errorData
            else:
                newError = np.sqrt(np.add(np.power(self.errorData,2),np.power(error,2)))
        else:
            print("Type secondDataset: {}\n".format(type(secondDataset)))
            raise TypeError('Operator only defined for two 2D-Datasets of same size or number values.')
        self.imageData = newImage
        self.errorData = newError
        return self
    
    def mul(self,secondDataset,error=None):
        if (type(secondDataset) == TwoDDataset) and (self.shape == secondDataset.shape):
            newImage = np.multiply(self.imageData, secondDataset.imageData)
            newError = np.sqrt(np.add(np.power(np.multiply(self.imageData,secondDataset.errorData),2)
                                      ,np.power(np.multiply(self.errorData,secondDataset.imageData),2)))
        elif isinstance(secondDataset,Number):
            newImage = np.multiply(self.imageData, secondDataset)
            if error == None:
                newError = self.errorData
            else:
                newError = np.sqrt(np.add(np.power(np.multiply(self.imageData,error),2)
                                          ,np.power(np.multiply(self.errorData,secondDataset),2)))
        else:
            raise TypeError('Operator only defined for two 2D-Datasets of same size or number values.')
        self.imageData = newImage
        self.errorData = newError
        return self
            
    def __init__(self, filename, poni, mask=None):
        self._init_parameters()
        self.inputfile = filename
        self.imageData = self._load_data()
        self.errorData = np.sqrt(self.imageData)
        self.shape = self.imageData.shape
        self.integrator = pyFAI.load(poni)
        if not mask == None:
            self.mask = self._load_mask(mask)
    
    def change_poni(self,poni):
        self.integrator = pyFAI.load(poni)
    
    def direct_beam_intensity(self):
        (x,y),(xsig,ysig)=self.direct_beam()
        direct_beam_array=self.imageData[int(y-ysig):int(y+ysig),int(x-xsig):int(x+xsig)]
        return direct_beam_array.sum()
        
    def direct_beam(self):
        x_projection = self.imageData.sum(0)
        y_projection = self.imageData.sum(1)
        
        x_initial = np.argmax(x_projection)
        x_max = x_projection[x_initial]
        y_initial = np.argmax(y_projection)
        y_max = y_projection[y_initial]
        
        x_0 = [x_initial, 0.5, x_max, 0]
        y_0 = [y_initial, 0.5, y_max, 0]
        
        x_bins = np.arange(0,len(x_projection),1)
        y_bins = np.arange(0,len(y_projection),1)
        
        x_f, x_cov = curve_fit(gaussian, x_bins, x_projection, p0=x_0)
        y_f, y_cov = curve_fit(gaussian, y_bins, y_projection, p0=y_0)
        
        # plt.clf()
        # fig, axes = plt.subplots(2,2)
        # axes[0][0].plot(y_bins,y_projection)
        # axes[0][0].plot(y_bins,gaussian(y_bins, *y_f))
        # axes[0][0].set_xlim((y_initial-10,y_initial+10))
        # axes[1][1].plot(x_bins,x_projection)
        # axes[1][1].plot(x_bins,gaussian(x_bins, *x_f))
        # axes[1][1].set_xlim((x_initial-10,x_initial+10))
        # axes[0][1].imshow(self.imageData[y_initial-10:y_initial+10,x_initial-10:x_initial+10])
        # plt.show()
        
        return (x_f[0],y_f[0]),(x_f[1],y_f[1])
        
    def plotImage(self):
        plt.imshow(self.imageData,norm=LogNorm())
        
    def plotMask(self):
        if type(self.mask)!=None:
            plt.imshow(self.mask)
    
    def pixels(self, mask=None):
        if type(mask) == type(None):
            if type(self.mask) != type(None):
                result = len(self.mask[self.mask==0].flatten())
            else:
                result = len(self.imageData.flatten())
        elif type(mask) == type(self.imageData):
            if mask.shape==self.imageData.shape:
                result = len(mask[mask==0].flatten())
            else:
                raise ValueError('Mask needs to be of same shape as Image.')
        else:
            raise ValueError('Mask needs to be numpy array.')
        return result
        
    
    def calculateSum(self, mask=None):
        if type(mask) == type(None):
            if type(self.mask) != type(None):
                inverseMask = np.where(self.mask == 0, 1,0)
                sumImage = np.multiply(inverseMask, self.imageData).flatten()
            else:
                sumImage = sumImage[sumImage >= 0]
        elif type(mask) == type(self.imageData):
            if mask.shape==self.imageData.shape:
                inverseMask = np.where(mask == 0, 1,0)
                sumImage = np.multiply(inverseMask, self.imageData)
                sumImage = sumImage.flatten()
            else:
                raise ValueError('Mask needs to be of same shape as Image.')
        else:
            raise ValueError('Mask needs to be numpy array.')
        imageSum = np.sum(sumImage)
        return imageSum
    
    def scatteringIntensity(self):
        mask = np.array(self.mask)
        (x,y),(sigx,sigy)=self.direct_beam()
        #print(x,y,sigx,sigy)
        mask[int(y)-int(sigy)-8:int(y)+int(sigy)+10,int(x)-int(sigx)-8:int(x)+int(sigx)+10] = 1
        scat_inte = self.calculateSum(mask)
        return scat_inte
    
    def integrateImage(self, bins=425):
        if type(self.mask)!=None:
            result = self.integrator.integrate1d_ng(self.imageData,npt = bins, mask=self.mask,
                                                    correctSolidAngle=True, unit = "q_nm^-1",
                                                    variance=np.power(self.errorData,2))
        else:
            result = self.integrator.integrate1d_ng(self.imageData,npt = bins, correctSolidAngle=True,
                                                    unit = "q_nm^-1",variance=np.power(self.errorData,2))
        return result

class OneDDataSet(BaseOneDDataSet):
    
    def __init__(self, pyFAIIntegratorResult, name, header=''):
        self.completeData = pyFAIIntegratorResult
        super().__init__(x = np.array(pyFAIIntegratorResult[0]),
                         y = np.array(pyFAIIntegratorResult[1]),
                         error = np.array(pyFAIIntegratorResult[2]),
                         header=header, name=name)

    def get_header(self):
        return self._header

    def write_data_nm(self, filename):
        
        data = zip(self.x,self.y,self.error)
        
        with open(filename,'w') as outputfile:
            outputfile.write(self._header)
            outputfile.write('#Created: {}\n'.format(datetime.now()))
            outputfile.write('#Q[nm^-1]\tIntensity[cm^-1]\tError\n')
            
            for line in data:
                for point in line:
                    outputfile.write("{}\t".format(point))
                outputfile.write("\n")

    def write_data_AA(self, filename):
        
        data = zip(self.x/10,self.y,self.error)
        
        with open(filename,'w') as outputfile:
            outputfile.write(self._header)
            outputfile.write('#Created: {}\n'.format(datetime.now()))
            outputfile.write('#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
            
            for line in data:
                for point in line:
                    outputfile.write("{}\t".format(point))
                outputfile.write("\n")
        
class TwoDReducer():
    
    def _set_calib_parameter(self, ParamName, parameterValue):
    
        if (type(parameterValue)==int) or (type(parameterValue)==float):
            return np.array(len(self.frames)*[parameterValue])
        elif (((type(parameterValue)==list) or (type(parameterValue)==np.ndarray))
              and (len(parameterValue)==len(self.frames))):
            return parameterValue
        else:
            raise ValueError('{} needs to be a number or list of numbers.'.format(ParamName))
       
    
    def _load_frames(self,dataFiles,poni,mask):
        self.frames = []
        for data_file in dataFiles:
            self.frames.append(TwoDDataset(data_file, poni,mask))
            self._header += '#{}\n'.format(data_file)
        
    
    def _init_parameters(self,dataFiles, poni, mask, time, thickness, CF, sample_name, darkCurrent,dcError):
        self._header = ('#Sample: {}\n'.format(sample_name)+
                    	'#Data Reduction performed at: {}\n'.format(datetime.now())+
                        '#Working Directory: {}\n'.format(os.getcwd())+
                        '#Data Files:\n')
        self._load_frames(dataFiles,poni,mask)
        self._header += '#Poni File: {}\n'.format(poni)
        self.poni = poni
        self._header += '#Mask File: {}\n'.format(mask)
        self.mask = mask
        with open(poni, 'r') as poni_file:
            for line in poni_file:
                self._header += '#{}\n'.format(line.strip())
        self.sample = sample_name
        self.times = self._set_calib_parameter("Measurement time", time)
        self.thickness = self._set_calib_parameter("Thickness", thickness)
        self.cf = self._set_calib_parameter("Calibration factor", CF)
        self.darkCurrent = self._set_calib_parameter("Dark current", darkCurrent)
        self.dcError = self._set_calib_parameter("Dark current error", dcError)
        self.transmission = None
        self._oneDDataSet = None
        
        self._header += ('#Mask File: {}\n'.format(mask)+
                         '#Counting Time per frame[s]: {}\n'.format(list(self.times))+
                         '#Sample Thickness [cm]: {}\n'.format(list(self.thickness))+
                         '#Calibration Factor: {}\n'.format(list(self.cf))+
                         '#Dark Current [cts/s/px]: {}+-{}\n'.format(list(self.darkCurrent),list(self.dcError)))
        
    def __init__(self,sample_name, dataFiles, transmissionFile, transmission_time, directBeamFile, time, thickness, CF, poni,
                 darkCurrent=6.275e-5,dcError=0.010431667, mask=None, header='', DB=False):
        self._header = header
        self._init_parameters(dataFiles, poni, mask, time, thickness, CF, sample_name, darkCurrent,dcError)
        self._header += '#Direct Beam File: {}\n'.format(directBeamFile)
        
        tf = self.create_transmission(transmissionFile)
        
        self.transmission = Transmission(directBeamFile, tf, mask, poni)
        self.transmission_counts = self.transmission.tm_counts()/transmission_time
        self.dbIntensity = TwoDDataset(directBeamFile, poni, mask).calculateSum()
        self.DB = DB
        
        self._header += '#Direct Beam Intensity[cts]: {}\n'.format(self.dbIntensity)
        self._header += '#Direct Beam Intensity[cts]: {}\n'.format(self.transmission.db_counts())
        self._header += '#Transmission Measurement Intensity[cts]: {}\n'.format(self.transmission.tm_counts())
        self._header += '#Transmission: {}\n'.format(self.transmission.transmission())
        
        self.reduceData()
    
    def create_transmission(self,transmissionFile):
        
        result = None
        self._header += '#Transmission Measurement Files:\n'
        for i, file in enumerate(transmissionFile):
            self._header += '#\t{}\n'.format(file)
            if i == 0:
                result = TwoDDataset(file, self.poni,self.mask)
            else:
                result = result.add(TwoDDataset(file, self.poni,self.mask))

        return result

    
    def reduceData(self):
        totalSumImage = None
        
        self._header += ('#Reduction Steps:\n'+
                         '#For each Frame frame: (frame-darkCurrent)*calibractionFactor/(measurement time*thickness*transmission counts per second)\n'+
                         '#Sum up all frames, divide by number of frames\n'+
                         '#Integrate with pyFAI using poni File\n')
        print(self.sample)
        scattering_intensity_first_frame = 1
        for i, frame in enumerate(self.frames):
            
            scattering_intensity = frame.scatteringIntensity()
            print(scattering_intensity)
            calibFactor = self.cf[i]/(self.times[i]*self.thickness[i]*self.transmission_counts)
            frameDC = self.times[i]*self.darkCurrent[i]
            frameDCerror = np.sqrt(self.times[i])*self.darkCurrent[i]
            tempFrame = (frame.sub(frameDC,frameDCerror)).mul(calibFactor)
            # tempFrame.direct_beam()
            if i == 0:
                scattering_intensity_first_frame=scattering_intensity
                totalSumImage = tempFrame
            else:
                # print(scattering_intensity_first_frame/scattering_intensity)
                tempFrame = tempFrame.mul(scattering_intensity_first_frame/scattering_intensity)
                totalSumImage = totalSumImage.add(tempFrame)
        
        totalSumImage = totalSumImage.mul(1/len(self.frames))
        if self.DB == True:
            self._header += '#Changed DB position in Poni. New Poni now:\n'
            (x,y),(sigx,sigy) = totalSumImage.direct_beam()
            with open("./temp.poni", 'w') as tempponi:
                with open(self.poni, 'r') as initial_poni:
                    for line in initial_poni:
                        if line.startswith('Poni1'):
                            print(line)
                            newline = 'Poni1: {}\n'.format(y*0.000172)
                            print(newline)
                            self._header += "#{}".format(newline)
                            tempponi.write(newline)
                        elif line.startswith('Poni2'):
                            print(line)
                            newline = 'Poni2: {}\n'.format(x*0.000172)
                            self._header += "#{}".format(newline)
                            print(newline)
                            tempponi.write(newline)
                        else:
                            tempponi.write(line)
                            self._header += "#{}".format(line)
            totalSumImage.change_poni("./temp.poni")
            
        self._oneDDataSet = OneDDataSet(totalSumImage.integrateImage(), self.sample, header=self._header)
        
    def getOneD(self):
        if type(self._oneDDataSet) == None:
            raise AttributeError('Data not yet reduced.')
        else:
            return self._oneDDataSet

class DataReductionMachine():
    pass        

def load_data(fn):
    
    x=[]
    y=[]
    
    with open(fn,'r') as infile:
        for line in infile:
            if not line.startswith('#'):
                data = line.split()
                x.append(float(data[0]))
                y.append(float(data[1]))
                
    return x,y

def create_filenames(start,stop):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = r"./rawdata/latest_{:07d}_craw.tiff".format(i)
        result.append(filename)
        
    return result
     
def main():
    pass
    
if __name__ == '__main__':
    main()