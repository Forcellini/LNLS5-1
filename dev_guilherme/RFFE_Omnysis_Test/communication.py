from rffe_test_lib import Agilent33521A
from rffe_test_lib import RFFEControllerBoard
from rffe_test_lib import AgilentE5061B
from rffe_test_lib import RF_switch_board_1
from rffe_test_lib import RF_switch_board_2

from subprocess import Popen

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

import time
import sys

SLEEP_TIME = 5.0

def communication(ip_network_analyzer,ip_switch_1,ip_switch_2,ip_rffe,ip_gerador_sinais_dc,
                  tela_leds):
    
    
    #Verificando a comunicação com o RFFE
    ping = Popen(['ping',str(ip_rffe),'-c','1',"-W","2"])
    ping.wait()
    ping_result = ping.poll()
    if (ping_result==0):
        rffe_str_result_msg="RFFE - Communication: OK"
        rffe_str_IP="RFFE - IP: "+str(ip_rffe)
        print(rffe_str_result_msg)
        tela_leds.ui.kled_RFFE.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led rffe",tela_leds.repaint())
        print("Led rffe",QApplication.processEvents())
    
    else:
        rffe_str_result_msg="RFFE - Communication: FAIL"
        rffe_str_IP="RFFE - IP: "+str(ip_rffe)
        print(rffe_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_RFFE.setState(1)
        tela_leds.ui.kled_RFFE.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led rffe",tela_leds.repaint())
        print("Led rffe",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
    
    rffe=RFFEControllerBoard(ip_rffe)
    rffe_str_msg_communication=[rffe_str_IP,rffe_str_result_msg]
      
    #Verificando a comunicação com o Network Analyzer
    ping = Popen(['ping',str(ip_network_analyzer),'-c','1',"-W","2"])
    ping.wait()
    ping_result = ping.poll()
    if (ping_result==0):
        network_str_result_msg="Network Analyzer - Communication: OK"
        network_str_IP="Network Analyzer - IP: "+str(ip_network_analyzer)
        print(network_str_result_msg)
        tela_leds.ui.kled_NETWORK.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led network",tela_leds.repaint())
        print("Led network",QApplication.processEvents())
    
    else:
        network_str_result_msg="Network Analyzer - Communication: FAIL"
        network_str_IP="Network Analyzer - IP: "+str(ip_network_analyzer)
        print(network_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_NETWORK.setState(1)
        tela_leds.ui.kled_NETWORK.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led network",tela_leds.repaint())
        print("Led network",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
    
    vna=AgilentE5061B(ip_network_analyzer)
    vna_str_msg_communication=[network_str_IP,network_str_result_msg]
    
    
    #Verificando a comunicação com o SWITCH 1
    ping = Popen(['ping',str(ip_switch_1),'-c','1',"-W","2"])
    ping.wait()
    ping_result = ping.poll()
    if (ping_result==0):
        switch_1_str_result_msg="RF Switch1 - Communication: OK"
        switch_1_str_IP="RF Switch1 - IP: "+str(ip_switch_1)
        print(switch_1_str_result_msg)
        tela_leds.ui.kled_SWITCH1.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch1",tela_leds.repaint())
        print("Led switch1",QApplication.processEvents())
    
    else:
        switch_1_str_result_msg="RF Switch1 - Communication: FAIL"
        switch_1_str_IP="RF Switch1 - IP: "+str(ip_switch_1)
        print(switch_1_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_SWITCH1.setState(1)
        tela_leds.ui.kled_SWITCH1.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch1",tela_leds.repaint())
        print("Led switch1",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
    
    rfsw_1=RF_switch_board_1(ip_switch_1)
    rfsw_1_str_msg_communication=[switch_1_str_IP,switch_1_str_result_msg]
    
    
    #Verificando a comunicação com o SWITCH 2
    ping = Popen(['ping',str(ip_switch_2),'-c','1',"-W","2"])
    ping.wait()
    ping_result = ping.poll()
    if (ping_result==0):
        switch_2_str_result_msg="RF Switch2 - Communication: OK"
        switch_2_str_IP="RF Switch2 - IP: "+str(ip_switch_2)
        print(switch_2_str_result_msg)
        tela_leds.ui.kled_SWITCH2.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch2",tela_leds.repaint())
        print("Led switch2",QApplication.processEvents())
    
    else:
        switch_2_str_result_msg="RF Switch2 - Communication: FAIL"
        switch_2_str_IP="RF Switch2 - IP: "+str(ip_switch_2)
        print(switch_2_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_SWITCH2.setState(1)
        tela_leds.ui.kled_SWITCH2.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch2",tela_leds.repaint())
        print("Led switch2",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
    
    rfsw_2=RF_switch_board_2(ip_switch_2)
    rfsw_2_str_msg_communication=[switch_2_str_IP,switch_2_str_result_msg]

    #Verificando a comunicação com o WAVEFORM GENERATOR
    ping = Popen(['ping',str(ip_gerador_sinais_dc),'-c','1',"-W","2"])
    ping.wait()
    ping_result = ping.poll()
    if (ping_result==0):
        waveform_generator_str_result_msg="Waveform Generator - Communication: OK"
        waveform_generator_str_IP="Waveform Generator - IP: "+str(ip_gerador_sinais_dc)
        print(waveform_generator_str_result_msg)
        tela_leds.ui.kled_WAVEFORM.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch2",tela_leds.repaint())
        print("Led switch2",QApplication.processEvents())
    
    else:
        waveform_generator_str_result_msg="Waveform Generator - Communication: FAIL"
        waveform_generator_str_IP="Waveform Generator - IP: "+str(ip_gerador_sinais_dc)
        print(waveform_generator_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_WAVEFORM.setState(1)
        tela_leds.ui.kled_WAVEFORM.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led waveform",tela_leds.repaint())
        print("Led waveform",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
    
    sgen=Agilent33521A(ip_gerador_sinais_dc)
    sgen_str_msg_communication=[waveform_generator_str_IP,waveform_generator_str_result_msg]
    
    print("Network/LAN configuration - ok!\n...\n")
    
    return(vna,rfsw_1,rfsw_2,rffe,sgen,
           rffe_str_msg_communication,vna_str_msg_communication,rfsw_1_str_msg_communication,rfsw_2_str_msg_communication,sgen_str_msg_communication)