# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:00:05 2023

@author: klaus
"""

import reduce_images as reducer
from reduce_images import load_data, TwoDDataset
from os.path import join,isdir
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np


def create_filenames(file,frame, datapath="./"):
    
    #fr_0089623_00232.tiff
    filename = join(datapath,r"fr_{:07d}_{:05d}.tiff".format(file,frame))
    return filename

def main():
    
    plt.clf()
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/frames"
    
    time = []
    intensities = []
    
    scattered_intensity = 0
    
    #BNT8 SAXS
    for data_file in range(89623, 89634+1):
        print("File: {}\n".format(data_file))
        for frame in range(240):
            print("Frame: {}".format(frame))
            dataset = TwoDDataset(create_filenames(data_file,frame,datapath),
                                  join(ponipath,"poni.poni"), join(ponipath,"mask_pyFAI.edf"))
            scattered_intensity += dataset.scatteringIntensity()
            if frame%20 == 0:
                time.append(((data_file-89623)*60)+frame/4)
            elif frame%20 == 19:
                intensities.append(scattered_intensity)
                scattered_intensity = 0
                
    
    with open(join(datapath,"BNT8scatteredIntensity.dat"),'w') as outputfile:
        for x,y in zip(time,intensities):
            outputfile.write("{}\t{}\n".format(x,y))
    
    plt.plot(time,intensities, label="BNT8")

    start_time = time[-1]
    time = []
    intensities = []

    #BNT10 SAXS
    startfile =89651
    endfile = 89662
    for data_file in range(startfile, endfile+1):
        print("File: {}\n".format(data_file))
        for frame in range(240):
            print("Frame: {}".format(frame))
            dataset = TwoDDataset(create_filenames(data_file,frame,datapath),
                                  join(ponipath,"poni.poni"), join(ponipath,"mask_pyFAI.edf"))
            scattered_intensity += dataset.scatteringIntensity()
            if frame%20 == 0:
                time.append(((data_file-startfile)*60)+start_time+frame/4)
            elif frame%20 == 19:
                intensities.append(scattered_intensity)
                scattered_intensity = 0
                
    
    with open(join(datapath,"BNT10scatteredIntensity.dat"),'w') as outputfile:
        for x,y in zip(time,intensities):
            outputfile.write("{}\t{}\n".format(x,y))
    
    plt.plot(time,intensities, label="BNT10")

    start_time = time[-1]    
    time = []
    intensities = []

    #Ref Zucker 1
    startfile =89665
    endfile = 89676
    for data_file in range(startfile, endfile+1):
        print("File: {}\n".format(data_file))
        for frame in range(240):
            print("Frame: {}".format(frame))
            dataset = TwoDDataset(create_filenames(data_file,frame,datapath),
                                  join(ponipath,"poni.poni"), join(ponipath,"mask_pyFAI.edf"))
            scattered_intensity += dataset.scatteringIntensity()
            if frame%20 == 0:
                time.append(((data_file-startfile)*60)+start_time+frame/4)
            elif frame%20 == 19:
                intensities.append(scattered_intensity)
                scattered_intensity = 0
                
    
    with open(join(datapath,"RefZucker1scatteredIntensity.dat"),'w') as outputfile:
        for x,y in zip(time,intensities):
            outputfile.write("{}\t{}\n".format(x,y))
    
    plt.plot(time,intensities, label="Ref Zucker 1")

    start_time = time[-1]  
    time = []
    intensities = []

    #Ref Zucker 2
    startfile =89679
    endfile = 89690
    for data_file in range(startfile, endfile+1):
        print("File: {}\n".format(data_file))
        for frame in range(240):
            print("Frame: {}".format(frame))
            dataset = TwoDDataset(create_filenames(data_file,frame,datapath),
                                  join(ponipath,"poni.poni"), join(ponipath,"mask_pyFAI.edf"))
            scattered_intensity += dataset.scatteringIntensity()
            if frame%20 == 0:
                time.append(((data_file-startfile)*60)+start_time+frame/4)
            elif frame%20 == 19:
                intensities.append(scattered_intensity)
                scattered_intensity = 0
                
    
    with open(join(datapath,"RefZucker2scatteredIntensity.dat"),'w') as outputfile:
        for x,y in zip(time,intensities):
            outputfile.write("{}\t{}\n".format(x,y))
    
    plt.plot(time,intensities, label="Ref Zucker 2")

    plt.legend()
    plt.show()
                

if __name__ == '__main__':
    
    main()