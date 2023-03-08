# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 12:33:13 2023

@author: klaus
"""

import reduce_images as reducer
from reduce_images import load_data
from os.path import join,isdir
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np


def create_filenames(start,stop, datapath="./"):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = join(datapath,r"latest_{:07d}_craw.tiff".format(i))
        result.append(filename)
        
    return result

def main():
    
    plt.clf()
    
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/221125_MessungBNT/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/221125_MessungBNT/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/221125_MessungBNT/calibrated_noBG"
    
    if not isdir(calib_path):
        makedirs(calib_path)
    if not isdir(calib_noBG_path):
        makedirs(calib_noBG_path)

    #GC SAXS
    data_files = create_filenames(88183, 88183,datapath)
    TM_file = r"./rawdata/latest_0088182_craw.tiff"
    DB_file = r"./rawdata/latest_0088191_craw.tiff"
    
                                               #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("GC SAXS", data_files,TM_file,DB_file,300, 0.1, 4.25e6, "./GC_saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    res = ds.getOneD()
    plt.loglog(res.x,res.y,label="GC SAXS measured") 

    #GC APS 
    x,y = load_data(r"./GC_APS.dat")
    plt.loglog(x,y,label="GC APS") 
    plt.xlim([2e-1,3])
    plt.ylim([5,40])
    plt.legend()
    plt.show()


if __name__ == '__main__':
    
    main()