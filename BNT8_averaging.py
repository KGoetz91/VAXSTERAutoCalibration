# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:06:28 2023

@author: klaus
"""

from reduce_images import OneDLoader as loader
import numpy as np
import matplotlib.pyplot as plt

def bnt8_neu():
    plt.clf()
    
    bg1 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated/RefZucker_Pos4_AA.dat")
    bg2 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated/Ref1_Pos4_Mean_AA.dat")
    bg = (bg1+bg2)*0.5
    
    bg.make_linear(4e-2)
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT8_neu.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    plt.loglog(bg.x,bg.y,label='BG linear')
    
    
    bnt8_new1 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated/BNT8_AA.dat")
    bnt8_new2 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated/BNT8_Mean_AA.dat")
    bnt8_new2 = bnt8_new2*1.1
    
    bnt8 = (bnt8_new1+bnt8_new2)*0.5
    bnt8 = bnt8*0.89
    bnt8.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT8_neu.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    plt.loglog(bnt8.x,bnt8.y,label="BNT 8")
    bnt8_noBG = bnt8 - bg
    bnt8_noBG.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT8_neu_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    # plt.loglog(bnt8_new1.x,bnt8_new1.y,label="1")
    # plt.loglog(bnt8_new2.x,bnt8_new2.y,label="2")
    plt.loglog(bnt8_noBG.x,bnt8_noBG.y,label="BNT 8 no BG")

    plt.legend()
    plt.show()

def bnt10_neu():
    plt.clf()
    
    bg1 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated/RefZucker_Pos4_AA.dat")
    bg2 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated/Ref1_Pos4_Mean_AA.dat")
    bg = (bg1+bg2)*0.5
    
    bg.make_linear(4e-2)
    plt.loglog(bg.x,bg.y,label='BG linear')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT10_neu.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    
    sample1 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated/BNT10_AA.dat")
    sample2 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated/BNT10_Mean_AA.dat")
    sample2 = sample2*1.1
    
    # plt.loglog(sample1.x,sample1.y,label="1")
    # plt.loglog(sample2.x,sample2.y,label="2")
    
    sample = (sample1+sample2)*0.5
    sample = sample*0.95
    plt.loglog(sample.x,sample.y,label="BNT 10 average")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT10_neu.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    sample_noBG = sample - bg
    plt.loglog(sample_noBG.x,sample_noBG.y,label="BNT 10 no BG")
    
    sample_noBG.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT10_neu_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    
    plt.legend()
    plt.show()

def bnt_8_alt():
    plt.clf()
    
    # bg1 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230313_WiederholungBNT8910/calibrated/RefZucker_Pos4_AA.dat")
    # bg2 = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230315_BNT810Ref1_absoluteCalibration_30minRepeatMeasurements/calibrated/Ref1_Pos4_Mean_AA.dat")
    # bg = (bg1+bg2)*0.5
    
    # plt.loglog(bg.x,bg.y,label='BG linear absolut')
    # bg.make_linear(4e-2)
    # plt.loglog(bg.x,bg.y,label='BG linear absolut')
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/RefZucker_AA.dat")
    # plt.loglog(bg.x,bg.y,label='BG')
    bg.make_linear(3e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT8_alt.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/BNT8_AA.dat")
    sample = sample*0.90
    plt.loglog(sample.x,sample.y,label="BNT 8 alt")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT8_alt.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample_noBG = sample - bg
    plt.loglog(sample_noBG.x,sample_noBG.y,label="BNT 8 alt no BG")

    sample_noBG.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT8_alt_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show()    

def bnt_10_alt():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/RefZucker_AA.dat")
    bg.make_linear(3e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT10_alt.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/BNT10_AA.dat")
    sample = sample*0.98
    plt.loglog(sample.x,sample.y,label="BNT 10 alt")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT10_alt.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    sample_noBG = sample - bg
    plt.loglog(sample_noBG.x,sample_noBG.y,label="BNT 10 alt no BG")

    sample_noBG.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT10_alt_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show()

def bnt_15():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/RefZucker_AA.dat")
    bg.make_linear(3e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT15.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/BNT15_AA.dat")
    sample = sample*1.07
    plt.loglog(sample.x,sample.y,label="BNT 15")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT15.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 15 no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT15_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show()

def bnt_16():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/RefZucker_AA.dat")
    bg.make_horizontal(0.07,3e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT16.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/BNT16_AA.dat")
    sample = sample*1.03
    plt.loglog(sample.x,sample.y,label="BNT 16")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT16.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 16 no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT16_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show()

def bnt_21():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/RefZucker_AA.dat")
    bg.make_linear(3e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT21.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/BNT21_AA.dat")
    sample = sample*1.05
    plt.loglog(sample.x,sample.y,label="BNT 21")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT21.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 21 no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT21_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show()        

def bnt_21_dia():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230321_BNT1621_nachDialyse_einkonzentriert/calibrated/Referenz_Mean_AA.dat")
    bg.make_linear(6e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT21_dia.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230321_BNT1621_nachDialyse_einkonzentriert/calibrated/BNT21_dia_conc_Mean_AA.dat")
    sample = sample*0.9
    plt.loglog(sample.x,sample.y,label="BNT 21 dia")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT21_dia_conc.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 21 dia no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT21_dia_conc_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show() 

def bnt_16_dia():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230321_BNT1621_nachDialyse_einkonzentriert/calibrated/Referenz_Mean_AA.dat")
    bg.make_linear(6e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT16_dia.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230321_BNT1621_nachDialyse_einkonzentriert/calibrated/BNT16_dia_conc_Mean_AA.dat")
    sample = sample*0.90
    plt.loglog(sample.x,sample.y,label="BNT 16 dia")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT16_dia_conc.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 16 dia no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT16_dia_conc_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show() 

def bnt_15_dia():
    plt.clf()
    
    # bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230321_BNT1621_nachDialyse_einkonzentriert/calibrated/Referenz_Mean_AA.dat")
    # bg.make_linear(6e-2)
    
    # plt.loglog(bg.x,bg.y,label='BG abs')
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/RefNoSugar_AA.dat")
    # plt.loglog(bg.x,bg.y,label='BG')
    # bg.make_horizontal(0.0295,4e-2)
    
    plt.loglog(bg.x,bg.y,label='BG')
    bg.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/RefZucker_zuBNT15_dia.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230216_MessungenBNT8_9_10/calibrated/BNT15_dialysiert_AA.dat")
    sample = sample*1.2
    plt.loglog(sample.x,sample.y,label="BNT 15 dia")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT15_dia.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 15 dia no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/BNT15_dia_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')

    plt.legend()
    plt.show()

def B_EF0018():
    plt.clf()
    
    bg_ref = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230321_BNT1621_nachDialyse_einkonzentriert/calibrated/Referenz_Mean_AA.dat")
    # bg_ref.make_linear(6e-2)
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated/Referenz_Mean_AA.dat")
    bg *= 0.96
    # plt.loglog(bg.x,bg.y, label="BG")
    # bg.make_horizontal(0.0297,1e-1)
    
    # plt.loglog(bg_ref.x,bg_ref.y, label='BG Ref')
    plt.loglog(bg.x,bg.y, label="BG")
    
    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated/B_EF0018_Mean_AA.dat")
    sample = sample*0.99
    plt.loglog(sample.x,sample.y,label="BNT 15 dia")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/B_EF0018.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 15 dia no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/B_EF0018_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    plt.legend()
    
    plt.show()

def A_EF0065():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated/Referenz_Mean_AA.dat")
    bg *= 0.97
    # bg.make_horizontal(0.03,1e-1)
    
    plt.loglog(bg.x,bg.y, label="BG")
    
    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated/A_EF0065_Mean_AA.dat")
    sample = sample*0.93
    plt.loglog(sample.x,sample.y,label="BNT 15 dia")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/A_EF0065.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 15 dia no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/A_EF0065_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    plt.legend()
    
    plt.show()

def B_EF0046():
    plt.clf()
    
    bg = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated/Referenz_Mean_AA.dat")
    bg *= 0.97
    # bg.make_horizontal(0.03,1e-1)
    
    plt.loglog(bg.x,bg.y, label="BG")
    
    sample = loader("Z:/Klaus/Data/LipidNanoparticles/SAXS/230327_EFSamples/calibrated/B_EF0046_Mean_AA.dat")
    sample = sample*0.83
    plt.loglog(sample.x,sample.y,label="BNT 15 dia")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/B_EF0046.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    sample = sample - bg
    plt.loglog(sample.x,sample.y,label="BNT 15 dia no BG")
    sample.write_data("Z:/Klaus/Data/LipidNanoparticles/SAXS/FinalDataSets/B_EF0046_noBG.dat", '#Q[AA^-1]\tIntensity[cm^-1]\tError\n')
    
    plt.legend()
    
    plt.show()

def main():
    # bnt8_neu()
    # bnt10_neu()
    # bnt_8_alt()
    # bnt_10_alt()
    # bnt_15()
    # bnt_16()
    # bnt_21()
    # bnt_21_dia()
    bnt_16_dia()
    # bnt_15_dia()
    #B_EF0018()
    #A_EF0065()
    #B_EF0046()
    
if __name__ == '__main__':
    main()