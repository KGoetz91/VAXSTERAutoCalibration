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
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated_noBG"
    
    if not isdir(calib_path):
        makedirs(calib_path)
    if not isdir(calib_noBG_path):
        makedirs(calib_noBG_path)

    # #GC SAXS
    # data_files = create_filenames(89036, 89036,datapath)
    # TM_file = create_filenames(89035,89035,datapath)[0]
    # DB_file = create_filenames(89034,89034,datapath)[0]
    
    # #                                                     TM time     time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("GC SAXS", data_files,TM_file,60,DB_file,300, 0.1, 7.1e4, join(ponipath,"GC_poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    # res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC SAXS measured") 

    # #GC APS 
    # x,y = load_data(r"./GC_APS.dat")
    # plt.loglog(x,y,label="GC APS") 
    # plt.xlim([0.9e-1,3])
    # plt.ylim([5,110])


    #Ref mit Zucker SAXS
    data_files = create_filenames(89214, 89225,datapath)
    TM_file = create_filenames(89213,89213,datapath)[0]
    DB_file = create_filenames(89212,89212,datapath)[0]
    
                                                                        #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("Ref mit Zucker",data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    bg_saxs = ds.getOneD()
    # bg_saxs.make_horizontal(0.0722,0.8)
    bg_saxs.write_data_AA(join(calib_path,"RefZucker_AA.dat"))
    plt.loglog(bg_saxs.x,bg_saxs.y,label="Ref Zucker")    
    
    #BNT8 SAXS
    data_files = create_filenames(89038, 89049,datapath)
    TM_file = create_filenames(89037,89037,datapath)[0]
    DB_file = create_filenames(89034,89034,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 8", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT8_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT8 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(join(calib_noBG_path,"BNT8_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT8 no BG SAXS")    

    #BNT9 SAXS
    data_files = create_filenames(89052, 89063,datapath)
    TM_file = create_filenames(89051,89051,datapath)[0]
    DB_file = create_filenames(89050,89050,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 9", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT9_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT9 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(join(calib_noBG_path,"BNT9_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT9 no BG SAXS")    

    #BNT10 SAXS
    data_files = create_filenames(89099, 89110,datapath)
    TM_file = create_filenames(89098,89098,datapath)[0]
    DB_file = create_filenames(89111,89111,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 10", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT10_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT10 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(join(calib_noBG_path,"BNT10_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT10 no BG SAXS")    

    plt.legend()
    plt.show()

if __name__ == '__main__':
    
    main()