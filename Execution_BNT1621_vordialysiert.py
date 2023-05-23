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
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230220_BNT1621_vorDialyse"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230220_BNT1621_vorDialyse/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230220_BNT1621_vorDialyse/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230220_BNT1621_vorDialyse/calibrated_noBG"
    
    if not isdir(calib_path):
        makedirs(calib_path)
    if not isdir(calib_noBG_path):
        makedirs(calib_noBG_path)

    # #GC SAXS
    # data_files = create_filenames(89694, 89694,datapath)
    # TM_file = create_filenames(89693,89693,datapath)[0]
    # DB_file = create_filenames(89692,89692,datapath)[0]
    
    # #                                                     TM time     time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("GC SAXS", data_files,TM_file,60,DB_file,300, 0.1, 7.1e4, join(ponipath,"GC_poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    # res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC SAXS measured") 

    # #GC APS 
    # x,y = load_data(r"./GC_APS.dat")
    # plt.loglog(x,y,label="GC APS") 
    # plt.xlim([0.9e-1,3])
    # plt.ylim([5,110])


    #Referenz
    data_files = create_filenames(89214, 89225,datapath)
    TM_file = create_filenames(89213,89213,datapath)
    DB_file = create_filenames(89212,89212,datapath)[0]
    
                                                                        #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("Ref mit Zucker",data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    bg = ds.getOneD()
    # bg_saxs.make_horizontal(0.0722,0.8)
    bg.write_data_AA(join(calib_path,"RefZucker_AA.dat"))
    plt.loglog(bg.x,bg.y,label="Ref Zucker")    

    #BNT16 SAXS
    data_files = create_filenames(89113, 89124,datapath)
    TM_file = create_filenames(89112,89112,datapath)
    DB_file = create_filenames(89111,89111,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 16 vor Dialyse", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT16_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT 16 vor Dialyse")    
    res = res-bg
    res.write_data_AA(join(calib_noBG_path,"BNT16_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT16 no BG")    

    #BNT21 SAXS
    data_files = create_filenames(89128, 89139,datapath)
    TM_file = create_filenames(89127,89127,datapath)
    DB_file = create_filenames(89126,89126,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 21 vor Dialyse", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res = res*1.07
    res.write_data_AA(join(calib_path,"BNT21_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT 21 vor Dialyse")    
    res = res-bg
    res.write_data_AA(join(calib_noBG_path,"BNT21_noBG_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT21 no BG") 
    
    plt.legend()
    plt.show()

if __name__ == '__main__':
    
    main()