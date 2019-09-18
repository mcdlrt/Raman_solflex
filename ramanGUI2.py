# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:48:13 2019

@author: Никита and Laurent Michaud
contact : laurent.g.michaud@gmail.com
"""

import sys
import tdms_parser as tdp
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QTextEdit, QGridLayout, QMainWindow, QAction, qApp, QFileDialog, QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon
import PyQt5.QtCore
import raman_parser2 as rp
import matplotlib.pyplot as plt
import pandas as pd

class RamanGUI(QMainWindow):    
    '''
    This class creates gui application for raman+tensile stage measurements
    Atrebutes:
        
    '''

    def __init__(self): 
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        self.homedir_init = r'S:\300-Projets_Transverses\300.56-Solflex\raman_data'  
        self.homedir = r'S:\300-Projets_Transverses\300.56-Solflex\raman_data'        
        self.crystalorientation = '110'
        self.ref_start = False
        self.ref_end = False
        self.time_coef = 1
        self.time_offset = 0
        self.PowerShift = 0
        #An exit action garanties you sucsesseful closing of the window(see def closeEvent)
        exitAction = QAction(QIcon('test.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.closeEvent)
        
        #A status bar in the left bottom corner of the window
        self.statusBar()
        self.statusBar().showMessage('Ready')
        
        #A button opens a dialog window to find a .tdms file(see def openTDMS)
        tdmsedit = QPushButton('Open tdms', self)
        tdmsedit.clicked.connect(self.openTDMS)
        tdmsedit.move(50, 60)
        
        #A line shows your .tdms file name 
        self.tdmsline = QLineEdit(self)
        self.tdmsline.setReadOnly(True)
        self.tdmsline.setText('...')
        self.tdmsline.move(170, 60)
        
        #A button opens a dialog window to find a .txt file with Raman data(see def openRaman)
        ramanbtn = QPushButton('Open raman', self)
        ramanbtn.clicked.connect(self.openRaman)
        ramanbtn.move(50, 100)
        
        #A line shows your .txt file name 
        self.ramanline = QLineEdit(self)
        self.ramanline.setReadOnly(True)
        self.ramanline.setText('...')
        self.ramanline.move(170, 100)
        
        #A button opens a dialog window to find a .txt file with Raman starting ref (see def openRefSart)
        RefStartBtn = QPushButton('Open ref start', self)
        RefStartBtn.clicked.connect(self.openRefSart)
        RefStartBtn.move(50, 300)
        
        #A line shows your .txt file name  for start ref
        self.RefStartLine = QLineEdit(self)
        self.RefStartLine.setReadOnly(True)
        self.RefStartLine.setText('...')
        self.RefStartLine.move(170, 300)
        
        #A button opens a dialog window to find a .txt file with Raman ending ref (see def openRefend)
        RefEndBtn = QPushButton('Open ref end', self)
        RefEndBtn.clicked.connect(self.openRefEnd)
        RefEndBtn.move(50, 350)
        
        #A line shows your .txt file name  for end ref
        self.RefEndLine = QLineEdit(self)
        self.RefEndLine.setReadOnly(True)
        self.RefEndLine.setText('...')
        self.RefEndLine.move(170, 350)
        
        # plot silicon strain (from .txt raman files) against macroscopic strain (from tdms file), see start function
        startbtn = QPushButton('Start!', self)
        startbtn.clicked.connect(self.start)
        startbtn.move(550, 450)
        
        #A tool where u can chose a crystal orientation
        cryor = QComboBox(self)
        cryor.addItems(['110', '100'])
        cryor.move(50, 140)
        cryor.activated[str].connect(self.crystalorientationset)
        self.b_uni = -337 # default value for [110] orientation
        
        #Group of line editers where you can see the value of length/width/thickness
        #from your .tdms file or set it manualy 
        self.lenlab = QLabel(self)
        self.lenlab.setText('Length, mm')
        self.lenlab.move(450, 60)
        
        self.lenline = QLineEdit(self)
        self.lenline.setText('...')
        self.lenline.textChanged[str].connect(self.setLength)
        self.lenline.move(570, 60)
        
        self.widlab = QLabel(self)
        self.widlab.setText('Width, mm')
        self.widlab.move(450, 100)
        
        self.widline = QLineEdit(self)
        self.widline.setText('...')
        self.lenline.textChanged[str].connect(self.setWidth)
        self.widline.move(570, 100)
        
        self.thicklab = QLabel(self)
        self.thicklab.setText('Thickness, mm')
        self.thicklab.move(450, 140)
        
        self.thickline = QLineEdit(self)
        self.thickline.setText('...')
        self.lenline.textChanged[str].connect(self.setThick)
        self.thickline.move(570, 140)
        
        #text box to choose offset shift to do laser power
        self.powershift_lab = QLabel(self)
        self.powershift_lab.setText('power shift $cm^{-1}$')
        self.powershift_lab.move(450, 290)
        
        self.PowerShiftLine = QLineEdit(self)
        self.PowerShiftLine.setText('0')
        self.PowerShiftLine.textChanged[str].connect(self.setPowerShift)
        self.PowerShiftLine.move(570, 290)

        #text box to choose coefficient corresponding to the 
        self.time_coeflab = QLabel(self)
        self.time_coeflab.setText('time coef')
        self.time_coeflab.move(450, 350)
        
        self.coefline = QLineEdit(self)
        self.coefline.setText('1')
        self.coefline.textChanged[str].connect(self.setTimeCoef)
        self.coefline.move(570, 350)

        #text box to choose time offset        
        self.timeOffsetLab = QLabel(self)
        self.timeOffsetLab.setText('time(raman)+=')
        self.timeOffsetLab.move(450, 400)
        
        self.timeOffsetLine = QLineEdit(self)
        self.timeOffsetLine.setText('0')
        self.timeOffsetLine.textChanged[str].connect(self.setTimeOffset)
        self.timeOffsetLine.move(570, 400)
        
        #A button creates a dialog window when you can set up your home directory
        dirbtn  = QPushButton('Set directory', self)
        dirbtn.clicked.connect(self.setHomeDir)
        dirbtn.move(50, 180)
        
#        # Chosse x array to plot tdms values
#        xcombo = QComboBox(self)
#        xcombo.addItems(['Time', 'Force', 'Elongation', 'Stress'])
#        xcombo.move(200, 220)
#        xcombo.activated[str].connect(self.setX)
#        
#        # choose y array to plot tdms values
#        ycombo = QComboBox(self)
#        ycombo.addItems(['Time', 'Force', 'Elongation', 'Stress'])
#        ycombo.move(350, 220)
#        ycombo.activated[str].connect(self.setY)
#        
#        plot = QPushButton('Plot it!', self)
#        #plot.clicked.connect(self.plotgraph(self.x, self.y))
#        plot.move(500, 220)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(exitAction)
        
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Raman Micromecha GUI')
        self.show()
        
    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            event.ignore()
   
    def setHomeDir(self, event):
        self.homedir = QFileDialog.getExistingDirectory(self, "Open Directory", 
        self.homedir_init, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        print(self.homedir)
        
    def openTDMS(self, event):
        self.tdms_name = QFileDialog(self).getOpenFileName(self, "Tensile stage data", self.homedir, "TDMS files (*.tdms)")
        self.tdmsline.setText(self.tdms_name[0])
        self.tdms_file = tdp.tdms(self.tdms_name[0])
        
        self.thickline.setText(str(self.tdms_file.Thickness))
        self.widline.setText(str(self.tdms_file.Width))
        self.lenline.setText(str(self.tdms_file.Length))
        
    def setThick(self, thick):
        self.tdms_file.Thickness = float(thick)
       
    def setWidth(self, width):    
        self.tdms_file.Width = float(width)
    
    def setLength(self, length):
        self.tdms_file.Length = float(length)

    def setTimeCoef(self,coef):
        try:
            self.time_coef = float(coef)
            print(self.time_coef)
        except ValueError:
            print('not a valid coeff')
            
    def setTimeOffset(self,offset):
        try:
            self.time_offset = float(offset)
            print(self.time_offset)
        except ValueError:
            print('not a valid offset')
    def setPowerShift(self,shift):
        try:
            self.PowerShift = float(shift)
        except ValueError:
            print('not a valid shift')
    def plotgraph(self, x, y):
        
        try:
            self.tdms_file.plot(x, y)
        except:
            print("You didn't choose the file!")
        
    def openRaman(self, event):
        self.raman_name = QFileDialog(self).getOpenFileNames(self, "Raman data", self.homedir, "TXT files (*.txt)")
        print(self.raman_name)
        #self.ramanline.setText(self.raman_name[0])
        
    def openRefSart(self,event):
        self.ref_start = QFileDialog(self).getOpenFileName(self, "Open ref start", self.homedir, "TXT files (*.txt)")
        self.ref_start = self.ref_start[0]
        self.RefStartLine.setText(self.ref_start)
        
    def openRefEnd(self,event):
        self.ref_end = QFileDialog(self).getOpenFileName(self, "Open ref end", self.homedir, "TXT files (*.txt)")
        self.ref_end = self.ref_end[0]
        self.RefEndLine.setText(self.ref_end)
        
    def crystalorientationset(self, text):
        self.crystalorientation = text
   
    def setX(self, text):
        self.x = text
        
    def setY(self, text):
        self.y = text
    
    def start(self, event):
        #creates DataFrame with all the data from TDMS and Raman file
        d = {'Filename':[],'Ref_si':[],'Elongation':[], 'Time':[], 'Force':[], 'StrainMacro':[], 'StrainSi':[], 'StressMacro':[],'StressSi':[],'Duration':[],'pCov':[], 'Err_strain':[], 'Err_Stress':[]}
        df = pd.DataFrame(data=d)
        for r_file in self.raman_name[0]:
            print("parsing {:}".format(r_file))
            print('{:}'.format(self.ref_start))
            print('{:}'.format(self.ref_end))
            try:
                r_o = rp.raman_spectrum(r_file,orientation=self.crystalorientation,file_type='t_scan', ref_start=self.ref_start, ref_end=self.ref_end, ref_si=520.7-self.PowerShift)
                for iii,t in enumerate(r_o.time_epoch):
                    if self.time_coef != 1:
                        t = r_o.epoch + (t-r_o.epoch)*self.time_coef
                    if self.time_offset != 0:
                        t = t+self.time_offset
                        
                    eps_macro = 100*self.tdms_file.get_Elongation(t, r_o.duration)/(self.tdms_file.Length*1000)
                    df = df.append({'Filename':r_o.filename
                        , 'Ref_si': r_o.ref_si
                        , 'Elongation': self.tdms_file.get_Elongation(t, r_o.duration)
                        , 'Time': t
                        , 'Force': self.tdms_file.get_value(t,r_o.duration,'Force')
                        , 'StrainMacro': eps_macro
                        , 'StrainSi':r_o.strain[iii]
                        , 'StressMacro':[]
                        , 'StressSi':r_o.stress[iii]
                        , 'Duration': r_o.duration
                        , 'pCov': r_o.pcov_peak[iii]
                        , 'Err_strain' : r_o.err_strain[iii]
                        , 'Err_stress' : r_o.err_stress[iii]}, ignore_index=True)
            except:
                r_o = rp.raman_spectrum(r_file,orientation=self.crystalorientation, ref_start=self.ref_start, ref_end=self.ref_end, ref_si=520.7-self.PowerShift)
                if self.time_offset!= 0:
                    eps_macro = 100*self.tdms_file.get_Elongation(r_o.epoch+self.time_offset, r_o.duration)/(self.tdms_file.Length*1000)                    
                else:
                    eps_macro = 100*self.tdms_file.get_Elongation(r_o.epoch, r_o.duration)/(self.tdms_file.Length*1000)
                df = df.append({'Filename':r_o.filename
                    , 'Ref_si': r_o.ref_si
                    , 'Elongation': self.tdms_file.get_Elongation(r_o.epoch, r_o.duration)
                    , 'Time': r_o.epoch
                    , 'Force': self.tdms_file.get_value(r_o.epoch,r_o.duration,'Force')
                    , 'StrainMacro': eps_macro
                    , 'StrainSi':r_o.strain
                    , 'StressMacro':[]
                    , 'StressSi': r_o.stress
                    , 'Duration': r_o.duration
                    , 'pCov': r_o.pcov_peak
                    , 'Err_strain' : r_o.err_strain
                    , 'Err_stress' : r_o.err_stress}, ignore_index=True)
                print(eps_macro)
        
        plt.figure()
        plt.errorbar(df['StrainMacro'], df['StrainSi'],df['Err_strain']*3+0.05, marker='o', markerfacecolor='None', color='k')
       # df.plot(x='StrainMacro',y='StrainSi', marker='v', markerfacecolor='None', color='k')
        plt.xlabel('Macroscopic strain %')
        plt.ylabel('Local Silicon Strain %')
        plt.gca().set_xlim(left=0)
        plt.minorticks_on()
        plt.title(self.tdms_file.filename)
        plt.show()
#        df.plot(x='StrainSi', y='Force', kind='scatter')
#        plt.show()
#        df.plot(x='StrainMacro',y='Force')
#        plt.show()
#        df.plot(x='Time',y='Elongation')
#        plt.show()
#        df.plot(x='Time', y='Force')
#        plt.show()
#        df.plot(x='StrainMacro',y='pCov',kind='scatter')
#        plt.show()
#        plt.figure()
#        plt.errorbar(df['StrainMacro'], df['StrainSi'],df['Err_strain'])
#        plt.show()
        df.to_csv('results.txt', sep='\t')

   
        
#        for r_file in self.raman_name[0]:
#            try:
#                r_o = rp.raman_time_scan(r_file,rejection=45)
#                r_o.fit_tscan()
#                r_o.plot_fit_raw()
#            except ValueError:
#                print('not a time scan {:}'.format(r_file))
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(PyQt5.QtCore.Qt.AA_DontShowIconsInMenus, False)
    ex = RamanGUI()
    sys.exit(app.exec_())