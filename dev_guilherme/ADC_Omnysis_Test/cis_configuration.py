from subprocess import Popen, PIPE
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import datetime
from subprocess import Popen
import sys
import time

SLEEP_TIME = 5.0


def cis_configuration(ad9510_pll_function_config,ad9510_pll_clock_sel_config,
                      ad9510_pll_clock_sel_ref_config,ad9510_a_divider_config,ad9510_b_divider_config,
                      ad9510_r_divider_config,ad9510_prescaler_config,ad9510_pll_powerdown_config,
                      ad9510_current_config,ad9510_outputs_config,si571_freq_config,si571_output_config,
                      ad9510_a_divider_config_check,ad9510_b_divider_config_check,ad9510_current_config_check,
                      ad9510_outputs_config_check,ad9510_pll_clock_sel_config_check,ad9510_pll_clock_sel_ref_config_check,
                      ad9510_prescaler_config_check,ad9510_pll_function_config_check,ad9510_pll_powerdown_config_check,
                      ad9510_r_divider_config_check,si571_freq_config_check,si571_output_config_check,all_config_check,
                      IP_CRATE,POSITION_ADC,POSITION_CRATE,tela_principal):





    
    
    
    ping_crate = Popen(['ping',str(IP_CRATE),'-c','1',"-W","2"])
    ping_crate.wait()
    ping_result = ping_crate.poll()
    if (ping_result==0):
        crate_str_result_msg="CRATE - COMUNICAÇÃO: OK"
        crate_str_IP="CRATE - IP: "+str(IP_CRATE)
        print(crate_str_result_msg)
        tela_principal.ui.communication_config.setText("OK")  
        tela_principal.repaint()
        QApplication.processEvents()
        communication_config_str = "OK"

    
    else:
        crate_str_result_msg="CRATE - COMUNICAÇÃO: FAIL"
        crate_str_IP="CRATE IP - "+str(IP_CRATE)
        print(crate_str_result_msg)
        print("Encerrando conexão")
        tela_principal.ui.communication_config.setText("FAIL")  
        tela_principal.repaint()
        QApplication.processEvents()
        communication_config_str = "FAIL"
        time.sleep(SLEEP_TIME)
        sys.exit()
        
    
    
    if (communication_config_str=="OK"):   
        fail_general = 0    
        local = "cd CRATE_ACESSO/bpm-app/.halcs-libs/examples\n"
        
        tela_principal.ui.progressBar_config.setValue(0)  
        tela_principal.repaint()
        QApplication.processEvents() 
        
        print("Iniciou a Configuração dos CIs - AD9510 & Si571")
        start_time=datetime.datetime.now()
        start_time_str=start_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Start_write_time:",start_time_str)
        
        cis_configuration_log=[]
        
        write_text="WRITTEN VALUE: "
        read_text="READ VALUE: "
        write_verification_text="WRITE CHECK: "
        read_verification_text="READ CHECK: "
       
     
        if(all_config_check==True):
            ad9510_pll_function_config_check=True
            ad9510_pll_clock_sel_config_check=True
            ad9510_pll_clock_sel_ref_config_check=True
            ad9510_a_divider_config_check=True
            ad9510_b_divider_config_check=True
            ad9510_r_divider_config_check=True
            ad9510_prescaler_config_check=True
            ad9510_pll_powerdown_config_check=True
            ad9510_current_config_check=True
            ad9510_outputs_config_check=True
            si571_freq_config_check=True
            si571_output_config_check=True
      
        
        if(ad9510_pll_function_config_check==True):
            
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -fmc_pll_function "+str(ad9510_pll_function_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_value=command_stdout[len(command_stdout)-2].decode("utf-8")
            read_value=command_stdout[len(command_stdout)-1].decode("utf-8")
            write_aux=str(write_value).replace(write_text,"")
            read_aux=str(read_value).replace(read_text,"")
            
            cis_configuration_log.append("PLL_FUNCTION CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("PLL_FUNCTION TEST: OK")
                cis_configuration_log.append("PLL_FUNCTION TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("PLL_FUNCTION TEST: FAIL")
                cis_configuration_log.append("PLL_FUNCTION TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
        
        else:
            cis_configuration_log.append("PLL_FUNCTION CONFIG: Não Realizado")  
      
        if(ad9510_pll_clock_sel_config_check==True):
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -pll_clk_sel "+str(ad9510_pll_clock_sel_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
     
            cis_configuration_log.append("PLL_CLOCK_SEL CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("PLL_CLOCK_SEL: OK")
                cis_configuration_log.append("PLL_CLOCK_SEL TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("PLL_CLOCK_SEL TEST: FAIL")
                cis_configuration_log.append("PLL_CLOCK_SEL TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
    
        else:
            cis_configuration_log.append("PLL_CLOCK_SEL CONFIG: Não Realizado") 
    
        
        if(ad9510_pll_clock_sel_ref_config_check==True):
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -pll_clk_sel_ref "+str(ad9510_pll_clock_sel_ref_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
            
            cis_configuration_log.append("PLL_CLOCK_SEL_REF CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("PLL_CLOCK_SEL_REF: OK")
                cis_configuration_log.append("PLL_CLOCK_SEL_REF TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("PLL_CLOCK_SEL_REF TEST: FAIL")
                cis_configuration_log.append("PLL_CLOCK_SEL_REF TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("PLL_CLOCK_SEL_REF CONFIG: Não Realizado") 
    
       
        if(ad9510_a_divider_config_check==True):
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -a_div "+str(ad9510_a_divider_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
            
            cis_configuration_log.append("A_DIVIDER CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("A_DIVIDER: OK")
                cis_configuration_log.append("A_DIVIDER TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("A_DIVIDER TEST: FAIL")
                cis_configuration_log.append("A_DIVIDER TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("A_DIVIDER CONFIG: Não Realizado") 
        
        if(ad9510_b_divider_config_check==True):    
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -b_div "+str(ad9510_b_divider_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
        
            cis_configuration_log.append("B_DIVIDER CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("B_DIVIDER: OK")
                cis_configuration_log.append("B_DIVIDER TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("B_DIVIDER: FAIL")
                cis_configuration_log.append("B_DIVIDER TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("B_DIVIDER CONFIG: Não Realizado") 
    
    
        tela_principal.ui.progressBar_config.setValue(50)  
        tela_principal.repaint()
        QApplication.processEvents() 
    
        if(ad9510_r_divider_config_check==True):     
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -r_div "+str(ad9510_r_divider_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
    
            cis_configuration_log.append("R_DIVIDER CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("R_DIVIDER TEST: OK")
                cis_configuration_log.append("R_DIVIDER TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("R_DIVIDER TEST: FAIL")
                cis_configuration_log.append("R_DIVIDER TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("R_DIVIDER CONFIG: Não Realizado") 
    
        
        if(ad9510_prescaler_config_check==True):     
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -prescaler_div "+str(ad9510_prescaler_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
            
            cis_configuration_log.append("PRESCALER CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("PRESCALER: OK")
                cis_configuration_log.append("PRESCALER TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("PRESCALER TEST: FAIL")
                cis_configuration_log.append("PRESCALER TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("PRESCALER CONFIG: Não Realizado") 
    
            
        if(ad9510_pll_powerdown_config_check==True):     
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -pll_pdown "+str(ad9510_pll_powerdown_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
            
            cis_configuration_log.append("PLL_PDOWN CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("PLL_PDOWN: OK")
                cis_configuration_log.append("PLL_PDOWN TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("PLL_PDOWN TEST: FAIL")
                cis_configuration_log.append("PLL_PDOWN TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("PLL_PDOWN CONFIG: Não Realizado")
    
        
        if(ad9510_current_config_check==True):    
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -cp_current "+str(ad9510_current_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
            
            cis_configuration_log.append("CURRENT CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("CURRENT: OK")
                cis_configuration_log.append("CURRENT TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("CURRENT TEST: FAIL")
                cis_configuration_log.append("CURRENT TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("CURRENT CONFIG: Não Realizado")
    
        
        if(ad9510_outputs_config_check==True):     
    
            command = "./THALES_ad9510_ctl_CONFIG -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -outputs "+str(ad9510_outputs_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
        
            cis_configuration_log.append("OUTPUTS CONFIG")
            ad9510_write_check=0
            ad9510_read_check=0
            check_function=0
        
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            if(write_aux!=read_aux):
                    cis_configuration_log.append("Fail Detected - Valor Escrito: "+str(write_aux)+" Valor lido: "+str(read_aux))
                    print("Fail Detected - Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                    check_function=check_function+1
            
            if (check_function==0):
                print("OUTPUTS: OK")
                cis_configuration_log.append("OUTPUTS TEST: OK")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
            else:
                print("OUTPUTS TEST: FAIL")
                cis_configuration_log.append("OUTPUTS TEST: FAIL")
                cis_configuration_log.append("Valor Escrito: ",write_aux," Valor lido: ",read_aux)
                fail_general=fail_general+1
                
        else:
            cis_configuration_log.append("OUTPUTS CONFIG: Não Realizado")
    
    
    
    
        '''################################################################'''    
        if(si571_freq_config_check==True):     
    
            command = "./THALES_si571_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -freq "+str(si571_freq_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
    
            si571_freq_write_check=0
            si571_freq_read_check=0
    
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                si571_freq_write_check=si571_freq_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                si571_freq_read_check=si571_freq_read_check+1    
        
            print("Verificação...")
        
            si571_freq_check=0
        
            if(read_value!=write_value or read_value!=str(format(si571_freq_config, '.6f'))):
                print("Valor Enviado pelo Comando: ",si571_freq_config)
                print("Valor Escrito :",write_value)
                print("Valor Lido: ",read_value)
                si571_freq_check=si571_freq_check+1
            
        
            if(si571_freq_check==0):
                print("Si571 Test: OK")
                si571_freq_result="OK"
            else:
                print("Si571 Test: FAIL")
                si571_freq_result="FAIL"    
                fail_general=fail_general+1
        
            if(si571_freq_write_check!=0):
                si571_freq_write_check_result = "FAIL"
                print("Utilizacao do método de Escrita: ",si571_freq_write_check_result)
                fail_general=fail_general+1
            else:
                si571_freq_write_check_result = "OK"  
                print("Utilizacao do método de Escrita: ",si571_freq_write_check_result)
     
            if(si571_freq_read_check!=0):
                si571_freq_read_check_result = "FAIL"
                fail_general=fail_general+1
                print("Utilizacao do método de Leitura: ",si571_freq_read_check_result)
            else:
                si571_freq_read_check_result = "OK"  
                print("Utilizacao do método de Leitura: ",si571_freq_read_check_result)  
    
            cis_configuration_log.append("Configuração para o Parâmetro: Si571 - Frequência")
            cis_configuration_log.append("Valor Enviado pelo Comando [Hz]: "+str(si571_freq_config))
            cis_configuration_log.append("Valor Escrito [Hz]: "+str(write_value))
            cis_configuration_log.append("Valor Lido [Hz]: "+str(read_value))
        
            cis_configuration_log.append("Utilizacao do método de Escrita: "+str(si571_freq_write_check_result))
            cis_configuration_log.append("Utilizacao do método de Leitura: "+str(si571_freq_read_check_result))
            cis_configuration_log.append("FINAL RESULT: "+str(si571_freq_result))
    
        else:
            cis_configuration_log.append("Si571 Freq CONFIG: Não Realizado")
    
    
    
        '''################################################################'''    
        if(si571_output_config_check==True):     
    
            command = "./THALES_si571_output_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -output "+str(si571_output_config)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
            write_value=write_aux.replace(write_text,"")
            read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
            read_value=read_aux.replace(read_text,"")
    
            si571_output_write_check=0
            si571_output_read_check=0
    
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                si571_output_write_check=si571_output_write_check+1
        
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                si571_output_read_check=si571_output_read_check+1    
        
            print("Verificação...")
        
            si571_output_check=0
        
            if(read_value!=write_value or read_value!=str(format(si571_output_config))):
                print("Valor Enviado pelo Comando: ",si571_output_config)
                print("Valor Escrito :",write_value)
                print("Valor Lido: ",read_value)
                si571_output_check=si571_output_check+1
            
        
            if(si571_output_check==0):
                print("Si571 Test: OK")
                si571_output_result="OK"
            else:
                print("Si571 Test: FAIL")
                si571_output_result="FAIL"    
                fail_general=fail_general+1
        
            if(si571_output_write_check!=0):
                si571_output_write_check_result = "FAIL"
                fail_general=fail_general+1
                print("Utilizacao do método de Escrita: ",si571_output_write_check_result)
            else:
                si571_output_write_check_result = "OK"  
                print("Utilizacao do método de Escrita: ",si571_output_write_check_result)
     
            if(si571_output_read_check!=0):
                si571_output_read_check_result = "FAIL"
                fail_general=fail_general+1
                print("Utilizacao do método de Leitura: ",si571_output_read_check_result)
            else:
                si571_output_read_check_result = "OK"  
                print("Utilizacao do método de Leitura: ",si571_output_read_check_result)  
    
            cis_configuration_log.append("Configuração para o Parâmetro: Si571 - Ouput")
            cis_configuration_log.append("Valor Enviado pelo Comando: "+str(si571_output_config))
            cis_configuration_log.append("Valor Escrito: "+str(write_value))
            cis_configuration_log.append("Valor Lido: "+str(read_value))
        
            cis_configuration_log.append("Utilizacao do método de Escrita: "+str(si571_output_write_check_result))
            cis_configuration_log.append("Utilizacao do método de Leitura: "+str(si571_output_read_check_result))
            cis_configuration_log.append("FINAL RESULT: "+str(si571_output_result))
    
        
        else:
            cis_configuration_log.append("Si571 Output CONFIG: Não Realizado")
        
        
        
        tela_principal.ui.progressBar_config.setValue(100)  
        tela_principal.repaint()
        QApplication.processEvents() 
        
        if (fail_general==0):
            tela_principal.ui.result_config.setText("OK")  
            tela_principal.repaint()
            QApplication.processEvents() 
        else:
            tela_principal.ui.result_config.setText("FAIL")  
            tela_principal.repaint()
            QApplication.processEvents() 
            
            
    
            
       
        
        
    
    
        #ad9510_pll_status_config = "Teste2"

    return (cis_configuration_log)