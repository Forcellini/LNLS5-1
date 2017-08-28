#!/usr/bin/pytho

#rffe_run_test
from rffe_test_lib import Agilent33521A
from rffe_test_lib import RFFEControllerBoard
from rffe_test_lib import AgilentE5061B
from rffe_test_lib import RF_switch_board_1
from rffe_test_lib import RF_switch_board_2
import sys
import read_metadata
import numpy as np
import test_lib
import shutil
import time
import os
import urllib.request
import datetime

from temperature_test import temperature_test
from crosstalk_test import crosstalk_test
from return_loss_test import return_loss_test_s11
from return_loss_test import return_loss_test_s22
from rf_switches_test import rf_switches_test
from frequency_response_test import frequency_response_test
from power_sweep_test import power_sweep_test
from attenuators_sweep_test import attenuators_sweep_test
from s_parameters_test import s_parameters_test
from communication import communication
from leds_rf_switch import leds_rf_switch

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QDateTime

def run_rffe_test_p_interface(tela_leds,
                              ip_switch_1,ip_switch_2,ip_rffe,ip_gerador_sinais_dc,ip_network_analyzer,
                              att_ref,switch_ref,freq_res_ref,ret_loss_s11_ref,ret_loss_s22_ref,linearity_ref,xtalk_ref,temp_min,temp_max,
                              att_tol,switch_tol,freq_res_tol_ref,ret_loss_s11_tol_ref,ret_loss_s22_tol_ref,linearity_tol,xtalk_tol_ref,
                              freq_res_tol_var,
                              s_parameter_test_selection,atenuadores_test_selection,switch_dc_test_selection,freq_resp_test_selection,ret_loss_test_selection,
                              linearidade_test_selection,crosstalk_test_selection,temp_test_selection,all_tests_selection,curva_s_parameter,
                              network_freq_central,network_freq_span,
                              network_pot_in_standard,network_pot_in_inicial,network_pot_in_final,network_pot_in_step,
                              rffe_attenuation_standard,rffe_attenuation_initial,rffe_attenuation_final,rffe_attenuation_step,
                              network_model,waveform_model,dc_power_model,rf_switch_model,rffe_serie,
                              network_start_bandwidth,network_stop_bandwidth,rffe_operador):

    ######################################
    #Initialization example:
    #python3 run_rffe_test.py 123456 /home/lnls-bpm/Desktop/test_report_bpm_hardware/rffe/rffe_test_metadata.txt /home/lnls-bpm/Desktop/test_report_bpm_hardware/rffe/test_evaluation

    print("\n- Loading parameters\n- Instruments configuration\n...\n")
    #rfsw_address
    ######################################
    #inserir programa de leitura da camera
    #serial_number=str(sys.argv[1])
    serial_number=rffe_serie

    #################################
    #metadata_path=str(sys.argv[2])
    metadata_path="rffe_test_metadata.txt"

    #datapath_save=str(sys.argv[3])
    datapath_save="result/"
    ######################################

    ##get current date and time
    current_time=str(time.strftime("%c"))
    current_day=str(time.strftime("%d-%m-%Y"))
    
    #Start Time do Teste
    start_time_general=datetime.datetime.now()
    start_time_general_str=start_time_general.strftime("%d-%m-%Y %H:%M:%S")
    
    
    #Diretório Principal
    try:
        os.makedirs(datapath_save + "sn_" + str(serial_number)+"/"+current_day)
    except:
        pass

    datapath_save=datapath_save + "sn_" + str(serial_number)+"/"+current_day+"/"
    
    #Diretório para armazenar as figuras do teste S Parameter
    try:
        os.makedirs(datapath_save + "figures/")
    except:
        pass

    datapath_save_figure=datapath_save + "figures/"
    
    #Diretório para armazenar os dados do S Parameter
    try:
        os.makedirs(datapath_save + "sparam_data/")
    except:
        pass

    datapath_save_sparam=datapath_save + "sparam_data/"

    #Obtém alguns dados do meta data (o número de pontos até o momento)
    #porem este parametro nao é utilizado na simulação
    metadata_param=read_metadata.read_vars(metadata_path)
    
    #Verifica a comunicacao com os equipamentos
    (vna,rfsw_1,rfsw_2,rffe,sgen,
     rffe_str_msg_communication,vna_str_msg_communication,rfsw_1_str_msg_communication,rfsw_2_str_msg_communication,sgen_str_msg_communication)=communication(ip_network_analyzer,ip_switch_1,ip_switch_2,ip_rffe,ip_gerador_sinais_dc,tela_leds)
    
    #Configuração das portas de acesso padrão do Switch

    #Switch 1 
    # 0 = Desliga canal
    # 1 = Set de 5dB de ganho
    # 2 = Set de 1dB de ganho
    # 3 = Set de 0dB de ganho

    sw1_port_1=3 #(0, 1, 2 ou 3) 
    sw1_port_2=3 #(0, 1, 2 ou 3) #mudar este valor serve apenas para teste
    #Este teste inteiro é realizado com o switch 1 ligado em 0dB. Não mudar este valor.

    #Switch 2 
    # 0 = Desliga canal
    # 1 = Liga canal 1
    # 2 = Liga canal 2
    # 3 = Liga canal 3
    # 4 = Liga canal 4

    sw2_port_1=3 #(0, 1, 2, 3 e 4)
    sw2_port_2=4 #(0, 1, 2, 3 e 4)

    #Equivalencia de nomes
    ip_sw1 = ip_switch_1
    ip_sw2 = ip_switch_2

    #Informacoes de controle do NETWORK ANALYZER
    pow_value=network_pot_in_standard
    center_freq=network_freq_central
    freq_span=network_freq_span
    #também poderíamos ter as duas variáveis abaixo
    #freq_start=int(metadata_param['freq_start'])
    #freq_stop=int(metadata_param['freq_stop'])
    
    #As variaveis abaixo definem as caracteristicas do teste de linearidade através do controle do network analyzer
    pow_sweep_ini=network_pot_in_inicial
    pow_sweep_end=network_pot_in_final
    pow_sweep_step=network_pot_in_step

    #Informacoes de controle do RFFE
    att_value=rffe_attenuation_standard
    n_points=int(float(metadata_param['n_points']))
    att_sweep_low=rffe_attenuation_initial
    att_sweep_high=rffe_attenuation_final
    att_step=rffe_attenuation_step
    #também temos as duas variáveis abaixo
    #rffe_attenuation_final
    #rffe_attenuation_initial
    
    #TOLERANCIA DOS TESTES com base nas variaveis originais do programa
    att_step_tol=float(att_tol)
    temp_min=float(temp_min)
    temp_max=float(temp_max)
    linearity_tol=float(linearity_tol)
    pow_sweep_correction_factor=4 #diferenca entre 5 dB e 1 dB, ou seja, step de 4dB
    '''s11_ref=float(ret_loss_s11_ref)
    s21_ref=float(freq_res_ref)
    s22_ref=float(ret_loss_s22_ref)
    s11_tol=float(ret_loss_s11_tol_ref)
    s21_tol=float(freq_res_tol)
    s22_tol=float(ret_loss_s22_tol)
    s12_ref=float(metadata_param['s12_ref'])
    s12_tol=float(metadata_param['s12_tolerance'])'''
    #pow_sweep_att=float(metadata_param['pow_sweep_att']) é equivalente aos pow_value
    #usado no teste de linearidade

    #acho que isto serve para realizar a varredura....
    start_bandwidth=network_start_bandwidth
    stop_bandwidth=network_stop_bandwidth
    step_bandwidth=float(metadata_param['step_bandwidth'])

    #Quando att_fail = 0, o teste de atenuação é considerado como OK e podemos prosseguir para realizar o teste de linearidade
    att_fail_1 = 0
    att_fail_2 = 0
    att_fail_3 = 0
    att_fail_4 = 0

    print("Test parameters loaded from metadata - ok!\n...\n")

    #Configuração Inicial de Segurança
    rffe.set_attenuator_value(att_value)
    sgen.set_signal_DC()
    sgen.set_pos("direct")
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 
    test_lib.set_vna(0, center_freq, freq_span, 0, vna)
    rfsw_1.sw1_pos(ip_sw1,3,3) #coloca o switch 1 na chave 3-3 = 0dBm
    rfsw_2.sw2_pos(ip_sw2,0,0) #desliga a chave 2
    tela_leds.ui.progressBar.setValue(0) 
    leds_rf_switch(3, 3, 0, 0, tela_leds)


    print("Set-up Configuration - Ok\n...")

    if (all_tests_selection==True):
        s_parameter_test_selection=True
        atenuadores_test_selection=True
        switch_dc_test_selection=True
        freq_resp_test_selection=True
        ret_loss_test_selection=True
        linearidade_test_selection=True
        crosstalk_test_selection=True
        temp_test_selection=True

    #LOG VARIABLE
    SPACE="############################################"
    log_file_general=[]
    set_up_log=[]
    s_parameter_test_log=[]
    attenuator_test_log=[]
    rf_switch_test_log=[]
    freq_resp_test_log=[]
    ret_loss_test_log=[]
    linearity_test_log=[]
    temperature_test_log=[]
    crosstalk_test_log=[]

    
    s_parameter_data_ch11_log=[]
    s_parameter_data_ch12_log=[]
    s_parameter_data_ch21_log=[]
    s_parameter_data_ch22_log=[]
    s_parameter_data_ch33_log=[]
    s_parameter_data_ch34_log=[]
    s_parameter_data_ch43_log=[]
    s_parameter_data_ch44_log=[]

  
    
    ################################################################  
    #S-Parameters test (NEW ONE) - OK
    if s_parameter_test_selection==True:
        tela_leds.ui.progressBar.setValue(0) 
        tela_leds.ui.kled_PARAMETRO_S_TEST.setState(1)
        tela_leds.ui.kled_PARAMETRO_S_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led s parameter",tela_leds.repaint())
        print("led s parameter",QApplication.processEvents()) 
                
        percentual=0
        espacamento=12
        
        sw2_port_1=1 
        sw2_port_2=2 
        
        #LOG INFO
        s_parameter_test_log.append(SPACE)
        s_parameter_test_log.append("S-Parameters Test")
        s_parameter_test_log.append("Test configuration:")
        s_parameter_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        s_parameter_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        s_parameter_test_log.append("Network Analyzer - Power Level [dB]: "+str(pow_value))
        s_parameter_test_log.append("Network Analyzer - Number of pts acquired per parameter: "+str(n_points))
        s_parameter_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
        s_parameter_test_log.append("RFFE Attenuation [dB]: "+str(att_value))
        s_parameter_test_log.append("RF Switch 1 Position: " +str(sw1_port_1)+"-"+str(sw1_port_2))
        s_parameter_test_log.append("Type of data acquired: S11, S12, S21, S22")
        s_parameter_test_log.append("Result Info:\n")
        
        
        (sparam_12,s_parameter_data_ch11,s_pos_a_ch,s_parameter_data_ch12,s_pos_b_ch,
         s_parameter_data_ch21,s_pos_c_ch,s_parameter_data_ch22,s_pos_d_ch,freq_data,freq_data_mhz) = s_parameters_test(vna,sgen,rffe,
                                                                                                                        rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                        rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                        center_freq, freq_span, 
                                                                                                                        pow_value, att_value,
                                                                                                                        serial_number,metadata_path,datapath_save,tela_leds,percentual,curva_s_parameter,datapath_save_figure)
        
        s_parameter_data_ch11_log.append("RFFE Ch: "+str(s_pos_a_ch[0])+"-"+str(s_pos_a_ch[1])+"\n")
        s_parameter_data_ch11_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch11_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch11[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch11[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch11[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch11[3][i]).ljust(espacamento))
            
        
        s_parameter_data_ch12_log.append("RFFE Ch: "+str(s_pos_b_ch[0])+"-"+str(s_pos_b_ch[1])+"\n")
        s_parameter_data_ch12_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch12_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch12[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch12[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch12[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch12[3][i]).ljust(espacamento))
            
        s_parameter_data_ch21_log.append("RFFE Ch: "+str(s_pos_c_ch[0])+"-"+str(s_pos_c_ch[1])+"\n")
        s_parameter_data_ch21_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch21_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch21[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch21[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch21[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch21[3][i]).ljust(espacamento))
        
        s_parameter_data_ch22_log.append("RFFE Ch: "+str(s_pos_d_ch[0])+"-"+str(s_pos_d_ch[1])+"\n")
        s_parameter_data_ch22_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch22_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch22[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch22[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch22[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch22[3][i]).ljust(espacamento))
            
        tela_leds.ui.progressBar.setValue(50)
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra s parameter",tela_leds.repaint())
        print("barra s parameter",QApplication.processEvents()) 
            
        sw2_port_1=3 
        sw2_port_2=4 
        percentual=50
        
        (sparam_34,s_parameter_data_ch33,s_pos_a_ch,s_parameter_data_ch34,s_pos_b_ch,
         s_parameter_data_ch43,s_pos_c_ch,s_parameter_data_ch44,s_pos_d_ch,freq_data,freq_data_mhz) = s_parameters_test(vna,sgen,rffe,
                                                                                                                        rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                        rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                        center_freq, freq_span, 
                                                                                                                        pow_value, att_value,
                                                                                                                        serial_number,metadata_path,datapath_save,tela_leds,percentual,curva_s_parameter,datapath_save_figure)
        
        
        s_parameter_data_ch33_log.append("RFFE Ch: "+str(s_pos_a_ch[0])+"-"+str(s_pos_a_ch[1])+"\n")
        s_parameter_data_ch33_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch33_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch33[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch33[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch33[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch33[3][i]).ljust(espacamento))
            
        
        s_parameter_data_ch34_log.append("RFFE Ch: "+str(s_pos_b_ch[0])+"-"+str(s_pos_b_ch[1])+"\n")
        s_parameter_data_ch34_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch34_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch34[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch34[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch34[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch34[3][i]).ljust(espacamento))
            
        s_parameter_data_ch43_log.append("RFFE Ch: "+str(s_pos_c_ch[0])+"-"+str(s_pos_c_ch[1])+"\n")
        s_parameter_data_ch43_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch43_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch43[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch43[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch43[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch43[3][i]).ljust(espacamento))
        
        s_parameter_data_ch44_log.append("RFFE Ch: "+str(s_pos_d_ch[0])+"-"+str(s_pos_d_ch[1])+"\n")
        s_parameter_data_ch44_log.append("Freq [MHz]".ljust(espacamento)+"S11 [dB]".ljust(espacamento)+"S12 [dB]".ljust(espacamento)+"S21 [dB]".ljust(espacamento)+"S22 [dB]".ljust(espacamento))
        for i in range (0,len(freq_data_mhz)):
            s_parameter_data_ch44_log.append(str(freq_data_mhz[i]).ljust(espacamento)+
                                             str(s_parameter_data_ch44[0][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch44[1][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch44[2][i]).ljust(espacamento)+
                                             str(s_parameter_data_ch44[3][i]).ljust(espacamento))
        
        tela_leds.ui.progressBar.setValue(100) 
        tela_leds.ui.kled_PARAMETRO_S_TEST.setState(1)
        tela_leds.ui.kled_PARAMETRO_S_TEST.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led s parameter",tela_leds.repaint())
        print("led s parameter",QApplication.processEvents()) 
        print("S-Parameters test - done")
        s_result="OK"
        s_parameter_test_log.append("S-Parameters Test FINAL RESULT: DATA ACQUIRED")
        s_parameter_test_log.append(SPACE+"\n")
        
    else:
        s_result="Data Not Acquired"
        s_parameter_test_log.append(SPACE)
        s_parameter_test_log.append("S-Parameters Test")
        s_parameter_test_log.append("S-Parameters Test FINAL RESULT: TEST NOT PERFORMED")
        s_parameter_test_log.append(SPACE+"\n")
        s_parameter_data_ch11_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch12_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch21_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch22_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch33_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch34_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch43_log.append("S-Paramenters Test - Test not Performed")
        s_parameter_data_ch44_log.append("S-Paramenters Test - Test not Performed")
        
        s_parameter_data_ch11="-"
        s_parameter_data_ch12="-"
        s_parameter_data_ch21="-"
        s_parameter_data_ch22="-"
        s_parameter_data_ch33="-"
        s_parameter_data_ch34="-"
        s_parameter_data_ch43="-"
        s_parameter_data_ch44="-"
        freq_data_mhz="-"
        freq_data="-"
        
        print("S-Parameters test - choosed not to be performed")
        tela_leds.ui.kled_PARAMETRO_S_TEST.setState(1)
        tela_leds.ui.kled_PARAMETRO_S_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led s parameter",tela_leds.repaint())
        print("led s parameter",QApplication.processEvents()) 
    
    #Variavel de saida
    s_param_res_ap=s_result
    ################################################################  
   

    ################################################################   
    #Attenuators sweep test (NEW ONE) - OK
    #Porta 1-1 e 2-2
    if atenuadores_test_selection==True:
        
        tela_leds.ui.progressBar.setValue(0) 
        tela_leds.ui.kled_ATENUADORES_TEST.setState(1)
        tela_leds.ui.kled_ATENUADORES_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led atenuadores",tela_leds.repaint())
        print("led atenuadores",QApplication.processEvents()) 
        
        #LOG INFO
        attenuator_test_log.append(SPACE)
        attenuator_test_log.append("Attenuator Sweep Test")
        attenuator_test_log.append("Test configuration:")
        attenuator_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        attenuator_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        attenuator_test_log.append("Network Analyzer - Power Level [dB]: "+str(pow_value))
        attenuator_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
        attenuator_test_log.append("RF Switch 1 Position: " +str(sw1_port_1)+"-"+str(sw1_port_2))
        attenuator_test_log.append("Type of data acquired: S21\n")
        attenuator_test_log.append("Tolerance:")
        attenuator_test_log.append("Upper Boundary Tolerance (abs)[dB]: "+ str(abs(att_step+att_step_tol)))
        attenuator_test_log.append("Lower Boundary Tolerance (abs)[dB]: "+ str(abs(att_step-att_step_tol)))
        attenuator_test_log.append("\nResult Info:\n")
        
        percentual=0
        fail_general_atenuadores=0

        sw2_port_1=1 
        sw2_port_2=2 
            
        (att_sweep_result_1,step_size_1,att_sweep_result_2,step_size_2,att_fail_1,att_fail_2,attenuator_test_log) = attenuators_sweep_test(vna,sgen,rffe,
                                                                                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                                           center_freq, freq_span,
                                                                                                                                           pow_value, att_value,
                                                                                                                                           att_sweep_low,att_sweep_high,att_step,att_step_tol,
                                                                                                                                           tela_leds,percentual,attenuator_test_log)
        if(att_fail_1==1):
            print("\nCanal 1 do Front End com Falha no Atenuador")
            fail_general_atenuadores=fail_general_atenuadores+1
            att_aprovacao_1="FAIL"
        else:
            att_aprovacao_1="OK"
            
        if(att_fail_2==1):
            print("Canal 2 do Front End com Falha no Atenuador")
            fail_general_atenuadores=fail_general_atenuadores+1
            att_aprovacao_2="FAIL"
        else:
            att_aprovacao_2="OK"
    
    else:
        sw2_port_1=1 
        sw2_port_2=2 
        att_sweep_result_1="Attenuator Sweep Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" --> Test not Performed"
        step_size_1 = "-"
        att_sweep_result_2="Attenuator Sweep Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" --> Test not Performed"
        step_size_2 = "-"
        #A linha abaixo serve para impedir que o teste de linearidade seja executado 
        #sem que o de atenuação tenha confirmado que o rffe está ok
        att_fail_1=1 
        att_fail_2=1
        print("Attenuator Sweep Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))

    #Porta 3-3 e 4-4
    if atenuadores_test_selection==True:
        sw2_port_1=3 
        sw2_port_2=4 
        step_size_3=list()
        step_size_4=list()
        percentual=50
         
        (att_sweep_result_3,step_size_3,att_sweep_result_4,step_size_4,att_fail_3,att_fail_4,attenuator_test_log) = attenuators_sweep_test(vna,sgen,rffe,
                                                                                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                                           center_freq, freq_span,
                                                                                                                                           pow_value, att_value,
                                                                                                                                           att_sweep_low,att_sweep_high,att_step,att_step_tol,
                                                                                                                                           tela_leds,percentual,attenuator_test_log)
        if(att_fail_3==1):
            print("\nCanal 3 do Front End com Falha no Atenuador")
            fail_general_atenuadores=fail_general_atenuadores+1
            att_aprovacao_3="FAIL"
        else:
            att_aprovacao_3="OK"
            
        if(att_fail_4==1):
            print("Canal 4 do Front End com Falha no Atenuador")
            fail_general_atenuadores=fail_general_atenuadores+1
            att_aprovacao_4="FAIL"
        else:
            att_aprovacao_4="OK"
        
        #Avaliação Final do Teste de Atenuadores: Indicação no LED    
        if (fail_general_atenuadores!=0):
            print("Teste de Atenuadores: Falha detectada")
            attenuator_test_log.append("Attenuator Sweep Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_ATENUADORES_TEST.setState(1)
            tela_leds.ui.kled_ATENUADORES_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led atenuadores",tela_leds.repaint())
            print("led atenuadores",QApplication.processEvents())
            
        else:
            print("Teste de Atenuadores: Passou em todos os canais")
            attenuator_test_log.append("Attenuator Sweep Test FINAL RESULT: OK")
            tela_leds.ui.kled_ATENUADORES_TEST.setState(1)
            tela_leds.ui.kled_ATENUADORES_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led atenuadores",tela_leds.repaint())
            print("led atenuadores",QApplication.processEvents())
            
        attenuator_test_log.append(SPACE+"\n")
            
            
            
    else:
        sw2_port_1=3 
        sw2_port_2=4 
        tela_leds.ui.kled_ATENUADORES_TEST.setState(1)
        tela_leds.ui.kled_ATENUADORES_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led atenuadores",tela_leds.repaint())
        print("led atenuadores",QApplication.processEvents())
        att_sweep_result_3="Attenuator Sweep Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" --> Test not Performed"
        step_size_3 = "-"
        att_sweep_result_4="Attenuator Sweep Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" --> Test not Performed"
        step_size_4 = "-"
        #A linha abaixo serve para impedir que o teste de linearidade seja executado 
        #sem que o de atenuação tenha confirmado que o rffe está ok
        att_fail_3=1 
        att_fail_4=1
        att_aprovacao_1="Test Not Performed"
        att_aprovacao_2="Test Not Performed"
        att_aprovacao_3="Test Not Performed"
        att_aprovacao_4="Test Not Performed"
        
        print("Attenuator Sweep Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))
        
        #LOG INFO
        attenuator_test_log.append(SPACE)
        attenuator_test_log.append("Attenuators Sweep Test")
        attenuator_test_log.append("Attenuator Sweep Test FINAL RESULT: TEST NOT PERFORMED")
        attenuator_test_log.append(SPACE+"\n")

        
    #Variavel de Saida    
    att_res_val=[step_size_1,step_size_2,step_size_3,step_size_4]
    att_res_ap=[att_aprovacao_1,att_aprovacao_2,att_aprovacao_3,att_aprovacao_4]
    
    ################################################################  
 


    ################################################################    
    #RF switches test (NEW ONE) - OK

    #Porta 1-1 e 2-2
    if switch_dc_test_selection==True:
        tela_leds.ui.progressBar.setValue(0)
        tela_leds.ui.kled_RF_SWITCH_TEST.setState(1)
        tela_leds.ui.kled_RF_SWITCH_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led rf switch",tela_leds.repaint())
        print("led rf switch",QApplication.processEvents())
         
        #LOG INFO
        rf_switch_test_log.append(SPACE)
        rf_switch_test_log.append("RF Switches Test")
        rf_switch_test_log.append("Test configuration:")
        rf_switch_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        rf_switch_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        rf_switch_test_log.append("Network Analyzer - Power Level [dB]: "+str(pow_value))
        rf_switch_test_log.append("RFFE Attenuation [dB]: "+str(att_value))
        rf_switch_test_log.append("RF Switch 1 Position: " +str(sw1_port_1)+"-"+str(sw1_port_2))
        rf_switch_test_log.append("Type of data acquired: S21\n")
        rf_switch_test_log.append("Tolerance:")
        rf_switch_test_log.append("Lower Boundary Tolerance (abs)[dB]: "+ str(abs(switch_ref+switch_tol)))
        rf_switch_test_log.append("\nResult Info:\n")
        
        #Determinação da posição da frequência central
        if (s_parameter_test_selection==True):
            freq_central_position_check=0
            for i in range (0, len(freq_data)):
                print("Frequência Central encontrada!!!")
                if (freq_data[i]==center_freq):
                    freq_central_position=i
                    freq_central_position_check=freq_central_position_check+1
                    break
            if(freq_central_position_check==0):
                print("Frequência Central não encontrada!!!")
                freq_central_position=int(len(freq_data)/2+1)
        else:
            print("BUG!")
            freq_central_position="-"
         
        percentual=0
        fail_general_rf_switch=0

        sw2_port_1=1 
        sw2_port_2=2
                
        (rf_sw_result_1,rf_sw_result_values_1,rf_sw_result_2,rf_sw_result_values_2,
         rf_switch_test_log,rf_sw_fail_1, rf_sw_fail_2) = rf_switches_test(vna,sgen,rffe,
                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                           center_freq, freq_span, 
                                                                           pow_value, att_value,
                                                                           switch_ref,switch_tol,tela_leds,percentual,rf_switch_test_log,
                                                                           s_parameter_test_selection,
                                                                           s_parameter_data_ch11,s_parameter_data_ch22,
                                                                           freq_central_position)
        if(rf_sw_fail_1==1):
            print("Canal 1 do Front End com Falha no RF Switches")
            rf_sw_aprovacao_1="FAIL"
            fail_general_rf_switch=fail_general_rf_switch+1
        else:
            rf_sw_aprovacao_1="OK"
            
        if(rf_sw_fail_2==1):
            print("Canal 2 do Front End com Falha no RF Switches")
            rf_sw_aprovacao_2="FAIL"
            fail_general_rf_switch=fail_general_rf_switch+1
        else:
            rf_sw_aprovacao_2="OK"
    
    else:
        rf_sw_result_1="RF Switches Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": Test not Performed"
        rf_sw_result_values_1 = "-"
        rf_sw_result_2="RF Switches Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": Test not Performed"
        rf_sw_result_values_2 = "-"
        print("RF Switch Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2)) 
        rf_sw_aprovacao_1="Test Not Performed"
        rf_sw_aprovacao_2="Test Not Performed"

    #Porta 3-3 e 4-4
    if switch_dc_test_selection==True:

        percentual=50
        
        sw2_port_1=3 
        sw2_port_2=4

        (rf_sw_result_3,rf_sw_result_values_3,rf_sw_result_4,rf_sw_result_values_4,
         rf_switch_test_log,rf_sw_fail_3, rf_sw_fail_4) = rf_switches_test(vna,sgen,rffe,
                                                                         rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                         rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                         center_freq, freq_span, 
                                                                         pow_value, att_value,
                                                                         switch_ref,switch_tol,tela_leds,percentual,rf_switch_test_log,
                                                                         s_parameter_test_selection,
                                                                         s_parameter_data_ch33,s_parameter_data_ch44,
                                                                         freq_central_position)
    
        if(rf_sw_fail_3==1):
            print("Canal 3 do Front End com Falha no RF Switches")
            rf_sw_aprovacao_3="FAIL"
            fail_general_rf_switch=fail_general_rf_switch+1
        else:
            rf_sw_aprovacao_3="OK"

        if(rf_sw_fail_4==1):
            print("Canal 4 do Front End com Falha no RF Switches")
            rf_sw_aprovacao_4="FAIL"
            fail_general_rf_switch=fail_general_rf_switch+1
        else:
            rf_sw_aprovacao_4="OK"
            

        #Avaliação Final do Teste de RF Switches: Indicação no LED    
        if (fail_general_rf_switch!=0):
            print("Teste de RF Switches: Falha detectada")
            rf_switch_test_log.append("RF Switches Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_RF_SWITCH_TEST.setState(1)
            tela_leds.ui.kled_RF_SWITCH_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led rf switches",tela_leds.repaint())
            print("led rf switches",QApplication.processEvents())
            
        else:
            print("Teste de RF Switches: Passou em todos os canais")
            rf_switch_test_log.append("RF Switches Test FINAL RESULT: OK")
            tela_leds.ui.kled_RF_SWITCH_TEST.setState(1)
            tela_leds.ui.kled_RF_SWITCH_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led rf switches",tela_leds.repaint())
            print("led rf switches",QApplication.processEvents())
    
    
        rf_switch_test_log.append(SPACE+"\n")
    else:
        rf_sw_result_3="RF Switches Test Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": Test not Performed"
        rf_sw_result_values_3 = "-"
        rf_sw_result_4="RF Switches Test Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": Test not Performed"
        rf_sw_result_values_4 = "-"
        print("RF Switch Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2)) 

        rf_sw_aprovacao_1="Test Not Performed"
        rf_sw_aprovacao_2="Test Not Performed"
        rf_sw_aprovacao_3="Test Not Performed"
        rf_sw_aprovacao_4="Test Not Performed"

        #LOG INFO
        rf_switch_test_log.append(SPACE)
        rf_switch_test_log.append("RF Switches Test")
        rf_switch_test_log.append("RF Switches Test FINAL RESULT: TEST NOT PERFORMED")
        rf_switch_test_log.append(SPACE+"\n")

        tela_leds.ui.kled_RF_SWITCH_TEST.setState(1)
        tela_leds.ui.kled_RF_SWITCH_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led rf switch",tela_leds.repaint())
        print("led rf switch",QApplication.processEvents())

    #Variavel de Saida
    switch_dc_res_val=[rf_sw_result_values_1,rf_sw_result_values_2,rf_sw_result_values_3,rf_sw_result_values_4]
    switch_dc_res_ap=[rf_sw_aprovacao_1,rf_sw_aprovacao_2,rf_sw_aprovacao_3,rf_sw_aprovacao_4]
    ################################################################      


    ################################################################  
    #Frequency Response

    #Porta 1-1 e 2-2
    if freq_resp_test_selection==True:
        
        tela_leds.ui.progressBar.setValue(0)
        tela_leds.ui.kled_RESP_FREQ_TEST.setState(1)
        tela_leds.ui.kled_RESP_FREQ_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led resp freq",tela_leds.repaint())
        print("led resp freq",QApplication.processEvents())
        
        #Freq data
        freq_data=vna.get_frequency_data()
        step_bandwidth=freq_data[1]-freq_data[0]
        
        #LOG INFO
        freq_resp_test_log.append(SPACE)
        freq_resp_test_log.append("Frequency Response Test")
        freq_resp_test_log.append("Test configuration:")
        freq_resp_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        freq_resp_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        freq_resp_test_log.append("Network Analyzer - Start Bandwidth [Hz]: "+str(start_bandwidth))
        freq_resp_test_log.append("Network Analyzer - Stop Bandwidth [Hz]: "+str(stop_bandwidth))
        freq_resp_test_log.append("Network Analyzer - Step Bandwidth [Hz]: "+str(step_bandwidth))
        freq_resp_test_log.append("Network Analyzer - Power Level [dB]: "+str(pow_value))
        freq_resp_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
        freq_resp_test_log.append("RFFE Attenuation [dB]: "+str(att_value))
        freq_resp_test_log.append("RF Switch 1 Position: " +str(sw1_port_1)+"-"+str(sw1_port_2))
        freq_resp_test_log.append("Type of data acquired: S21\n")
        freq_resp_test_log.append("Tolerance:")
        freq_resp_test_log.append("Lower Boundary Tolerance [Reference Value] [dB]: "+ str(freq_res_ref+freq_res_tol_ref))
        freq_resp_test_log.append("Lower Boundary Tolerance [Varredura] [dB]: "+ str(-abs(freq_res_tol_var)))
        freq_resp_test_log.append("Upper Boundary Tolerance [Varredura] [dB]: "+ str(abs(freq_res_tol_var)))
        freq_resp_test_log.append("\nResult Info:\n")
        
        fail_general_freq_resp=0
        percentual=0
        
        sw2_port_1=1 
        sw2_port_2=2 
        (freq_resp_result_1,freq_resp_result_2,
         delta_1,delta_2,
         maximum_value_1,maximum_value_2,
         freq_maximum_1,freq_maximum_2,
         freq_resp_test_log,
         fail_1,fail_2)=frequency_response_test(vna,sgen,rffe,
                                                rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                center_freq, freq_span,
                                                pow_value, att_value,
                                                freq_res_ref,freq_res_tol_ref,freq_res_tol_var,
                                                start_bandwidth,stop_bandwidth,step_bandwidth,
                                                freq_resp_test_log,tela_leds,percentual,
                                                s_parameter_test_selection,
                                                s_parameter_data_ch11,s_parameter_data_ch22,
                                                freq_data)

        #Aprovação dos Testes
        if(fail_1!=0):
            fail_general_freq_resp=fail_general_freq_resp+1
            freq_resp_aprovacao_1="FAIL"
        else:
            freq_resp_aprovacao_1="OK"

        if(fail_2!=0):
            fail_general_freq_resp=fail_general_freq_resp+1
            freq_resp_aprovacao_2="FAIL"
        else:
            freq_resp_aprovacao_2="OK" 
                 
                 
        
    else:
        freq_resp_result_1="Frequency Response Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+": Test not Performed"
        freq_resp_result_2="Frequency Response Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+": Test not Performed"
        delta_1 = "-"
        delta_2 = "-"
        maximum_value_1="-"
        maximum_value_2="-"
        freq_maximum_1="-"
        freq_maximum_2="-"
        freq_resp_aprovacao_1="Test Not performed"
        freq_resp_aprovacao_2="Test Not performed"
        
        print("Frequency Response Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))

    #Porta 3-3 e 4-4
    if freq_resp_test_selection==True:
        
        percentual=50
        
        sw2_port_1=3 
        sw2_port_2=4
        (freq_resp_result_3,freq_resp_result_4,
         delta_3,delta_4,
         maximum_value_3,maximum_value_4,
         freq_maximum_3,freq_maximum_4,
         freq_resp_test_log,
         fail_3,fail_4)=frequency_response_test(vna,sgen,rffe,
                                                rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                center_freq, freq_span,
                                                pow_value, att_value,
                                                freq_res_ref,freq_res_tol_ref,freq_res_tol_var,
                                                start_bandwidth,stop_bandwidth,step_bandwidth,
                                                freq_resp_test_log,tela_leds,percentual,
                                                s_parameter_test_selection,
                                                s_parameter_data_ch11,s_parameter_data_ch22,
                                                freq_data)
         
        #Aprovação dos Testes
        if(fail_3!=0):
            fail_general_freq_resp=fail_general_freq_resp+1
            freq_resp_aprovacao_3="FAIL"
        else:
            freq_resp_aprovacao_3="OK"

        if(fail_4!=0):
            fail_general_freq_resp=fail_general_freq_resp+1
            freq_resp_aprovacao_4="FAIL"
        else:
            freq_resp_aprovacao_4="OK" 
    
        #Avaliação Final do Teste de Freq Resp: Indicação no LED    
        if (fail_general_freq_resp!=0):
            print("Teste de Freq Resp: Falha detectada")
            freq_resp_test_log.append("Frequency Response Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_RESP_FREQ_TEST.setState(1)
            tela_leds.ui.kled_RESP_FREQ_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led freq res",tela_leds.repaint())
            print("led freq res",QApplication.processEvents())
        
        else:
            print("Teste de Freq Resp: Passou em todos os canais")
            freq_resp_test_log.append("Frequency Response Test FINAL RESULT: OK")
            tela_leds.ui.kled_RESP_FREQ_TEST.setState(1)
            tela_leds.ui.kled_RESP_FREQ_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led freq res",tela_leds.repaint())
            print("led freq res",QApplication.processEvents())   
            
        freq_resp_test_log.append(SPACE+"\n")
    else:
        freq_resp_result_3="Frequency Response Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": Test not Performed"
        freq_resp_result_4="Frequency Response Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": Test not Performed"
        delta_3 = "-"
        delta_4 = "-"
        maximum_value_3="-"
        maximum_value_4="-"
        freq_maximum_3="-"
        freq_maximum_4="-"
        freq_resp_aprovacao_3="Test Not Performed"
        freq_resp_aprovacao_4="Test Not Performed"
        
        freq_resp_test_log.append(SPACE)
        freq_resp_test_log.append("Frequency Response Test")
        freq_resp_test_log.append("Frequency Response Test FINAL RESULT: TEST NOT PERFORMED")
        freq_resp_test_log.append(SPACE+"\n")
        
        #Atualização do Led
        tela_leds.ui.kled_RESP_FREQ_TEST.setState(1)
        tela_leds.ui.kled_RESP_FREQ_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led freq res",tela_leds.repaint())
        print("led freq res",QApplication.processEvents())
        
    #Variavel de saida
    freq_resp_res_val_freqmax=[freq_maximum_1,freq_maximum_2,freq_maximum_3,freq_maximum_4]
    freq_resp_res_val_max=[maximum_value_1,maximum_value_2,maximum_value_3,maximum_value_4]
    freq_resp_res_val_delta=[delta_1,delta_2,delta_3,delta_4]
    freq_resp_res_ap=[freq_resp_aprovacao_1,freq_resp_aprovacao_2,freq_resp_aprovacao_3,freq_resp_aprovacao_4]
    ################################################################  


    ################################################################     
    #Return Loss (NEW ONE) - OK

    #S11
    #Porta 1-1 e 2-2
    if ret_loss_test_selection==True:
        
        tela_leds.ui.progressBar.setValue(0)
        tela_leds.ui.kled_RETURN_LOSS_TEST.setState(1)
        tela_leds.ui.kled_RETURN_LOSS_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led ret loss",tela_leds.repaint())
        print("led ret loss",QApplication.processEvents())
        
        #Freq data
        freq_data=vna.get_frequency_data()
        step_bandwidth=freq_data[1]-freq_data[0]
        
        #LOG INFO
        ret_loss_test_log.append(SPACE)
        ret_loss_test_log.append("Return Loss Test")
        ret_loss_test_log.append("Test configuration:")
        ret_loss_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        ret_loss_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        ret_loss_test_log.append("Network Analyzer - Start Bandwidth [Hz]: "+str(start_bandwidth))
        ret_loss_test_log.append("Network Analyzer - Stop Bandwidth [Hz]: "+str(stop_bandwidth))
        ret_loss_test_log.append("Network Analyzer - Step Bandwidth [Hz]: "+str(step_bandwidth))
        ret_loss_test_log.append("Network Analyzer - Power Level [dB]: "+str(pow_value))
        ret_loss_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
        ret_loss_test_log.append("RFFE Attenuation [dB]: "+str(att_value))
        ret_loss_test_log.append("RF Switch 1 Position: " +str(sw1_port_1)+"-"+str(sw1_port_2))
        ret_loss_test_log.append("Type of data acquired: S11 e S22\n")
        ret_loss_test_log.append("Tolerance:")
        ret_loss_test_log.append("Tolerance S11 Test")
        ret_loss_test_log.append("Lower Boundary Tolerance [Reference Value] (abs)[dB]: "+ str(abs(ret_loss_s11_ref+ret_loss_s11_tol_ref)))
        ret_loss_test_log.append("Upper Boundary Tolerance [Reference Value] (real)[dB]: "+str(0.0))
        ret_loss_test_log.append("Tolerance S22 Test")
        ret_loss_test_log.append("Lower Boundary Tolerance [Reference Value] (abs)[dB]: "+ str(abs(ret_loss_s22_ref+ret_loss_s22_tol_ref)))
        ret_loss_test_log.append("Upper Boundary Tolerance [Reference Value] (real)[dB]: "+str(0.0))
        ret_loss_test_log.append("\nResult Info:\n")

        
        fail_general_ret_loss=0
        percentual=0
        
        ret_loss_test_log.append("Return Loss: S11 TEST")
        
        sw2_port_1=1 
        sw2_port_2=2     
        (ret_loss_result_1,ret_loss_result_2,
         maximum_value_1,maximum_value_2,
         minimum_value_1,minimum_value_2,
         ret_loss_test_log,
         fail_1,fail_2) = return_loss_test_s11(vna,sgen,rffe,
                                              rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                              rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                              center_freq, freq_span, 
                                              pow_value, att_value,
                                              ret_loss_s11_ref, ret_loss_s11_tol_ref,
                                              start_bandwidth,stop_bandwidth,step_bandwidth,
                                              ret_loss_test_log,percentual,
                                              s_parameter_test_selection,
                                              s_parameter_data_ch11,s_parameter_data_ch22,
                                              freq_data,tela_leds)
         
        #Aprovação dos Testes
        if(fail_1!=0):
            fail_general_ret_loss=fail_general_ret_loss+1
            ret_loss_aprovacao_1="FAIL"
        else:
            ret_loss_aprovacao_1="OK"

        if(fail_2!=0):
            fail_general_ret_loss=fail_general_ret_loss+1
            ret_loss_aprovacao_2="FAIL"
        else:
            ret_loss_aprovacao_2="OK" 

    else:
        ret_loss_result_1="Return Loss S11 Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+": Test not Performed"
        ret_loss_result_2="Return Loss S11 Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+": Test not Performed"
        #delta_1 = "-"
        #delta_2 = "-"
        maximum_value_1="-"
        maximum_value_2="-"
        minimum_value_1="-"
        minimum_value_2="-"
        ret_loss_aprovacao_1="Test Not performed"
        ret_loss_aprovacao_2="Test Not performed"
        
    #Porta 3-3 e 4-4
    if ret_loss_test_selection==True:
        
        percentual=25
        
        sw2_port_1=3 
        sw2_port_2=4    

        (ret_loss_result_3,ret_loss_result_4,
         maximum_value_3,maximum_value_4,
         minimum_value_3,minimum_value_4,
         ret_loss_test_log,
         fail_3,fail_4) = return_loss_test_s11(vna,sgen,rffe,
                                              rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                              rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                              center_freq, freq_span, 
                                              pow_value, att_value,
                                              ret_loss_s11_ref, ret_loss_s11_tol_ref,
                                              start_bandwidth,stop_bandwidth,step_bandwidth,
                                              ret_loss_test_log,percentual,
                                              s_parameter_test_selection,
                                              s_parameter_data_ch33,s_parameter_data_ch44,
                                              freq_data,tela_leds)
   
    
    
        #Aprovação dos Testes
        if(fail_3!=0):
            fail_general_ret_loss=fail_general_ret_loss+1
            ret_loss_aprovacao_3="FAIL"
        else:
            ret_loss_aprovacao_3="OK"

        if(fail_4!=0):
            fail_general_ret_loss=fail_general_ret_loss+1
            ret_loss_aprovacao_4="FAIL"
        else:
            ret_loss_aprovacao_4="OK" 
       
        #Avaliação Ret Loss S11:     
        if (fail_general_ret_loss!=0):
            print("Teste de Return Loss: Falha detectada")
            ret_loss_test_log.append("Return Loss Test S11: FAIL\n")
        else:
            print("Teste de Ret Loss: Passou em todos os canais")
            ret_loss_test_log.append("Return Loss Test S11: OK\n")
    
    else:
        ret_loss_result_3="Return Loss S11 Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": Test not Performed"
        ret_loss_result_4="Return Loss S11 Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": Test not Performed"
        #delta_3 = "-"
        #delta_4 = "-"
        maximum_value_3="-"
        maximum_value_4="-"
        minimum_value_3="-"
        minimum_value_4="-"
        ret_loss_aprovacao_3="Test Not Performed"
        ret_loss_aprovacao_4="Test Not Performed"
        ret_loss_test_log.append(SPACE)
        ret_loss_test_log.append("Return Loss Test")
        ret_loss_test_log.append("Return Loss Test S11 FINAL RESULT: TEST NOT PERFORMED")
        
    ret_loss_res_val_min_s11=[minimum_value_1,minimum_value_2,minimum_value_3,minimum_value_4]
    ret_loss_res_val_max_s11=[maximum_value_1,maximum_value_2,maximum_value_3,maximum_value_4]
    ret_loss_res_val_delta_s11=[delta_1,delta_2,delta_3,delta_4]
    ret_loss_res_ap_s11=[ret_loss_aprovacao_1,ret_loss_aprovacao_2,ret_loss_aprovacao_3,ret_loss_aprovacao_4]
  
    
    #S22   
    #Porta 1-1 e 2-2
    if ret_loss_test_selection==True:
        sw2_port_1=1 
        sw2_port_2=2     
        
        ret_loss_test_log.append("Return Loss: S22 TEST")
        
        percentual=50
        sw2_port_1=1 
        sw2_port_2=2  
    
        fail_general_ret_loss_part2=0
         
        (ret_loss_result_1,ret_loss_result_2,
         maximum_value_1,maximum_value_2,
         minimum_value_1,minimum_value_2,
         ret_loss_test_log,
         fail_1,fail_2) = return_loss_test_s22(vna,sgen,rffe,
                                               rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                               rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                               center_freq, freq_span, 
                                               pow_value, att_value,
                                               ret_loss_s22_ref, ret_loss_s22_tol_ref,
                                               start_bandwidth,stop_bandwidth,step_bandwidth,
                                               ret_loss_test_log,percentual,
                                               s_parameter_test_selection,
                                               s_parameter_data_ch11,s_parameter_data_ch22,
                                               freq_data,tela_leds)
         
        #Aprovação dos Testes
        if(fail_1!=0):
            fail_general_ret_loss_part2=fail_general_ret_loss_part2+1
            ret_loss_aprovacao_1="FAIL"
        else:
            ret_loss_aprovacao_1="OK"

        if(fail_2!=0):
            fail_general_ret_loss_part2=fail_general_ret_loss_part2+1
            ret_loss_aprovacao_2="FAIL"
        else:
            ret_loss_aprovacao_2="OK" 

    else:
        ret_loss_result_1="Return Loss S22 Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+": Test not Performed"
        ret_loss_result_2="Return Loss S22 Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+": Test not Performed"
        #delta_1 = "-"
        #delta_2 = "-"
        maximum_value_1="-"
        maximum_value_2="-"
        minimum_value_1="-"
        minimum_value_2="-"
        ret_loss_aprovacao_1="Test Not performed"
        ret_loss_aprovacao_2="Test Not performed"
        
    #Porta 3-3 e 4-4
    if ret_loss_test_selection==True:
        
        percentual=50
        
        sw2_port_1=3 
        sw2_port_2=4    

        percentual=75
        
        (ret_loss_result_3,ret_loss_result_4,
         maximum_value_3,maximum_value_4,
         minimum_value_3,minimum_value_4,
         ret_loss_test_log,
         fail_3,fail_4) = return_loss_test_s22(vna,sgen,rffe,
                                               rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                               rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                               center_freq, freq_span, 
                                               pow_value, att_value,
                                               ret_loss_s22_ref, ret_loss_s22_tol_ref,
                                               start_bandwidth,stop_bandwidth,step_bandwidth,
                                               ret_loss_test_log,percentual,
                                               s_parameter_test_selection,
                                               s_parameter_data_ch33,s_parameter_data_ch44,
                                               freq_data,tela_leds)
   
    
    
        #Aprovação dos Testes
        if(fail_3!=0):
            fail_general_ret_loss_part2=fail_general_ret_loss_part2+1
            ret_loss_aprovacao_3="FAIL"
        else:
            ret_loss_aprovacao_3="OK"

        if(fail_4!=0):
            fail_general_ret_loss_part2=fail_general_ret_loss_part2+1
            ret_loss_aprovacao_4="FAIL"
        else:
            ret_loss_aprovacao_4="OK" 

        #Avaliação Ret Loss S22:     
        if (fail_general_ret_loss_part2!=0):
            print("Teste de Return Loss: Falha detectada")
            ret_loss_test_log.append("Return Loss Test S22: FAIL")
        else:
            print("Teste de Ret Loss: Passou em todos os canais")
            ret_loss_test_log.append("Return Loss Test S22: OK")
    
        #Avaliação Final do Teste de Ret Loss: Indicação no LED    
        if ((fail_general_ret_loss+fail_general_ret_loss_part2)!=0):
            print("Teste de Return Loss: Falha detectada")
            ret_loss_test_log.append("Return Loss Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_RETURN_LOSS_TEST.setState(1)
            tela_leds.ui.kled_RETURN_LOSS_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led ret loss",tela_leds.repaint())
            print("led ret loss",QApplication.processEvents())
        
        else:
            print("Teste de Ret Loss: Passou em todos os canais")
            ret_loss_test_log.append("Return Loss Test FINAL RESULT: OK")
            tela_leds.ui.kled_RETURN_LOSS_TEST.setState(1)
            tela_leds.ui.kled_RETURN_LOSS_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led ret loss",tela_leds.repaint())
            print("led ret loss",QApplication.processEvents())  
                    
        ret_loss_test_log.append(SPACE+"\n") 
            
    else:
        ret_loss_result_3="Return Loss S22 Channel "+str(sw2_port_1)+ "-" + str(sw2_port_1)+": Test not Performed"
        ret_loss_result_4="Return Loss S22 Channel "+str(sw2_port_2)+ "-" + str(sw2_port_2)+": Test not Performed"
        #delta_3 = "-"
        #delta_4 = "-"
        maximum_value_3="-"
        maximum_value_4="-"
        minimum_value_3="-"
        minimum_value_4="-"
        ret_loss_test_log.append("Return Loss Test S22 FINAL RESULT: TEST NOT PERFORMED")
        ret_loss_test_log.append(SPACE+"\n")
        ret_loss_aprovacao_3="Test Not performed"
        ret_loss_aprovacao_4="Test Not performed"
        
        #Atualização do Led
        tela_leds.ui.kled_RETURN_LOSS_TEST.setState(1)
        tela_leds.ui.kled_RETURN_LOSS_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led ret loss",tela_leds.repaint())
        print("led ret loss",QApplication.processEvents())        

    #ret_loss_res_val_min_s22=[minimum_value_1,minimum_value_2,minimum_value_3,minimum_value_4]
    ret_loss_res_val_max_s22=[maximum_value_1,maximum_value_2,maximum_value_3,maximum_value_4]
    #ret_loss_res_val_delta_s22=[delta_1,delta_2,delta_3,delta_4]
    ret_loss_res_ap_s22=[ret_loss_aprovacao_1,ret_loss_aprovacao_2,ret_loss_aprovacao_3,ret_loss_aprovacao_4]
    ################################################################  


    ################################################################      
    #Power sweep 

    #Porta 1-1 e 2-2
    if linearidade_test_selection==True:
        
        tela_leds.ui.progressBar.setValue(0)
        tela_leds.ui.kled_LINEARIDADE_TEST.setState(1)
        tela_leds.ui.kled_LINEARIDADE_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led linearity",tela_leds.repaint())
        print("led linearity",QApplication.processEvents())
        
       #LOG INFO
        linearity_test_log.append(SPACE)
        linearity_test_log.append("Power Sweep (Linearity) Test")
        linearity_test_log.append("Test configuration:")
        linearity_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        linearity_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        linearity_test_log.append("Network Analyzer - Average Factor: 10")
        linearity_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
        linearity_test_log.append("RFFE Attenuation [dB]: "+str(att_value))
        linearity_test_log.append("Type of data acquired: S21\n")
        linearity_test_log.append("Tolerance:")
        linearity_test_log.append("Lower Boundary Tolerance [Reference Value] (abs)[dB]: "+ str(abs(linearity_ref-linearity_tol)))
        linearity_test_log.append("Upper Boundary Tolerance [Reference Value] (real)[dB]: "+str(abs(linearity_ref-linearity_tol)))
        linearity_test_log.append("\nResult Info:")

        #Determinação da posição da frequência central
        #Freq data
        freq_data=vna.get_frequency_data()
        
        
        freq_central_position_check=0
        for i in range (0, len(freq_data)):
            if (freq_data[i]==center_freq):
                print("Frequência Central encontrada!!!")
                freq_central_position=i
                freq_central_position_check=1
                break
        if(freq_central_position_check==0):
            print("Frequência Central não encontrada!!!")
            print("valor aqui:", int(len(freq_data)/2+1))
            print("valor aqui:",freq_data)
            freq_central_position=int(len(freq_data)/2+1)
        
        fail_general_linearity=0
        percentual=0
        
        sw2_port_1=1 
        sw2_port_2=2  


        (pow_sweep_result_1,pow_sweep_result_2,fail_1,fail_2)=power_sweep_test(vna,sgen,rffe,
                                                                                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                       center_freq, freq_span, 
                                                                                       pow_value, att_value,
                                                                                       pow_sweep_ini,pow_sweep_end,pow_sweep_step,
                                                                                       linearity_ref, linearity_tol,pow_sweep_correction_factor,
                                                                                       att_fail_1,att_fail_2,
                                                                                       tela_leds,percentual,linearity_test_log,
                                                                                       freq_central_position)
    
        if(fail_1!=0):
            aprovacao_1="FAILED"
            fail_general_linearity=fail_general_linearity+1
        else:
            aprovacao_1="OK"
        
        if(fail_2!=0):
            aprovacao_2="FAILED"
            fail_general_linearity=fail_general_linearity+1
        else:
            aprovacao_2="OK"
    
    
    else:
        lin_result_1="Linearity Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"        --> Test not Performed"
        lin_result_2="Linearity Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"        --> Test not Performed"
        pow_sweep_result_1 = "Data not acquired"
        pow_sweep_result_2 = "Data not acquired"
        print("Linearity Test Channel --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
    
    #Porta 3-3 e 4-4
    if linearidade_test_selection==True:
        
        percentual=50
        
        sw2_port_1=3 
        sw2_port_2=4  
        pow_sweep_result_3 = list()
        pow_sweep_result_4= list()
        (pow_sweep_result_3,pow_sweep_result_4,fail_3,fail_4)=power_sweep_test(vna,sgen,rffe,
                                                                                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                       center_freq, freq_span, 
                                                                                       pow_value, att_value,
                                                                                       pow_sweep_ini,pow_sweep_end,pow_sweep_step,
                                                                                       linearity_ref, linearity_tol,pow_sweep_correction_factor,
                                                                                       att_fail_3,att_fail_4,
                                                                                       tela_leds,percentual,linearity_test_log,
                                                                                       freq_central_position)
    
        
        if(fail_3!=0):
            aprovacao_3="FAILED"
            fail_general_linearity=fail_general_linearity+1
        else:
            aprovacao_3="OK"
        
        if(fail_4!=0):
            aprovacao_4="FAILED"
            fail_general_linearity=fail_general_linearity+1
        else:
            aprovacao_4="OK"
            

        #Avaliação Final do Teste de Linearidade: Indicação no LED    
        if (fail_general_linearity!=0):
            print("Teste de Linearidade: Falha detectada")
            linearity_test_log.append("Linearity Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_LINEARIDADE_TEST.setState(1)
            tela_leds.ui.kled_LINEARIDADE_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led linearity",tela_leds.repaint())
            print("led linearity",QApplication.processEvents())
        
        else:
            print("Teste de Linearidade: Passou em todos os canais")
            linearity_test_log.append("Linearity Test FINAL RESULT: OK")
            tela_leds.ui.kled_LINEARIDADE_TEST.setState(1)
            tela_leds.ui.kled_LINEARIDADE_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led ret loss",tela_leds.repaint())
            print("led ret loss",QApplication.processEvents())  
        
        linearity_test_log.append(SPACE+"\n")     
    
    else:
        lin_result_3="Linearity Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"        --> Test not Performed"
        lin_result_4="Linearity Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"        --> Test not Performed"
        pow_sweep_result_3 = "Data not acquired"
        pow_sweep_result_4 = "Data not acquired"
        print("Linearity Test Channel --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
        
        aprovacao_1="Test Not Performed"
        aprovacao_2="Test Not Performed"
        aprovacao_3="Test Not Performed"
        aprovacao_4="Test Not Performed"
        
        linearity_test_log.append(SPACE)
        linearity_test_log.append("Power Sweep (Linearity) Test")
        linearity_test_log.append("Linearity Test FINAL RESULT: TEST NOT PERFORMED")
        linearity_test_log.append(SPACE+"\n")
        
        tela_leds.ui.kled_LINEARIDADE_TEST.setState(1)
        tela_leds.ui.kled_LINEARIDADE_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led ret loss",tela_leds.repaint())
        print("led ret loss",QApplication.processEvents()) 
        
    linearity_res_val=[pow_sweep_result_1,pow_sweep_result_2,pow_sweep_result_3,pow_sweep_result_4]
    linearity_res_ap=[aprovacao_1,aprovacao_2,aprovacao_3,aprovacao_4]
    
    ################################################################  


    ################################################################  
    #Crosstalk test (NEW ONE) -OK

    #Porta 1-1 e 2-2
    if crosstalk_test_selection==True:
        
        tela_leds.ui.progressBar.setValue(0)
        tela_leds.ui.kled_CROSSTALK_TEST.setState(1)
        tela_leds.ui.kled_CROSSTALK_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led xtalk",tela_leds.repaint())
        print("led xtalk",QApplication.processEvents())
        
        #Freq data
        freq_data=vna.get_frequency_data()
        step_bandwidth=freq_data[1]-freq_data[0]
        
        #LOG INFO
        crosstalk_test_log.append(SPACE)
        crosstalk_test_log.append("Crosstalk Test Test")
        crosstalk_test_log.append("Test configuration:")
        crosstalk_test_log.append("Network Analyzer - Center Frequency [Hz]: "+str(center_freq))
        crosstalk_test_log.append("Network Analyzer - Span Frequency [Hz]: "+str(freq_span))
        crosstalk_test_log.append("Network Analyzer - Start Bandwidth [Hz]: "+str(start_bandwidth))
        crosstalk_test_log.append("Network Analyzer - Stop Bandwidth [Hz]: "+str(stop_bandwidth))
        crosstalk_test_log.append("Network Analyzer - Step Bandwidth [Hz]: "+str(step_bandwidth))
        crosstalk_test_log.append("Network Analyzer - Power Level [dB]: "+str(pow_value))
        crosstalk_test_log.append("Waveform Generator - DC Offset [V]: "+str(3.0))
        crosstalk_test_log.append("RFFE Attenuation [dB]: "+str(att_value))
        crosstalk_test_log.append("RF Switch 1 Position: " +str(sw1_port_1)+"-"+str(sw1_port_2))
        crosstalk_test_log.append("Type of data acquired: S21\n")
        crosstalk_test_log.append("Tolerance:")
        crosstalk_test_log.append("Lower Boundary Tolerance [Reference Value] (abs) [dB]: "+ str(abs(xtalk_ref+xtalk_tol_ref)))
        crosstalk_test_log.append("\nResult Info:\n")
        
        fail_general_crosstalk=0
        
        percentual=0
        
        sw2_port_1=1 
        sw2_port_2=2  
        (maximum_value12,maximum_value21,fail_12,fail_21)=crosstalk_test(vna,sgen,rffe,
                                                                     rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                     rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                     center_freq, freq_span, 
                                                                     pow_value, att_value,
                                                                     xtalk_ref,xtalk_tol_ref,
                                                                     start_bandwidth,stop_bandwidth,
                                                                     crosstalk_test_log,percentual,tela_leds,
                                                                     s_parameter_test_selection,
                                                                     s_parameter_data_ch11,s_parameter_data_ch22,
                                                                     s_parameter_data_ch12,s_parameter_data_ch21,
                                                                     freq_data)
        
        if(fail_12!=0):
            aprovacao_12="FAILED"
            fail_general_crosstalk=fail_general_crosstalk+1
        else:
            aprovacao_12="OK"

        if(fail_21!=0):
            aprovacao_21="FAILED"
            fail_general_crosstalk=fail_general_crosstalk+1
        else:
            aprovacao_21="OK"

    else:
        xtalk_result_12 = "Data not acquired for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2)
        maximum_value12="-"
        maximum_value21="-"
        fail_12="Test Not Performed"
        fail_21="Test Not Performed"
        
        print("Crosstalk Test --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
    
    #Porta 3-3 e 4-4
    if crosstalk_test_selection==True:
        
        percentual=50
        
        sw2_port_1=3 
        sw2_port_2=4  

        (maximum_value34,maximum_value43,fail_34,fail_43)=crosstalk_test(vna,sgen,rffe,
                                                                     rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                     rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                     center_freq, freq_span, 
                                                                     pow_value, att_value,
                                                                     xtalk_ref,xtalk_tol_ref,
                                                                     start_bandwidth,stop_bandwidth,
                                                                     crosstalk_test_log,percentual,tela_leds,
                                                                     s_parameter_test_selection,
                                                                     s_parameter_data_ch33,s_parameter_data_ch44,
                                                                     s_parameter_data_ch34,s_parameter_data_ch43,
                                                                     freq_data)
    
        if(fail_34!=0):
            aprovacao_34="FAILED"
            fail_general_crosstalk=fail_general_crosstalk+1
        else:
            aprovacao_34="OK"

        if(fail_43!=0):
            aprovacao_43="FAILED"
            fail_general_crosstalk=fail_general_crosstalk+1
        else:
            aprovacao_43="OK"
            
        #Avaliação Final do Teste de Ret Loss: Indicação no LED    
        if (fail_general_crosstalk!=0):
            print("Teste de Crosstalk: Falha detectada")
            crosstalk_test_log.append("Crosstalk Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_CROSSTALK_TEST.setState(1)
            tela_leds.ui.kled_CROSSTALK_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led xtalk",tela_leds.repaint())
            print("led xtalk",QApplication.processEvents())
        
        else:
            print("Teste de Crosstalk: Passou em todos os canais")
            crosstalk_test_log.append("Crosstalk Test FINAL RESULT: OK")
            tela_leds.ui.kled_CROSSTALK_TEST.setState(1)
            tela_leds.ui.kled_CROSSTALK_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led xtalk",tela_leds.repaint())
            print("led xtalk",QApplication.processEvents())  
                    
        crosstalk_test_log.append(SPACE+"\n") 
            
    
    
    else:
        xtalk_result_34 = "Data not acquired for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2)
        print("Crosstalk Test --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
        maximum_value34="-"
        maximum_value43="-"
        aprovacao_12="Test Not Performed"
        aprovacao_21="Test Not Performed"
        aprovacao_34="Test Not Performed"
        aprovacao_43="Test Not Performed"

        crosstalk_test_log.append(SPACE)
        crosstalk_test_log.append("Crosstalk Test")
        crosstalk_test_log.append("Crosstalk Test FINAL RESULT: TEST NOT PERFORMED")
        crosstalk_test_log.append(SPACE+"\n")
        
        tela_leds.ui.kled_CROSSTALK_TEST.setState(1)
        tela_leds.ui.kled_CROSSTALK_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led xtalk",tela_leds.repaint())
        print("led xtalk",QApplication.processEvents())         
        
        
        
    crosstalk_res_val=[maximum_value12,maximum_value21,maximum_value34,maximum_value43]
    crosstalk_res_ap=[aprovacao_12,aprovacao_21,aprovacao_34,aprovacao_43]    

   
    ################################################################  


    ################################################################    
    #Temperature Test (NEW ONE) - OK
    if temp_test_selection==True:
        
        
        tela_leds.ui.progressBar.setValue(0)
        tela_leds.ui.kled_TEMPERATURE_TEST.setState(1)
        tela_leds.ui.kled_TEMPERATURE_TEST.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led temp",tela_leds.repaint())
        print("led temp",QApplication.processEvents())
        
       #LOG INFO
        temperature_test_log.append(SPACE)
        temperature_test_log.append("Temperature Measurement Test")
        temperature_test_log.append("Test configuration:")
        temperature_test_log.append("Type of data acquired: Temperature\n")
        temperature_test_log.append("Tolerance:")
        temperature_test_log.append("Lower Boundary Tolerance [Reference Value] [°C]: "+ str(temp_min))
        temperature_test_log.append("Upper Boundary Tolerance [Reference Value] [°C]: "+str(temp_max))
        temperature_test_log.append("\nResult Info:")

        (temperature,temperature_test_log,fail)=temperature_test(rffe,temp_min,temp_max,temperature_test_log,tela_leds)

        if(fail!=0):
            temp_aprovacao="FAILED"
            print("Teste de Temperatura: Falha detectada")
            temperature_test_log.append("Temperature Measurement Test FINAL RESULT: FAIL")
            tela_leds.ui.kled_TEMPERATURE_TEST.setState(1)
            tela_leds.ui.kled_TEMPERATURE_TEST.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led temp",tela_leds.repaint())
            print("led temp",QApplication.processEvents())  
                    
        
        else:
            temp_aprovacao="OK"
            print("Teste de Temperatura: OK")
            temperature_test_log.append("Temperature Measurement Test FINAL RESULT: OK")
            tela_leds.ui.kled_TEMPERATURE_TEST.setState(1)
            tela_leds.ui.kled_TEMPERATURE_TEST.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print("led temp",tela_leds.repaint())
            print("led temp",QApplication.processEvents())   
            
        temperature_test_log.append(SPACE+"\n")
    else:
        tela_leds.ui.kled_TEMPERATURE_TEST.setState(1)
        tela_leds.ui.kled_TEMPERATURE_TEST.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("led temp",tela_leds.repaint())
        print("led temp",QApplication.processEvents())  
        temp_test="Temperature Measurement Test: Test not Performed"
        temperature = ["-","-","-","-","-"]
        print("Temperature Test: Test not Performed")
        temperature_test_log.append(SPACE)
        temperature_test_log.append("Temperature Measurement Test")
        temperature_test_log.append("Temperature Measurement Test FINAL RESULT: TEST NOT PERFORMED")
        temperature_test_log.append(SPACE+"\n")
        temp_aprovacao="Test not Performed"
            
    temperature_res_val=temperature
    temperature_res_ap=temp_aprovacao  
    
    ################################################################      

    sw_version="RFFE Software Version: " +str(rffe.get_software_version())

    #Print the test result in the txt file
    #test_result=([current_time],[att_sweep_resultA],[att_sweep_resultB],[rf_sw_result],[freq_resp_resultA],[freq_resp_resultB],[return_loss_resultA],[return_loss_resultB],[xtalk_resp_resultA],[xtalk_resp_resultB],[lin_resultA],[lin_resultB],[temp_test])
    #test_lib.list_to_file(0,test_result,datapath_save + serial_number + "_result.txt")

    #print metadata with the correct filename
    #shutil.copy2(metadata_path,datapath_save+serial_number+"_metadata.txt")

    #print test result values with the correct filename
    #test_result_values=([current_time],[sw_version],[att_sweep_resultA],[step_sizeA],[att_sweep_resultB],[step_sizeB],[rf_sw_result],[s21_sw_result],[freq_resp_resultA],[freq_resp_resultB],[s21_freq_resp],[return_loss_resultA],[return_loss_resultB],[s11_freq_resp],[lin_resultA],[pow_sweep_resultA],[lin_resultB],[pow_sweep_resultB],[xtalk_resp_resultA],[xtalk_resp_resultB],[xtalk_result],[temp_test],[temperature])
    sw_version="RFFE Software Version: " +str(rffe.get_software_version().decode("utf-8"))


    print("\nTest finished!")

    ##Close ethernet connection
    vna.close_connection()
    rffe.close_connection()
    rfsw_1.close_connection()
    rfsw_2.close_connection()
    sgen.close_connection()
    
    #Horario Final do Teste
    stop_time_general=datetime.datetime.now()
    stop_time_general_str=start_time_general.strftime("%d-%m-%Y %H:%M:%S")
    stop_qt_time=QDateTime.currentDateTime()
    
    #Duracao do Teste
    duracao_teste_general=((stop_time_general - start_time_general).total_seconds())/60
    duracao_teste_general_str=str(round(duracao_teste_general,4))
    
    #LOG INFO
    set_up_log.append("TESTE DA PLACA: RFFE\n")
    set_up_log.append("Operador: "+str(rffe_operador))
    set_up_log.append("Numero de Serie: "+str(rffe_serie))
    set_up_log.append(sw_version)
    set_up_log.append(rffe_str_msg_communication[0])
    set_up_log.append(rffe_str_msg_communication[1])
    set_up_log.append("Start Time: "+start_time_general_str)
    set_up_log.append("End Time: "+stop_time_general_str)
    set_up_log.append("Duracao do Teste: "+duracao_teste_general_str+" min\n")
    set_up_log.append("Set-up Info:")
    set_up_log.append("Network Analyzer Model: "+network_model)
    set_up_log.append(vna_str_msg_communication[0])
    set_up_log.append(vna_str_msg_communication[1])
    set_up_log.append("Waveform Generator Model: "+waveform_model)
    set_up_log.append(sgen_str_msg_communication[0])
    set_up_log.append(sgen_str_msg_communication[1])
    set_up_log.append("RF Switch Model: "+rf_switch_model)
    set_up_log.append(rfsw_1_str_msg_communication[0])
    set_up_log.append(rfsw_1_str_msg_communication[1])
    set_up_log.append(rfsw_2_str_msg_communication[0])
    set_up_log.append(rfsw_2_str_msg_communication[1])
    set_up_log.append("DC Power Supply Model: "+dc_power_model+"\n")
    set_up_log.append("RESULTS:\n")


    #LOG INFO: GERAL
    for i in range (0,len(set_up_log)):
        log_file_general.append(set_up_log[i])

    for i in range (0,len(s_parameter_test_log)):
        log_file_general.append(s_parameter_test_log[i])
        
    for i in range (0,len(attenuator_test_log)):
        log_file_general.append(attenuator_test_log[i])

    for i in range (0,len(rf_switch_test_log)):
        log_file_general.append(rf_switch_test_log[i])
    
    for i in range (0,len(freq_resp_test_log)):
        log_file_general.append(freq_resp_test_log[i])
       
    for i in range (0,len(ret_loss_test_log)):
        log_file_general.append(ret_loss_test_log[i])
        
    for i in range (0,len(linearity_test_log)):
        log_file_general.append(linearity_test_log[i])
        
    for i in range (0,len(crosstalk_test_log)):
        log_file_general.append(crosstalk_test_log[i])
        
    for i in range (0,len(temperature_test_log)):
        log_file_general.append(temperature_test_log[i])
        
    #LOG INFO: DATA DO S-PARAMETERS
    
    #CH1-1
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch11_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch11_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch11.txt")
    
    #CH1-2
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch12_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch12_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch12.txt")

    #CH2-1
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch21_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch21_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch21.txt")

    #CH2-2
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch22_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch22_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch22.txt")
        


    #CH3-3
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch33_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch33_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch33.txt")
    
    #CH3-4
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch34_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch34_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch34.txt")

    #CH4-3
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch43_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch43_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch43.txt")

    #CH4-4
    log_file_sparam_data_general=[]
    for i in range (0,len(set_up_log)):
        log_file_sparam_data_general.append(set_up_log[i])
    for i in range (0,len(s_parameter_data_ch44_log)):
        log_file_sparam_data_general.append(s_parameter_data_ch44_log[i])

    test_lib.list_to_file_aux(0,log_file_sparam_data_general,datapath_save_sparam + serial_number + "_sparam_ch44.txt")

    test_lib.list_to_file_aux(0,log_file_general,datapath_save + serial_number + "_result_general.txt")

    tela_leds.ui.progressBar.setValue(100) 
    tela_leds.repaint()
    QApplication.processEvents()
    print("led geral",tela_leds.repaint())
    print("led geral",QApplication.processEvents())


    return (s_param_res_ap,
            att_res_val,att_res_ap,
            switch_dc_res_val,switch_dc_res_ap,
            freq_resp_res_val_freqmax,freq_resp_res_val_max,freq_resp_res_val_delta,freq_resp_res_ap,
            ret_loss_res_val_max_s11 ,ret_loss_res_ap_s11,ret_loss_res_val_max_s22,ret_loss_res_ap_s22,
            linearity_res_val,linearity_res_ap,
            crosstalk_res_val,crosstalk_res_ap,
            temperature_res_val,temperature_res_ap,
            stop_qt_time)