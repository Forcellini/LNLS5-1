from subprocess import Popen,PIPE
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import time

def ddr3(tela_leds,check_fpga):
    
    tela_leds.ui.progressBar.setValue(0)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    local="cd TESTE_AUTOMATIZADO_DDR3/arquivos_fpga/\n"
    comando3="sh TESTE_AUTOMATIZADO_DDR3/script2g.sh"
    '''local="cd TESTE_AUTOMATIZADO_DDR3/arquivos_fpga/\n"
    comando1="impact -batch fpga_fase1"
    comando2="impact -batch fpga_fase2"
    comando3="sh TESTE_AUTOMATIZADO_DDR3/script2g.sh"
    
    if(check_fpga==True):
        #Fase 1 da Gravação da FPGA
        command_stdout = Popen(local+comando1,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()
        
        fpga_str = 'Cable connection established'
        check_fpga = fpga_str in str(command_stdout)
        if(check_fpga==True):
            print("Fase 1 de 2 da Gravação da FPGA: Completa")
        else:
            print("Encerrando o Programa...falha na Gravação da FPGA Fase 1")
            sys.exit()
        
        #Fase 2 da Gravação da FPGA
        command_stdout = Popen(local+comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()
        
        fpga_str = 'Programmed successfully'
        check_fpga = fpga_str in str(command_stdout)
        if(check_fpga==True):
            print("Fase 2 de 2 da Gravação da FPGA: Completa")
            print("FPGA Gravada com Sucesso!")
        else:
            print("Encerrando o Programa...falha na Gravação da FPGA Fase 2")
            sys.exit()
    
    else:
        print("FPGA: Opcao nao selecionada")'''
    if (check_fpga==False):
        print("Warning: FPGA NAO SELECIONADA")
            
    
    tela_leds.ui.progressBar.setValue(15)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    #Teste da Memória DDR3
    Popen(["gnome-terminal"])
    command_stdout=Popen(comando3,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()
    
    time.sleep(2800)
    
    tela_leds.ui.progressBar.setValue(95)  
    tela_leds.repaint()
    QApplication.processEvents()
    #Verificação dos resultados obtidos
    infile = r"TESTE_AUTOMATIZADO_DDR3/history.log"
    
    important_written = []
    keep_phrases_written = ["of 32 WRITTEN"]
    with open(infile) as f:
        f = f.readlines()
    
    for line in f:
        for phrase in keep_phrases_written:
            if phrase in line:
                important_written.append(line)
                break
    
    print("Número de Blocos ESCRITOS:",len(important_written))
    
    
    important_read = []
    keep_phrases_read = ["of 32 READ "]
    with open(infile) as f:
        f = f.readlines()
    
    for line in f:
        for phrase in keep_phrases_read:
            if phrase in line:
                important_read.append(line)
                break
    print("Número de Blocos LIDOS:",len(important_read))
    
    important_final_result = []
    keep_phrases_final_result = ["END OF PROGRAM: SUCCESS!"]
    with open(infile) as f:
        f = f.readlines()
    
    for line in f:
        for phrase in keep_phrases_final_result:
            if phrase in line:
                important_final_result.append(line)
                break
    print("Resultado do Success:",len(important_final_result))
    
    important_num_of_bytes = []
    keep_phrases_num_of_bytes = ["NUM OF BYTES:"]
    with open(infile) as f:
        f = f.readlines()
    
    for line in f:
        for phrase in keep_phrases_num_of_bytes:
            if phrase in line:
                important_num_of_bytes.append(line)
                break
    print("Resultado do Num_of_Bytes:",len(important_num_of_bytes))
    texto_num_bytes="NUM OF BYTES: "
    
    print(important_num_of_bytes)
    if(len(important_num_of_bytes)==1):
        ddr3_num_of_bytes=important_num_of_bytes[0].replace(texto_num_bytes,"")
        ddr3_num_of_bytes=ddr3_num_of_bytes.replace("\n","")
    else:
        ddr3_num_of_bytes="-"
    
    ddr3_num_of_reads=len(important_read)
    ddr3_num_of_writes=len(important_written)
    
    if(len(important_num_of_bytes)==1):
        ddr3_total_num_of_bytes=int(ddr3_num_of_bytes)*int(ddr3_num_of_reads)
    else:
        ddr3_total_num_of_bytes="-"
    final_result=len(important_final_result)
    
    
    if(final_result==1):
        ddr3_aprovacao="OK"
        ddr3_result="DDR3 AFC - RESULTADO DO TESTE: OK"
        tela_leds.ui.kled_DDR3.setState(1)
        tela_leds.ui.kled_DDR3.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led DDR3",tela_leds.repaint())
        print("Led DDR3",QApplication.processEvents())  
    else:
        ddr3_aprovacao="FAIL"
        ddr3_result="DDR3 AFC - RESULTADO DO TESTE: FAIL"
        tela_leds.ui.kled_DDR3.setState(1)
        tela_leds.ui.kled_DDR3.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led DDR3",tela_leds.repaint())
        print("Led DDR3",QApplication.processEvents())        
        
    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    return(ddr3_aprovacao,ddr3_result,ddr3_num_of_reads,ddr3_num_of_writes,ddr3_num_of_bytes,ddr3_total_num_of_bytes)
    



