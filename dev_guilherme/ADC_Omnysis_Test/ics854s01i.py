from subprocess import Popen, PIPE
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def ics854s01i(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds):
    
    local = "cd CRATE_ACESSO/bpm-app/.halcs-libs/examples\n"
    
    tela_leds.ui.progressBar.setValue(0)  
    tela_leds.repaint()
    QApplication.processEvents() 
       
    print("Iniciou o teste do ICS854S01I")
    start_time=datetime.datetime.now()
    start_time_str=start_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Start_write_time:",start_time_str)
    
    write_text="WRITTEN VALUE: "
    read_text="READ VALUE: "
    write_verification_text="WRITE CHECK: "
    read_verification_text="READ CHECK: "
    ics854s01i_write_check=0
    ics854s01i_read_check=0
    ics854s01i_log=[]
    
    #pll_clk_sel = 0 Clock from external source (MMCX J4) function mode 
    ics854s01i_log.append("Teste do PLL_CLK_SEL FROM EXTERNAL SOURCE - MMCX J4: 0")
    print("Teste do PLL_CLK_SEL FROM EXTERNAL SOURCE - MMCX J4: 0")
    pll_clk_sel=0
    command= "./THALES_ics854s01i_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -fmc_pll_function "+str(pll_clk_sel) 
    command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()
    write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
    write_value=write_aux.replace(write_text,"")
    
    read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
    read_value=read_aux.replace(read_text,"")
    
    #Verifica se foi capaz de enviar comandos através do método de escrita
    write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
    write_verification_aux=write_verification_aux.replace(write_verification_text,"")
    if (write_verification_aux!=str(0)):
        ics854s01i_write_check=ics854s01i_write_check+1
        
    #Verifica se foi capaz de enviar comandos através do método de leitura
    read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
    read_verification_aux=read_verification_aux.replace(read_verification_text,"")
    if (read_verification_aux!=str(0)):
        ics854s01i_read_check=ics854s01i_read_check+1
         
    print("Verificação...")

    tela_leds.ui.progressBar.setValue(50)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    
    pll_clk_sel_check_mmcx=0
    if(read_value!=write_value or read_value!=str(pll_clk_sel)):
        print("PLL_CLK_SEL: FAIL")
        print("Valor Enviado pelo Comando: ",pll_clk_sel)
        print("Valor Escrito : ",write_value)
        print("Valor Lido: ",read_value)
        pll_clk_sel_check_mmcx=pll_clk_sel_check_mmcx+1
        
    if(pll_clk_sel_check_mmcx==0):
        print("PLL_CLK_SEL FROM EXTERNAL SOURCE - MMCX J4: OK")
        pll_clk_sel_mmcx_result="OK"
    else:
        print("PLL_CLK_SEL FROM EXTERNAL SOURCE - MMCX J4: FAIL")
        pll_clk_sel_mmcx_result="FAIL"    
    
    ics854s01i_log.append("Valor Enviado pelo Comando: "+str(pll_clk_sel))
    ics854s01i_log.append("Valor Escrito : "+str(write_value))
    ics854s01i_log.append("Valor Lido : "+str(read_value))    
    
    
    #pll_clk_sel = 1 Clock from FMC PIN (FMC_CLK line) function mode 
    ics854s01i_log.append("Teste do PLL_CLK_SEL FROM FMC PIN (FMC_CLK LINE): 1")
    print("Teste do PLL_CLK_SEL FROM FMC PIN (FMC_CLK LINE): 1")
    pll_clk_sel=1
    command= "./THALES_ics854s01i_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -fmc_pll_function "+str(pll_clk_sel) 
    command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()
    write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
    write_value=write_aux.replace(write_text,"")
    
    read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
    read_value=read_aux.replace(read_text,"")
    
    #Verifica se foi capaz de enviar comandos através do método de escrita
    write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
    write_verification_aux=write_verification_aux.replace(write_verification_text,"")
    if (write_verification_aux!=str(0)):
        ics854s01i_write_check=ics854s01i_write_check+1
        
    #Verifica se foi capaz de enviar comandos através do método de leitura
    read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
    read_verification_aux=read_verification_aux.replace(read_verification_text,"")
    if (read_verification_aux!=str(0)):
        ics854s01i_read_check=ics854s01i_read_check+1

    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents()   
    
    print("Verificação...")
    
    pll_clk_sel_check_fmc_pin=0
    if(read_value!=write_value or read_value!=str(pll_clk_sel)):
        print("PLL_CLK_SEL : FAIL")
        print("Valor Enviado pelo Comando: ",pll_clk_sel)
        print("Valor Escrito :",write_value)
        print("Valor Lido: ",read_value)
        pll_clk_sel_check_fmc_pin=pll_clk_sel_check_fmc_pin+1
        
    if(pll_clk_sel_check_fmc_pin==0):
        print("PLL_CLK_SEL FROM FMC PIN (FMC_CLK LINE): OK")
        pll_clk_sel_fmc_pin_result="OK"
    else:
        print("PLL_CLK_SEL FROM FMC PIN (FMC_CLK LINE): FAIL")
        pll_clk_sel_fmc_pin_result="FAIL"
        
    if (pll_clk_sel_mmcx_result!="OK" or pll_clk_sel_fmc_pin_result!="OK"):
        ics854s01i_result="FAIL"
        print("Teste do ICS854S01I: FAIL")
    else:
        ics854s01i_result="OK"
        print("Teste do ICS854S01I: OK")   
        
    if(ics854s01i_write_check!=0):
        ics854s01i_write_check_result = "FAIL"
        print("Utilizacao do método de Escrita: ",ics854s01i_write_check_result)
    else:
        ics854s01i_write_check_result = "OK"  
        print("Utilizacao do método de Escrita: ",ics854s01i_write_check_result)
        
 
    if(ics854s01i_read_check!=0):
        ics854s01i_read_check_result = "FAIL"
        print("Utilizacao do método de Leitura: ",ics854s01i_read_check_result)
    else:
        ics854s01i_read_check_result = "OK"  
        print("Utilizacao do método de Leitura: ",ics854s01i_read_check_result)   

        
    ics854s01i_log.append("Valor Enviado pelo Comando: "+str(pll_clk_sel))
    ics854s01i_log.append("Valor Escrito : "+str(write_value))
    ics854s01i_log.append("Valor Lido : "+str(read_value))
    ics854s01i_log.append("Utilizacao do metodo de Escrita: "+str(ics854s01i_write_check_result))
    ics854s01i_log.append("Utilizacao do metodo de Leitura: "+str(ics854s01i_read_check_result))    
    ics854s01i_log.append("FINAL RESULT: "+str(ics854s01i_result))
        
    end_time=datetime.datetime.now()
    end_time_str=end_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim do Teste do ICS854S01I")
    print("End_write_time:",end_time_str)
    duracao=((end_time - start_time).total_seconds())/60
    print("Duração do Teste: ",round(duracao,4))
    
 

    return (ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,ics854s01i_log)