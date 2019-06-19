# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 18:44:47 2019

@author: LM254515
"""

import raman_parser as rp
import numpy as np
import tdms_parser as tp
import matplotlib.pyplot as plt

b_uni = -337
L0 =10000

r_file = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\txt_map\SOP_110_200nm_2_01.txt"
t_file = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190607_uniax\tdms\SOP_110_200nm_2019_06_07_15_05_1.tdms"

r_o = rp.raman_time_scan(r_file)
t_o = tp.tdms_file(t_file)
r_o.fit_tscan()
plt.figure()
for iii,t in enumerate(r_o.time_epoch):
    if iii == 0:
        t0 = t
    plt.scatter(100*t_o.get_elongation(((t-t0)*r_o.duration)+t0,r_o.duration)/L0,100*(r_o.peak_shift_array[iii]-r_o.ref_si)/b_uni,marker = 'o',c ='k')
    print(iii,t,t_o.get_elongation(((t-t0)*r_o.duration)+t0,r_o.duration))
plt.xlabel('Macroscopic sttrain %')
plt.ylabel('Local Silicon Strain %')    
    