# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:12:36 2019

@author: LM254515
laurent.michaud@cea.fr
scipt used to plot tensile test results from Raman data and TDMS curve created by a micromecha tensile stage
"""

import matplotlib.pyplot as plt
import raman_parser as rp
import wx #package for GUI, we can use another if needed


class MainFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Raman_tensileGUI')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.HORIZONTAL)        
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Load files')
        my_btn.Bind(wx.EVT_BUTTON, self.OnOpen)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)        
        self.Show()
    
    def doLoadData(self,pathnames):
        try:
            for iii in pathnames:
                print(pathnames)
            
        except:
            wx.LogError("Cannot open file") 


    def OnOpen(self, event):
    
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open txt files", wildcard="txt files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
    
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
    
            # Proceed loading the file chosen by the userwx open multiple fil
            pathnames = fileDialog.GetPaths()
            try:
                self.doLoadData(pathnames)
            except IOError:
                wx.LogError("Cannot open file")            

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()