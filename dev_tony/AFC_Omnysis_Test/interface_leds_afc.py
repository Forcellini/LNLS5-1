# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_leds_afc.ui'
#
# Created: Thu Feb  9 15:45:24 2017
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(660, 476)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 30, 281, 131))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 20, 281, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.kled_CRATE = KLed(self.frame)
        self.kled_CRATE.setGeometry(QtCore.QRect(20, 50, 28, 28))
        self.kled_CRATE.setObjectName(_fromUtf8("kled_CRATE"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 58, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.kled_FPGA = KLed(self.frame)
        self.kled_FPGA.setGeometry(QtCore.QRect(20, 90, 28, 28))
        self.kled_FPGA.setObjectName(_fromUtf8("kled_FPGA"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(60, 90, 121, 31))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(20, 180, 281, 191))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(0, 20, 281, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.kled_EEPROM = KLed(self.frame_2)
        self.kled_EEPROM.setGeometry(QtCore.QRect(20, 60, 28, 28))
        self.kled_EEPROM.setObjectName(_fromUtf8("kled_EEPROM"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(60, 60, 58, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(60, 100, 58, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.kled_DDR3 = KLed(self.frame_2)
        self.kled_DDR3.setGeometry(QtCore.QRect(20, 100, 28, 28))
        self.kled_DDR3.setObjectName(_fromUtf8("kled_DDR3"))
        self.label_6 = QtGui.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(60, 140, 101, 31))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.kled_SENSORES_IPMI = KLed(self.frame_2)
        self.kled_SENSORES_IPMI.setGeometry(QtCore.QRect(20, 140, 28, 28))
        self.kled_SENSORES_IPMI.setObjectName(_fromUtf8("kled_SENSORES_IPMI"))
        self.frame_3 = QtGui.QFrame(Dialog)
        self.frame_3.setGeometry(QtCore.QRect(350, 60, 281, 281))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.label_7 = QtGui.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(0, 20, 281, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.kled_OK = KLed(self.frame_3)
        self.kled_OK.setGeometry(QtCore.QRect(20, 60, 28, 28))
        self.kled_OK.setObjectName(_fromUtf8("kled_OK"))
        self.label_8 = QtGui.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(60, 60, 58, 31))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_FALHOU = QtGui.QLabel(self.frame_3)
        self.label_FALHOU.setGeometry(QtCore.QRect(60, 100, 58, 31))
        self.label_FALHOU.setObjectName(_fromUtf8("label_FALHOU"))
        self.kled_FALHOU = KLed(self.frame_3)
        self.kled_FALHOU.setGeometry(QtCore.QRect(20, 100, 28, 28))
        self.kled_FALHOU.setColor(QtGui.QColor(255, 0, 0))
        self.kled_FALHOU.setObjectName(_fromUtf8("kled_FALHOU"))
        self.label_10 = QtGui.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(60, 140, 101, 31))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.kled_EXECUCAO = KLed(self.frame_3)
        self.kled_EXECUCAO.setGeometry(QtCore.QRect(20, 140, 28, 28))
        self.kled_EXECUCAO.setColor(QtGui.QColor(255, 255, 0))
        self.kled_EXECUCAO.setObjectName(_fromUtf8("kled_EXECUCAO"))
        self.kled_N_EXECUTADO = KLed(self.frame_3)
        self.kled_N_EXECUTADO.setGeometry(QtCore.QRect(20, 180, 28, 28))
        self.kled_N_EXECUTADO.setColor(QtGui.QColor(0, 0, 255))
        self.kled_N_EXECUTADO.setObjectName(_fromUtf8("kled_N_EXECUTADO"))
        self.label_11 = QtGui.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(60, 180, 141, 31))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.kled_N_AVALIADO = KLed(self.frame_3)
        self.kled_N_AVALIADO.setGeometry(QtCore.QRect(20, 220, 28, 28))
        self.kled_N_AVALIADO.setState(KLed.Off)
        self.kled_N_AVALIADO.setObjectName(_fromUtf8("kled_N_AVALIADO"))
        self.label_12 = QtGui.QLabel(self.frame_3)
        self.label_12.setGeometry(QtCore.QRect(60, 220, 171, 31))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(150, 420, 331, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.OK_BUTTON_LEDS = QtGui.QPushButton(Dialog)
        self.OK_BUTTON_LEDS.setGeometry(QtCore.QRect(530, 418, 87, 27))
        self.OK_BUTTON_LEDS.setObjectName(_fromUtf8("OK_BUTTON_LEDS"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Status", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">COMUNICAÇÃO</span></p></body></html>", None))
        self.label_2.setText(_translate("Dialog", "CRATE", None))
        self.label_9.setText(_translate("Dialog", "Gravação de FPGA", None))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">TESTES</span></p></body></html>", None))
        self.label_4.setText(_translate("Dialog", "EEPROM", None))
        self.label_5.setText(_translate("Dialog", "DDR3", None))
        self.label_6.setText(_translate("Dialog", "SENSORES IMPI", None))
        self.label_7.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">LEGENDA</span></p></body></html>", None))
        self.label_8.setText(_translate("Dialog", "OK", None))
        self.label_FALHOU.setText(_translate("Dialog", "Falhou", None))
        self.label_10.setText(_translate("Dialog", "Em execução", None))
        self.label_11.setText(_translate("Dialog", "Não será executado", None))
        self.label_12.setText(_translate("Dialog", "Status ainda não avaliado", None))
        self.OK_BUTTON_LEDS.setText(_translate("Dialog", "OK", None))

from PyKDE4.kdeui import KLed

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

