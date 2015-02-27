# -*- coding: utf-8 -*-

import sys
import os
from matplotlib.backends import qt4_compat
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import numpy as np

# bibli perso
import interface.fctInterface as gui
import datetime as dt
import Utilities.calcul as ut

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName(_fromUtf8("GroupBox"))
        GroupBox.resize(661, 532)
        GroupBox.setFixedSize(GroupBox.size())
        
        # QWidget
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        self.widget = QtGui.QWidget(GroupBox)
        self.widget.setGeometry(QtCore.QRect(-1, 99, 661, 431))
        self.widget.setAutoFillBackground(True)
        self.widget.setObjectName(_fromUtf8("widget"))
        
        self.layout = QtGui.QVBoxLayout(self.widget)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.widget, coordinates = False)

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.mpl_toolbar)
        rect = 0,0.05,1,0.9
        self.axes = self.fig.add_axes(rect)
        self.widget.setLayout(self.layout)

        # Choix filtrage date
        self.dateTimeEditStart = QtGui.QDateTimeEdit(GroupBox)
        self.dateTimeEditStart.setGeometry(QtCore.QRect(210, 20, 191, 24))
        self.dateTimeEditStart.setObjectName(_fromUtf8("dateTimeEditStart"))
        self.dateTimeEditEnd = QtGui.QDateTimeEdit(GroupBox)
        self.dateTimeEditEnd.setGeometry(QtCore.QRect(210, 70, 191, 24))
        self.dateTimeEditEnd.setObjectName(_fromUtf8("dateTimeEditEnd"))

        # choix filtre
        self.comboBox = QtGui.QComboBox(GroupBox)
        self.comboBox.setGeometry(QtCore.QRect(470, 20, 141, 26))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))

        self.comboBox.insertItem(0,"Epanechnikov")
        self.comboBox.insertItem(1,"Gaussian")
        self.comboBox.insertItem(2,"Kalman")

        # file button
        self.fileButton = QtGui.QPushButton(GroupBox)
        self.fileButton.setGeometry(QtCore.QRect(0, 20, 115, 32))
        self.fileButton.setObjectName(_fromUtf8("fileButton"))

        def buttonFct():    # choix fichiers, récup liste et id + mise en place date min et max
            path = QtGui.QFileDialog.getOpenFileNames(None, "Choix un ou plusieurs fichiers", "", "(*.DIAG *.DS *.CSV)")

            if path != []:

                self.listId = []
                self.listList = []
                self.dateMin = []
                self.dateMax = []

                # recuperation des listes et des identifiants
                for i in xrange(len(path)):
                    tmp = []
                    tmp, identifiant = gui.lectureListesEtId(path[i])
                    self.dateMin.append(ut.convertDateToSecond(tmp[0]["date"]))
                    self.dateMax.append(ut.convertDateToSecond(tmp[-1]["date"]))
                    self.listList.append(tmp)
                    self.listId.append(identifiant)

                # conversion et mise en place dans gui
                tmpMin = ut.convertSecondToDatetime(min(self.dateMin))
                tmpMax = ut.convertSecondToDatetime(max(self.dateMax))
                self.QDateMin = QtCore.QDateTime(tmpMin["annee"], tmpMin["mois"], tmpMin["jour"], tmpMin["heure"], tmpMin["min"], tmpMin["sec"])
                self.QDateMax = QtCore.QDateTime(tmpMax["annee"], tmpMax["mois"], tmpMax["jour"], tmpMax["heure"], tmpMax["min"], tmpMax["sec"])
                self.dateTimeEditStart.setDateTimeRange(self.QDateMin, self.QDateMax) 
                self.dateTimeEditEnd.setDateTimeRange(self.QDateMin, self.QDateMax)
                self.dateTimeEditStart.setDateTime(self.QDateMin)
                self.dateTimeEditEnd.setDateTime(self.QDateMax) 

        self.fileButton.clicked.connect(buttonFct)

        # Save button        
        self.saveButton = QtGui.QPushButton(GroupBox)
        self.saveButton.setGeometry(QtCore.QRect(0, 70, 115, 32))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        
        def sauvegarder():
            # servira à creer les .res (fonction à mettre dans fctInterface.py)
            gui.saveRes(self.listId, self.listLongitudes, self.listLatitudes, self.listTemps)

        self.saveButton.clicked.connect(sauvegarder)

        # labels
        self.labelEnd = QtGui.QLabel(GroupBox)
        self.labelEnd.setGeometry(QtCore.QRect(170, 70, 59, 16))
        self.labelEnd.setObjectName(_fromUtf8("labelEnd"))
        self.labelStart = QtGui.QLabel(GroupBox)
        self.labelStart.setGeometry(QtCore.QRect(150, 20, 59, 16))
        self.labelStart.setAlignment(QtCore.Qt.AlignCenter)
        self.labelStart.setObjectName(_fromUtf8("labelStart"))
        
        # go button
        self.goButton = QtGui.QPushButton(GroupBox)
        self.goButton.setGeometry(QtCore.QRect(480, 60, 115, 32))
        self.goButton.setObjectName(_fromUtf8("goButton"))

        self.dejaVu = 0

        def gogoGadgeto():
            # lancera le tracé

            # données pour filtrage par date
            start = self.dateTimeEditStart.dateTime().toPyDateTime()
            end = self.dateTimeEditEnd.dateTime().toPyDateTime()
            ref = dt.datetime(2000, 1, 1, 0, 0, 0)

            if self.QDateMin.toPyDateTime() == start:
                startSecond = 0.0
            else:
                startSecond = (start - ref).total_seconds()

            if self.QDateMax.toPyDateTime() == end:
                endSecond = 0.0
            else:
                endSecond = (end - ref).total_seconds()

            # init
            self.listLatitudes = []
            self.listLongitudes = []
            self.listTemps = []

            for i in range(len(self.listList)):
                lats, lons, temps = gui.toutEnUn(self.listList[i], startSecond, endSecond, self.comboBox.currentIndex())
                self.listLatitudes.append(lats)
                self.listLongitudes.append(lons)
                self.listTemps.append(temps)

            if self.dejaVu == 0:
                monLon = sum(self.listLongitudes[0])/len(self.listLongitudes[0])
                monLat = sum(self.listLatitudes[0])/len(self.listLatitudes[0])
                self.dejaVu = 1

                # Mise en place de la carte au premier passage/clic sur "file(s)"
                self.m = Basemap(width=12000000,height=9000000,projection='lcc', lat_0=monLat, lon_0=monLon, resolution='c', ax=self.axes)
                self.m.drawcoastlines()
                #self.m.drawmapboundary(fill_color='aqua')
                self.m.fillcontinents(color='coral',lake_color='aqua')

                self.m.drawmeridians(np.arange(10,351,30), labels=[0,1,1,0])
                self.m.drawparallels(np.arange(0,90,10), labels=[1,0,0,1])

            for i in range(len(self.listLatitudes)):
                x,y = self.m(self.listLongitudes[i],self.listLatitudes[i])
                self.m.plot(x,y,'-')

            self.canvas.draw()

        self.goButton.clicked.connect(gogoGadgeto)

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox", None))
        GroupBox.setTitle(_translate("GroupBox", "GroupBox", None))
        self.fileButton.setText(_translate("GroupBox", "File(s)", None))
        self.saveButton.setText(_translate("GroupBox", "Save", None))
        self.labelEnd.setText(_translate("GroupBox", "End", None))
        self.labelStart.setText(_translate("GroupBox", "Start", None))
        self.goButton.setText(_translate("GroupBox", "Go", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GroupBox = QtGui.QGroupBox()
    ui = Ui_GroupBox()
    ui.setupUi(GroupBox)
    GroupBox.show()
    sys.exit(app.exec_())

