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


def create_filenames(start,stop, datapath="./"):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = join(datapath,r"latest_{:07d}_craw.tiff".format(i))
        result.append(filename)
        
    return result

def main():
    
    plt.clf()
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated_noBG"
    
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

    res8 = []
    res10 = []
    resRef = []

    # #BNT 8 Capillary
    # bnt8_cap=CapillaryScan(680, join(ponipath,'vaxster_20220920.log'))
    # thick8 = float(bnt8_cap.cap_thickness()/10)
    # #BNT 9 Capillary
    # bnt9_cap=CapillaryScan(681, join(ponipath,'vaxster_20220920.log'))
    # thick9 = float(bnt9_cap.cap_thickness()/10)
    # #BNT 10 Capillary
    # bnt10_cap=CapillaryScan(682, join(ponipath,'vaxster_20220920.log'))
    # thick10 = float(bnt10_cap.cap_thickness()/10)
    # #Ref1 Capillary
    # ref1_cap=CapillaryScan(683, join(ponipath,'vaxster_20220920.log'))
    # ref1 = float(ref1_cap.cap_thickness()/10)
    # #Ref2 Capillary
    # ref2_cap=CapillaryScan(684, join(ponipath,'vaxster_20220920.log'))
    # ref2 = float(ref2_cap.cap_thickness()/10)

    #BNT8
    for j in range(5):
        print(j)
        start = 89708+j*26
        if j == 4:
            stuff = range(3)
        else:
            stuff = range(4)
        for i in stuff:
            data_files = create_filenames((start+1)+(6*i), (start+1)+(6*i),datapath)
            print(data_files)
            TM_file = create_filenames(start+(6*i),start+(6*i),datapath)
            DB_file = create_filenames(89692,89692,datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("BNT 8 {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.1151938, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
        
            res = ds.getOneD()
            res8.append(res)
            res.write_data_AA(join(calib_path,"BNT8_{}_AA.dat".format(i+4*j)))
            plt.loglog(res.x,res.y,label="BNT8 {}".format(i+4*j))
            
            tstart=start+2
            data_files = create_filenames((tstart+1)+(6*i), (tstart+1)+(6*i),datapath)
            print(data_files)
            TM_file = create_filenames((tstart)+(6*i),tstart+(6*i),datapath)
            DB_file = create_filenames(89692,89692,datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("BNT 10 {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.107581, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
        
            res = ds.getOneD()
            res10.append(res)
            res.write_data_AA(join(calib_path,"BNT10_{}_AA.dat".format(i+4*j)))
            plt.loglog(res.x,res.y,label="BNT10 {}".format(i+4*j))
            
            tstart=start+4
            data_files = create_filenames((tstart+1)+(6*i), (tstart+1)+(6*i),datapath)
            print(data_files)
            TM_file = create_filenames((tstart)+(6*i),tstart+(6*i),datapath)
            DB_file = create_filenames(89692,89692,datapath)[0]
                                                        #time  d   CF      poni       mask
            ds = reducer.TwoDReducer("Ref1 Pos4 {}".format(i+4*j), data_files,TM_file,1800,DB_file,1800, 0.0989530, 7.1e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
        
            res = ds.getOneD()
            resRef.append(res)
            res.write_data_AA(join(calib_path,"Ref1_Pos4_{}_AA.dat".format(i+4*j)))
            plt.loglog(res.x,res.y,label="Ref1 Pos4 {}".format(i+4*j))

    for i in range(len(res8)):
        if i == 0:
            Sum8 = res8[i]
            Sum10 = res10[i]
            SumRef = resRef[i]
        else:
            Sum8 = Sum8+res8[i]
            Sum10 = Sum10+res10[i]
            SumRef = SumRef+resRef[i]
    
    Sum8 = Sum8*(1/len(res8))
    Sum8.write_data_AA(join(calib_path,"BNT8_Mean_AA.dat"))
    Sum10 = Sum10*(1/len(res8))
    Sum10.write_data_AA(join(calib_path,"BNT10_Mean_AA.dat"))
    SumRef = SumRef*(1/len(res8))
    SumRef.write_data_AA(join(calib_path,"Ref1_Pos4_Mean_AA.dat"))

    plt.plot(Sum8.x,Sum8.y, label="BNT 8 Mean")
    plt.plot(Sum10.x,Sum10.y, label="BNT 10 Mean")
    plt.plot(SumRef.x,SumRef.y, label="Ref1 Pos4 Mean")

    plt.legend()
    plt.show()

if __name__ == '__main__':
    
    main()