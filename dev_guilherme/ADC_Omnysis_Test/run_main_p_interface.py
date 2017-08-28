#import paramiko
#import matlab.engine
from start_communication import start_communication
from get_data import get_data
from sfdr_dBFS import sfdr_dBFS
from enob import enob
from zeros_fft_volts import zeros_fft_volts
from frequency_fft_detect import frequency_fft_detect
from switch_connection import switch_connection
from result_parameters import result_parameters, result_data,results_components
#from list_rw_file2 import list_to_file, list_to_file_aux
from list_rw_file2 import list_to_file_aux
from crosstalk import crosstalk
from missing_codes import missing_codes
from half_ptts import half_ptts
from volts_to_dBFS import volts_to_dBFS
from snr_dBFS import snr_dBFS
from sinad import sinad
from dif_amp import dif_amp
from eeprom import eeprom
import time
import matplotlib.pyplot as plt
from fpga import fpga
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from ics854s01i import ics854s01i
from si571 import si571
from ad9510 import ad9510
import datetime



def run_main_p_interface(ip_crate,ip_switch,ip_gerador_sinais_clock,ip_gerador_sinais_input,
                         posicao_AFC,posicao_AD,freq_clock,freq_in,amp_clock,amp_in,freq_clock_missingcodes,freq_in_missingcodes,amp_clock_missingcodes,amp_in_missingcodes,perda_filtro_missingcodes,
                         pts_FFT,pts_crate,pts_crate_missingcodes,n_requisicoes,
                         snr_criterio,sfdr_criterio,enob_criterio,crosstalk_criterio,dif_amp_criterio,
                         snr_check,enob_check,sfdr_check,crosstalk_check,missingcodes_check,dif_ampl_check,grafico_check,gravar_fpga_check,
                         utilizarMatlab_check,all_tests_selection,tela_leds,
                         eeprom_check,si571_check, ad9510_check, ics854s01i_check, sensor_temp_check,
                         operador,n_serie_adc):

    #Start Time do Teste
    start_time_general=datetime.datetime.now()
    start_time_general_str=start_time_general.strftime("%Y-%m-%d %H:%M:%S")
        
    #CONSTANTS
    FUNDO_ESCALA_ADC = 2.25 #volts
    AMPLITUDE_SINAL_ENTRADA=amp_in #dB
    AMPLITUDE_SINAL_CLOCK=amp_clock #dB
    MAX_CONTAGEM_ADC = 32768 #2^15 --> ADC de 16 bits
    NUM_PONTS_CRATE = pts_crate #100000
    NUM_PONTS_CRATE_MISSINGCODES=pts_crate_missingcodes #1000000
    NUM_PONTS_FFT = pts_FFT #99995
    IP_SWITCH=ip_switch
    IP_CRATE=ip_crate
    IP_GERADOR_SINAIS_CLOCK=ip_gerador_sinais_clock
    IP_GERADOR_SINAIS_INPUT=ip_gerador_sinais_input
    USERNAME = 'root'
    PASSWORD = 'root'
    POSITION_CRATE=posicao_AFC #Posição do slot do crate
    POSITION_ADC=posicao_AD #(1 ou 0) - 1 para em baixo,0 para em cima
    FREQUENCY_SAMPLE= freq_clock*1000000 #fs -> frequeência de amostragem = frequência do clock 118230000 (5dBm)
    FREQUENCY_INPUT = freq_in*1000000 #fin -> frequência do sinal de entrada 499944000 (9.5dBm com filtro passa baixa com perda de 3dBm)
    numero_media=n_requisicoes
    datapath_save="result/"
    serial_number=n_serie_adc
    FREQUENCY_SAMPLE_MISSINGCODES= freq_clock_missingcodes*1000000 #fs -> frequeência de amostragem = frequência do clock 118230000 (5dBm)
    FREQUENCY_INPUT_MISSINGCODES = freq_in_missingcodes*1000000 #fin -> frequência do sinal de entrada 499944000 (9.5dBm com filtro passa baixa com perda de 3dBm)
    AMPLITUDE_SINAL_ENTRADA_MISSINGCODES=amp_in_missingcodes #dB
    AMPLITUDE_SINAL_CLOCK_MISSINGCODES=amp_clock_missingcodes #dB
    AMPLITUDE_SINAL_ENTRADA_DIF_AMP= -22.5 #dBm
    
    #Configura a comunicação com o Crate e o MATLAB
    #(eng,ssh,sig_gen_clock,sig_gen_input)=start_communication(IP_CRATE,USERNAME,PASSWORD,POSITION_CRATE,IP_SWITCH,IP_GERADOR_SINAIS_CLOCK,IP_GERADOR_SINAIS_INPUT)
    print("Verificando as comunicações...")
    (eng,sig_gen_clock,sig_gen_input,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result)=start_communication(IP_CRATE,USERNAME,PASSWORD,POSITION_CRATE,IP_SWITCH,IP_GERADOR_SINAIS_CLOCK,IP_GERADOR_SINAIS_INPUT,tela_leds,utilizarMatlab_check)
    
    
    if (gravar_fpga_check==True):
        print("Iniciando a gravação da fpga...")
        tela_leds.ui.kled_fpga.setState(1)
        tela_leds.ui.kled_fpga.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led fpga",tela_leds.repaint())
        print("Led fpga",QApplication.processEvents())
        
        (fpga_str_result)=fpga(gravar_fpga_check,IP_CRATE,USERNAME,PASSWORD,POSITION_CRATE,tela_leds)
        
        tela_leds.ui.kled_fpga.setState(1)
        tela_leds.ui.kled_fpga.setColor(QtGui.QColor(0, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led fpga",tela_leds.repaint())
        print("Led fpga",QApplication.processEvents())
    else:
        fpga_str_result="FGPA: Opcao nao selecionada"
        print(fpga_str_result)
        tela_leds.ui.kled_fpga.setState(1)
        tela_leds.ui.kled_fpga.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led fpga",tela_leds.repaint())
        print("Led fpga",QApplication.processEvents())
        
    
    if (all_tests_selection==True):
        snr_check=True
        enob_check=True
        sfdr_check=True
        crosstalk_check=True
        missingcodes_check=True
        dif_ampl_check=True
        eeprom_check=True
        si571_check=True
        ad9510_check=True
        ics854s01i_check=True
        sensor_temp_check=True
        

    print("Iniciou Teste do AD")

    
    #Variáveis para armazenar os resultados
    snr_result_values=[]
    sfdr_result_values=[]
    enob_result_values=[]

    snr_result_values_matlab=[]
    sfdr_result_values_matlab=[]
    enob_result_values_matlab=[]

    crosstalk_values=[]
    missing_codes_total=[]

    #Check para gerar os logs de cada aquisicao de dados
    #snr, sfdr, enob e crosstalk
    aquisition_nivel_1=0 
    #missingcodes
    aquisition_nivel_2=0 
    #dif amp
    aquisition_nivel_3=0 
    
    #Calcula as frequências para plotar no gráfico
    frequencia_fft=frequency_fft_detect(NUM_PONTS_FFT, FREQUENCY_SAMPLE)
    frequencia_fft_half=[]
    i=0
    for i in range (0,int(NUM_PONTS_FFT/2)-1):
        frequencia_fft_half.append(frequencia_fft[i])
    
    
    #Cria zeros para fft e volts - Servem para o cálculo das médias
    (channel_fft_media_dBFS,channel_volts_media)=zeros_fft_volts(NUM_PONTS_FFT, NUM_PONTS_CRATE)
   
    #Realiza a aquisição de dados
    channel_volts_list=[]
    channel_fft_volts_list=[]
    crate_data_list=[]
    
    
    #Aquisição de Dados 
    if (snr_check==True or enob_check==True or sfdr_check==True or crosstalk_check==True):
        
        aquisition_nivel_1=1
        
        tela_leds.ui.progressBar.setValue(0)  
        tela_leds.repaint()
        QApplication.processEvents() 
        
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led aquisicao de dados",tela_leds.repaint())
        print("Led aquisicao de dados",QApplication.processEvents())
        
        #Set do Gerador de Sinais - Input Signal
        sig_gen_clock.set_frequency(FREQUENCY_SAMPLE)
        sig_gen_clock.set_amplitude(AMPLITUDE_SINAL_CLOCK)
        sig_gen_input.set_frequency(FREQUENCY_INPUT)
        sig_gen_input.set_amplitude(AMPLITUDE_SINAL_ENTRADA)
        time.sleep(1)
        
        tela_leds.ui.progressBar.setValue(5)  
        tela_leds.repaint()
        QApplication.processEvents() 
            
        print("Aquisição de Dados Iniciada...")
        n_canal_switch=0
        while (n_canal_switch<4): #4 Canais no switch, e cada canal representa a vez em que 1 canal do AD ficou ativo
            
            #Aciona a porta PORT do SWITCH
            switch_port=n_canal_switch+1
            switch_connection(IP_SWITCH,switch_port)
            print("Realizando medição AD do Canal", n_canal_switch+1)
        
 
            (channel_volts,channel_fft_volts,crate_data)=get_data(eng, switch_port, IP_CRATE, USERNAME, PASSWORD, POSITION_CRATE, POSITION_ADC, 
                                                                             NUM_PONTS_CRATE, FUNDO_ESCALA_ADC, MAX_CONTAGEM_ADC, NUM_PONTS_FFT, 
                                                                             FREQUENCY_SAMPLE, FREQUENCY_INPUT, numero_media, frequencia_fft, 
                                                                             channel_fft_media_dBFS, channel_volts_media)
            channel_volts_list.append(channel_volts)
            channel_fft_volts_list.append(channel_fft_volts)
            crate_data_list.append(crate_data)
        
            tela_leds.ui.progressBar.setValue(n_canal_switch*75/4+5)  
            tela_leds.repaint()
            QApplication.processEvents() 
            
            n_canal_switch=n_canal_switch+1
        
        #channel_volts_list[canal do switch ativo][número de vez da média executado na rotina][canal do AD com dados coletados][valores deste canal]    
        
        #print(channel_volts_list[0][0][0])
        #print(channel_volts_list[1][0][1])
        #print(channel_volts_list[2][0][2])
        #print(channel_volts_list[3][0][3])
        #input("chegou")
        

        #Converte todos os valores obtidos de da FFT de VOLTS para dBFS
        canal_1_switch=[]
        canal_2_switch=[]
        canal_3_switch=[]
        canal_4_switch=[]
        i=0
   
        while (i<numero_media):
            canal_1_switch.append(volts_to_dBFS(channel_fft_volts_list[0][i],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng))
            canal_2_switch.append(volts_to_dBFS(channel_fft_volts_list[1][i],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng))
            canal_3_switch.append(volts_to_dBFS(channel_fft_volts_list[2][i],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng))
            canal_4_switch.append(volts_to_dBFS(channel_fft_volts_list[3][i],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng))
            
            tela_leds.ui.progressBar.setValue((i+1)*10/numero_media+80)  
            tela_leds.repaint()
            QApplication.processEvents() 
            
            i=i+1
            
            

        channel_fft_dBFS_list=[canal_1_switch,canal_2_switch,canal_3_switch,canal_4_switch]
    
        #Utiliza apenas a metade do gráfico. Prepara também dois vetores distintos: Um com harmônicas, e outro sem
  
        canal_1_switch_with_harmonics=[]
        canal_2_switch_with_harmonics=[]
        canal_3_switch_with_harmonics=[]
        canal_4_switch_with_harmonics=[]

        canal_1_switch_no_harmonics=[]
        canal_2_switch_no_harmonics=[]
        canal_3_switch_no_harmonics=[]
        canal_4_switch_no_harmonics=[]
        

        canal_1_switch_with_harmonics_volts=[]
        canal_2_switch_with_harmonics_volts=[]
        canal_3_switch_with_harmonics_volts=[]
        canal_4_switch_with_harmonics_volts=[]
    
        canal_1_switch_no_harmonics_volts=[]
        canal_2_switch_no_harmonics_volts=[]
        canal_3_switch_no_harmonics_volts=[]
        canal_4_switch_no_harmonics_volts=[]
  
        i=0
        while (i<numero_media):
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[0][i],channel_fft_volts_list[0][i],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,1)
            canal_1_switch_with_harmonics.append(aux_with_harmonics)
            canal_1_switch_no_harmonics.append(aux_no_harmonics)
            canal_1_switch_with_harmonics_volts.append(aux_with_harmonics_volts)
            canal_1_switch_no_harmonics_volts.append(aux_no_harmonics_volts)
        
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[1][i],channel_fft_volts_list[1][i],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,2)
            canal_2_switch_with_harmonics.append(aux_with_harmonics)
            canal_2_switch_no_harmonics.append(aux_no_harmonics)
            canal_2_switch_with_harmonics_volts.append(aux_with_harmonics_volts)
            canal_2_switch_no_harmonics_volts.append(aux_no_harmonics_volts)
        
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[2][i],channel_fft_volts_list[2][i],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,3)
            canal_3_switch_with_harmonics.append(aux_with_harmonics)
            canal_3_switch_no_harmonics.append(aux_no_harmonics)
            canal_3_switch_with_harmonics_volts.append(aux_with_harmonics_volts)
            canal_3_switch_no_harmonics_volts.append(aux_no_harmonics_volts)
        
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[3][i],channel_fft_volts_list[3][i],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,4)
            canal_4_switch_with_harmonics.append(aux_with_harmonics)
            canal_4_switch_no_harmonics.append(aux_no_harmonics)
            canal_4_switch_with_harmonics_volts.append(aux_with_harmonics_volts)
            canal_4_switch_no_harmonics_volts.append(aux_no_harmonics_volts)
            
            tela_leds.ui.progressBar.setValue(i*10/numero_media+90)  
            tela_leds.repaint()
            QApplication.processEvents()
                
            i=i+1   
    
        channel_fft_dBFS_half_with_harmonics_list=[canal_1_switch_with_harmonics,canal_2_switch_with_harmonics,canal_3_switch_with_harmonics,canal_4_switch_with_harmonics]
        channel_fft_dBFS_half_no_harmonics_list=[canal_1_switch_no_harmonics,canal_2_switch_no_harmonics,canal_3_switch_no_harmonics,canal_4_switch_no_harmonics]
        channel_fft_half_with_harmonics_list=[canal_1_switch_with_harmonics_volts,canal_2_switch_with_harmonics_volts,canal_3_switch_with_harmonics_volts,canal_4_switch_with_harmonics_volts]
        channel_fft_half_no_harmonics_list=[canal_1_switch_no_harmonics_volts,canal_2_switch_no_harmonics_volts,canal_3_switch_no_harmonics_volts,canal_4_switch_no_harmonics_volts]

        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        
        tela_leds.ui.progressBar.setValue(100)  
        #tela_leds.repaint()
        #QApplication.processEvents()
        
        print("Led aquisicao de dados",tela_leds.repaint())
        print("Led aquisicao de dados",QApplication.processEvents())
        

        
    else:
        
        print("Dados não serão adquiridos")
        
    #Teste do SNR
    if (snr_check==True):
        print("Iniciou o Teste do SNR")
        tela_leds.ui.kled_snr.setState(1)
        tela_leds.ui.kled_snr.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        
        tela_leds.ui.progressBar.setValue(0)  
        print("Led snr",tela_leds.repaint())
        print("Led snr",QApplication.processEvents())
        
        snr_ch1=[]
        snr_ch2=[]
        snr_ch3=[]
        snr_ch4=[]
    
        snr_ch1_matlab=[]
        snr_ch2_matlab=[]
        snr_ch3_matlab=[]
        snr_ch4_matlab=[]
        
        step=0
    
        i=0
        while (i<numero_media):
            (snr_aux,snr_aux_matlab)=snr_dBFS(channel_fft_half_no_harmonics_list[0][i],channel_volts_list[0][i],channel_fft_dBFS_half_no_harmonics_list[0][i],
                                          frequencia_fft_half,FREQUENCY_INPUT,
                                          FUNDO_ESCALA_ADC,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,
                                          eng,1,i,grafico_check,utilizarMatlab_check)
            snr_ch1.append(snr_aux)
            snr_ch1_matlab.append(snr_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*20/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
    
            (snr_aux,snr_aux_matlab)=snr_dBFS(channel_fft_half_no_harmonics_list[1][i],channel_volts_list[1][i],channel_fft_dBFS_half_no_harmonics_list[1][i],
                                          frequencia_fft_half,FREQUENCY_INPUT,
                                          FUNDO_ESCALA_ADC,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,
                                          eng,2,i,grafico_check,utilizarMatlab_check)
            snr_ch2.append(snr_aux)
            snr_ch2_matlab.append(snr_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*40/numero_media +step)  
            tela_leds.repaint()
            QApplication.processEvents() 
        
            (snr_aux,snr_aux_matlab)=snr_dBFS(channel_fft_half_no_harmonics_list[2][i],channel_volts_list[2][i],channel_fft_dBFS_half_no_harmonics_list[2][i],
                                          frequencia_fft_half,FREQUENCY_INPUT,
                                          FUNDO_ESCALA_ADC,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,
                                          eng,3,i,grafico_check,utilizarMatlab_check)
            snr_ch3.append(snr_aux)
            snr_ch3_matlab.append(snr_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*60/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
        
            (snr_aux,snr_aux_matlab)=snr_dBFS(channel_fft_half_no_harmonics_list[3][i],channel_volts_list[3][i],channel_fft_dBFS_half_no_harmonics_list[3][i],
                                          frequencia_fft_half,FREQUENCY_INPUT,
                                          FUNDO_ESCALA_ADC,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,
                                          eng,4,i,grafico_check,utilizarMatlab_check)
            snr_ch4.append(snr_aux)
            snr_ch4_matlab.append(snr_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*80/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
            
            step=(i+1)*60/numero_media+step
        
            i=i+1
    
        aux1=0
        aux2=0
        aux3=0
        aux4=0

        i=0
        while (i<numero_media):
            aux1=aux1+snr_ch1[i][0]
            aux2=aux2+snr_ch2[i][1]
            aux3=aux3+snr_ch3[i][2]
            aux4=aux4+snr_ch4[i][3]
            i=i+1
    
        aux1=aux1/numero_media
        aux2=aux2/numero_media
        aux3=aux3/numero_media
        aux4=aux4/numero_media
        
        snr_result_values=[aux1,aux2,aux3,aux4]
        print("SNR Médio - Método Pŕoprio:",snr_result_values)
    
        if(utilizarMatlab_check==True):
            aux1=0
            aux2=0
            aux3=0
            aux4=0
            i=0
            while (i<numero_media):
                aux1=aux1+snr_ch1_matlab[i][0]
                aux2=aux2+snr_ch2_matlab[i][1]
                aux3=aux3+snr_ch3_matlab[i][2]
                aux4=aux4+snr_ch4_matlab[i][3]
                i=i+1
    
            aux1=aux1/numero_media
            aux2=aux2/numero_media
            aux3=aux3/numero_media
            aux4=aux4/numero_media
        
            snr_result_values_matlab=[aux1,aux2,aux3,aux4]
            print("SNR Médio - Método Matlab:",snr_result_values_matlab)
        else:
            snr_result_values_matlab='-inf'
            print("SNR Médio - Método Matlab: Matlab não utilizado")

        tela_leds.ui.progressBar.setValue(90)  
        tela_leds.repaint()
        QApplication.processEvents()             
        
        #Teste de Aprovação - LED
        j=0
        teste_aprovacao=0
        for j in range (0,4):
            #Avaliação do SNR
            if(utilizarMatlab_check==True):
                if (snr_result_values[j]>snr_result_values_matlab[j]):
                    aux = snr_result_values[j]
                else:
                    aux = snr_result_values_matlab[j]
            else:
                aux=snr_result_values[j]
            
            if (aux < snr_criterio):
                #Falhou
                aux2=1
            else:
                #Aprovado
                aux2=0
            teste_aprovacao=teste_aprovacao+aux2
        if(teste_aprovacao==0):
            #Todos os canais foram aprovados
            tela_leds.ui.kled_snr.setState(1)
            tela_leds.ui.kled_snr.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.ui.progressBar.setValue(100)  
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led snr",tela_leds.repaint())
            print("Led snr",QApplication.processEvents())
        else:
            #Algum/Todos os canais falharam/falhou
            tela_leds.ui.kled_snr.setState(1)
            tela_leds.ui.kled_snr.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.ui.progressBar.setValue(100)  
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led snr",tela_leds.repaint())
            print("Led snr",QApplication.processEvents())
            
    else:
        print("Teste do SNR não realizado")
        snr_result_values ="Teste não realizado"
        snr_result_values_matlab="Teste não realizado"
        tela_leds.ui.kled_snr.setState(1)
        tela_leds.ui.kled_snr.setColor(QtGui.QColor(0, 0, 255))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led snr",tela_leds.repaint())
        print("Led snr",QApplication.processEvents())
        
    #Teste do SINAD e ENOB
    if (enob_check==True):
        print("Iniciou o Teste do ENOB")
        tela_leds.ui.kled_enob.setState(1)
        tela_leds.ui.kled_enob.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.ui.progressBar.setValue(0)  
        
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led enob",tela_leds.repaint())
        print("Led enob",QApplication.processEvents())
        
        sinad_ch1=[]
        sinad_ch2=[]
        sinad_ch3=[]
        sinad_ch4=[]
    
        sinad_ch1_matlab=[]
        sinad_ch2_matlab=[]
        sinad_ch3_matlab=[]
        sinad_ch4_matlab=[]
    
        i=0
        step=0
        
        while (i<numero_media):
            (sinad_aux,sinad_aux_matlab)=sinad(channel_fft_half_with_harmonics_list[0][i],channel_volts_list[0][i],channel_fft_dBFS_half_with_harmonics_list[0][i],
                                           frequencia_fft_half,NUM_PONTS_FFT,FREQUENCY_INPUT,
                                           FUNDO_ESCALA_ADC,
                                           eng,1,i,grafico_check, utilizarMatlab_check)
            sinad_ch1.append(sinad_aux)
            sinad_ch1_matlab.append(sinad_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*20/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 


            (sinad_aux,sinad_aux_matlab)=sinad(channel_fft_half_with_harmonics_list[1][i],channel_volts_list[1][i],channel_fft_dBFS_half_with_harmonics_list[1][i],
                                           frequencia_fft_half,NUM_PONTS_FFT,FREQUENCY_INPUT,
                                           FUNDO_ESCALA_ADC,
                                           eng,2,i,grafico_check,utilizarMatlab_check)
            sinad_ch2.append(sinad_aux)
            sinad_ch2_matlab.append(sinad_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*40/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
        
            (sinad_aux,sinad_aux_matlab)=sinad(channel_fft_half_with_harmonics_list[2][i],channel_volts_list[2][i],channel_fft_dBFS_half_with_harmonics_list[2][i],
                                           frequencia_fft_half,NUM_PONTS_FFT,FREQUENCY_INPUT,
                                           FUNDO_ESCALA_ADC,
                                           eng,3,i,grafico_check,utilizarMatlab_check)
            sinad_ch3.append(sinad_aux)
            sinad_ch3_matlab.append(sinad_aux_matlab)
            
            tela_leds.ui.progressBar.setValue((i+1)*60/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
        
            (sinad_aux,sinad_aux_matlab)=sinad(channel_fft_half_with_harmonics_list[3][i],channel_volts_list[3][i],channel_fft_dBFS_half_with_harmonics_list[3][i],
                                           frequencia_fft_half,NUM_PONTS_FFT,FREQUENCY_INPUT,
                                           FUNDO_ESCALA_ADC,
                                           eng,4,i,grafico_check,utilizarMatlab_check)
            sinad_ch4.append(sinad_aux)
            sinad_ch4_matlab.append(sinad_aux_matlab)        
       
            tela_leds.ui.progressBar.setValue((i+1)*80/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
            
            step=(i+1)*80/numero_media+step
            
            i=i+1
    
        sinad_aux1=0
        sinad_aux2=0
        sinad_aux3=0
        sinad_aux4=0

        
        i=0
        while (i<numero_media):
            sinad_aux1=sinad_aux1+sinad_ch1[i][0]
            sinad_aux2=sinad_aux2+sinad_ch2[i][1]
            sinad_aux3=sinad_aux3+sinad_ch3[i][2]
            sinad_aux4=sinad_aux4+sinad_ch4[i][3]
        
            i=i+1
    
        sinad_aux1=sinad_aux1/numero_media
        sinad_aux2=sinad_aux2/numero_media
        sinad_aux3=sinad_aux3/numero_media
        sinad_aux4=sinad_aux4/numero_media
        
        sinad_media=[sinad_aux1,sinad_aux2,sinad_aux3,sinad_aux4]
        print("SINAD Médio - Método Pŕoprio:",sinad_media)
    
        if (utilizarMatlab_check==True):
            sinad_aux1=0
            sinad_aux2=0
            sinad_aux3=0
            sinad_aux4=0
            i=0
            while (i<numero_media):
                sinad_aux1=sinad_aux1+sinad_ch1_matlab[i][0]
                sinad_aux2=sinad_aux2+sinad_ch2_matlab[i][1]
                sinad_aux3=sinad_aux3+sinad_ch3_matlab[i][2]
                sinad_aux4=sinad_aux4+sinad_ch4_matlab[i][3]
                i=i+1
    
            sinad_aux1=sinad_aux1/numero_media
            sinad_aux2=sinad_aux2/numero_media
            sinad_aux3=sinad_aux3/numero_media
            sinad_aux4=sinad_aux4/numero_media
        
            sinad_media_matlab=[sinad_aux1,sinad_aux2,sinad_aux3,sinad_aux4]
            print("SINAD Médio - Método Matlab:",sinad_media_matlab)
        else:
            sinad_media_matlab="-inf"
            print("SINAD Médio - Método Matlab: Matlab não utilizado")

        tela_leds.ui.progressBar.setValue(90)  
        tela_leds.repaint()
        QApplication.processEvents() 
            
        #Teste do ENOB
        (enob_result_values,enob_result_values_matlab)=enob(sinad_media,sinad_media_matlab,utilizarMatlab_check)
    
        print("ENOB Médio - Método Pŕoprio: ",enob_result_values)
        if (utilizarMatlab_check==True):
            print("ENOB Médio - Método Matlab: ",enob_result_values_matlab) 
        else:
            print("ENOB Médio - Método Matlab: Matlab não utilizado")
        #Teste de Aprovação - LED
        j=0
        teste_aprovacao=0
        for j in range (0,4):
            #Avaliação do ENOB
            if (utilizarMatlab_check==True):
                if (enob_result_values[j]>enob_result_values_matlab[j]):
                    aux = enob_result_values[j]
                else:
                    aux = enob_result_values_matlab[j]
            else:
                aux = enob_result_values[j]
            if (aux < snr_criterio):
                #Falhou
                aux2=1
            else:
                #Aprovado
                aux2=0
        teste_aprovacao=teste_aprovacao+aux2
        if(teste_aprovacao==0):
            #Todos os canais foram aprovados
            tela_leds.ui.kled_enob.setState(1)
            tela_leds.ui.kled_enob.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            tela_leds.ui.progressBar.setValue(100) 
            print("Led enob",tela_leds.repaint())
            print("Led enob",QApplication.processEvents())
        else:
            #Algum/Todos os canais falharam/falhou
            tela_leds.ui.kled_enob.setState(1)
            tela_leds.ui.kled_enob.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            tela_leds.ui.progressBar.setValue(100) 
            print("Led enob",tela_leds.repaint())
            print("Led enob",QApplication.processEvents())
        
    else:
        print("Teste do ENOB não realizado")
        enob_result_values="Teste não realizado" 
        enob_result_values_matlab="Teste não realizado"
        tela_leds.ui.kled_enob.setState(1)
        tela_leds.ui.kled_enob.setColor(QtGui.QColor(0, 0, 255))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led enob",tela_leds.repaint())
        print("Led enob",QApplication.processEvents())
   
    #Teste do SFDR (Spurious Free Dynamic Range) Desconsidera as harmônicas da placa, conforme sugestão do LNLS
    if(sfdr_check==True):
        print("Iniciou o Teste do SFDR")
        tela_leds.ui.kled_sfdr.setState(1)
        tela_leds.ui.kled_sfdr.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        tela_leds.ui.progressBar.setValue(0) 
        print("Led sfdr",tela_leds.repaint())
        print("Led sfdr",QApplication.processEvents())
        
        ch1_fft_media_with_harmonics=[]
        ch2_fft_media_with_harmonics=[]
        ch3_fft_media_with_harmonics=[]
        ch4_fft_media_with_harmonics=[]

        i=0
        j=0
        while (j<len(frequencia_fft_half)):
            aux1=0
            aux2=0
            aux3=0
            aux4=0
        
            i=0
            while (i<numero_media):
                aux1=aux1+channel_fft_dBFS_half_no_harmonics_list[0][i][0][j]
                aux2=aux2+channel_fft_dBFS_half_no_harmonics_list[1][i][1][j]
                aux3=aux3+channel_fft_dBFS_half_no_harmonics_list[2][i][2][j]
                aux4=aux4+channel_fft_dBFS_half_no_harmonics_list[3][i][3][j]

                i=i+1
            
            ch1_fft_media_with_harmonics.append(aux1)
            ch2_fft_media_with_harmonics.append(aux2)
            ch3_fft_media_with_harmonics.append(aux3)
            ch4_fft_media_with_harmonics.append(aux4)
        
            j=j+1
        
        i=0
        while(i<len(frequencia_fft_half)):
            ch1_fft_media_with_harmonics[i]=ch1_fft_media_with_harmonics[i]/numero_media
            ch2_fft_media_with_harmonics[i]=ch2_fft_media_with_harmonics[i]/numero_media
            ch3_fft_media_with_harmonics[i]=ch3_fft_media_with_harmonics[i]/numero_media
            ch4_fft_media_with_harmonics[i]=ch4_fft_media_with_harmonics[i]/numero_media
            i=i+1
   
        channel_fft_media_dBFS=[ch1_fft_media_with_harmonics,ch2_fft_media_with_harmonics,ch3_fft_media_with_harmonics,ch4_fft_media_with_harmonics]
   
        if (grafico_check==True):
            z=0
            while (z<4):
                plt.plot(frequencia_fft_half,channel_fft_media_dBFS[z])
                plt.title('Gráfico utilizado no cálculo do SFDR (Sem Harmônicas)- Porta do AD:'+str(z+1))
                plt.xlabel('FREQUENCY [Hz]')
                plt.ylabel('AMPLITUDE [dBFS]')
                plt.grid()
                plt.show()
                #time.sleep(5)
                z=z+1
   
        tela_leds.ui.progressBar.setValue(10)
        tela_leds.repaint()
        QApplication.processEvents()
        
        (sfdr_result_values,sfdr_result_values_matlab)=sfdr_dBFS(channel_fft_media_dBFS,channel_volts_list,
                                              switch_port,frequencia_fft_half,frequencia_fft,
                                              FREQUENCY_INPUT,NUM_PONTS_FFT,eng,numero_media,utilizarMatlab_check,tela_leds)
    
        print("SFDR Médio - Método Próprio: ",sfdr_result_values)
        
        if(utilizarMatlab_check==True):
            print("SFDR Médio - Método Matlab: ",sfdr_result_values_matlab)
        else:
            print("SFDR Médio - Método Matlab: Matlab não utilizado")
        #Teste de Aprovação - LED
        j=0
        teste_aprovacao=0
        for j in range (0,4):
            #Avaliação do SFDR
            if(utilizarMatlab_check==True):
                if (sfdr_result_values[j]>sfdr_result_values_matlab[j]):
                    aux = sfdr_result_values[j]
                else:
                    aux = sfdr_result_values_matlab[j]
            else:
                aux = sfdr_result_values[j]
            if (aux < sfdr_criterio):
                #Falhou
                aux2=1
            else:
                #Aprovado
                aux2=0
        teste_aprovacao=teste_aprovacao+aux2
        if(teste_aprovacao==0):
            #Todos os canais foram aprovados
            tela_leds.ui.kled_sfdr.setState(1)
            tela_leds.ui.kled_sfdr.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            tela_leds.ui.progressBar.setValue(100)
            print("Led sfdr",tela_leds.repaint())
            print("Led sfdr",QApplication.processEvents())
        else:
            #Algum/Todos os canais falharam/falhou
            tela_leds.ui.kled_sfdr.setState(1)
            tela_leds.ui.kled_sfdr.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            tela_leds.ui.progressBar.setValue(100)
            print("Led sfdr",tela_leds.repaint())
            print("Led sfdr",QApplication.processEvents())
    
    else:
        print("Teste do SFDR não realizado")
        sfdr_result_values ="Teste não realizado"
        sfdr_result_values_matlab="Teste não realizado"
        tela_leds.ui.kled_sfdr.setState(1)
        tela_leds.ui.kled_sfdr.setColor(QtGui.QColor(0, 0, 255))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led sfdr",tela_leds.repaint())
        print("Led sfdr",QApplication.processEvents())
    
    #Teste de Crosstalk
    if (crosstalk_check==True):
        print("Iniciou o Teste do CROSSTALK")
        tela_leds.ui.kled_crosstalk.setState(1)
        tela_leds.ui.kled_crosstalk.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        tela_leds.ui.progressBar.setValue(0)
        print("Led crosstalk",tela_leds.repaint())
        print("Led crosstalk",QApplication.processEvents())
        
        crosstalk_value_ch1=[]
        crosstalk_value_ch2=[]
        crosstalk_value_ch3=[]
        crosstalk_value_ch4=[]
   
        i=0
        step=0
        while (i<numero_media):
            (crosstalk_values,crosstalk_canal)=crosstalk(channel_fft_dBFS_half_with_harmonics_list[0][i],frequencia_fft_half,
                                                         NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,FREQUENCY_INPUT,
                                                         eng,1,i,grafico_check)
        
            crosstalk_value_ch1.append(crosstalk_values)
            crosstalk_canal_ch1=crosstalk_canal

            tela_leds.ui.progressBar.setValue((i+1)*20/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
                    
            (crosstalk_values,crosstalk_canal)=crosstalk(channel_fft_dBFS_half_with_harmonics_list[1][i],frequencia_fft_half,
                                                         NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,FREQUENCY_INPUT,
                                                         eng,2,i,grafico_check)
        
            crosstalk_value_ch2.append(crosstalk_values)
            crosstalk_canal_ch2=crosstalk_canal

            tela_leds.ui.progressBar.setValue((i+1)*40/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
                    
            (crosstalk_values,crosstalk_canal)=crosstalk(channel_fft_dBFS_half_with_harmonics_list[2][i],frequencia_fft_half,
                                                         NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,FREQUENCY_INPUT,
                                                         eng,3,i,grafico_check)
        
            crosstalk_value_ch3.append(crosstalk_values)
            crosstalk_canal_ch3=crosstalk_canal
        
            tela_leds.ui.progressBar.setValue((i+1)*60/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 
            
            (crosstalk_values,crosstalk_canal)=crosstalk(channel_fft_dBFS_half_with_harmonics_list[3][i],frequencia_fft_half,
                                                         NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,FREQUENCY_INPUT,
                                                         eng,4,i,grafico_check)
        
            crosstalk_value_ch4.append(crosstalk_values)
            crosstalk_canal_ch4=crosstalk_canal

            tela_leds.ui.progressBar.setValue((i+1)*80/numero_media+step)  
            tela_leds.repaint()
            QApplication.processEvents() 

            step=(i+1)*80/numero_media+step
            i=i+1
    
           
        crosstalk_values=[crosstalk_value_ch1,crosstalk_value_ch2,crosstalk_value_ch3,crosstalk_value_ch4]
        crosstalk_canal_analisado=[crosstalk_canal_ch1,crosstalk_canal_ch2,crosstalk_canal_ch3,crosstalk_canal_ch4]
        
        #obtém as médias  
        i=0
        j=0
    
        for j in range (0, 4):
            aux1=0
            aux2=0
            aux3=0
            for i in range (0, numero_media):
                aux1=aux1+crosstalk_values[j][i][0]
                aux2=aux2+crosstalk_values[j][i][1]
                aux3=aux3+crosstalk_values[j][i][2]
            crosstalk_values[j]=[aux1/numero_media,aux2/numero_media,aux3/numero_media] 
            print("Resultado do Crosstalk Canal ",str(j+1)," - Valores: ",crosstalk_values[j]," Canais: ",crosstalk_canal_analisado[j])    
            
        
        #Teste de Aprovação - LED
        j=0
        z=0
        teste_aprovacao=0
        #Avaliação do CROSSTALK
        for j in range (0,4):
            for z in range (0,3):
                aux = crosstalk_values[j][z]
                if (aux < crosstalk_criterio):
                    #Falhou
                    aux2=1
                else:
                    #Aprovado
                    aux2=0
                teste_aprovacao=teste_aprovacao+aux2
        if(teste_aprovacao==0):
            #Todos os canais foram aprovados
            tela_leds.ui.kled_crosstalk.setState(1)
            tela_leds.ui.kled_crosstalk.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            tela_leds.ui.progressBar.setValue(100) 
            print("Led crosstalk",tela_leds.repaint())
            print("Led crosstalk",QApplication.processEvents())
        else:
            #Algum/Todos os canais falharam/falhou
            tela_leds.ui.kled_crosstalk.setState(1)
            tela_leds.ui.kled_crosstalk.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            tela_leds.ui.progressBar.setValue(100)
            print("Led crosstalk",tela_leds.repaint())
            print("Led crosstalk",QApplication.processEvents())
            

    else:
        print("Teste do CROSSTALK não realizado")
        crosstalk_values="Teste não realizado"
        crosstalk_canal_analisado=[[2,3,4],[1,3,4],[1,2,4],[1,2,3]]
        tela_leds.ui.kled_crosstalk.setState(1)
        tela_leds.ui.kled_crosstalk.setColor(QtGui.QColor(0, 0, 255))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led crosstalk",tela_leds.repaint())
        print("Led crosstalk",QApplication.processEvents())
    
    if (missingcodes_check==True ):
        
        print("Aquisição de Dados para o Missing Codes Iniciada...")
        aquisition_nivel_2=1
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        tela_leds.ui.progressBar.setValue(0)
        print("Led missingcodes",tela_leds.repaint())
        print("Led missingcodes",QApplication.processEvents())
        
        crate_data_list_missingcodes=[]

        sig_gen_clock.set_frequency(FREQUENCY_SAMPLE_MISSINGCODES)
        sig_gen_clock.set_amplitude(AMPLITUDE_SINAL_CLOCK_MISSINGCODES)
        sig_gen_input.set_frequency(FREQUENCY_INPUT_MISSINGCODES)
        sig_gen_input.set_amplitude(AMPLITUDE_SINAL_ENTRADA_MISSINGCODES)
        
        time.sleep(1)
        
        n_canal_switch=0
        while (n_canal_switch<4): #4 Canais no switch, e cada canal representa a vez em que 1 canal do AD ficou ativo
            #Aciona a porta PORT do SWITCH
            switch_port=n_canal_switch+1
            switch_connection(IP_SWITCH,switch_port)
            print("Realizando medição AD do Canal", n_canal_switch+1)
        
            #Set do Gerador de Sinais - Input Signal
            
  
            (channel_volts_missingcodes,channel_fft_volts_missingcodes,crate_data_missingcodes)=get_data(eng, switch_port, IP_CRATE, USERNAME, PASSWORD, POSITION_CRATE, POSITION_ADC,
                                                                                                         NUM_PONTS_CRATE_MISSINGCODES, FUNDO_ESCALA_ADC, MAX_CONTAGEM_ADC, NUM_PONTS_FFT,
                                                                                                         FREQUENCY_SAMPLE_MISSINGCODES, FREQUENCY_INPUT_MISSINGCODES, numero_media, frequencia_fft,
                                                                                                         channel_fft_media_dBFS, channel_volts_media)
            crate_data_list_missingcodes.append(crate_data_missingcodes)
        
            tela_leds.ui.progressBar.setValue((n_canal_switch+1)*100/4)
            tela_leds.repaint()
            QApplication.processEvents()
            
            n_canal_switch=n_canal_switch+1
        #channel_volts_missingcodes[posicao do switch ativa][numero media][canais adquiridos][pontos do "canal adquirido"]
        #print(len(crate_data_list_missingcodes))
        #print(len(crate_data_list_missingcodes[0]))
        #print(len(crate_data_list_missingcodes[0][0]))
        #print(len(crate_data_list_missingcodes[0][0][0]))
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led missingcodes",tela_leds.repaint())
        print("Led missingcodes",QApplication.processEvents())
    else:
        
        print("Dados para o Missing Codes não serão adquiridos")
        crate_data_list_missingcodes=("Dados para o Missing Codes não serão adquiridos")

  
       
    ##Calcula o Missing Codes
    if (missingcodes_check==True):
        
        
        print("Iniciou o Teste do MISSING CODES")
        
        tela_leds.ui.progressBar.setValue(0)  
        tela_leds.ui.kled_missing_codes.setState(1)
        tela_leds.ui.kled_missing_codes.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led missingcodes",tela_leds.repaint())
        print("Led missingcodes",QApplication.processEvents())
        
        aux1=crate_data_list_missingcodes[0][0][0]
        aux2=crate_data_list_missingcodes[1][0][1]
        aux3=crate_data_list_missingcodes[2][0][2]
        aux4=crate_data_list_missingcodes[3][0][3]
        
        missing_codes_total=[aux1,aux2,aux3,aux4]
        

        (missingcodes_result_value_final,missingcodes_detected_positions,
         missingcodes_result_final,missingcodes_result_aprovacao,sinal_entrada_crate)=missing_codes(missing_codes_total,NUM_PONTS_CRATE,AMPLITUDE_SINAL_ENTRADA_MISSINGCODES,
                                                                                numero_media,MAX_CONTAGEM_ADC,eng,grafico_check,perda_filtro_missingcodes,tela_leds)
    
        if(missingcodes_result_aprovacao[0]=="OK" and missingcodes_result_aprovacao[1]=="OK" and missingcodes_result_aprovacao[2]=="OK" and missingcodes_result_aprovacao[3]=="OK"):
            tela_leds.ui.kled_missing_codes.setState(1)
            tela_leds.ui.kled_missing_codes.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.ui.progressBar.setValue(100)  
            tela_leds.repaint()
            QApplication.processEvents()
            print("Led missingcodes",tela_leds.repaint())
            print("Led missingcodes",QApplication.processEvents())
        
        else:
            tela_leds.ui.kled_missing_codes.setState(1)
            tela_leds.ui.kled_missing_codes.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.ui.progressBar.setValue(100)  
            tela_leds.repaint()
            QApplication.processEvents()
            print("Led missingcodes",tela_leds.repaint())
            print("Led missingcodes",QApplication.processEvents())
            
    
    else:
        missingcodes_result_value_final="Teste não realizado"
        missingcodes_detected_positions="Teste não realizado"
        missingcodes_result_final="Teste não realizado"
        missingcodes_result_aprovacao=["Teste não realizado","Teste não realizado","Teste não realizado","Teste não realizado"]
        sinal_entrada_crate=0
        tela_leds.ui.kled_missing_codes.setState(1)
        tela_leds.ui.kled_missing_codes.setColor(QtGui.QColor(0, 0, 255))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led missingcodes",tela_leds.repaint())
        print("Led missingcodes",QApplication.processEvents())
 
 

    #Aquisição de Dados para o Teste de Linearidade do AD - Diferença das Amplitudes
    if (dif_ampl_check==True ):
        
        aquisition_nivel_3=1
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led aquisicao de dados",tela_leds.repaint())
        print("Led aquisicao de dados",QApplication.processEvents())
            
        print("Aquisição de Dados Iniciada - Diferença das Amplitudes...")
        
        number_of_power_simulation=0
        n_canal_switch=0
        channel_dif_amp_dBFS=[]
        channel_volts_list=[]
        channel_fft_volts_list=[]
        crate_data_dif_amp_list=[]
        step=0
        
        while(number_of_power_simulation<11):
            print("Realização medicação ",number_of_power_simulation+1,"de 11")
            sig_gen_clock.set_frequency(FREQUENCY_SAMPLE)
            sig_gen_clock.set_amplitude(AMPLITUDE_SINAL_CLOCK)
            sig_gen_input.set_frequency(FREQUENCY_INPUT)
            sig_gen_input.set_amplitude(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+number_of_power_simulation*2)
            time.sleep(1)
            n_canal_switch=0
            channel_fft_volts_list=[]
            crate_data_ch_switch=[]
            while (n_canal_switch<4): #4 Canais no switch, e cada canal representa a vez em que 1 canal do AD ficou ativo
                #Aciona a porta PORT do SWITCH
                switch_port=n_canal_switch+1
                switch_connection(IP_SWITCH,switch_port)
                print("Realizando medição AD do Canal", n_canal_switch+1)
                #Set do Gerador de Sinais - Input Signal
                
                #Varia a tensão de entrada de 0 até 8 dBm com step de 2 dBm
                
  
                (channel_volts,channel_fft_volts,crate_data)=get_data(eng, switch_port, IP_CRATE, USERNAME, PASSWORD, POSITION_CRATE, POSITION_ADC, 
                                                                             NUM_PONTS_CRATE, FUNDO_ESCALA_ADC, MAX_CONTAGEM_ADC, NUM_PONTS_FFT, 
                                                                             FREQUENCY_SAMPLE, FREQUENCY_INPUT, 1, frequencia_fft, 
                                                                             channel_fft_media_dBFS, channel_volts_media)
                
                channel_fft_volts_list.append(channel_fft_volts)
                crate_data_ch_switch.append(crate_data)
                #crate_data_ch_switch[canal_ativo_switch][num_media=1vez][4 canais do ad][valores]
                
                tela_leds.ui.progressBar.setValue((n_canal_switch+1)*9.08/4+step)  
                tela_leds.repaint()
                QApplication.processEvents() 
            
                n_canal_switch=n_canal_switch+1

            #Converte todos os valores obtidos de da FFT de VOLTS para dBFS
            #channel_fft_volts_list[switch][vez da média = 1 ie 0][4 canais][valores da fft]
            
            crate_data_dif_amp_list.append(crate_data_ch_switch)
            canal_1_switch=volts_to_dBFS(channel_fft_volts_list[0][0],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng)
            canal_2_switch=volts_to_dBFS(channel_fft_volts_list[1][0],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng)
            canal_3_switch=volts_to_dBFS(channel_fft_volts_list[2][0],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng)
            canal_4_switch=volts_to_dBFS(channel_fft_volts_list[3][0],NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng)

            channel_fft_dBFS_list=[canal_1_switch,canal_2_switch,canal_3_switch,canal_4_switch]
            
            #channel_fft_dBFS_list[4 switches][4 canais]

            #Utiliza apenas a metade do gráfico. Prepara também dois vetores distintos: Um com harmônicas, e outro sem
            canal_1_switch_with_harmonics=[]
            canal_2_switch_with_harmonics=[]
            canal_3_switch_with_harmonics=[]
            canal_4_switch_with_harmonics=[]

            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[0],channel_fft_volts_list[0][0],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,1)
            canal_1_switch_with_harmonics.append(aux_with_harmonics)
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[1],channel_fft_volts_list[1][0],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,2)
            canal_2_switch_with_harmonics.append(aux_with_harmonics)
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[2],channel_fft_volts_list[2][0],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,3)
            canal_3_switch_with_harmonics.append(aux_with_harmonics)
            (aux_with_harmonics,aux_no_harmonics,aux_with_harmonics_volts,aux_no_harmonics_volts) = half_ptts(channel_fft_dBFS_list[3],channel_fft_volts_list[3][0],frequencia_fft_half,FREQUENCY_INPUT, NUM_PONTS_FFT,4)
            canal_4_switch_with_harmonics.append(aux_with_harmonics)
            channel_fft_dBFS_half_with_harmonics_list=[canal_1_switch_with_harmonics,canal_2_switch_with_harmonics,canal_3_switch_with_harmonics,canal_4_switch_with_harmonics]
       

            channel_dif_amp_dBFS.append(channel_fft_dBFS_half_with_harmonics_list) #channel_dif_amp_dBFS[11 níveis de potência][4 canais ativos do switch][4 canais de ad][valores de 1 canal]
        
            step=step+9.08
 
            number_of_power_simulation=number_of_power_simulation+1
            
            
            #print("number_of_power_simulation",number_of_power_simulation)
            #print("size of channel_dif_amp_dBFS",len(channel_dif_amp_dBFS))

        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.ui.progressBar.setValue(100)
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led aquisicao de dados",tela_leds.repaint())
        print("Led aquisicao de dados",QApplication.processEvents())
        
        
    else:
        crate_data_dif_amp_list="-"
        print("Dados não serão adquiridos - Diferença das Amplitudes")  
        
        
    #Teste da DIFERENÇA DAS AMPLITUDES
    if (dif_ampl_check==True):
        print("Iniciou o Teste da DIF. AMP.")
        tela_leds.ui.kled_dif_amp.setState(1)
        tela_leds.ui.kled_dif_amp.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        tela_leds.ui.progressBar.setValue(0)
        print("Led dif amp",tela_leds.repaint())
        print("Led dif amp",QApplication.processEvents())

        
        (dif_amp_result_values,teste_aprovacao)=dif_amp(channel_dif_amp_dBFS,frequencia_fft_half,eng,grafico_check,tela_leds,AMPLITUDE_SINAL_ENTRADA_DIF_AMP,dif_amp_criterio)
        
        
        if(teste_aprovacao=="OK"):
            tela_leds.ui.kled_dif_amp.setState(1)
            tela_leds.ui.kled_dif_amp.setColor(QtGui.QColor(0, 255, 0))
            tela_leds.ui.progressBar.setValue(100)
            tela_leds.repaint()
            QApplication.processEvents()
            print("Led dif amp",tela_leds.repaint())
            print("Led dif amp",QApplication.processEvents())
        else:
            tela_leds.ui.kled_dif_amp.setState(1)
            tela_leds.ui.kled_dif_amp.setColor(QtGui.QColor(255, 0, 0))
            tela_leds.ui.progressBar.setValue(100)
            tela_leds.repaint()
            QApplication.processEvents()
            print("Led dif amp",tela_leds.repaint())
            print("Led dif amp",QApplication.processEvents())

    else:
        print("Teste da DIF. AMP. não realizado")
        dif_amp_result_values ="Teste não realizado"
        tela_leds.ui.kled_dif_amp.setState(1)
        tela_leds.ui.kled_dif_amp.setColor(QtGui.QColor(0, 0, 255))

        print("Led dif amp",tela_leds.repaint())
        print("Led dif amp",QApplication.processEvents())  
      

    #Teste do componente EEPROM
    if(eeprom_check==True):
        print("Teste do Componente EEPROM iniciado...")
        tela_leds.ui.kled_eeprom.setState(1)
        tela_leds.ui.kled_eeprom.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led eeprom",tela_leds.repaint())
        print("Led eeprom",QApplication.processEvents())
        
        (eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
         eeprom_all_values_dec,eeprom_all_values_hex,
         eeprom_memory_position_standard_dec,eeprom_memory_position_standard_hex,
         eeprom_value_write,eeprom_value_read)=eeprom(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds)
        
        if(eeprom_write_check_result=="OK" and eeprom_read_check_result=="OK"):
            tela_leds.ui.kled_eeprom.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led eeprom",tela_leds.repaint())
            print("Led eeprom",QApplication.processEvents())
            
        else:
            tela_leds.ui.kled_eeprom.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led eeprom",tela_leds.repaint())
            print("Led eeprom",QApplication.processEvents())
         
            
        if(eeprom_result=="OK"):
            tela_leds.ui.kled_eeprom.setState(1)
            tela_leds.ui.kled_eeprom.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led eeprom",tela_leds.repaint())
            print("Led eeprom",QApplication.processEvents())
        
        else:
            tela_leds.ui.kled_eeprom.setState(1)
            tela_leds.ui.kled_eeprom.setColor(QtGui.QColor(255,0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led eeprom",tela_leds.repaint())
            print("Led eeprom",QApplication.processEvents())
    
    else:
        print("Teste do Componente EEPROM não será realizado")
        eeprom_result="Teste não realizado"
        eeprom_write_check_result="Teste não realizado"
        eeprom_read_check_result="Teste não realizado"
        tela_leds.ui.kled_eeprom.setState(1)
        tela_leds.ui.kled_eeprom.setColor(QtGui.QColor(0,0,255))
        eeprom_all_values_dec="-"
        eeprom_all_values_hex="-"
        eeprom_memory_position_standard_dec="-"
        eeprom_memory_position_standard_hex="-"
        eeprom_value_write="-"
        eeprom_value_read="-"
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led eeprom",tela_leds.repaint())
        print("Led eeprom",QApplication.processEvents())
    
    
    #Teste do componente ICS854S01I
    if(ics854s01i_check==True):
        print("Teste do Componente ICS854S01I iniciado...")
        tela_leds.ui.kled_ics854s01i.setState(1)
        tela_leds.ui.kled_ics854s01i.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led ics854s01i",tela_leds.repaint())
        print("Led ics854s01i",QApplication.processEvents())
        
        (ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,ics854s01i_log)=ics854s01i(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds)
        
        if(ics854s01i_write_check_result=="OK" and ics854s01i_read_check_result=="OK"):
            tela_leds.ui.kled_ics854s01i.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ics854s01i",tela_leds.repaint())
            print("Led ics854s01i",QApplication.processEvents())
            
        else:
            tela_leds.ui.kled_ics854s01i.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ics854s01i",tela_leds.repaint())
            print("Led ics854s01i",QApplication.processEvents())
         
            
        if(ics854s01i_result=="OK"):
            tela_leds.ui.kled_ics854s01i.setState(1)
            tela_leds.ui.kled_ics854s01i.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ics854s01i",tela_leds.repaint())
            print("Led ics854s01i",QApplication.processEvents())
        
        else:
            tela_leds.ui.kled_ics854s01i.setState(1)
            tela_leds.ui.kled_ics854s01i.setColor(QtGui.QColor(255,0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ics854s01i",tela_leds.repaint())
            print("Led ics854s01i",QApplication.processEvents())
    
    else:
        print("Teste do Componente ICS854S01I não será realizado")
        ics854s01i_result="Teste não realizado"
        ics854s01i_write_check_result="Teste não realizado"
        ics854s01i_read_check_result="Teste não realizado"
        tela_leds.ui.kled_ics854s01i.setState(1)
        tela_leds.ui.kled_ics854s01i.setColor(QtGui.QColor(0,0,255))
        ics854s01i_log="-"
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led ics854s01i",tela_leds.repaint())
        print("Led ics854s01i",QApplication.processEvents())
    
    
    #Teste do componente SI571
    if(si571_check==True):
        print("Teste do Componente ICS854S01I iniciado...")
        tela_leds.ui.kled_si571.setState(1)
        tela_leds.ui.kled_si571.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led si571",tela_leds.repaint())
        print("Led si571",QApplication.processEvents())
        
        (si571_result,si571_write_check_result,si571_read_check_result,si571_log)=si571(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds)
        
        if(si571_write_check_result=="OK" and si571_read_check_result=="OK"):
            tela_leds.ui.kled_si571.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led si571",tela_leds.repaint())
            print("Led si571",QApplication.processEvents())
            
        else:
            tela_leds.ui.kled_si571.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led si571",tela_leds.repaint())
            print("Led si571",QApplication.processEvents())
         
            
        if(si571_result=="OK"):
            tela_leds.ui.kled_si571.setState(1)
            tela_leds.ui.kled_si571.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led si571",tela_leds.repaint())
            print("Led si571",QApplication.processEvents())
        
        else:
            tela_leds.ui.kled_si571.setState(1)
            tela_leds.ui.kled_si571.setColor(QtGui.QColor(255,0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led si571",tela_leds.repaint())
            print("Led si571",QApplication.processEvents())
    
    else:
        print("Teste do Componente SI571 não será realizado")
        si571_result="Teste não realizado"
        si571_write_check_result="Teste não realizado"
        si571_read_check_result="Teste não realizado"
        tela_leds.ui.kled_si571.setState(1)
        tela_leds.ui.kled_si571.setColor(QtGui.QColor(0,0,255))
        si571_log="-"
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led si571",tela_leds.repaint())
        print("Led si571",QApplication.processEvents())
 
 
    #Teste do componente AD9510
    if(ad9510_check==True):
        print("Teste do Componente AD9510 iniciado...")
        tela_leds.ui.kled_ad9510.setState(1)
        tela_leds.ui.kled_ad9510.setColor(QtGui.QColor(255, 255, 0))
        tela_leds.ui.kled_data_acquisition.setState(1)
        tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 255, 0))
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led ad9510",tela_leds.repaint())
        print("Led ad9510",QApplication.processEvents())
        
        (ad9510_result,ad9510_write_check_result,ad9510_read_check_result,ad9510_log)=ad9510(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds)
        
        if(ad9510_write_check_result=="OK" and ad9510_read_check_result=="OK"):
            tela_leds.ui.kled_ad9510.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ad9510",tela_leds.repaint())
            print("Led ad9510",QApplication.processEvents())
            
        else:
            tela_leds.ui.kled_ad9510.setState(1)
            tela_leds.ui.kled_data_acquisition.setColor(QtGui.QColor(255, 0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ad9510",tela_leds.repaint())
            print("Led ad9510",QApplication.processEvents())
         
            
        if(ad9510_result=="OK"):
            tela_leds.ui.kled_ad9510.setState(1)
            tela_leds.ui.kled_ad9510.setColor(QtGui.QColor(0, 255, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ad9510",tela_leds.repaint())
            print("Led ad9510",QApplication.processEvents())
        
        else:
            tela_leds.ui.kled_ad9510.setState(1)
            tela_leds.ui.kled_ad9510.setColor(QtGui.QColor(255,0, 0))
            #tela_leds.repaint()
            #QApplication.processEvents()
            print("Led ad9510",tela_leds.repaint())
            print("Led ad9510",QApplication.processEvents())
    
    else:
        print("Teste do Componente AD9510 não será realizado")
        ad9510_result="Teste não realizado"
        ad9510_write_check_result="Teste não realizado"
        ad9510_read_check_result="Teste não realizado"
        tela_leds.ui.kled_ad9510.setState(1)
        tela_leds.ui.kled_ad9510.setColor(QtGui.QColor(0,0,255))
        ad9510_log="-"
        #tela_leds.repaint()
        #QApplication.processEvents()
        print("Led ad9510",tela_leds.repaint())
        print("Led ad9510",QApplication.processEvents())   
 
 
        #Stop Time do Teste
    stop_time_general=datetime.datetime.now() #serve para cálculos de tempo
    stop_time_general_str=stop_time_general.strftime("%Y-%m-%d %H:%M:%S")
    
    #Duracao do Teste Inteiro           
    duracao_teste_general=((stop_time_general - start_time_general).total_seconds())/60
    duracao_teste_general_str=str(round(duracao_teste_general,4))
    
    #Analisa os resultados obtidos
    (snr_result_final,sfdr_result_final,enob_result_final,crosstalk_result_final,dif_amp_result_final,
           eeprom_result_final,ics854s01i_result_final,si571_result_final,ad9510_result_final,
           snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao,crosstalk_result_aprovacao,dif_amp_result_aprovacao,
           snr_result_value_final,sfdr_result_value_final,enob_result_value_final,crosstalk_result_values,dif_amp_result_value_final,
           result)=result_parameters(snr_result_values, snr_result_values_matlab, snr_criterio,
                               sfdr_result_values, sfdr_result_values_matlab, sfdr_criterio,
                               enob_result_values, enob_result_values_matlab, enob_criterio,
                               crosstalk_values,crosstalk_canal_analisado,crosstalk_criterio,
                               missingcodes_result_value_final,missingcodes_detected_positions,missingcodes_result_final,missingcodes_result_aprovacao,sinal_entrada_crate,
                               dif_amp_result_values,dif_amp_criterio, AMPLITUDE_SINAL_ENTRADA_DIF_AMP,
                               utilizarMatlab_check,
                               eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
                               ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,
                               si571_result,si571_write_check_result,si571_read_check_result,
                               ad9510_result,ad9510_write_check_result,ad9510_read_check_result,
                               start_time_general_str,stop_time_general_str,duracao_teste_general_str,serial_number,
                               fpga_str_result,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result,
                               FREQUENCY_INPUT,FREQUENCY_SAMPLE,FREQUENCY_INPUT_MISSINGCODES,FREQUENCY_SAMPLE_MISSINGCODES,
                               AMPLITUDE_SINAL_ENTRADA,AMPLITUDE_SINAL_CLOCK,AMPLITUDE_SINAL_ENTRADA_MISSINGCODES,AMPLITUDE_SINAL_CLOCK_MISSINGCODES,
                               NUM_PONTS_CRATE,NUM_PONTS_CRATE_MISSINGCODES,NUM_PONTS_FFT,
                               operador,n_serie_adc)




    #Salva os resultados finais
    list_to_file_aux(0,result, datapath_save+"test_results/"+ serial_number + "_final_results.txt")
    
    #Cria os Relatórios da Aquisição de dados
    result_data(aquisition_nivel_1,aquisition_nivel_2,aquisition_nivel_3,
                serial_number,datapath_save,
                crate_data_list,crate_data_list_missingcodes,crate_data_dif_amp_list,
                numero_media,NUM_PONTS_CRATE,NUM_PONTS_CRATE_MISSINGCODES,
                start_time_general_str,stop_time_general_str,duracao_teste_general_str,
                fpga_str_result,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result,
                FREQUENCY_INPUT,FREQUENCY_SAMPLE,FREQUENCY_INPUT_MISSINGCODES,FREQUENCY_SAMPLE_MISSINGCODES,
                AMPLITUDE_SINAL_ENTRADA,AMPLITUDE_SINAL_CLOCK,AMPLITUDE_SINAL_ENTRADA_MISSINGCODES,AMPLITUDE_SINAL_CLOCK_MISSINGCODES,AMPLITUDE_SINAL_ENTRADA_DIF_AMP)
    
    
    
    
    #Todos os dados de uma vez só
    #list_to_file(0,crate_data_list, datapath_save + serial_number + "_crate_data2.txt")
    
    
    
    #Salva os dados da EEPROM:
    results_components(eeprom_check,serial_number,datapath_save,
                       start_time_general_str,stop_time_general_str,duracao_teste_general_str,
                       fpga_str_result,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result,
                       eeprom_all_values_dec,eeprom_all_values_hex,
                       eeprom_memory_position_standard_dec,eeprom_memory_position_standard_hex,
                       eeprom_value_write,eeprom_value_read,
                       ics854s01i_check,ics854s01i_log,
                       si571_check,si571_log,
                       ad9510_check,ad9510_log)
           
           
    
           

    
 
    return(snr_result_value_final,sfdr_result_value_final,enob_result_value_final,crosstalk_values,missingcodes_result_value_final,dif_amp_result_values,
           snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao,crosstalk_result_aprovacao,missingcodes_result_aprovacao,dif_amp_result_aprovacao,
           eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
           ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,
           si571_result,si571_write_check_result,si571_read_check_result,
           ad9510_result,ad9510_write_check_result,ad9510_read_check_result,sinal_entrada_crate)


