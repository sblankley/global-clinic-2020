#!/usr/bin/env python
#-*- coding:utf-8 -*
#main.py

### Setup

# import necessary libraries
import backend
from backend import taskgrouping, CSVReader, settings, control 
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

backend.settings.init() # initialize "global" variables list

### UI Classes

class SplashWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()
    dataOpen = QtCore.pyqtSignal()

    def __init__(self):
        # General HelpWindow settings 
        super(SplashWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('backend\splash.ui', self) # Load the splash window .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("HMC Optimization Suite")
        self.setWindowIcon(QIcon('backend\hmc.png'))

        # Settings specific to the Splash Window 

    def on_pushButtonContinueToInput_clicked(self):
        self.dataOpen.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit() 

class Warning(QtWidgets.QMainWindow):

    go = QtCore.pyqtSignal()
    cancel = QtCore.pyqtSignal()

    def __init__(self):
        super(Warning, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('backend\warning.ui', self) # Load the main .ui file
        self.setWindowTitle('Unsaved changes will be lost!')        
        self.setWindowIcon(QIcon('backend\hmc.png'))

        layout = QtWidgets.QGridLayout()
    
    def on_pushButtonContinue_clicked(self):
        self.go.emit()

    def on_pushButtonCancel_clicked(self):
        self.cancel.emit()


class Check(QtWidgets.QMainWindow):

    save = QtCore.pyqtSignal()
    go = QtCore.pyqtSignal()
    cancel = QtCore.pyqtSignal()

    def __init__(self, fileName):
        super(Check, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('backend\check.ui', self) # Load the main .ui file
        self.setWindowTitle('Unsaved changes will be lost!')        
        self.setWindowIcon(QIcon('backend\hmc.png'))

        layout = QtWidgets.QGridLayout()

        self.fileName = fileName
        # push button connection
        #self.pushButtonContinue.clicked.connect(self.save_table)
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
    #
    # Initialize the GUI window and define the objects within it
    #
    def __init__(self):
        super(DataWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('backend\dataWindow.ui', self) # Load the main .ui file

        self.fileName = r'backend\template.csv' # default input filename
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("HMC Optimization Suite")
        self.setWindowIcon(QIcon('backend\hmc.png'))
        self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
        self.tableView.setModel(self.model)

        # manually connect pushbuttons to avoid doubling the connection when using auto-connect
        self.pushButtonLoad.clicked.connect(self.upload)
        self.pushButtonWrite.clicked.connect(self.save_table)

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #
    # startup function to load template
    #
    def startup(self):
        self.model.clear()
        self.loadCsv(self.fileName)
    #
    # Functions for connecting buttons to external functionality
    #
    def on_pushButtonResults_clicked(self):
        self.results.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit()    

    def upload(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        new, _ = QFileDialog.getOpenFileName(None, "Choose input data file", "", "Comma Separated Value Files, (* .csv)", options = options )
        if(new):
            self.fileName = new
            self.model.clear()
            self.loadCsv(self.fileName)
    
    def save_table(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_file, _ = QFileDialog.getSaveFileName(None,"Choose input file to save","","Comma Separated Values Files (*.csv)", options=options)
        if save_file:
            ext = ""
            # check if user input a .csv file extension: if not, append with .csv
            for x in [-4,-3,-2,-1]:
                end = str(save_file[x])
                ext += end
            if (ext == ".csv"):                
                self.fileName = save_file
            else:
                save_file += ".csv"
                self.fileName = save_file        
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
                self.model.appendRow(items)
                for rowNum1 in range(0,len(list(csv.reader(fileName)))+1):
                    for colNum1 in range(0,10):
                        self.model.setData(
                                    self.model.index(rowNum1, colNum1), QtCore.Qt.AlignCenter, 
                                    QtCore.Qt.TextAlignmentRole
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
        uic.loadUi('backend\help.ui', self) # Load the main .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("HMC Optimization Suite Help")
        self.setWindowIcon(QIcon('backend\hmc.png'))

    def on_pushButtonDone_clicked(self):
        self.done.emit()

class ResultsWindow(QtWidgets.QMainWindow):

    startover = QtCore.pyqtSignal()
    helpOpen = QtCore.pyqtSignal()

    # Initialize the GUI window and define the objects within it
    def __init__(self):
       super(ResultsWindow, self).__init__() # Call the inherited classes __init__ method
       uic.loadUi(r'backend\results.ui', self) # Load the main .ui file, prepend with 'r' to avoid '/r' issue
       self.fileName = "pLineOpt.csv" # default output file name
       self.imageName = "StationLayout.png" # default output file name
       self.model = QtGui.QStandardItemModel(self)
       self.setWindowTitle("HMC Optimization Results")
       self.setWindowIcon(QIcon('backend\hmc.png'))
       self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
       self.tableView.setModel(self.model)
       self.initUI()

       self.pushButtonSaveTable.clicked.connect(self.save_table)   # create non-implicit function to avoid double-press issue
       self.pushButtonSaveLayout.clicked.connect(self.save_layout) # ^

       # tableview settings to have window contents dynamically resize
       self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
       self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
   
    def initUI(self):
        mainWindow = self
        width = mainWindow.frameGeometry().width()*0.00466
        height = mainWindow.frameGeometry().height()*0.0093
        canvas = Canvas(self, width, height)
        canvas.move(0,0)
        self.show()

    def save_table(self):
        # system dialog code
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_file, _ = QFileDialog.getSaveFileName(None,"Choose output data file","","Comma Separated Values Files (*.csv)", options=options)
        if save_file:
            print(save_file)
            ext = ""
            for x in [-4,-3,-2,-1]:
                end = str(save_file[x])
                ext += end
            print(ext)
            if (ext == ".csv"):                
                self.fileName = save_file
            else:
                save_file += ".csv"
                self.fileName = save_file        
            #csvwrite
            self.writeCsv(self.fileName)

    def save_layout(self):
    # system dialog code
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_file, _ = QFileDialog.getSaveFileName(None,"Choose output data file","","Comma Separated Values Files (*.png)", options=options)
        if save_file:
            print(save_file)
            ext = ""
            # check if user input a .csv file extension: if not, append with .csv
            for x in [-4,-3,-2,-1]:
                end = str(save_file[x])
                ext += end
            print(ext)
            if (ext == ".png"):                
                self.imageName = save_file
            else:
                save_file += ".png"
                self.imageName = save_file        
            #saveimage
            c = Canvas(self, width=6, height=7.2)
            c.saveImage(self.imageName)

    # initial loading function
    def load_init(self):
        self.model.clear()
        self.loadCsv(self.fileName)

    def on_pushButtonReturn_clicked(self):
        self.startover.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit()    
    
    # .csv functions
    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

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
    
class Canvas(FigureCanvas):
    def __init__(self, parent = None, width=10, height=10, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.fileName = "StationPlacement.png"
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        ax = self.axes
        ax.set_title('Layout Results')
        xgrid, ygrid, maxwidth, maxlen = 0, 0, 0, 0
        ax.grid(True)

        placement = settings.myList['placement']
        stations  = settings.myList['real_stations']
        a = len(stations)
        rect = []
        for s in range(0,a):
            self.stationWidth = placement[s][0]
            self.stationLength = placement[s][1]
            self.xlcorner = placement[s][2]
            self.ylcorner = placement[s][3]
            self.cx = self.xlcorner + self.stationWidth/2
            self.cy = self.ylcorner + self.stationLength/2

            if placement[s][2]>xgrid:
                xgrid=placement[s][2]
            if placement[s][3]>ygrid:
                ygrid=placement[s][3]
            if placement[s][1]>maxlen:
                maxlen=placement[s][1]
            if placement[s][0]>maxwidth:
                maxwidth=placement[s][0]
            
            print(placement)

            rect.append(
                patches.Rectangle((self.xlcorner, self.ylcorner), self.stationWidth,
                                  self.stationLength, fc = '#d6bc8a',linewidth=1.5, edgecolor='k', fill='False')
            )
                        
            ax.text(self.cx, self.cy, 'S%1i' % (s+1), color='k', 
                    ha='center', va='center', weight='bold')

            Xbound = 1.2*xgrid+maxwidth
            Ybound = 2*ygrid+maxlen
            ax.set_xticks(numpy.arange(0, numpy.rint(Xbound), step=numpy.ceil(Xbound/10)))
            ax.set_yticks(numpy.arange(0, numpy.rint(Ybound), step=numpy.ceil(Ybound/10)))

            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
        for item in rect:
            ax.add_patch(item)

        plt.show()

    def saveImage(self, fileName):
        with open(fileName, "wb") as layoutImage:
            self.axes.figure.savefig(layoutImage)

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

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
        self.window.show()

    def show_check(self):
        self.check = Check(self.window.fileName)
        self.check.cancel.connect(self.check.close) 
        self.check.go.connect(self.show_results)
        self.check.save.connect(self.new_save)
        self.check.show()

    def new_save(self):
        self.window.save_table()
        self.show_results()        

    def show_results(self):
        self.check.close()
        control.run_opt(self.check.fileName)
        self.results = ResultsWindow()
        self.results.load_init() # .csv shows on startup
        self.results.helpOpen.connect(self.show_help)
        self.results.startover.connect(self.show_warning)
        self.window.close()
        self.results.show()
    
    ## secondary window functions 

    def show_help(self):
        self.help = HelpWindow()
        self.help.done.connect(self.close_help)
        self.help.show()

    def close_help(self):
        self.help.close()

    def show_warning(self):
        self.warning = Warning()
        self.warning.go.connect(self.close_results)
        self.warning.cancel.connect(self.close_warning)
        self.warning.show()

    def close_warning(self):
        self.warning.close()
    
    def close_results(self):
        self.warning.close()
        self.results.close()
        

app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_splash()
sys.exit(app.exec_())


if __name__ == '__main__':
    main()
