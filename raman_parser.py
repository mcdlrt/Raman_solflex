# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:33:34 2019

@author: LM254515
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit 
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
        y (flaat array): counts number used for fit
    
    
    """
    def lorentzian(x,x0,a,gam,c):
        return a * gam**2 / ( gam**2 + ( x - x0 )**2)+c
            
    def __init__(self,filename,wn_min=480,wn_max=560):
        try:
            with open(filename,'rU') as f: # 
                self.filename = f
                self.data = pd.read_csv(f,header = 35, sep = '\t',names = ['wavenumber','counts'],index_col = 0 )
                self.header = pd.read_csv(f,sep = '=\t',nrows = 35,names = ["parameter","value"],engine ='python')
                self.wn_min = wn_min
                self.wn_max = wn_max 
                
        except IOError:
            print("file {} not found!".format(filename))
            pass
            
    def __fit__(self):
        self.x = self.data.index[(self.data.index>=sel.wn_min)&(self.data.index<=self.wn_max)]
        self.y = self.data.counts[self.wn_min,self.wn_max]
        p0 = []
        self.fit = curve_fit(self.lorentzian,x,y,p0)
    
