import sys
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
import utm
class globir:

    def __init__(self, url):
        self.url=url
        self.arr=[]
        self.year=''
        self.day=''
        self.hour=''
        self.min=''
        self.sx=9900
        self.sy=5400
    def set_time(self):
        self.year=self.url[-10:-8]
        self.day=self.url[-8:-5]
        self.hour=self.url[-4:-2]
        self.min=self.url[-2:]
    def extract_local_arr(self):
        IN=open(self.url, 'rb')
    # Read the first 768 bytes of the file containing the header and navigation information
        dataOffset=768
        header=struct.unpack('<192I', IN.read(768))
 
    # Extract the data parameters
        lines=header[8]
        elements=header[9]
        arraySize=lines*elements
        format="%4dB" % (arraySize)
        dataOffset=header[33]   # offset to data array (bytes)
 
    # Read image array into a 1D array
        IN.seek(dataOffset)
        array=struct.unpack(format, IN.read(arraySize))
        IN.close()
 
    # Set up 2D array and reshape to 2D array to plot the data
        array2D=[]
        for n in range(0,lines):
            array2D.append(array[n*elements:(n+1)*elements])
        self.arr=np.array(array2D)
    def cut(self,lon,lat):
        array2D=[]
        #lat0,lat1= convert_mer_px(lat)
        self.arr=self.arr[lat[0]:lat[1]]   
        self.sy=lat[1]-lat[0]
        for row in self.arr:
            array2D.append(row[lon[0]:lon[1]])
        self.arr=np.array(array2D)
        self.sx=lon[1]-lon[0]
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
         day=int(self.day)-310
         dpi=300
         fig = plt.figure(frameon=False)
         fig.set_size_inches(self.sx/dpi*(948/310), self.sy*(948/310)/dpi)
         ax = plt.Axes(fig, [0., 0., 1., 1.])
         ax.set_axis_off()
         fig.add_axes(ax)
         ax.imshow(self.arr,cmap='gray',interpolation='none')
         plt.savefig(str(day)+'.png',pad_inches=0.0, bbox_inches='tight',dpi=300)
         plt.close()
       # plt.figure()
        #fig=plt.imshow(self.arr, cmap='gray', interpolation='none')
        #fig.set_size_inches(self.sx/300,self.sy/300)
        #plt.axis('off')
        #fig.axes.get_xaxis().set_visible(False)
        #fig.axes.get_yaxis().set_visible(False)
        #day=int(self.day)-310
        #plt.savefig(str(day)+'.png',pad_inches=0.0, bbox_inches='tight',dpi=300)
        #plt.close() 
def convert_mer_px(lat):
    south = degtorad(-61)
    north = degtorad(66)
    height=5400
    y_min=mercN(south)
    y_max=mercN(north)
    y_factor=1/(y_max-y_min)
   #----------------------------
    y_0=int( (7653/ 2) - (9900 * mercN(degtorad(lat[0])) / (2 * np.pi)))
    y_1=int((7653/ 2) - (9900* mercN(degtorad(lat[1])) / (2 * np.pi)))
    return y_0,y_1
def mercN(lat):
    return np.log(np.tan((np.pi/4)+(lat/2)))
def degtorad(deg):
    return deg*np.pi/180