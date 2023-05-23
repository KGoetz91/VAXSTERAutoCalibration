# -*- coding: utf-8 -*-
"""
Created on Fri May 12 12:23:47 2023

@author: Klaus
"""

from reduce_images import TwoDDataset, TwoDReducer, OneDDataSet

import numpy as np
from os.path import isfile

import hdf5plugin
import h5py

import os
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class ILLSAXS_TwoDDataset(TwoDDataset):

    def _load_data(self):
        if not isfile(self.inputfile):
          raise ValueError('The given file {} does not exist.'.format(self.inputfile))
        with h5py.File(self.inputfile) as f:
          data = np.rot90(f["entry0/D22/Saxs/data3"][()][:,:,0])
          # xdet = float(f['{:08d}/instrument/xdet/value'.format(number)][()])
          # time = float(f['{:08d}/instrument/det/preset'.format(number)][()])
        return data
    
    def totalTime(self):
        with h5py.File(self.inputfile) as f:
            time = float(f["entry0/D22/Saxs/measureTime"][()][0])
        return time
    
class ILLSAXS_TwoDReducer(TwoDReducer):
    
    def _load_data(self,data_file,poni, mask):
        new_frame = ILLSAXS_TwoDDataset(data_file, poni,mask)
        return new_frame
        
    def _load_frames(self,dataFiles,poni,mask):
        self.frames = []
        times = []
        image_sums = []
        for data_file in dataFiles:
            new_frame = self._load_data(data_file, poni, mask)
            self.frames.append(new_frame)
            self._header += '#{}\n'.format(data_file)
            time = new_frame.totalTime()
            image_sum = new_frame.calculateSum()
            times.append(time)
            image_sums.append(image_sum)
        self.times = self._set_calib_parameter("Measurement time", times)
        self.transmissions = self._set_calib_parameter("Transmission values", image_sums)
    
    def _init_parameters(self,dataFiles, poni, mask, thickness, CF, sample_name):
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
        self.thickness = self._set_calib_parameter("Thickness", float(thickness))
        self.cf = self._set_calib_parameter("Calibration factor", CF)

        self._oneDDataSet = None
        self._header += ('#Mask File: {}\n'.format(mask)+
                         '#Counting Time per frame[s]: {}\n'.format(list(self.times))+
                         '#Sample Thickness [cm]: {}\n'.format(list(self.thickness))+
                         '#Calibration Factor: {}\n'.format(list(self.cf)))
        
    def _init_gamma(self,gammaFiles, poni, mask):
        result = 0
        
        results = []
        
        for data_file in gammaFiles:
            gamma_frame = self._load_data(data_file, self.poni, self.mask)
            counts = gamma_frame.calculateSum()
            time = gamma_frame.totalTime()
            pixels = gamma_frame.pixels()
            results.append(counts/(time*pixels))
            
        result = np.mean(results)
        error = np.sqrt(result)  #TODO this is not really correct yet
            
        self.darkCurrent = self._set_calib_parameter("Gamma Background", float(result))
        self.dcError = self._set_calib_parameter("Gamma Background error", float(error))
        self._header += '#Dark Current [cts/s/px]: {}+-{}\n'.format(list(self.darkCurrent),list(self.dcError))
        pass
        
    def reduceData(self):
        totalSumOneD = None
        
        self._header += ('#Reduction Steps:\n'+
                         '#For each Frame frame: (frame-GammaBG)*calibractionFactor/(measurement time*thickness*total intensity counts per second)\n'+
                         '#Sum up all frames, divide by number of frames\n'+
                         '#Integrate with pyFAI using poni File\n')
        print(self.sample)
        for i, frame in enumerate(self.frames):
            
            scattering_intensity = frame.scatteringIntensity()
            print(scattering_intensity)
            calibFactor = self.cf[i]/(self.times[i]*self.thickness[i]*self.transmissions[i])
            frameDC = self.times[i]*self.darkCurrent[i]
            frameDCerror = np.sqrt(self.times[i])*self.darkCurrent[i]
            tempFrame = (frame.sub(frameDC,frameDCerror)).mul(calibFactor)
            
            plt.clf()
            plt.imshow(tempFrame.imageData,norm=LogNorm())
            plt.show()
            
            if self.DB == True:
                self._header += '#Changed DB position in Poni. New Poni now:\n'
                (x,y),(sigx,sigy) = tempFrame.direct_beam()
                with open("./temp.poni", 'w') as tempponi:
                    with open(self.poni, 'r') as initial_poni:
                        for line in initial_poni:
                            if line.startswith('Poni1'):
                                print(line)
                                newline = 'Poni1: {}\n'.format(y*0.000075)
                                print(newline)
                                self._header += "#{}".format(newline)
                                tempponi.write(newline)
                            elif line.startswith('Poni2'):
                                print(line)
                                newline = 'Poni2: {}\n'.format(x*0.000075)
                                self._header += "#{}".format(newline)
                                print(newline)
                                tempponi.write(newline)
                            else:
                                tempponi.write(line)
                                self._header += "#{}".format(line)
                tempFrame.change_poni("./temp.poni")
            
            if i == 0:
                totalSumOneD = OneDDataSet(tempFrame.integrateImage(), self.sample, header=self._header)
            else:
                totalSumOneD = totalSumOneD+OneDDataSet(tempFrame.integrateImage(), self.sample, header=self._header)
        
        totalSumOneD = totalSumOneD * (1/len(self.frames))
            
        self._oneDDataSet = totalSumOneD

        
    def __init__(self,sample_name, dataFiles, gammaFiles, thickness, CF, poni,
                 mask=None, header='', DB=False):
        self._header = header
        self._init_parameters(dataFiles, poni, mask, thickness, CF, sample_name)
        self._init_gamma(gammaFiles, poni, mask)
        
        self._header += '#Image Sums used for Transmission [cts]: {}\n'.format(self.transmissions)
        self.DB = DB
        self.reduceData()
