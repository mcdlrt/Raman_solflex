# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:48:13 2019

@author: Никита
"""

import sys
import tdms_parser as tdp
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QTextEdit, QGridLayout, QMainWindow, QAction, qApp, QFileDialog, QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon
import PyQt5.QtCore
import raman_parser as rp
import matplotlib.pyplot as plt

class RamanGUI(QMainWindow):    
    '''
    This class creates gui application for raman+tensile stage measurements
    Atrebutes:
        
    '''

    def __init__(self): 
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        self.homedir = 'C:/'       
        
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
        
        #A button creates a dialog window when you can set up your home directory
        dirbtn  = QPushButton('Set directory', self)
        dirbtn.clicked.connect(self.setHomeDir)
        dirbtn.move(50, 180)
        
        # Chosse x array to plot tdms values
        xcombo = QComboBox(self)
        xcombo.addItems(['Time', 'Force', 'Elongation', 'Stress'])
        xcombo.move(200, 220)
        xcombo.activated[str].connect(self.setX)
        
        # choose y array to plot tdms values
        ycombo = QComboBox(self)
        ycombo.addItems(['Time', 'Force', 'Elongation', 'Stress'])
        ycombo.move(350, 220)
        ycombo.activated[str].connect(self.setY)
        
        plot = QPushButton('Plot it!', self)
        #plot.clicked.connect(self.plotgraph(self.x, self.y))
        plot.move(500, 220)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(exitAction)
        
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('TestGUI')
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
        "C:/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
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
    
    def plotgraph(self, x, y):
        
        try:
            self.tdms_file.plot(x, y)
        except:
            print("You didn't choose the file!")
        
    def openRaman(self, event):
        self.raman_name = QFileDialog(self).getOpenFileNames(self, "Raman data", self.homedir, "TXT files (*.txt)")
        print(self.raman_name)
        #self.ramanline.setText(self.raman_name[0])
       
    def crystalorientationset(self, text):
        self.crystalorientation = text
        if text == '110':
            self.b_uni = -337
        elif text =='100':
            self.b_uni = -335.7
   
    def setX(self, text):
        self.x = text
        
    def setY(self, text):
        self.y = text
    
    def start(self, event):
        t_AF = 0 # autofocus time, to be defined later
        plt.figure()
        for r_file in self.raman_name[0]:
            r_o = rp.raman_time_scan(r_file)
            r_o.fit_tscan()
            for iii,t in enumerate(r_o.time):
                time_elongation = r_o.epoch+(t*(r_o.duration+t_AF))
                eps_macro = 100*self.tdms_file.get_Elongation(time_elongation, r_o.duration)/(self.tdms_file.Length*1000)
                eps_Si = 100*(r_o.peak_shift_array[iii]-r_o.ref_si)/self.b_uni
                plt.scatter(eps_macro,eps_Si,marker = 'o',c ='k')
        plt.xlabel('Macroscopic strain %')
        plt.ylabel('Local Silicon Strain %')
        plt.show()
        
        for r_file in self.raman_name[0]:
            r_o = rp.raman_time_scan(r_file)
            r_o.fit_tscan()
            r_o.plot_fit_raw()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(PyQt5.QtCore.Qt.AA_DontShowIconsInMenus, False)
    ex = RamanGUI()
    sys.exit(app.exec_())