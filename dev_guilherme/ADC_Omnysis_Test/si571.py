from subprocess import Popen, PIPE
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def si571(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds):
    
    local = "cd CRATE_ACESSO/bpm-app/.halcs-libs/examples\n"
    
    tela_leds.ui.progressBar.setValue(0)  
    tela_leds.repaint()
    QApplication.processEvents() 
       
    print("Iniciou o Teste do Si571")
    start_time=datetime.datetime.now()
    start_time_str=start_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Start_write_time:",start_time_str)
    
    si571_log=[]
   
    write_text="WRITTEN VALUE: "
    read_text="READ VALUE: "
    write_verification_text="WRITE CHECK: "
    read_verification_text="READ CHECK: "
    si571_write_check=0
    si571_read_check=0
    
    #Este valor ainda precisa ser melhor definido - 130000000 Hz
    freq_value=120000000
    
    command= "./THALES_si571_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -freq "+str(freq_value) 
    command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()
    write_aux=command_stdout[len(command_stdout)-2].decode("utf-8")
    write_value=write_aux.replace(write_text,"")
    read_aux=command_stdout[len(command_stdout)-1].decode("utf-8")
    read_value=read_aux.replace(read_text,"")
    
    tela_leds.ui.progressBar.setValue(50)  
    tela_leds.repaint()
    QApplication.processEvents() 
    
    #Verifica se foi capaz de enviar comandos através do método de escrita
    write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
    write_verification_aux=write_verification_aux.replace(write_verification_text,"")
    if (write_verification_aux!=str(0)):
        si571_write_check=si571_write_check+1
    
    #Verifica se foi capaz de enviar comandos através do método de leitura
    read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
    read_verification_aux=read_verification_aux.replace(read_verification_text,"")
    if (read_verification_aux!=str(0)):
        si571_read_check=si571_read_check+1    
    
    print("Verificação...")
    
    si571_check=0
    
    if(read_value!=write_value or read_value!=str(format(freq_value, '.6f'))):
        print("Valor Enviado pelo Comando: ",freq_value)
        print("Valor Escrito :",write_value)
        print("Valor Lido: ",read_value)
        si571_check=si571_check+1
        
    
    if(si571_check==0):
        print("Si571 Test: OK")
        si571_result="OK"
    else:
        print("Si571 Test: FAIL")
        si571_result="FAIL"    
    
    if(si571_write_check!=0):
        si571_write_check_result = "FAIL"
        print("Utilizacao do método de Escrita: ",si571_write_check_result)
    else:
        si571_write_check_result = "OK"  
        print("Utilizacao do método de Escrita: ",si571_write_check_result)
 
    if(si571_read_check!=0):
        si571_read_check_result = "FAIL"
        print("Utilizacao do método de Leitura: ",si571_read_check_result)
    else:
        si571_read_check_result = "OK"  
        print("Utilizacao do método de Leitura: ",si571_read_check_result)   
    
    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents() 
    
    end_time=datetime.datetime.now()
    end_time_str=end_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim da ESCRITA na EEPROM do ADC")
    print("End_write_time:",end_time_str)
    duracao=((end_time - start_time).total_seconds())/60
    print("Duração do Teste: ",round(duracao,4))
    
    si571_log.append("Valor Enviado pelo Comando: "+str(freq_value))
    si571_log.append("Valor Escrito: "+str(write_value))
    si571_log.append("Valor Lido: "+str(read_value))

    si571_log.append("Utilizacao do método de Escrita: "+str(si571_write_check_result))
    si571_log.append("Utilizacao do método de Leitura: "+str(si571_read_check_result))
    si571_log.append("FINAL RESULT: "+str(si571_result))

    return (si571_result,si571_write_check_result,si571_read_check_result,si571_log)