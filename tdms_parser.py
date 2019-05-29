# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:55:36 2019

@author: LM254515
"""

import os

class tdms_file:
    def __init__(self,filename):
        self.filename = filename
        self.ctime = os.path.getctime(self.filename)        # creation time since epoch