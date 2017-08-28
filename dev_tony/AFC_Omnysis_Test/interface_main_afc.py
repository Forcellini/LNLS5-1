# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_main_afc.ui'
#
# Created: Fri Feb 24 06:49:45 2017
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
        MainWindow.resize(691, 457)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.INICIAR_TESTE_BUTTON = QtGui.QPushButton(self.centralwidget)
        self.INICIAR_TESTE_BUTTON.setGeometry(QtCore.QRect(470, 390, 87, 27))
        self.INICIAR_TESTE_BUTTON.setObjectName(_fromUtf8("INICIAR_TESTE_BUTTON"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 61))
        self.label.setObjectName(_fromUtf8("label"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 100, 291, 111))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(0, 20, 291, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.splitter = QtGui.QSplitter(self.frame)
        self.splitter.setGeometry(QtCore.QRect(50, 60, 202, 26))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.label_2 = QtGui.QLabel(self.splitter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.IP_CRATE = QtGui.QLineEdit(self.splitter)
        self.IP_CRATE.setObjectName(_fromUtf8("IP_CRATE"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(40, 230, 291, 191))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(0, 20, 291, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.CHECK_EEPROM = QtGui.QRadioButton(self.frame_2)
        self.CHECK_EEPROM.setGeometry(QtCore.QRect(30, 60, 104, 20))
        self.CHECK_EEPROM.setAutoExclusive(False)
        self.CHECK_EEPROM.setObjectName(_fromUtf8("CHECK_EEPROM"))
        self.CHECK_DDR3 = QtGui.QRadioButton(self.frame_2)
        self.CHECK_DDR3.setGeometry(QtCore.QRect(30, 90, 104, 20))
        self.CHECK_DDR3.setAutoExclusive(False)
        self.CHECK_DDR3.setObjectName(_fromUtf8("CHECK_DDR3"))
        self.CHECK_SENSORES_IPMI = QtGui.QRadioButton(self.frame_2)
        self.CHECK_SENSORES_IPMI.setGeometry(QtCore.QRect(30, 120, 131, 20))
        self.CHECK_SENSORES_IPMI.setAutoExclusive(False)
        self.CHECK_SENSORES_IPMI.setObjectName(_fromUtf8("CHECK_SENSORES_IPMI"))
        self.CHECK_TODOS = QtGui.QRadioButton(self.frame_2)
        self.CHECK_TODOS.setGeometry(QtCore.QRect(100, 150, 104, 20))
        self.CHECK_TODOS.setAutoExclusive(False)
        self.CHECK_TODOS.setObjectName(_fromUtf8("CHECK_TODOS"))
        self.dateTimeEdit = QtGui.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(290, 30, 151, 26))
        self.dateTimeEdit.setFrame(True)
        self.dateTimeEdit.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(360, 100, 301, 111))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(0, 10, 291, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.checkBox_FPGA = QtGui.QCheckBox(self.frame_3)
        self.checkBox_FPGA.setGeometry(QtCore.QRect(30, 60, 111, 20))
        self.checkBox_FPGA.setObjectName(_fromUtf8("checkBox_FPGA"))
        self.CLOSE_BUTTON = QtGui.QPushButton(self.centralwidget)
        self.CLOSE_BUTTON.setGeometry(QtCore.QRect(570, 390, 87, 27))
        self.CLOSE_BUTTON.setObjectName(_fromUtf8("CLOSE_BUTTON"))
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(370, 230, 291, 131))
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.label_8 = QtGui.QLabel(self.frame_4)
        self.label_8.setGeometry(QtCore.QRect(0, 20, 291, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.splitter_3 = QtGui.QSplitter(self.frame_4)
        self.splitter_3.setGeometry(QtCore.QRect(50, 60, 202, 26))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.label_9 = QtGui.QLabel(self.splitter_3)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.OPERADOR = QtGui.QLineEdit(self.splitter_3)
        self.OPERADOR.setObjectName(_fromUtf8("OPERADOR"))
        self.N_SERIE_AFC = QtGui.QLineEdit(self.frame_4)
        self.N_SERIE_AFC.setGeometry(QtCore.QRect(129, 90, 123, 26))
        self.N_SERIE_AFC.setObjectName(_fromUtf8("N_SERIE_AFC"))
        self.label_10 = QtGui.QLabel(self.frame_4)
        self.label_10.setGeometry(QtCore.QRect(42, 90, 81, 26))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Teste da AFC", None))
        self.INICIAR_TESTE_BUTTON.setText(_translate("MainWindow", "Iniciar Teste", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>Selecione os testes desejados. </p><p>Após isso, clique em INICIAR TESTE.</p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">PARÂMETROS DE COMUNICAÇÃO</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "IP do CRATE", None))
        self.IP_CRATE.setText(_translate("MainWindow", "10.0.18.14", None))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">TESTES A SEREM REALIZADOS</span></p></body></html>", None))
        self.CHECK_EEPROM.setText(_translate("MainWindow", "EEPROM", None))
        self.CHECK_DDR3.setText(_translate("MainWindow", "DDR3", None))
        self.CHECK_SENSORES_IPMI.setText(_translate("MainWindow", "SENSORES IPMI", None))
        self.CHECK_TODOS.setText(_translate("MainWindow", "TODOS", None))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">FPGA</span></p></body></html>", None))
        self.checkBox_FPGA.setText(_translate("MainWindow", "Gravar FPGA", None))
        self.CLOSE_BUTTON.setText(_translate("MainWindow", "Fechar", None))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">INFORMAÇÕES GERAIS</span></p></body></html>", None))
        self.label_9.setText(_translate("MainWindow", "Operador", None))
        self.OPERADOR.setText(_translate("MainWindow", "Fernando", None))
        self.N_SERIE_AFC.setText(_translate("MainWindow", "1111111", None))
        self.label_10.setText(_translate("MainWindow", "N. Série AFC", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

