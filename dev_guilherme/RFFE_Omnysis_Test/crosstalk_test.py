from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
from rffe_test_lib import Agilent33521A #necessário para enviar comandos para o sgen
from rffe_test_lib import RF_switch_board_1 #necessário para enviar comandos para o switch 1
from rffe_test_lib import RF_switch_board_2 #necessário para enviar comandos para o switch 2
from rffe_test_lib import RFFEControllerBoard #necessário para enviar comandos para o RFFE
import test_lib

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from leds_rf_switch import leds_rf_switch

def crosstalk_test(vna,sgen,rffe,
                   rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                   rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                   center_freq, freq_span, 
                   pow_value, att_value,
                   xtalk_ref,xtalk_tol_ref,
                   start_bandwidth,stop_bandwidth,
                   crosstalk_test_log,percentual,tela_leds,
                   s_parameter_test_selection,
                   s_parameter_data_chAA,s_parameter_data_chBB,
                   s_parameter_data_chAB,s_parameter_data_chBA,
                   freq_data):


    print("Running Crosstalk test - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2))

    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra xtalk",tela_leds.repaint())
    print("barra xtalk",QApplication.processEvents())  
    
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
    




    #Variables
    data_chAA_filter=[]
    data_chBB_filter=[]

    data_chAB_filter=[]
    data_chBA_filter=[]
        
    #Data Acquisition
    if(s_parameter_test_selection==True):
        
        print("Utilizando os dados adquiridos no teste do S-Parameters")
        #Neste teste utilizamos o parâmetro S21 
        #s_parameter_data_chA=[s11,s12,s21,s22]
        data_chAB=s_parameter_data_chAB[2]
        data_chBA=s_parameter_data_chBA[2]
                
        #start_bandwidth_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>=start_bandwidth):
                start_bandwidth_position=i
                break
        print("Frquencia Detectada: ",freq_data[start_bandwidth_position],"Frequencia Esperada: ",start_bandwidth)
            
        #stop_bandwith_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>stop_bandwidth):
                stop_bandwidth_position=i-1
                break   
        print("Frequencia Detectada:",freq_data[stop_bandwidth_position],"Frequencia Esperada: ",stop_bandwidth) 
        
        for i in range (start_bandwidth_position,stop_bandwidth_position):
            data_chAB_filter.append(data_chAB[i])
            data_chBA_filter.append(data_chBA[i])   
                     
        print("Aquisição de dados completa...")
        
        tela_leds.ui.progressBar.setValue(45+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra xtalk",tela_leds.repaint())
        print("barra xtalk",QApplication.processEvents())    
    else:
        
        print("Aquisição de dados necessária...Iniciando aquisição...")
       
        #Data acquisition for channel A 1-2 or 3-4
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_2, tela_leds)
        data_chAB=vna.get_s21_data()
        
        #Data acquisition for channel B 2-1 or 4-3
        print("Channel "+str(sw2_port_2)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_1, tela_leds)
        data_chBA=vna.get_s21_data()
        
        #Data acquisition for channel A 1-1 or 3-3
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        s_parameter_data_chAA=vna.get_s21_data()
        
        #Data acquisition for channel B 2-2 or 4-4
        print("Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        s_parameter_data_chBB=vna.get_s21_data()
        
        
        
        
        
        
        #start_bandwidth_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>=start_bandwidth):
                start_bandwidth_position=i
                break
        print("Frquencia Detectada: ",freq_data[start_bandwidth_position],"Frequencia Esperada: ",start_bandwidth)
            
        #stop_bandwith_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>stop_bandwidth):
                stop_bandwidth_position=i-1
                break   
        print("Frequencia Detectada:",freq_data[stop_bandwidth_position],"Frequencia Esperada: ",stop_bandwidth) 
        
        for i in range (start_bandwidth_position,stop_bandwidth_position):
            data_chAB_filter.append(data_chAB[i])
            data_chBA_filter.append(data_chBA[i])  
            
        print("Aquisição de dados completa...")       
        
        tela_leds.ui.progressBar.setValue(45+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra xtalk",tela_leds.repaint())
        print("barra xtalk",QApplication.processEvents())  
    
    #Tolerance
    print("Lower Boundary: ",xtalk_ref+xtalk_tol_ref)
        
    #Calculations and Results of Channel A: 1-2 or 3-4  
    #Determinar a maior amplitude, e a menor amplitude para comparação:
    maximum_valueAB= -1000
    minimum_valueAB=  1000
    
    for i in range (0,len(data_chAB_filter)):
        if(data_chAB_filter[i]>maximum_valueAB):
            maximum_valueAB=data_chAB_filter[i]
            freq_maximum_position_AB=i
        if(data_chAB_filter[i]<minimum_valueAB):
            minimum_valueAB=data_chAB_filter[i]
            freq_minimum_position_AB=i
    
    freq_maximum_AB=freq_data[freq_maximum_position_AB+start_bandwidth_position]
    freq_minimum_AB=freq_data[freq_minimum_position_AB+start_bandwidth_position]
    
    print("Valor Máximo: ",maximum_valueAB, " Frequência: ",freq_maximum_AB)
    print("Valor Mínimo: ",minimum_valueAB, " Frequência: ",freq_minimum_AB)


    #calculo aqui
    if(s_parameter_test_selection==True):
        xtalk_valueAB=abs(maximum_valueAB-s_parameter_data_chAA[2][freq_maximum_position_AB+start_bandwidth_position])

    else:
        xtalk_valueAB=abs(maximum_valueAB-s_parameter_data_chAA[freq_maximum_position_AB+start_bandwidth_position])

        
    if (xtalk_valueAB<abs((xtalk_ref+xtalk_tol_ref))):
        xtalk_resultA="Crosstalk Channel "+str(sw2_port_1)+ "-" + str(sw2_port_2)+": FAILED"
        fail_A=1
    else:
        xtalk_resultA="Crosstalk Channel "+str(sw2_port_1)+ "-" + str(sw2_port_2)+": OK"
        fail_A=0
    
    print(xtalk_resultA)
        

    #Calculations and Results of Channel B: 2-1 or 4-3  
    #Determinar a maior amplitude, e a menor amplitude para comparação:
    maximum_valueBA= -1000
    minimum_valueBA=  1000
    
    for i in range (0,len(data_chBA_filter)):
        if(data_chBA_filter[i]>maximum_valueBA):
            maximum_valueBA=data_chBA_filter[i]
            freq_maximum_position_BA=i
        if(data_chBA_filter[i]<minimum_valueBA):
            minimum_valueBA=data_chBA_filter[i]
            freq_minimum_position_BA=i
    
    freq_maximum_BA=freq_data[freq_maximum_position_BA+start_bandwidth_position]
    freq_minimum_BA=freq_data[freq_minimum_position_BA+start_bandwidth_position]
    
    print("Valor Máximo: ",maximum_valueBA, " Frequência: ",freq_maximum_BA)
    print("Valor Mínimo: ",minimum_valueBA, " Frequência: ",freq_minimum_BA)

    #calculo aqui
    if(s_parameter_test_selection==True):
        xtalk_valueBA=abs(maximum_valueBA-s_parameter_data_chBB[2][freq_maximum_position_BA+start_bandwidth_position])
    else:
        xtalk_valueBA=abs(maximum_valueBA-s_parameter_data_chBB[freq_maximum_position_BA+start_bandwidth_position])

    #calculation
    if (xtalk_valueBA<abs((xtalk_ref+xtalk_tol_ref))):
        xtalk_resultB="Crosstalk Channel "+str(sw2_port_2)+ "-" + str(sw2_port_1)+": FAILED"
        fail_B=1
        print(xtalk_resultB)

    else:
        xtalk_resultB="Crosstalk Channel "+str(sw2_port_2)+ "-" + str(sw2_port_1)+": OK"
        fail_B=0
        print(xtalk_resultB)




    #LOG INFO
    xtalk_valueAB=round(xtalk_valueAB,2)
    strA_1="Channel "+str(sw2_port_1)+ "-" + str(sw2_port_2)  
    strA_2="Crosstalk [dB]: "+str(xtalk_valueAB)
    #strA_3="Frequency at Maximum Value [Hz]: "+str(freq_maximum_A)
    crosstalk_test_log.append(strA_1)
    crosstalk_test_log.append(strA_2)
    #crosstalk_test_log.append(strA_3)
    crosstalk_test_log.append(xtalk_resultA+"\n")

    xtalk_valueBA=round(xtalk_valueBA,2)    
    strB_1="Channel "+str(sw2_port_2)+ "-" + str(sw2_port_1)  
    strB_2="Crosstalk [dB]: "+str(xtalk_valueBA)
    #strB_3="Frequency at Maximum Value [Hz]: "+str(freq_maximum_B)
    crosstalk_test_log.append(strB_1)
    crosstalk_test_log.append(strB_2)
    #crosstalk_test_log.append(strB_3)
    crosstalk_test_log.append(xtalk_resultB+"\n")


    
    tela_leds.ui.progressBar.setValue(50+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra xtalk",tela_leds.repaint())
    print("barra xtalk",QApplication.processEvents())   

    
    return (xtalk_valueAB,xtalk_valueBA,fail_A,fail_B)