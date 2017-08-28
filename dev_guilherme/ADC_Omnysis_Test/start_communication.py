from subprocess import Popen
"import matlab.engine"
import socket
from signal_generator_clock_connection import Signal_Generator_Clock
from signal_generator_input_connection import Signal_Generator_Input
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import time

SLEEP_TIME = 5.0

def start_communication(IP_CRATE,USERNAME,PASSWORD,POSITION_CRATE,IP_SWITCH,IP_GERADOR_SINAIS_CLOCK,IP_GERADOR_SINAIS_INPUT,tela_leds,utilizarMatlab_check):


    print("Iniciando Comunicação com o Crate...")
    
    #position_AD=2*POSITION_CRATE-1
    
    ping_crate = Popen(['ping',str(IP_CRATE),'-c','1',"-W","2"])
    ping_crate.wait()
    ping_result = ping_crate.poll()
    if (ping_result==0):
        crate_str_result_msg="CRATE - COMUNICAÇÃO: OK"
        crate_str_IP="CRATE - IP: "+str(IP_CRATE)
        print(crate_str_result_msg)
        tela_leds.ui.kled_crate.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led crate",tela_leds.repaint())
        print("Led crate",QApplication.processEvents())
    
    else:
        crate_str_result_msg="CRATE - COMUNICAÇÃO: FAIL"
        crate_str_IP="CRATE IP - "+str(IP_CRATE)
        print(crate_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_crate.setState(1)
        tela_leds.ui.kled_crate.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led crate",tela_leds.repaint())
        print("Led crate",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()

  
    print("Iniciar Conexão com o SWITCH")
    ping_switch = Popen(['ping',str(IP_SWITCH),'-c','1',"-W","2"])
    ping_switch.wait()
    ping_result = ping_switch.poll()
    if (ping_result==0):
        switch_str_result_msg="SWITCH - COMUNICAÇÃO: OK"
        switch_str_IP="SWITCH - IP: "+str(IP_SWITCH)
        print(switch_str_result_msg)
        tela_leds.ui.kled_switch.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch",tela_leds.repaint())
        print("Led switch",QApplication.processEvents())
        
    else:
        switch_str_result_msg="SWITCH - COMUNICAÇÃO: FAIL"
        switch_str_IP="SWITCH - IP: "+str(IP_SWITCH)
        print(switch_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_switch.setState(1)
        tela_leds.ui.kled_switch.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led switch",tela_leds.repaint())
        print("Led switch",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()

    print("Iniciar Conexão com o Gerador de Sinais - Input Signal")
    ping_sig_gen_input = Popen(['ping',str(IP_GERADOR_SINAIS_INPUT),'-c','1',"-W","2"])
    ping_sig_gen_input.wait()
    ping_result = ping_sig_gen_input.poll()
    if (ping_result==0):
        sig_gen_in_str_result_msg="GERADOR DE SINAIS INPUT - COMUNICAÇÃO: OK"
        sig_gen_in_str_IP="GERADOR DE SINAIS INPUT - IP: "+str(IP_GERADOR_SINAIS_INPUT)
        print(sig_gen_in_str_result_msg)
        tela_leds.ui.kled_ger_sin_in.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led Ger Sig In",tela_leds.repaint())
        print("Led Ger Sig In",QApplication.processEvents())
        sig_gen_input=Signal_Generator_Input(IP_GERADOR_SINAIS_INPUT)
        
    else:
        sig_gen_in_str_result_msg="GERADOR DE SINAIS INPUT - COMUNICAÇÃO: FAIL"
        sig_gen_in_str_IP="GERADOR DE SINAIS INPUT - IP: "+str(IP_GERADOR_SINAIS_INPUT)
        print(sig_gen_in_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_ger_sin_in.setState(1)
        tela_leds.ui.kled_ger_sin_in.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led Ger Sig In",tela_leds.repaint())
        print("Led Ger Sig In",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
           
    print("Iniciar Conexão com o Gerador de Sinais - Clock Signal")
    ping_sig_gen_clock = Popen(['ping',str(IP_GERADOR_SINAIS_CLOCK),'-c','1',"-W","2"])
    ping_sig_gen_clock.wait()
    ping_result = ping_sig_gen_clock.poll()
    if (ping_result==0):
        sig_gen_clock_str_result_msg="GERADOR DE SINAIS CLOCK - COMUNICAÇÃO: OK"
        sig_gen_clock_str_IP="GERADOR DE SINAIS CLOCK - IP: "+str(IP_GERADOR_SINAIS_CLOCK)
        print(sig_gen_clock_str_result_msg)
        tela_leds.ui.kled_ger_sin_clk.setState(1)
        tela_leds.repaint()
        QApplication.processEvents()
        sig_gen_clock=Signal_Generator_Clock(IP_GERADOR_SINAIS_CLOCK)
        print("Led Ger Sig Clk",tela_leds.repaint())
        print("Led Ger Sig Clk",QApplication.processEvents())
                
    else:
        sig_gen_clock_str_result_msg="GERADOR DE SINAIS CLOCK - COMUNICAÇÃO: FAIL"
        sig_gen_clock_str_IP="GERADOR DE SINAIS CLOCK - IP: "+str(IP_GERADOR_SINAIS_CLOCK)
        print(sig_gen_clock_str_result_msg)
        print("Encerrando conexão")
        tela_leds.ui.kled_ger_sin_clk.setState(1)
        tela_leds.ui.kled_ger_sin_clk.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led Ger Sig Clk",tela_leds.repaint())
        print("Led Ger Sig Clk",QApplication.processEvents())
        time.sleep(SLEEP_TIME)
        sys.exit()
    

    if(utilizarMatlab_check==True):
        print("Iniciar Conexão com Matlab")
        eng = matlab.engine.connect_matlab()
        matlab_str_result="MATLAB - CONEXÃO: OK"
        print(matlab_str_result)
    else:
        matlab_str_result="MATLAB - CONEXÃO: Opcao nao escolhidao"
        print(matlab_str_result)
        eng=0
    
    crate_str_result=[crate_str_result_msg,crate_str_IP]
    switch_str_result=[switch_str_result_msg,switch_str_IP]
    sig_gen_in_str_result=[sig_gen_in_str_result_msg,sig_gen_in_str_IP]
    sig_gen_clock_str_result=[sig_gen_clock_str_result_msg,sig_gen_clock_str_IP]
    
    #return (eng,ssh,sig_gen_clock,sig_gen_input)
    return (eng,sig_gen_clock,sig_gen_input,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result)