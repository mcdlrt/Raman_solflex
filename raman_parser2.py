# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:58:35 2019

@author: LM254515
"""
import time
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

dict_param = {'peak_pos':[[515,530],'Raman shift $cm^{-1}'],
              'FWHM':[[1,3],'Silicon Raman peak FWHM $cm^{-1}'],
              '110':[[-0.5,0.5],'Uniaxial strain along [110] direction %'],
              '100':[[-0.5,0.5],'Uniaxial strain along [100] direction %'],
              'biax':[[-0.5,0.5],'Biaxial strain %']}
    
def __calibration__(r_o):
    """Function that change wave number array according to reference shift in time
    Args:
        r_o (objetc) = Raman_spectrum object
    """
    def ref(t, rs, re):
        """ does a linear fit of Ref shift with time
        output ref values at given time t
        """
        return rs.peak_pos+(t-rs.epoch)*((re.peak_pos-rs.peak_pos)/(re.epoch-rs.epoch))
    return (r_o.ref_si - ref(r_o.epoch, r_o.ref_start, r_o.ref_end))

def __headersize__(filename):
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
        return l_i
    except IOError:
        print("file {} not found!".format(filename))
    except:
        print('could not reader header size of {:}'.format(filename))

def __lorentzian__(x, x0, a, gam, c):
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

class raman_spectrum:
    """ Raman class for all types of scan (single, xy, z, timescan)
    """
    def __init_type__(self):
        """dictionnary for init for different file type
        """
        init_type = {'single':self.__single__,
                     'xy_map':self.__xy_map__,
                     'z_scan':self.__z_scan__,
                     't_scan':self.__t_scan__}
        return init_type
    
    def __header_attributes__(self):
        """ Set header parameter as attribute for the raman_spectrum object
        """
        for iii, param in enumerate(self.header.parameter):
            try: 
                setattr(self, param.strip('#').split(' ')[0].strip('.'), float(self.header.iloc[iii,1]))
            except ValueError:
                setattr(self, param.strip('#').split(' ')[0].strip('.'), self.header.iloc[iii,1])
            except:
                print('Parameter {:s} can not be set as attribute'.format(param))
                
    def __init__(self, filename, wn_min=490, wn_max=550, ref_si=520.7, rejection=False, ref_start=False, ref_end=False, file_type='single', eps_range=False, cmap='coolwarm', orientation='110'):
        """init function
        Argx:
            file_type (string, default='single') = type of scan ('single', 'xy_map', 'z_scan', 't_scan')
            orientation (string, default='110') = stress orientation ('110', '100','biax')
        """
        self.filename = filename
        self.wn_min = wn_min
        self.wn_max = wn_max
        self.ref_si = ref_si
        self.cmap = cmap
        self.hs = __headersize__(self.filename)
        self.eps_range = eps_range
        self.file_type = file_type
        self.orientation = orientation
        if orientation =='110':
            self.b_uni = -337
            self.E = 169 #young modulus in GPa
        elif orientation == '100':
            self.b_uni = -250.6
            self.E = 130
        elif orientation == 'biax':
            self.b_uni = -727
            self.E = 180
        else:
            print('{:} is not a valid stress orientation'.format(orientation))
        try:
            self.data = pd.read_csv(self.filename, header=self.hs, sep='\t')
            self.header = pd.read_csv(self.filename,
                                      sep='=\t',
                                      nrows=self.hs,
                                      names=["parameter", "value"],
                                      engine='python')
            self.__header_attributes__()
            self.epoch = time.mktime(time.strptime(self.Acquired, "%d.%m.%Y %H:%M:%S"))      # date of scan since epoch in s
            self.duration = self.Acq*self.Accumulations
            self.ND = float(self.ND.strip('%'))
            if ref_start and ref_end:
                try:
                    self.ref_start = raman_spectrum(ref_start)
                    self.ref_end = raman_spectrum(ref_end)
                    self.dw = __calibration__(self)
                except:
                    print('calibration failed')
            else:
                self.dw = 0
            self.__init_type__()[file_type]()
            self.err_strain = 100*self.pcov_peak/self.b_uni
            self.err_stress = 1000*(self.err_strain/self.E)/100

        except TypeError:
            print('File {:} can not be parsed'.format(filename))

    def __single__(self):
        """init for single spectrum
        """
        try: 
            self.data.columns = ['wn', 'counts']
            self.wn = self.data.values[:,0] + self.dw
            self.id_min = np.argmax(self.wn > self.wn_min)
            self.id_max = np.argmin(self.wn < self.wn_max)
            self.x_fit = self.wn[self.id_min:self.id_max]
            [self.popt, self.pcov] = self.__fit__(self.data.counts.values[self.id_min:self.id_max] / self.Acq)
            self.pcov_peak = self.pcov[0,0]
            self.peak_pos = self.popt[0]
            self.intensity = self.popt[1]
            self.FWHM = 2*self.popt[2]
            self.strain = 100 * (self.peak_pos - self.ref_si)/self.b_uni
            self.stress = 1000*(self.strain*self.E)/100 # stress in GPa
        except:
            print('file {:} can not be fitted'.format(self.filename))

    def __xy_map__(self):
        """init for xy_map
        """
        try: 
            self.data.rename(columns={'Unnamed: 0':'x','Unnamed: 1':'y'}, inplace=True)
            self.data.rename(columns={c: float(c) for c in self.data.columns[2:]})
            wn = self.data.columns[2:]
            self.wn = np.array([float(iii) for iii in wn]) + self.dw
            self.x = self.data.x.unique()                       # x values in µm
            self.y = self.data.y.unique()                       # y valles in µm
            self.id_min = np.argmax(self.wn > self.wn_min)
            self.id_max = np.argmin(self.wn < self.wn_max)
            self.x_fit = self.wn[self.id_min:self.id_max]

            
            self.peak_pos = np.zeros([len(self.x), len(self.y)])*np.nan 
            self.FWHM = np.zeros_like(self.peak_pos)*np.nan
            self.strain = np.zeros_like(self.peak_pos)*np.nan
            self.stress = np.zeros_like(self.peak_pos)*np.nan
            self.intensity = np.zeros_like(self.peak_pos)*np.nan
            self.baseline = np.zeros_like(self.peak_pos)*np.nan
            self.peakwidth = np.zeros_like(self.peak_pos)*np.nan
            self.pcov_peak = np.zeros_like(self.peak_pos)*np.nan
            for iii in np.arange(len(self.x)):
                for jjj in np.arange(len(self.y)):
                    try:
                        y_fit = self.data.values[iii*np.size(self.y)+jjj, self.id_min:self.id_max]/self.Acq
                        [self.peak_pos[iii,jjj], self.intensity[iii,jjj], self.peakwidth[iii,jjj], self.baseline[iii,jjj]], pcov = self.__fit__(y_fit)
                        self.pcov_peak[iii,jjj] = pcov[0,0]
                    except:
                        print("fit error")
            self.FWHM = 2*self.peakwidth
            self.strain = 100 * (self.peak_pos - self.ref_si)/self.b_uni
            self.stress = 1000*(self.strain*self.E)/100 # stress in GPa
            self.mean_strain = np.nanmean(self.strain)
            self.std_strain = np.nanstd(self.strain)
            self.mean_stress = np.nanmean(self.stress)
            self.std_stress = np.nanstd(self.stress)
               
        except TypeError:
            print('file {:} can not be fitted'.format(self.filename))
            
    def __z_scan__(self):
        """init for z_scan
        """
        try:
            self.data.rename(columns={'Unnamed: 0':'z'}, inplace=True)
            wn = self.data.columns[1:]
            self.wn = np.array([float(jjj) for jjj in wn]) + self.dw
            self.z = self.data.index
            self.id_min = np.argmax(self.wn > self.wn_min)
            self.id_max = np.argmin(self.wn < self.wn_max)
            self.x_fit = self.wn[self.id_min:self.id_max]
            
            self.peak_pos = np.zeros_like(self.z)*np.nan 
            self.FWHM = np.zeros_like(self.z)*np.nan
            self.strain = np.zeros_like(self.z)*np.nan
            self.stress = np.zeros_like(self.z)*np.nan
            self.intensity = np.zeros_like(self.z)*np.nan
            self.baseline = np.zeros_like(self.z)*np.nan
            self.peakwidth = np.zeros_like(self.z)*np.nan
            self.pcov_peak = np.zeros_like(self.z)*np.nan
        
            for iii in np.arange(len(self.time)):
                [self.peak_pos[iii], self.intensity[iii], self.peakwidth[iii], self.baseline[iii]], pcov = self.__fit__(self.data.values[iii, self.id_min:self.id_max]/self.Acq)
                self.pcov_peak[iii] = pcov[0,0]
            self.FWHM = 2*self.peakwidth
            self.strain = 100 * (self.peak_pos - self.ref_si)/self.b_uni
            self.stress = 1000*(self.strain*self.E)/100 # stress in GPa            
        except:
            print('file {:} can not be fitted'.format(self.filename))
            
    def __t_scan__(self):
        """init for t_scan
        """
        try:
            self.data.rename(columns={'Unnamed: 0':'time'}, inplace=True)
            wn = self.data.columns[1:]
            self.wn = np.array([float(jjj) for jjj in wn]) + self.dw
            self.time = self.data.time
            self.time_epoch = self.time + self.epoch
            self.id_min = np.argmax(self.wn > self.wn_min)
            self.id_max = np.argmin(self.wn < self.wn_max)
            self.x_fit = self.wn[self.id_min:self.id_max]
            
            self.peak_pos = np.zeros_like(self.time)*np.nan 
            self.FWHM = np.zeros_like(self.time)*np.nan
            self.strain = np.zeros_like(self.time)*np.nan
            self.stress = np.zeros_like(self.time)*np.nan
            self.intensity = np.zeros_like(self.time)*np.nan
            self.baseline = np.zeros_like(self.time)*np.nan
            self.peakwidth = np.zeros_like(self.time)*np.nan
            self.pcov_peak = np.zeros_like(self.time)*np.nan
        
            for iii in np.arange(len(self.time)):
                [self.peak_pos[iii], self.intensity[iii], self.peakwidth[iii], self.baseline[iii]], pcov = self.__fit__(self.data.values[iii, self.id_min:self.id_max]/self.Acq)
                self.pcov_peak[iii] = pcov[0,0]
 
            self.FWHM = 2*self.peakwidth
            self.strain = 100 * (self.peak_pos - self.ref_si)/self.b_uni
            self.stress = 1000*(self.strain*self.E)/100 # stress in GPa            
        except:
            print('file {:} can not be fitted'.format(self.filename))

    def plot_fit(self):
        """ Plot raw datas and correspoding fit
        """
        plt.figure()
        plt.xlabel('Wave numbers $cm^{-1}$')
        plt.ylabel('Counts/s')
        plt.minorticks_on()
        if self.file_type == 'single':
            plt.scatter(self.x_fit,self.data.counts.values[self.id_min:self.id_max]/self.Acq, facecolors='none', edgecolors='r')
            plt.plot(self.x_fit,__lorentzian__(self.x_fit,self.popt[0], self.popt[1], self.popt[2], self.popt[3]))
            
        else:
            for iii in np.arange(len(self.peak_pos)):
                plt.scatter(self.x_fit,self.data.values[iii,self.id_min:self.id_max]/self.Acq, facecolors='none', edgecolors='r')
                plt.plot(self.x_fit,__lorentzian__(self.x_fit,self.peak_pos[iii], self.intensity[iii], self.peakwidth[iii], self.baseline[iii]))
        plt.ylim(bottom=0)
        plt.show()

    def __fit__(self, y_fit_el, p0=[520, 10, 1.5, 0.5], bounds_f=([500, 1, 0.5, 0], [525, 10000, 10, 100])):
        try:
            [popt,pcov] = curve_fit(__lorentzian__,
                                self.x_fit,
                                y_fit_el,
                                p0=p0,
                                bounds=bounds_f)
            return popt, pcov
        except:
            print('fit error')
            return [np.nan, np.nan, np.nan, np.nan], np.zeros([4,4])*np.nan
    def __set_vmin_vmax__(self, param):
        """ Center vmin and vmax of current plot"""
        im = plt.gca().get_images()[0]
        if self.eps_range:
            im.set_clim(-self.eps_range,self.eps_range)
        else:
            im.set_clim(-np.max(np.abs(param)),np.max(np.abs(param)))   