# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:12:17 2023

@author: klaus
"""

from reduce_images import TwoDDataset as Image

import matplotlib.pyplot as plt

def create_filenames(start,stop):
    
    result=[]
    
    for i in range(start,stop+1):
        filename = r"./rawdata/latest_{:07d}_craw.tiff".format(i)
        result.append(filename)
        
    return result

def main():
    files = create_filenames(88248, 88259)
    for file in files:
        i = Image(file, "saxs_poni.poni")
        i.plotImage()
        # plt.xlim((200,300))
        # plt.ylim((250,400))
        # plt.show()
        
        
if __name__ == '__main__':
    main()
