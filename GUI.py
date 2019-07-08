#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from GUIFunctions import fun
import re
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        #Labels
        #self.overall = QtGui.QLabel('Overall')
        self.value = QtGui.QLabel('Value')
        self.rooms = QtGui.QLabel('Rooms')
        self.location = QtGui.QLabel('Location')
        self.cleanliness = QtGui.QLabel('Cleanliness')
        self.service = QtGui.QLabel('Service')
        self.review = QtGui.QLabel('Review')
        self.result = QtGui.QLabel('')
        self.n=0
        #Bottoni
        self.button = QtGui.QPushButton("Esegui")
        self.button.setEnabled(False)

        #EditLines
        #self.overallEdit = QtGui.QLineEdit()
        self.valueEdit = QtGui.QLineEdit()
        self.roomsEdit = QtGui.QLineEdit()
        self.locationEdit = QtGui.QLineEdit()
        self.cleanlinessEdit = QtGui.QLineEdit()
        self.serviceEdit = QtGui.QLineEdit()
        self.reviewEdit = QtGui.QTextEdit()
        self.edits = [self.valueEdit, self.locationEdit, self.cleanlinessEdit, self.serviceEdit, self.roomsEdit]

        #Pozionamento elementi nella griglia
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        #grid.addWidget(self.overall, 1, 0)
        #grid.addWidget(self.overallEdit, 1, 1)
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
        #self.overallEdit.editingFinished.connect(self.editingFinished)
        self.valueEdit.editingFinished.connect(self.editingFinished)
        self.locationEdit.editingFinished.connect(self.editingFinished)
        self.cleanlinessEdit.editingFinished.connect(self.editingFinished)
        self.serviceEdit.editingFinished.connect(self.editingFinished)
        self.roomsEdit.editingFinished.connect(self.editingFinished)
        

        #info sulla finestra
        self.setLayout(grid) 
        self.setGeometry(500, 500, 350, 300)
        self.setWindowTitle('Review Demo')    
        self.show()
        

    def buttonClicked(self):
        plt.close()
        sender = self.sender()
        #overall = self.overall.text()
        value = self.value.text()
        location = self.location.text()
        cleanliness = self.cleanliness.text()
        service = self.service.text()
        rooms = self.rooms.text()
        data = []
        for edit in self.edits:
            data.append(int(edit.text()))

        text = self.reviewEdit.toPlainText()
        keywords = ["bad", "old,", "good", "great", "comfortable", "clean"]
        for keyword in keywords:
            if re.search(keyword, text, re.IGNORECASE):
                data.append(1)
            else:
                data.append(0)
        result = fun(data)
        strResult = "classe 1:\t" + str(round(float(result[1L])*100, 2))+" % " + "\n" + "classe 2:\t" + str(round(float(result[2L]*100), 2))+" %" + "\n" + "classe 3:\t" + str(round(float(result[3L]*100), 2))+" %" + "\n" + "classe 4:\t" + str(round(float(result[4L]*100), 2))+" %" + "\n" + "classe 5:\t" + str(round(float(result[5L]*100), 2))+" %"
        print("eseguita funzione")       
        self.result.setText(strResult)


        objects = ("Classe 1", "Classe 2", "Classe 3", "Classe 4", "Classe 5")
        y_pos = np.arange(len(objects))
        performance = [
                        round(float(result[1L])*100,2),
                        round(float(result[2L])*100,2),
                        round(float(result[3L])*100,2),
                        round(float(result[4L])*100,2),
                        round(float(result[5L])*100,2)
                     ]

        plt.bar(y_pos, performance, align="center", alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel("%")
        plt.title("Probability distribution")
        plt.show()
       


    def editingFinished(self):
        sender = self.sender()
        allGood = [False,False,False,False,False]
        i = 0
        for edit in self.edits:
            value = edit.text()
            text = False
            if(value != ""):
                try:
                    value = int(value)
                except:
                    text = True
                if (text) or (value <= 0) or (value>5) and not (value == None) :
                    edit.setText("inserire valore compreso tra 1 e 5")
                else:
                    allGood[i] = True
            i += 1
        for el in allGood:
            if el == False:
                self.button.setEnabled(False)
                return
        self.button.setEnabled(True)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()