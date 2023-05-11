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
    
    ponipath ="Z:/Klaus/Data/LipidNanoparticles/SAXS/230509_LNP_ILL_Beamtime"
    datapath = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230509_LNP_ILL_Beamtime/rawdata"
    calib_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230509_LNP_ILL_Beamtime/calibrated"
    calib_noBG_path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230509_LNP_ILL_Beamtime/calibrated_noBG"
    
    if not isdir(calib_path):
        makedirs(calib_path)
    if not isdir(calib_noBG_path):
        makedirs(calib_noBG_path)

    plt.clf()

    file_dict = {
                "EF_0089_1": [91406,91418,91430],
                "EF_0089_2": [91409,91421,91433],
                "EF_0089_4": [91412,91424,91436],
                "EF_0100"  : [91415,91427,91439]}
    
    mult_dict = {"EF_0089_1": 1,
                 "EF_0089_2": 1,
                 "EF_0089_4": 1.02,
                 "EF_0100"  : 1.025}
    
    result_dict = {}

    for data_set in file_dict.keys():
        
        for ctr, j in enumerate(file_dict[data_set]):
            data_files = create_filenames(j, j,datapath)
            TM_file = create_filelist([j-1,j+1],datapath)
            DB_file = create_filelist([91389],datapath)[0]
            
                                                                                     #time    d      CF      poni                                  mask
            ds = reducer.TwoDReducer("{}".format(j), data_files,TM_file,1800,DB_file,1800, 0.1086, 5.6e4, join(ponipath,"poni.poni"), mask = join(ponipath,"mask.edf"), darkCurrent=6.275e-5)
            res = ds.getOneD()
            
            if ctr == 0:
                result_dict[data_set]=res
            else:
                result_dict[data_set]=result_dict[data_set]+res
                
        result_dict[data_set]=result_dict[data_set]*(mult_dict[data_set]/len(file_dict[data_set]))
        if data_set == "EF_0100":
            result_dict[data_set].make_linear(0.9)
        plt.loglog(result_dict[data_set].x,result_dict[data_set].y,label = data_set)
        
    bg = result_dict["EF_0100"]
    for data_set in file_dict.keys():
        result_dict[data_set].write_data_AA(join(calib_path,"{}_AA.dat".format(data_set)))
        (result_dict[data_set]-bg).write_data_AA(join(calib_noBG_path,"{}_noBG_AA.dat".format(data_set)))
    plt.legend()
    plt.show()
        
if __name__ == '__main__':
    
    main()