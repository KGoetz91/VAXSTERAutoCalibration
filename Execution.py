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


def create_filenames(start,stop, datapath=".0"):
    
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
    # data_files = create_filenames(88183, 88183,datapath)
    # TM_file = create_filenames(88182,88182,datapath)[0]
    # DB_file = create_filenames(88191,88191,datapath)[0]
    
    # #                                                     TM time     time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("GC SAXS", data_files,TM_file,60,DB_file,300, 0.1, 7.1e4, "./GC_saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    # res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC SAXS measured") 

    #GC WAXS
    # data_files = create_filenames(88190, 88190,datapath)
    # TM_file = create_filenames(88189,88189,datapath)[0]
    # DB_file = create_filenames(88188,88188,datapath)[0]
    
    #                                            #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("GC WAXS", data_files,TM_file,60,DB_file,60, 0.1, 8.3e2, "./GC_waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    # res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC WAXS measured") 

    #GC APS 
    # x,y = load_data(r"./GC_APS.dat")
    # plt.loglog(x,y,label="GC APS") 
    # plt.xlim([0.9e-1,3])
    # plt.ylim([5,110])
    # plt.legend()
    # plt.show()

    #Ref mit Zucker SAXS
    data_files = create_filenames(88248, 88259,datapath)
    TM_file = create_filenames(88247,88247,datapath)[0]
    DB_file = create_filenames(88191,88191,datapath)[0]
    
                                                                        #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("Ref mit Zucker SAXS",data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    bg_saxs = ds.getOneD()
    # bg_saxs.make_horizontal(0.0722,0.8)
    bg_saxs.write_data_AA(join(calib_path,"RefZucker_saxs_AA.dat"))
    plt.loglog(bg_saxs.x,bg_saxs.y,label="Ref Zucker SAXS")    
    
    # #Ref mit Zucker WAXS
    # data_files = create_filenames(88229, 88230,datapath)
    # TM_file = create_filenames(88228,88228,datapath)[0]
    # DB_file = create_filenames(88188,88188,datapath)[0]
    
    #                                             #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("Ref mit Zucker WAXS",data_files,TM_file,60,DB_file,3600, 0.1, 8.3e2, "./waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=0)

    # bg_waxs = ds.getOneD()
    # bg_waxs.write_data_AA(join(calib_path,"RefZucker_waxs_AA.dat"))
    # plt.loglog(bg_waxs.x,bg_waxs.y,label="Ref Zucker WAXS")  

    #BNT2 WAXS
    # data_files = create_filenames(88194, 88195,datapath)
    # TM_file = create_filenames(88193,88193,datapath)[0]
    # DB_file = create_filenames(88188,88188,datapath)[0]
    
    #                                             #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("BNT 2 WAXS", data_files,TM_file,60,DB_file,3600, 0.1, 8.3e2, "./waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    # res = ds.getOneD()
    # res.write_data_AA(join(calib_path,"BNT2_waxs_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT2 WAXS")    
    # res = res-bg_waxs
    # res.write_data_AA(join(calib_noBG_path,"BNT2_waxs_noBG_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT2 no BG WAXS")    
    
    #BNT2 SAXS
    data_files = create_filenames(88197, 88208,datapath)
    TM_file = create_filenames(88196,88196,datapath)[0]
    DB_file = create_filenames(88191,88191,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 2 SAXS", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT2_saxs_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT2 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(join(calib_noBG_path,"BNT2_saxs_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT2 no BG SAXS")    

    #BNT3 SAXS
    data_files = create_filenames(88213, 88224,datapath)
    TM_file = create_filenames(88212,88212,datapath)[0]
    DB_file = create_filenames(88191,88191,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 3 SAXS", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, "./saxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT3_saxs_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT3 SAXS")    
    res = res-bg_saxs
    res.write_data_AA(join(calib_noBG_path,"BNT3_saxs_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT3 no BG SAXS")    
    
    #BNT3 WAXS
    # data_files = create_filenames(88210, 88211,datapath)
    # TM_file = create_filenames(88209,88209,datapath)[0]
    # DB_file = create_filenames(88188,88188,datapath)[0]
    
    #                                             #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("BNT 3 WAXS", data_files,TM_file,60,DB_file,3600, 0.1, 8.3e2, "./waxs_poni.poni", mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    # res = ds.getOneD()
    # res.write_data_AA(join(calib_path,"BNT3_waxs_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT3 WAXS")    
    # res = res-bg_waxs
    # res.write_data_AA(join(calib_noBG_path,"BNT3_waxs_noBG_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT3 no BG WAXS")   

    plt.legend()
    plt.show()

if __name__ == '__main__':
    
    main()