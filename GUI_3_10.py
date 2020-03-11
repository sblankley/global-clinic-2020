#!/usr/bin/env python
#-*- coding:utf-8 -*
#GUI_3_10.py

import sys, csv 
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import result_trigger

class Warning(QtWidgets.QMainWindow):

    go = QtCore.pyqtSignal()
    cancel = QtCore.pyqtSignal()

    def __init__(self):
        super(Warning, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('warning.ui', self) # Load the main .ui file
        self.setWindowTitle('Warning!')        
        self.setWindowIcon(QIcon('hmc.png'))

        layout = QtWidgets.QGridLayout()
    
    def on_pushButtonContinue_clicked(self):
        self.go.emit()

    def on_pushButtonCancel_clicked(self):
        self.cancel.emit()

class DataWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()
    results  = QtCore.pyqtSignal()

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
                ]
                self.model.appendRow(items)

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

class ResultsWindow(QtWidgets.QMainWindow):

    startover = QtCore.pyqtSignal()
    helpOpen = QtCore.pyqtSignal()

    # Initialize the GUI window and define the objects within it
    def __init__(self,fileName):
       super(ResultsWindow, self).__init__() # Call the inherited classes __init__ method
       uic.loadUi('results.ui', self) # Load the main .ui file

       self.fileName = fileName
       self.model = QtGui.QStandardItemModel(self)
       self.setWindowTitle("HMC Optimization Results!")
       self.setWindowIcon(QIcon('hmc.png'))
       self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
       self.tableView.setModel(self.model)
    
    # Functions for connecting buttons to external functionality
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

    # def show_welcome(self):
    #     self.welcome = Welcome()
    #     self.welcome.pushbutton.connect(self.show_main)
    #     self.welcome.show()

    def show_main(self):
        #self.welcome.close()
        self.window = DataWindow("pLine.csv")
        self.window.on_pushButtonLoad_clicked() # call this in the defn. to have .csv show on startup
        self.window.helpOpen.connect(self.show_help)
        #self.window.results.connect(self.wait_for_results)
        self.window.results.connect(self.show_results)
        self.window.show()
    
    def show_help(self):
        self.help = HelpWindow()
        self.help.done.connect(self.close_help)
        self.help.show()

    def close_help(self):
        self.help.close()
    
    def wait_for_results(self):
        self.wait = WaitWindow()
        self.wait.done.connect(self.show_results)
        self.wait.show()
        # result_trigger.run_optimization()
        # result_trigger.translate_to_csv()


    def show_results(self):
        result_trigger.run_optimization()
        result_trigger.translate_to_csv()
        self.results = ResultsWindow("pLineOpt.csv")
        self.results.load_init() # call this in the defn. to have .csv show on startup
        self.results.helpOpen.connect(self.show_help)
        self.results.startover.connect(self.show_warning)
        #self.wait.close()
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
        self.window.show()



app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_main()
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