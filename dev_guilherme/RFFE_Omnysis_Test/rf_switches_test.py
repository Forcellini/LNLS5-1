from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
from rffe_test_lib import Agilent33521A #necessário para enviar comandos para o sgen
from rffe_test_lib import RF_switch_board_1 #necessário para enviar comandos para o switch 1
from rffe_test_lib import RF_switch_board_2 #necessário para enviar comandos para o switch 2
from rffe_test_lib import RFFEControllerBoard #necessário para enviar comandos para o RFFE
import test_lib
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from leds_rf_switch import leds_rf_switch



def rf_switches_test(vna,sgen,rffe,
                     rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                     rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                     center_freq, freq_span, 
                     pow_value, att_value,
                     switch_ref,switch_tol,tela_leds,percentual,rf_switch_test_log,
                     s_parameter_test_selection,
                     s_parameter_data_chA,s_parameter_data_chB,
                     freq_central_position):
    
    print("\nRunning RF switches test - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2)+"\n")

    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra rf switch",tela_leds.repaint())
    print("barra rf switch",QApplication.processEvents())
            
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
    
    #Data Acquisition
    if (s_parameter_test_selection==True):
        #Neste teste utilizamos o parâmetro S21 com medição na freq central
        #s_parameter_data_chA=[s11,s12,s21,s22]
       
        #Canal A: 1-1 ou 3-3
        #Canal B: 2-2 ou 4-4
        print("Using S-Parameters data for direct position")
        #Nível DC: ALTO
        data_chA_ctr_freq_direct=s_parameter_data_chA[2][freq_central_position]
        data_chB_ctr_freq_direct=s_parameter_data_chB[2][freq_central_position]
        #Atualiza barra de progresso
        tela_leds.ui.progressBar.setValue(25+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra rf switch",tela_leds.repaint())
        print("barra rf switch",QApplication.processEvents())

        #Nível DC: BAIXO
        sgen.set_pos("inverted")
        
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        s21_test=float(test_lib.marker_value(0,center_freq, "s21", vna))
        data_chA_ctr_freq_inverted= s21_test

        print("Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        s21_test=float(test_lib.marker_value(0,center_freq, "s21", vna))
        data_chB_ctr_freq_inverted=s21_test
        #Atualiza barra de progresso
        tela_leds.ui.progressBar.setValue(50+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra rf switch",tela_leds.repaint())
        print("barra rf switch",QApplication.processEvents())

    else:
        print("Acquiring data...")
        #Canal A (1-1 ou 3-3)
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        #NÍVEL DC: ALTO
        sgen.set_pos("direct")
        s21_test=float(test_lib.marker_value(0,center_freq, "s21", vna))
        data_chA_ctr_freq_direct= s21_test
        #Nível DC: BAIXO
        sgen.set_pos("inverted")
        s21_test=float(test_lib.marker_value(0,center_freq, "s21", vna))
        data_chA_ctr_freq_inverted= s21_test
        #Atualiza barra de progresso
        tela_leds.ui.progressBar.setValue(25+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra rf switch",tela_leds.repaint())
        print("barra rf switch",QApplication.processEvents())
        
        
        #Canal B (2-2 ou 4-4)
        print("Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        #Nível DC: ALTO
        sgen.set_pos("direct")
        s21_test=float(test_lib.marker_value(0,center_freq, "s21", vna))
        data_chB_ctr_freq_direct=s21_test
        #Nível DC: BAIXO
        sgen.set_pos("inverted")
        s21_test=float(test_lib.marker_value(0,center_freq, "s21", vna))
        data_chB_ctr_freq_inverted=s21_test
        #Atualiza barra de progresso
        tela_leds.ui.progressBar.setValue(50+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra rf switch",tela_leds.repaint())
        print("barra rf switch",QApplication.processEvents())
        
    #Tolerance
    print("Lower Boundary: ", abs(switch_ref+switch_tol))
     
    #Calculations and Results of Channel A (1-1 ou 3-3) 
    rf_sw_result_valuesA = abs(round((abs(float(data_chA_ctr_freq_direct)-float(data_chA_ctr_freq_inverted))),2))
    if rf_sw_result_valuesA<abs(switch_ref+switch_tol):
        rf_sw_resultA="RF Switches Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": FAILED"
        print("Result: ", rf_sw_result_valuesA)
        print("RF Switches Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": FAILED")
        rf_sw_fail_A=1

    else:
        rf_sw_resultA="RF Switches Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": OK"
        print("Result: ", rf_sw_result_valuesA)
        print("RF Switches Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+ ": OK")
        rf_sw_fail_A=0

    #Calculations and Results of Channel B (2-2 ou 4-4)
    rf_sw_result_valuesB = abs(round((abs(float(data_chB_ctr_freq_direct)-float(data_chB_ctr_freq_inverted))),2))
    if rf_sw_result_valuesB<abs(switch_ref+switch_tol):
        rf_sw_resultB="RF Switches Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+ ": FAILED"
        print("Result: ", rf_sw_result_valuesB)
        print("RF Switches Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+ ": FAILED")
        rf_sw_fail_B=1

    else:
        rf_sw_resultB="RF Switches Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+ ": OK"
        print("Result: ", rf_sw_result_valuesB)
        print("RF Switches Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+ ": OK")
        rf_sw_fail_B=0

    #LOG INFO
    rf_switch_test_log.append("Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1))
    rf_switch_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
    rf_switch_test_log.append("Measurement [dB]:"+str(round(data_chA_ctr_freq_direct,2)))
    rf_switch_test_log.append("Waveform Generator - DC Offset [V]: "+str(0.0))
    rf_switch_test_log.append("Measurement [dB]:"+str(round(data_chA_ctr_freq_inverted,2)))
    rf_switch_test_log.append("Result Value [dB]:"+str(rf_sw_result_valuesA))
    rf_switch_test_log.append(rf_sw_resultA+"\n")
    
    rf_switch_test_log.append("Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
    rf_switch_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
    rf_switch_test_log.append("Measurement [dB]:"+str(round(data_chB_ctr_freq_direct,2)))
    rf_switch_test_log.append("Waveform Generator - DC Offset [V]: "+str(0.0))
    rf_switch_test_log.append("Measurement [dB]:"+str(round(data_chB_ctr_freq_inverted,2)))
    rf_switch_test_log.append("Result Value [dB]:"+str(rf_sw_result_valuesB))
    rf_switch_test_log.append(rf_sw_resultB+"\n")
    
    #volta a condição original por segurança
    sgen.set_pos("direct")  
    
    return (rf_sw_resultA,rf_sw_result_valuesA,rf_sw_resultB,rf_sw_result_valuesB,
            rf_switch_test_log,rf_sw_fail_A, rf_sw_fail_B)