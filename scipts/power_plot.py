# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:37:37 2019

@author: LM254515
"""

import raman_parser as rp
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_list = filedialog.askopenfilenames()
l_files = ["1","10","25","50","100"]
plt.figure()
#for l_file in l_files:
fit_peak = []
for iii in np.arange(len(file_list)):
    fit_peak.append(rp.raman_spectrum(file_list[iii]))
    #fit_peak = rp.raman_spectrum(r"power/SI_pw_{}_01.txt".format(l_file))
    #fit_peak = rp.raman_spectrum(r"C:\Работа\Стажировка\DATA\20190617_bulge\txt\filter\SOP_200nm_SPIS_filter_{}_01.txt".format(l_file))
    fit_peak[iii].fit()
    plt.scatter(l_files[iii],fit_peak[iii].peak_pos)
    print(file_list[iii])
    
    