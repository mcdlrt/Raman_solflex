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

class tdms:
    
    def __init__(self,filename):
        self.filename = filename
        self.ctime = os.path.getctime(self.filename)
        self.mtime = os.path.getmtime(self.filename)
        self.file = TdmsFile(filename)
        self.readfile()
        try : 
            self.readfile()
        except :
            print('error')
        self.set_epoch_time()
        
    def readfile(self):
        
        parameters = self.file.object(u'Paramètres de test')
        self.Thickness = parameters.properties['Epaisseur']
        self.Length = parameters.properties['Longueur Utile']
        self.LengthTotale = parameters.properties['Longueur Totale']
        self.Width = parameters.properties['Largeur']
        
        self.group = u'Traction / Compression'
        self.Time = self.file.object(self.group, u'Temps (s)').data   #fr Temps
        self.Speed = self.file.object(self.group, u'Vitesse (µm/s)').data
        self.Elongation = self.file.object(self.group, u'Allongement (µm)').data
        self.Force = self.file.object(self.group, u'Force (N)').data
        self.Stress = self.file.object(self.group, u'Contrainte (Mpa)').data
        self.Deformation = self.file.object(self.group, u'Déformation (%)').data
    
    def plot(self, a, b):
        fig = plt.figure()
        plt.plot(getattr(self, a),getattr(self, b),'bo')
        plt.xlabel(a)
        plt.ylabel(b)
        plt.show()
        
    def set_epoch_time(self):
        self.epoch_time = self.Time+self.mtime - self.Time[-1]
        
    def get_value(self,r_time,duration,attr):
        val = getattr(self,attr)
        mean_val = np.mean(val[(self.epoch_time>r_time) & (self.epoch_time<r_time+duration)])
        return mean_val
    
    def get_Elongation(self,r_time,duration):
        return(self.get_value(r_time,duration,'Elongation'))
        
        