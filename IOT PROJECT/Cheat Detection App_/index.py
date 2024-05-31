from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import datetime
from xlrd import *
from xlsxwriter import *
import os
import sys
from os.path import dirname, realpath, join
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUiType
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
#autre class qui contient  second wondow
from Ui_MainWindow import *
from  Ui_MatplotlibCanvas import *


MainUI,_ = loadUiType('main.ui')











class Main(QMainWindow ,MainUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.Handel_UI_Changes()
    
        
    def open_other_window(self):
        self.window=QtWidgets.QMainWindow()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
    #♥la meme chose
    def open_other_window_3em(self):
        self.window=QtWidgets.QMainWindow()
        self.ui=Ui_MatplotlibCanvas()
        self.ui.setupUi(self.window)
        self.window.show()
    




    #function une foix  cliquer sur le button push.. passe a l'index de  tab bar li lfo9
    def Handel_Buttons(self):
        self.pushButton_2.clicked.connect(self.uploadButton_to_tab)
        self.pushButton_3.clicked.connect(self.processing_datasetButton_to_tab)
        self.pushButton_6.clicked.connect(self.unsepervised_model_button_to_tab)
        #self.pushButton.clicked.connect(self.browse_open)
        
        self.pushButton.clicked.connect(self.OpenFile)
        self.pushButton_4.clicked.connect(self.dataHead)
      
        #self.pushButton_plus.clicked.connect(self.input_output)
       # self.describe.clicked.connect(self.decribe_data)
        #self.btn_plot.clicked.connect(self.op)
        #self.show_img_btn.clicked.connect(self.show_any_img)
       # self.open_second_window_btn.clicked.connect(self.open_other_window)
        #self.plot_perfect_btn.clicked.connect(self.open_other_window_3em)
     #function return  indes de tab bar   
    def uploadButton_to_tab(self):
        self.tabWidget.setCurrentIndex(0)    
    def processing_datasetButton_to_tab(self):
        self.tabWidget.setCurrentIndex(1)  
    def unsepervised_model_button_to_tab(self):
        self.tabWidget.setCurrentIndex(2) 
    def input_output(self):
        inp1=int(self.input1.toPlainText())
        inp2=int(self.input2.toPlainText())
        print(inp1,inp2)
        out=inp1+inp2
        self.output.setText(str(out))
   
        
        
    
    #upload file
    def OpenFile(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')[0]
            self.all_data = pd.read_csv(path)
        except:
            print(path)
            
    def decribe_data(self):
       self.edit_describe.setText(str(self.all_data.describe()))
      
        
      

        
     #head data
    def dataHead(self):
        numColomn = self.spinBox.value()
        if numColomn == 0:
            NumRows = len(self.all_data.index)
        else:
            NumRows = numColomn
        self.tableWidget.setColumnCount(len(self.all_data.columns))
        self.tableWidget.setRowCount(NumRows)
        self.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)

        for i in range(NumRows):
            for j in range(len(self.all_data.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.all_data.iat[i, j])))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
 
    
    def plot_data(self):
         x=self.all_data.iloc[:,3]
         y=self.all_data.iloc[:,2]
         print(x.shape,y.shape)
         img=plt.plot(x,y)
         cv2.imshow("Result", img)
         
    def op(self):
         import pandas as pd
         import seaborn as sns
         data = pd.read_csv('C:/Users/bouib/OneDrive/Bureau/S3 ENSIAS/covid19.csv')
         sns.pairplot(data[:3])
    
    def show_any_img(self):
        self.photo.setPixmap(QtGui.QPixmap("C:/Users/bouib/OneDrive/Bureau/Imprement/images.jfif"))
    
    #def browse_open(self):
       # path = QFileDialog.getOpenFileName(self, 'Open a file', '',
        #                                'All Files (*.*)')
        #if path != ('', ''):
         #   print("File path : "+ path[0])
            
   
            
            
    #function  l ikhfa2douk tab1,tab2,tab3 ... 
    def Handel_UI_Changes(self):
       # self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(True)  #// dir false bach takhfiha
       
        

      
def main():
    app = QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

