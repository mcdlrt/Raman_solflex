# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 18:44:47 2019

@author: LM254515
"""

import raman_parser as rp
import numpy as np
import tdms_parser as tp
import matplotlib.pyplot as plt



def plot_strain_timescan(raman_files,tdms_file, L0=20000, b_uni=-337, t_AF=5):
    t_o = tp.tdms_file(tdms_file)
    plt.figure()
    for r_file in raman_files:
        r_o = rp.raman_time_scan(r_file)
        r_o.fit_tscan()
        for iii,t in enumerate(r_o.time_epoch):
            if iii == 0:
                t0 = t
            plt.scatter(100*t_o.get_elongation(((t-t0)*r_o.duration)+t0+t_AF,r_o.duration)/L0,100*(r_o.peak_shift_array[iii]-r_o.ref_si)/b_uni,marker = 'o',c ='k')
            print(iii,t,100*t_o.get_elongation(((t-t0)*r_o.duration)+t0+t_AF,r_o.duration)/L0)
    plt.xlabel('Macroscopic sttrain %')
    plt.ylabel('Local Silicon Strain %')
    plt.show()
    
raman_files = [r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_02.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_03.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_04.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_05.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_06.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_07.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_08.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_09.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_10.txt',
               r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP3_110_200nm_11.txt']
tdms_file = r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\tdms\SOP3_110_200nm_2019_06_07_10_07_1.tdms'

plot_strain_timescan(raman_files,tdms_file)   

raman_files2 = [r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP_110_200nm_2_01.txt',
                r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP_110_200nm_2_02.txt']
tdms_file2 = r'S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\tdms\SOP_110_200nm_2019_06_07_15_05_1.tdms'
plot_strain_timescan(raman_files2,tdms_file2)   
#b_uni = -337
#L0 = 10000
#t_AF = 10 
#
#r_file = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP_110_200nm_2_03.txt"
#t_file = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\tdms\SOP_110_200nm_2019_06_07_15_05_1.tdms"
#
#r_o = rp.raman_time_scan(r_file)
#t_o = tp.tdms_file(t_file)
#r_o.fit_tscan()
#plt.figure()
#for iii,t in enumerate(r_o.time_epoch):
#    if iii == 0:
#        t0 = t
#    plt.scatter(100*t_o.get_elongation(((t-t0)*r_o.duration)+t0+t_AF,r_o.duration)/L0,100*(r_o.peak_shift_array[iii]-r_o.ref_si)/b_uni,marker = 'o',c ='k')
#    print(iii,t,t_o.get_elongation(((t-t0)*r_o.duration)+t0,r_o.duration))
#plt.xlabel('Macroscopic sttrain %')
#plt.ylabel('Local Silicon Strain %')    
#
#
#
#r_file = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP_110_200nm_2_02.txt"
#t_file = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\tdms\SOP_110_200nm_2019_06_07_15_05_1.tdms"
#
#
#
#r_o = rp.raman_time_scan(r_file)
#t_o = tp.tdms_file(t_file)
#r_o.fit_tscan()
#plt.figure()
#for iii,t in enumerate(r_o.time_epoch):
#    if iii == 0:
#        t0 = t
#    plt.scatter(100*t_o.get_elongation(((t-t0)*r_o.duration)+t0+t_AF,r_o.duration)/L0,100*(r_o.peak_shift_array[iii]-r_o.ref_si)/b_uni,marker = 'o',c ='k')
#    print(iii,t,t_o.get_elongation(((t-t0)*r_o.duration)+t0,r_o.duration))
#plt.xlabel('Macroscopic sttrain %')
#plt.ylabel('Local Silicon Strain %')

