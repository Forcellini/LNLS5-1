from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
from rffe_test_lib import Agilent33521A #necessário para enviar comandos para o sgen
from rffe_test_lib import RF_switch_board_1 #necessário para enviar comandos para o switch 1
from rffe_test_lib import RF_switch_board_2 #necessário para enviar comandos para o switch 2
from rffe_test_lib import RFFEControllerBoard #necessário para enviar comandos para o RFFE
import test_lib

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from leds_rf_switch import leds_rf_switch

def return_loss_test_s11(vna,sgen,rffe,
                         rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                         rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                         center_freq, freq_span, 
                         pow_value, att_value,
                         ret_loss_s11_ref, ret_loss_s11_ref_tol,
                         start_bandwidth,stop_bandwidth,step_bandwidth,
                         ret_loss_test_log,percentual,
                         s_parameter_test_selection,
                         s_parameter_data_chA,s_parameter_data_chB,
                         freq_data,tela_leds):
    
    print("\nRunning return loss test s11 - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2)+"\n")

    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra ret loss",tela_leds.repaint())
    print("barra ret loss",QApplication.processEvents())  

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
    data_chA_filter=[]
    data_chB_filter=[]

    #Data Acquisition
    if(s_parameter_test_selection==True):
        
        print("Utilizando os dados adquiridos no teste do S-Parameters")
        #Neste teste utilizamos o parâmetro S21 
        #s_parameter_data_chA=[s11,s12,s21,s22]
        data_chA=s_parameter_data_chA[0]
        data_chB=s_parameter_data_chB[0]
                
        #start_bandwidth_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>=start_bandwidth):
                start_bandwidth_position=i
                break
        print("Frequencia Detectada: ",freq_data[start_bandwidth_position],"Frequencia Esperada: ",start_bandwidth)
            
        #stop_bandwith_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>stop_bandwidth):
                stop_bandwidth_position=i-1
                break   
        print(freq_data[stop_bandwidth_position],stop_bandwidth) 
        
        for i in range (start_bandwidth_position,stop_bandwidth_position):
            data_chA_filter.append(data_chA[i])
            data_chB_filter.append(data_chB[i])   
                     
        print("Aquisição de dados completa...")
        
        tela_leds.ui.progressBar.setValue(45+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra ret loss",tela_leds.repaint())
        print("barra ret loss",QApplication.processEvents())    
   
    else:
        
        print("Aquisição de dados necessária...Iniciando aquisição...")
        
        #Data acquisition for channel A 1-1 or 3-3
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        data_chA=vna.get_s11_data()
        
        #Data acquisition for channel B 2-2 or 4-4
        print("Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        data_chB=vna.get_s11_data()

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
            data_chA_filter.append(data_chA[i])
            data_chB_filter.append(data_chB[i])  
            
        print("Aquisição de dados completa...")       
        
        tela_leds.ui.progressBar.setValue(25+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra ret loss",tela_leds.repaint())
        print("barra ret loss",QApplication.processEvents())  

    
    #Tolerance
    print("Lower Boundary: ",abs(ret_loss_s11_ref+ret_loss_s11_ref_tol))
    print("Upper Boundary: ",str(0))
    
    #Calculations and Results of Channel A: 1-1 or 3-3  
    #Determinar a maior amplitude, e a menor amplitude para comparação:
    maximum_valueA= -1000
    minimum_valueA=  1000
    
    for i in range (0,len(data_chA_filter)):
        if(data_chA_filter[i]>maximum_valueA):
            maximum_valueA=data_chA_filter[i]
            freq_maximum_position_A=i
        if(data_chA_filter[i]<minimum_valueA):
            minimum_valueA=data_chA_filter[i]
            freq_minimum_position_A=i
            
    freq_maximum_A=freq_data[freq_maximum_position_A+start_bandwidth_position]
    freq_minimum_A=freq_data[freq_minimum_position_A+start_bandwidth_position]
    
   
    print("Valor Máximo: ",maximum_valueA, " Frequência: ",freq_maximum_A)
    print("Valor Mínimo: ",minimum_valueA, " Frequência: ",freq_minimum_A)
    
   
    #Verifica se o valor dentro da varredutra não ficou maior do que a tolerância máxima (ou seja, ponto máximo em relação com o ponto mínimo)
    #Verifica se o valor do ganho no filtro atingiu o valor mínimo especificado
    #deltaA=maximum_valueA-minimum_valueA
    #ret_loss_resultA_value = abs(deltaA)
    #str1_A="Result Delta Varredura (abs) [dB]: " +str(round(ret_loss_resultA_value,2))
    str2_A="Result Maximum (abs) [dB]: "+str(round(maximum_valueA,2))
    str3_A="Result Minimum (abs) [dB]: "+str(round(minimum_valueA,2))
    str4_A="Result Maximum - Frequency [Hz]: "+str(freq_maximum_A)   
    str5_A="Result Minimum - Frequency [Hz]: "+str(freq_minimum_A)    
    
    if (abs(maximum_valueA)<abs(ret_loss_s11_ref+ret_loss_s11_ref_tol) or maximum_valueA>0):
        ret_loss_resultA="Return Loss Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": FAILED"
        fail_A=1
    else:
        ret_loss_resultA="Return Loss Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": OK"
        fail_A=0

    print(ret_loss_resultA)
        

    #Calculations and Results of Channel B: 2-2 or 4-4  
    #Determinar a maior amplitude, e a menor amplitude para comparação:
    maximum_valueB= -1000
    minimum_valueB=  1000
    
    for i in range (0,len(data_chB_filter)):
        if(data_chB_filter[i]>maximum_valueB):
            maximum_valueB=data_chB_filter[i]
            freq_maximum_position_B=i
        if(data_chB_filter[i]<minimum_valueB):
            minimum_valueB=data_chB_filter[i]
            freq_minimum_position_B=i
    
    freq_maximum_B=freq_data[freq_maximum_position_B+start_bandwidth_position]
    freq_minimum_B=freq_data[freq_minimum_position_B+start_bandwidth_position]
    
    print("Valor Máximo: ",maximum_valueB, " Frequência: ",freq_maximum_B)
    print("Valor Mínimo: ",minimum_valueB, " Frequência: ",freq_minimum_B)

    
    #Verifica se o valor dentro da varredutra não ficou maior do que a tolerância máxima (ou seja, ponto máximo em relação com o ponto mínimo)
    #Verifica se o valor do ganho no filtro atingiu o valor mínimo especificado
    #deltaB=maximum_valueB-minimum_valueB
    #ret_loss_resultB_value = abs(deltaB)
    #str1_B="Result Delta Varredura (abs) [dB]: " +str(round(ret_loss_resultB_value,2))
    str2_B="Result Maximum (abs) [dB]: "+str(round(maximum_valueB,2)) 
    str3_B="Result Minimum (abs) [dB]: "+str(round(minimum_valueB,2))
    str4_B="Result Maximum - Frequency [Hz]: "+str(freq_maximum_B)   
    str5_B="Result Minimum - Frequency [Hz]: "+str(freq_minimum_B)  
     
    if (abs(maximum_valueB)<abs(ret_loss_s11_ref+ret_loss_s11_ref_tol) or maximum_valueB>0):
        ret_loss_resultB="Return Loss Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": FAILED"
        fail_B=1
    else:
        ret_loss_resultB="Return Loss Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": OK"
        fail_B=0
    print(ret_loss_resultB)   
   
    
     
   #LOG INFO
    ret_loss_test_log.append("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
    #ret_loss_test_log.append(str1_A)
    ret_loss_test_log.append(str2_A)
    #ret_loss_test_log.append(str3_A)
    ret_loss_test_log.append(str4_A)
    #ret_loss_test_log.append(str5_A)
    ret_loss_test_log.append(ret_loss_resultA+"\n")

    ret_loss_test_log.append("Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
    #ret_loss_test_log.append(str1_B)
    ret_loss_test_log.append(str2_B)
    #ret_loss_test_log.append(str3_B)
    ret_loss_test_log.append(str4_B)
    #ret_loss_test_log.append(str5_B)
    ret_loss_test_log.append(ret_loss_resultB+"\n")
    
    maximum_valueA=abs(maximum_valueA)
    maximum_valueB=abs(maximum_valueB)
    
    return (ret_loss_resultA,ret_loss_resultB,
            maximum_valueA,maximum_valueB,
            minimum_valueA,minimum_valueB,
            ret_loss_test_log,
            fail_A,fail_B)

def return_loss_test_s22(vna,sgen,rffe,
                         rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                         rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                         center_freq, freq_span, 
                         pow_value, att_value,
                         ret_loss_s22_ref, ret_loss_s22_ref_tol,
                         start_bandwidth,stop_bandwidth,step_bandwidth,
                         ret_loss_test_log,percentual,
                         s_parameter_test_selection,
                         s_parameter_data_chA,s_parameter_data_chB,
                         freq_data,tela_leds):
    
    print("\nRunning return loss test s22 - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2)+"\n")

    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra ret loss",tela_leds.repaint())
    print("barra ret loss",QApplication.processEvents())  

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
    data_chA_filter=[]
    data_chB_filter=[]

    #Data Acquisition
    if(s_parameter_test_selection==True):
        
        print("Utilizando os dados adquiridos no teste do S-Parameters")
        #Neste teste utilizamos o parâmetro S21 
        #s_parameter_data_chA=[s11,s12,s21,s22]
        data_chA=s_parameter_data_chA[3]
        data_chB=s_parameter_data_chB[3]
                
        #start_bandwidth_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>=start_bandwidth):
                start_bandwidth_position=i
                break
        print("Frequencia Detectada: ",freq_data[start_bandwidth_position],"Frequencia Esperada: ",start_bandwidth)
            
        #stop_bandwith_position
        for i in range (0,len(freq_data)):
            if(freq_data[i]>stop_bandwidth):
                stop_bandwidth_position=i-1
                break   
        print(freq_data[stop_bandwidth_position],stop_bandwidth) 
        
        for i in range (start_bandwidth_position,stop_bandwidth_position):
            data_chA_filter.append(data_chA[i])
            data_chB_filter.append(data_chB[i])   
                     
        print("Aquisição de dados completa...")
        print(data_chA_filter)
        print(data_chB_filter)
        
        tela_leds.ui.progressBar.setValue(25+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra ret loss",tela_leds.repaint())
        print("barra ret loss",QApplication.processEvents())    
    else:
        
        print("Aquisição de dados necessária...Iniciando aquisição...")
        
        #Data acquisition for channel A 1-1 or 3-3
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        data_chA=vna.get_s22_data()
        
        #Data acquisition for channel B 2-2 or 4-4
        print("Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        data_chB=vna.get_s22_data()

        #Frequency Data Acquisition
        freq_data=vna.get_frequency_data()
        
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
            data_chA_filter.append(data_chA[i])
            data_chB_filter.append(data_chB[i])  
            
        print("Aquisição de dados completa...")       
        
        tela_leds.ui.progressBar.setValue(25+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra ret loss",tela_leds.repaint())
        print("barra ret loss",QApplication.processEvents())  
    
    #Tolerance
    print("Lower Boundary: ",abs(ret_loss_s22_ref+ret_loss_s22_ref_tol))
    print("Upper Boundary: ",str(0))
    
    #Calculations and Results of Channel A: 1-1 or 3-3  
    #Determinar a maior amplitude, e a menor amplitude para comparação:
    maximum_valueA= -1000
    minimum_valueA=  1000
    
    for i in range (0,len(data_chA_filter)):
        if(data_chA_filter[i]>maximum_valueA):
            maximum_valueA=data_chA_filter[i]
            freq_maximum_position_A=i
        if(data_chA_filter[i]<minimum_valueA):
            minimum_valueA=data_chA_filter[i]
            freq_minimum_position_A=i
            
    freq_maximum_A=freq_data[freq_maximum_position_A+start_bandwidth_position]
    freq_minimum_A=freq_data[freq_minimum_position_A+start_bandwidth_position]
    
    print("Valor Máximo: ",maximum_valueA, " Frequência: ",freq_maximum_A)
    print("Valor Mínimo: ",minimum_valueA, " Frequência: ",freq_minimum_A)
    
    #Verifica se o valor dentro da varredutra não ficou maior do que a tolerância máxima (ou seja, ponto máximo em relação com o ponto mínimo)
    #Verifica se o valor do ganho no filtro atingiu o valor mínimo especificado
    #deltaA=maximum_valueA-minimum_valueA
    #ret_loss_resultA_value = abs(deltaA)
    #str1_A="Result Delta Varredura (abs) [dB]: " +str(round(ret_loss_resultA_value,2))
    str2_A="Result Maximum (abs) [dB]: "+str(round(maximum_valueA,2))
    str3_A="Result Minimum (abs) [dB]: "+str(round(minimum_valueA,2))
    str4_A="Result Maximum - Frequency [Hz]: "+str(freq_maximum_A)   
    str5_A="Result Minimum - Frequency [Hz]: "+str(freq_minimum_A)    
    
    if (abs(maximum_valueA)<abs(ret_loss_s22_ref+ret_loss_s22_ref_tol) or maximum_valueA>0):
        ret_loss_resultA="Return Loss Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": FAILED"
        fail_A=1
    else:
        ret_loss_resultA="Return Loss Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": OK"
        fail_A=0

    print(ret_loss_resultA)
        

    #Calculations and Results of Channel B: 2-2 or 4-4  
    #Determinar a maior amplitude, e a menor amplitude para comparação:
    maximum_valueB= -1000
    minimum_valueB=  1000
    
    for i in range (0,len(data_chB_filter)):
        if(data_chB_filter[i]>maximum_valueB):
            maximum_valueB=data_chB_filter[i]
            freq_maximum_position_B=i
        if(data_chB_filter[i]<minimum_valueB):
            minimum_valueB=data_chB_filter[i]
            freq_minimum_position_B=i
    
    if(s_parameter_test_selection==True):
        freq_maximum_B=freq_data[freq_maximum_position_B+start_bandwidth_position]
        freq_minimum_B=freq_data[freq_minimum_position_B+start_bandwidth_position]
    else:
        freq_maximum_B=freq_maximum_position_B*step_bandwidth+start_bandwidth
        freq_minimum_B=freq_minimum_position_B*step_bandwidth+start_bandwidth
    
    print("Valor Máximo: ",maximum_valueB, " Frequência: ",freq_maximum_B)
    print("Valor Mínimo: ",minimum_valueB, " Frequência: ",freq_minimum_B)
    
    #Verifica se o valor dentro da varredutra não ficou maior do que a tolerância máxima (ou seja, ponto máximo em relação com o ponto mínimo)
    #Verifica se o valor do ganho no filtro atingiu o valor mínimo especificado
    #deltaB=maximum_valueB-minimum_valueB
    #ret_loss_resultB_value = abs(deltaB)
    #str1_B="Result Delta Varredura (abs) [dB]: " +str(round(ret_loss_resultB_value,2))
    str2_B="Result Maximum (abs) [dB]: "+str(round(maximum_valueB,2)) 
    str3_B="Result Minimum (abs) [dB]: "+str(round(minimum_valueB,2))
    str4_B="Result Maximum - Frequency [Hz]: "+str(freq_maximum_B)   
    str5_B="Result Minimum - Frequency [Hz]: "+str(freq_minimum_B)  
     
    if (abs(maximum_valueB)<abs(ret_loss_s22_ref+ret_loss_s22_ref_tol) or maximum_valueB>0):
        ret_loss_resultB="Return Loss Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": FAILED"
        fail_B=1
    else:
        ret_loss_resultB="Return Loss Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": OK"
        fail_B=0
    print(ret_loss_resultB)   
   
    
   #LOG INFO
    ret_loss_test_log.append("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
    #ret_loss_test_log.append(str1_A)
    ret_loss_test_log.append(str2_A)
    #ret_loss_test_log.append(str3_A)
    ret_loss_test_log.append(str4_A)
    #ret_loss_test_log.append(str5_A)
    ret_loss_test_log.append(ret_loss_resultA+"\n")

    ret_loss_test_log.append("Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
    #ret_loss_test_log.append(str1_B)
    ret_loss_test_log.append(str2_B)
    #ret_loss_test_log.append(str3_B)
    ret_loss_test_log.append(str4_B)
    #ret_loss_test_log.append(str5_B)
    ret_loss_test_log.append(ret_loss_resultB+"\n")
    
    tela_leds.ui.progressBar.setValue(25+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra ret loss",tela_leds.repaint())
    print("barra ret loss",QApplication.processEvents())     
    
    maximum_valueA=abs(maximum_valueA)
    maximum_valueB=abs(maximum_valueB)
    
    return (ret_loss_resultA,ret_loss_resultB,
            maximum_valueA,maximum_valueB,
            minimum_valueA,minimum_valueB,
            ret_loss_test_log,
            fail_A,fail_B)