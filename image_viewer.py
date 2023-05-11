# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:12:17 2023

@author: klaus
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def create_filenames(path, start,stop):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = r"{}/latest_{:07d}_craw.tiff".format(path, i)
        result.append(filename)
        
    return result

def make_filenames(path, numbers):
    result=[]
    
    for i in numbers:
        filename = r"{}/latest_{:07d}_craw.tiff".format(path, i)
        result.append(filename)
        
    return result


def main():
    path = "Z:/Klaus/Data/LipidNanoparticles/SAXS/230509_LNP_ILL_Beamtime/rawdata"
    files = create_filenames(path, 91385,91459)

    for file in files:
        plt.clf()
        plt.title(file)
        i = np.array(Image.open(file))
        plt.imshow(i,norm=LogNorm())
        plt.show()
        
        
if __name__ == '__main__':
    main()
