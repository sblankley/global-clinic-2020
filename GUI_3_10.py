#!/usr/bin/env python
#-*- coding:utf-8 -*
#GUI_3_10.py

import sys, csv 
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import result_trigger

class SplashWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()
    dataOpen = QtCore.pyqtSignal()

    def __init__(self):
        # General HelpWindow settings 
        super(SplashWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('splash.ui', self) # Load the splash window .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("HMC Optimization Suite")
        self.setWindowIcon(QIcon('hmc.png'))

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
        uic.loadUi('warning.ui', self) # Load the main .ui file
        self.setWindowTitle('Warning')        
        self.setWindowIcon(QIcon('hmc.png'))

        layout = QtWidgets.QGridLayout()
    
    def on_pushButtonContinue_clicked(self):
        self.go.emit()

    def on_pushButtonCancel_clicked(self):
        self.cancel.emit()

class DataWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()
    results  = QtCore.pyqtSignal()
    # fileOpen = QtCore.pyqtSignal()


    # Initialize the GUI window and define the objects within it
    def __init__(self,fileName):
       super(DataWindow, self).__init__() # Call the inherited classes __init__ method
       uic.loadUi('table_test_OG.ui', self) # Load the main .ui file

       self.fileName = fileName
       self.model = QtGui.QStandardItemModel(self)
       self.setWindowTitle("HMC Optimization Suite")
       self.setWindowIcon(QIcon('hmc.png'))
       self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
       self.tableView.setModel(self.model)


    
    # Functions for connecting buttons to external functionality
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)
        # self.openFile.emit()
        # self.window.openFile.connect(self.open_file)

    def on_pushButtonLoad_clicked(self):
        self.model.clear()
        self.loadCsv(self.fileName)

    def on_pushButtonResults_clicked(self):
        self.results.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit()    

    # .csv functions
    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                # This didn't work to color the takt time cells
                    # if self.model.index(row) == "-":
                    #     return QBrush(Qt.black) 
                ]
                self.model.appendRow(items)

                # self.check = QtGui.QStandardItem.setCheckState(items)
                # if self.check == "1"
                #     return QtGui.QStandardItem.setBackground(QBrush, Qt.black)

                # Also didn't work to color the takt time cells
                # index = self.tableView.currentIndex()
                # NewIndex = self.tableView.model().index(index.row(), 6)
                # print('Index is :', NewIndex)
                # Name = self.tableView.model().data(NewIndex)
                # if Name == "-": 
                #     return QBrush(Qt.black)

    def writeCsv(self, fileName):
        with open(fileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)
            
    # def color(self,filName):
        # for rowNumber in range(start:6, stop:6, step:1) and columnNumber in range(start:2, stop:max(self.model.colmnCount), step:1):


    ## Making the background cell colored: 
    # def flags(self, index):
    #     return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        
    # def data(self, index, role):
    #     if index.isValid():
    #         data, changed = self._data[index.row()][index.column()]

    #         if role in [Qt.DisplayRole, Qt.EditRole]:
    #             return data

    #         if role == Qt.BackgroundRole and data == "-":        # <---------
    #             return QBrush(Qt.black) 

    # def setData(self, index, value, role):
    #     if role == Qt.EditRole:
    #         self._data[index.row()][index.column()] = [value, True]
    #         self.dataChanged.emit(index, index)
    #         return True
    #     return False

class HelpWindow(QtWidgets.QMainWindow):

    done = QtCore.pyqtSignal()

    def __init__(self):
        # General HelpWindow settings 
        super(HelpWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('help.ui', self) # Load the main .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("HMC Optimization Suite Help")
        self.setWindowIcon(QIcon('hmc.png'))

        # Settings specific to the Help Window

    def on_pushButtonDone_clicked(self):
        self.done.emit()

# class Label(QtWidgets.QLabel):
#     def __init__(self, parent=None):
#         super(Label, self).__init__(parent=parent)

#     def paintEvent(self, e):
#         super().paintEvent(e)
#         painter = Qt.Gui.QPainter(self)
#         painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
#         painter.drawRect(600,50,40,20)

class ResultsWindow(QtWidgets.QMainWindow):

    startover = QtCore.pyqtSignal()
    helpOpen = QtCore.pyqtSignal()

    # Initialize the GUI window and define the objects within it
    def __init__(self,fileName):
       super(ResultsWindow, self).__init__() # Call the inherited classes __init__ method
       uic.loadUi('results.ui', self) # Load the main .ui file
       self.fileName = fileName
       self.model = QtGui.QStandardItemModel(self)
       self.setWindowTitle("HMC Optimization Results")
       self.setWindowIcon(QIcon('hmc.png'))
       self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
       self.tableView.setModel(self.model)

       self.box = QtWidgets.QGraphicsView(self)
       self.box.setGeometry(600, 50, 40, 20)
       self.box.setStyleSheet('QGraphicsView { background: rgba(255,255,255,.5); border: 2px solid black }')

       self.box = QtWidgets.QGraphicsView(self)
       self.box.setGeometry(650, 100, 70, 30)
       self.box.setStyleSheet('QGraphicsView { background: rgba(255,255,255,.5); border: 2px solid black }')

       self.box = QtWidgets.QGraphicsView(self)
       self.box.setGeometry(500, 200, 30, 80)
       self.box.setStyleSheet('QGraphicsView { background: rgba(255,255,255,.5); border: 2px solid black }')

       self.box = QtWidgets.QGraphicsView(self)
       self.box.setGeometry(800, 70, 20, 50)
       self.box.setStyleSheet('QGraphicsView { background: rgba(255,255,255,.5); border: 2px solid black }')

       self.box = QtWidgets.QGraphicsView(self)
       self.box.setGeometry(700, 200, 100, 60)
       self.box.setStyleSheet('QGraphicsView { background: rgba(255,255,255,.5); border: 2px solid black }')

       self.text = QtWidgets.QGraphicsTextItem("Hello world")
       self.text.setPos(650, 100)
    #    self.Label = QtWidgets.QLabel(self)
    #    self.setCentralWidget(self.centralwidget)
    #    self.centralwidget = QtWidgets.QWidget(self)
    #    self.centralwidget.setObjectName("centralwidget")
    
    # Functions for connecting buttons to external functionality  
        
    # def paintEvent(self, e):
    #     # super().paintEvent(e)
    #     painter = QPainter(self)
    #     painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
    #     painter.drawRect(600,50,40,20)

    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

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
                
                # self.data = QtWidgets.QTableView(self.model)
                # self.data.resizeColumnsToContents()
     

    def writeCsv(self, fileName):
        with open(fileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)

class Controller:

    def __init__(self):
        pass

    # def file_open(self):
    #     self.openFile = QtGui.QAction("&Open File", self)
    # #    self.openFile.setShortcut("Ctrl+O")
    #     self.openFile.setStatusTip('Open File')
        

    def show_splash(self):
        self.splash = SplashWindow()
        self.splash.helpOpen.connect(self.show_help)
        self.splash.dataOpen.connect(self.show_main)
        self.splash.dataOpen.connect(self.close_splash)
        self.splash.show()

    def close_splash(self):
        self.splash.close()

    def show_main(self):
        #self.welcome.close()
        self.window = DataWindow("pLine.csv")
        # self.window.data(index,Qt.DisplayRole)
        self.window.on_pushButtonLoad_clicked() # call this in the defn. to have .csv show on startup
        self.window.helpOpen.connect(self.show_help)
        #self.window.results.connect(self.wait_for_results)
        self.window.results.connect(self.show_results)
        self.window.on_pushButtonWrite_clicked()
        self.window.show()
    
    def show_help(self):
        self.help = HelpWindow()
        self.help.done.connect(self.close_help)
        self.help.show()

    def close_help(self):
        self.help.close()
    
    def wait_for_results(self):
        self.wait = WaitWindow()
        #self.wait.done.connect(self.show_results)
        self.wait.show()
        # result_trigger.run_optimization()
        # result_trigger.translate_to_csv()
        self.wait.hide()
        self.results.show()

    def show_results(self):
        result_trigger.run_optimization()
        result_trigger.translate_to_csv()
        self.results = ResultsWindow("pLineOpt.csv")
        self.results.load_init() # call this in the defn. to have .csv show on startup
        self.results.helpOpen.connect(self.show_help)
        self.results.startover.connect(self.show_warning)
        #self.wait.close()
        self.window.close()
        self.results.show()

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
        # self.window.close()
        



app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_splash()
sys.exit(app.exec_())


if __name__ == '__main__':
    main()




#class WaitWindow(QtWidgets.QMainWindow):

#     startover = QtCore.pyqtSignal()
#     done = QtCore.pyqtSignal()

#     # Initialize the GUI window and define the objects within it
#     def __init__(self):
#        super(WaitWindow, self).__init__() # Call the inherited classes __init__ method
#        uic.loadUi('wait_for_results.ui', self) # Load the main .ui file

#        self.model = QtGui.QStandardItemModel(self)
#        self.setWindowTitle("Waiting for HMC Optimization Results...")
#        self.setWindowIcon(QIcon('hmc.png'))
    
#     # Functions for connecting buttons to external functionality
#     def on_pushButtonWrite_clicked(self):
#         self.writeCsv(self.fileName)

#     def on_pushButtonLoad_clicked(self):
#         self.model.clear()
#         self.loadCsv(self.fileName)

#     def on_pushButtonReturn_clicked(self):
#         self.startover.emit()
    
#     def on_pushButtonDone_clicked(self):
#         self.done.emit()  