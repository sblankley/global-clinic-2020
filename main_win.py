#!/usr/bin/env python
#-*- coding:utf-8 -*
#main.py

### Setup

# import necessary libraries
import backend
from backend import optimization, CSVReader, settings, control 
import sys, csv 
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import numpy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math 

## Initial setup things
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) # enable high DPI scaling for high-res displays
backend.settings.init() # initialize "global" variables list

### UI Classes
class SplashWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()
    dataOpen = QtCore.pyqtSignal()

    def __init__(self):
        # General HelpWindow settings 
        super(SplashWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'backend\splash.ui', self) # Load the splash window .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("Welcome!")
        self.setWindowIcon(QIcon(r'backend\hmc.png'))

    def on_pushButtonContinueToInput_clicked(self):
        self.dataOpen.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit() 

class Error(QtWidgets.QMainWindow):

    go = QtCore.pyqtSignal()
    cancel = QtCore.pyqtSignal()

    def __init__(self, fileName):
        super(Error, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'backend\error.ui', self) # Load the main .ui file
        self.setWindowTitle('Input data file error')        
        self.setWindowIcon(QIcon(r'backend\hmc.png'))
        
        # pushbutton connections
        self.pushButtonContinue.clicked.connect(self.go.emit)
        self.pushButtonCancel.clicked.connect(self.cancel.emit)

class Warning(QtWidgets.QMainWindow):

    go = QtCore.pyqtSignal()
    cancel = QtCore.pyqtSignal()

    def __init__(self):
        super(Warning, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'backend\warning.ui', self) # Load the main .ui file
        self.setWindowTitle('Unsaved changes will be lost!')        
        self.setWindowIcon(QIcon(r'backend\hmc.png'))
        
        # pushbutton connections
        self.pushButtonContinue.clicked.connect(self.go.emit)
        self.pushButtonCancel.clicked.connect(self.cancel.emit)

class Check(QtWidgets.QMainWindow):

    save = QtCore.pyqtSignal()
    go = QtCore.pyqtSignal()
    cancel = QtCore.pyqtSignal()

    def __init__(self, fileName):
        super(Check, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'backend\check.ui', self) # Load the main .ui file
        self.setWindowTitle('Unsaved changes will be lost!')        
        self.setWindowIcon(QIcon(r'backend\hmc.png'))

        layout = QtWidgets.QGridLayout()

        self.fileName = fileName
        self.pushButtonSave.clicked.connect(self.save_and_continue)
    
    def on_pushButtonContinue_clicked(self):
        self.go.emit()

    def on_pushButtonCancel_clicked(self):
        self.cancel.emit()
    
    def save_and_continue(self):
        self.save.emit()

class DataWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()
    results  = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()
    
    #
    # Initialize the GUI window and define the objects within it
    #
    def __init__(self):
        super(DataWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'backend\dataWindow.ui', self) # Load the main .ui file

        self.fileName = r'template.csv' # default input filename
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("Enter the production line data to be optimized")
        self.setWindowIcon(QIcon(r'backend\hmc.png'))
        self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
        self.tableView.setModel(self.model)
        self.save_file = r'pLine.csv'

        # manually connect pushbuttons to avoid doubling the connection when using auto-connect
        self.pushButtonLoad.clicked.connect(self.upload)
        self.pushButtonWrite.clicked.connect(self.save_table)
        self.pushButtonResults.clicked.connect(self.results.emit)
        self.pushButtonHelp.clicked.connect(self.helpOpen.emit)

        # scaling settings for the window
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    #
    # startup function to load template
    #
    def startup(self):
        self.model.clear()
        self.loadCsv(self.fileName)
    
    #
    # import new file to GUI
    #
    def upload(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.new, _ = QFileDialog.getOpenFileName(None, "Choose input data file", "", "Comma Separated Value Files, (* .csv)", options = options )
        if (self.new):
            ext = ""
            for x in [-4,-3,-2,-1]:
                end = str(self.new[x])
                ext += end
            if (ext == ".csv"): # .csv file extension?
                self.fileName = self.new                
                self.model.clear()
                self.loadCsv(self.fileName)
            else: #if not, they've selected an incompatible filename
                self.errorFunct()
    
    #
    # emit error signal to open error 
    # 
    def errorFunct(self): 
        self.error.emit()
   
    #
    # save GUI table to file
    #    
    def save_table(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.temp_file, _ = QFileDialog.getSaveFileName(None,"Choose input file to save","","Comma Separated Values Files (*.csv)", options=options)
        if (self.temp_file):
            self.fileName = self.temp_file
            ext = ""
            # check if user input a .csv file extension: if not, append with .csv
            for x in [-4,-3,-2,-1]:
                end = str(self.fileName[x])
                ext += end
            if (ext == ".csv"):                
                self.fileName = self.temp_file
            else:
                self.fileName += ".csv"
            self.writeCsv(self.fileName)
    
    #
    # .csv functions
    #
    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row 
                ]
                # gray out columns and add color to headers
                self.model.appendRow(items)
                for rowNum1 in range(0,len(list(csv.reader(fileName)))+1):
                    for colNum1 in range(0,10):
                        self.model.setData(
                                    self.model.index(rowNum1, colNum1), QtCore.Qt.AlignCenter, 
                                    QtCore.Qt.TextAlignmentRole
                                )
                        if rowNum1 == 0:
                            self.model.setData(
                                    self.model.index(0, colNum1), QBrush(
                                        QColor(214,188,138)), QtCore.Qt.BackgroundRole
                                )
                for rowNum2 in range(2,len(list(csv.reader(fileName)))+1):
                    for colNum2 in range(8,10):
                        self.model.setData(
                                    self.model.index(rowNum2, colNum2), QBrush(
                                        QColor(211, 211, 211)), QtCore.Qt.BackgroundRole
                                )
                
    def writeCsv(self, fileName):
        with open(fileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = []
                for columnNumber in range(self.model.columnCount()):
                    cell = self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    self.model.setData(
                            self.model.index(rowNumber, columnNumber), QtCore.Qt.AlignCenter, 
                            QtCore.Qt.TextAlignmentRole
                        )               
                    fields.append(cell)
                writer.writerow(fields)          
    
class HelpWindow(QtWidgets.QMainWindow):

    done = QtCore.pyqtSignal()

    def __init__(self):
        # General HelpWindow settings 
        super(HelpWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(r'backend\help.ui', self) # Load the main .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon(r'backend\hmc.png'))

    def on_pushButtonDone_clicked(self):
        self.done.emit()

class ResultsWindow(QtWidgets.QMainWindow):

    startover = QtCore.pyqtSignal()
    helpOpen = QtCore.pyqtSignal()
    back = QtCore.pyqtSignal()

    # Initialize the GUI window and define the objects within it
    def __init__(self):
       super(ResultsWindow, self).__init__() # Call the inherited classes __init__ method
       uic.loadUi(r'backend\results.ui', self) # Load the main .ui file, prepend with 'r' to avoid '/r' issue
       self.imageName = "StationLayout.png" # default output file name
       self.model = QtGui.QStandardItemModel(self)
       self.setWindowTitle("Optimized Results")
       self.setWindowIcon(QIcon(r'backend\hmc.png'))
       self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
       self.tableView.setModel(self.model)
       self.MplWidget = self.findChild(QtWidgets.QWidget,"MplWidget") # looks for MplWidget object in results.ui
       self.mplwidget = MplWidget(self.MplWidget)
       widget = QWidget()
       layout = QGridLayout() # sets layout
       # defines a grid layout for each widget by row, column, rowSpan, columnSpan
       layout.addWidget(self.tableView, 0,0,3,12) 
       layout.addWidget(self.mplwidget, 4,0,2,12)
       layout.addWidget(self.pushButtonHelp, 7,0,1,1)
       layout.addWidget(self.pushButtonSaveLayout, 7,8,1,1)
       layout.addWidget(self.pushButtonSaveTable, 7,9,1,1)
       layout.addWidget(self.pushButtonBack, 7,10,1,1)
       layout.addWidget(self.pushButtonReturn, 7,11,1,1)
       widget.setLayout(layout) # sets layout
       self.setCentralWidget(widget) # makes all these widgets central widgets
       self.save_file = r'pLineOpt.csv'

       self.pushButtonSaveTable.clicked.connect(self.save_table)   # create non-implicit function to avoid double-press issue
       self.pushButtonSaveLayout.clicked.connect(self.save_layout) # ^

       self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) # ensures all text is visible in each column
   

    def save_table(self):
        # system dialog code
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        temp_file, _ = QFileDialog.getSaveFileName(None,"Choose output data file","","Comma Separated Values Files (*.csv)", options=options)
        if (temp_file):
            self.save_file = temp_file
            ext = ""
            for x in [-4,-3,-2,-1]:
                end = str(self.save_file[x])
                ext += end
            if (ext == ".csv"):                
                self.fileName = save_file
            else:
                self.save_file += ".csv"
            #csvwrite
            self.writeCsv(self.save_file)

    def save_layout(self):
    # system dialog code
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_file, _ = QFileDialog.getSaveFileName(None,"Choose output data file","","Comma Separated Values Files (*.png)", options=options)
        if save_file:
            ext = ""
            # check if user input a .csv file extension: if not, append with .csv
            for x in [-4,-3,-2,-1]:
                end = str(self.save_file[x])
                ext += end
            if (ext == ".png"):                
                self.imageName = save_file
            else:
                save_file += ".png"
                self.imageName = save_file        
            #saveimage
            c = MplWidget()
            c.saveImage(self.imageName)

    # initial loading function
    def load_init(self):
        self.model.clear()
        self.loadCsv(self.save_file)

    def on_pushButtonReturn_clicked(self):
        self.startover.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit()    
    
    def on_pushButtonBack_clicked(self):
        self.back.emit()


    # .csv functions
    def loadCsv(self, fileName):
        row_dict = settings.myList['row_dict']
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)
                compCounter = settings.myList['compCounter']
                numCol = compCounter + 5
                for rowNum1 in range(0,len(list(csv.reader(fileName)))):
                    for colNum1 in range(0,numCol):
                        self.model.setData(
                                    self.model.index(rowNum1, colNum1), QtCore.Qt.AlignCenter, 
                                    QtCore.Qt.TextAlignmentRole
                                )
                        if rowNum1 == 0:
                            self.model.setData(
                                    self.model.index(0, colNum1), QBrush(
                                        QColor(214,188,138)), QtCore.Qt.BackgroundRole
                                )

    def writeCsv(self, fileName):
        with open(fileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = []
                for columnNumber in range(self.model.columnCount()):
                    cell = self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    self.model.setData(
                            self.model.index(rowNumber, columnNumber), QtCore.Qt.AlignCenter, 
                            QtCore.Qt.TextAlignmentRole
                        )
                    fields.append(cell)
                writer.writerow(fields)
    
# class that plots the station placement results from taskgrouping.py
class MplWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__ ( self ,  parent )
        self.setParent(parent)
        self.canvas  =  FigureCanvas ( Figure()) # figsize=(4, 4), dpi=100))
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
  
        self.canvas.axes  =  self.canvas.figure.add_subplot(111)        
    
        self.fileName = "StationPlacement.png"
        ax = self.canvas.axes
        ax.set_title('Layout Results')
        xgrid, ygrid, maxwidth, maxlen = 0, 0, 0, 0
        ax.grid(True)

        placement = settings.myList['placement']
        stations  = settings.myList['real_stations']
        a = len(stations)
        rect = []
        for s in range(0,a):
            self.stationLength = placement[s][0]
            self.stationWidth = placement[s][1]
            self.xlcorner = placement[s][2]
            self.ylcorner = placement[s][3]
            self.cx = self.xlcorner + self.stationLength/2
            self.cy = self.ylcorner + self.stationWidth/2

            if placement[s][2]>xgrid:
                xgrid=placement[s][2]
            if placement[s][3]>ygrid:
                ygrid=placement[s][3]
            if placement[s][1]>maxwidth:
                maxwidth=placement[s][1]
            if placement[s][0]>maxlen:
                maxlen=placement[s][0]

            rect.append(
                patches.Rectangle((self.xlcorner, self.ylcorner), self.stationLength,
                                  self.stationWidth, fc = '#d6bc8a',linewidth=1.5, edgecolor='k', fill='False')
            )
                        
            ax.text(self.cx, self.cy, 'S%1i' % (s+1), color='k', 
                    ha='center', va='center', weight='bold')
        spacer = 1
        lastStationLength = placement[a-1][0]
        Xbound = xgrid+lastStationLength+spacer
        Ybound = ygrid+maxwidth+spacer
        ax.set_xticks(numpy.arange(0, numpy.ceil(Xbound)+numpy.ceil(Xbound/10)+1, step=numpy.ceil(Xbound/10)))
        ax.set_yticks(numpy.arange(0, numpy.ceil(Ybound)+1, step=numpy.ceil(Ybound/10)))

        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')

        for item in rect:
            ax.add_patch(item)

        plt.show()

    def saveImage(self, fileName):
        with open(fileName, "wb") as layoutImage:
            self.canvas.axes.figure.savefig(layoutImage)

class Controller:

    def __init__(self):
        pass

    # primary window functions

    def show_splash(self):
        self.splash = SplashWindow()
        self.splash.helpOpen.connect(self.show_help)
        self.splash.dataOpen.connect(self.show_main)
        self.splash.dataOpen.connect(self.splash.close)
        self.splash.show()

    def show_main(self):
        self.window = DataWindow()
        self.window.startup() # .csv shows on startup
        self.window.helpOpen.connect(self.show_help)
        self.window.results.connect(self.show_check)
        self.window.error.connect(self.show_error)
        self.window.show()

    def show_check(self):
        self.check = Check(self.window.fileName)
        self.check.cancel.connect(self.check.close) 
        self.check.go.connect(self.show_results)
        self.check.save.connect(self.new_save)
        self.check.show()

    def new_save(self):
        self.window.save_table()
        if(self.window.temp_file):
            self.check.fileName = self.window.fileName
            self.show_results()        
    
    def show_results(self):
        self.check.close()
        control.run_opt(self.check.fileName)
        self.results = ResultsWindow()
        self.results.load_init() # .csv shows on startup
        self.results.helpOpen.connect(self.show_help)
        self.results.startover.connect(self.show_warning_exit)
        self.results.back.connect(self.show_warning_back)
        self.window.close()
        self.results.show()
    
    ## secondary window functions 

    def show_help(self):
        self.help = HelpWindow()
        self.help.done.connect(self.help.close)
        self.help.show()
        
    def show_error(self):
        self.error = Error(self.window.fileName)
        self.error.go.connect(self.new_upload)
        self.error.cancel.connect(self.error.close)
        self.error.show()

    def new_upload(self):
        self.window.upload()
        self.error.close() 

    def show_warning_exit(self):
        self.warning = Warning()
        self.warning.go.connect(self.exit)
        self.warning.cancel.connect(self.close_warning)
        self.warning.show()

    def show_warning_back(self):
        self.warning = Warning()
        self.warning.go.connect(self.return_to_input)
        self.warning.cancel.connect(self.close_warning)
        self.warning.show()

    def close_warning(self):
        self.warning.close()
    
    def return_to_input(self):
        self.warning.close()
        self.results.close()
        self.window.show()

    def exit(self):
        self.warning.close()
        self.results.close()
        

app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
controller = Controller()
controller.show_splash()
sys.exit(app.exec_())
