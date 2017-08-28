import time
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def dif_amp(channel_dif_amp_dBFS,frequencia_fft_half,eng,grafico_check,tela_leds,AMPLITUDE_SINAL_ENTRADA_DIF_AMP,dif_amp_criterio):
   
   
    #channel_dif_amp_dBFS[vez da potencia][switch][canal]
    '''print("tem que ser 5 potencia",len(channel_dif_amp_dBFS))
    print("tem que ser 4 switch",len(channel_dif_amp_dBFS[0]))
    print("tem que ser 1 media",len(channel_dif_amp_dBFS[0][0]))
    print("tem que ser 4 canal",len(channel_dif_amp_dBFS[0][0][0]))
    print("tem que ser fft",len(channel_dif_amp_dBFS[0][0][0][0]))'''
    
    amplitude_fund_input_freq_ch_1=-1000
    amplitude_fund_input_freq_ch_2=-1000
    amplitude_fund_input_freq_ch_3=-1000
    amplitude_fund_input_freq_ch_4=-1000
    
    amplitude_fund_input_freq_ch1_list=[]
    amplitude_fund_input_freq_ch2_list=[]
    amplitude_fund_input_freq_ch3_list=[]
    amplitude_fund_input_freq_ch4_list=[]
    
    freq_fund_input_freq_ch1_list=[]
    freq_fund_input_freq_ch2_list=[]
    freq_fund_input_freq_ch3_list=[]
    freq_fund_input_freq_ch4_list=[]
    

    number_of_power_simulation=0
    
    while(number_of_power_simulation<11):
        i=0
        for i in range (0, len(frequencia_fft_half)):
            if (channel_dif_amp_dBFS[number_of_power_simulation][0][0][0][i]>amplitude_fund_input_freq_ch_1):
                amplitude_fund_input_freq_ch_1 = channel_dif_amp_dBFS[number_of_power_simulation][0][0][0][i]           
                freq1=i
            
            if (channel_dif_amp_dBFS[number_of_power_simulation][1][0][1][i]>amplitude_fund_input_freq_ch_2):
                amplitude_fund_input_freq_ch_2 = channel_dif_amp_dBFS[number_of_power_simulation][1][0][1][i]
                freq2=i 
                
            if (channel_dif_amp_dBFS[number_of_power_simulation][2][0][2][i]>amplitude_fund_input_freq_ch_3):
                amplitude_fund_input_freq_ch_3 = channel_dif_amp_dBFS[number_of_power_simulation][2][0][2][i]
                freq3 = i
            
            if (channel_dif_amp_dBFS[number_of_power_simulation][3][0][3][i]>amplitude_fund_input_freq_ch_4):
                amplitude_fund_input_freq_ch_4 = channel_dif_amp_dBFS[number_of_power_simulation][3][0][3][i]
                freq4 =i
        
        amplitude_fund_input_freq_ch1_list.append(amplitude_fund_input_freq_ch_1)
        amplitude_fund_input_freq_ch2_list.append(amplitude_fund_input_freq_ch_2)
        amplitude_fund_input_freq_ch3_list.append(amplitude_fund_input_freq_ch_3)
        amplitude_fund_input_freq_ch4_list.append(amplitude_fund_input_freq_ch_4)
        
        freq_fund_input_freq_ch1_list.append(freq1)
        freq_fund_input_freq_ch2_list.append(freq2)
        freq_fund_input_freq_ch3_list.append(freq3)
        freq_fund_input_freq_ch4_list.append(freq4)
        
        tela_leds.ui.progressBar.setValue((number_of_power_simulation+1)*60/11)
        tela_leds.repaint()
        QApplication.processEvents()
        
        number_of_power_simulation=number_of_power_simulation+1
    
    print("Amplitudes do Canal 1")
    print(amplitude_fund_input_freq_ch1_list)
    print("Frequencias do Canal 1")
    print(freq_fund_input_freq_ch1_list)
    
    print("Amplitudes do Canal 2")
    print(amplitude_fund_input_freq_ch2_list)
    print("Frequencias do Canal 2")
    print(freq_fund_input_freq_ch2_list)

    print("Amplitudes do Canal 3")
    print(amplitude_fund_input_freq_ch3_list)
    print("Frequencias do Canal 3")
    print(freq_fund_input_freq_ch3_list)
    
    print("Amplitudes do Canal 4")
    print(amplitude_fund_input_freq_ch4_list)
    print("Frequencias do Canal 4")
    print(freq_fund_input_freq_ch4_list)
    
    dif_amp_ch_1_3=[]
    dif_amp_ch_2_4=[]
    number_of_power_simulation=0
    while(number_of_power_simulation<11): 
        dif_amp_ch_1_3.append(abs(amplitude_fund_input_freq_ch1_list[number_of_power_simulation]-amplitude_fund_input_freq_ch3_list[number_of_power_simulation]))
        dif_amp_ch_2_4.append(abs(amplitude_fund_input_freq_ch2_list[number_of_power_simulation]-amplitude_fund_input_freq_ch4_list[number_of_power_simulation]))
        
        number_of_power_simulation=number_of_power_simulation+1
    
       
    #Calcular a Diferença entre o valor obtido na menor amplitude de entrada com os demais valores calculados
    number_of_power_simulation=0
    dif_amp_ch_1_3_final=[]
    dif_amp_ch_2_4_final=[]
    while(number_of_power_simulation<11):
        dif_amp_ch_1_3_final.append(abs(dif_amp_ch_1_3[0])-abs(dif_amp_ch_1_3[number_of_power_simulation]))
        dif_amp_ch_2_4_final.append(abs(dif_amp_ch_2_4[0])-abs(dif_amp_ch_2_4[number_of_power_simulation]))
        number_of_power_simulation=number_of_power_simulation+1
        
    print("Valores obtidos para os Canais 1-3:")
    print(dif_amp_ch_1_3)
    print("Valores obtidos para os Canais 2-4:") 
    print(dif_amp_ch_2_4)   
    print("Valores obtidos para os Canais 1-3 (dif. entre os canais com o de menor pot. de entr.:")
    print(dif_amp_ch_1_3_final)
    print("Valores obtidos para os Canais 2-4 (dif. entre os canais com o de menor pot. de entr.:")    
    print(dif_amp_ch_2_4_final)
    
    tela_leds.ui.progressBar.setValue(85)
    tela_leds.repaint()
    QApplication.processEvents()
    
    #vetor x
    i=0
    x=AMPLITUDE_SINAL_ENTRADA_DIF_AMP
    vetor_input_signal=[]
    for i in range (0,11):
        vetor_input_signal.append(x+2*i)
    
    
    if (grafico_check==True):
        plt.plot(vetor_input_signal,dif_amp_ch_1_3_final)
        plt.title('Gráfico utilizado no cálculo do DIF. AMP - Porta do AD:1-3')
        plt.xlabel('Potência de Entrada [dBm]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        plt.show()

        plt.plot(vetor_input_signal,dif_amp_ch_2_4_final)
        plt.title('Gráfico utilizado no cálculo do DIF. AMP - Porta do AD:2-4')
        plt.xlabel('Potência de Entrada [dBm]')
        plt.ylabel('AMPLITUDE [dB]')
        plt.grid()
        plt.show()
   
    dif_amp_values=[dif_amp_ch_1_3_final,dif_amp_ch_2_4_final]
    
    
    teste_1=0
    teste_2=0
    i=0    
    for i in range (0,11):
        #Canal 1-3
        if (abs(dif_amp_values[0][i])>dif_amp_criterio):
            teste_1=teste_1+1
        #Canal 2-4
        if (abs(dif_amp_values[1][i])>dif_amp_criterio):
            teste_2=teste_2+1
                
    if(teste_1==0):
        aux1_aprovacao="OK"
    else:
        aux1_aprovacao="Falhou"
    if(teste_2==0):
        aux2_aprovacao="OK"
    else:
        aux2_aprovacao="Falhou"
    
    if (aux1_aprovacao!="OK" or aux2_aprovacao !="OK"):
        teste_aprovacao="FAIL"
    else:
        teste_aprovacao="OK"
    
    return(dif_amp_values,teste_aprovacao)