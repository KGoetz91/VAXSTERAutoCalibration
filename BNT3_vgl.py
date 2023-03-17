# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 17:12:16 2023

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

    #BNT3 SAXS
    for i in range(88213,88225):
        data_files = create_filenames(i, i,datapath)
        TM_file = create_filenames(88212,88212,datapath)[0]
        DB_file = create_filenames(88191,88191,datapath)[0]
        
                                                    #time  d   CF      poni       mask
        ds = reducer.TwoDReducer("BNT 3 SAXS", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=0)
    
        res = ds.getOneD()
        plt.loglog(res.x,res.y,label="BNT3 SAXS",color="green")  

    #BNT2 SAXS
    for i in range(88197, 88208):
        data_files = create_filenames(i, i,datapath)
        TM_file = create_filenames(88196,88196,datapath)[0]
        DB_file = create_filenames(88191,88191,datapath)[0]
        
                                                    #time  d   CF      poni       mask
        ds = reducer.TwoDReducer("BNT 2 SAXS", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=0)
    
        res = ds.getOneD()
        plt.loglog(res.x,res.y,label="BNT2 SAXS",color="red")         

    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    
    main()