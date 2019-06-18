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
        self.mtime = os.path.getmtime(self.filename)
        self.file = TdmsFile(filename)
        
        try : 
            self.readfile()
        except :
            print('error')
        self.set_epoch_time()
    
    def paramters(self):
        parameters = tdms_file.object(u'Paramètres de test')
        self.Epaisseur = parameters.properties['Epaisseur']
        self.LongueurUtile = parameters.properties['Longueur Utile']
        self.LongueurTotale = parameters.properties['Longueur Totale']
        self.Largeur = parameters.properties['Largeur']
        
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
        plt.xlabel(a)
        plt.ylabel(b)
        plt.show()
        
    def set_epoch_time(self):
        self.epoch_time = self.time+self.mtime - self.time[-1]
        
    def get_value(self,r_time,duration,attr):
        val = getattr(self,attr)
        med_val = np.median(val[(self.epoch_time>r_time) & (self.epoch_time<r_time+duration)])
        return med_val
    
    def get_elongation(self,r_time,duration):
        return(self.get_value(r_time,duration,'elongation'))
        
        