# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:33:34 2019

@author: LM254515

Contains different class for parsing and fiting Raman spectrum of Si obtain on a Horiba Labram HR
laurent.g.michaud@gmail.com
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
import time

def headersize(filename):
    """return line index of last parameter in the header of any raman scan txt file
    args
    """
    try:
        with open(filename, 'rU') as f:
            l_i = 0
            l = f.readline().replace('\n', '')
            while l != '\n' and l != '' and l.find('=') != -1:
                l = f.readline().replace('\n', '')
                l_i += 1
                
    except IOError:
            print("file {} not found!".format(filename))            
    except:
        print('could not reader header size of {:}'.format(filename))
    return l_i
                
def lorentzian(x, x0, a, gam, c):
    """Lorentzian function
    Args:
        x = input x value array
        x0 = peak position
        a = intensitie factor
        gam = width
        c = baseline
    Return:
        lenrezian_function(x) (array)            
    """
    return a * gam**2/(gam**2 +(x-x0)**2)+c

class raman_time_scan:
    """Parse and fit Time scan for Si Raman measurement
    Args:
        filename(string) = path and filename of .txt Raman timescan
        wn_min (float, default=490): lower wave number limit in cm^-1
        wn_max (float ,default=550): higher wave number limit in cm^-1
        ref_si (float, default=520.7) : Raman shift of reference Si sample
    Metods:
        fit : fit single scan at a defined time with a lorentzian function
        fit_tscan : fit every scan of the file using fit function
        plot_tscan : plot peak shift as a function of time
    
    """
    def __init__(self, filename, wn_min=490, wn_max=550, ref_si=520.7):
        self.filename = filename
        self.wn_min = wn_min
        self.wn_max = wn_max
        self.ref_si = ref_si
        try:
            self.hs = headersize(self.filename)
            self.data = pd.read_csv(self.filename, header=self.hs, sep='\t', index_col=0) #
            self.data.rename(columns={'Unnamed: 0':'time'}, inplace=True)
            self.header = pd.read_csv(self.filename,
                                      sep='=\t',
                                      nrows=self.hs,
                                      names=["parameter", "value"],
                                      engine='python')
            wn = self.data.columns[1:]
            self.wn = np.array([float(jjj) for jjj in wn])
            self.time = self.data.index
            self.id_min = np.argmax(self.wn > wn_min)
            self.id_max = np.argmin(self.wn < wn_max)
            self.epoch = time.mktime(time.strptime(
                    self.header[self.header['parameter'].str.match('Acquired')].values[0, 1],
                    "%d.%m.%Y %H:%M:%S"))      # date of scan since epoch in s
            # date of scan since epoch in s
            self.time_epoch = self.time + self.epoch
            self.duration = float(self.header.value[1])*float(self.header.value[0])

        except IOError:
            print("file {} not found!".format(filename))
        except IndexError:
            print('index error')

    def fit_tscan(self):
        """Method to fit silicon raman peak as a function of time
        Attributes:
            peak_shift_array =
            peak_intensity_array =
            surf_z =
            fit =
        """
        peak_shift_array = np.zeros(self.time.size)
        peak_intensity_array = np.zeros(self.time.size)
        for iii, t_i in enumerate(self.time):
            try:
                self.fit(iii)
                peak_shift_array[iii] = self.peak_pos
                peak_intensity_array[iii] = self.popt[1]
            except RuntimeError:
                peak_shift_array[iii] = np.nan
                peak_intensity_array[iii] = np.nan
        self.peak_shift_array = peak_shift_array
        self.peak_intensity_array = peak_intensity_array

    def fit(self, iii, p0=[520, 1, 2, 0], bounds_f=([500, 0, 0, 0], [540, 1000, 10, 100])):
        self.x_fit = self.wn[self.id_min:self.id_max]
        self.y_fit = self.data.values[iii, self.id_min:self.id_max]
        self.p0 = p0
        [self.popt, self.pcov] = curve_fit(lorentzian,
                                           self.x_fit,
                                           self.y_fit,
                                           p0=self.p0,
                                           bounds=bounds_f)
        self.peak_pos = self.popt[0]

    def plot_tscan(self):
        self.fit_tscan()
        plt.figure()
        plt.plot(self.time, self.peak_shift_array, 'ko')
        plt.xlabel("time (s)")
        plt.ylabel("raman shift $cm^{-1}$")
        plt.show()

class raman_mapping_z:
    """Parse and fit  Silion Raman z scan
    Uses a lsq method to fit a lorentzian curve

    Args:
        filename(string) = path and filename of .txt Raman z mapping
        wn_min (float, default=490): lower wave number limit in cm^-1
        wn_max (float ,default=550): higher wave number limit in cm^-1
        ref_si (float, default=520.7) : Raman shift of reference Si sample

    Attributes:
        filename (string) : filname of .txt Raman z mapping
        data (pandas.DataFrame) : contains all the data from .txt file
        header (pandas.Dataframe) : header from the txt file, parameter and value
        wn (float array) : wave number in cm^-1
        epoch : starting time of scan in epoch time (s)
        peak_pos
        peak_shift_array (np.array) : Silicon Raman shift array from the fit
        peak_intensity_array (np.array) : Intensity of the silicon Raman peak
       surf_z (float) : Relative z coordinate of the silicon surface,
           correponds to the max intensity of Silicon Raman peak
           /!\ if the surface is not in focus range, surf_z will correpsond to an extremmum
       hs (int): header size, line index of last parameter
    Methods:
        fit = fit single scan at a certain depth
        fit_zscan : fit a spectrum of the corresponding index to a lorentzian curve
        plot_zscan : plot Raman peak intensity as a function of scan relative z coordinates
    """
    def __init__(self, filename, wn_min=490, wn_max=550, ref_si=520.7, cmap='coolwarm'):
        self.filename = filename
        self.wn_min = wn_min
        self.wn_max = wn_max
        self.ref_si = ref_si
        
        try:
            self.hs = headersize(self.filename)
            self.data = pd.read_csv(self.filename,
                                    header=self.hs,
                                    sep='\t',
                                    index_col=0)
            self.data.rename(columns={'Unnamed: 0':'z'}, inplace=True)
            self.header = pd.read_csv(self.filename,
                                      sep='=\t',
                                      nrows=self.hs,
                                      names=["parameter", "value"],
                                      engine='python')
            wn = self.data.columns[1:]
            self.wn = np.array([float(iii) for iii in wn])
            self.z = self.data.index
            self.id_min = np.argmax(self.wn > wn_min)
            self.id_max = np.argmin(self.wn < wn_max)
            self.epoch = time.mktime(time.strptime(
                    self.header[self.header['parameter'].str.match('Acquired')].values[0, 1],
                    "%d.%m.%Y %H:%M:%S"))      # date of scan since epoch in s
        except IOError:
            print("file {} not found!".format(filename))

    def fit(self, iii,p0=[520, 1, 2, 0], bounds_f=([500, 0, 0, 0], [540, 1000, 10, 100])):
        self.x_fit = self.wn[self.id_min:self.id_max]
        self.y_fit = self.data.values[iii,self.id_min:self.id_max]
        self.p0 = p0
        [self.popt, self.pcov] = curve_fit(lorentzian, self.x_fit, self.y_fit, p0=self.p0, bounds=bounds_f)
        self.peak_pos = self.popt[0]
          
    def fit_zscan(self):
        """Method to fit silicon raman peak as a function of scan depth
        Attributes:
            peak_shift_array =
            peak_intensity_array = 
            surf_z = 
            fit = 
        """
        peak_shift_array = np.zeros(self.z.size)
        peak_intensity_array = np.zeros(self.z.size)
        for iii,z_i in enumerate(self.z):
            try:
                self.fit(iii)
                peak_shift_array[iii] = self.peak_pos
                peak_intensity_array[iii] = self.popt[1]
            except RuntimeError:
                peak_shift_array[iii] = np.nan
                peak_intensity_array[iii] =np.nan
        self.peak_shift_array = peak_shift_array
        self.peak_intensity_array = peak_intensity_array
        self.surf_z = self.z[self.peak_intensity_array.argmax()]

    def plot_zscan(self):
        self.fit_zscan()
        plt.figure()
        plt.plot(self.z, self.peak_intensity_array, 'ko')
        plt.xlabel("z (um)")
        plt.ylabel("raman shift intsity (cts/s)")
        plt.show()
class raman_mapping_xy :
    """Parse and fit xy Silion Raman mapping
    Uses a lsq method to fit a lorentzian curve
    
    Args :
        filename (str): .txt filename created by sofware Labspec...
        wn_min (float,default = 480): lower wave number limit in cm^-1 
        wn_max (float,default = 560): higher wave number limit in cm^-1
        ref_si (float, default=520.7) : Raman shift of reference Si sample
        eps_range (float, default = 0) : range of strain for imshow plot vmin = - eps_range, vmax = eps_range

    
    Attributes : 
        x (np.array) : x array (µm)
        y (np.array) : y array (µm)
        peak_pos
        peak_shift_array (np.array) : Matrix of Silicon Raman shift, relative to the Si_ref value
        eps_110 (np.array) : strain in a case of Si 100 crystal strained along <110> direction
        eps_100 (np.array) : strain in a case of Si 100 crystal strained along <100> direction
        eps_biax (np.array) : strain in a case of Si 100 crystal strained biaxialy in a 100 plane
        hs (int): header size, line index of last parameter
        filename (string) : filname of .txt Raman z mapping
        data (pandas.DataFrame) : contains all the data from .txt file
        header (pandas.Dataframe) : header from the txt file, parameter and value
        wn (float array) : wave number in cm^-1        
    Methods : 
        fit : fit scan in a certain x,y point
        fit_map : fit the whole xy map and create peak_shift_array attribute
        plot_biax : plot biaxial strain using imshow
        plot_strain100 : plot uniaxial strain along [100] direction using imshow
        plot_strain110 : plot uniaxial strain along [110] using imshow
    """
    def __init__(self, filename, wn_min=490, wn_max=550, ref_si = 520.7,cmap='coolwarm',eps_range = 0):
        self.filename = filename
        self.wn_min = wn_min
        self.wn_max = wn_max
        self.ref_si = ref_si
        self.cmap = cmap
        self.hs = headersize(self.filename)
        self.eps_range = eps_range
        try:
            self.data = pd.read_csv(self.filename, header=self.hs, sep='\t')
            self.data.rename(columns={'Unnamed: 0':'x','Unnamed: 1':'y'}, inplace=True)
            self.data.rename(columns={c: float(c) for c in self.data.columns[2:]})
            self.header = pd.read_csv(self.filename, sep = '=\t', nrows=self.hs, names=["parameter", "value"], engine='python')
            wn = self.data.columns[2:]
            self.wn = np.array([float(iii) for iii in wn])    # list of wavenumber
            self.x = self.data.x.unique()                       # x values in µm
            self.y = self.data.y.unique()                       # y valles in µm
            #self.epoch = time.mktime(time.strptime(self.header[self.header['parameter'].str.match('Acquired')].values[0,1],"%d.%m.%Y %H:%M:%S")) 
            
        except IOError:
            print("file {} not found!".format(filename))
            pass
        self.id_min = np.argmax(self.wn > wn_min)
        self.id_max = np.argmin(self.wn < wn_max)
        try:
            self.z = self.header[self.header['parameter'].str.contains('Z ')].values[0, 1]
        except:
            print('Z axis value not stored in {:}'.format(self.filename))
            

    def fit(self, iii, jjj, p0=[520, 1, 2, 0], bounds_f=([500, 0, 0, 0], [540, 1000, 10, 100])):
        """Method used to fit raman data with a lorenztian curve
        Args :
            iii (int): x indices
            jjj (int): y indices
        """
        self.x_fit = self.wn[self.id_min:self.id_max]
        self.y_fit = self.data.values[iii*np.size(self.y)+jjj, self.id_min:self.id_max] / float(self.header.value[0])         # counts per second

        self.p0 = p0
        [self.popt, self.pcov] = curve_fit(lorentzian, self.x_fit, self.y_fit,p0=self.p0, bounds=bounds_f)
        self.peak_pos = self.popt[0]

    def fit_map(self):
        """Method used to map Raman shift
        
        """
        peak_shift_array = np.zeros([np.size(self.x),np.size(self.y)])
        for iii,el_x in enumerate (self.x):
            for jjj,el_y in enumerate(self.y):
                try:
                    self.fit(iii, jjj)
                    peak_shift_array[iii, jjj] = self.peak_pos -self.ref_si
                except RuntimeError:
                    peak_shift_array[iii, jjj] = np.nan
        self.peak_shift_array = peak_shift_array
    def plot_map_shift(self):
        
        self.fit_map()
        fig = plt.figure()
        plt.imshow(self.peak_shift_array, cmap=self.cmap
                        ,vmin=-5, vmax = 5
                        , extent=[0, self.x[-1]-self.x[0], 0, self.y[-1]-self.y[0]])
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Raman shift $cm^{-1}$')
        plt.show()
     
    def strain110(self):
        self.fit_map()
        b_110 = -337
        self.eps_110 = 100*self.peak_shift_array / b_110
        self.eps_110_mean = np.nanmean(self.eps_110)
        self.eps_110_std = np.nanstd(self.eps_110)
       
    def strain_biax(self) :
        self.fit_map()
        b_biax = -733
        self.eps_biax = 100*self.peak_shift_array / b_biax
        self.eps_biax_mean = np.nanmean(self.eps_biax)
        self.eps_biax_std = np.nanstd(self.eps_biax)
        
    def strain100(self):
        self.fit_map()
        b_100 = -335.7
        self.eps_100 = 100*self.peak_shift_array / b_100
        self.eps_100_mean = np.nanmean(self.eps_100)
        self.eps_100_std = np.nanstd(self.eps_100)
        
    def plot_strain110(self):
        self.strain110()
        fig = plt.figure()
        plt.imshow(self.eps_110,cmap=self.cmap
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
        self.set_vmin_vmax(self.eps_110)                
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Uniaxial strain along [110] %%')
        plt.show()
        
    def plot_strain100(self):
        self.strain100()
        fig = plt.figure()
        plt.imshow(self.eps_100,cmap=self.cmap
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
        self.set_vmin_vmax(self.eps_100)                                                
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Uniaxial strain along [100] %%')
        plt.show()

    def plot_biax(self):
        self.strain_biax()
        fig = plt.figure()
        plt.imshow(self.eps_biax,cmap=self.cmap
                        ,vmin = -np.max(np.abs(self.eps_biax)), vmax = np.max(np.abs(self.eps_biax))
                        , extent = [0,self.x[-1]-self.x[0],0,self.y[-1]-self.y[0]])
        self.set_vmin_vmax(self.eps_biax)                                        
        plt.colorbar()
        plt.xlabel('µm')
        plt.xlabel('µm')
        plt.title('Biaxial strain %%')
        plt.show()
        print("mean biax strain = {:.4f} +- {:.4f}".format(np.nanmean(self.eps_biax),np.nanstd(self.eps_biax)))

    def plot_fit_raw():                
        print('to be done')
        
    def set_vmin_vmax(self, eps):
        im = plt.gca().get_images()[0]
        if self.eps_range:
            im.set_clim(-self.eps_range,self.eps_range)
        else:
            im.set_clim(-np.max(np.abs(eps)),np.max(np.abs(eps)))
            
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
        hs (int) : header line number
    
    Methods :
        fit : fit a lorentziand function to the experimental datas
        plot: plot experimental data and fit results
    
    
    """
            
    def __init__(self,filename, wn_min=490, wn_max=550):
        try: 
            self.filename = filename
            self.hs = headersize(self.filename)
            self.data = pd.read_csv(self.filename, header=self.hs, sep='\t', names=['wavenumber', 'counts'], index_col=0)
            self.header = pd.read_csv(self.filename, sep='=\t', nrows=self.hs, names=["parameter", "value"], engine='python')
            self.wn_min = wn_min
            self.wn_max = wn_max
            self.epoch = time.mktime(time.strptime(self.header[self.header['parameter'].str.match('Acquired')].values[0, 1],"%d.%m.%Y %H:%M:%S"))

        except IOError:
            print("file {} not found!".format(filename))

    def fit(self):
        """Mehod used to fit raman data with a lorenztian curve
        """
        self.x = self.data.index[(self.data.index>=self.wn_min)&(self.data.index<=self.wn_max)].values
        self.y = self.data.counts[self.wn_min:self.wn_max].values / float(self.header.value[0])         # counts per second

        self.p0 = [self.x[self.y.argmax()], 1, 2, 0]     # initial values for fit parameters
        [self.popt, self.pcov] = curve_fit(lorentzian, self.x, self.y, self.p0)
        self.peak_pos = self.popt[0]
    
    def plot(self,output_folder= os.getcwd):
        """Method to plot experimental data and fit results in a choosen folder
        """
        self.fit()
        fig1 = plt.figure()
        plt.plot(self.x,self.y,'bo')
        plt.plot(self.x , lorentzian(self.x,self.popt[0],self.popt[1],self.popt[2],self.popt[3]))
        plt.xlabel('Wave number $cm^{-1}$')
        plt.ylabel('Counts per second')
        plt.show()

    def plot_raw(self):
        fig1 = plt.figure()
        plt.plot(self.data.index,self.data.counts,'k')
        plt.xlabel('Wave number $cm^{-1}$')
        plt.ylabel('Counts per second')
        plt.show()
