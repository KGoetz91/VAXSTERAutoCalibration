# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:06:28 2023

@author: klaus
"""

from reduce_images import OneDLoader as loader
import numpy as np
import matplotlib.pyplot as plt

from os.path import join
from os import listdir

from matplotlib import rcParams as pltParams

datapath = "Z:/Beamtimes/ILL/230510_LipidNanoParticles/processed/LNP_SANS_Klaus230530"
processed = "Z:/Beamtimes/ILL/230510_LipidNanoParticles/processed/LNP_SANS_Klaus230530/noBG"

filelist = list(listdir(datapath))

def make_plot_nice():

    plt.style.use("seaborn-v0_8")
    pltParams["lines.linewidth"] = 3
    
    pltParams.update({"font.size": 22}) 
    pltParams["font.weight"] = "bold"
    

def make_filename(number):
    for file in filelist:
        if str(number) in file:
            return join(datapath,file)

def backgrounds():
    bg1 = loader(make_filename(138918))
    plt.loglog(bg1.x,bg1.y,label="D2O")
    bg1 = loader(make_filename(138996))
    plt.loglog(bg1.x,bg1.y,label="95% D2O")
    bg1 = loader(make_filename(139022))
    plt.loglog(bg1.x,bg1.y,label="91% D2O")
    bg1 = loader(make_filename(138970))
    plt.loglog(bg1.x,bg1.y,label="90% D2O")
    bg1 = loader(make_filename(139009))
    plt.loglog(bg1.x,bg1.y,label="85% D2O")

def d2o_samples():
    bg1 = loader(make_filename(138918))
    bg1 *= 1.6
    plt.loglog(bg1.x,bg1.y,label="D2O")
    
    ef_89_1 = loader(make_filename(138709))
    plt.loglog(ef_89_1.x,ef_89_1.y, label="Original 89_1")
    ef_89_2 = loader(make_filename(138766))
    plt.loglog(ef_89_2.x,ef_89_2.y, label="Original 89_2")
    
    ef_92_2 = loader(make_filename(138723))
    plt.loglog(ef_92_2.x,ef_92_2.y, label="dDSPC 92_2")
    ef_92_3 = loader(make_filename(138805))
    plt.loglog(ef_92_3.x,ef_92_3.y, label="dDSPC 92_3")
    
    ef_100_1 = loader(make_filename(138740))
    plt.loglog(ef_100_1.x,ef_100_1.y, label="dChol 100_1")
    ef_100_2 = loader(make_filename(138823))
    plt.loglog(ef_100_2.x,ef_100_2.y, label="dChol 100_2")
    
    ef_104_1 = loader(make_filename(138753))
    plt.loglog(ef_104_1.x,ef_104_1.y, label="dDSPC dChol 104_1")
    ef_104_2 = loader(make_filename(138839))
    plt.loglog(ef_104_2.x,ef_104_2.y, label="dDSPC dChol 104_2")
    
    bnt_4_1 = loader(make_filename(138905))
    plt.loglog(bnt_4_1.x,bnt_4_1.y, label="BNT4_01")
    bnt_4_2 = loader(make_filename(139062))
    plt.loglog(bnt_4_2.x,bnt_4_2.y, label="BNT4_02, verdünnt 1:1")
 
def d2o_noBG_samples():
    bg1 = loader(make_filename(138918))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    # plt.loglog(bg1.x,bg1.y,label="D2O")
    
    
    ef_89_1 = loader(make_filename(138709))
    mean = np.mean(ef_89_1.y[np.logical_and(ef_89_1.x>=0.16,ef_89_1.x<=0.32)])
    ef_89_1 *= bg_mean/mean
    # plt.loglog(ef_89_1.x,ef_89_1.y, label="Original 89_1")
    ef_89_1 -= bg1
    plt.loglog(ef_89_1.x,ef_89_1.y, label="Original 89_1")
    
    ef_89_2 = loader(make_filename(138766))
    mean = np.mean(ef_89_2.y[np.logical_and(ef_89_2.x>=0.16,ef_89_2.x<=0.32)])
    ef_89_2 *= bg_mean/mean
    # plt.loglog(ef_89_2.x,ef_89_2.y, label="Original 89_2")
    ef_89_2 -= bg1
    plt.loglog(ef_89_2.x,ef_89_2.y, label="Original 89_2")
    
    ef_92_2 = loader(make_filename(138723))
    mean = np.mean(ef_92_2.y[np.logical_and(ef_92_2.x>=0.16,ef_92_2.x<=0.32)])
    ef_92_2 *= bg_mean/mean
    # plt.loglog(ef_92_2.x,ef_92_2.y, label="dDSPC 92_2")
    ef_92_2 -= bg1
    plt.loglog(ef_92_2.x,ef_92_2.y, label="dDSPC 92_2")

    ef_92_3 = loader(make_filename(138805))
    mean = np.mean(ef_92_3.y[np.logical_and(ef_92_3.x>=0.16,ef_92_3.x<=0.32)])
    ef_92_3 *= bg_mean/mean
    # plt.loglog(ef_92_3.x,ef_92_3.y, label="dDSPC 92_3")
    ef_92_3 -= bg1
    plt.loglog(ef_92_3.x,ef_92_3.y, label="dDSPC 92_3")

    ef_100_1 = loader(make_filename(138740))
    mean = np.mean(ef_100_1.y[np.logical_and(ef_100_1.x>=0.16,ef_100_1.x<=0.32)])
    ef_100_1 *= bg_mean/mean
    # plt.loglog(ef_100_1.x,ef_100_1.y, label="dChol 100_1")
    ef_100_1 -= bg1
    plt.loglog(ef_100_1.x,ef_100_1.y, label="dChol 100_1")

    ef_100_2 = loader(make_filename(138823))
    mean = np.mean(ef_100_2.y[np.logical_and(ef_100_2.x>=0.16,ef_100_2.x<=0.32)])
    ef_100_2 *= bg_mean/mean
    # plt.loglog(ef_100_2.x,ef_100_2.y, label="dChol 100_2")
    ef_100_2 -= bg1
    plt.loglog(ef_100_2.x,ef_100_2.y, label="dChol 100_2")
    
    ef_104_1 = loader(make_filename(138753))
    mean = np.mean(ef_104_1.y[np.logical_and(ef_104_1.x>=0.16,ef_104_1.x<=0.32)])
    ef_104_1 *= bg_mean/mean
    # plt.loglog(ef_104_1.x,ef_104_1.y, label="dDSPC dChol 104_1")
    ef_104_1 -= bg1
    plt.loglog(ef_104_1.x,ef_104_1.y, label="dDSPC dChol 104_1")

    ef_104_2 = loader(make_filename(138839))
    mean = np.mean(ef_104_2.y[np.logical_and(ef_104_2.x>=0.16,ef_104_2.x<=0.32)])
    ef_104_2 *= bg_mean/mean
    # plt.loglog(ef_104_2.x,ef_104_2.y, label="dDSPC dChol 104_2")
    ef_104_2 -= bg1
    plt.loglog(ef_104_2.x,ef_104_2.y, label="dDSPC dChol 104_2")
    
    bnt_4_1 = loader(make_filename(138905))
    mean = np.mean(bnt_4_1.y[np.logical_and(bnt_4_1.x>=0.16,bnt_4_1.x<=0.32)])
    bnt_4_1 *= bg_mean/mean
    # plt.loglog(bnt_4_1.x,bnt_4_1.y, label="BNT4_01")
    bnt_4_1 -= bg1
    plt.loglog(bnt_4_1.x,bnt_4_1.y, label="BNT4_01")

    bnt_4_2 = loader(make_filename(139062))
    mean = np.mean(bnt_4_2.y[np.logical_and(bnt_4_2.x>=0.16,bnt_4_2.x<=0.32)])
    bnt_4_2 *= bg_mean/mean
    # plt.loglog(bnt_4_2.x,bnt_4_2.y, label="BNT4_02, verdünnt 1:1") 
    bnt_4_2 -= bg1
    plt.loglog(bnt_4_2.x,bnt_4_2.y, label="BNT4_02, verdünnt 1:1")   
 
def d2o95_samples():
    bg1 = loader(make_filename(138996))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    # plt.loglog(bg1.x,bg1.y,label="95% D2O")
    
    ef_89_3 = loader(make_filename(138779))
    mean = np.mean(ef_89_3.y[np.logical_and(ef_89_3.x>=0.16,ef_89_3.x<=0.32)])
    ef_89_3 *= bg_mean/mean
    ef_89_3 -= bg1
    plt.loglog(ef_89_3.x,ef_89_3.y, label="Original 89_3")
    
    ef_89_4 = loader(make_filename(138792))
    mean = np.mean(ef_89_4.y[np.logical_and(ef_89_4.x>=0.16,ef_89_4.x<=0.32)])
    ef_89_4 *= bg_mean/mean
    ef_89_4 -= bg1
    plt.loglog(ef_89_4.x,ef_89_4.y, label="Original 89_4")
    
    ef_92_2_05 = loader(make_filename(138865))
    mean = np.mean(ef_92_2_05.y[np.logical_and(ef_92_2_05.x>=0.16,ef_92_2_05.x<=0.32)])
    ef_92_2_05 *= bg_mean/mean
    ef_92_2_05 -= bg1
    plt.loglog(ef_92_2_05.x,ef_92_2_05.y, label="dDSPC 92_2_05")
    
    ef_92_3_05 = loader(make_filename(139210))
    mean = np.mean(ef_92_3_05.y[np.logical_and(ef_92_3_05.x>=0.16,ef_92_3_05.x<=0.32)])
    ef_92_3_05 *= bg_mean/mean
    ef_92_3_05 -= bg1
    plt.loglog(ef_92_3_05.x,ef_92_3_05.y, label="dDSPC 92_3_05")
    
    ef_100_1_05 = loader(make_filename(139131))
    mean = np.mean(ef_100_1_05.y[np.logical_and(ef_100_1_05.x>=0.16,ef_100_1_05.x<=0.32)])
    ef_100_1_05 *= bg_mean/mean
    ef_100_1_05 -= bg1
    plt.loglog(ef_100_1_05.x,ef_100_1_05.y, label="dChol 100_1_05")
    
    ef_100_2_05 = loader(make_filename(139250))
    mean = np.mean(ef_100_2_05.y[np.logical_and(ef_100_2_05.x>=0.16,ef_100_2_05.x<=0.32)])
    ef_100_2_05 *= bg_mean/mean
    ef_100_2_05 -= bg1
    plt.loglog(ef_100_2_05.x,ef_100_2_05.y, label="dChol 100_2_05")
    
    ef_104_1_05 = loader(make_filename(139184))
    mean = np.mean(ef_104_1_05.y[np.logical_and(ef_104_1_05.x>=0.16,ef_104_1_05.x<=0.32)])
    ef_104_1_05 *= bg_mean/mean
    ef_104_1_05 -= bg1
    plt.loglog(ef_104_1_05.x,ef_104_1_05.y, label="dDSPC dChol 104_1_05")
    
    ef_104_2_05 = loader(make_filename(139315))
    mean = np.mean(ef_104_2_05.y[np.logical_and(ef_104_2_05.x>=0.16,ef_104_2_05.x<=0.32)])
    ef_104_2_05 *= bg_mean/mean
    ef_104_2_05 -= bg1
    plt.loglog(ef_104_2_05.x,ef_104_2_05.y, label="dDSPC dChol 104_2_05")
    
    bnt_4_3 = loader(make_filename(138983))
    mean = np.mean(bnt_4_3.y[np.logical_and(bnt_4_3.x>=0.16,bnt_4_3.x<=0.32)])
    bnt_4_3 *= bg_mean/mean
    bnt_4_3 -= bg1
    plt.loglog(bnt_4_3.x,bnt_4_3.y, label="BNT4_03")
    
    bnt_4_4 = loader(make_filename(139079))
    mean = np.mean(bnt_4_4.y[np.logical_and(bnt_4_4.x>=0.16,bnt_4_4.x<=0.32)])
    bnt_4_4 *= bg_mean/mean
    bnt_4_4 -= bg1
    plt.loglog(bnt_4_4.x,bnt_4_4.y, label="BNT4_04, verdünnt 1:1")
 
def d2o90_samples():
    bg1 = loader(make_filename(139022))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    # plt.loglog(bg1.x,bg1.y,label="91% D2O")
    # bg1 = loader(make_filename(138970))
    # plt.loglog(bg1.x,bg1.y,label="90% D2O")
    
    ef_89_5 = loader(make_filename(138852))
    mean = np.mean(ef_89_5.y[np.logical_and(ef_89_5.x>=0.16,ef_89_5.x<=0.32)])
    ef_89_5 *= bg_mean/mean
    ef_89_5 -= bg1
    plt.loglog(ef_89_5.x,ef_89_5.y, label="Original 89_5")
    
    ef_89_6 = loader(make_filename(138878))
    mean = np.mean(ef_89_6.y[np.logical_and(ef_89_6.x>=0.16,ef_89_6.x<=0.32)])
    ef_89_6 *= bg_mean/mean
    ef_89_6 -= bg1
    plt.loglog(ef_89_6.x,ef_89_6.y, label="Original 89_6")
    
    ef_92_2_10 = loader(make_filename(139118))
    mean = np.mean(ef_92_2_10.y[np.logical_and(ef_92_2_10.x>=0.16,ef_92_2_10.x<=0.32)])
    ef_92_2_10 *= bg_mean/mean
    ef_92_2_10 -= bg1
    plt.loglog(ef_92_2_10.x,ef_92_2_10.y, label="dDSPC 92_2_10")
    
    ef_92_3_10 = loader(make_filename(139236))
    mean = np.mean(ef_92_3_10.y[np.logical_and(ef_92_3_10.x>=0.16,ef_92_3_10.x<=0.32)])
    ef_92_3_10 *= bg_mean/mean
    ef_92_3_10 -= bg1
    plt.loglog(ef_92_3_10.x,ef_92_3_10.y, label="dDSPC 92_3_10")
    
    ef_100_1_10 = loader(make_filename(139157))
    mean = np.mean(ef_100_1_10.y[np.logical_and(ef_100_1_10.x>=0.16,ef_100_1_10.x<=0.32)])
    ef_100_1_10 *= bg_mean/mean
    ef_100_1_10 -= bg1
    plt.loglog(ef_100_1_10.x,ef_100_1_10.y, label="dChol 100_1_10")
    
    ef_100_2_10 = loader(make_filename(139276))
    mean = np.mean(ef_100_2_10.y[np.logical_and(ef_100_2_10.x>=0.16,ef_100_2_10.x<=0.32)])
    ef_100_2_10 *= bg_mean/mean
    ef_100_2_10 -= bg1
    plt.loglog(ef_100_2_10.x,ef_100_2_10.y, label="dChol 100_2_10")
    
    ef_104_1_10 = loader(make_filename(139197))
    mean = np.mean(ef_104_1_10.y[np.logical_and(ef_104_1_10.x>=0.16,ef_104_1_10.x<=0.32)])
    ef_104_1_10 *= bg_mean/mean
    ef_104_1_10 -= bg1
    plt.loglog(ef_104_1_10.x,ef_104_1_10.y, label="dDSPC dChol 104_1_10")
    
    ef_104_2_10 = loader(make_filename(139328))
    mean = np.mean(ef_104_2_10.y[np.logical_and(ef_104_2_10.x>=0.16,ef_104_2_10.x<=0.32)])
    ef_104_2_10 *= bg_mean/mean
    ef_104_2_10 -= bg1
    plt.loglog(ef_104_2_10.x,ef_104_2_10.y, label="dDSPC dChol 104_2_10")
    
    bnt_4_5 = loader(make_filename(139035))
    mean = np.mean(bnt_4_5.y[np.logical_and(bnt_4_5.x>=0.16,bnt_4_5.x<=0.32)])
    bnt_4_5 *= bg_mean/mean
    bnt_4_5 -= bg1
    plt.loglog(bnt_4_5.x,bnt_4_5.y, label="BNT4_03, verdünnt 1:1")
    
    bnt_4_6 = loader(make_filename(139092))
    mean = np.mean(bnt_4_6.y[np.logical_and(bnt_4_6.x>=0.16,bnt_4_6.x<=0.32)])
    bnt_4_6 *= bg_mean/mean
    bnt_4_6 -= bg1
    plt.loglog(bnt_4_6.x,bnt_4_6.y, label="BNT4_04, verdünnt 1:6")    

def d2o85_samples():
    bg1 = loader(make_filename(139009))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    # plt.loglog(bg1.x,bg1.y,label="85% D2O")
    
    ef_92_1 = loader(make_filename(138892))
    mean = np.mean(ef_92_1.y[np.logical_and(ef_92_1.x>=0.16,ef_92_1.x<=0.32)])
    ef_92_1 *= bg_mean/mean
    ef_92_1 -= bg1
    plt.loglog(ef_92_1.x,ef_92_1.y, label="Original 92_1")
    ef_89_1_15 = loader(make_filename(139289))
    mean = np.mean(ef_89_1_15.y[np.logical_and(ef_89_1_15.x>=0.16,ef_89_1_15.x<=0.32)])
    ef_89_1_15 *= bg_mean/mean
    ef_89_1_15 -= bg1
    plt.loglog(ef_89_1_15.x,ef_89_1_15.y, label="Original 89_1_15")
    
    ef_92_2_15 = loader(make_filename(139144))
    mean = np.mean(ef_92_2_15.y[np.logical_and(ef_92_2_15.x>=0.16,ef_92_2_15.x<=0.32)])
    ef_92_2_15 *= bg_mean/mean
    ef_92_2_15 -= bg1
    plt.loglog(ef_92_2_15.x,ef_92_2_15.y, label="dDSPC 92_2_15")
    ef_92_3_15 = loader(make_filename(139263))
    mean = np.mean(ef_92_3_15.y[np.logical_and(ef_92_3_15.x>=0.16,ef_92_3_15.x<=0.32)])
    ef_92_3_15 *= bg_mean/mean
    ef_92_3_15 -= bg1
    plt.loglog(ef_92_3_15.x,ef_92_3_15.y, label="dDSPC 92_3_15")
    
    ef_100_1_15 = loader(make_filename(139170))
    mean = np.mean(ef_100_1_15.y[np.logical_and(ef_100_1_15.x>=0.16,ef_100_1_15.x<=0.32)])
    ef_100_1_15 *= bg_mean/mean
    ef_100_1_15 -= bg1
    plt.loglog(ef_100_1_15.x,ef_100_1_15.y, label="dChol 100_1_15")
    ef_100_2_15 = loader(make_filename(139302))
    mean = np.mean(ef_100_2_15.y[np.logical_and(ef_100_2_15.x>=0.16,ef_100_2_15.x<=0.32)])
    ef_100_2_15 *= bg_mean/mean
    ef_100_2_15 -= bg1
    plt.loglog(ef_100_2_15.x,ef_100_2_15.y, label="dChol 100_2_15")
    
    ef_104_1_15 = loader(make_filename(139223))
    mean = np.mean(ef_104_1_15.y[np.logical_and(ef_104_1_15.x>=0.16,ef_104_1_15.x<=0.32)])
    ef_104_1_15 *= bg_mean/mean
    ef_104_1_15 -= bg1
    plt.loglog(ef_104_1_15.x,ef_104_1_15.y, label="dDSPC dChol 104_1_15")
    ef_104_2_15 = loader(make_filename(139341))
    mean = np.mean(ef_104_2_15.y[np.logical_and(ef_104_2_15.x>=0.16,ef_104_2_15.x<=0.32)])
    ef_104_2_15 *= bg_mean/mean
    ef_104_2_15 -= bg1
    plt.loglog(ef_104_2_15.x,ef_104_2_15.y, label="dDSPC dChol 104_2_15")
    
    bnt_4_7 = loader(make_filename(139049))
    mean = np.mean(bnt_4_7.y[np.logical_and(bnt_4_7.x>=0.16,bnt_4_7.x<=0.32)])
    bnt_4_7 *= bg_mean/mean
    bnt_4_7 -= bg1
    plt.loglog(bnt_4_7.x,bnt_4_7.y, label="BNT4_07")
    bnt_4_8 = loader(make_filename(139105))
    mean = np.mean(bnt_4_8.y[np.logical_and(bnt_4_8.x>=0.16,bnt_4_8.x<=0.32)])
    bnt_4_8 *= bg_mean/mean
    bnt_4_8 -= bg1
    plt.loglog(bnt_4_8.x,bnt_4_8.y, label="BNT4_08")

def original_samples():
    bg1 = loader(make_filename(138918))
    bg1 *= 1.6
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_89_1 = loader(make_filename(138709))
    mean = np.mean(ef_89_1.y[np.logical_and(ef_89_1.x>=0.16,ef_89_1.x<=0.32)])
    ef_89_1 *= bg_mean/mean
    ef_89_1 -= bg1
    ef_89_1.write_data(join(processed,"EF_089_1_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_1.x,ef_89_1.y,ls="solid", c="blue", label="Original 89_1")
    
    ef_89_2 = loader(make_filename(138766))
    mean = np.mean(ef_89_2.y[np.logical_and(ef_89_2.x>=0.16,ef_89_2.x<=0.32)])
    ef_89_2 *= bg_mean/mean
    ef_89_2 -= bg1
    ef_89_2.write_data(join(processed,"EF_089_2_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_2.x,ef_89_2.y,ls="--", c="blue", label="Original 89_2")
    
    bg1 = loader(make_filename(138996))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_89_3 = loader(make_filename(138779))
    mean = np.mean(ef_89_3.y[np.logical_and(ef_89_3.x>=0.16,ef_89_3.x<=0.32)])
    ef_89_3 *= bg_mean/mean
    ef_89_3 -= bg1
    ef_89_3.write_data(join(processed,"EF_089_3_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_3.x,ef_89_3.y, ls="solid", c="red",label="Original 89_3")
    
    ef_89_4 = loader(make_filename(138792))
    mean = np.mean(ef_89_4.y[np.logical_and(ef_89_4.x>=0.16,ef_89_4.x<=0.32)])
    ef_89_4 *= bg_mean/mean
    ef_89_4 -= bg1
    ef_89_4.write_data(join(processed,"EF_089_4_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_4.x,ef_89_4.y, ls="--", c="red",label="Original 89_4")
    
    bg1 = loader(make_filename(139022))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_89_5 = loader(make_filename(138852))
    mean = np.mean(ef_89_5.y[np.logical_and(ef_89_5.x>=0.16,ef_89_5.x<=0.32)])
    ef_89_5 *= bg_mean/mean
    ef_89_5 -= bg1
    ef_89_5.write_data(join(processed,"EF_089_5_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_5.x,ef_89_5.y, ls="solid", c="green",label="Original 89_5")
    
    ef_89_6 = loader(make_filename(138878))
    mean = np.mean(ef_89_6.y[np.logical_and(ef_89_6.x>=0.16,ef_89_6.x<=0.32)])
    ef_89_6 *= bg_mean/mean
    ef_89_6 -= bg1
    ef_89_6.write_data(join(processed,"EF_089_6_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_6.x,ef_89_6.y, ls="--", c="green",label="Original 89_6")
    
    bg1 = loader(make_filename(139009))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_92_1 = loader(make_filename(138892))
    mean = np.mean(ef_92_1.y[np.logical_and(ef_92_1.x>=0.16,ef_92_1.x<=0.32)])
    ef_92_1 *= bg_mean/mean
    ef_92_1 -= bg1
    ef_92_1.write_data(join(processed,"EF_092_1_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_1.x,ef_92_1.y, ls="solid", c="purple",label="Original 92_1")
    ef_89_1_15 = loader(make_filename(139289))
    mean = np.mean(ef_89_1_15.y[np.logical_and(ef_89_1_15.x>=0.16,ef_89_1_15.x<=0.32)])
    ef_89_1_15 *= bg_mean/mean
    ef_89_1_15 -= bg1
    ef_89_1_15 *= 1/0.85
    ef_89_1_15.write_data(join(processed,"EF_089_1_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_89_1_15.x,ef_89_1_15.y, ls="--", c="purple",label="Original 89_1_15")
    
    
def ddspc():
    bg1 = loader(make_filename(138918))
    bg1 *= 1.6
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_92_2 = loader(make_filename(138723))
    mean = np.mean(ef_92_2.y[np.logical_and(ef_92_2.x>=0.16,ef_92_2.x<=0.32)])
    ef_92_2 *= bg_mean/mean
    ef_92_2 -= bg1
    ef_92_2.write_data(join(processed,"ef_92_2_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_2.x,ef_92_2.y, ls="solid", c="blue",label="dDSPC 92_2")

    ef_92_3 = loader(make_filename(138805))
    mean = np.mean(ef_92_3.y[np.logical_and(ef_92_3.x>=0.16,ef_92_3.x<=0.32)])
    ef_92_3 *= bg_mean/mean
    ef_92_3 -= bg1
    ef_92_3.write_data(join(processed,"ef_92_3_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_3.x,ef_92_3.y, ls="--", c="blue",label="dDSPC 92_3")

    
    bg1 = loader(make_filename(138996))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_92_2_05 = loader(make_filename(138865))
    mean = np.mean(ef_92_2_05.y[np.logical_and(ef_92_2_05.x>=0.16,ef_92_2_05.x<=0.32)])
    ef_92_2_05 *= bg_mean/mean
    ef_92_2_05 -= bg1
    ef_92_2_05.write_data(join(processed,"ef_92_2_05_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_2_05.x,ef_92_2_05.y,  ls="solid", c="red",label="dDSPC 92_2_05")
    
    ef_92_3_05 = loader(make_filename(139210))
    mean = np.mean(ef_92_3_05.y[np.logical_and(ef_92_3_05.x>=0.16,ef_92_3_05.x<=0.32)])
    ef_92_3_05 *= bg_mean/mean
    ef_92_3_05 -= bg1
    ef_92_3_05.write_data(join(processed,"ef_92_3_05_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_3_05.x,ef_92_3_05.y,  ls="--", c="red",label="dDSPC 92_3_05")

    
    bg1 = loader(make_filename(139022))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_92_2_10 = loader(make_filename(139118))
    mean = np.mean(ef_92_2_10.y[np.logical_and(ef_92_2_10.x>=0.16,ef_92_2_10.x<=0.32)])
    ef_92_2_10 *= bg_mean/mean
    ef_92_2_10 -= bg1
    ef_92_2_10.write_data(join(processed,"ef_92_2_10_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_2_10.x,ef_92_2_10.y, ls="solid", c="green",label="dDSPC 92_2_10")
    
    ef_92_3_10 = loader(make_filename(139236))
    mean = np.mean(ef_92_3_10.y[np.logical_and(ef_92_3_10.x>=0.16,ef_92_3_10.x<=0.32)])
    ef_92_3_10 *= bg_mean/mean
    ef_92_3_10 -= bg1
    ef_92_3_10.write_data(join(processed,"ef_92_3_10_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_3_10.x,ef_92_3_10.y,ls="--", c="green", label="dDSPC 92_3_10")
    
    bg1 = loader(make_filename(139009))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])

    ef_92_2_15 = loader(make_filename(139144))
    mean = np.mean(ef_92_2_15.y[np.logical_and(ef_92_2_15.x>=0.16,ef_92_2_15.x<=0.32)])
    ef_92_2_15 *= bg_mean/mean
    ef_92_2_15 -= bg1
    ef_92_2_15.write_data(join(processed,"ef_92_2_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_2_15.x,ef_92_2_15.y,ls="solid", c="purple", label="dDSPC 92_2_15")
    ef_92_3_15 = loader(make_filename(139263))
    mean = np.mean(ef_92_3_15.y[np.logical_and(ef_92_3_15.x>=0.16,ef_92_3_15.x<=0.32)])
    ef_92_3_15 *= bg_mean/mean
    ef_92_3_15 -= bg1
    ef_92_3_15.write_data(join(processed,"ef_92_3_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_92_3_15.x,ef_92_3_15.y, ls="--", c="purple",label="dDSPC 92_3_15")
    
    
def dchol():
    bg1 = loader(make_filename(138918))
    bg1 *= 1.6
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_100_1 = loader(make_filename(138740))
    mean = np.mean(ef_100_1.y[np.logical_and(ef_100_1.x>=0.16,ef_100_1.x<=0.32)])
    ef_100_1 *= bg_mean/mean
    ef_100_1 -= bg1
    ef_100_1.write_data(join(processed,"ef_100_1_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_1.x,ef_100_1.y, ls="solid", c="blue",label="dChol 100_1")

    ef_100_2 = loader(make_filename(138823))
    mean = np.mean(ef_100_2.y[np.logical_and(ef_100_2.x>=0.16,ef_100_2.x<=0.32)])
    ef_100_2 *= bg_mean/mean
    ef_100_2 -= bg1
    ef_100_2.write_data(join(processed,"ef_100_2_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_2.x,ef_100_2.y, ls="--", c="blue",label="dChol 100_2")
    
    bg1 = loader(make_filename(138996))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_100_1_05 = loader(make_filename(139131))
    mean = np.mean(ef_100_1_05.y[np.logical_and(ef_100_1_05.x>=0.16,ef_100_1_05.x<=0.32)])
    ef_100_1_05 *= bg_mean/mean
    ef_100_1_05 -= bg1
    ef_100_1_05.write_data(join(processed,"ef_100_1_05_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_1_05.x,ef_100_1_05.y,  ls="solid", c="red",label="dChol 100_1_05")
    
    ef_100_2_05 = loader(make_filename(139250))
    mean = np.mean(ef_100_2_05.y[np.logical_and(ef_100_2_05.x>=0.16,ef_100_2_05.x<=0.32)])
    ef_100_2_05 *= bg_mean/mean
    ef_100_2_05 -= bg1
    ef_100_2_05.write_data(join(processed,"ef_100_2_05_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_2_05.x,ef_100_2_05.y, ls="--", c="red", label="dChol 100_2_05")
    
    bg1 = loader(make_filename(139022))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_100_1_10 = loader(make_filename(139157))
    mean = np.mean(ef_100_1_10.y[np.logical_and(ef_100_1_10.x>=0.16,ef_100_1_10.x<=0.32)])
    ef_100_1_10 *= bg_mean/mean
    ef_100_1_10 -= bg1
    ef_100_1_10.write_data(join(processed,"ef_100_1_10_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_1_10.x,ef_100_1_10.y, ls="solid", c="green",label="dChol 100_1_10")
    
    ef_100_2_10 = loader(make_filename(139276))
    mean = np.mean(ef_100_2_10.y[np.logical_and(ef_100_2_10.x>=0.16,ef_100_2_10.x<=0.32)])
    ef_100_2_10 *= bg_mean/mean
    ef_100_2_10 -= bg1
    ef_100_2_10.write_data(join(processed,"ef_100_2_10_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_2_10.x,ef_100_2_10.y, ls="--", c="green",label="dChol 100_2_10")

    bg1 = loader(make_filename(139009))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_100_1_15 = loader(make_filename(139170))
    mean = np.mean(ef_100_1_15.y[np.logical_and(ef_100_1_15.x>=0.16,ef_100_1_15.x<=0.32)])
    ef_100_1_15 *= bg_mean/mean
    ef_100_1_15 -= bg1
    ef_100_1_15.write_data(join(processed,"ef_100_1_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_1_15.x,ef_100_1_15.y, ls="solid", c="purple",label="dChol 100_1_15")
    ef_100_2_15 = loader(make_filename(139302))
    mean = np.mean(ef_100_2_15.y[np.logical_and(ef_100_2_15.x>=0.16,ef_100_2_15.x<=0.32)])
    ef_100_2_15 *= bg_mean/mean
    ef_100_2_15 -= bg1
    ef_100_2_15.write_data(join(processed,"ef_100_2_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_100_2_15.x,ef_100_2_15.y, ls="--", c="purple",label="dChol 100_2_15")

def dand():
    bg1 = loader(make_filename(138918))
    bg1 *= 1.6
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_104_1 = loader(make_filename(138753))
    mean = np.mean(ef_104_1.y[np.logical_and(ef_104_1.x>=0.16,ef_104_1.x<=0.32)])
    ef_104_1 *= bg_mean/mean
    ef_104_1 -= bg1
    ef_104_1.write_data(join(processed,"ef_104_1_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_1.x,ef_104_1.y, ls="solid", c="blue",label="dDSPC dChol 104_1")

    ef_104_2 = loader(make_filename(138839))
    mean = np.mean(ef_104_2.y[np.logical_and(ef_104_2.x>=0.16,ef_104_2.x<=0.32)])
    ef_104_2 *= bg_mean/mean
    ef_104_2 -= bg1
    ef_104_2.write_data(join(processed,"ef_104_2_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_2.x,ef_104_2.y, ls="--", c="blue",label="dDSPC dChol 104_2")
    
    bg1 = loader(make_filename(138996))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_104_1_05 = loader(make_filename(139184))
    mean = np.mean(ef_104_1_05.y[np.logical_and(ef_104_1_05.x>=0.16,ef_104_1_05.x<=0.32)])
    ef_104_1_05 *= bg_mean/mean
    ef_104_1_05 -= bg1
    ef_104_1_05.write_data(join(processed,"ef_104_1_05_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_1_05.x,ef_104_1_05.y,  ls="solid", c="red",label="dDSPC dChol 104_1_05")
    
    ef_104_2_05 = loader(make_filename(139315))
    mean = np.mean(ef_104_2_05.y[np.logical_and(ef_104_2_05.x>=0.16,ef_104_2_05.x<=0.32)])
    ef_104_2_05 *= bg_mean/mean
    ef_104_2_05 -= bg1
    ef_104_2_05.write_data(join(processed,"ef_104_2_05_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_2_05.x,ef_104_2_05.y,  ls="--", c="red",label="dDSPC dChol 104_2_05")
    

    bg1 = loader(make_filename(139022))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
        
    ef_104_1_10 = loader(make_filename(139197))
    mean = np.mean(ef_104_1_10.y[np.logical_and(ef_104_1_10.x>=0.16,ef_104_1_10.x<=0.32)])
    ef_104_1_10 *= bg_mean/mean
    ef_104_1_10 -= bg1
    ef_104_1_10.write_data(join(processed,"ef_104_1_10_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_1_10.x,ef_104_1_10.y, ls="solid", c="green",label="dDSPC dChol 104_1_10")
    
    ef_104_2_10 = loader(make_filename(139328))
    mean = np.mean(ef_104_2_10.y[np.logical_and(ef_104_2_10.x>=0.16,ef_104_2_10.x<=0.32)])
    ef_104_2_10 *= bg_mean/mean
    ef_104_2_10 -= bg1
    ef_104_2_10.write_data(join(processed,"ef_104_2_10_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_2_10.x,ef_104_2_10.y, ls="--", c="green",label="dDSPC dChol 104_2_10")
    
    bg1 = loader(make_filename(139009))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    ef_104_1_15 = loader(make_filename(139223))
    mean = np.mean(ef_104_1_15.y[np.logical_and(ef_104_1_15.x>=0.16,ef_104_1_15.x<=0.32)])
    ef_104_1_15 *= bg_mean/mean
    ef_104_1_15 -= bg1
    ef_104_1_15.write_data(join(processed,"ef_104_1_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_1_15.x,ef_104_1_15.y,ls="solid", c="purple", label="dDSPC dChol 104_1_15")
    ef_104_2_15 = loader(make_filename(139341))
    mean = np.mean(ef_104_2_15.y[np.logical_and(ef_104_2_15.x>=0.16,ef_104_2_15.x<=0.32)])
    ef_104_2_15 *= bg_mean/mean
    ef_104_2_15 -= bg1
    ef_104_2_15.write_data(join(processed,"ef_104_2_15_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(ef_104_2_15.x,ef_104_2_15.y,ls="--", c="purple", label="dDSPC dChol 104_2_15")
    
def bnt():
    bg1 = loader(make_filename(138918))
    bg1 *= 1.6
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    bnt_4_1 = loader(make_filename(138905))
    mean = np.mean(bnt_4_1.y[np.logical_and(bnt_4_1.x>=0.16,bnt_4_1.x<=0.32)])
    bnt_4_1 *= bg_mean/mean
    bnt_4_1 -= bg1
    bnt_4_1.write_data(join(processed,"bnt_4_1_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_1.x,bnt_4_1.y,ls="solid", c="blue", label="BNT4_01")

    bnt_4_2 = loader(make_filename(139062))
    mean = np.mean(bnt_4_2.y[np.logical_and(bnt_4_2.x>=0.16,bnt_4_2.x<=0.32)])
    bnt_4_2 *= bg_mean/mean
    bnt_4_2 -= bg1
    bnt_4_2.write_data(join(processed,"bnt_4_2_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_2.x,bnt_4_2.y, ls="--", c="blue",label="BNT4_02, verdünnt 1:1") 
    
    bg1 = loader(make_filename(138996))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
    
    bnt_4_3 = loader(make_filename(138983))
    mean = np.mean(bnt_4_3.y[np.logical_and(bnt_4_3.x>=0.16,bnt_4_3.x<=0.32)])
    bnt_4_3 *= bg_mean/mean
    bnt_4_3 -= bg1
    bnt_4_3.write_data(join(processed,"bnt_4_3_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_3.x,bnt_4_3.y,  ls="solid", c="red",label="BNT4_03")
    
    bnt_4_4 = loader(make_filename(139079))
    mean = np.mean(bnt_4_4.y[np.logical_and(bnt_4_4.x>=0.16,bnt_4_4.x<=0.32)])
    bnt_4_4 *= bg_mean/mean
    bnt_4_4 -= bg1
    bnt_4_4.write_data(join(processed,"bnt_4_4_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_4.x,bnt_4_4.y, ls="--", c="red", label="BNT4_04, verdünnt 1:1")
    
    bg1 = loader(make_filename(139022))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
        
    bnt_4_5 = loader(make_filename(139035))
    mean = np.mean(bnt_4_5.y[np.logical_and(bnt_4_5.x>=0.16,bnt_4_5.x<=0.32)])
    bnt_4_5 *= bg_mean/mean
    bnt_4_5 -= bg1
    bnt_4_5.write_data(join(processed,"bnt_4_5_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_5.x,bnt_4_5.y,ls="solid", c="green", label="BNT4_03, verdünnt 1:1")
    
    bnt_4_6 = loader(make_filename(139092))
    mean = np.mean(bnt_4_6.y[np.logical_and(bnt_4_6.x>=0.16,bnt_4_6.x<=0.32)])
    bnt_4_6 *= bg_mean/mean
    bnt_4_6 -= bg1
    bnt_4_6.write_data(join(processed,"bnt_4_6_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_6.x,bnt_4_6.y,ls="--", c="green", label="BNT4_04, verdünnt 1:6")    
    
    bg1 = loader(make_filename(139009))
    bg_mean = np.mean(bg1.y[np.logical_and(bg1.x>=0.16,bg1.x<=0.32)])
        
    bnt_4_7 = loader(make_filename(139049))
    mean = np.mean(bnt_4_7.y[np.logical_and(bnt_4_7.x>=0.16,bnt_4_7.x<=0.32)])
    bnt_4_7 *= bg_mean/mean
    bnt_4_7 -= bg1
    bnt_4_7.write_data(join(processed,"bnt_4_7_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_7.x,bnt_4_7.y, ls="solid", c="purple",label="BNT4_07")
    bnt_4_8 = loader(make_filename(139105))
    mean = np.mean(bnt_4_8.y[np.logical_and(bnt_4_8.x>=0.16,bnt_4_8.x<=0.32)])
    bnt_4_8 *= bg_mean/mean
    bnt_4_8 -= bg1
    bnt_4_8.write_data(join(processed,"bnt_4_8_noBG.dat"), "#Q[1/nm]\tIntensity[1/cm]\tError Intensity\n")
    plt.loglog(bnt_4_8.x,bnt_4_8.y, ls="--", c="purple",label="BNT4_08")
    
def main():
    
    plt.clf()

    # backgrounds()
    # d2o_samples()
    # d2o_noBG_samples()
    # d2o95_samples()
    # d2o90_samples()
    # d2o85_samples()
    # original_samples()
    # ddspc()
    # dchol()
    # dand()
    bnt()
    
    plt.title("BNT Samples")
    plt.xlabel("Q [1/nm]")
    plt.ylabel("Intensity [1/cm]")
    
    make_plot_nice()
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    main()