from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QDateTime

import  sys

from run_rffe_test_p_interface import run_rffe_test_p_interface
import interface_principal_rffe
import interface_resultados_rffe
import interface_status_leds_rffe



#import interface_resultado_final
#from run_main_p_interface import run_main_p_interface



#PRIMEIRA JANELA
class TestWindow_RFFE(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = interface_principal_rffe.Ui_MainWindow() 
        self.ui.setupUi(self) 
        #Ação dos botões
        self.ui.START_BUTTON.clicked.connect(self.Start_Simulation)
        self.ui.EXIT_BUTTON.clicked.connect(self.Exit_Simulation)
        self.janela_resultados = MyDialog(self)
        self.janela_resultados.ui.tabWidget.widget(0)
        self.janela_status_led = MyDialog_StatusLed(self)
        
        self.ui.dateTimeEdit_tela_inicial.setDateTime(QDateTime.currentDateTime())
        

    def Exit_Simulation(self):
        print ("Fecha Aplicação")
        exit()
        #self.janela_nova.exec_()
        #self.teste_aqui.show()
       
        

    def Start_Simulation(self):
        
        #Equipament IPs
        ip_switch_1 = self.ui.IP_SWITCH_1.text()
        ip_switch_2 = self.ui.IP_SWITCH_2.text()
        ip_rffe = self.ui.IP_RFFE.text()
        ip_gerador_sinais_dc = self.ui.IP_GERADOR_SINAIS_DC.text()
        ip_network_analyzer = self.ui.IP_NETWORK_ANALYZER.text()
      
        #Input Parameters
        network_freq_central=float(self.ui.NETWORK_FREQ_CENTRAL.text())*1000000
        network_freq_span=float(self.ui.NETWORK_FREQ_SPAN.text())*1000000
        network_pot_in_standard=float(self.ui.NETWORK_POT_IN_STANDARD.text())
        network_pot_in_inicial=float(self.ui.NETWORK_POT_IN_INITIAL.text())
        network_pot_in_final=float(self.ui.NETWORK_POT_IN_FINAL.text())
        network_pot_in_step=float(self.ui.NETWORK_POT_IN_STEP.text())
        network_start_bandwidth = float(self.ui.NETWORK_START_BANDWIDTH.text())*1000000
        network_stop_bandwidth = float(self.ui.NETWORK_STOP_BANDWIDTH.text())*1000000
        
        rffe_attenuation_standard=float(self.ui.RFFE_ATTENUATION_STANDARD.text())
        rffe_attenuation_initial=float(self.ui.RFFE_ATTENUATION_INITIAL.text())
        rffe_attenuation_final=float(self.ui.RFFE_ATTENUATION_FINAL.text())
        rffe_attenuation_step=float(self.ui.RFFE_ATTENUATION_STEP.text())
        
        #Set-up description
        network_model=self.ui.NETWORK_MODEL.text()
        waveform_model=self.ui.WAVEFORM_MODEL.text()
        dc_power_model=self.ui.DC_POWER_MODEL.text()
        rf_switch_model=self.ui.RF_SWITCH_MODEL.text()
        rffe_serie=self.ui.RFFE_SERIE.text()
        rffe_operador=self.ui.RFFE_OPERADOR.text()
        
        #Critérios de avaliação
        att_ref = float(self.ui.ATT_REF.text())
        switch_ref = float(self.ui.SWITCH_REF.text())
        freq_res_ref = float(self.ui.FREQ_RES_REF.text())
        ret_loss_s11_ref = float(self.ui.RET_LOSS_S11_REF.text())
        ret_loss_s22_ref = float(self.ui.RET_LOSS_S22_REF.text())
        linearity_ref = float(self.ui.LINEARITY_REF.text())
        xtalk_ref = float(self.ui.XTALK_REF.text())
        temp_min = float(self.ui.TEMP_MIN.text())
        temp_max = float(self.ui.TEMP_MAX.text())

        att_tol = float(self.ui.ATT_TOL.text())
        switch_tol = float(self.ui.SWITCH_TOL.text())
        freq_res_tol_ref = float(self.ui.FREQ_RES_TOL_REF.text())
        ret_loss_s11_tol_ref = float(self.ui.RET_LOSS_S11_TOL_REF.text())
        ret_loss_s22_tol_ref = float(self.ui.RET_LOSS_S22_TOL_REF.text())
        xtalk_tol_ref = float(self.ui.XTALK_TOL_REF.text())
        freq_res_tol_var = float(self.ui.FREQ_RES_TOL_VAR.text())
        linearity_tol = float(self.ui.LINEARITY_TOL.text())
        
        #Seleção de Opções
        s_parameter_test_selection = self.ui.PARAMETRO_S.isChecked()
        atenuadores_test_selection = self.ui.ATENUADORES.isChecked()
        switch_dc_test_selection = self.ui.SWITCH_DC.isChecked()
        freq_resp_test_selection = self.ui.FREQ_RESP.isChecked()
        ret_loss_test_selection = self.ui.RETURN_LOSS.isChecked()
        linearidade_test_selection = self.ui.LINEARIDADE.isChecked()
        crosstalk_test_selection = self.ui.CROSSTALK.isChecked()
        temp_test_selection = self.ui.TEMPERATURA.isChecked()
        all_tests_selection = self.ui.ALL_TESTS.isChecked()
        
        curva_s_parameter=self.ui.CURVA_S_PARAMETER.isChecked()
        
        
        (s_param_res_ap,
            att_res_val,att_res_ap,
            switch_dc_res_val,switch_dc_res_ap,
            freq_resp_res_val_freqmax,freq_resp_res_val_max,freq_resp_res_val_delta,freq_resp_res_ap,
            ret_loss_res_val_max_s11 ,ret_loss_res_ap_s11,ret_loss_res_val_max_s22,ret_loss_res_ap_s22,
            linearity_res_val,linearity_res_ap,
            crosstalk_res_val,crosstalk_res_ap,
            temperature_res_val,temperature_res_ap,stop_qt_time)=self.janela_status_led.Open_Window(ip_switch_1,ip_switch_2,ip_rffe,ip_gerador_sinais_dc,ip_network_analyzer,
                                                                                         att_ref,switch_ref,freq_res_ref,ret_loss_s11_ref,ret_loss_s22_ref,linearity_ref,xtalk_ref,temp_min,temp_max,
                                                                                         att_tol,switch_tol,freq_res_tol_ref,ret_loss_s11_tol_ref,ret_loss_s22_tol_ref,linearity_tol,xtalk_tol_ref,
                                                                                         freq_res_tol_var,
                                                                                         s_parameter_test_selection,atenuadores_test_selection,switch_dc_test_selection,freq_resp_test_selection,ret_loss_test_selection,
                                                                                         linearidade_test_selection,crosstalk_test_selection,temp_test_selection,all_tests_selection,curva_s_parameter,
                                                                                         network_freq_central,network_freq_span,
                                                                                         network_pot_in_standard,network_pot_in_inicial,network_pot_in_final,network_pot_in_step,
                                                                                         rffe_attenuation_standard,rffe_attenuation_initial,rffe_attenuation_final,rffe_attenuation_step,
                                                                                         network_model,waveform_model,dc_power_model,rf_switch_model,rffe_serie,
                                                                                         network_start_bandwidth,network_stop_bandwidth,rffe_operador)






        #RESULTADOS FINAIS
        
        #TESTE DE ATENUAÇÃO
        self.janela_resultados.ui.atenuador_crit_max.setText(str(abs(att_ref+att_tol)))
        self.janela_resultados.ui.atenuador_crit_min.setText(str(abs(att_ref-att_tol)))
        self.janela_resultados.ui.att_ch1_resultado.setText(att_res_ap[0])
        self.janela_resultados.ui.att_ch2_resultado.setText(att_res_ap[1])
        self.janela_resultados.ui.att_ch3_resultado.setText(att_res_ap[2])
        self.janela_resultados.ui.att_ch4_resultado.setText(att_res_ap[3])
        
        if(str(att_res_ap[0])!="Test Not Performed"):

            for i in range (0,len(att_res_val[0])):
                self.janela_resultados.ui.tableWidget_atenuadores.setItem(0,i, QtGui.QTableWidgetItem(str(i+1)))
            for i in range (0,len(att_res_val[0])):
                self.janela_resultados.ui.tableWidget_atenuadores.setItem(1,i, QtGui.QTableWidgetItem(str(att_res_val[0][i])))
            for i in range (0,len(att_res_val[1])):
                self.janela_resultados.ui.tableWidget_atenuadores.setItem(2,i, QtGui.QTableWidgetItem(str(att_res_val[1][i])))                
            for i in range (0,len(att_res_val[2])):
                self.janela_resultados.ui.tableWidget_atenuadores.setItem(3,i, QtGui.QTableWidgetItem(str(att_res_val[2][i])))
            for i in range (0,len(att_res_val[3])):
                self.janela_resultados.ui.tableWidget_atenuadores.setItem(4,i, QtGui.QTableWidgetItem(str(att_res_val[3][i])))

                                                
        #RF SWITCHES
        self.janela_resultados.ui.switch_dc_ch1_medicao.setText(str(switch_dc_res_val[0]))
        self.janela_resultados.ui.switch_dc_ch2_medicao.setText(str(switch_dc_res_val[1]))
        self.janela_resultados.ui.switch_dc_ch3_medicao.setText(str(switch_dc_res_val[2]))
        self.janela_resultados.ui.switch_dc_ch4_medicao.setText(str(switch_dc_res_val[3]))
        self.janela_resultados.ui.switch_dc_crit.setText(str(abs(switch_tol+switch_ref)))
        self.janela_resultados.ui.switch_dc_ch1_resultado.setText(switch_dc_res_ap[0])
        self.janela_resultados.ui.switch_dc_ch2_resultado.setText(switch_dc_res_ap[1]) 
        self.janela_resultados.ui.switch_dc_ch3_resultado.setText(switch_dc_res_ap[2])
        self.janela_resultados.ui.switch_dc_ch4_resultado.setText(switch_dc_res_ap[3]) 
        
        #FREQ RESP
        self.janela_resultados.ui.freq_dif_max_1.setText(str(freq_resp_res_val_delta[0]))
        self.janela_resultados.ui.freq_dif_max_2.setText(str(freq_resp_res_val_delta[1]))
        self.janela_resultados.ui.freq_dif_max_3.setText(str(freq_resp_res_val_delta[2]))
        self.janela_resultados.ui.freq_dif_max_4.setText(str(freq_resp_res_val_delta[3]))

        self.janela_resultados.ui.freq_freq_max_1.setText(str(freq_resp_res_val_freqmax[0]))
        self.janela_resultados.ui.freq_freq_max_2.setText(str(freq_resp_res_val_freqmax[1]))
        self.janela_resultados.ui.freq_freq_max_3.setText(str(freq_resp_res_val_freqmax[2]))
        self.janela_resultados.ui.freq_freq_max_4.setText(str(freq_resp_res_val_freqmax[3]))
    
        self.janela_resultados.ui.freq_amp_max_1.setText(str(freq_resp_res_val_max[0]))
        self.janela_resultados.ui.freq_amp_max_2.setText(str(freq_resp_res_val_max[1]))
        self.janela_resultados.ui.freq_amp_max_3.setText(str(freq_resp_res_val_max[2]))
        self.janela_resultados.ui.freq_amp_max_4.setText(str(freq_resp_res_val_max[3]))
                                                          
        self.janela_resultados.ui.freq_resp_crit_min.setText(str(abs(freq_res_ref+freq_res_tol_ref)))
        self.janela_resultados.ui.freq_resp_crit_dif.setText(str(abs(freq_res_tol_var)))
        
        self.janela_resultados.ui.freq_resp_ch1_resultado.setText(freq_resp_res_ap[0])
        self.janela_resultados.ui.freq_resp_ch2_resultado.setText(freq_resp_res_ap[1]) 
        self.janela_resultados.ui.freq_resp_ch3_resultado.setText(freq_resp_res_ap[2])
        self.janela_resultados.ui.freq_resp_ch4_resultado.setText(freq_resp_res_ap[3])
        
        
        #RETURN LOSS
        self.janela_resultados.ui.ret_loss_s11_crit.setText(str(abs(ret_loss_s11_ref+ret_loss_s11_tol_ref)))
        self.janela_resultados.ui.ret_loss_s22_crit.setText(str(abs(ret_loss_s22_ref+ret_loss_s22_tol_ref)))
        
        self.janela_resultados.ui.ret_loss_s11_ch1_medicao.setText(str(ret_loss_res_val_max_s11[0]))
        self.janela_resultados.ui.ret_loss_s11_ch2_medicao.setText(str(ret_loss_res_val_max_s11[1]))
        self.janela_resultados.ui.ret_loss_s11_ch3_medicao.setText(str(ret_loss_res_val_max_s11[2]))
        self.janela_resultados.ui.ret_loss_s11_ch4_medicao.setText(str(ret_loss_res_val_max_s11[3]))
        
        self.janela_resultados.ui.ret_loss_s22_ch1_medicao.setText(str(ret_loss_res_val_max_s22[0]))
        self.janela_resultados.ui.ret_loss_s22_ch2_medicao.setText(str(ret_loss_res_val_max_s22[1]))
        self.janela_resultados.ui.ret_loss_s22_ch3_medicao.setText(str(ret_loss_res_val_max_s22[2]))
        self.janela_resultados.ui.ret_loss_s22_ch4_medicao.setText(str(ret_loss_res_val_max_s22[3]))               
        
        self.janela_resultados.ui.ret_loss_s11_ch1_resultado.setText(ret_loss_res_ap_s11[0])
        self.janela_resultados.ui.ret_loss_s11_ch2_resultado.setText(ret_loss_res_ap_s11[1])
        self.janela_resultados.ui.ret_loss_s11_ch3_resultado.setText(ret_loss_res_ap_s11[2])
        self.janela_resultados.ui.ret_loss_s11_ch4_resultado.setText(ret_loss_res_ap_s11[3])
        
        self.janela_resultados.ui.ret_loss_s22_ch1_resultado.setText(ret_loss_res_ap_s22[0])
        self.janela_resultados.ui.ret_loss_s22_ch2_resultado.setText(ret_loss_res_ap_s22[1])
        self.janela_resultados.ui.ret_loss_s22_ch3_resultado.setText(ret_loss_res_ap_s22[2])
        self.janela_resultados.ui.ret_loss_s22_ch4_resultado.setText(ret_loss_res_ap_s22[3])
        
        #LINEARIDADE
        self.janela_resultados.ui.linearidade_crit.setText(str(abs(linearity_ref+linearity_tol)))
        self.janela_resultados.ui.linearidade_ch1_resultado.setText(linearity_res_ap[0])
        self.janela_resultados.ui.linearidade_ch2_resultado.setText(linearity_res_ap[1])
        self.janela_resultados.ui.linearidade_ch3_resultado.setText(linearity_res_ap[2])
        self.janela_resultados.ui.linearidade_ch4_resultado.setText(linearity_res_ap[3])
        
        if(str(linearity_res_ap[0])!="Test Not Performed"):

            for i in range (0,len(linearity_res_val[0])):
                self.janela_resultados.ui.tableWidget_linearidade.setItem(0,i, QtGui.QTableWidgetItem(str(i+1)))
            for i in range (0,len(linearity_res_val[0])):
                self.janela_resultados.ui.tableWidget_linearidade.setItem(1,i, QtGui.QTableWidgetItem(str(linearity_res_val[0][i])))
            for i in range (0,len(linearity_res_val[1])):
                self.janela_resultados.ui.tableWidget_linearidade.setItem(2,i, QtGui.QTableWidgetItem(str(linearity_res_val[1][i])))                
            for i in range (0,len(linearity_res_val[2])):
                self.janela_resultados.ui.tableWidget_linearidade.setItem(3,i, QtGui.QTableWidgetItem(str(linearity_res_val[2][i])))
            for i in range (0,len(linearity_res_val[3])):
                self.janela_resultados.ui.tableWidget_linearidade.setItem(4,i, QtGui.QTableWidgetItem(str(linearity_res_val[3][i])))



        
        #CROSSTALK
        self.janela_resultados.ui.crosstalk_ch1_medicao.setText(str(crosstalk_res_val[0]))
        self.janela_resultados.ui.crosstalk_ch2_medicao.setText(str(crosstalk_res_val[1]))
        self.janela_resultados.ui.crosstalk_ch3_medicao.setText(str(crosstalk_res_val[2]))
        self.janela_resultados.ui.crosstalk_ch4_medicao.setText(str(crosstalk_res_val[3]))
        self.janela_resultados.ui.crosstalk_crit.setText(str(abs(xtalk_ref+xtalk_tol_ref)))
        self.janela_resultados.ui.crosstalk_ch1_resultado.setText(crosstalk_res_ap[0])
        self.janela_resultados.ui.crosstalk_ch2_resultado.setText(crosstalk_res_ap[1]) 
        self.janela_resultados.ui.crosstalk_ch3_resultado.setText(crosstalk_res_ap[2])
        self.janela_resultados.ui.crosstalk_ch4_resultado.setText(crosstalk_res_ap[3]) 
        
        #TEMPERATURE
        self.janela_resultados.ui.TEMP_VAL_1.setText(str(temperature_res_val[0]))
        self.janela_resultados.ui.TEMP_VAL_2.setText(str(temperature_res_val[1]))
        self.janela_resultados.ui.TEMP_VAL_3.setText(str(temperature_res_val[2]))
        self.janela_resultados.ui.TEMP_VAL_4.setText(str(temperature_res_val[3]))
        self.janela_resultados.ui.TEMP_VAL_5.setText(str(temperature_res_val[4]))
        self.janela_resultados.ui.temp_crit_max.setText(str(temp_max))
        self.janela_resultados.ui.temp_crit_min.setText(str(temp_min))
        self.janela_resultados.ui.temp_resultado.setText(temperature_res_ap)

        
        
        
       

        #Exibe a tela de resultados finais
        
        self.janela_resultados.show()
        self.janela_resultados.ui.dateTimeEdit_result.setDateTime(stop_qt_time)

#SEGUNDA JANELA
class MyDialog_StatusLed(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = interface_status_leds_rffe.Ui_Dialog()
        self.ui.setupUi(self) 
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.ui.OK_Button.clicked.connect(self.Close_Result)
        
       
    def Close_Result(self):
        
        self.close()
        
    def Open_Window(self,ip_switch_1,ip_switch_2,ip_rffe,ip_gerador_sinais_dc,ip_network_analyzer,
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
        
        
        self.open()
        self.repaint()
        QApplication.processEvents()
        
        #Iniciar todos os LEDs apagados
        self.ui.kled_RFFE.setState(0)
        self.ui.kled_NETWORK.setState(0)
        self.ui.kled_SWITCH1.setState(0)
        self.ui.kled_SWITCH2.setState(0)
        self.ui.kled_WAVEFORM.setState(0)
        self.ui.kled_PARAMETRO_S_TEST.setState(0)
        self.ui.kled_ATENUADORES_TEST.setState(0)
        self.ui.kled_RESP_FREQ_TEST.setState(0)
        self.ui.kled_RF_SWITCH_TEST.setState(0)
        self.ui.kled_RETURN_LOSS_TEST.setState(0)
        self.ui.kled_LINEARIDADE_TEST.setState(0)
        self.ui.kled_CROSSTALK_TEST.setState(0)
        self.ui.kled_TEMPERATURE_TEST.setState(0)
        self.ui.kled_CH1_A_SWITCH1.setState(0)
        self.ui.kled_CH2_A_SWITCH1.setState(0)
        self.ui.kled_CH3_A_SWITCH1.setState(0)
        self.ui.kled_CH4_A_SWITCH1.setState(0)
        self.ui.kled_CH1_B_SWITCH1.setState(0)
        self.ui.kled_CH2_B_SWITCH1.setState(0)
        self.ui.kled_CH3_B_SWITCH1.setState(0)
        self.ui.kled_CH4_B_SWITCH1.setState(0)
        self.ui.kled_CH1_A_SWITCH2.setState(0)
        self.ui.kled_CH2_A_SWITCH2.setState(0)
        self.ui.kled_CH3_A_SWITCH2.setState(0)
        self.ui.kled_CH4_A_SWITCH2.setState(0)
        self.ui.kled_CH1_B_SWITCH2.setState(0)
        self.ui.kled_CH2_B_SWITCH2.setState(0)
        self.ui.kled_CH3_B_SWITCH2.setState(0)
        self.ui.kled_CH4_B_SWITCH2.setState(0)
        
        self.ui.kled_RFFE.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_NETWORK.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_WAVEFORM.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_PARAMETRO_S_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_ATENUADORES_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_RESP_FREQ_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_RETURN_LOSS_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_LINEARIDADE_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CROSSTALK_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_TEMPERATURE_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_RF_SWITCH_TEST.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH1_A_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH2_A_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH3_A_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH4_A_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH1_B_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH2_B_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH3_B_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH4_B_SWITCH1.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH1_A_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH2_A_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH3_A_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH4_A_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH1_B_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH2_B_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH3_B_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        self.ui.kled_CH4_B_SWITCH2.setColor(QtGui.QColor(0, 255, 0))
        
       

        self.repaint()
        QApplication.processEvents()
        
        
        
        
        (s_param_res_ap,
         att_res_val,att_res_ap,
         switch_dc_res_val,switch_dc_res_ap,
         freq_resp_res_val_freqmax,freq_resp_res_val_max,freq_resp_res_val_delta,freq_resp_res_ap,
         ret_loss_res_val_max_s11 ,ret_loss_res_ap_s11,ret_loss_res_val_max_s22,ret_loss_res_ap_s22,
         linearity_res_val,linearity_res_ap,
         crosstalk_res_val,crosstalk_res_ap,
         temperature_res_val,temperature_res_ap,stop_qt_time)=run_rffe_test_p_interface(self,
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
                                                                           network_start_bandwidth,network_stop_bandwidth,rffe_operador)

        
        
        return(s_param_res_ap,
            att_res_val,att_res_ap,
            switch_dc_res_val,switch_dc_res_ap,
            freq_resp_res_val_freqmax,freq_resp_res_val_max,freq_resp_res_val_delta,freq_resp_res_ap,
            ret_loss_res_val_max_s11 ,ret_loss_res_ap_s11,ret_loss_res_val_max_s22,ret_loss_res_ap_s22,
            linearity_res_val,linearity_res_ap,
            crosstalk_res_val,crosstalk_res_ap,
            temperature_res_val,temperature_res_ap,stop_qt_time)

                
#TERCEIRA JANELA
class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = interface_resultados_rffe.Ui_Dialog()
        #self.ui=teste_botoes.Ui_Dialog()
        self.ui.setupUi(self) 
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.ui.OK_BUTTON.clicked.connect(self.Close_Result)
    
    def Close_Result(self):
        self.close()

       
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TestWindow_RFFE()
    window.show()
    sys.exit(app.exec_())