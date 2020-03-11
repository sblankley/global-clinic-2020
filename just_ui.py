import csv
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self, fileName):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('table_test_OG.ui', self) # Load the .ui file

        self.fileName = fileName
        self.model = QtGui.QStandardItemModel(self)

        self.setWindowTitle("GUI Tab!")
        self.tableView = self.findChild(QtWidgets.QTableView,"tableView")
        self.tableView.setModel(self.model)

        self.pushButtonLoad = self.findChild(QtWidgets.QPushButton, "pushButtonLoad")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonWrite = self.findChild(QtWidgets.QPushButton, "pushButtonWrite")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.pushButtonContinue = self.findChild(QtWidgets.QPushButton, "pushButtonResults")
        self.pushButtonContinue.clicked.connect(self.on_pushButtonResults_clicked)

        #self.pushButtonContinue = self.findChild(QtWidgets.QPushButton, "pushButtonReturn")
        #self.pushButtonContinue.clicked.connect(self.on_pushButtonReturn_clicked)

        self.pushButtonHelp = self.findChild(QtWidgets.QPushButton, "pushButtonHelp")
        self.pushButtonHelp.clicked.connect(self.on_pushButtonHelp_clicked)

        #self.pushButtonDone = self.findChild(QtWidgets.QPushButton, "pushButtonDone")
        #self.pushButtonDone.clicked.connect(self.on_pushButtonDone_clicked)

        self.show()
        self.loadCsv(self.fileName)

    def loadCsv(self, fileName):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)
     

    def writeCsv(self, fileName):
        with open(fileName, "w") as fileOutput:
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

    # @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.model.clear()
        self.loadCsv(self.fileName)

    def on_pushButtonResults_clicked(self):
        # uic.hide('table_test.ui', self)
        uic.loadUi('tab3.ui', self)

    def on_pushButtonDone_clicked(self):
        #uic.hide('help.ui', self)
        uic.loadUi('table_test_OG.ui', self)

    #def on_pushButtonReturn_clicked(self):
    
    def on_pushButtonHelp_clicked(self):
        #uic.hide('table_test.ui', self)
        uic.loadUi('help.ui', self)


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui("pLine.csv") # Create an instance of our class
app.exec_() # Start the application