import csv, sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#import new


class DataWindow(QtWidgets.QMainWindow):

    helpOpen = QtCore.pyqtSignal()

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
       
       #self.show()
       #self.loadCsv(self.fileName)
   
    # .csv functions
    # def loadCsv(self, fileName):
    #     with open(fileName, "r") as fileInput:
    #         for row in csv.reader(fileInput):    
    #             items = [
    #                 QtGui.QStandardItem(field)
    #                 for field in row
    #             ]
    #             self.model.appendRow(items)

    # def writeCsv(self, fileName):
    #     with open(fileName, "w") as fileOutput:
    #         writer = csv.writer(fileOutput)
    #         for rowNumber in range(self.model.rowCount()):
    #             fields = [
    #                 self.model.data(
    #                     self.model.index(rowNumber, columnNumber),
    #                     QtCore.Qt.DisplayRole
    #                 )
    #                 for columnNumber in range(self.model.columnCount())
    #             ]
    #             writer.writerow(fields)

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
    
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

    def on_pushButtonLoad_clicked(self):
        self.model.clear()
        self.loadCsv(self.fileName)

    def on_pushButtonResults_clicked(self):
        self.helpOpen.emit()
    
    def on_pushButtonHelp_clicked(self):
        self.helpOpen.emit()    

class HelpWindow(QtWidgets.QMainWindow):

    done = QtCore.pyqtSignal()

    def __init__(self):
        # General MainWindow settings 
        super(HelpWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('help.ui', self) # Load the main .ui file
        self.model = QtGui.QStandardItemModel(self)
        self.setWindowTitle("HMC Optimization Suite Help")
        self.setWindowIcon(QIcon('hmc.png'))

        # Settings specific to the Help Window

    def on_pushButtonDone_clicked(self):
        self.done.emit()

class Login(QtWidgets.QWidget):

    open_main = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def login(self):
        self.open_main.emit()


class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.window = DataWindow("pLine.csv")
        self.window.on_pushButtonLoad_clicked()
        #self.window.helpOpen.connect(self.show_login)
        self.window.helpOpen.connect(self.show_help)
        self.window.show()
    
    def show_help(self):
        self.help = HelpWindow()
        self.help.done.connect(self.close_help)
        self.help.show()

    def show_login(self):
        self.login = Login()
        self.login.open_main.connect(self.close_login)
        self.login.show()

    def show_window_two(self, text):
        self.window_two = WindowTwo(text)
        self.window.close()
        self.window_two.show()

    def close_help(self):
        self.help.close()
        self.window.show()


app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_main()
sys.exit(app.exec_())


if __name__ == '__main__':
    main()