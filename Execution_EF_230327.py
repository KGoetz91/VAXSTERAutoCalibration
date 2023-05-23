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

    resB_EF0018 = []
    resA_EF0065 = []
    resB_EF0046 = []
    
    scat_EF18 = []
    scat_EF65 = []
    scat_EF46 = []

    for j in range(8):
        start = 90134+j*39
        for i in range(4):
            # B_EF0018
            tstart = start+3+(9*i)
            data_files = create_filenames((tstart+1), (tstart+1),datapath)
            TM_file = create_filelist([(tstart),(tstart+2)],datapath)
            DB_file = create_filelist([90130],datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("B_EF0018 {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.1086, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
            print("{}, {}, {}".format(tstart,tstart+1,tstart+2))
            res = ds.getOneD()
            if (i+4*j != 18) and (tstart+1!=90312): 
                resB_EF0018.append(res)
                plt.loglog(res.x,res.y,label="B_EF0018 {}".format(i+4*j))
                for frame in ds.frames:
                    scat_EF18.append(frame.scatteringIntensity())
                
            
            res.write_data_AA(join(calib_path,"B_EF0018_{}_AA.dat".format(i+4*j)))
            
            #A_EF0065
            tstart=tstart+3
            data_files = create_filenames((tstart+1), (tstart+1),datapath)
            TM_file = create_filelist([(tstart),(tstart+2)],datapath)
            DB_file = create_filelist([90130],datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("A_EF0065 {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.1022, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
            print("{}, {}, {}".format(tstart,tstart+1,tstart+2))
            for frame in ds.frames:
                scat_EF65.append(frame.scatteringIntensity())
            res = ds.getOneD()
            resA_EF0065.append(res)
            res.write_data_AA(join(calib_path,"A_EF0065_{}_AA.dat".format(i+4*j)))
            plt.loglog(res.x,res.y,label="A_EF0065 {}".format(i+4*j))
            
            #B_EF0046
            tstart=tstart+3
            data_files = create_filenames((tstart+1), (tstart+1),datapath)
            TM_file = create_filelist([(tstart),(tstart+2)],datapath)
            DB_file = create_filelist([90130],datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("B_EF0046 {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.0996, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
            print("{}, {}, {}".format(tstart,tstart+1,tstart+2))
            for frame in ds.frames:
                scat_EF46.append(frame.scatteringIntensity())
            res = ds.getOneD()
            resB_EF0046.append(res)
            res.write_data_AA(join(calib_path,"B_EF0046_{}_AA.dat".format(i+4*j)))
            plt.loglog(res.x,res.y,label="B_EF0046 {}".format(i+4*j))

    for i in range(len(resB_EF0018)):
        if i == 0:
            SumB_EF0018 = resB_EF0018[i]
            SumA_EF0065 = resA_EF0065[i]
            SumB_EF0046 = resB_EF0046[i]
        else:
            SumB_EF0018 += resB_EF0018[i]
            SumA_EF0065 += resA_EF0065[i]
            SumB_EF0046 += resB_EF0046[i]
    
    SumB_EF0018 = SumB_EF0018*(1/len(resB_EF0018))
    SumB_EF0018.write_data_AA(join(calib_path,"B_EF0018_Mean_AA.dat"))
    SumA_EF0065 = SumA_EF0065*(1/len(resA_EF0065))
    SumA_EF0065.write_data_AA(join(calib_path,"A_EF0065_Mean_AA.dat"))
    SumB_EF0046 = SumB_EF0046*(1/len(resB_EF0046))
    SumB_EF0046.write_data_AA(join(calib_path,"B_EF0046_Mean_AA.dat"))

    plt.plot(SumB_EF0018.x,SumB_EF0018.y, label="B_EF0018 Mean")
    plt.plot(SumA_EF0065.x,SumA_EF0065.y, label="A_EF0065 Mean")
    plt.plot(SumB_EF0046.x,SumB_EF0046.y, label="B_EF0046 Mean")

    # plt.legend()
    plt.show()
    
    plt.clf()
    
    plt.plot(scat_EF18, label="B_EF0018 Mean")
    plt.plot(scat_EF46, label="B_EF0046 Mean")
    plt.plot(scat_EF65, label="B_EF0065 Mean")

    plt.legend()
    plt.show()
if __name__ == '__main__':
    
    main()