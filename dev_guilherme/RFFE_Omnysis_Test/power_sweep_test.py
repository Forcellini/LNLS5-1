from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
from rffe_test_lib import Agilent33521A #necessário para enviar comandos para o sgen
from rffe_test_lib import RF_switch_board_1 #necessário para enviar comandos para o switch 1
from rffe_test_lib import RF_switch_board_2 #necessário para enviar comandos para o switch 2
from rffe_test_lib import RFFEControllerBoard #necessário para enviar comandos para o RFFE
import test_lib
import urllib.request
import numpy as np
import time


from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from leds_rf_switch import leds_rf_switch

SLEEP_TIME = 5.0



def power_sweep_test(vna,sgen,rffe,
                     rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                     rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                     center_freq, freq_span, 
                     pow_value, att_value,
                     pow_sweep_ini,pow_sweep_end,pow_sweep_step,
                     linearity_ref, linearity_tol,pow_sweep_correction_factor,
                     att_fail_A,att_fail_B,
                     tela_leds,percentual,linearity_test_log,
                     freq_central_position):

    print("\nRunning Power Sweep (Linearity) test - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2))
    
    tela_leds.ui.progressBar.setValue(5+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra linearity",tela_leds.repaint())
    print("barra linearity",QApplication.processEvents())
            
    #Configuração Inicial de Segurança - Atenuador do RFFE no máximo, e VNA setado para pow_value dB
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
    rffe.set_attenuator_value(att_value)
    sgen.set_signal_DC()
    sgen.set_pos("direct")
    test_lib.set_vna(0, center_freq, freq_span, 0, vna)
    rfsw_1.sw1_pos(ip_sw1,3,3) #coloca o switch 1 na chave 3-3 = 0dBm
    rfsw_2.sw2_pos(ip_sw2,0,0)
    leds_rf_switch(3, 3, 0, 0, tela_leds)


    #Aquisição de dados 
    pow_sweep_resultA_1db=[]
    pow_sweep_resultA_5db=[]
    pow_sweep_resultB_1db=[]
    pow_sweep_resultB_5db=[]
    pow_sweep_resultA=[]
    pow_sweep_resultB=[]
    
    aver_value = 20
    aver_feedback =0
    vna.send_command(b":SENSE1:AVER:COUN "+ format(aver_value).encode('utf-8') + b"\n")
    vna.send_command(b":SENSE1:AVER ON\n")
    
    '''while(aver_feedback!=aver_value):
        aver_feedback=vna.check_avarage()
        print("valor no loop",aver_feedback)
    print("Average Factor: OK")'''
    
    
    espacamento=20
    
    #Aquisição de dados para o Canal A: 1-1 ou 3-3 para 1 dB no SWITCH 1   
    #Configuração deste teste
    #TESTE 1: Atenuação do Switch 1 configurado para 1 dB (Porta 2-2)
    print("falha em A: ",att_fail_A)
    if (att_fail_A==0): #só realiza este teste se o teste de atenuação for aprovado

        #Nível de 1 dB no Switch 1
        #Inicialização de Segurança
        vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 

        sw1_port_1=2
        print("Running power sweep test: 1dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1))
        rfsw_1.sw1_pos(ip_sw1,sw1_port_1,sw1_port_1) #porta 2-2 do switch 1
       
        #Canal A: 1-1 ou 3-3 do Switch 2
        strA_1="Running power sweep test: 1dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1)
        strA_2="Switch 2 - Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)
        print("Switch 2 - Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1) 
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        
        power_values=np.arange(float(pow_sweep_ini),float(pow_sweep_end),float(pow_sweep_step)) 
        print(pow_sweep_ini,pow_sweep_end,pow_sweep_step)
        print(power_values)
        
        for i in range (0,len(power_values)):
            vna.set_power_range(power_values[i])
            vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
            if (i==0):
                time.sleep(SLEEP_TIME)
            data_chA=vna.get_s21_data()
            data_chA_center_freq=data_chA[freq_central_position]
            pow_sweep_resultA_1db.append(data_chA_center_freq)
        print("Data acquired!")
        print("Canal A 1dB:",pow_sweep_resultA_1db)
        
        strA_3="Data Acquired:"
        strA_4="Input Power [dB]".ljust(espacamento)+"Measurement [dB]".ljust(espacamento)
        
        #Nível de 5 dB no Switch 1
        #Inicialização de Segurança
        vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 
        
        sw1_port_1=1
        print("Running power sweep test: 5dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1))
        rfsw_1.sw1_pos(ip_sw1,sw1_port_1,sw1_port_1) #porta 1-1 do switch 1
       
        #Canal A: 1-1 ou 3-3 do Switch 2
        print("Switch 2 - Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1))
        strA_5="Running power sweep test: 5dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1)
        strA_6="Switch 2 - Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)
        rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1) 
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)
        
        for i in range (0,len(power_values)):
            vna.set_power_range(power_values[i])
            vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
            if (i==0):
                time.sleep(SLEEP_TIME)

            data_chA=vna.get_s21_data()
            data_chA_center_freq=data_chA[freq_central_position]
            pow_sweep_resultA_5db.append(data_chA_center_freq)
        
        strA_7="Data Acquired:"
        strA_8="Input Power [dB]".ljust(espacamento)+"Measurement [dB]".ljust(espacamento)
        
        print("Data acquired!")
        print("Canal A 5dB:",pow_sweep_resultA_5db)

    else:
        strA_1="Data for Channel: Switch 2 - Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+" was not acquired due to safety reasons"
        strA_2="Attenuator test for this channel was not performed or attenuator test for this channel has failed"
        print("This test was not performed due to safety reasons")


    tela_leds.ui.progressBar.setValue(25+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra linearity",tela_leds.repaint())
    print("barra linearity",QApplication.processEvents())

    #Aquisição de dados para o Canal B: 2-2 ou 4-4 para 1 dB no SWITCH 1   
    #Configuração deste teste
    #TESTE 1: Atenuação do Switch 1 configurado para 1 dB (Porta 2-2)
    print("falha em B: ",att_fail_B)
    if (att_fail_B==0): #só realiza este teste se o teste de atenuação for aprovado

        #Nível de 1 dB no Switch 1
        #Inicialização de Segurança
        vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 

        sw1_port_1=2
        print("Running power sweep test: 1dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1))
        rfsw_1.sw1_pos(ip_sw1,sw1_port_1,sw1_port_1) #porta 2-2 do switch 1
       
        #Canal B: 2-2 ou 4-4 do Switch 2
        print("Switch 2 - Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2))
        strB_1="Running power sweep test: 1dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1)
        strB_2="Switch 2 - Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2) 
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        
        power_values=np.arange(float(pow_sweep_ini),float(pow_sweep_end),float(pow_sweep_step)) 
        
        for i in range (0,len(power_values)):
            vna.set_power_range(power_values[i])
            vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
            data_chB=vna.get_s21_data()
            data_chB_center_freq=data_chB[freq_central_position]
            pow_sweep_resultB_1db.append(data_chB_center_freq)
        print("Data acquired!")
        print("Canal B 1dB:",pow_sweep_resultB_1db)
 
        strB_3="Data Acquired:"
        strB_4="Input Power [dB]".ljust(espacamento)+"Measurement [dB]".ljust(espacamento)
        
        #Nível de 5 dB no Switch 1
        #Inicialização de Segurança
        vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 
        
        sw1_port_1=1
        print("Running power sweep test: 5dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1))
        rfsw_1.sw1_pos(ip_sw1,sw1_port_1,sw1_port_1) #porta 1-1 do switch 1
       
        #Canal A: 2-2 ou 4-4 do Switch 2
        print("Switch 2 - Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2))
        rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2) 
        strB_5="Running power sweep test: 5dB of Attenuation - Switch 1 - Channel: "+str(sw1_port_1)+ "-" + str(sw1_port_1)
        strB_6="Switch 2 - Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)
        leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)
        
        for i in range (0,len(power_values)):
            vna.set_power_range(power_values[i])
            vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
            data_chB=vna.get_s21_data()
            data_chB_center_freq=data_chB[freq_central_position]
            pow_sweep_resultB_5db.append(data_chB_center_freq)
        print("Canal B 5dB:",pow_sweep_resultB_5db)
        print("Data acquired!")
        
        strB_7="Data Acquired:"
        strB_8="Input Power [dB]".ljust(espacamento)+"Measurement [dB]".ljust(espacamento)
        
    else:
        strB_1="Data for Channel: Switch 2 - Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+" was not acquired due to safety reasons"
        strB_2="Attenuator test for this channel was not performed or attenuator test for this channel has failed"
        print("This test was not performed due to safety reasons")

    tela_leds.ui.progressBar.setValue(45+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra linearity",tela_leds.repaint())
    print("barra linearity",QApplication.processEvents())
    
    
    #Tolerance
    print("Upper Boundary: ", linearity_ref+linearity_tol) 
    print("Lower Boundary: ", linearity_ref-linearity_tol)
     
    #Calculations Channel A
    if (att_fail_A==0):   
        fail_A=0
        
        for i in range(0,len(power_values)):
            pow_sweep_resultA.append(pow_sweep_resultA_1db[i]-pow_sweep_resultA_5db[i])
            pow_sweep_resultA[i]=round(abs(abs(pow_sweep_resultA[i])-pow_sweep_correction_factor),2)
            if (pow_sweep_resultA[i]>(linearity_ref+linearity_tol)):
                fail_A=fail_A+1
        
        if fail_A!=0:
            lin_resultA="Linearity Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": FAILED"
            print("Result: ", pow_sweep_resultA)

        else:
            lin_resultA="Linearity Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": OK"
            print("Result: ", pow_sweep_resultA)
 
    else:
        lin_resultA = "Linearity Test for Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1) + ": FAILED"
        pow_sweep_resultA = "-"
        print(lin_resultA)


    #Calculations Channel B
    if (att_fail_B==0):   
        fail_B=0
        
        for i in range(0,len(power_values)):
            pow_sweep_resultB.append(pow_sweep_resultB_1db[i]-pow_sweep_resultB_5db[i])
            pow_sweep_resultB[i]=round(abs(abs(pow_sweep_resultB[i])-pow_sweep_correction_factor),2)
            if (pow_sweep_resultB[i]>(linearity_ref+linearity_tol)):
                fail_B=fail_B+1
        
        if fail_B!=0:
            lin_resultB="Linearity Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": FAILED"
            print("Result: ", pow_sweep_resultB)

        else:
            lin_resultB="Linearity Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": OK"
            print("Result: ", pow_sweep_resultB)
 
    else:
        lin_resultB = "Linearity Test for Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2) + ": FAILED"
        pow_sweep_resultB = "-"  
        print(lin_resultB)      
        
    
    if(att_fail_A==0):
               
        linearity_test_log.append("\n"+strA_2)
        linearity_test_log.append(strA_1)
        linearity_test_log.append(strA_3)
        linearity_test_log.append(strA_4)
        for i in range (0,len(power_values)):
            linearity_test_log.append(str(power_values[i]).ljust(espacamento)+str(pow_sweep_resultA_1db[i]).ljust(espacamento))

        linearity_test_log.append(strA_5)
        #linearity_test_log.append(strA_6)
        linearity_test_log.append(strA_7)
        linearity_test_log.append(strA_8)
        for i in range (0,len(power_values)):
            linearity_test_log.append(str(power_values[i]).ljust(espacamento)+str(pow_sweep_resultA_5db[i]).ljust(espacamento))
  
        linearity_test_log.append("Final Result:")
        #linearity_test_log.append(strA_6)
        linearity_test_log.append("Measurement".ljust(espacamento)+"Result [dB]".ljust(espacamento))
        for i in range (0,len(pow_sweep_resultA)):
            linearity_test_log.append(str((i+1)).ljust(espacamento)+str(pow_sweep_resultA[i]).ljust(espacamento))
        linearity_test_log.append(lin_resultA+"\n")
    else:
        fail_A=1
        linearity_test_log.append(strA_1)
        linearity_test_log.append(strA_2)
        linearity_test_log.append(lin_resultA)

    if(att_fail_B==0):

        linearity_test_log.append("\n"+strB_2)
        linearity_test_log.append(strB_1)
        linearity_test_log.append(strB_3)
        linearity_test_log.append(strB_4)
        for i in range (0,len(power_values)):
            linearity_test_log.append(str(power_values[i]).ljust(espacamento)+str(pow_sweep_resultB_1db[i]).ljust(espacamento))
        
        linearity_test_log.append(strB_5)
        #linearity_test_log.append(strB_6)
        linearity_test_log.append(strB_7)
        linearity_test_log.append(strB_8)
        for i in range (0,len(power_values)):
            linearity_test_log.append(str(power_values[i]).ljust(espacamento)+str(pow_sweep_resultB_5db[i]).ljust(espacamento))
 
        linearity_test_log.append("Final Result:")
        #linearity_test_log.append(strB_6)
        linearity_test_log.append("Measurement".ljust(espacamento)+"Result [dB]".ljust(espacamento))
        for i in range (0,len(pow_sweep_resultA)):
            linearity_test_log.append(str((i+1)).ljust(espacamento)+str(pow_sweep_resultB[i]).ljust(espacamento))
        linearity_test_log.append(lin_resultB+"\n")
    else:
        fail_B=1
        linearity_test_log.append(strB_1)
        linearity_test_log.append(strB_2)
        linearity_test_log.append(lin_resultB)
        
    
    #Coloca o equipamento para operar na potência de referência 
    vna.set_power_range(pow_value)
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
    #Coloca o switch 1 no valor de referência de 0 dB
    sw1_port_1=3
    rfsw_1.sw1_pos(ip_sw1,sw1_port_1,sw1_port_1) #porta 1-1 do switch 1
    leds_rf_switch(sw1_port_1, sw1_port_2, 0, 0, tela_leds)
    vna.send_command(b":SENSE1:AVER OFF\n")


    tela_leds.ui.progressBar.setValue(50+percentual)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra linearity",tela_leds.repaint())
    print("barra linearity",QApplication.processEvents())
    
    
    return (pow_sweep_resultA,pow_sweep_resultB,fail_A,fail_B)