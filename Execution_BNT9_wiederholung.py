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
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated_noBG"
    
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


    # #Pos 4: Ref mit Zucker SAXS
    # data_files = create_filenames(89665, 89676,datapath)
    # TM_file = create_filenames(89664,89664,datapath)[0]
    # DB_file = create_filenames(89663,89663,datapath)[0]
    
    #                                                                     #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("Ref mit Zucker, Position 4",data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    # bg_1 = ds.getOneD()
    # # bg_saxs.make_horizontal(0.0722,0.8)
    # bg_1.write_data_AA(join(calib_path,"RefZucker_Pos4_AA.dat"))
    # plt.loglog(bg_1.x,bg_1.y,label="Ref Zucker Pos. 4")    

    # #Pos 5: Ref mit Zucker SAXS
    # data_files = create_filenames(89679, 89690,datapath)
    # TM_file = create_filenames(89678,89678,datapath)[0]
    # DB_file = create_filenames(89677,89677,datapath)[0]
    
    #                                                                     #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("Ref mit Zucker, Position 5",data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    # bg_2 = ds.getOneD()
    # # bg_saxs.make_horizontal(0.0722,0.8)
    # bg_2.write_data_AA(join(calib_path,"RefZucker_Pos5_AA.dat"))
    # plt.loglog(bg_2.x,bg_2.y,label="Ref Zucker Pos. 5")  
    
    #BNT8 SAXS
    data_files = create_filenames(89705, 89705,datapath)
    TM_file = create_filenames(89622,89622,datapath)[0]
    DB_file = create_filenames(89621,89621,datapath)[0]
    
                                                #time  d   CF      poni       mask
    ds = reducer.TwoDReducer("BNT 8", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    res = ds.getOneD()
    res.write_data_AA(join(calib_path,"BNT8_offset_AA.dat"))
    plt.loglog(res.x,res.y,label="BNT8 SAXS")    
    # res = res-bg_saxs
    # res.write_data_AA(join(calib_noBG_path,"BNT8_noBG_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT8 no BG SAXS")    

    # #BNT9 SAXS
    # data_files = create_filenames(89637, 89648,datapath)
    # TM_file = create_filenames(89636,89636,datapath)[0]
    # DB_file = create_filenames(89635,89635,datapath)[0]
    
    #                                             #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("BNT 9", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    # res = ds.getOneD()
    # res.write_data_AA(join(calib_path,"BNT9_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT9 SAXS")    
    # # res = res-bg_saxs
    # # res.write_data_AA(join(calib_noBG_path,"BNT9_noBG_AA.dat"))
    # # plt.loglog(res.x,res.y,label="BNT9 no BG SAXS")    

    # #BNT10 SAXS
    # data_files = create_filenames(89651, 89662,datapath)
    # TM_file = create_filenames(89650,89650,datapath)[0]
    # DB_file = create_filenames(89649,89649,datapath)[0]
    
    #                                             #time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("BNT 10", data_files,TM_file,60,DB_file,3600, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)

    # res = ds.getOneD()
    # res.write_data_AA(join(calib_path,"BNT10_AA.dat"))
    # plt.loglog(res.x,res.y,label="BNT10 SAXS")    
    # # res = res-bg_saxs
    # # res.write_data_AA(join(calib_noBG_path,"BNT10_noBG_AA.dat"))
    # # plt.loglog(res.x,res.y,label="BNT10 no BG SAXS")    

    plt.legend()
    plt.show()

if __name__ == '__main__':
    
    main()