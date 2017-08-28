import numpy as np
#import matlab.engine
from math import sqrt, floor
import time
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication


def missing_codes (missing_codes_total,NUM_PONTS_CRATE,AMPLITUDE_SINAL_ENTRADA,
                   numero_media,MAX_CONTAGEM_ADC,eng,grafico_check,perda_filtro_missingcodes,tela_leds):
    
    #Converte o sinal de entrada de votls para o formato de leitura do AD
    #Converte o valor de dBm para Volts, considerando um sistema de 50 Ohms
    #(valor inserido pelo usário como Tensão de saída do Gerador de Sinais - Input)
    #esses valores já são dados em volts-pico através da leitura do AD
    amplitude_volts=sqrt((50/1000)*pow(10,((AMPLITUDE_SINAL_ENTRADA-perda_filtro_missingcodes)/10)))
    
    #Converte a tensão de entrada em valor AD
    sinal_entrada_crate=(amplitude_volts)*MAX_CONTAGEM_ADC;
    sinal_entrada_crate=floor(sinal_entrada_crate)
    
    print(AMPLITUDE_SINAL_ENTRADA-perda_filtro_missingcodes, "[dBm]",amplitude_volts,"[volts]",sinal_entrada_crate,"[crate]")
 
    #Determina todos os valores possíveis de serem lidos pelo AD
    valores_possiveis_crate=[]            
    z=0
    for z in range (-sinal_entrada_crate,sinal_entrada_crate+1,1):
        valores_possiveis_crate.append(z)
    
    tela_leds.ui.progressBar.setValue(5)  
    tela_leds.repaint()
    QApplication.processEvents() 
    
    #Calcula o histograma     
    (hist_ch1, bin_edges_ch1) = np.histogram(missing_codes_total[0], bins = valores_possiveis_crate)
    (hist_ch2, bin_edges_ch2) = np.histogram(missing_codes_total[1], bins = valores_possiveis_crate)
    (hist_ch3, bin_edges_ch3) = np.histogram(missing_codes_total[2], bins = valores_possiveis_crate)
    (hist_ch4, bin_edges_ch4) = np.histogram(missing_codes_total[3], bins = valores_possiveis_crate)
   
    #Plota o histograma
    missingcodes_detected_ch1=[]
    missingcodes_detected_ch2=[]
    missingcodes_detected_ch3=[]
    missingcodes_detected_ch4=[]
    
    missing_positions_ch1=[]
    missing_positions_ch2=[]
    missing_positions_ch3=[]
    missing_positions_ch4=[]
    
    i=0
    contador0_1=0
    contador1_1=0
        
    contador0_2=0
    contador1_2=0

    contador0_3=0
    contador1_3=0

    contador0_4=0
    contador1_4=0
    
    for i in range (0,len(valores_possiveis_crate)-1):
        if(hist_ch1[i]==0):
            missingcodes_detected_ch1.append(1)
            missing_positions_ch1.append(i+1-sinal_entrada_crate) #o primeiro valor não temos pois o histograma mascara ele - posição 0
            contador0_1=contador0_1+1
        else:
            missingcodes_detected_ch1.append(0)
            contador1_1=contador1_1+1
       
        if(hist_ch2[i]==0):
            missingcodes_detected_ch2.append(1)
            missing_positions_ch2.append(i+1-sinal_entrada_crate)
            contador0_2=contador0_2+1
        else:
            missingcodes_detected_ch2.append(0)
            contador1_2=contador1_2+1
        
        if(hist_ch3[i]==0):
            missingcodes_detected_ch3.append(1)
            missing_positions_ch3.append(i+1-sinal_entrada_crate)
            contador0_3=contador0_3+1
        else:
            missingcodes_detected_ch3.append(0)
            contador1_3=contador1_3+1
        
        if(hist_ch4[i]==0):
            missingcodes_detected_ch4.append(1)
            missing_positions_ch4.append(i+1-sinal_entrada_crate)
            contador0_4=contador0_4+1
        else:
            missingcodes_detected_ch4.append(0)
            contador1_4=contador1_4+1
            
        #tela_leds.ui.progressBar.setValue((i+1)*90/(len(valores_possiveis_crate)-1)+5)  
        #tela_leds.repaint()
        #QApplication.processEvents() 


    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents() 

    contador_ch1=[contador0_1,contador1_1]
    contador_ch2=[contador0_2,contador1_2]
    contador_ch3=[contador0_3,contador1_3]
    contador_ch4=[contador0_4,contador1_4]
    
    contador=[contador_ch1,contador_ch2,contador_ch3,contador_ch4]
    
    canal1_result="MISSING CODES: CANAL 1: #valores com zero: " + str(contador[0][0]) + " #valores corretos:" + str(contador[0][1])
    canal2_result="MISSING CODES: CANAL 2: #valores com zero: " + str(contador[1][0]) + " #valores corretos:" + str(contador[1][1])
    canal3_result="MISSING CODES: CANAL 3: #valores com zero: " + str(contador[2][0]) + " #valores corretos:" + str(contador[2][1])
    canal4_result="MISSING CODES: CANAL 4: #valores com zero: " + str(contador[3][0]) + " #valores corretos:" + str(contador[3][1])
    print(canal1_result)
    print(canal2_result)
    print(canal3_result)
    print(canal4_result)
    
    missingcodes_result_aprovacao=[]
    for i in range (0,4):
        if (contador[i][0]!=0):
            missingcodes_result_aprovacao.append("FAIL")
        else:
            missingcodes_result_aprovacao.append("OK")
    
    
    #Vetor com as posições que não foram convertidas no AD
    missingcodes_detected_positions=[missing_positions_ch1,missing_positions_ch2,missing_positions_ch3,missing_positions_ch4]
    missingcodes_result_value_final=[contador[0],contador[1],contador[2],contador[3]]
    missingcodes_result_final=[canal1_result,canal2_result,canal3_result,canal4_result]
    
    
    
   
    if (grafico_check==True):
        #Gráfico Canal 1
        plt.bar(bin_edges_ch1[:-1], missingcodes_detected_ch1, width = 1)
        plt.xlim(min(bin_edges_ch1), max(bin_edges_ch1))
        plt.xlabel('Valores de Leituras do AD [Canal 1] - Range: '+str(valores_possiveis_crate[0])+' - '+str(valores_possiveis_crate[len(valores_possiveis_crate)-1])+']')
        plt.ylabel('Falhas Detectadas')
        plt.show()
        
        plt.bar(bin_edges_ch2[:-1], missingcodes_detected_ch2, width = 1)
        plt.xlim(min(bin_edges_ch2), max(bin_edges_ch2))
        plt.xlabel('Valores de Leituras do AD [Canal 2] - Range: ['+str(valores_possiveis_crate[0])+' - '+str(valores_possiveis_crate[len(valores_possiveis_crate)-1])+']')
        plt.ylabel('Falhas Detectadas')
        plt.show()  

        plt.bar(bin_edges_ch3[:-1], missingcodes_detected_ch3, width = 1)
        plt.xlim(min(bin_edges_ch3), max(bin_edges_ch3))
        plt.xlabel('Valores de Leituras do AD [Canal 3] - Range: ['+str(valores_possiveis_crate[0])+' - '+str(valores_possiveis_crate[len(valores_possiveis_crate)-1])+']')
        plt.ylabel('Falhas Detectadas')
        plt.show()
        
        plt.bar(bin_edges_ch4[:-1], missingcodes_detected_ch4, width = 1)
        plt.xlim(min(bin_edges_ch4), max(bin_edges_ch4))
        plt.xlabel('Valores de Leituras do AD [Canal 4] - Range: ['+str(valores_possiveis_crate[0])+' - '+str(valores_possiveis_crate[len(valores_possiveis_crate)-1])+']')
        plt.ylabel('Falhas Detectadas')
        plt.show()        
 

    return(missingcodes_result_value_final,missingcodes_detected_positions,missingcodes_result_final,missingcodes_result_aprovacao,sinal_entrada_crate)