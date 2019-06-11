# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:55:36 2019

@author: LM254515
"""

import os
from nptdms import TdmsFile
import matplotlib.pyplot as plt
import scipy as sps
import numpy as np

class tdms_file:
    
    def __init__(self,filename):
        self.filename = filename
        self.ctime = os.path.getctime(self.filename)
        self.file = TdmsFile(filename)
    
    def readfile(self):
        self.group = u'Traction / Compression'
        self.time = self.file.object(self.group, u'Temps (s)').data   #fr Temps
        self.speed = self.file.object(self.group, u'Vitesse (µm/s)').data
        self.elongation = self.file.object(self.group, u'Allongement (µm)').data
        self.force = self.file.object(self.group, u'Force (N)').data
        self.stress = self.file.object(self.group, u'Contrainte (Mpa)').data
        self.deformation = self.file.object(self.group, u'Déformation (%)').data
    
    def plot(self, a, b):
        fig = plt.figure()
        plt.plot(getattr(self, a),getattr(self, b),'bo')
        plt.xlabel()
        plt.ylabel()
        plt.show()
        
    