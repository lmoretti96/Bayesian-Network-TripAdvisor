#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        #Labels
        self.overall = QtGui.QLabel('Overall')
        self.value = QtGui.QLabel('Value')
        self.rooms = QtGui.QLabel('Rooms')
        self.location = QtGui.QLabel('Location')
        self.cleanliness = QtGui.QLabel('Cleanliness')
        self.service = QtGui.QLabel('Service')
        self.review = QtGui.QLabel('Review')
        self.result = QtGui.QLabel('')

        #Bottoni
        self.button = QtGui.QPushButton("Esegui")

        #EditLines
        self.overallEdit = QtGui.QLineEdit()
        self.valueEdit = QtGui.QLineEdit()
        self.roomsEdit = QtGui.QLineEdit()
        self.locationEdit = QtGui.QLineEdit()
        self.cleanlinessEdit = QtGui.QLineEdit()
        self.serviceEdit = QtGui.QLineEdit()
        self.reviewEdit = QtGui.QTextEdit()
        self.edits = [self.overallEdit, self.valueEdit, self.roomsEdit, self.locationEdit, self.cleanlinessEdit, self.serviceEdit, self.reviewEdit]

        #Pozionamento elementi nella griglia
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.overall, 1, 0)
        grid.addWidget(self.overallEdit, 1, 1)
        grid.addWidget(self.value, 2, 0)
        grid.addWidget(self.valueEdit, 2, 1)
        grid.addWidget(self.location, 3, 0)
        grid.addWidget(self.locationEdit, 3, 1)
        grid.addWidget(self.cleanliness, 4, 0)
        grid.addWidget(self.cleanlinessEdit, 4, 1)
        grid.addWidget(self.service, 5, 0)
        grid.addWidget(self.serviceEdit, 5, 1)
        grid.addWidget(self.rooms, 6, 0)
        grid.addWidget(self.roomsEdit, 6, 1)
        grid.addWidget(self.review, 7, 0)
        grid.addWidget(self.reviewEdit, 7, 1)
        grid.addWidget(self.button, 8,1)
        grid.addWidget(self.result, 9,1)

        #Azioni triggerate
        self.button.clicked.connect(self.buttonClicked)   
        self.overallEdit.editingFinished.connect(self.editingFinished)
        self.valueEdit.editingFinished.connect(self.editingFinished)
        self.locationEdit.editingFinished.connect(self.editingFinished)
        self.cleanlinessEdit.editingFinished.connect(self.editingFinished)
        self.serviceEdit.editingFinished.connect(self.editingFinished)
        self.roomsEdit.editingFinished.connect(self.editingFinished)

        #info sulla finestra
        self.setLayout(grid) 
        self.setGeometry(500, 500, 350, 300)
        self.setWindowTitle('Review')    
        self.show()
        
    def buttonClicked(self):
        sender = self.sender()
        print("eseguita funzione")
        self.result.setText("Risultato ")
    
    def editingFinished(self):
        sender = self.sender()
        edits = self.edits
        for edit in edits:
            value = edit.text()
            text = False
            if(value != ""):
                try:
                    value = int(value)
                except:
                    text = True
                if (text) or (value <= 0) or (value>5) and not (value == None) :
                    edit.setText("inserire valore compreso tra 1 e 5")


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()