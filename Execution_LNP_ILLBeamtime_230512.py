# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 12:33:13 2023

@author: klaus
"""

# import reduce_images as reducer
import ILL_SAXANS_reducers as reducer
# from reduce_images import load_data,CapillaryScan
from os.path import join,isdir,isfile
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np

def create_filelist(flist, datapath="./"):
    
    result=[]
    
    for i in flist:
        filename = join(datapath,r"{:d}.nxs".format(i))
        result.append(filename)
        
    return result

def create_filenames(start,stop, datapath="./"):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = join(datapath,r"{:d}.nxs".format(i))
        result.append(filename)
        
    return result

def check_paths(path, folders):
    result = {}
    for folder in folders.keys():
        complete_folder_path = join(path, folders[folder])
        result[folder] = complete_folder_path
        if not isdir(complete_folder_path):
            makedirs(complete_folder_path)
    return result

def check_files(complete_folders, files):
    result = {}
    for file in files.keys():
        file_path = join(complete_folders[file], files[file])
        if not isfile(file_path):
            raise  Exception("File {} not found.".format(file_path))
        else:
            result[file] = file_path
    return result
        
def GC():

    # #GC SAXS
    # data_files = create_filenames(91565, 91565,datapath)
    # TM_file = create_filelist([91564,91566],datapath)
    # DB_file = create_filenames(91565,91565,datapath)[0]
    
    # #                                                     TM time     time  d   CF      poni       mask
    # ds = reducer.TwoDReducer("GC", data_files,TM_file,1200,DB_file,600, 0.1, 5.6e4, join(ponipath,"poni.poni"), mask = "./mask_pyFAI.edf", darkCurrent=6.275e-5)
    # res = ds.getOneD()
    # plt.loglog(res.x,res.y,label="GC measured") 

    # #GC APS 
    # x,y = load_data(r"./GC_APS.dat")
    # plt.loglog(x,y,label="GC APS") 
    # #plt.xlim([0.9e-1,3])
    # #plt.ylim([5,110])
    pass    

def reduce_data(data_set, data_files, gamma_files, parameters,folders,files):
    full_data_paths = create_filenames(data_files[0], data_files[1],folders['datapath'])
    full_gamma_paths = create_filelist(gamma_files,folders['datapath'])
    
    full_poni_path = files['poni']
    full_mask_path = files['mask']
    
    calib_path = folders['calib_path']
    calib_noBG_path = folders['calib_noBG_path']
    
    thickness = parameters["thickness"]
    calibration_factor = parameters["CF"]    
    
    ds = reducer.ILLSAXS_TwoDReducer(data_set,                                 # Sample Name for internal Reference and header
                                     full_data_paths,                          # List of all Data files             
                                     full_gamma_paths,                         # List of all Gamma files             
                                     thickness,                                # Sample Thickness (double)
                                     calibration_factor,                       # calibration factor (double)
                                     full_poni_path,                           # Poni file (string) 
                                     mask = full_mask_path,                    # Mask file (string)
                                     DB = True                                 # If true the DB position is fitted for each data set
                                     )
    
    res = ds.getOneD()
    return res

def main():
    
    plt.clf()
    
    #Base path to were the reduction takes place. This will be put in front of 
    #all working folders
    path = r"E:/ILL May 23 Data/"
    
    #Working folders
    #poni: Path where the poni file for the reduction is located. 
    #mask: Path where the mask file for the reduction is located. 
    #datapath: Path to the rawdata nexus files
    #calib_path: Path were radially averaged 1D Data is stored
    #calib_noBG_path: Path were background corrected 1D Data is stored
    folders = {
              "poni" : "",
              "mask" : "",
              "datapath" : "rawdata",
              "calib_path" : "calibrated",
              "calib_noBG_path" : "calibrated_noBG"
              }
    
    #Additional Files
    #poni: Name of the poni file for the reduction
    #mask: Name of the mask file for the reduction
    files = {
             "poni": "final_poni.poni",
             "mask": "mask.edf"}
    
    #checks if the folders exist and creates the complete folder paths in complete_folders
    complete_folders = check_paths(path, folders)
    complete_files = check_files(complete_folders, files)

    #dictionary of data files
    #Key is the sample name
    #Value is tuple of (first file, last file)
    file_dict = {
                 "EF_0092_2"  : (138723,138734)}
    
    #dictionar of gamma BG files
    #Key is the same sample name as used in file_dict
    #Value is a list of gamma BG measurements
    gamma_dict = {
                  "EF_0092_2"  : [138739]}
    
    #Standard Parameters
    std_params = {
                    "CF": 1,
                    "thickness": np.sqrt(2),
                    }
    
    #dictionary of all parameters for each sample filled for now with standard params for all samples
    parameter_dict = {}
    for sample in file_dict.keys():
        parameter_dict[sample] = std_params
    
    #Empty dictionary to store results
    #Keys: same sample names as in file_dict
    #values: OneDDatasets of the radially averaged and absolute calibrated Data
    result_dict = {}

    #do not change below
    #ready the pyplot canvas
    plt.clf()
    #loop over all sample keys in file_dict
    for data_set in file_dict.keys():
        
        data = reduce_data(data_set, file_dict[data_set],gamma_dict[data_set],
                           parameter_dict[data_set],complete_folders,complete_files)
        result_dict[data_set] = data
        plt.loglog(data.x,data.y,label=(data_set))

    #enable legend and show the pyplot canvas
    plt.legend()
    plt.show()
        
if __name__ == '__main__':
    
    main()