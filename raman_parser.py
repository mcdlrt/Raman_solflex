# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:33:34 2019

@author: LM254515
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit 

class raman_spectrum:
    def __init__(self,filename,wn_min,wn_max):
        try:
            with open(filename,'rU') as f:
                self.filename = f
                self.data = pd.read_csv(f,header = 35, sep = '\t',names = ['wavenumber','counts'],index_col = 0 )
                self.header = pd.read_csv(f,sep = '=\t',nrows = 35,names = ["parameter","value"],engine ='python')
                self.wn_min = wn_min
                self.wn_max = wn_max 
                
        except IOError:
            print("file {} not found!".format(filename))
            pass
            
    def __fit__(self):
        x = self.data.index[(self.data.index>=sel.wn_min)&(self.data.index<=self.wn_max)]
        y = self.data.counts[self.wn_min,self.wn_max]
        self.fit = curve_fit(__lorentzian__,x,y)
    def __lorentzian__(x,x0,a,gam):
        return a * gam**2 / ( gam**2 + ( x - x0 )**2)
