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

from temperature_test import temperature_test
from crosstalk_test import crosstalk_test
from return_loss_test import return_loss_test_s11
from return_loss_test import return_loss_test_s22
from rf_switches_test import rf_switches_test
from frequency_response_test import frequency_response_test
from power_sweep_test import power_sweep_test
from attenuators_sweep_test import attenuators_sweep_test
from s_parameters_test import s_parameters_test


######################################
#Initialization example:
#python3 run_rffe_test.py 123456 /home/lnls-bpm/Desktop/test_report_bpm_hardware/rffe/rffe_test_metadata.txt /home/lnls-bpm/Desktop/test_report_bpm_hardware/rffe/test_evaluation

print("\n- Loading parameters\n- Instruments configuration\n...\n")
#rfsw_address
######################################
#inserir programa de leitura da camera
#serial_number=str(sys.argv[1])
serial_number="escolher algum novo de seriado"

#################################
#metadata_path=str(sys.argv[2])
metadata_path="rffe_test_metadata.txt"

#datapath_save=str(sys.argv[3])
datapath_save="result/"
######################################

##get current date and time
current_time=str(time.strftime("%c"))
current_day=str(time.strftime("%d-%m-%Y"))

try:
    os.makedirs(datapath_save + "sn_" + str(serial_number)+"/"+current_day)
except:
  pass

datapath_save=datapath_save + "sn_" + str(serial_number)+"/"+current_day+"/"

metadata_param=read_metadata.read_vars(metadata_path)

#Network Configuration
vna=AgilentE5061B(metadata_param['ip_vna'])
rfsw_1=RF_switch_board_1(metadata_param['ip_sw1'])
rfsw_2=RF_switch_board_2(metadata_param['ip_sw2'])
rffe=RFFEControllerBoard(metadata_param['ip_rffe'])
sgen=Agilent33521A(metadata_param['ip_sgen'])

#Configuração das portas de acesso padrão do Switch

#Switch 1 
# 0 = Desliga canal
# 1 = Set de 5dB de ganho
# 2 = Set de 1dB de ganho
# 3 = Set de 0dB de ganho

sw1_port_1=3 #(0, 1, 2 ou 3) 
sw1_port_2=sw1_port_1 #(0, 1, 2 ou 3) #mudar este valor serve apenas para teste
#Este teste inteiro é realizado com o switch 1 ligado em 0dB. Não mudar este valor.

#Switch 2 
# 0 = Desliga canal
# 1 = Liga canal 1
# 2 = Liga canal 2
# 3 = Liga canal 3
# 4 = Liga canal 4

sw2_port_1=3 #(0, 1, 2, 3 e 4)
sw2_port_2=4 #(0, 1, 2, 3 e 4)

print("Network/LAN configuration - ok!\n...\n")

#Constants data acquisition

ip_sw1 = metadata_param['ip_sw1']
ip_sw2 = metadata_param['ip_sw2']
pow_value=float(metadata_param['pow_value'])
center_freq=int(metadata_param['freq_center'])
freq_span=int(metadata_param['freq_span'])
freq_start=int(metadata_param['freq_start'])
freq_stop=int(metadata_param['freq_stop'])

att_value=float(metadata_param['att_value'])
pow_value=float(metadata_param['pow_value'])
n_points=int(float(metadata_param['n_points']))
xtalk_ref=float(metadata_param['xtalk_ref'])
xtalk_tol=float(metadata_param['xtalk_tolerance'])
center_freq=int(metadata_param['freq_center'])
freq_span=int(metadata_param['freq_span'])
att_step=float(metadata_param['att_sweep_step'])
pow_sweep_ini=float(metadata_param['pow_sweep_ini'])
pow_sweep_end=float(metadata_param['pow_sweep_end'])
pow_sweep_att=float(metadata_param['pow_sweep_att'])
pow_sweep_step=float(metadata_param['pow_sweep_step'])
att_sweep_low=float(metadata_param['att_sweep_low'])
att_sweep_high=float(metadata_param['att_sweep_high'])
att_step_tol=float(metadata_param['att_step_tol'])
temp_min=float(metadata_param['temp_min'])
temp_max=float(metadata_param['temp_max'])
linearity_tol=float(metadata_param['linearity_tol'])
pow_sweep_correction_factor=float(metadata_param['pow_sweep_cor_fac'])
start_bandwidth=float(metadata_param['start_bandwidth'])
stop_bandwidth=float(metadata_param['stop_bandwidth'])
step_bandwidth=float(metadata_param['step_bandwidth'])

#Quando att_fail = 0, o teste de atenuação é considerado como OK e podemos prosseguir para realizar o teste de linearidade
att_fail_1 = 1
att_fail_2 = 1
att_fail_3 = 0
att_fail_4 = 0

s11_ref=float(metadata_param['s11_ref'])
s12_ref=float(metadata_param['s12_ref'])
s21_ref=float(metadata_param['s21_ref'])
s22_ref=float(metadata_param['s22_ref'])
s11_tol=float(metadata_param['s11_tolerance'])
s12_tol=float(metadata_param['s12_tolerance'])
s21_tol=float(metadata_param['s21_tolerance'])
s22_tol=float(metadata_param['s22_tolerance'])

print("Test parameters loaded from metadata - ok!\n...\n")

#Configuração Inicial de Segurança
rffe.set_attenuator_value(att_value)
sgen.set_signal_DC()
sgen.set_pos("direct")
vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 
test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
rfsw_1.sw1_pos(ip_sw1,sw1_port_1,sw1_port_1)
rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1)

print("Set-up Configuration - Ok\n...")

################################################################  
#S-Parameters test (NEW ONE) - OK
if metadata_param['s_parameters_test']=="run":
    sw2_port_1=1 
    sw2_port_2=2 
    (sparam_12) = s_parameters_test(vna,sgen,rffe,
                                    rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                    rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                    center_freq, freq_span, freq_start, freq_stop,
                                    pow_value, att_value,
                                    serial_number,metadata_path,datapath_save)

    sw2_port_1=3 
    sw2_port_2=4 
    (sparam_34) = s_parameters_test(vna,sgen,rffe,
                                    rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                    rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                    center_freq, freq_span, freq_start, freq_stop,
                                    pow_value, att_value,
                                    serial_number,metadata_path,datapath_save)
    print("S-Parameters test - done")
else:
    print("S-Parameters test - choosed not to be performed")
################################################################  
   
  
################################################################   
#Attenuators sweep test (NEW ONE) - OK

#Porta 1-1 e 2-2
if metadata_param['att_sweep_test']=="run":
    sw2_port_1=1 
    sw2_port_2=2 
    step_size_1=list()
    step_size_2=list()
    (att_sweep_result_1,step_size_1,att_sweep_result_2,step_size_2,att_fail_1,att_fail_2) = attenuators_sweep_test(vna,sgen,rffe,
                                                                                                                   rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                   rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                   center_freq, freq_span, freq_start, freq_stop,
                                                                                                                   pow_value, att_value,
                                                                                                                   att_sweep_low,att_sweep_high,att_step,att_step_tol)
    if(att_fail_1==1):
        print("\nCanal 1 do Front End com Falha no Atenuador")
    if(att_fail_2==1):
        print("Canal 2 do Front End com Falha no Atenuador")
    
else:
    att_sweep_result_1="Attenuator Sweep Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" --> Test not Performed"
    step_size_1 = "Data not acquired"
    att_sweep_result_2="Attenuator Sweep Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" --> Test not Performed"
    step_size_2 = "Data not acquired"
    #A linha abaixo serve para impedir que o teste de linearidade seja executado 
    #sem que o de atenuação tenha confirmado que o rffe está ok
    att_fail_1=1 
    att_fail_2=1
    print("Attenuator Sweep Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))


#Porta 3-3 e 4-4
if metadata_param['att_sweep_test']=="run":
    sw2_port_1=3 
    sw2_port_2=4 
    step_size_3=list()
    step_size_4=list()
    (att_sweep_result_3,step_size_3,att_sweep_result_4,step_size_4,att_fail_3,att_fail_4) = attenuators_sweep_test(vna,sgen,rffe,
                                                                                                                   rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                   rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                   center_freq, freq_span, freq_start, freq_stop,
                                                                                                                   pow_value, att_value,
                                                                                                                   att_sweep_low,att_sweep_high,att_step,att_step_tol)
    if(att_fail_3==1):
        print("\nCanal 3 do Front End com Falha no Atenuador")
    if(att_fail_4==1):
        print("Canal 4 do Front End com Falha no Atenuador")
else:
    att_sweep_result_3="Attenuator Sweep Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" --> Test not Performed"
    step_size_3 = "Data not acquired"
    att_sweep_result_4="Attenuator Sweep Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" --> Test not Performed"
    step_size_4 = "Data not acquired"
    #A linha abaixo serve para impedir que o teste de linearidade seja executado 
    #sem que o de atenuação tenha confirmado que o rffe está ok
    att_fail_3=1 
    att_fail_4=1
    print("Attenuator Sweep Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))
    
################################################################  
 

################################################################    
#RF switches test (NEW ONE) - OK

#Porta 1-1 e 2-2
if metadata_param['sw_test']=="run":
    sw2_port_1=1 
    sw2_port_2=2
    (rf_sw_result_1,rf_sw_result_values_1,rf_sw_result_2,rf_sw_result_values_2) = rf_switches_test(vna,sgen,rffe,
                                                                                                   rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                   rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                   center_freq, freq_span, freq_start, freq_stop,
                                                                                                   pow_value, att_value,
                                                                                                   xtalk_ref)
else:
    rf_sw_result_1="RF Switches Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" --> Test not Performed"
    rf_sw_result_values_1 = "Data not acquired"
    rf_sw_result_2="RF Switches Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" --> Test not Performed"
    rf_sw_result_values_2 = "Data not acquired"
    print("RF Switch Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2)) 

#Porta 3-3 e 4-4
if metadata_param['sw_test']=="run":
    sw2_port_1=3 
    sw2_port_2=4
    (rf_sw_result_3,rf_sw_result_values_3,rf_sw_result_4,rf_sw_result_values_4) = rf_switches_test(vna,sgen,rffe,
                                                                                                   rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                   rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                   center_freq, freq_span, freq_start, freq_stop,
                                                                                                   pow_value, att_value,
                                                                                                   xtalk_ref)
else:
    rf_sw_result_3="RF Switches Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" --> Test not Performed"
    rf_sw_result_values_3 = "Data not acquired"
    rf_sw_result_4="RF Switches Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" --> Test not Performed"
    rf_sw_result_values_4 = "Data not acquired"
    print("RF Switch Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2)) 
################################################################      


################################################################  
#Frequency Response (NEW ONE) -OK

#Porta 1-1 e 2-2
if metadata_param['freq_response']=="run":
    sw2_port_1=1 
    sw2_port_2=2 
    (freq_resp_result_1,freq_resp_result_2,freq_resp_result_values_1,freq_resp_result_values_2)=frequency_response_test(vna,sgen,rffe,
                                                                                                                        rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                        rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                        center_freq, freq_span, freq_start, freq_stop,
                                                                                                                        pow_value, att_value,
                                                                                                                        s21_ref,s21_tol,
                                                                                                                        start_bandwidth,stop_bandwidth,step_bandwidth)
else:
    freq_resp_result_1="Frequency Response Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"    --> Test not Performed"
    freq_resp_result_2="Frequency Response Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"    --> Test not Performed"
    freq_resp_result_values_1 = "Data not acquired"
    freq_resp_result_values_2 = "Data not acquired"
    print("Frequency Response Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))

#Porta 3-3 e 4-4
if metadata_param['freq_response']=="run":
    sw2_port_1=3 
    sw2_port_2=4
    (freq_resp_result_3,freq_resp_result_4,freq_resp_result_values_3,freq_resp_result_values_4)=frequency_response_test(vna,sgen,rffe,
                                                                                                                        rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                        rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                        center_freq, freq_span, freq_start, freq_stop,
                                                                                                                        pow_value, att_value,
                                                                                                                        s21_ref,s21_tol,
                                                                                                                        start_bandwidth,stop_bandwidth,step_bandwidth)
else:
    freq_resp_result_3="Frequency Response Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"    --> Test not Performed"
    freq_resp_result_4="Frequency Response Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"    --> Test not Performed"
    freq_resp_result_values_3 = "Data not acquired"
    freq_resp_result_values_4 = "Data not acquired"
    print("Frequency Response Test: Test not Performed for Channel "+str(sw2_port_1)+" - " +str(sw2_port_2))
################################################################  


################################################################     
#Return Loss (NEW ONE) - OK

#S11
#Porta 1-1 e 2-2
if metadata_param['return_loss']=="run":
    sw2_port_1=1 
    sw2_port_2=2     
    (return_loss_result_1_11, return_loss_result_value_1_11,return_loss_result_2_11, return_loss_result_value_2_11) = return_loss_test_s11(vna,sgen,rffe,
                                                                                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                                           center_freq, freq_span, freq_start, freq_stop,
                                                                                                                                           pow_value, att_value,
                                                                                                                                           s11_ref, s11_tol,
                                                                                                                                           start_bandwidth,stop_bandwidth,step_bandwidth)
else:
    return_loss_result_1_11="Return Loss Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"           --> Test not Performed"
    return_loss_result_2_11="Return Loss Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"           --> Test not Performed"
    return_loss_result_value_1_11 = "Data not acquired"
    return_loss_result_value_2_11 = "Data not acquired"
    print("Return Loss Test: Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))

#Porta 3-3 e 4-4
if metadata_param['return_loss']=="run":
    sw2_port_1=3 
    sw2_port_2=4    
    (return_loss_result_3_11, return_loss_result_value_3_11,return_loss_result_4_11, return_loss_result_value_4_11) = return_loss_test_s11(vna,sgen,rffe,
                                                                                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                                           center_freq, freq_span, freq_start, freq_stop,
                                                                                                                                           pow_value, att_value,
                                                                                                                                           s11_ref, s11_tol,
                                                                                                                                           start_bandwidth,stop_bandwidth,step_bandwidth)
else:
    return_loss_result_3_11="Return Loss Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"           --> Test not Performed"
    return_loss_result_4_11="Return Loss Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"           --> Test not Performed"
    return_loss_result_value_3_11 = "Data not acquired"
    return_loss_result_value_4_11 = "Data not acquired"
    print("Return Loss Test: Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
   
    
#S22   
#Porta 1-1 e 2-2
if metadata_param['return_loss']=="run":
    sw2_port_1=1 
    sw2_port_2=2     
    (return_loss_result_1_22, return_loss_result_value_1_22,return_loss_result_2_22, return_loss_result_value_2_22) = return_loss_test_s22(vna,sgen,rffe,
                                                                                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                                           center_freq, freq_span, freq_start, freq_stop,
                                                                                                                                           pow_value, att_value,
                                                                                                                                           s22_ref, s22_tol,
                                                                                                                                           start_bandwidth,stop_bandwidth,step_bandwidth)
else:
    return_loss_result_1_22="Return Loss Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"           --> Test not Performed"
    return_loss_result_2_22="Return Loss Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"           --> Test not Performed"
    return_loss_result_value_1_22 = "Data not acquired"
    return_loss_result_value_2_22 = "Data not acquired"
    print("Return Loss Test: Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))

#Porta 3-3 e 4-4
if metadata_param['return_loss']=="run":
    sw2_port_1=3 
    sw2_port_2=4    
    (return_loss_result_3_22, return_loss_result_value_3_22,return_loss_result_4_22, return_loss_result_value_4_22) = return_loss_test_s22(vna,sgen,rffe,
                                                                                                                                           rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                                                           rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                                                           center_freq, freq_span, freq_start, freq_stop,
                                                                                                                                           pow_value, att_value,
                                                                                                                                           s22_ref, s22_tol,
                                                                                                                                           start_bandwidth,stop_bandwidth,step_bandwidth)
else:
    return_loss_result_3_22="Return Loss Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"           --> Test not Performed"
    return_loss_result_4_22="Return Loss Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"           --> Test not Performed"
    return_loss_result_value_3_22 = "Data not acquired"
    return_loss_result_value_4_22 = "Data not acquired"
    print("Return Loss Test: Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
    
    
################################################################  


################################################################      
#Power sweep (NEW ONE) - OK

#Porta 1-1 e 2-2
if metadata_param['power_sweep']=="run":
    sw2_port_1=1 
    sw2_port_2=2  
    pow_sweep_result_1 = list()
    pow_sweep_result_2= list()
    (lin_result_1,lin_result_2,pow_sweep_result_1,pow_sweep_result_2)=power_sweep_test(vna,sgen,rffe,
                                                                                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                       center_freq, freq_span, freq_start, freq_stop,
                                                                                       pow_value, att_value,
                                                                                       pow_sweep_att,pow_sweep_ini,pow_sweep_end,pow_sweep_step,linearity_tol,pow_sweep_correction_factor,
                                                                                       att_fail_1,att_fail_2)
else:
    lin_result_1="Linearity Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"        --> Test not Performed"
    lin_result_2="Linearity Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"        --> Test not Performed"
    pow_sweep_result_1 = "Data not acquired"
    pow_sweep_result_2 = "Data not acquired"
    print("Linearity Test Channel --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
    
#Porta 3-3 e 4-4
if metadata_param['power_sweep']=="run":
    sw2_port_1=3 
    sw2_port_2=4  
    pow_sweep_result_3 = list()
    pow_sweep_result_4= list()
    (lin_result_3,lin_result_4,pow_sweep_result_3,pow_sweep_result_4)=power_sweep_test(vna,sgen,rffe,
                                                                                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                       center_freq, freq_span, freq_start, freq_stop,
                                                                                       pow_value, att_value,
                                                                                       pow_sweep_att,pow_sweep_ini,pow_sweep_end,pow_sweep_step,linearity_tol,pow_sweep_correction_factor,
                                                                                       att_fail_3,att_fail_4)
else:
    lin_result_3="Linearity Test Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"        --> Test not Performed"
    lin_result_4="Linearity Test Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"        --> Test not Performed"
    pow_sweep_result_3 = "Data not acquired"
    pow_sweep_result_4 = "Data not acquired"
    print("Linearity Test Channel --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
################################################################  


################################################################  
#Crosstalk test (NEW ONE) -OK

#Porta 1-1 e 2-2
if metadata_param['xtalk']=="run":
    sw2_port_1=1 
    sw2_port_2=2  
    xtalk_result_12=list()
    (xtalk_resp_result_1, xtalk_resp_result_2, xtalk_result_12,result_ch_1,result_ch_2)=crosstalk_test(vna,sgen,rffe,
                                                                                                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                       center_freq, freq_span, freq_start, freq_stop,
                                                                                                       pow_value, att_value,
                                                                                                       xtalk_ref,xtalk_tol)
else:
    xtalk_resp_result_1="Crosstalk Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"             --> Test not Performed"
    xtalk_resp_result_2="Crosstalk Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"             --> Test not Performed"
    xtalk_result_12 = "Data not acquired for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2)
    print("Crosstalk Test --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
    
#Porta 3-3 e 4-4
if metadata_param['xtalk']=="run":
    sw2_port_1=3 
    sw2_port_2=4  
    xtalk_result_34=list()
    (xtalk_resp_result_3, xtalk_resp_result_4, xtalk_result_34,result_ch_3,result_ch_4)=crosstalk_test(vna,sgen,rffe,
                                                                                                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                                                                                                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                                                                                                       center_freq, freq_span, freq_start, freq_stop,
                                                                                                       pow_value, att_value,
                                                                                                       xtalk_ref,xtalk_tol)
else:
    xtalk_resp_result_3="Crosstalk Channel "+str(sw2_port_1)+ " - " + str(sw2_port_1)+"             --> Test not Performed"
    xtalk_resp_result_4="Crosstalk Channel "+str(sw2_port_2)+ " - " + str(sw2_port_2)+"             --> Test not Performed"
    xtalk_result_34 = "Data not acquired for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2)
    print("Crosstalk Test --> Test not Performed for Channel "+str(sw2_port_1)+ " - " + str(sw2_port_2))
################################################################  


################################################################    
#Temperature Test (NEW ONE) - OK
if metadata_param['temp']=="run":
    (temp_test,temperature)=temperature_test(rffe,temp_min,temp_max)
else:
    temp_test="Temperature Measurement         --> Not Performed"
    temperature = "Data not acquired"
    print("Temperature Test: Test not Performed")
################################################################      

sw_version="RFFE Software Version: " +str(rffe.get_software_version())

#Print the test result in the txt file
#test_result=([current_time],[att_sweep_resultA],[att_sweep_resultB],[rf_sw_result],[freq_resp_resultA],[freq_resp_resultB],[return_loss_resultA],[return_loss_resultB],[xtalk_resp_resultA],[xtalk_resp_resultB],[lin_resultA],[lin_resultB],[temp_test])
#test_lib.list_to_file(0,test_result,datapath_save + serial_number + "_result.txt")

#print metadata with the correct filename
shutil.copy2(metadata_path,datapath_save+serial_number+"_metadata.txt")

#print test result values with the correct filename
#test_result_values=([current_time],[sw_version],[att_sweep_resultA],[step_sizeA],[att_sweep_resultB],[step_sizeB],[rf_sw_result],[s21_sw_result],[freq_resp_resultA],[freq_resp_resultB],[s21_freq_resp],[return_loss_resultA],[return_loss_resultB],[s11_freq_resp],[lin_resultA],[pow_sweep_resultA],[lin_resultB],[pow_sweep_resultB],[xtalk_resp_resultA],[xtalk_resp_resultB],[xtalk_result],[temp_test],[temperature])
sw_version="RFFE Software Version: " +str(rffe.get_software_version())

test_result_values=([current_time],[sw_version],
                    [att_sweep_result_1],[step_size_1],[att_sweep_result_2],[step_size_2],
                    [att_sweep_result_3],[step_size_3],[att_sweep_result_4],[step_size_4],
                    [rf_sw_result_1],[rf_sw_result_values_1],[rf_sw_result_2],[rf_sw_result_values_2],
                    [rf_sw_result_3],[rf_sw_result_values_3],[rf_sw_result_4],[rf_sw_result_values_4],
                    [freq_resp_result_1],[freq_resp_result_values_1],[freq_resp_result_2],[freq_resp_result_values_2],
                    [freq_resp_result_3],[freq_resp_result_values_3],[freq_resp_result_4],[freq_resp_result_values_4],
                    [lin_result_1],[pow_sweep_result_1],[lin_result_2],[pow_sweep_result_2],
                    [lin_result_3],[pow_sweep_result_3],[lin_result_4],[pow_sweep_result_4],
                    [return_loss_result_1_11],[return_loss_result_value_1_11],[return_loss_result_2_11],[return_loss_result_value_2_11],
                    [return_loss_result_3_11],[return_loss_result_value_3_11],[return_loss_result_4_11],[return_loss_result_value_4_11],
                    [return_loss_result_1_22],[return_loss_result_value_1_22],[return_loss_result_2_22],[return_loss_result_value_2_22],
                    [return_loss_result_3_22],[return_loss_result_value_3_22],[return_loss_result_4_22],[return_loss_result_value_4_22],
                    [xtalk_resp_result_1],[xtalk_resp_result_2],[xtalk_result_12],
                    [xtalk_resp_result_3],[xtalk_resp_result_4],[xtalk_result_34],
                    [temp_test],[temperature])


#print metadata with the correct filename
shutil.copy2(metadata_path,datapath_save+serial_number+"_metadata.txt")

test_lib.list_to_file(0,test_result_values,datapath_save + serial_number + "_result_values.txt")

print("\nTest finished!")

##Close ethernet connection
vna.close_connection()
rffe.close_connection()
rfsw_1.close_connection()
rfsw_2.close_connection()
sgen.close_connection()





#TESTES ANTIGOS

#S-parameters test
'''
print ("Porta 1-1 do Switch") 
#rfsw.sw1_pos(canal_a)
#rfsw.sw2_pos(canal_a)
rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1) #(3,3)


s11_pos1=vna.get_s11_data()
s12_pos1=vna.get_s12_data()
s21_pos1=vna.get_s21_data()
s22_pos1=vna.get_s22_data()

s11_pos1=np.array([[s11_pos1]]).T
s12_pos1=np.array([[s12_pos1]]).T
s21_pos1=np.array([[s21_pos1]]).T
s22_pos1=np.array([[s22_pos1]]).T
sparam_pos1 = np.c_[s11_pos1, s12_pos1, s21_pos1, s22_pos1]

print("...\n")

print ("Porta 1-2 do Switch")
#rfsw.sw1_pos(canal_a)
#rfsw.sw2_pos(canal_b)
rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_2) #(3,4)

#addr=urllib.request.urlopen("http://10.0.18.19/:SP4TA:STATE:1")
#addr=urllib.request.urlopen("http://10.0.18.19/:SP4TB:STATE:2")

s11_pos2=vna.get_s11_data()
s12_pos2=vna.get_s12_data()
s21_pos2=vna.get_s21_data()
s22_pos2=vna.get_s22_data()

s11_pos2=np.array([[s11_pos2]]).T
s12_pos2=np.array([[s12_pos2]]).T
s21_pos2=np.array([[s21_pos2]]).T
s22_pos2=np.array([[s22_pos2]]).T
sparam_pos2 = np.c_[s11_pos2, s12_pos2, s21_pos2, s22_pos2]

print("...\n")

print ("Porta 2-1 do Switch")
#rfsw.sw1_pos(canal_b)
#rfsw.sw2_pos(canal_a)
rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_1) #(4,3)

#addr=urllib.request.urlopen("http://10.0.18.19/:SP4TA:STATE:2")
#addr=urllib.request.urlopen("http://10.0.18.19/:SP4TB:STATE:1")
s11_pos3=vna.get_s11_data()
s12_pos3=vna.get_s12_data()
s21_pos3=vna.get_s21_data()
s22_pos3=vna.get_s22_data()

s11_pos3=np.array([[s11_pos3]]).T
s12_pos3=np.array([[s12_pos3]]).T
s21_pos3=np.array([[s21_pos3]]).T
s22_pos3=np.array([[s22_pos3]]).T
sparam_pos3 = np.c_[s11_pos3, s12_pos3, s21_pos3, s22_pos3]

print("...\n")

print ("Porta 2-2 do Switch")
#rfsw.sw1_pos(canal_b)
#rfsw.sw2_pos(canal_b)

rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)

#addr=urllib.request.urlopen("http://10.0.18.19/:SP4TA:STATE:2")
#addr=urllib.request.urlopen("http://10.0.18.19/:SP4TB:STATE:2")

s11_pos4=vna.get_s11_data()
s12_pos4=vna.get_s12_data()
s21_pos4=vna.get_s21_data()
s22_pos4=vna.get_s22_data()

s11_pos4=np.array([[s11_pos4]]).T
s12_pos4=np.array([[s12_pos4]]).T
s21_pos4=np.array([[s21_pos4]]).T
s22_pos4=np.array([[s22_pos4]]).T
sparam_pos4 = np.c_[s11_pos4, s12_pos4, s21_pos4, s22_pos4]'''


#Teste auxiliar
'''
auxiliar = list()
print("Teste para verificar o ganho máximo no filtro: Atenuador setado para 0dB")
test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
sgen.set_pos("direct")
rffe.set_attenuator_value(0)
vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
rfsw.sw1_pos(canal_a)
rfsw.sw2_pos(canal_a)
auxiliar=round((float(test_lib.marker_value(0,center_freq, "s21", vna))),2)
print("Valor medido: ", auxiliar)'''





#Teste de atenuadores
'''#Attenuators sweep test (OLD ONE)

#TESTE OK!!!!
 
#(atenuador programável switch 1 fixo a 0dB, switch 2 pos 1 0 até 30dB, pos 2 0 até 30dB)
#as variáveis a baixo são declaradas como do tipo list(), ou seja, vão funcionar como listas
s21_testA=list() 
step_sizeA=list()
s21_testB=list()
step_sizeB=list()

if metadata_param['att_sweep_test']=="run":
    print("Running attenuators sweep test ... \n")
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    sgen.set_pos("direct")
    s21=vna.get_s21_data() #Select the S21 measurement in theNetwork Analyzer
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
    
    #Data aquisition for channel A
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_a)
    print("Running attenuators sweep test, Channel A ... \n")
   
    for att in range (int(att_sweep_low), int(att_sweep_high+1)*2, int(att_step*2)):

        rffe.set_attenuator_value(att/2)
        s21=test_lib.marker_value(0,center_freq,"s21", vna)
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testA.append(round(s21,2))
       
    fail=0

    print("Upper Boundary: ", abs(att_step+att_step_tol))
    print("Lower Boundary: ", abs(att_step-att_step_tol))
        
    for i in range(0,len(s21_testA)-1):
        step_sizeA.append(round(s21_testA[i+1]-s21_testA[i],2))
        if abs(float(step_sizeA[i]))>abs(att_step+att_step_tol) or abs(float(step_sizeA[i]))<abs(att_step-att_step_tol):
            fail=1
    if fail==1:
        att_sweep_resultA="Attenuator Sweep Test Channel A --> FAILED"
        print("Result: Attenuator Sweep Test Channel A --> FAILED")
        print("Result: ",step_sizeA)
    else:
        att_sweep_resultA="Attenuator Sweep Test Channel A --> Ok"
        print("Result: Attenuator Sweep Test Channel A --> Ok")
        print("Result: ",step_sizeA)

    
    #Data aquisition for channel B
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_b)
    print("Running attenuators sweep test, Channel B ... \n")
    
    
    for att in range (int(att_sweep_low), int(att_sweep_high+1)*2, int(att_step*2)):
        rffe.set_attenuator_value(att/2)
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testB.append(round(s21,2))
  
    for i in range(0,len(s21_testB)-1):
        step_sizeB.append(round(s21_testB[i+1]-s21_testB[i],2))
        if abs(float(step_sizeB[i]))>abs(att_step+att_step_tol) or abs(float(step_sizeB[i]))<abs(att_step-att_step_tol):
            fail=1
    if fail==1:
        att_sweep_resultB="Attenuator Sweep Test Channel B --> FAILED"
        print("Result: Attenuator Sweep Test Channel B --> FAILED")
        print("Result: ",step_sizeB)
    else:
        att_sweep_resultB="Attenuator Sweep Test Channel B --> Ok"
        print("Result: Attenuator Sweep Test Channel B --> Ok")
        print("Result: ",step_sizeB)
else:
    att_sweep_resultA="Attenuator Sweep Test Channel A --> Test not Performed"
    step_sizeA = "Data not acquired"
    att_sweep_resultB="Attenuator Sweep Test Channel B --> Test not Performed"
    step_sizeB = "Data not acquired"
    print("Attenuator Sweep Test: Test not Performed")'''
    
    
    
    


#Teste de switches

'''#RF switches test (OLD ONE)

#Teste OK !!!

s21_sw_resultA=list()
s21_sw_resultB=list()
if metadata_param['sw_test']=="run":
    print("\nRunning RF switches test ... \n")
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    rffe.set_attenuator_value(att_value)

    #Canal A
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_a)
    sgen.set_pos("direct")
    s21_testA=float(test_lib.marker_value(0,center_freq, "s21", vna))
    s21_sw_resultA.append(round(s21_testA,2))
    sgen.set_pos("inverted")
    s21_testB=float(test_lib.marker_value(0,center_freq, "s21", vna))
    s21_sw_resultA.append(round(s21_testB,2))

    print("Lower Boundary: ", abs(xtalk_ref))
        
    if abs(float(s21_testA)-float(s21_testB))<abs(xtalk_ref):
        rf_sw_result_valuesA = round((abs(float(s21_testA)-float(s21_testB))),2)
        rf_sw_resultA="RF Switches Test Channel A --> FAILED"
        print("RF Switches Test Channel A --> FAILED")
        print("Result: ", rf_sw_result_valuesA)
    else:
        rf_sw_result_valuesA = round((abs(float(s21_testA)-float(s21_testB))),2)
        rf_sw_resultA="RF Switches Test Channel A --> Ok"
        print("RF Switches Test Channel A --> Ok")
        print("Result: ", rf_sw_result_valuesA)
        
    #Canal B
    
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_b)
    sgen.set_pos("direct")
    s21_testB=float(test_lib.marker_value(0,center_freq, "s21", vna))
    s21_sw_resultB.append(round(s21_testB,2))
    sgen.set_pos("inverted")
    s21_testA=float(test_lib.marker_value(0,center_freq, "s21", vna))
    s21_sw_resultB.append(round(s21_testA,2))
        
    if abs(float(s21_testB)-float(s21_testA))<abs(xtalk_ref):
        rf_sw_result_valuesB = round((abs(float(s21_testB)-float(s21_testA))),2)
        rf_sw_resultB="RF Switches Test Channel B--> FAILED"
        print("RF Switches Test Channel B--> FAILED")
        print("Result: ", rf_sw_result_valuesB)
    else:
        rf_sw_result_valuesB = round((abs(float(s21_testB)-float(s21_testA))),2)
        rf_sw_resultB="RF Switches Test Channel B --> Ok"
        print("RF Switches Test Channel B --> Ok")
        print("Result: ", rf_sw_result_valuesB)
        
else:
    rf_sw_resultA="RF Switches Test Channel A --> Test not Performed"
    rf_sw_result_valuesA = "Data not acquired"
    rf_sw_resultB="RF Switches Test Channel B --> Test not Performed"
    rf_sw_result_valuesB = "Data not acquired"
    print("RF Switch Test: Test not Performed")'''
    
    
    
    


#Teste de Resposta em Frequência
'''#Frequency Response (OLD ONE)

#A princípio, teste ok !!!......o valor da variável s21_ref foi alterado para 4.5. O valor original era 1.3
#conforme sugestão do sérgio.

#VERIFICAR SE O VALOR DO GANHO OBTIDO NO FILTRO PARA ATENUAÇÃO DE 30dB 
#ESTÁ OCORRENDO CONFORME PROJETO (atualmente o valor máximo que ele atinge está por volta de 34 dB)

s21_freq_resp=list()
if metadata_param['freq_response']=="run":
    print("\nRunning Frequency Response test ... \n")
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    sgen.set_pos("direct")
    rffe.set_attenuator_value(att_value)
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_a)
    s21_testA=float(test_lib.marker_value(0,center_freq, "s21", vna))
    s21_freq_resp.append(round(s21_testA,2))
    
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_b)
    sgen.set_pos("direct")
    s21_testB=float(test_lib.marker_value(0,center_freq, "s21", vna))
    s21_freq_resp.append(round(s21_testB,2))
    
    print("Upper Boundary: ",s21_tol)
    
    if abs(float(s21_testA)-s21_ref)>s21_tol:
        freq_resp_resultA="Frequency Response Channel A    --> FAILED"
        freq_resp_resultA_values = round((abs(float(s21_testA)-s21_ref)),2)
        print("Frequency Response Channel A    --> FAILED")
        print("Result: ", freq_resp_resultA_values)
    else:
        freq_resp_resultA="Frequency Response Channel A    --> Ok"
        freq_resp_resultA_values = round((abs(float(s21_testA)-s21_ref)),2)
        print("Frequency Response Channel A    --> OK")
        print("Result: ", freq_resp_resultA_values)
    
    if abs(float(s21_testB)-s21_ref)>s21_tol:
        freq_resp_resultB="Frequency Response Channel B    --> FAILED"
        freq_resp_resultB_values = round((abs(float(s21_testB)-s21_ref)),2)
        print("Frequency Response Channel B    --> FAILED")
        print("Result: ", freq_resp_resultB_values)
    else:
        freq_resp_resultB="Frequency Response Channel B    --> Ok"
        freq_resp_resultB_values = round((abs(float(s21_testB)-s21_ref)),2)
        print("Frequency Response Channel B    --> OK")
        print("Result: ", freq_resp_resultB_values)
else:
    freq_resp_resultA="Frequency Response Channel A    --> Test not Performed"
    freq_resp_resultB="Frequency Response Channel B    --> Test not Performed"
    freq_resp_resultA_values = "Data not acquired"
    freq_resp_resultB_values = "Data not acquired"
    print("Frequency Response Test: Test not Performed")'''
    
    
    


#Teste de Return Loss
'''#Return Loss (OLD ONE)
s11_freq_resp=list()
if metadata_param['return_loss']=="run":
    print("\nRunning return loss test ... \n")
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    sgen.set_pos("direct")
    rffe.set_attenuator_value(att_value)
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_a)
    s11_testA=float(test_lib.marker_value(0,center_freq, "s11", vna))
    s11_freq_resp.append(round(s11_testA,2))
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_b)
    sgen.set_pos("direct")
    s11_testB=float(test_lib.marker_value(0,center_freq, "s11", vna))
    s11_freq_resp.append(round(s11_testB,2))
    
    print("Lower Boundary: ",abs(s11_ref+s11_tol))
    
    if abs(float(s11_testA))<abs(s11_ref+s11_tol):
        return_loss_resultA="Return Loss Channel A           --> FAILED"
        return_loss_resultA_value= round((abs(float(s11_testA))),2)
        print("Return Loss Channel A           --> FAILED")
        print("Result: ",return_loss_resultA_value)
    else:
        return_loss_resultA="Return Loss Channel A           --> Ok"
        return_loss_resultA_value= round((abs(float(s11_testA))),2)
        print("Return Loss Channel A           --> Ok")
        print("Result: ",return_loss_resultA_value)
    
    if abs(float(s11_testB))<abs(s11_ref+s11_tol):
        return_loss_resultB="Return Loss Channel B           --> FAILED"
        return_loss_resultB_value= round((abs(float(s11_testB))),2)
        print("Return Loss Channel B           --> FAILED")
        print("Result: ",return_loss_resultA_value)
    else:
        return_loss_resultB="Return Loss Channel B           --> Ok"
        return_loss_resultB_value= round((abs(float(s11_testB))),2)
        print("Return Loss Channel B           --> Ok")
        print("Result: ",return_loss_resultB_value)
else:
    return_loss_resultA="Return Loss Channel A           --> Test not Performed"
    return_loss_resultB="Return Loss Channel B           --> Test not Performed"
    return_loss_resultA_value = "Data not acquired"
    return_loss_resultB_value = "Data not acquired"
    print("Return Loss Test: Test not Performed")'''
    
    
    



#Teste de Linearidade
'''#Power sweep ( testes de linearidade : switch 1 : alternação 1dB/5dB segun método do JC cf doc test linearidade (OLD ONE)
pow_sweep_resultA_1db=list()
pow_sweep_resultB_1db=list()
pow_sweep_result_values_comparedA_1db = list()
pow_sweep_result_values_comparedB_1db = list()

pow_sweep_resultA_5db=list()
pow_sweep_resultB_5db=list()
pow_sweep_result_values_comparedA_5db = list()
pow_sweep_result_values_comparedB_5db = list()

pow_sweep_resultA = list()
pow_sweep_resultB = list()


#por segurança
vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")


if metadata_param['power_sweep']=="run":
    
    #TESTE 1: ATENUAÇÃO DO SWITCH 1 CONFIGURADO PARA 1 dB
    addr=urllib.request.urlopen("http://10.0.18.13/:SP4TA:STATE:2")
    addr=urllib.request.urlopen("http://10.0.18.13/:SP4TB:STATE:2")
    
    print("Running power sweep and linearity test: 1dB of Attenuation ... \n")
    rffe.set_attenuator_value(pow_sweep_att)
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    sgen.set_pos("direct")
    power_values=np.arange(float(pow_sweep_ini),float(pow_sweep_end),float(pow_sweep_step))
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_a)
    s21_testA=0
    s21_testA=list()
    for i in range (0,len(power_values)):
        vna.set_power_range(power_values[i])
        vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testA.append(round(s21,2))
        
    pow_sweep_resultA_1db=s21_testA
    
    #initialize the test routine for channel B
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_b)
    s21_testB=0
    s21_testB=list()
    for i in range (0,len(power_values)):
        vna.set_power_range(power_values[i])
        vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testB.append(round(s21,2))
 #Test analysis: verify if the linearity is inside the limits
    pow_sweep_resultB_1db=s21_testB
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    
    print("Upper Boundary: ", abs(float(linearity_tol)))
    
         
    #TESTE 2: ATENUAÇÃO DO SWITCH 1 CONFIGURADO PARA 5 dB
    addr=urllib.request.urlopen("http://10.0.18.13/:SP4TA:STATE:1")
    addr=urllib.request.urlopen("http://10.0.18.13/:SP4TB:STATE:1")
    
    print("Running power sweep and linearity test: 5dB of Attenuation... \n")
    rffe.set_attenuator_value(pow_sweep_att)
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    sgen.set_pos("direct")
    power_values=np.arange(float(pow_sweep_ini),float(pow_sweep_end),float(pow_sweep_step))
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_a)
    s21_testA=0
    s21_testA=list()
    for i in range (0,len(power_values)):
        
        vna.set_power_range(power_values[i])
        vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testA.append(round(s21,2))
    
    
    pow_sweep_resultA_5db=s21_testA
    
    #initialize the test routine for channel B
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_b)
    s21_testB=0
    s21_testB=list()
    for i in range (0,len(power_values)):
        
        vna.set_power_range(power_values[i])
        vna.send_command(b":SOUR1:POW "+format(power_values[i]).encode('utf-8')+b"\n")
        s21=float(test_lib.marker_value(0,center_freq,"s21", vna))
        s21_testB.append(round(s21,2))
 #Test analysis: verify if the linearity is inside the limits
    pow_sweep_resultB_5db=s21_testB
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    
     
    #TESTE CORRETO    
    fail=0
    for i in range(0,len(power_values)):
        pow_sweep_resultA.append(round((abs(float(pow_sweep_resultA_1db[i])-float(pow_sweep_resultA_5db[i]))-pow_sweep_correction_factor),2))
        if abs(po

        w_sweep_resultA[i])>abs(float(linearity_tol)):
            fail=1
    if fail==1:
        lin_resultA="Linearity Test Channel A        --> FAILED"
        print("Linearity Test Channel A        --> FAILED")
        print("Result: ", pow_sweep_resultA)
    else:
        lin_resultA="Linearity Test Channel A        --> Ok"
        print("Linearity Test Channel A        --> Ok")
        print("Result: ", pow_sweep_resultA)
        
    fail=0
    for i in range(0,len(power_values)):
        pow_sweep_resultB.append(round((abs(float(pow_sweep_resultB_1db[i])-float(pow_sweep_resultB_5db[i]))-pow_sweep_correction_factor),2))
        if abs(pow_sweep_resultB[i])>abs(float(linearity_tol)):
            fail=1
    if fail==1:
        lin_resultB="Linearity Test Channel B        --> FAILED"
        print("Linearity Test Channel B        --> FAILED")
        print("Result: ", pow_sweep_resultB)
    else:
        lin_resultB="Linearity Test Channel B        --> Ok"
        print("Linearity Test Channel B        --> Ok")
        print("Result: ", pow_sweep_resultB)
                
        
else:
    lin_resultA="Linearity Test Channel A        --> Test not Performed"
    lin_resultB="Linearity Test Channel B        --> Test not Performed"
    pow_sweep_resultA = "Data not acquired"
    pow_sweep_resultB = "Data not acquired"






#Coloca o equipamento para operar na potência de referência 
vna.set_power_range(pow_value)
vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
#Coloca o switch 1 no valor de referência de 0 dB
addr=urllib.request.urlopen("http://10.0.18.13/:SP4TA:STATE:3")
addr=urllib.request.urlopen("http://10.0.18.13/:SP4TB:STATE:3")'''






#Teste de Crosstalk
'''#Crosstalk test (OLD ONE)
if metadata_param['xtalk']=="run":
    
    xtalk_result=list()  
    print("Running Crosstalk test ... \n")
    test_lib.set_vna(0, center_freq, freq_span, freq_start, freq_stop, 0, vna)
    sgen.set_pos("direct")
    rffe.set_attenuator_value(att_value)
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n")
    rfsw.sw1_pos(canal_a)
    rfsw.sw2_pos(canal_b)
    s21_testA=float(test_lib.marker_value(0,center_freq, "s21", vna))
    xtalk_result.append(round(s21_testA-xtalk_tol,2))
    rfsw.sw1_pos(canal_b)
    rfsw.sw2_pos(canal_a)
    sgen.set_pos("direct")
    s21_testB=float(test_lib.marker_value(0,center_freq, "s21", vna))
    xtalk_result.append(round(s21_testB-xtalk_tol,2))

    print("Lower Boundary: ",abs(xtalk_ref+xtalk_tol))
    
    if abs(s21_testA)<abs(xtalk_ref+xtalk_tol):
        xtalk_resp_resultA="Crosstalk Channel A             --> FAILED"
        print("Crosstalk Channel A             --> FAILED")
        print("Result: ",abs(round(s21_testA,2)))
    else:
        xtalk_resp_resultA="Crosstalk Channel A             --> Ok"
        print("Crosstalk Channel A             --> Ok")
        print("Result: ",abs(round(s21_testA,2)))
        
    if abs(s21_testB)<abs(xtalk_ref+xtalk_tol):
        xtalk_resp_resultB="Crosstalk Channel B             --> FAILED"
        print("Crosstalk Channel B             --> FAILED")
        print("Result: ",abs(round(s21_testB,2)))
    else:
        xtalk_resp_resultB="Crosstalk Channel B             --> Ok"
        print("Crosstalk Channel B             --> Ok")
        print("Result: ",abs(round(s21_testB,2)))
    
    print("Total Result: ",xtalk_result)
    
else:
    xtalk_resp_resultA="Crosstalk Channel A             --> Test not Performed"
    xtalk_resp_resultB="Crosstalk Channel B             --> Test not Performed"
    xtalk_result = "Data not acquired"
    print("Crosstalk Test --> Test not Performed")'''
    
    
    
    



#Teste de temperatura
'''#Temperature Measurement (OLD ONE)
if metadata_param['temp']=="run":
    print("\nRunning Temperature test ... \n")
    temperature=rffe.get_temp1()
    print("Entrou 1")
    fail=0
    if (temperature < 5 or temperature >100):
        print("Entrou 2")
        temperature = rffe.get_temp2()
        if (temperature < 5 or temperature > 100):
            fail=1
    temperature=round(temperature,2)
    
    print("Lower Boundary: ",temp_min)
    print("Upper Boundary: ",temp_max)
    
    if (temperature<temp_min or temperature>temp_max):
        fail=1
    if (fail==1):
        temp_test="Temperature Measurement         --> FAILED"
        print("Temperature Measurement         --> FAILED")
        print("Result: ", temperature)
    elif (fail==0):
        temp_test="Temperature Measurement         --> Ok"
        print("Temperature Measurement         --> Ok")
        print("Result: ", temperature)
else:
    temp_test="Temperature Measurement         --> Not Performed"
    temperature = "Data not acquired"
    print("Temperature Test: Test not Performed")'''




    
   
