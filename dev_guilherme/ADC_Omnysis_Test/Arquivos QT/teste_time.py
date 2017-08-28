# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teste_time.ui'
#
# Created: Thu Jan 26 12:01:00 2017
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
        Dialog.resize(643, 413)
        self.dateTimeEdit = QtGui.QDateTimeEdit(Dialog)
        self.dateTimeEdit.setGeometry(QtCore.QRect(130, 80, 161, 26))
        self.dateTimeEdit.setAcceptDrops(False)
        self.dateTimeEdit.setFrame(False)
        self.dateTimeEdit.setCalendarPopup(False)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(60, 150, 113, 26))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(70, 250, 241, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

