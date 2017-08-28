from subprocess import Popen
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import time
import sys

SLEEP_TIME = 5.0

def start_communication(IP_CRATE,tela_leds):


    print("Iniciando Comunicação com o Crate...")
    
    #position_AD=2*POSITION_CRATE-1
    
    ping_crate = Popen(['ping',str(IP_CRATE),'-c','1',"-W","2"])
    ping_crate.wait()
    ping_result = ping_crate.poll()
    if (ping_result==0):
        print("Comunicação com o CRATE: OK")
        tela_leds.ui.kled_CRATE.setState(1)
        tela_leds.ui.kled_CRATE.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led crate",tela_leds.repaint())
        print("Led crate",QApplication.processEvents())
    
    else:
        print("Comunicação com o CRATE: FAIL")
        print("Encerrando conexão")
        tela_leds.ui.kled_CRATE.setState(1)
        tela_leds.ui.kled_CRATE.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led crate",tela_leds.repaint())
        print("Led crate",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
        
    return()