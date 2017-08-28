# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaceloopback.ui'
#
# Created: Fri May 12 13:15:14 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(444, 209)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.BotaoGTP = QtGui.QPushButton(self.centralwidget)
        self.BotaoGTP.setGeometry(QtCore.QRect(30, 60, 161, 51))
        self.BotaoGTP.setObjectName(_fromUtf8("BotaoGTP"))
        self.BotaoRTM = QtGui.QPushButton(self.centralwidget)
        self.BotaoRTM.setGeometry(QtCore.QRect(250, 60, 161, 51))
        self.BotaoRTM.setObjectName(_fromUtf8("BotaoRTM"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 444, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuLoopback = QtGui.QMenu(self.menubar)
        self.menuLoopback.setObjectName(_fromUtf8("menuLoopback"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuLoopback.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.BotaoGTP.setText(_translate("MainWindow", "TESTE DE PINOS DE\n"
" ALTA VELOCIDADE", None))
        self.BotaoRTM.setText(_translate("MainWindow", "TESTE DE PINOS RTM", None))
        self.menuLoopback.setTitle(_translate("MainWindow", "Loopback", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

