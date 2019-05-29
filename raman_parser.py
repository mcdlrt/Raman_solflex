# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:33:34 2019

@author: LM254515
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit 
import matplotlib.pyplot as plt
import os
import time
#test
class raman_spectrum:
    """parse and fit .txt single silicon raman spectrum from a horiba Raman spectrometer
    
    Uses a lsq method to fit a loretzian curve to a raman peak of silicon
    
    Args :
        filename (str): .txt filename created by sofware Labspec...
        wn_min (float,default = 480): lower wave number limit in cm^-1 
        wn_max (float,default = 560): higher wave number limit in cm^-1
    
    Attributes :
        filename (str): filename of the raman spectrum
        data(pandas dataframe): contains wavenumbers as index ands counts
        header (pandas dataframe): contains file header
        wn_min (float,default = 480): lower wave number limit in cm^-1 
        wn_max (float,default = 560): higher wave number limit in cm^-1
        x (float array): wave number array used for fit
        y (flaat array): counts/s number used for fit
    
    Methods :
        fit : fit a lorentziand function to the experimental datas
        plot: plot experimental data and fit results
    
    
    """
    def lorentzian(self,x,x0,a,gam,c):
        return a * gam**2 / ( gam**2 + ( x - x0 )**2)+c
            
    def __init__(self,filename,wn_min=490,wn_max=550):
        try: 
            self.filename = filename
            self.data = pd.read_csv(self.filename,header = 35, sep = '\t',names = ['wavenumber','counts'],index_col = 0 )
            self.header = pd.read_csv(self.filename,sep = '=\t',nrows = 35,names = ["parameter","value"],engine ='python')
            self.wn_min = wn_min
            self.wn_max = wn_max
            self.epoch = time.mktime(time.strptime(self.header.value[34],"%d.%m.%Y %H:%M:%S"))      # date of scan since epoch in s
                
        except IOError:
            print("file {} not found!".format(filename))
            pass
            
    def fit(self):
        """function used to fit raman data with a lorenztian curve
        """
        self.x = self.data.index[(self.data.index>=self.wn_min)&(self.data.index<=self.wn_max)].values
        self.y = self.data.counts[self.wn_min:self.wn_max].values / float(self.header.value[0])         # counts per second
        
        self.p0 = [self.x[self.y.argmax()], 1,2,0]     # initial values for fit parameters
        [self.popt, self.pcov] = curve_fit(self.lorentzian,self.x,self.y,self.p0)
    
    def plot(self,output_folder= os.getcwd):
        """Method to plot experimental data and fit results in a choosen folder
        """
        self.fit()
        fig1 = plt.figure()
        plt.plot(self.x,self.y,'bo')
        plt.plot(self.x , self.lorentzian(self.x,self.popt[0],self.popt[1],self.popt[2],self.popt[3]))
        plt.xlabel('Wave number $cm^{-1}$')
        plt.ylabel('Counts per second')
        plt.show()

