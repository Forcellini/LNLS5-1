from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QDateTime,QTimer
from subprocess import Popen,PIPE
import interfaceloopback
import sys


#PRIMEIRA JANELA
class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = interfaceloopback.Ui_MainWindow() 
        self.ui.setupUi(self) 
        #Ação dos botões
        ''' self.ui.BotaoEND.clicked.connect(self.BotaoEND)'''
        self.ui.BotaoGTP.clicked.connect(self.BotaoGTP)
        self.ui.BotaoRTM.clicked.connect(self.BotaoRTM)

        

        ''' def BotaoEND(self):
        print("End")'''
    
    def BotaoGTP(self):
        print("Teste GTP")
        comando2 = "/opt/Xilinx/Vivado/2016.2/bin/vivado -source /home/tadeu/workspace/AFC_Loopback/GTP.tcl"

        command_stdout = Popen(comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()


        
    def BotaoRTM(self):
        print("Teste RTM")
        comando2 = "/opt/Xilinx/Vivado/2016.2/bin/vivado -source /home/tadeu/workspace/AFC_Loopback/RTM_IO.tcl"
        command_stdout1 = Popen(comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout1=command_stdout1.splitlines()
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())