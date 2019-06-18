# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:48:13 2019

@author: Никита
"""

import sys
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QTextEdit, QGridLayout, QMainWindow, QAction, qApp, QFileDialog, QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon
import PyQt5.QtCore

class RamanGUI(QMainWindow):    
    def __init__(self): 
        super().__init__()
        self.initUI()
        
    def initUI(self):        

        #textEdit = QTextEdit()
        #self.setCentralWidget(textEdit)
        self.homedir = 'C:/'
        
        exitAction = QAction(QIcon('test.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.closeEvent)
        '''randomAction = QAction(QIcon('test.png'), '&Random', self)
        randomAction.setStatusTip('Pointless button')
        #randomAction.triggered.connect(qApp.
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(randomAction)'''
        
        self.statusBar()
        self.statusBar().showMessage('Ready')
        
        '''dirbtn  = QPushButton('Home directory', self)
        dirbtn.clicked.connect(self.setHomeDir)
        dirbtn.move(50, 180)'''
        
        tdmsedit = QLineEdit()
        ramanedit = QLineEdit()
        tdmslabel = QLabel('Open tdms')
        ramanlabel = QLabel('Open raman')
        
        #tdmsedit = QPushButton('Open tdms', self)
        #tdmsedit.clicked.connect(self.openTDMS)
        #tdmsedit.move(50, 60)
        
        #ramanbtn = QPushButton('Open raman', self)
        #ramanbtn.clicked.connect(self.openRaman)
        #ramanbtn.move(50, 100)
        
        
        
        startbtn = QPushButton('Start!', self)
        startbtn.clicked.connect(self.start)
        startbtn.move(550, 450)
        
        combo = QComboBox(self)
        combo.addItems(['110', '100'])
        #combo.move(50, 140)
        combo.activated[str].connect(self.crystalorientationset)
        '''menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(exitAction)'''
    
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(tdmslabel, 1, 2)
        grid.addWidget(tdmsedit, 1, 1)
        grid.addWidget(ramanlabel, 2, 0)
        grid.addWidget(ramanedit, 2, 1)
        grid.addWidget(combo, 3, 1)
        self.setLayout(grid)
        
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('TestGUI')    
        self.show()
        
    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            #event.accept()
            sys.exit(app.exec_())
        else:
            event.ignore()
   
    def setHomeDir(self, event):
        self.homedir = QFileDialog.getExistingDirectory(self, "Open Directory", 
        "C:/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        print(self.homedir)
        
        
    def openTDMS(self, event):
        self.tdms_file = QFileDialog(self).getOpenFileName(self, "Tensile stage data", "C:/", "TDMS files (*.tdms)")
        
    def openRaman(self, event):
        self.raman_file = QFileDialog(self).getOpenFileName(self, "Raman data", "C:/", "TXT files (*.txt)")
    
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