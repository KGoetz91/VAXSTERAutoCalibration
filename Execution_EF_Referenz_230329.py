# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 12:33:13 2023

@author: klaus
"""

import reduce_images as reducer
from reduce_images import load_data,CapillaryScan
from os.path import join,isdir
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np

def create_filelist(flist, datapath="./"):
    
    result=[]
    
    for i in flist:
        filename = join(datapath,r"latest_{:07d}_craw.tiff".format(i))
        result.append(filename)
        
    return result

def create_filenames(start,stop, datapath="./"):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = join(datapath,r"latest_{:07d}_craw.tiff".format(i))
        result.append(filename)
        
    return result

def main():
    
    plt.clf()
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated_noBG"
    
    if not isdir(calib_path):
        makedirs(calib_path)
    if not isdir(calib_noBG_path):
        makedirs(calib_noBG_path)

    # #GC SAXS
    # data_files = create_filenames(89707, 89707,datapath)
    # TM_file = create_filenames(89706,89760,datapath)[0]
    # DB_file = create_filenames(89692,89692,datapath)[0]
    
    # #                                                     TM time     time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("GC", data_files,TM_file,1800,DB_file,1800, 0.1, 7.1e4, join(ponipath,"GC_poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    # res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC measured") 

    # #GC APS 
    # x,y = load_data(r"./GC_APS.dat")
    # plt.loglog(x,y,label="GC APS") 
    # plt.xlim([0.9e-1,3])
    # plt.ylim([5,110])

    resRef = []

    for j in range(6):
        start = 90473+j*12
        for i in range(4):
            # Referenz
            tstart = start+3+(2*i)
            data_files = create_filenames((tstart+1), (tstart+1),datapath)
            TM_file = create_filelist([(tstart),(tstart+2)],datapath)
            DB_file = create_filelist([90130],datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("Referenz {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.1086, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
            print("{}, {}, {}".format(tstart,tstart+1,tstart+2))
            res = ds.getOneD()
            resRef.append(res)
            res.write_data_AA(join(calib_path,"Referenz_{}_AA.dat".format(i+4*j)))
            plt.loglog(res.x,res.y,label="Referenz {}".format(i+4*j))
            
    for i in range(len(resRef)):
        if i == 0:
            SumRef = resRef[i]
        else:
            SumRef += resRef[i]
    
    SumRef = SumRef*(1/len(resRef))
    SumRef.write_data_AA(join(calib_path,"Referenz_Mean_AA.dat"))

    plt.plot(SumRef.x,SumRef.y, label="Referenz Mean")

    plt.legend()
    plt.show()

if __name__ == '__main__':
    
    main()