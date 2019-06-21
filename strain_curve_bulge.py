# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:45:47 2019

@author: LM254515
"""

import raman_parser as rp
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_list = filedialog.askopenfilenames()
z0 = 0
eps_biax = np.zeros_like(file_list)
eps_biax_std = np.zeros_like(file_list)
z = np.zeros_like(file_list)
a = 10
t_furu = 230e-6        # Thickness in µm
E_furu = 215e6      # Young modulus in Pa
v_furu = 0.4        # poisson modulus
E_bsi = 1.5e9 
v_bsi = 0.4  
t_bsi = 40e-6 
   
def Y(E,v):
    """function to compute biaxial young modulus"""
    return (E/(1-v))

Y_furu = Y(E_furu,v_furu) 
def strain_macro(z,z0):
    return 100*2*(np.square(z)-np.square(z0))/(3*np.square(a))
def pressure(z,Y,t):
    return (8*Y*t*np.power(z,3))/(3*np.power(a,3))


r_obj = []
for iii in np.arange(len(file_list)):
    r_obj.append(rp.raman_mapping_xy(file_list[iii], wn_min=500, wn_max=540))       # raman mapping object
    r_obj[iii].strain_biax()
    eps_biax[iii] = r_obj[iii].eps_biax_mean
    eps_biax_std[iii] = r_obj[iii].eps_biax_std
    z[iii] = r_obj[iii].z
    r_obj[iii].plot_biax()
    print(file_list[iii])
    
    
    
z = -z.astype(float)*0.001
eps_biax = eps_biax.astype(float)
eps_biax_std = eps_biax_std.astype(float)

#plt.figure()
#plt.errorbar(strain_macro(z,z0),eps_biax,eps_biax_std,linestyle='',marker = 'o')
#plt.xlabel('Bulge macroscopic strain %')
#plt.ylabel('Silicon local strain %')


#x_h = np.linspace(0,2)
#plt.figure()
#plt.plot(pressure(x_h,Y_furu,t_furu)/1000, strain_macro(x_h,0))