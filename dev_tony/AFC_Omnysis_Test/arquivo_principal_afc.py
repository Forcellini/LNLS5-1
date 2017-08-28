from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QDateTime,QTimer
import  sys
from list_rw_file3 import list_to_file
import time

import interface_leds_afc
import interface_main_afc
import interface_results_afc

import time
import datetime
from eeprom_afc import eeprom_afc
from Communication import start_communication
from sensores_ipmi_py27 import sensores_ipmi
from ddr3 import ddr3
from subprocess import Popen,PIPE
import sys



#PRIMEIRA JANELA - MAIN AFC
class TestWindow_AFC(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = interface_main_afc.Ui_MainWindow() 
        self.ui.setupUi(self) 
        self.ui.INICIAR_TESTE_BUTTON.clicked.connect(self.Start_Simulation)
        self.ui.CLOSE_BUTTON.clicked.connect(self.Stop_Simulation)
        self.SEGUNDA_JANELA = SEGUNDA_JANELA(self)
        self.TERCEIRA_JANELA = TERCEIRA_JANELA(self)
        start_time_general=QDateTime.currentDateTime()
        self.ui.dateTimeEdit.setDateTime(start_time_general)
    
    def Stop_Simulation(self):
        self.close()
           
    def Start_Simulation(self):
        print("Realizar a aquisição dos dados da interface principal")
        
        ip_crate=self.ui.IP_CRATE.text()
        check_eeprom=self.ui.CHECK_EEPROM.isChecked()
        check_ddr3=self.ui.CHECK_DDR3.isChecked()
        check_sensores_ipmi=self.ui.CHECK_SENSORES_IPMI.isChecked()
        check_fpga = self.ui.checkBox_FPGA.isChecked()
        
        #Informações Gerais
        operador=self.ui.OPERADOR.text()
        n_serie_afc=self.ui.N_SERIE_AFC.text()

        #Horário de Inicío do Teste        
        start_time_general=datetime.datetime.now() #serve para cálculos de tempo

        datapath_save="result/"
        serial_number="111111111"

        
        (eeprom_afc_aprovacao,eeprom_total_valores,eeprom_valores_corretos,eeprom_valores_problemas,
         sensores_ipmi_data_type,sensores_ipmi_data_value,sensores_ipmi_data_units,sensores_ipmi_medicao,sensores_ipmi_aprovacao,
         ddr3_aprovacao,ddr3_num_of_reads,ddr3_num_of_writes,ddr3_num_of_bytes,ddr3_total_num_of_bytes)=self.SEGUNDA_JANELA.metodo_afc_execucao_testes(ip_crate,check_eeprom,check_ddr3,check_sensores_ipmi,check_fpga,datapath_save,serial_number,start_time_general,n_serie_afc,operador)
        
        stop_time_general=QDateTime.currentDateTime()
        self.TERCEIRA_JANELA.ui.dateTimeEdit.setDateTime(stop_time_general)
        
        #EEPROM TEST
        self.TERCEIRA_JANELA.ui.EEPROM_RESULTADO_FINAL.setText(eeprom_afc_aprovacao)
        self.TERCEIRA_JANELA.ui.EEPROM_NUM_POSICOES.setText(str(eeprom_total_valores))
        self.TERCEIRA_JANELA.ui.EEPROM_NUM_CORRETOS.setText(str(eeprom_valores_corretos))
        self.TERCEIRA_JANELA.ui.EEPROM_NUM_PROBLEMAS.setText(str(eeprom_valores_problemas))
        
        #SENSORES IPMI TEST
        if(sensores_ipmi_aprovacao=="Teste não realizado"):
            self.TERCEIRA_JANELA.ui.SENSORES_IPMI_RESULTADO.setText(sensores_ipmi_aprovacao)
            for i in range (0,63):
                self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,0, QtGui.QTableWidgetItem("-"))
                self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,1, QtGui.QTableWidgetItem("-"))
                self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,2, QtGui.QTableWidgetItem("-"))
                self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,3, QtGui.QTableWidgetItem("-"))
        
        else:
            self.TERCEIRA_JANELA.ui.SENSORES_IPMI_RESULTADO.setText(sensores_ipmi_aprovacao)
            if (sensores_ipmi_aprovacao=="OK"):
                for i in range (0,len(sensores_ipmi_data_type)):
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,0, QtGui.QTableWidgetItem(str(sensores_ipmi_medicao[i])))
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,1, QtGui.QTableWidgetItem(str(sensores_ipmi_data_type[i])))
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,2, QtGui.QTableWidgetItem(str(sensores_ipmi_data_value[i])))
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,3, QtGui.QTableWidgetItem(str(sensores_ipmi_data_units[i])))
            else:
                for i in range (0,len(sensores_ipmi_data_type)):
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,0, QtGui.QTableWidgetItem("-"))
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,1, QtGui.QTableWidgetItem("-"))
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,2, QtGui.QTableWidgetItem("-"))
                    self.TERCEIRA_JANELA.ui.SENSORES_IPMI_TABELA.setItem(i,3, QtGui.QTableWidgetItem("-"))
                 
        #DDR3 TEST
        self.TERCEIRA_JANELA.ui.DDR3_NUM_ESCRITOS.setText(str(ddr3_num_of_writes))
        self.TERCEIRA_JANELA.ui.DDR3_NUM_LIDOS.setText(str(ddr3_num_of_reads))
        self.TERCEIRA_JANELA.ui.DDR3_RESULTADO_FINAL.setText(str(ddr3_aprovacao))
        self.TERCEIRA_JANELA.ui.DDR3_NUM_BYTES.setText(str(ddr3_num_of_bytes))
        self.TERCEIRA_JANELA.ui.DDR3_NUM_BYTES_TOTAL.setText(str(ddr3_total_num_of_bytes))
                
        
        
        
        self.TERCEIRA_JANELA.show()
        
        
        

#SEGUNDA JANELA - LEDS
class SEGUNDA_JANELA(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = interface_leds_afc.Ui_Dialog()
        self.ui.setupUi(self) 
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.ui.OK_BUTTON_LEDS.clicked.connect(self.close_button)
                
    def metodo_afc_execucao_testes(self,ip_crate,check_eeprom,check_ddr3,check_sensores_ipmi,check_fpga,datapath_save,serial_number,start_time_general,n_serie_afc,operador):
        
        self.open()
        self.repaint()
        QApplication.processEvents()
        
        
        #Iniciar todos os LEDs apagados
        self.ui.kled_CRATE.setState(0)
        self.ui.kled_DDR3.setState(0)
        self.ui.kled_EEPROM.setState(0)
        self.ui.kled_SENSORES_IPMI.setState(0)
        self.ui.kled_FPGA.setState(0)
        
        self.ui.kled_CRATE.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_DDR3.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_EEPROM.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_SENSORES_IPMI.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_FPGA.setColor(QtGui.QColor(0, 255, 0))
        
        self.repaint()
        QApplication.processEvents()
        
        #Verifica a comunicação com o CRATE (em caso de falha, o programa fechará)
        start_communication(ip_crate, self)
        
        
        local="cd TESTE_AUTOMATIZADO_DDR3/arquivos_fpga/\n"
        comando1="impact -batch fpga_fase1"
        comando2="impact -batch fpga_fase2"
        comando3="sh TESTE_AUTOMATIZADO_DDR3/script2g.sh"
    
        if(check_fpga==True):
           
            self.ui.progressBar.setValue(0)  
            self.ui.kled_FPGA.setState(1)
            self.ui.kled_FPGA.setColor(QtGui.QColor(255, 255, 0))
            
            self.repaint()
            QApplication.processEvents()
            print("Led FPGA",self.repaint())
            print("Led FPGA",QApplication.processEvents())

            #Fase 1 da Gravação da FPGA
            command_stdout = Popen(local+comando1,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
        
            fpga_str = 'Cable connection established'
            check_fpga = fpga_str in str(command_stdout)
            if(check_fpga==True):
                print("Fase 1 de 2 da Gravação da FPGA: Completa")
            else:
                print("Encerrando o Programa...falha na Gravação da FPGA Fase 1")
                self.ui.kled_FPGA.setState(1)
                self.ui.kled_FPGA.setColor(QtGui.QColor(255, 0, 0))
                self.repaint()
                QApplication.processEvents()
                print("Led FPGA",self.repaint())
                print("Led FPGA",QApplication.processEvents())
                fpga_status="FAIL"
                time.sleep(5.0)
                sys.exit()
            
            self.ui.progressBar.setValue(30)  
            self.repaint()
            QApplication.processEvents()
            #Fase 2 da Gravação da FPGA
            command_stdout = Popen(local+comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            
            fpga_str = 'Programmed successfully'
            check_fpga = fpga_str in str(command_stdout)
            if(check_fpga==True):
                print("Fase 2 de 2 da Gravação da FPGA: Completa")
                print("FPGA Gravada com Sucesso!")
                self.ui.kled_FPGA.setState(1)
                self.ui.kled_FPGA.setColor(QtGui.QColor(0, 255, 0))
                self.ui.progressBar.setValue(100)
                self.repaint()
                QApplication.processEvents()
                print("Led FPGA",self.repaint())
                print("Led FPGA",QApplication.processEvents())
                fpga_status="OK"
                

            else:
                fpga_status="FAIL"
                print("Encerrando o Programa...falha na Gravação da FPGA Fase 2")
                self.ui.kled_FPGA.setState(1)
                self.ui.kled_FPGA.setColor(QtGui.QColor(255, 0, 0))
                self.repaint()
                QApplication.processEvents()
                print("Led FPGA",self.repaint())
                print("Led FPGA",QApplication.processEvents())
                time.sleep(5.0)
                sys.exit()
        
        else:
            print("FPGA: Opcao nao selecionada")
            fpga_status="FPGA: Opcao nao selecionada"
        
        #TESTE DA EEPROM
        if (check_eeprom==True):
            self.ui.kled_EEPROM.setState(1)
            self.ui.kled_EEPROM.setColor(QtGui.QColor(255, 255, 0))
            self.repaint()
            QApplication.processEvents()
            print("Led EEPROM",self.repaint())
            print("Led EEPROM",QApplication.processEvents())
            (eeprom_afc_aprovacao,eeprom_afc_result,eeprom_total_valores,eeprom_valores_corretos,eeprom_valores_problemas,
             posicao_memoria_str,valores_escrito_padrao,valores_lidos)=eeprom_afc(self,ip_crate)
        else:
            eeprom_afc_result="EEPROM_AFC - TESTE NÃO REALIZADO"
            eeprom_afc_aprovacao="Teste não realizado"
            eeprom_total_valores="-"
            eeprom_valores_corretos="-"
            eeprom_valores_problemas="-"
            posicao_memoria_str="-"
            valores_escrito_padrao="-"
            valores_lidos="-"
            print(eeprom_afc_result)
            self.ui.kled_EEPROM.setState(1)
            self.ui.kled_EEPROM.setColor(QtGui.QColor(0, 0, 255))
            self.repaint()
            QApplication.processEvents()
            print("Led EEPROM",self.repaint())
            print("Led EEPROM",QApplication.processEvents())
        
        #TESTE DOS SENSORES IPMI    
        if (check_sensores_ipmi==True):
            self.ui.kled_SENSORES_IPMI.setState(1)
            self.ui.kled_SENSORES_IPMI.setColor(QtGui.QColor(255, 255, 0))
            self.repaint()
            QApplication.processEvents()
            print("Led SENSORES IPMI",self.repaint())
            print("Led SENSORES IPMI",QApplication.processEvents())
            (sensores_ipmi_data_type,sensores_ipmi_data_value,sensores_ipmi_data_units,sensores_ipmi_medicao,sensores_ipmi_aprovacao,sensores_ipmi_result)=sensores_ipmi(self)
        else:
            sensores_ipmi_result="SENSORES IPMI - TESTE NÃO REALIZADO"
            sensores_ipmi_aprovacao="Teste não realizado"
            sensores_ipmi_data_type="-"
            sensores_ipmi_data_value="-"
            sensores_ipmi_data_units="-"
            sensores_ipmi_medicao="-"
            print(sensores_ipmi_result)
            self.ui.kled_SENSORES_IPMI.setState(1)
            self.ui.kled_SENSORES_IPMI.setColor(QtGui.QColor(0, 0, 255))
            self.repaint()
            QApplication.processEvents()
            print("Led SENSORES IPMI",self.repaint())
            print("Led SENSORES IPMI",QApplication.processEvents())
            
        #TESTE DA DDR3
        if (check_ddr3==True):
            self.ui.kled_DDR3.setState(1)
            self.ui.kled_DDR3.setColor(QtGui.QColor(255, 255, 0))
            self.repaint()
            QApplication.processEvents()
            print("Led DDR3",self.repaint())
            print("Led DDR3",QApplication.processEvents())
            (ddr3_aprovacao,ddr3_result,ddr3_num_of_reads,ddr3_num_of_writes,ddr3_num_of_bytes,ddr3_total_num_of_bytes)=ddr3(self,check_fpga)
        else:
            ddr3_result="DDR3 - TESTE NÃO REALIZADO"
            ddr3_aprovacao="Teste não realizado"
            ddr3_num_of_reads="-"
            ddr3_num_of_writes="-"
            ddr3_num_of_bytes="-"
            ddr3_total_num_of_bytes="-"
            print(ddr3_result)
            self.ui.kled_DDR3.setState(1)
            self.ui.kled_DDR3.setColor(QtGui.QColor(0, 0, 255))
            self.repaint()
            QApplication.processEvents()
            print("Led DDR3",self.repaint())
            print("Led DDR3",QApplication.processEvents())
    
        #Horário de Inicío do Teste        
        start_time_general_str=start_time_general.strftime("%Y-%m-%d %H:%M:%S")
        
        stop_time_general=datetime.datetime.now() #serve para cálculos de tempo
        stop_time_general_str=stop_time_general.strftime("%Y-%m-%d %H:%M:%S")
               
        duracao_teste=((stop_time_general - start_time_general).total_seconds())/60
        
        #Salva os resultados finais
        result=[]
        result.append("Teste da Placa: AFC\n\n")
        result.append("Operador: "+str(operador))
        result.append("Número de Série: "+str(n_serie_afc))
        result.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result.append("Duração do Teste: "+str(round(duracao_teste,4))+" min\n")
        result.append("FPGA Status: "+str(fpga_status)+"\n")
        result.append("Resultados:")
        result.append(eeprom_afc_result)
        result.append("EEPROM AFC - NÚMERO DE POSIÇÕES DA MEMÓRIA TESTADA: "+str(eeprom_total_valores))
        result.append("EEPROM AFC - NÚMERO DE POSIÇÕES DA MEMÓRIA FUNCIONANDO: "+str(eeprom_valores_corretos))
        result.append("EEPROM AFC - NÚMERO DE POSIÇÕES DA MEMÓRIA COM PROBLEMAS: "+str(eeprom_valores_problemas))
        result.append(sensores_ipmi_result)
        result.append(ddr3_result)
        result.append("DDR3 AFC - NÚMERO DE BYTES LIDOS POR BLOCO: "+str(ddr3_num_of_bytes))      
        print(ddr3_num_of_bytes)
        result.append("DDR3 AFC - NÚMERO DE BLOCOS ESCRITOS : "+str(ddr3_num_of_writes))
        result.append("DDR3 AFC - NÚMERO DE BLOCOS LIDOS: "+str(ddr3_num_of_reads))
        result.append("DDR3 AFC - TOTAL DE POSICOES DA MEMORIA TESTADA: "+str(ddr3_total_num_of_bytes))
        list_to_file(0,result, datapath_save + serial_number + "_result_afc_test.txt")   
        
        
        #Armazena os valores adquiridos do teste da EEPROM
        result_eeprom_values=[]
        result_eeprom_values.append("Teste da Placa: AFC - Dados do Componente EEPROM\n\n")
        result_eeprom_values.append("Número de Série: "+str(serial_number))
        result_eeprom_values.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_eeprom_values.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_eeprom_values.append("Duração do Teste: "+str(round(duracao_teste,4))+" min\n\n")
        result_eeprom_values.append("Valores Adquiridos:")
        result_eeprom_values.append("Pos. Memória    Valor Escrito    Valor Lido")
        for i in range (0,len(posicao_memoria_str)):
            result_eeprom_values.append("    "+str(posicao_memoria_str[i])+"            "+str(valores_escrito_padrao[i])+"                "+str(valores_lidos[i]))

        list_to_file(0,result_eeprom_values, datapath_save + serial_number + "_result_eeprom_values.txt")  
        
        #Armazena os valores adquiridos do teste do SENSORES IPMI
        result_sensores_ipmi_values=[]
        result_sensores_ipmi_values.append("Teste da Placa: AFC - Dados dos SENSORES IPMI\n\n")
        result_sensores_ipmi_values.append("Número de Série: "+str(serial_number))
        result_sensores_ipmi_values.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_sensores_ipmi_values.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_sensores_ipmi_values.append("Duração do Teste: "+str(round(duracao_teste,4))+" min\n\n")
        result_sensores_ipmi_values.append("Valores Adquiridos:")
        result_sensores_ipmi_values.append("Medicao      Variavel               Valor Lido              Unidade")
        
        for i in range (0,len(sensores_ipmi_medicao)):
            frase="    "+str(sensores_ipmi_medicao[i]).ljust(2)+"    "+str(sensores_ipmi_data_type[i]).ljust(16)+"            "+str(sensores_ipmi_data_value[i]).ljust(8)+"                "+str(sensores_ipmi_data_units[i])
            result_sensores_ipmi_values.append(frase)

        list_to_file(0,result_sensores_ipmi_values, datapath_save + serial_number + "_result_sensores_ipmi_values.txt")  
        
        
        
        
        self.ui.progressBar.setValue(100)  
        self.repaint()
        QApplication.processEvents()
        
        return(eeprom_afc_aprovacao,eeprom_total_valores,eeprom_valores_corretos,eeprom_valores_problemas,
               sensores_ipmi_data_type,sensores_ipmi_data_value,sensores_ipmi_data_units,sensores_ipmi_medicao,sensores_ipmi_aprovacao,
               ddr3_aprovacao,ddr3_num_of_reads,ddr3_num_of_writes,ddr3_num_of_bytes,ddr3_total_num_of_bytes)
    
        
      
    def close_button(self):
        self.close()
        #TERCEIRA_JANELA(self).show()
        
        
    
#TERCEIRA JANELA - RESULTADOS
class TERCEIRA_JANELA(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = interface_results_afc.Ui_Dialog()
        self.ui.setupUi(self) 
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.ui.OK_BUTTON_RESULTS.clicked.connect(self.OK_BUTTON_TERCEIRA_JANELA)
        
    def OK_BUTTON_TERCEIRA_JANELA(self):
        self.close()
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TestWindow_AFC()
    window.show()
    sys.exit(app.exec_())
