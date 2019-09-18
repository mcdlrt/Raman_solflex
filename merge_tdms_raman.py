# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:36:40 2019

@author: LM254515
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import raman_parser2 as rp
import tdms_parser as tdp

def merge_tdms_raman(tdms_name, raman_name, ref_start=False, ref_end=False, ep_si=200, dir_si='110', shift_pw=0, time_offset=0, time_coef=1, save_path=r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\recap2',save_name='result'):
    tdms_file = tdp.tdms(tdms_name)
    d = {'Filename':[],'Ref_si':[],'Elongation':[], 'Time':[], 'Force':[], 'StrainMacro':[], 'StrainSi':[], 'StressMacro':[],'StressSi':[],'Duration':[],'pCov':[], 'Err_strain':[], 'FWHM':[]}
    df = pd.DataFrame(data=d)
    for r_file in raman_name:
        print("parsing {:}".format(r_file))
        print('{:}'.format(ref_start))
        print('{:}'.format(ref_end))
        try:
            r_o = rp.raman_spectrum(r_file, orientation=dir_si,file_type='t_scan', ref_start=ref_start, ref_end=ref_end, ref_si=520.7-shift_pw)
            for iii,t in enumerate(r_o.time_epoch):
                if time_coef != 1:
                    t = r_o.epoch + (t-r_o.epoch)*time_coef
                if time_offset != 0:
                    t = t+time_offset
                    
                eps_macro = 100*tdms_file.get_Elongation(t, r_o.duration)/(tdms_file.Length*1000)
                df = df.append({'Filename':r_o.filename
                    , 'Ref_si': r_o.ref_si
                    , 'Elongation': tdms_file.get_Elongation(t, r_o.duration)
                    , 'Time': t
                    , 'Force': tdms_file.get_value(t,r_o.duration,'Force')
                    , 'StrainMacro': eps_macro
                    , 'StrainSi':r_o.strain[iii]
                    , 'StressMacro':[]
                    , 'StressSi':r_o.stress[iii]
                    , 'Duration': r_o.duration
                    , 'pCov': r_o.pcov_peak[iii]
                    , 'Err_strain' : r_o.err_strain[iii]
                    , 'Err_stress' : r_o.err_stress[iii]
                    , 'FWHM' : r_o.FWHM[iii]}, ignore_index=True)
        except:
            r_o = rp.raman_spectrum(r_file,orientation=dir_si, ref_start=ref_start, ref_end=ref_end, ref_si=520.7-shift_pw)
            eps_macro = 100*tdms_file.get_Elongation(r_o.epoch+time_offset, r_o.duration)/(tdms_file.Length*1000)                    
            df = df.append({'Filename':r_o.filename
                , 'Ref_si': r_o.ref_si
                , 'Elongation': tdms_file.get_Elongation(r_o.epoch+time_offset, r_o.duration)
                , 'Time': r_o.epoch
                , 'Force': tdms_file.get_value(r_o.epoch+time_offset,r_o.duration,'Force')
                , 'StrainMacro': eps_macro
                , 'StrainSi':r_o.strain
                , 'StressMacro':[]
                , 'StressSi': r_o.stress
                , 'Duration': r_o.duration
                , 'pCov': r_o.pcov_peak
                , 'Err_strain' : r_o.err_strain
                , 'Err_stress' : r_o.err_stress
                , 'FWHM' : r_o.FWHM}, ignore_index=True)
            print(eps_macro)
    
#    plt.figure()
#    plt.errorbar(df['StrainMacro'], df['StrainSi'],df['Err_strain']*3+0.05, marker='o', markerfacecolor='None', color='k')
   # df.plot(x='StrainMacro',y='StrainSi', marker='v', markerfacecolor='None', color='k')
#    plt.xlabel('Macroscopic strain %')
#    plt.ylabel('Local Silicon Strain %')
#    plt.gca().set_xlim(left=0)
#    plt.minorticks_on()
#    plt.title(tdms_file.filename)
#    plt.show()
    #plt.savefig('{}\{}.png'.format(save_path,save_name))
#        df.plot(x='StrainSi', y='Force', kind='scatter')
#        plt.show()
#        df.plot(x='StrainMacro',y='Force')
#        plt.show()
#        df.plot(x='Time',y='Elongation')
#        plt.show()
#        df.plot(x='Time', y='Force')
#        plt.show()
#        df.plot(x='StrainMacro',y='pCov',kind='scatter')
#        plt.show()
#        plt.figure()
#        plt.errorbar(df['StrainMacro'], df['StrainSi'],df['Err_strain'])
#        plt.show()
    #df.to_csv('{}\{}.txt'.format(save_path,save_name), sep='\t')
    return df    