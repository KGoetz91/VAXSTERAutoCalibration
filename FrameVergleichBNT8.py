# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:53:31 2023

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
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated_frames"

    ponipath2 ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910"
    datapath2 = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/rawdata"
    calib_path2 = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated_frames"
    
    if not isdir(calib_path):
        makedirs(calib_path)
    if not isdir(calib_path2):
        makedirs(calib_path2)
        
    TM_file1=
    TM_file2=
    DB_file=89692    
    Data1_start=
    Data1_end=
    Data2_start=
    Data2_end
    
    for i in range(4):
        data_files = create_filenames((start+1)+(6*i), (start+1)+(6*i),datapath)
        TM_file = create_filenames(start+(6*i),start+(6*i),datapath)[0]
        DB_file = create_filenames(89692,89692,datapath)[0]
                                                    #time  d   CF      poni       mask
        ds = reducer.TwoDReducer("BNT 8 {}".format(i), data_files,TM_file,1800,DB_file,1800, 0.1, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    
        res = ds.getOneD()
        res8.append(res)
        res.write_data_AA(join(calib_path,"BNT8_frame_{}_AA.dat".format(i)))
        plt.loglog(res.x,res.y,label="BNT8 old {}".format(i))    