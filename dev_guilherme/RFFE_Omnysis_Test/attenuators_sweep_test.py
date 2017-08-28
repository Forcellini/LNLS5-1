from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
from rffe_test_lib import Agilent33521A #necessário para enviar comandos para o sgen
from rffe_test_lib import RF_switch_board_1 #necessário para enviar comandos para o switch 1
from rffe_test_lib import RF_switch_board_2 #necessário para enviar comandos para o switch 2
from rffe_test_lib import RFFEControllerBoard #necessário para enviar comandos para o RFFE
import test_lib
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from leds_rf_switch import leds_rf_switch

def attenuators_sweep_test(vna,sgen,rffe,
                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                           center_freq, freq_span, 
                           pow_value, att_value,
                           att_sweep_low,att_sweep_high,att_step,att_step_tol,
                           tela_leds,percentual,attenuator_test_log):
    
    print("\nRunning attenuators sweep test - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2)+"... ")
    
    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra attenuator",tela_leds.repaint())
    print("barra attenuator",QApplication.processEvents())
        
    #Configuração Inicial de Segurança - Atenuador do RFFE no máximo, e VNA setado para pow_value dB
    rffe.set_attenuator_value(att_value)
    sgen.set_signal_DC()
    sgen.set_pos("direct")
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 
    test_lib.set_vna(0, center_freq, freq_span, 0, vna)
    rfsw_1.sw1_pos(ip_sw1,3,3) #coloca o switch 1 na chave 3-3 = 0dBm
    rfsw_2.sw2_pos(ip_sw2,0,0)
    leds_rf_switch(3, 3, 0, 0, tela_leds)
    #vna.send_command(b":SENSE1:AVER:COUN "+ format(10).encode('utf-8') + b"\n")
    vna.send_command(b":SENSE1:AVER OFF\n")
    
    #Variáveis do tipo lista que serão utilizadas
    s21_testA=[]
    step_sizeA=[]
    s21_testB=[]
    step_sizeB=[]
    nivel_attenuation_A=[]
    nivel_attenuation_B=[]
    
    #Data acquisition for channel 1-1 or 3-3
    print("\nRunning attenuators sweep test, Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1))

    rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
    leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)

    """Sets the attenuation value of both front-ends. The argument should be a
    floating-point number representing the attenuation (in dB) between 0 dB and 31.5 dB, with a
    0.5 dB step size. Argument values other than these will be disconsidered."""
    for att in range (int(att_sweep_low*2), int(att_sweep_high+1)*2, int(att_step*2)):
        rffe.set_attenuator_value(att/2)
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testA.append(round(s21,2))
        nivel_attenuation_A.append(att/2)
    
    fail=0

    #Tolerance 
    print("Upper Boundary: ", abs(att_step+att_step_tol))
    print("Lower Boundary: ", abs(att_step-att_step_tol))
    
    #Calculations of Channel 1-1 or 3-3      
    for i in range(0,len(s21_testA)-1):
        step_sizeA.append(round(s21_testA[i+1]-s21_testA[i],2))
        if abs(float(step_sizeA[i]))>abs(att_step+att_step_tol) or abs(float(step_sizeA[i]))<abs(att_step-att_step_tol):
            fail=1
    
    #Results of Channel 1-1 or 3-3
    if fail==1:
        att_sweep_resultA="Attenuator Sweep Test Result Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": FAILED"
        print("Result: ",step_sizeA)
        print("Result: Attenuator Sweep Test Result Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": FAILED")
        fail_A = 1
    else:
        att_sweep_resultA="Attenuator Sweep Test Result Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": OK"
        print("Result: ",step_sizeA)
        print("Result: Attenuator Sweep Test Result Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": OK")
        fail_A = 0
        
    fail=0
    
    tela_leds.ui.progressBar.setValue(25+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra rf switch",tela_leds.repaint())
    print("barra rf switch",QApplication.processEvents())

    #Data acquisition for Channel 2-2 or 4-4
    print("Running attenuators sweep test, Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
 
    rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
    leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)

    """Sets the attenuation value of both front-ends. The argument should be a
    floating-point number representing the attenuation (in dB) between 0 dB and 31.5 dB, with a
    0.5 dB step size. Argument values other than these will be disconsidered."""
    for att in range (int(att_sweep_low*2), int(att_sweep_high+1)*2, int(att_step*2)):
        rffe.set_attenuator_value(att/2)
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testB.append(round(s21,2))
        nivel_attenuation_B.append(att/2)
  
    #Calculations of Channel 2-2 or 4-4
    for i in range(0,len(s21_testB)-1):
        step_sizeB.append(round(s21_testB[i+1]-s21_testB[i],2))
        print(step_sizeB[i])
        if abs(float(step_sizeB[i]))>abs(att_step+att_step_tol) or abs(float(step_sizeB[i]))<abs(att_step-att_step_tol):
            fail=1
    
    #Results of Channel 2-2 or 4-4
    if fail==1:
        att_sweep_resultB="Attenuator Sweep Test Result Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": FAILED"
        print("Result: ",step_sizeB)
        print("Result: Attenuator Sweep Test Result Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": FAILED")
        fail_B = 1
    else:
        att_sweep_resultB="Attenuator Sweep Test Result Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": OK"
        print("Result: ",step_sizeB)
        print("Result: Attenuator Sweep Test Result Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": OK")
        fail_B = 0
    
    tela_leds.ui.progressBar.setValue(50+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra rf switch",tela_leds.repaint())
    print("barra rf switch",QApplication.processEvents())
    
    #LOG INFO
    espacamento=25
    attenuator_test_log.append("Attenuators sweep test - RFFE Channel: "+str(sw2_port_1)+" - "+str(sw2_port_1))
    attenuator_test_log.append("RFFE Attenuation [dB]".ljust(espacamento)+"Result Values [dB]".ljust(espacamento))
    for i in range (0, len(step_sizeA)):
        step_sizeA[i]=abs(step_sizeA[i])
        attenuator_test_log.append(str(nivel_attenuation_A[i]).ljust(espacamento)
                                   +str(step_sizeA[i]).ljust(espacamento))
    attenuator_test_log.append(att_sweep_resultA+"\n")
    attenuator_test_log.append("Attenuators sweep test - RFFE Channel: "+str(sw2_port_2)+" - "+str(sw2_port_2))
    attenuator_test_log.append("RFFE Attenuation [dB]".ljust(espacamento)+"Result Values [dB]".ljust(espacamento))
    for i in range (0, len(step_sizeB)):
        step_sizeB[i]=abs(step_sizeB[i])
        attenuator_test_log.append(str(nivel_attenuation_B[i]).ljust(espacamento)
                                   +str(step_sizeB[i]).ljust(espacamento))
    attenuator_test_log.append(att_sweep_resultB+"\n")
    
    return (att_sweep_resultA,step_sizeA,att_sweep_resultB,step_sizeB,fail_A,fail_B,attenuator_test_log)