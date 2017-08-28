from subprocess import Popen,PIPE
import sys
import paramiko
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import time

SLEEP_TIME = 5.0

def fpga(gravar_fpga_check,IP_CRATE,USERNAME,PASSWORD,POSITION_CRATE,tela_leds):
    if (gravar_fpga_check==True):
        print("Iniciou a Gravação da FPGA")
        local = "cd Fpga/impact_fpga\n"
        comando1="impact -batch gravar_arquivo_svf_script"
        comando2="impact -batch gravar_arquivo_bit_script"

        tela_leds.ui.progressBar.setValue(0)  
        tela_leds.repaint()
        QApplication.processEvents() 
            
        command_stdout = Popen(local+comando1,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()
        fpga_str = 'Cable connection established'
        check_fpga = fpga_str in str(command_stdout)
        if(check_fpga==True):
            print("Fase 1 de 2 da Gravação da FPGA: Completa")
            tela_leds.ui.progressBar.setValue(10)  
            tela_leds.repaint()
            QApplication.processEvents() 
        else:
            print("Fase 1 de 2 da Gravação da FPGA: FAIL")
            print(command_stdout)
            print("Encerrando o Programa...")
            tela_leds.ui.kled_fpga.setState(1)
            tela_leds.ui.kled_fpga.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print(tela_leds.repaint())
            print(QApplication.processEvents())
            time.sleep(SLEEP_TIME)
            sys.exit()
            sys.exit()

        command_stdout = Popen(local+comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()

        fpga_str = 'Programmed successfully'
        
        check_fpga = fpga_str in str(command_stdout)
        if(check_fpga==True):
            print("Fase 2 de 2 da Gravação da FPGA: Completa")
            print("FPGA Gravada com Sucesso!")
            
            tela_leds.ui.progressBar.setValue(70)  
            tela_leds.repaint()
            QApplication.processEvents() 
            #FIXME: Isto ocorre pois algumas vezes ao gravarmos a FPGA o CRATE não reconhece a fpga...
            print("Verificando se a FPGA foi reconhecida no CRATE...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IP_CRATE, username=str(USERNAME), password=str(PASSWORD))
            stdin, stdout, stderr  = ssh.exec_command('cd /dev/;ls')
            stdin.flush()
            fpga_line=stdout.readlines()
            fgpa_str = 'fpga\n'
            fpga_check = fgpa_str in fpga_line
            if(fpga_check==True):
                print("FPGA reconhecida!")
                tela_leds.ui.progressBar.setValue(100)  
                tela_leds.repaint()
                QApplication.processEvents() 
            else:
                print("FPGA nao reconhecida!")
                print("Encerrando o programa...")
                tela_leds.ui.kled_fpga.setState(1)
                tela_leds.ui.kled_fpga.setColor(QtGui.QColor(255, 0, 0))
                tela_leds.repaint()
                QApplication.processEvents()
                print(tela_leds.repaint())
                print(QApplication.processEvents())
                time.sleep(SLEEP_TIME)
                sys.exit()
        else:
            print("Fase 2 de 2 da Gravação da FPGA: FAIL")
            print(command_stdout)
            print("Encerrando o Programa...")
            tela_leds.ui.kled_fpga.setState(1)
            tela_leds.ui.kled_fpga.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.repaint()
            QApplication.processEvents()
            print(tela_leds.repaint())
            print(QApplication.processEvents())
            time.sleep(SLEEP_TIME)
            sys.exit()
            
    fpga_str_result="FPGA: Gravacao realizada com sucesso"
            
        
    return (fpga_str_result)
        