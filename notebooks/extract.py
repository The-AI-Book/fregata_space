import sys
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen

class globir:

    def __init__(self, url):
        self.url=url
        self.arr=[]
        self.year=''
        self.day=''
        self.hour=''
        self.min=''
        
    def set_time(self):
        self.year=self.url[-10:-8]
        self.day=self.url[-8:-5]
        self.hour=self.url[-4:-2]
        self.min=self.url[-2:]

    def extract_arr(self):
        with urlopen(self.url) as x:
            IN = x.read(768)
        header=struct.unpack('<192I',IN)
        # Extract the data parameters
        lines=header[8]
        elements=header[9]
        arraySize=lines*elements
        format="%4dB" % (arraySize)
        dataOffset=header[33]   # offset to data array (bytes)
        with urlopen(self.url) as x:
            X = x.read(arraySize)
        # Read image array into a 1D array

        array=struct.unpack(format, X)

        # Set up 2D array and reshape to 2D array to plot the data
        array2D=[]
        for n in range(0,lines):
            array2D.append(array[n*elements:(n+1)*elements])
        self.arr=np.array(array2D)
    def show_arr(self):
        return self.arr
    def show_im(self):
        plt.figure(figsize=(30,20))
        fig=plt.imshow(self.arr, cmap='gray', interpolation='none')
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.show()
 