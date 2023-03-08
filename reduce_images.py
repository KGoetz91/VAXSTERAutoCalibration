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

import os

def linear_function(x, m, b):
    return m*x+b

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
    eq_ind = np.where(x1==x)
    if len(eq_ind[0]) == 1:
      y2.append(y1[eq_ind[0][0]])
      e2.append(e1[eq_ind[0][0]])
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

class Transmission:
    
    def __init__(self,DB,data,mask,poni):
        self.DBImage = TwoDDataset(DB, poni,mask)
        self.transmissionImage = TwoDDataset(data, poni,mask)
        
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
        
    def plotImage(self):
        plt.clf()
        plt.imshow(np.log10(self.imageData))
        plt.show()
        
    def plotMask(self):
        if type(self.mask)!=None:
            plt.imshow(self.mask)
        
    def calculateSum(self):
        if type(self.mask) != None:
            inverseMask = np.where(self.mask == 0, 1,0)
            sumImage = np.multiply(inverseMask, self.imageData).flatten()
            #sumImage = sumImage[sumImage != 0]
            #imageSize = sumImage.size
        else:
            sumImage = sumImage[sumImage >= 0]
        imageSum = np.sum(sumImage)
        return imageSum
    
    def integrateImage(self, bins=425):
        if type(self.mask)!=None:
            result = self.integrator.integrate1d_ng(self.imageData,npt = bins, mask=self.mask,
                                                    correctSolidAngle=True, unit = "q_nm^-1",
                                                    variance=np.power(self.errorData,2))
        else:
            result = self.integrator.integrate1d_ng(self.imageData,npt = bins, correctSolidAngle=True,
                                                    unit = "q_nm^-1",variance=np.power(self.errorData,2))
        return result

class OneDDataSet:
    
    def __mul__(self,value):
        if isinstance(value,Number):
            self._header += "#Arithmetic operation multiplication: {}*{}\n".format(self.name, value)
            self.y = self.y*value
            return self
        else:
            raise ValueError('Only numbers are possible.')
    
    def spline(self,x1,y1,x2,y2):
        
        x_min = max(min(x1),min(x2))
        x_max = min(max(x1),max(x2))
        
        y1_new = np.where(x1 > x_min, y1, None)
        y1_new = np.where(x1 < x_max, y1_new, None)
        y1_new = y1_new[y1_new != None]
        x1_new = x1[x1>x_min]
        x1_new = x1_new[x1_new<x_max]
        
        y_spline = []
        
        x_spline, y_spline, e_spline = spline_data(x1_new,[x2,y2,y2])
        
        return x_spline,y1_new,y_spline
    
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
        if type(secondDataset)==OneDDataSet:
            self._header += "#Arithmetic operation subtraction: {}-{}\n".format(self.name, secondDataset.name)
            x1 = self.x
            y1 = self.y
            
            x2 = secondDataset.x
            y2 = secondDataset.y
            
            xspline,y3,y4 = self.spline(x1,y1,x2,y2)
            self.y = np.subtract(y3,y4)
            self.x = xspline
            
        elif isinstance(secondDataset, Number):
            self._header += "#Arithmetic operation subtraction: {}-{}\n".format(self.name, secondDataset)
            self.y = self.y-secondDataset
        else:
            raise ValueError('Subtraction only defined for numbers and other 1D-Datasets')
        return self
    
    def __init__(self, pyFAIIntegratorResult, name, header=''):
        self._header = header
        self.name = name
        self.completeData = pyFAIIntegratorResult
        self.x = np.array(pyFAIIntegratorResult[0])
        self.y = np.array(pyFAIIntegratorResult[1])
        self.error = np.array(pyFAIIntegratorResult[2])

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
       
    
    def _init_parameters(self,dataFiles, poni, mask, time, thickness, CF, sample_name, darkCurrent,dcError):
        self._header = ('#Sample: {}\n'.format(sample_name)+
                    	'#Data Reduction performed at: {}\n'.format(datetime.now())+
                        '#Working Directory: {}\n'.format(os.getcwd())+
                        '#Data Files:\n')
        self.frames = []
        for data_file in dataFiles:
            self.frames.append(TwoDDataset(data_file, poni,mask))
            self._header += '#{}\n'.format(data_file)
        self._header += '#Poni File: {}\n'.format(poni)
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
        
    def __init__(self,sample_name, dataFiles, transmissionFile, directBeamFile, time, thickness, CF, poni,
                 darkCurrent=6.275e-5,dcError=0.010431667, mask=None, header=''):
        self._header = header
        self._init_parameters(dataFiles, poni, mask, time, thickness, CF, sample_name, darkCurrent,dcError)
        self._header += '#Direct Beam File: {}\n'.format(directBeamFile)
        self._header += '#Transmission Measurement File: {}\n'.format(transmissionFile)
        
        self.transmission = Transmission(directBeamFile, transmissionFile, mask, poni).transmission()
        self.dbIntensity = TwoDDataset(directBeamFile, poni, mask).calculateSum()
        
        self._header += '#Direct Beam Intensity[cts]: {}\n'.format(self.dbIntensity)
        self._header += '#Transmission: {}\n'.format(self.transmission)
        
        self.reduceData()
        
    def reduceData(self):
        totalSumImage = None
        
        self._header += ('#Reduction Steps:\n'+
                         '#For each Frame frame: (frame-darkCurrent)*calibractionFactor/(measurement time*directBeamIntensity*thickness*transmission)\n'+
                         '#Sum up all frames, divide by number of frames\n'+
                         '#Integrate with pyFAI using poni File\n')
        
        for i, frame in enumerate(self.frames):
            calibFactor = self.cf[i]/(self.dbIntensity*self.times[i]*self.thickness[i]*self.transmission)
            frameDC = self.times[i]*self.darkCurrent[i]
            frameDCerror = np.sqrt(self.times[i])*self.darkCurrent[i]
            tempFrame = (frame.sub(frameDC,frameDCerror)).mul(calibFactor)
            if i == 0:
                totalSumImage = tempFrame
            else:
                totalSumImage = totalSumImage.add(tempFrame)
        
        totalSumImage = totalSumImage.mul(1/len(self.frames))
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

    plt.clf()
    
    calib_dir = "calibrated"
    calib_noBG_dir = "calibrated_noBG"
    
    if not os.path.isdir(calib_dir):
        os.makedirs(calib_dir)
    if not os.path.isdir(calib_noBG_dir):
        os.makedirs(calib_noBG_dir)

    #GC SAXS
    data_files = create_filenames(88183, 88183)
    TM_file = r"./rawdata/latest_0088182_craw.tiff"
    DB_file = r"./rawdata/latest_0088191_craw.tiff"
    
                                               #time  d   CF      poni       mask
    ds = TwoDReducer("GC SAXS", data_files,TM_file,DB_file,300, 0.1, 4.25e6, "./GC_saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC SAXS measured") 

    #GC WAXS
    data_files = create_filenames(88190, 88190)
    TM_file = r"./rawdata/latest_0088189_craw.tiff"
    DB_file = r"./rawdata/latest_0088188_craw.tiff"
    
                                               #time  d   CF      poni       mask
    ds = TwoDReducer("GC WAXS", data_files,TM_file,DB_file,60, 0.1, 5e4, "./GC_waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC WAXS measured") 

    #GC APS 
    # x,y = load_data(r"./GC_APS.dat")
    # plt.loglog(x,y,label="GC APS") 
    # plt.xlim([2e-1,3])
    # plt.ylim([5,40])
    # plt.legend()
    # plt.show()

    #Ref mit Zucker SAXS
    data_files = create_filenames(88248, 88259)
    TM_file = r"./rawdata/latest_0088247_craw.tiff"
    DB_file = r"./rawdata/latest_0088191_craw.tiff"
    
                                                                        #time  d   CF      poni       mask
    ds = TwoDReducer("Ref mit Zucker SAXS",data_files,TM_file,DB_file,3600, 0.1, 4.25e6, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    bg_saxs = ds.getOneD()
    bg_saxs.write_data_AA(r"./calibrated/RefZucker_saxs_AA.dat")
    plt.loglog(bg_saxs.x,bg_saxs.y,label="Ref Zucker SAXS")    
    
    #Ref mit Zucker WAXS
    data_files = create_filenames(88229, 88230)
    TM_file = r"./rawdata/latest_0088228_craw.tiff"
    DB_file = r"./rawdata/latest_0088188_craw.tiff"
    
                                                #time  d   CF      poni       mask
    ds = TwoDReducer("Ref mit Zucker WAXS",data_files,TM_file,DB_file,3600, 0.1, 5e4, "./waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    bg_waxs = ds.getOneD()
    bg_waxs.write_data_AA(r"./calibrated/RefZucker_waxs_AA.dat")
    plt.loglog(bg_waxs.x,bg_waxs.y,label="Ref Zucker WAXS")  
    
    #BNT3 SAXS
    data_files = create_filenames(88213, 88224)
    TM_file = r"./rawdata/latest_0088212_craw.tiff"
    DB_file = r"./rawdata/latest_0088191_craw.tiff"
    
                                                #time  d   CF      poni       mask
    ds = TwoDReducer("BNT 3 SAXS", data_files,TM_file,DB_file,3600, 0.1, 4.25e6, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(r"./calibrated/BNT3_saxs_AA.dat")
    plt.loglog(res.x,res.y,label="BNT3 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(r"./calibrated_noBG/BNT3_saxs_noBG_AA.dat")
    plt.loglog(res.x,res.y,label="BNT3 no BG SAXS")    
    
    #BNT2 WAXS
    data_files = create_filenames(88194, 88195)
    TM_file = r"./rawdata/latest_0088193_craw.tiff"
    DB_file = r"./rawdata/latest_0088188_craw.tiff"
    
                                                #time  d   CF      poni       mask
    ds = TwoDReducer("BNT 2 WAXS", data_files,TM_file,DB_file,3600, 0.1, 5e4, "./waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(r"./calibrated/BNT2_waxs_AA.dat")
    plt.loglog(res.x,res.y,label="BNT2 WAXS")    
    res = res-bg_waxs
    res.write_data_AA(r"./calibrated_noBG/BNT2_waxs_noBG_AA.dat")
    plt.loglog(res.x,res.y,label="BNT2 no BG WAXS")    
    
    #BNT2 SAXS
    data_files = create_filenames(88197, 88208)
    TM_file = r"./rawdata/latest_0088196_craw.tiff"
    DB_file = r"./rawdata/latest_0088191_craw.tiff"
    
                                                #time  d   CF      poni       mask
    ds = TwoDReducer("BNT 2 SAXS", data_files,TM_file,DB_file,3600, 0.1, 4.25e6, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(r"./calibrated/BNT2_saxs_AA.dat")
    plt.loglog(res.x,res.y,label="BNT2 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(r"./calibrated_noBG/BNT2_saxs_noBG_AA.dat")
    plt.loglog(res.x,res.y,label="BNT2 no BG SAXS")    
    
    #BNT3 WAXS
    data_files = create_filenames(88210, 88211)
    TM_file = r"./rawdata/latest_0088209_craw.tiff"
    DB_file = r"./rawdata/latest_0088188_craw.tiff"
    
                                                #time  d   CF      poni       mask
    ds = TwoDReducer("BNT 3 WAXS", data_files,TM_file,DB_file,3600, 0.1, 5e4, "./waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(r"./calibrated/BNT3_waxs_AA.dat")
    plt.loglog(res.x,res.y,label="BNT3 WAXS")    
    res = res-bg_waxs
    res.write_data_AA(r"./calibrated_noBG/BNT3_waxs_noBG_AA.dat")
    plt.loglog(res.x,res.y,label="BNT3 no BG WAXS")   
    
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()