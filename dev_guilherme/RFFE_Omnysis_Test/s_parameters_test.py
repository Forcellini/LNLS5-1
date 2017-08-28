from rffe_test_lib import AgilentE5061B #necessário para enviar comandos para o vna
import numpy as np
import test_lib
from leds_rf_switch import leds_rf_switch
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
import matplotlib.pyplot as plt

def s_parameters_test (vna,sgen,rffe,
                       rfsw_1,ip_sw1,sw1_port_1,sw1_port_2,
                       rfsw_2,ip_sw2,sw2_port_1,sw2_port_2,
                       center_freq, freq_span, 
                       pow_value, att_value,
                       serial_number,metadata_path,datapath_save,tela_leds,percentual,curva_s_parameter,datapath_save_figure):


    print("\nStarting tests. Measuring S-parameters - Ports: "+str(sw2_port_1)+ " - " + str(sw2_port_2)+"\n")
     
    tela_leds.ui.progressBar.setValue(5+percentual)
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra s parameter",tela_leds.repaint())
    print("barra s parameter",QApplication.processEvents()) 
       
    #Configuração Inicial de Segurança - Atenuador do RFFE no máximo, e VNA setado para pow_value dB
    rffe.set_attenuator_value(att_value)
    sgen.set_signal_DC()
    sgen.set_pos("direct")
    vna.send_command(b":SOUR1:POW "+format(pow_value).encode('utf-8')+b"\n") 
    test_lib.set_vna(0, center_freq, freq_span, 0, vna)
    rfsw_1.sw1_pos(ip_sw1,3,3) #coloca o switch 1 na chave 3-3 = 0dBm
    rfsw_2.sw2_pos(ip_sw2,0,0)
    leds_rf_switch(3, 3, 0, 0, tela_leds)

        
    #Data acquisition for channel 1-1 or 3-3
    
    #Frequency Data Acquisition
    freq_data=vna.get_frequency_data()
    
    #This one's purpose in exclusive to plot the data
    freq_data_mhz=[]
    for i in range (0,len(freq_data)):
        freq_data_mhz.append(freq_data[i]/1000000)

    print ("Porta "+str(sw2_port_1)+ " - " + str(sw2_port_1)+" do Switch") 
    rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_1) 
    leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_1, tela_leds)

    s11_pos1=vna.get_s11_data()
    s12_pos1=vna.get_s12_data()
    s21_pos1=vna.get_s21_data()
    s22_pos1=vna.get_s22_data()
    
    s_pos_a=[s11_pos1,s12_pos1,s21_pos1,s22_pos1]
    s_pos_a_ch=[sw2_port_1,sw2_port_1]
            
    if (curva_s_parameter==True):
        fig=plt.figure()
        plt.plot(freq_data_mhz,s11_pos1)
        plt.title('Parâmetro S11 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_1)+'_s11.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s12_pos1)
        plt.title('Parâmetro S12 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_1)+'_s12.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s21_pos1)
        plt.title('Parâmetro S21 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_1)+'_s21.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s22_pos1)
        plt.title('Parâmetro S22 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_1)+'_s22.png',dpi=fig.dpi)
        plt.close(fig)
        

    
    


    s11_pos1=np.array([[s11_pos1]]).T
    s12_pos1=np.array([[s12_pos1]]).T
    s21_pos1=np.array([[s21_pos1]]).T
    s22_pos1=np.array([[s22_pos1]]).T
    sparam_pos1 = np.c_[s11_pos1, s12_pos1, s21_pos1, s22_pos1]
    
    tela_leds.ui.progressBar.setValue(12.5+percentual)
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra s parameter",tela_leds.repaint())
    print("barra s parameter",QApplication.processEvents()) 

    #Data acquisition for channel 1-2 or 3-4
    print ("Porta "+str(sw2_port_1)+ " - " + str(sw2_port_2)+" do Switch")
    rfsw_2.sw2_pos(ip_sw2,sw2_port_1,sw2_port_2)
    leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_1, sw2_port_2, tela_leds)

    s11_pos2=vna.get_s11_data()
    s12_pos2=vna.get_s12_data()
    s21_pos2=vna.get_s21_data()
    s22_pos2=vna.get_s22_data()
    
    s_pos_b=[s11_pos2,s12_pos2,s21_pos2,s22_pos2]
    s_pos_b_ch=[sw2_port_1,sw2_port_2]
    
    if (curva_s_parameter==True):
        fig=plt.figure()
        plt.plot(freq_data_mhz,s11_pos2)
        plt.title('Parâmetro S11 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_2)+'_s11.png',dpi=fig.dpi)
        plt.close(fig)
        
        
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s12_pos2)
        plt.title('Parâmetro S12 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_2)+'_s12.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s21_pos2)
        plt.title('Parâmetro S21 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_2)+'_s21.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s22_pos2)
        plt.title('Parâmetro S22 [Ch:'+str(sw2_port_1)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_1)+str(sw2_port_2)+'_s22.png',dpi=fig.dpi)
        plt.close(fig)
        
    
    
    

    s11_pos2=np.array([[s11_pos2]]).T
    s12_pos2=np.array([[s12_pos2]]).T
    s21_pos2=np.array([[s21_pos2]]).T
    s22_pos2=np.array([[s22_pos2]]).T
    sparam_pos2 = np.c_[s11_pos2, s12_pos2, s21_pos2, s22_pos2]
    
    
    tela_leds.ui.progressBar.setValue(25+percentual)
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra s parameter",tela_leds.repaint())
    print("barra s parameter",QApplication.processEvents()) 
    
    
    #Data acquisition for channel 2-1 or 4-3
    print ("Porta "+str(sw2_port_2)+ " - " + str(sw2_port_1)+" do Switch")
    rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_1) #(4,3)
    leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_1, tela_leds)

    s11_pos3=vna.get_s11_data()
    s12_pos3=vna.get_s12_data()
    s21_pos3=vna.get_s21_data()
    s22_pos3=vna.get_s22_data()
    
    s_pos_c=[s11_pos3,s12_pos3,s21_pos3,s22_pos3]
    s_pos_c_ch=[sw2_port_2,sw2_port_1]

    if (curva_s_parameter==True):
        fig=plt.figure()
        plt.plot(freq_data_mhz,s11_pos3)
        plt.title('Parâmetro S11 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_1)+'_s11.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s12_pos3)
        plt.title('Parâmetro S12 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_1)+'_s12.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s21_pos3)
        plt.title('Parâmetro S21 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_1)+'_s21.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s22_pos3)
        plt.title('Parâmetro S22 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_1)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_1)+'_s22.png',dpi=fig.dpi)
        plt.close(fig)
        


    s11_pos3=np.array([[s11_pos3]]).T
    s12_pos3=np.array([[s12_pos3]]).T
    s21_pos3=np.array([[s21_pos3]]).T
    s22_pos3=np.array([[s22_pos3]]).T
    sparam_pos3 = np.c_[s11_pos3, s12_pos3, s21_pos3, s22_pos3]

    tela_leds.ui.progressBar.setValue(37.5+percentual)
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra s parameter",tela_leds.repaint())
    print("barra s parameter",QApplication.processEvents()) 

    #Data acquisition for channel 2-2 or 4-4
    print ("Porta "+str(sw2_port_2)+ " - " + str(sw2_port_2)+" do Switch")
    rfsw_2.sw2_pos(ip_sw2,sw2_port_2,sw2_port_2)
    leds_rf_switch(sw1_port_1, sw1_port_2, sw2_port_2, sw2_port_2, tela_leds)

    s11_pos4=vna.get_s11_data()
    s12_pos4=vna.get_s12_data()
    s21_pos4=vna.get_s21_data()
    s22_pos4=vna.get_s22_data()
    
    s_pos_d=[s11_pos4,s12_pos4,s21_pos4,s22_pos4]
    s_pos_d_ch=[sw2_port_2,sw2_port_2]
    
    if (curva_s_parameter==True):
        fig=plt.figure()
        plt.plot(freq_data_mhz,s11_pos4)
        plt.title('Parâmetro S11 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_2)+'_s11.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s12_pos4)
        plt.title('Parâmetro S12 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_2)+'_s12.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s21_pos4)
        plt.title('Parâmetro S21 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_2)+'_s21.png',dpi=fig.dpi)
        plt.close(fig)
        
        fig=plt.figure()
        plt.plot(freq_data_mhz,s22_pos4)
        plt.title('Parâmetro S22 [Ch:'+str(sw2_port_2)+'-'+str(sw2_port_2)+']')
        plt.xlabel('FREQUENCY [MHz]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        #plt.show()
        fig.savefig(datapath_save_figure+'ch_'+str(sw2_port_2)+str(sw2_port_2)+'_s22.png',dpi=fig.dpi)
        plt.close(fig)
        

    s11_pos4=np.array([[s11_pos4]]).T
    s12_pos4=np.array([[s12_pos4]]).T
    s21_pos4=np.array([[s21_pos4]]).T
    s22_pos4=np.array([[s22_pos4]]).T
    sparam_pos4 = np.c_[s11_pos4, s12_pos4, s21_pos4, s22_pos4]

    tela_leds.ui.progressBar.setValue(50+percentual)
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra s parameter",tela_leds.repaint())
    print("barra s parameter",QApplication.processEvents()) 


    freq_data=vna.get_frequency_data()
    freq_data_file=np.array([[freq_data]]).T
    sparam=np.c_[freq_data_file, sparam_pos1, sparam_pos2, sparam_pos3, sparam_pos4]
    
    print("\nSaving test data...")

    #test_lib.list_to_file(0,sparam,datapath_save + serial_number + "_data_ch_"+str(sw2_port_1)+ "_" + str(sw2_port_2)+".txt")

    return (sparam,
            s_pos_a,s_pos_a_ch,s_pos_b,s_pos_b_ch,s_pos_c,s_pos_c_ch,s_pos_d,s_pos_d_ch,freq_data,freq_data_mhz)
