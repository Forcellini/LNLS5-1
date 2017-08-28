from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
from rffe_test_lib import Agilent33521A #necessário para enviar comandos para o sgen
from rffe_test_lib import RF_switch_board_1 #necessário para enviar comandos para o switch 1
from rffe_test_lib import RF_switch_board_2 #necessário para enviar comandos para o switch 2
from rffe_test_lib import RFFEControllerBoard #necessário para enviar comandos para o RFFE
import test_lib

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from leds_rf_switch import leds_rf_switch

def frequency_response_test(vna,sgen,rffe,
                            rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                            rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                            center_freq, freq_span, 
                            pow_value, att_value,
                            freq_res_ref,freq_res_tol_ref,freq_res_tol_var,
                            start_bandwidth,stop_bandwidth,step_bandwidth,
                            freq_resp_test_log,tela_leds,percentual,
                            s_parameter_test_selection,
                            s_parameter_data_chA,s_parameter_data_chB,
                            freq_data):
    

    print("\nRunning Frequency Response test - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2)+"\n")
    
    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra freq res",tela_leds.repaint())
    print("barra freq res",QApplication.processEvents())    


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
        data_chA=s_parameter_data_chA[2]
        data_chB=s_parameter_data_chB[2]
                
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
        
        tela_leds.ui.progressBar.setValue(45+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra freq res",tela_leds.repaint())
        print("barra freq res",QApplication.processEvents())    
    else:
        
        print("Aquisição de dados necessária...Iniciando aquisição...")
       
        #Data acquisition for channel A 1-1 or 3-3
        print("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        data_chA=vna.get_s21_data()
        
        #Data acquisition for channel B 2-2 or 4-4
        print("Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        data_chB=vna.get_s21_data()
        
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
        
        tela_leds.ui.progressBar.setValue(45+percentual)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra freq res",tela_leds.repaint())
        print("barra freq res",QApplication.processEvents())  
    
    #Tolerance
    print("Lower Boundary: ",freq_res_ref+freq_res_tol_ref)
        
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
    deltaA=maximum_valueA-minimum_valueA
    freq_resp_resultA_value = abs(deltaA)
    str1_A="Result Delta Varredura (abs) [dB]: " +str(round(freq_resp_resultA_value,2))
    str2_A="Result Maximum (abs) [dB]: "+str(round(maximum_valueA,2))
    str3_A="Result Minimum (abs) [dB]: "+str(round(minimum_valueA,2))
    str4_A="Result Maximum - Frequency [Hz]: "+str(freq_maximum_A)   
    str5_A="Result Minimum - Frequency [Hz]: "+str(freq_minimum_A)
    
     
    if (abs(deltaA)>freq_res_tol_var) or (abs(maximum_valueA)<(freq_res_ref+freq_res_tol_ref)):
        freq_resp_resultA="Frequency Response Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": FAILED"
        fail_A=1
    else:
        freq_resp_resultA="Frequency Response Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": OK"
        fail_A=0
    
    print(freq_resp_resultA)
        

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
    deltaB=maximum_valueB-minimum_valueB
    freq_resp_resultB_value = abs(deltaB)
    str1_B="Result Delta Varredura (abs) [dB]: " +str(round(freq_resp_resultB_value,2))
    str2_B="Result Maximum (abs) [dB]: "+str(round(maximum_valueB,2)) 
    str3_B="Result Minimum (abs) [dB]: "+str(round(minimum_valueB,2))
    str4_B="Result Maximum - Frequency [Hz]: "+str(freq_maximum_B)   
    str5_B="Result Minimum - Frequency [Hz]: "+str(freq_minimum_B)  
     
    if (abs(deltaB)>freq_res_tol_var) or (abs(maximum_valueB)<(freq_res_ref+freq_res_tol_ref)):
        freq_resp_resultB="Frequency Response Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": FAILED"
        fail_B=1
        print(freq_resp_resultB)

    else:
        freq_resp_resultB="Frequency Response Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": OK"
        fail_B=0
        print(freq_resp_resultB)

    
    #LOG INFO
    freq_resp_test_log.append("Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
    freq_resp_test_log.append(str1_A)
    freq_resp_test_log.append(str2_A)
    freq_resp_test_log.append(str3_A)
    freq_resp_test_log.append(str4_A)
    freq_resp_test_log.append(str5_A)
    freq_resp_test_log.append(freq_resp_resultA+"\n")

    freq_resp_test_log.append("Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2))
    freq_resp_test_log.append(str1_B)
    freq_resp_test_log.append(str2_B)
    freq_resp_test_log.append(str3_B)
    freq_resp_test_log.append(str4_B)
    freq_resp_test_log.append(str5_B)
    freq_resp_test_log.append(freq_resp_resultB+"\n")

    
    tela_leds.ui.progressBar.setValue(50+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra freq res",tela_leds.repaint())
    print("barra freq res",QApplication.processEvents())          

    deltaA=round(deltaA,2)
    deltaB=round(deltaB,2)
    
    return (freq_resp_resultA,freq_resp_resultB,
            deltaA,deltaB,
            maximum_valueA,maximum_valueB,
            freq_maximum_A,freq_maximum_B,
            freq_resp_test_log,
            fail_A,fail_B)


#A princípio, teste ok !!!......o valor da variável s21_ref foi alterado para 4.5. O valor original era 1.3
#conforme sugestão do sérgio.
#VERIFICAR SE O VALOR DO GANHO OBTIDO NO FILTRO PARA ATENUAÇÃO DE 30dB 
#ESTÁ OCORRENDO CONFORME PROJETO (atualmente o valor máximo que ele atinge está por volta de 34 dB)

