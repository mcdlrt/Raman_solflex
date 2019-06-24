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

class RamanGUI(QMainWindow):    
    def __init__(self): 
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        '''
        '''
        
        self.homedir = 'C:/'       
        
        exitAction = QAction(QIcon('test.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.closeEvent)
        
        self.statusBar()
        self.statusBar().showMessage('Ready')
        
        tdmsedit = QPushButton('Open tdms', self)
        tdmsedit.clicked.connect(self.openTDMS)
        tdmsedit.move(50, 60)
        
        self.tdmsline = QLineEdit(self)
        self.tdmsline.setReadOnly(True)
        self.tdmsline.setText('...')
        self.tdmsline.move(170, 60)
        
        ramanbtn = QPushButton('Open raman', self)
        ramanbtn.clicked.connect(self.openRaman)
        ramanbtn.move(50, 100)
        
        self.ramanline = QLineEdit(self)
        self.ramanline.setReadOnly(True)
        self.ramanline.setText('...')
        self.ramanline.move(170, 100)
        
        startbtn = QPushButton('Start!', self)
        startbtn.clicked.connect(self.start)
        startbtn.move(550, 450)
        
        cryor = QComboBox(self)
        cryor.addItems(['110', '100'])
        cryor.move(50, 140)
        cryor.activated[str].connect(self.crystalorientationset)
        
        dirbtn  = QPushButton('Set directory', self)
        dirbtn.clicked.connect(self.setHomeDir)
        dirbtn.move(50, 180)
        
        self.lenlab = QLabel(self)
        self.lenlab.setText('Length, mm')
        self.lenlab.move(50, 220)
        
        self.lenline = QLineEdit(self)
        self.lenline.setText('...')
        self.lenline.textChanged[str].connect(self.setLength)
        self.lenline.move(150, 220)
        
        self.widlab = QLabel(self)
        self.widlab.setText('Width, mm')
        self.widlab.move(50, 260)
        
        self.widline = QLineEdit(self)
        self.widline.setText('...')
        self.lenline.textChanged[str].connect(self.setWidth)
        self.widline.move(150, 260)
        
        self.thicklab = QLabel(self)
        self.thicklab.setText('Thickness, mm')
        self.thicklab.move(50, 300)
        
        self.thickline = QLineEdit(self)
        self.thickline.setText('...')
        self.lenline.textChanged[str].connect(self.setThick)
        self.thickline.move(150, 300)
        
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
        self.tdms_file.parameters()
        self.thickline.setText(str(self.tdms_file.Thickness))
        self.widline.setText(str(self.tdms_file.Width))
        self.lenline.setText(str(self.tdms_file.Length))
        
    def setThick(self, thick):
        self.tdms_file.Thickness = float(thick)
       
    def setWidth(self, width):    
        self.tdms_file.Width = float(width)
    
    def setLength(self, length):
        self.tdms_file.Length = float(length)
        
    def openRaman(self, event):
        self.raman_name = QFileDialog(self).getOpenFileName(self, "Raman data", self.homedir, "TXT files (*.txt)")
        self.ramanline.setText(self.raman_name[0])
       
    def crystalorientationset(self, text):
        self.crystalorientation = text
        print(self.crystalorientation)
    
    def start(self, event):
        print('START!')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(PyQt5.QtCore.Qt.AA_DontShowIconsInMenus, False)
    ex = RamanGUI()
    sys.exit(app.exec_())