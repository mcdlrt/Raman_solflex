# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:37:37 2019

@author: LM254515
"""

import raman_parser as rp
import matplotlib.pyplot as plt
l_files = ["0.1","1","10","25","50","100"]
plt.figure()
for l_file in l_files:
    fit_peak = rp.raman_spectrum(r"power/SI_pw_{}_01.txt".format(l_file))
    fit_peak.fit()
    plt.scatter(float(l_file),fit_peak.peak_pos)
    
    
    