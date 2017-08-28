from subprocess import Popen, PIPE
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def eeprom(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds):

    local = "cd CRATE_ACESSO/bpm-app/.halcs-libs/examples\n"
    
    
    #Para escrever todos os valores possíveis em 2 Bytes [00 - FF]
    j=0
    eeprom_all_values_hex=[]
    eeprom_all_values_dec=[]
    #Máximo de posições na memória que devo escrever/ler na eeprom é a posição 8191 
    #Os valors all_values_hex são os valores que serão mostrados como escritos pelo crate
    #pois o código do LNLS mostra o valor que foi escrito em hexadecimal
    #convertendo o valor de decimal (entrada do usuário) para um valor em hexadecimal (saída no terminal)
    
    while (j<8192):
        i=0
        while(i<256):
            eeprom_all_values_hex.append(format(i,'02x').upper())
            eeprom_all_values_dec.append(i)
            i=i+1
        j=j+i
    
    #Posições na memória em hexadecimal
    eeprom_memory_position_standard_hex=[]
    i=0
    
    while (i<8192):
        eeprom_memory_position_standard_hex.append(format(i,'02x').upper())
        i=i+1
    
    print("Iniciou a ESCRITA na EEPROM do ADC")
    start_write_time=datetime.datetime.now()
    start_write_time_str=start_write_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Start_write_time:",start_write_time_str)
    
    memory_text="MEMORY ADDRESS: 0x"
    write_text="WRITTEN VALUE: 0x"
    write_verification_text="WRITE CHECK: "
    read_verification_text="READ CHECK: "
    
    memory_position_write=[]
    eeprom_value_write=[]
    write_verification=[]
    address=0
    eeprom_memory_position_standard_dec=[]
    
    while (address<len(eeprom_all_values_dec)):
        command_write= "./THALES_fmc130m_eeprom_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -rw 1 -addr "+str(address) +" -data "+str(eeprom_all_values_dec[address])
        command_stdout_write = Popen(local+command_write,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout_write=command_stdout_write.splitlines()
        memory_position_aux=command_stdout_write[len(command_stdout_write)-2].decode("utf-8")
        memory_position_aux=memory_position_aux.replace(memory_text,"")
        value_aux=command_stdout_write[len(command_stdout_write)-1].decode("utf-8")
        value_aux=value_aux.replace(write_text,"")
        memory_position_write.append(memory_position_aux)
        eeprom_value_write.append(value_aux)
        eeprom_memory_position_standard_dec.append(address)
        
        #Verifica se foi capaz de enviar comandos através do método de escrita
        write_verification_aux=command_stdout_write[len(command_stdout_write)-3].decode("utf-8")
        write_verification_aux=write_verification_aux.replace(write_verification_text,"")
        write_verification.append(write_verification_aux)
        
        
        tela_leds.ui.progressBar.setValue((address*50)/len(eeprom_all_values_dec))  
        tela_leds.repaint()
        QApplication.processEvents()
        address=address+1
    
    end_write_time=datetime.datetime.now()
    end_write_time_str=end_write_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim da ESCRITA na EEPROM do ADC")
    print("End_write_time:",end_write_time_str)
    
   
    print("Iniciou a LEITURA na EEPROM do ADC")
    start_read_time=datetime.datetime.now()
    start_read_time_str=start_read_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Start_read_time:",start_read_time_str)
    read_text="VALUE READ: 0x"
    memory_position_read=[]
    eeprom_value_read=[]
    read_verification=[]
    address=0
    
    while (address<len(eeprom_all_values_dec)):
        command_read= "./THALES_fmc130m_eeprom_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -rw 0 -addr "+str(address)
        command_stdout_read = Popen(local+command_read,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout_read=command_stdout_read.splitlines()
        memory_position_aux=command_stdout_read[len(command_stdout_read)-2].decode("utf-8")
        memory_position_aux=memory_position_aux.replace(memory_text,"")
        value_aux=command_stdout_read[len(command_stdout_read)-1].decode("utf-8")
        value_aux=value_aux.replace(read_text,"")
        memory_position_read.append(memory_position_aux)
        eeprom_value_read.append(value_aux)
        
        #Verifica se foi capaz de enviar comandos através do método de escrita
        read_verification_aux=command_stdout_read[len(command_stdout_read)-3].decode("utf-8")
        read_verification_aux=read_verification_aux.replace(read_verification_text,"")
        read_verification.append(read_verification_aux)
        
        tela_leds.ui.progressBar.setValue((address*50)/len(eeprom_all_values_dec)+50)  
        tela_leds.repaint()
        QApplication.processEvents()        
        
        address=address+1
    
    end_read_time=datetime.datetime.now()
    end_read_time_str=end_read_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim da LEITURA na EEPROM do ADC")
    print("End_read_time:",end_read_time_str)
    
    print("Verificação das memórias da eeprom...")
    start_check_time=datetime.datetime.now()
    start_check_time_str=start_check_time.strftime("%Y-%m-%d %H:%M:%S")
    memory_test_check=0
    for i in range (0, len(eeprom_all_values_dec)):
        if (memory_position_read[i]!=memory_position_write[i] or memory_position_read[i]!=eeprom_memory_position_standard_hex[i]):
        #if (memory_position_read[i]!=memory_position_standard_hex[i]):
            print("Memória Acessada Escrita/Leitura Diferem - Posição: ",i)
            print(memory_position_read[i],memory_position_write[i],eeprom_memory_position_standard_hex[i])
            memory_test_check=memory_test_check+1
    
    value_test_check=0
    for i in range (0, len(eeprom_all_values_dec)):
        if (eeprom_value_read[i]!=eeprom_value_write[i] or eeprom_value_read[i]!=eeprom_all_values_hex[i]):
        #if (value_read[i]!=all_values_hex[i]):
            print("Valor Escrito/Lido com Diferem - Posição: ",i)
            print(eeprom_value_read[i],eeprom_value_write[i],eeprom_all_values_hex[i])
            value_test_check=value_test_check+1    
    
    end_check_time=datetime.datetime.now()
    end_check_time_str=end_check_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim da Teste da EEPROM do ADC")
    print("Start_check_time:",start_check_time_str)
    print("End_check_time:",end_check_time_str)
    
    duration_write=((end_write_time - start_write_time).total_seconds())/60
    duration_read=((end_read_time - start_read_time).total_seconds())/60
    duration_check=((end_check_time - start_check_time).total_seconds())/60
    duration_global=((end_check_time - start_write_time).total_seconds())/60
    
    print("Duracao do Teste de ESCRITA:",round(duration_write,4))
    print("Duracao do Teste de LEITURA:",round(duration_read,4))
    print("Duracao do Teste de CHECK:",round(duration_check,4))
    print("Duracao do Teste TOTAL:",round(duration_global,4))
    
    if(memory_test_check==0):
        print("Memórias Acessadas: OK")
    else:
        print("Memórias Acessadas: FAIL")
    
    if(value_test_check==0):
        print("Valores Escritos/Lidos: OK")
    else:
        print("Valores Escritos/Lidos: FAIL")
    
    
    eeprom_write_check=0
    eeprom_read_check=0
    i=0
    for i in range (0, len(eeprom_value_write)):
        if(write_verification[i]!=str(0)):
            eeprom_write_check=eeprom_write_check+1
            
        if(read_verification[i]!=str(0)):
            eeprom_read_check=eeprom_read_check+1
            
    if(eeprom_write_check==0):
        print("Utilizacao do método de Escrita: OK")
        eeprom_write_check_result="OK"
    else:
        print("Utilizacao do método de Escrita: FAIL")
        print(eeprom_write_check)
        eeprom_write_check_result="FAIL"
    
    if(eeprom_read_check==0):
        print("Utilizacao do método de Leitura: OK")
        eeprom_read_check_result="OK"
    else:
        print("Utilizacao do método de Leitura: FAIL")
        print(eeprom_read_check)
        eeprom_read_check_result="FAIL"

                
    if(value_test_check==0 and memory_test_check==0):
        eeprom_result ="OK"
        print("EEPROM: OK")
    else:
        eeprom_result="FAIL"
        print("EEPROM: FAIL")
    
    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents()       
    
    
    
       
    return(eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
           eeprom_all_values_dec,eeprom_all_values_hex,
           eeprom_memory_position_standard_dec,eeprom_memory_position_standard_hex,
           eeprom_value_write,eeprom_value_read)