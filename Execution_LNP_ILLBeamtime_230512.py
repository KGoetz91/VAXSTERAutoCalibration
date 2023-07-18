# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 12:33:13 2023

@author: klaus
"""

# import reduce_images as reducer
import ILL_SAXANS_reducers as reducer
from reduce_images import load_data
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
    if type(gamma_files) == type(None):
        full_gamma_paths = None
    elif type(gamma_files) == float:
        full_gamma_paths = gamma_files
    else:
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
    path = r"Z:/Beamtimes/ILL/230510_LipidNanoParticles"
    
    #Working folders
    #poni: Path where the poni file for the reduction is located. 
    #mask: Path where the mask file for the reduction is located. 
    #datapath: Path to the rawdata nexus files
    #calib_path: Path were radially averaged 1D Data is stored
    #calib_noBG_path: Path were background corrected 1D Data is stored
    folders = {
              "poni" : "processed/LNP_SAXS_Klaus230530/",
              "mask" : "processed/LNP_SAXS_Klaus230530/",
              "datapath" : "rawdata",
              "calib_path" : "processed/LNP_SAXS_Klaus230530/calibrated",
              "calib_noBG_path" : "processed/LNP_SAXS_Klaus230530/calibrated_noBG"
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
                    "EF0089_1 original"       : (138709,138720),
                    "EF0092_2 DSPC 100 D2O"   : (138723,138734),
                    "EF0100_1 Chol 100 D2O"   : (138740,138751),
                    "EF0104_1 & 100 D2O"      : (138753,138764),
                    "EF0089_2 original"       : (138766,138777),
                    "EF0089_3 95 D2O"         : (138779,138790),
                    "EF0089_4 95 D2O"         : (138792,138803),
                    "EF0092_3 DSPC 100 D2O"   : (138805,138816),
                    "EF0100_2 Chol 100 D2O"   : (138828,138837),
                    "EF0104_2 & 100 D2O"      : (138839,138850),
                    "EF0089_5 91 D2O"         : (138852,138863),
                    "EF0092_2_05 DSPC 95 D2O" : (138865,138876),
                    "EF0089_6 91 D2O"         : (138878,138889),
                    "EF0092_1 85 D2O"         : (138892,138903),
                    "BNT4_01 100 D2O"         : (138905,138916),
                    "Buffer 100 D2O (Ref)"    : (138918,138953),
                    "GC"                      : (139075,139077),
                    "Buffer 90 D2O (Ref)"     : (138970,138981),
                    "BNT4_03 95 D2O"          : (138983,138994),
                    "Buffer 95 D2O (Ref)"     : (138996,139007),
                    "Buffer 85 D2O (Ref)"     : (139009,139020),
                    "Buffer 91 D2O (Ref)"     : (139022,139033),
                    "BNT4_05 90 D2O 1:2 verduennt": (139036,139046),
                    "BNT4_07 85 D2O"          : (139049,139060),
                    "BNT4_02 100 D2O 1:2 verduennt": (139062,139073),
                    "BNT4_04 95 D2O 1:2 verduennt": (139079,139090),
                    "BNT4_06 90 D2O 1:7 verduennt": (139092,139103),
                    "BNT4_08 85 D2O ": (139105,139116),
                    "EF92_02_10 90 D2O DSPC": (139118,139129),
                    "EF100_01_05 95 D2O Chol": (139131,139142),
                    "EF92_02_15 85 D2O DSPC": (139144,139155),
                    "EF100_01_10 90 D2O Chol": (139157,139168),
                    "EF100_01_15 85 D2O Chol": (139170,139181),
                    "EF104_01_05 95 D2O CholDSPC": (139184,139195),
                    "EF104_01_10 90 D2O CholDSPC": (139197,139208),
                    "EF092_03_05 95 D2O DSPC": (139210,139221),
                    "EF104_01_15 85 D2O CholDSPC": (139223,139234),
                    "EF092_03_10 90 D2O DSPC": (139236,139247),
                    "EF100_02_5 95 D2O Chol": (139250,139261),
                    "EF092_03_15 85 D2O DSPC": (139263,139274),
                    "EF100_02_10 90 D2O Chol": (139276,139287),
                    "EF089_01_15 85 D2O ": (139289,139300),
                    "EF100_02_15 85 D2O Chol": (139302,139313),
                    "EF104_02_05 95 D2O CholDSPC": (139315,139326),
                    "EF104_02_10 90 D2O CholDSPC": (139328,139339),
                    "EF104_02_15 85 D2O CholDSPC": (139341,139352),
                 }
    
    #dictionar of gamma BG files
    #Key is the same sample name as used in file_dict
    #Value is a list of gamma BG measurements
    #A single float value or None if no gamma background is to be subtracted
    gamma_dict = {}
    for data_set in file_dict.keys():
        gamma_dict[data_set] = [file_dict[data_set][1]+1]
    gamma_dict["EF0089_1 original"]     = [138739]
    gamma_dict["EF0092_2 DSPC 100 D2O"] = [138739]
    gamma_dict["EF92_02_15 85 D2O DSPC"]= None
    gamma_dict["BNT4_05 90 D2O 1:2 verduennt"] = [139048]
    # for key in file_dict.keys():
    #     gamma_dict[key] = None
    
    #Standard Parameters
    std_params = {
                    "CF": 5.6e11,
                    "thickness": np.sqrt(2),
                    }
    
    #dictionary of all parameters for each sample filled for now with standard params for all samples
    parameter_dict = {}
    for sample in file_dict.keys():
        parameter_dict[sample] = std_params
    print(parameter_dict)
    parameter_dict['GC'] = {"CF": 5.6e11,
                            "thickness": np.sqrt(2)}
    print(parameter_dict)
    
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
        data.write_data_AA(join(complete_folders['calib_path'],"{}_AA.dat".format(data_set)))
        plt.loglog(data.x,data.y,label=(data_set))
        
    plt.show()
    plt.clf()
    
    bg = result_dict["Buffer 100 D2O (Ref)"]
    bg_mean = np.mean(bg.y[np.logical_and(bg.x>=0.035,bg.x<=0.15)])
    
    for dataset in file_dict.keys():
        mean = np.mean(result_dict[dataset].y[np.logical_and(result_dict[dataset].x>=0.035,result_dict[dataset].x<=0.15)])
        result_dict[dataset] = (result_dict[dataset]*(bg_mean/mean)) - bg
        result_dict[dataset].write_data_AA(join(complete_folders['calib_noBG_path'],"{}_noBG_AA.dat".format(dataset)))
        plt.loglog(result_dict[dataset].x,result_dict[dataset].y,label=dataset)
        

    #enable legend and show the pyplot canvas
    plt.legend()
    plt.show()
        
if __name__ == '__main__':
    
    main()