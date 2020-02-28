import csv

from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtWidgets import QApplication, QLabel
# from PyQt5.QtCore import Qt

# from PyQt5.uic import loadUi

#   from PyQt5 import QtWidgets, uic


# class Ui(QtWidgets.QDialog):
#     def __init__(self):



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, fileName, parent=None):
        super(MainWindow, self).__init__(parent)
        self.fileName = fileName

        self.setWindowTitle("My Awesome App")

        # label = QtWidgets.QLabel("hello")
        # label.setAlignment(QtCore.Qt.AlignCenter)
        # self.setCentralWidget(label)

        uic.loadUi('table_test.ui', self) # Load the .ui file

        self.model = QtGui.QStandardItemModel(self)

        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.pushButtonSave.clicked.connect(self.on_pushButtonSave_clicked)
        
        self.loadCsv(self.fileName)

        # super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        
        # self.show() # Show the GUI

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

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonSave_clicked(self):
        self.writeCsv(self.fileName)
    

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MainWindow')

    main = MainWindow("data.csv")
    main.show()

    sys.exit(app.exec_())


  
# import sys



# app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
# window = MainWindow() # Create an instance of our class
# app.exec_() # Start the application