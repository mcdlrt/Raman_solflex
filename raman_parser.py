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

class raman_mapping_z :
    """Parse and fit xy Silion Raman z scan
    Uses a lsq method to fit a lorentzian curve
    
    Args :
        filename (str): .txt filename created by sofware Labspec...
        wn_min (float,default = 480): lower wave number limit in cm^-1 
        wn_max (float,default = 560): higher wave number limit in cm^-1
    
    Attributes : 
        x
        y
        peak_pos
    
    Methods : 
        
    """
    def __init__(self, filename,wn_min=490,wn_max=550,ref_si = 520.7,cmap = 'coolwarm'):
        self.filename = filename
        self.wn_min = wn_min
        self.wn_max = wn_max
        self.ref_si = ref_si
        try : 
            self.data = pd.read_csv(self.filename,header = 35, sep = '\t',index_col = 0)
            self.data.rename(columns = {'Unnamed: 0':'z'},inplace=True)
            self.header = pd.read_csv(self.filename,sep = '=\t',nrows = 34,names = ["parameter","value"],engine ='python')
            wn = self.data.columns[1:]
            self.wn = np.array([float(iii) for iii in wn])
            self.z = self.data.index
            self.id_min = np.argmax(self.wn>wn_min)
            self.id_max = np.argmin(self.wn<wn_max)
        except IOError:
            print("file {} not found!".format(filename))
            pass
        
    def lorentzian(self,x,x0,a,gam,c):
        return a * gam**2 / ( gam**2 + ( x - x0 )**2)+c
    def fit(self,iii,p0 = [520,1,2,0]):
          self.x_fit = self.wn[self.id_min:self.id_max]
          self.y_fit = self.data.values[iii,self.id_min:self.id_max]
          self.p0 = p0
          [self.popt, self.pcov] = curve_fit(self.lorentzian,self.x_fit,self.y_fit,p0 = self.p0)
          self.peak_pos = self.popt[0]
          
    def fit_zscan(self):
        peak_shift_array = np.zeros_like(self.z)
        peak_intensity_array = np.zeros_like(self.z)
        for iii,z_i in enumerate(self.z) :
            try :
                self.fit()
                peak_shift_array = self.peak_pos
                peak_shift_array = self.popt[1]
            except RuntimeError:
                peak_shift_array[iii] = np.nan
                peak_intensity_array[iii] =np.nan
        self.peak_shift_array = peak_shift_array
        self.peak_intensity_array = peak_intensity_array
        
    def plot_zscan(self):
        self.fit_zscan()
        plt.figure()
        plt.plot(self.z, self.peak_intensity_array,'o')
class raman_mapping_xy :
    """Parse and fit xy Silion Raman mapping
    Uses a lsq method to fit a lorentzian curve
    
    Args :
        filename (str): .txt filename created by sofware Labspec...
        wn_min (float,default = 480): lower wave number limit in cm^-1 
        wn_max (float,default = 560): higher wave number limit in cm^-1
    
    Attributes : 
        x
        y
        peak_pos
    
    Methods : 
        
    """
    def __init__(self,filename,wn_min=490,wn_max=550,ref_si = 520.7,cmap = 'coolwarm'):
        self.filename = filename
        self.wn_min = wn_min
        self.wn_max = wn_max
        self.ref_si = ref_si
        self.cmap = cmap
        try :
            self.data = pd.read_csv(self.filename,header = 35, sep = '\t')
            self.data.rename(columns = {'Unnamed: 0':'x','Unnamed: 1':'y'},inplace=True)
            self.data.rename(columns={c: float(c) for c in self.data.columns[2:]})
            
            self.header = pd.read_csv(self.filename,sep = '=\t',nrows = 34,names = ["parameter","value"],engine ='python')
            wn = self.data.columns[2:]
            self.wn = np.array([float(iii) for iii in wn])    # list of wavenumber
            self.x = self.data.x.unique()                       # x values in µm
            self.y = self.data.y.unique()                       # y valles in µm
        except IOError:
            print("file {} not found!".format(filename))
            pass
        self.id_min = np.argmax(self.wn>wn_min)
        self.id_max = np.argmin(self.wn<wn_max)

    def lorentzian(self,x,x0,a,gam,c):
        return a * gam**2 / ( gam**2 + ( x - x0 )**2)+c
        
    def fit(self,iii,jjj,p0 = [520,1,2,0]):
        """Method used to fit raman data with a lorenztian curve
        Args :
            iii (int): x indices
            jjj (int): y indices
        """
        self.x_fit = self.wn[self.id_min:self.id_max]
        self.y_fit = self.data.values[iii*np.size(self.y)+jjj,self.id_min:self.id_max] / float(self.header.value[0])         # counts per second
        
        self.p0 = p0
        [self.popt, self.pcov] = curve_fit(self.lorentzian,self.x_fit,self.y_fit,p0 = self.p0)
        self.peak_pos = self.popt[0]
        
    def fit_map(self):
        """Method used to map Raman shift
        
        """
        peak_shift_array = np.zeros([np.size(self.x),np.size(self.y)])
        for iii,el_x in enumerate (self.x):
            for jjj,el_y in enumerate(self.y):
                
                try :
                    self.fit(iii,jjj)
                    peak_shift_array[iii,jjj] = self.peak_pos -self.ref_si
                except RuntimeError:
                    peak_shift_array[iii,jjj] = np.nan
        self.peak_shift_array = peak_shift_array
    def plot_map_shift(self):
        
        self.fit_map()
        fig = plt.figure()
        plt.imshow(self.peak_shift_array,cmap=self.cmap
                        ,vmin = -5, vmax = 5
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
                        
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Raman shift $cm^{-1}$')
        plt.show()
     
    def strain110(self):
       self.fit_map()
       b_110 = -337
       self.eps_110 = self.peak_shift_array / b_110
       
    def strain_biax(self) :
        self.fit_map()
        b_biax = -733
        self.eps_biax = self.peak_shift_array / b_biax
        
    def strain100(self):
        self.fit_map()
        b_100 = -1
        self.eps_100 = self.peak_shift_array / b_100
        
    def plot_strain110(self):
        self.strain110()
        fig = plt.figure()
        plt.imshow(self.eps_110,cmap=self.cmap
                        ,vmin = -5, vmax = 5
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
                        
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Uniaxial strain along [110] %%')
        plt.show()
        
    def plot_strain100(self):
        self.strain100()
        fig = plt.figure()
        plt.imshow(self.eps_100,cmap=self.cmap
                        ,vmin = -5, vmax = 5
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
                        
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Uniaxial strain along [100] %%')
        plt.show()

    def plot_biax(self):
        self.strain_biax()
        fig = plt.figure()
        plt.imshow(self.eps_biax,cmap=self.cmap
                        #,vmin = -5, vmax = 5
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
                        
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Biaxial strain %%')
        plt.show()                
        
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
            #self.epoch = time.mktime(time.strptime(self.header.value[34],"%d.%m.%Y %H:%M:%S"))      # date of scan since epoch in s
                
        except IOError:
            print("file {} not found!".format(filename))
            pass
            
    def fit(self):
        """Mehod used to fit raman data with a lorenztian curve
        """
        self.x = self.data.index[(self.data.index>=self.wn_min)&(self.data.index<=self.wn_max)].values
        self.y = self.data.counts[self.wn_min:self.wn_max].values / float(self.header.value[0])         # counts per second
        
        self.p0 = [self.x[self.y.argmax()], 1,2,0]     # initial values for fit parameters
        [self.popt, self.pcov] = curve_fit(self.lorentzian,self.x,self.y,self.p0)
        self.peak_pos = self.popt[0]
    
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

