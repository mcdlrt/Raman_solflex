# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:06:13 2019

@author: LM254515
"""

import raman_parser as rp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
def lin_fun(x,a,b):
    return a*x+b

filepath = r"S:\300-Projets_Transverses\300.56-Solflex\raman_data\20190605_bulge\txt"
file_prefix = r"Si_zscan_p0.06_"
file_index = np.array([1,2,3,4,5,6])
z0 = np.array([0,0,0,0,0,0])
surf_z = np.zeros_like(file_index)
time_array = np.zeros_like(file_index)
fit_array = np.zeros_like(file_index)
for iii,el in enumerate(file_index):
    print("fit {}{}_{:0<1d}.txt".format(filepath,file_prefix,el))
    r_o =  rp.raman_mapping_z(r"{}\\{}{:0>2d}.txt".format(filepath,file_prefix,el))
    r_o.fit_zscan()
    surf_z[iii] = r_o.surf_z
    time_array[iii] = r_o.epoch
    
surf_z = surf_z - z0
time_array = time_array - time_array[0]

plt.figure()

[popt,pcov] = curve_fit(lin_fun,time_array,surf_z)

plt.figure()
plt.plot(time_array,surf_z,'ko')
plt.plot(time_array,lin_fun(time_array,popt[0],popt[1]))
plt.show()

print("drift speed = {:04f}µm/s".format(popt[0]))