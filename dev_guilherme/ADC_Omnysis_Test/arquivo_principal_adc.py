import  sys
from PyQt4 import QtGui, QtCore
import interface_principal
import interface_resultado_final
from run_main_p_interface import run_main_p_interface
import interface_status_leds
import datetime
from PyQt4.QtGui import QApplication
#import teste_time #pode apagar depois
from PyQt4.QtCore import QDateTime,QTimer
from cis_configuration import cis_configuration
from list_rw_file2 import list_to_file_aux




#PRIMEIRA JANELA
class TestWindow_ADC(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = interface_principal.Ui_MainWindow() 
        self.ui.setupUi(self) 
        #Ação dos botões
        self.ui.START_BUTTON.clicked.connect(self.Start_Simulation)
        self.ui.STOP_BUTTON.clicked.connect(self.Stop_Simulation)
        self.ui.CONFIG_BUTTON.clicked.connect(self.Config_Simulation)
        self.janela_resultados = MyDialog(self)
        self.janela_resultados.ui.tabWidget.widget(0)
        self.janela_status_led = MyDialog_StatusLed(self)
        self.ui.dateTimeEdit_MainScreen.setDateTime(QDateTime.currentDateTime())

        
        #FIXME
        ###self.janela_resultados.ui.OK_BUTTON.clicked(self.ui.dateTimeEdit_MainScreen.setDateTime(QDateTime.currentDateTime()))       
        

        

    def Stop_Simulation(self):
        print ("Fecha Aplicação")
        exit()
        '''self.janela_teste.open()
        self.janela_teste.ui.lineEdit.setText("oi")
        qdate=QDateTime.currentDateTime()
        qdate_str=str(qdate.toString('dd.MM.yyyy hh:mm:ss'))
        self.janela_teste.ui.dateTimeEdit.setDateTime(qdate)
        self.janela_teste.ui.lineEdit.setText(qdate_str)
        self.janela_teste.ui.progressBar.setValue(10)
        #self.janela_teste.ui.dateTimeEdit.setQtCore'''
        
        
    def Start_Simulation(self):
        ip_crate = self.ui.IP_CRATE.text()
        ip_switch = self.ui.IP_SWITCH.text()
        ip_gerador_sinais_clock = self.ui.IP_GERADOR_SINAIS_CLOCK.text()
        ip_gerador_sinais_input = self.ui.IP_GERADOR_SINAIS_INPUT.text()
        posicao_AFC=int(self.ui.POSICAO_AFC.text())
        posicao_AD=int(self.ui.POSICAO_AD.text())
        freq_clock=float(self.ui.FREQ_CLOCK.text())
        freq_in=float(self.ui.FREQ_IN.text())
        amp_clock=float(self.ui.AMP_CLOCK.text())
        amp_in=float(self.ui.AMP_IN.text())
        freq_clock_missingcodes=float(self.ui.FREQ_CLOCK_MISSINGCODES.text())
        freq_in_missingcodes=float(self.ui.FREQ_IN_MISSINGCODES.text())
        amp_clock_missingcodes=float(self.ui.AMP_CLOCK_MISSINGCODES.text())
        amp_in_missingcodes=float(self.ui.AMP_IN_MISSINGCODES.text())
        perda_filtro_missingcodes=float(self.ui.PERDA_FILTRO_MISSINGCODES.text())
        pts_FFT=int(self.ui.N_FFT.text())
        pts_crate=int(self.ui.N_CRATE.text())
        pts_crate_missingcodes=int(self.ui.N_CRATE_MISSINGCODES.text())
        n_requisicoes=int(self.ui.N_REQUISICOES.text())
        snr_criterio=float(self.ui.SNR_CRITERIO.text())
        sfdr_criterio=float(self.ui.SFDR_CRITERIO.text())
        enob_criterio=float(self.ui.ENOB_CRITERIO.text())
        crosstalk_criterio=float(self.ui.CROSSTALK_CRITERIO.text())
        missingcode_criterio=int(self.ui.MISSINGCODE_CRITERIO.text())
        dif_amp_criterio=float(self.ui.DIF_AMPL_CRITERIO.text())
        all_tests_selection = self.ui.check_all.isChecked()
        snr_check=self.ui.check_snr.isChecked()
        enob_check=self.ui.check_enob.isChecked()
        sfdr_check=self.ui.check_sfdr.isChecked()
        crosstalk_check=self.ui.check_crosstalk.isChecked()
        missingcodes_check=self.ui.check_missingcodes.isChecked()
        dif_ampl_check=self.ui.check_dif_ampl.isChecked()
        eeprom_check=self.ui.check_eeprom.isChecked()
        si571_check=self.ui.check_si571.isChecked()
        ics854s01i_check=self.ui.check_ics854s01i.isChecked()
        ad9510_check=self.ui.check_ad9510.isChecked()
        sensor_temp_check=self.ui.check_sensor_temperatura.isChecked()
        grafico_check=self.ui.checkGraficos.isChecked()
        gravar_fpga_check=self.ui.checkGravarFPGA.isChecked()
        utilizarMatlab_check=self.ui.checkUtilizarMATLAB.isChecked()
        timestamp=QDateTime.currentDateTime()
        operador=self.ui.OPERADOR.text()
        n_serie_adc=self.ui.N_SERIE_ADC.text()

        
        #Vai para a função que abre a Tela dos Leds
        (snr_result_values,sfdr_result_values,enob_result_values,
         crosstalk_values,missing_code_result_value_final,dif_amp_result_values,
         snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao,
         crosstalk_result_aprovacao,missing_code_result_aprovacao,dif_amp_result_aprovacao,timestamp_str,
         eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
         ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,
         si571_result,si571_write_check_result,si571_read_check_result,
         ad9510_result,ad9510_write_check_result,ad9510_read_check_result,sinal_entrada_crate)=self.janela_status_led.Abrir_Tela(ip_crate,ip_switch,ip_gerador_sinais_clock,
                                                                                                                              ip_gerador_sinais_input,posicao_AFC,posicao_AD,freq_clock,freq_in,amp_clock,amp_in,
                                                                                                                              freq_clock_missingcodes,freq_in_missingcodes,amp_clock_missingcodes,amp_in_missingcodes,perda_filtro_missingcodes,
                                                                                                                              pts_FFT,pts_crate,pts_crate_missingcodes,n_requisicoes,
                                                                                                                              snr_criterio,sfdr_criterio,enob_criterio,crosstalk_criterio,dif_amp_criterio,
                                                                                                                              snr_check,enob_check,sfdr_check,crosstalk_check,
                                                                                                                              missingcodes_check,dif_ampl_check,grafico_check,gravar_fpga_check,utilizarMatlab_check,
                                                                                                                              all_tests_selection,timestamp,
                                                                                                                              eeprom_check,si571_check, ad9510_check, ics854s01i_check, sensor_temp_check,
                                                                                                                              operador,n_serie_adc)
        '''#Informar horário de início do teste
        self.janela_teste.ui.lineEdit.setText(timestamp_str) ''' 
        
        #Canal 1
        #SNR
        if (("Teste não realizado" in str(snr_result_aprovacao[0]))==True):
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH1.setText("-")
            self.janela_resultados.ui.SNR_RESULT_CH1.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH1.setText(str(round(snr_result_values[0],2)))
            self.janela_resultados.ui.SNR_RESULT_CH1.setText(snr_result_aprovacao[0])
        
        
        #SFDR
        if (("Teste não realizado" in str(sfdr_result_values[0]))==True):
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH1.setText("-")
            self.janela_resultados.ui.SFDR_RESULT_CH1.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH1.setText(str(round(sfdr_result_values[0],2)))
            self.janela_resultados.ui.SFDR_RESULT_CH1.setText(sfdr_result_aprovacao[0])        
        #ENOB
        if (("Teste não realizado" in str(enob_result_values[0]))==True):
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH1.setText("-")
            self.janela_resultados.ui.ENOB_RESULT_CH1.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH1.setText(str(round(enob_result_values[0],2)))
            self.janela_resultados.ui.ENOB_RESULT_CH1.setText(enob_result_aprovacao[0])   
        #CROSSTALK
        if (("Teste não realizado" in str(crosstalk_values))==True):
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH1_2.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH1_3.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH1_4.setText("-")
            self.janela_resultados.ui.CROSSTALK_RESULT_CH1.setText("Teste não realizado") 
            
        else:
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH1_2.setText(str(round(crosstalk_values[0][0],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH1_3.setText(str(round(crosstalk_values[0][1],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH1_4.setText(str(round(crosstalk_values[0][2],2)))
            self.janela_resultados.ui.CROSSTALK_RESULT_CH1.setText(crosstalk_result_aprovacao[0])  

        #Canal 2
        #SNR
        if (("Teste não realizado" in str(snr_result_aprovacao[1]))==True):
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH2.setText("-")
            self.janela_resultados.ui.SNR_RESULT_CH2.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH2.setText(str(round(snr_result_values[1],2)))
            self.janela_resultados.ui.SNR_RESULT_CH2.setText(snr_result_aprovacao[1])
        #SFDR
        if (("Teste não realizado" in str(sfdr_result_values[1]))==True):
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH2.setText("-")
            self.janela_resultados.ui.SFDR_RESULT_CH2.setText("Teste não realizado") 
        else:
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH2.setText(str(round(sfdr_result_values[1],2)))
            self.janela_resultados.ui.SFDR_RESULT_CH2.setText(sfdr_result_aprovacao[1])        
        #ENOB
        if (("Teste não realizado" in str(enob_result_values[1]))==True):
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH2.setText("-")
            self.janela_resultados.ui.ENOB_RESULT_CH2.setText("Teste não realizado") 
        else:
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH2.setText(str(round(enob_result_values[1],2)))
            self.janela_resultados.ui.ENOB_RESULT_CH2.setText(enob_result_aprovacao[1])   
        #CROSSTALK
        if (("Teste não realizado" in str(crosstalk_values))==True):
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH2_1.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH2_3.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH2_4.setText("-")
            self.janela_resultados.ui.CROSSTALK_RESULT_CH2.setText("Teste não realizado")
        else:
            
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH2_1.setText(str(round(crosstalk_values[1][0],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH2_3.setText(str(round(crosstalk_values[1][1],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH2_4.setText(str(round(crosstalk_values[1][2],2)))
            self.janela_resultados.ui.CROSSTALK_RESULT_CH2.setText(crosstalk_result_aprovacao[1])
        
        
        #Canal 3
        #SNR
        if (("Teste não realizado" in str(snr_result_aprovacao[2]))==True):
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH3.setText("-")
            self.janela_resultados.ui.SNR_RESULT_CH3.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH3.setText(str(round(snr_result_values[2],2)))
            self.janela_resultados.ui.SNR_RESULT_CH3.setText(snr_result_aprovacao[2])
        #SFDR
        if (("Teste não realizado" in str(sfdr_result_values[2]))==True):
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH3.setText("-")
            self.janela_resultados.ui.SFDR_RESULT_CH3.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH3.setText(str(round(sfdr_result_values[2],2)))
            self.janela_resultados.ui.SFDR_RESULT_CH3.setText(sfdr_result_aprovacao[2])        
        #ENOB
        if (("Teste não realizado" in str(enob_result_values[2]))==True):
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH3.setText("-")
            self.janela_resultados.ui.ENOB_RESULT_CH3.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH3.setText(str(round(enob_result_values[2],2)))
            self.janela_resultados.ui.ENOB_RESULT_CH3.setText(enob_result_aprovacao[2])   
        #CROSSTALK
        if (("Teste não realizado" in str(crosstalk_values))==True):
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH3_1.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH3_2.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH3_4.setText("-")
            self.janela_resultados.ui.CROSSTALK_RESULT_CH3.setText("Teste não realizado")  
        else:
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH3_1.setText(str(round(crosstalk_values[2][0],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH3_2.setText(str(round(crosstalk_values[2][1],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH3_4.setText(str(round(crosstalk_values[2][2],2)))
            self.janela_resultados.ui.CROSSTALK_RESULT_CH3.setText(crosstalk_result_aprovacao[2])  
       
        #Canal 4
        #SNR
        if (("Teste não realizado" in str(snr_result_aprovacao[3]))==True):
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH4.setText("-")
            self.janela_resultados.ui.SNR_RESULT_CH4.setText("Teste não realizado")
        else:
            self.janela_resultados.ui.SNR_VALOR_MEDIDO_CH4.setText(str(round(snr_result_values[3],2)))
            self.janela_resultados.ui.SNR_RESULT_CH4.setText(snr_result_aprovacao[3])
        #SFDR
        if (("Teste não realizado" in str(sfdr_result_values[3]))==True):
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH4.setText("-")
            self.janela_resultados.ui.SFDR_RESULT_CH4.setText("Teste não realizado") 
        else:
            self.janela_resultados.ui.SFDR_VALOR_MEDIDO_CH4.setText(str(round(sfdr_result_values[3],2)))
            self.janela_resultados.ui.SFDR_RESULT_CH4.setText(sfdr_result_aprovacao[3])        
        #ENOB
        if (("Teste não realizado" in str(enob_result_values[3]))==True):
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH4.setText("-")
            self.janela_resultados.ui.ENOB_RESULT_CH4.setText("Teste não realizado") 
        else:
            self.janela_resultados.ui.ENOB_VALOR_MEDIDO_CH4.setText(str(round(enob_result_values[3],2)))
            self.janela_resultados.ui.ENOB_RESULT_CH4.setText(enob_result_aprovacao[3])   
        #CROSSTALK
        if (("Teste não realizado" in str(crosstalk_values))==True):
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH4_1.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH4_2.setText("-")
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH4_3.setText("-")
            self.janela_resultados.ui.CROSSTALK_RESULT_CH4.setText("Teste não realizado")  
        else:
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH4_1.setText(str(round(crosstalk_values[3][0],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH4_2.setText(str(round(crosstalk_values[3][1],2)))
            self.janela_resultados.ui.CROSSTALK_VALOR_MEDIDO_CH4_3.setText(str(round(crosstalk_values[3][2],2)))
            self.janela_resultados.ui.CROSSTALK_RESULT_CH4.setText(crosstalk_result_aprovacao[3])  
        
        
        
        self.janela_resultados.ui.SNR_CRITERIO.setText(str(snr_criterio))
        self.janela_resultados.ui.SFDR_CRITERIO.setText(str(sfdr_criterio))
        self.janela_resultados.ui.ENOB_CRITERIO.setText(str(enob_criterio))       
        self.janela_resultados.ui.CROSSTALK_CRITERIO.setText(str(crosstalk_criterio))
        self.janela_resultados.ui.MISSINGCODES_CRITERIO.setText(str(missingcode_criterio))
        self.janela_resultados.ui.DIF_AMPL_CRITERIO.setText(str(dif_amp_criterio))
        
        #DIFERENÇA DAS AMPLITUDES
        if (("Teste não realizado" in str(dif_amp_result_values))==True):
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_1.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_2.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_3.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_4.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_5.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_6.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_7.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_8.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_9.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_10.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_11.setText("-")
            
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_1.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_2.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_3.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_4.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_5.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_6.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_7.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_8.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_9.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_10.setText("-")
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_11.setText("-")
            

            self.janela_resultados.ui.DIF_AMP_RESULT_CH1CH3.setText(dif_amp_result_aprovacao[0]) 
            self.janela_resultados.ui.DIF_AMP_RESULT_CH2CH4.setText(dif_amp_result_aprovacao[1])
        else:

            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_1.setText(str(round(abs(dif_amp_result_values[0][0]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_2.setText(str(round(abs(dif_amp_result_values[0][1]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_3.setText(str(round(abs(dif_amp_result_values[0][2]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_4.setText(str(round(abs(dif_amp_result_values[0][3]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_5.setText(str(round(abs(dif_amp_result_values[0][4]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_6.setText(str(round(abs(dif_amp_result_values[0][5]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_7.setText(str(round(abs(dif_amp_result_values[0][6]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_8.setText(str(round(abs(dif_amp_result_values[0][7]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_9.setText(str(round(abs(dif_amp_result_values[0][8]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_10.setText(str(round(abs(dif_amp_result_values[0][9]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH1CH3_11.setText(str(round(abs(dif_amp_result_values[0][10]),4)))
            
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_1.setText(str(round(abs(dif_amp_result_values[1][0]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_2.setText(str(round(abs(dif_amp_result_values[1][1]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_3.setText(str(round(abs(dif_amp_result_values[1][2]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_4.setText(str(round(abs(dif_amp_result_values[1][3]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_5.setText(str(round(abs(dif_amp_result_values[1][4]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_6.setText(str(round(abs(dif_amp_result_values[1][5]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_7.setText(str(round(abs(dif_amp_result_values[1][6]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_8.setText(str(round(abs(dif_amp_result_values[1][7]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_9.setText(str(round(abs(dif_amp_result_values[1][8]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_10.setText(str(round(abs(dif_amp_result_values[1][9]),4)))
            self.janela_resultados.ui.DIF_AMP_VALOR_MEDIDO_CH2CH4_11.setText(str(round(abs(dif_amp_result_values[1][10]),4)))     
            
            self.janela_resultados.ui.DIF_AMP_RESULT_CH1CH3.setText(dif_amp_result_aprovacao[0]) 
            self.janela_resultados.ui.DIF_AMP_RESULT_CH2CH4.setText(dif_amp_result_aprovacao[1])
        
        #MISSING CODES
        
        if(str(missing_code_result_aprovacao[0])=="Teste não realizado"):
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH1.setText(missing_code_result_aprovacao[0])
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH2.setText(missing_code_result_aprovacao[1])
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH3.setText(missing_code_result_aprovacao[2])
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH4.setText(missing_code_result_aprovacao[3])
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH1.setText("-")
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH2.setText("-")
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH3.setText("-")
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH4.setText("-")
            self.janela_resultados.ui.MISSINGCODES_RANGE_MAXIMO.setText("-")
            self.janela_resultados.ui.MISSINGCODES_RANGE_MINIMO.setText("-")

        else:
            self.janela_resultados.ui.MISSINGCODES_RANGE_MAXIMO.setText(str(sinal_entrada_crate))
            self.janela_resultados.ui.MISSINGCODES_RANGE_MINIMO.setText(str(-sinal_entrada_crate))
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH1.setText(missing_code_result_aprovacao[0])
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH2.setText(missing_code_result_aprovacao[1])
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH3.setText(missing_code_result_aprovacao[2])
            self.janela_resultados.ui.MISSINGCODE_RESULT_CH4.setText(missing_code_result_aprovacao[3])
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH1.setText(str(missing_code_result_value_final[0][0]))
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH2.setText(str(missing_code_result_value_final[1][0]))
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH3.setText(str(missing_code_result_value_final[2][0]))
            self.janela_resultados.ui.MISSINGCODE_VALOR_MEDIDO_CH4.setText(str(missing_code_result_value_final[3][0]))
        
        
        #EEPROM
        self.janela_resultados.ui.EEPROM_RESULT_FINAL.setText(eeprom_result)
        self.janela_resultados.ui.EEPROM_READ_RESULT.setText(eeprom_read_check_result)
        self.janela_resultados.ui.EEPROM_WRITE_RESULT.setText(eeprom_write_check_result)
        
        #ICS854S01I
        self.janela_resultados.ui.ICS854S01I_RESULT_FINAL.setText(ics854s01i_result)
        self.janela_resultados.ui.ICS854S01I_READ_RESULT.setText(ics854s01i_read_check_result)
        self.janela_resultados.ui.ICS854S01I_WRITE_RESULT.setText(ics854s01i_write_check_result)

        #SI571
        self.janela_resultados.ui.SI571_RESULT_FINAL.setText(si571_result)
        self.janela_resultados.ui.SI571_READ_RESULT.setText(si571_read_check_result)
        self.janela_resultados.ui.SI571_WRITE_RESULT.setText(si571_write_check_result)
        
        #AD9510
        self.janela_resultados.ui.AD9510_RESULT_FINAL.setText(ad9510_result)
        self.janela_resultados.ui.AD9510_READ_RESULT.setText(ad9510_read_check_result)
        self.janela_resultados.ui.AD9510_WRITE_RESULT.setText(ad9510_write_check_result)

        
        #Exibe a tela de resultados finais
        self.janela_resultados.ui.dateTimeEdit_result.setDateTime(QDateTime.currentDateTime())
        self.janela_resultados.show()

        
    def Config_Simulation(self):
        ad9510_pll_function_config = int(self.ui.ad9510_pll_function_config.text())
        ad9510_pll_clock_sel_config = int(self.ui.ad9510_pll_clock_sel_config.text())
        ad9510_pll_clock_sel_ref_config = int(self.ui.ad9510_pll_clock_sel_ref_config.text())
        ad9510_a_divider_config=int(self.ui.ad9510_a_divider_config.text())
        ad9510_b_divider_config=int(self.ui.ad9510_b_divider_config.text())
        ad9510_r_divider_config=int(self.ui.ad9510_r_divider_config.text()) 
        ad9510_prescaler_config=int(self.ui.ad9510_prescaler_config.text()) 
        ad9510_pll_powerdown_config=int(self.ui.ad9510_pll_powerdown_config.text()) 
        ad9510_current_config=int(self.ui.ad9510_current_config.text()) 
        ad9510_outputs_config=str(self.ui.ad9510_outputs_config.text()) 
        si571_freq_config=int(self.ui.si571_freq_config.text())    
        si571_output_config=int(self.ui.si571_output_config.text())
        
        POSITION_CRATE=int(self.ui.POSICAO_AFC.text())
        POSITION_ADC=int(self.ui.POSICAO_AD.text())
        IP_CRATE = self.ui.IP_CRATE.text()
        
        ad9510_a_divider_config_check=self.ui.ad9510_a_divider_config_check.isChecked()
        ad9510_b_divider_config_check=self.ui.ad9510_b_divider_config_check.isChecked()
        ad9510_current_config_check=self.ui.ad9510_current_config_check.isChecked()
        ad9510_outputs_config_check=self.ui.ad9510_outputs_config_check.isChecked()
        ad9510_pll_clock_sel_config_check=self.ui.ad9510_pll_clock_sel_config_check.isChecked()
        ad9510_pll_clock_sel_ref_config_check=self.ui.ad9510_pll_clock_sel_ref_config_check.isChecked()
        ad9510_pll_function_config_check=self.ui.ad9510_pll_function_config_check.isChecked()
        ad9510_prescaler_config_check=self.ui.ad9510_prescaler_config_check.isChecked()
        ad9510_pll_powerdown_config_check=self.ui.ad9510_pll_powerdown_config_check.isChecked()
        ad9510_r_divider_config_check=self.ui.ad9510_r_divider_config_check.isChecked()
        si571_freq_config_check=self.ui.si571_freq_config_check.isChecked()
        si571_output_config_check=self.ui.si571_output_config_check.isChecked()
        all_config_check=self.ui.all_config_check.isChecked()
          
        
        (cis_configuration_log) = cis_configuration(ad9510_pll_function_config,ad9510_pll_clock_sel_config,
                                                                                                                ad9510_pll_clock_sel_ref_config,ad9510_a_divider_config,ad9510_b_divider_config,
                                                                                                                ad9510_r_divider_config,ad9510_prescaler_config,ad9510_pll_powerdown_config,
                                                                                                                ad9510_current_config,ad9510_outputs_config,si571_freq_config,si571_output_config,
                                                                                                                ad9510_a_divider_config_check,ad9510_b_divider_config_check,ad9510_current_config_check,
                                                                                                                ad9510_outputs_config_check,ad9510_pll_clock_sel_config_check,ad9510_pll_clock_sel_ref_config_check,
                                                                                                                ad9510_prescaler_config_check,ad9510_pll_function_config_check,ad9510_pll_powerdown_config_check,
                                                                                                                ad9510_r_divider_config_check,si571_freq_config_check,si571_output_config_check,all_config_check,
                                                                                                                IP_CRATE,POSITION_ADC,POSITION_CRATE,self) 
        datapath_save="result/"
        n_serie_adc=self.ui.N_SERIE_ADC.text()
        #Salva os resultados finais
        list_to_file_aux(0,cis_configuration_log, datapath_save+"ci_configuration/"+ n_serie_adc + "_ciconfig.txt")
        #self.ui.ad9510_pll_status_config.setText(str(ad9510_pll_status_config))   


        
#SEGUNDA JANELA
class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = interface_resultado_final.Ui_Dialog()
        #self.ui=teste_botoes.Ui_Dialog()
        self.ui.setupUi(self) 
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.ui.OK_BUTTON.clicked.connect(self.Close_Result)
        
    def Close_Result(self):
        
        
        self.close()

#TERCEIRA JANELA
class MyDialog_StatusLed(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = interface_status_leds.Ui_Dialog()
        self.ui.setupUi(self) 
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.ui.OK_Button.clicked.connect(self.Close_Result)
        
       
    def Close_Result(self):
        
        self.close()
        
    def Abrir_Tela(self,ip_crate,ip_switch,ip_gerador_sinais_clock,ip_gerador_sinais_input,
                   posicao_AFC,posicao_AD,freq_clock,freq_in,amp_clock,amp_in,freq_clock_missingcodes,
                   freq_in_missingcodes,amp_clock_missingcodes,amp_in_missingcodes,perda_filtro_missingcodes,
                   pts_FFT,pts_crate,pts_crate_missingcodes,n_requisicoes,
                   snr_criterio,sfdr_criterio,enob_criterio,crosstalk_criterio,dif_amp_criterio,
                   snr_check,enob_check,sfdr_check,crosstalk_check,missingcodes_check,dif_ampl_check,
                   grafico_check,gravar_fpga_check,utilizarMatlab_check,all_tests_selection,timestamp,
                   eeprom_check,si571_check, ad9510_check, ics854s01i_check, sensor_temp_check,
                   operador,n_serie_adc):
        
        self.open()
        self.repaint()
        QApplication.processEvents()
        
        
        #Iniciar todos os LEDs apagados
        self.ui.kled_crate.setState(0)
        self.ui.kled_switch.setState(0)
        self.ui.kled_ger_sin_clk.setState(0)
        self.ui.kled_ger_sin_in.setState(0)
        self.ui.kled_data_acquisition.setState(0)
        self.ui.kled_snr.setState(0)
        self.ui.kled_enob.setState(0)
        self.ui.kled_sfdr.setState(0)
        self.ui.kled_crosstalk.setState(0)
        self.ui.kled_missing_codes.setState(0)
        self.ui.kled_dif_amp.setState(0)
        self.ui.kled_ad9510.setState(0)
        self.ui.kled_si571.setState(0)
        self.ui.kled_eeprom.setState(0)
        self.ui.kled_ics854s01i.setState(0)
        self.ui.kled_sensor_temperatura.setState(0)
        self.ui.kled_fpga.setState(0)
        
        self.ui.kled_crate.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_switch.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_ger_sin_clk.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_ger_sin_in.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_snr.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_enob.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_sfdr.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_crosstalk.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_missing_codes.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_dif_amp.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_ad9510.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_si571.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_eeprom.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_ics854s01i.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_sensor_temperatura.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_fpga.setColor(QtGui.QColor(0,255,0))
        self.repaint()
        QApplication.processEvents()
        
        timestamp_str=str(timestamp.toString('dd.MM.yyyy hh:mm:ss'))
        
        (snr_result_values,sfdr_result_values,enob_result_values,crosstalk_values,
         missing_code_result_value_final,dif_amp_result_values,
         snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao,
         crosstalk_result_aprovacao,
         missing_code_result_aprovacao,dif_amp_result_aprovacao,
         eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
         ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,
         si571_result,si571_write_check_result,si571_read_check_result,
         ad9510_result,ad9510_write_check_result,ad9510_read_check_result,sinal_entrada_crate)=run_main_p_interface(ip_crate,ip_switch,ip_gerador_sinais_clock,ip_gerador_sinais_input,
                                                                                      posicao_AFC,posicao_AD,freq_clock,freq_in,amp_clock,amp_in,freq_clock_missingcodes,freq_in_missingcodes,amp_clock_missingcodes,amp_in_missingcodes,perda_filtro_missingcodes,
                                                                                      pts_FFT,pts_crate,pts_crate_missingcodes,n_requisicoes,
                                                                                      snr_criterio,sfdr_criterio,enob_criterio,crosstalk_criterio,dif_amp_criterio,
                                                                                      snr_check,enob_check,sfdr_check,crosstalk_check,missingcodes_check,dif_ampl_check,grafico_check,gravar_fpga_check,
                                                                                      utilizarMatlab_check,all_tests_selection,self,
                                                                                      eeprom_check,si571_check, ad9510_check, ics854s01i_check, sensor_temp_check,
                                                                                      operador,n_serie_adc)                
        
        
        self.ui.progressBar.setValue(100) 
        self.repaint()
        QApplication.processEvents() 
        print("Carregando a barra final...",self.repaint())
        print("Carregando a barra final...",QApplication.processEvents()) 
        

        return(snr_result_values,sfdr_result_values,enob_result_values,
               crosstalk_values,missing_code_result_value_final,dif_amp_result_values,
               snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao,
               crosstalk_result_aprovacao,missing_code_result_aprovacao,dif_amp_result_aprovacao,timestamp_str,
               eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
               ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,
               si571_result,si571_write_check_result,si571_read_check_result,
               ad9510_result,ad9510_write_check_result,ad9510_read_check_result,sinal_entrada_crate)
        


'''#QUARTA JANELA - TESTES
class Janela_Teste(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Janela_Teste, self).__init__(parent)
        self.ui = teste_time.Ui_Dialog()
        self.ui.setupUi(self) 
       
        self.verticalLvalores_possiveis_crateayout = QtGui.QVBoxLayout(self)'''
       
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TestWindow_ADC()
    window.show()
    sys.exit(app.exec_())