from math import log10, sqrt
"import matlab.engine"
import matplotlib.pyplot as plt

def sinad(channel_fft_volts,channel_volts,channel_fft_dBFS_half_with_harmonics,
          frequencia_fft_half,NUM_PONTS_FFT,FREQUENCY_INPUT,
          FUNDO_ESCALA_ADC,
          eng,switch_port,n_media,grafico_check,utilizarMatlab_check): 
        
    i=0
    amplitude_fund_input_freq_ch_1=-1000
    amplitude_fund_input_freq_ch_2=-1000
    amplitude_fund_input_freq_ch_3=-1000
    amplitude_fund_input_freq_ch_4=-1000
    
    freq_amplitude_aux1=0
    freq_amplitude_aux2=0
    freq_amplitude_aux3=0
    freq_amplitude_aux4=0
    
    for i in range (0, len(frequencia_fft_half)):
        if (channel_fft_volts[0][i]>amplitude_fund_input_freq_ch_1):
            amplitude_fund_input_freq_ch_1 = channel_fft_volts[0][i]
            freq_amplitude_aux1=i
            
        if (channel_fft_volts[1][i]>amplitude_fund_input_freq_ch_2):
            amplitude_fund_input_freq_ch_2 = channel_fft_volts[1][i]
            freq_amplitude_aux2=i
            
        if (channel_fft_volts[2][i]>amplitude_fund_input_freq_ch_3):
            amplitude_fund_input_freq_ch_3 = channel_fft_volts[2][i]
            freq_amplitude_aux3=i
            
        if (channel_fft_volts[3][i]>amplitude_fund_input_freq_ch_4):
            amplitude_fund_input_freq_ch_4 = channel_fft_volts[3][i]
            freq_amplitude_aux4=i

    aux1=0
    aux2=0
    aux3=0
    aux4=0

    teste=[]
    i=0
    for i in range (0,len(frequencia_fft_half)):

        if(i!=freq_amplitude_aux1 and (i>1.03*freq_amplitude_aux1 or i<0.97*freq_amplitude_aux1)):
            if(channel_fft_volts[0][i]!=float('-inf')):
                aux1=aux1+pow(channel_fft_volts[0][i],2)
                teste.append(channel_fft_volts[0][i])
        if(i!=freq_amplitude_aux2 and (i>1.03*freq_amplitude_aux2 or i<0.97*freq_amplitude_aux2)):
            if(channel_fft_volts[1][i]!=float('-inf')):
                aux2=aux2+pow(channel_fft_volts[1][i],2)
        if(i!=freq_amplitude_aux3 and (i>1.03*freq_amplitude_aux3 or i<0.97*freq_amplitude_aux3)):
            if(channel_fft_volts[2][i]!=float('-inf')):
                aux3=aux3+pow(channel_fft_volts[2][i],2)
        if(i!=freq_amplitude_aux4 and (i>1.03*freq_amplitude_aux4 or i<0.97*freq_amplitude_aux4)):
            if(channel_fft_volts[3][i]!=float('-inf')):
                aux4=aux4+pow(channel_fft_volts[3][i],2)
    
        
   #Cálculo do SINAD - Método Próprio
    sinad_ch1=20*log10(amplitude_fund_input_freq_ch_1/sqrt(aux1))                
    sinad_ch2=20*log10(amplitude_fund_input_freq_ch_2/sqrt(aux2))   
    sinad_ch3=20*log10(amplitude_fund_input_freq_ch_3/sqrt(aux3))   
    sinad_ch4=20*log10(amplitude_fund_input_freq_ch_4/sqrt(aux4)) 
    
    #Cálculo do SINAD - Matlab
    
    if (utilizarMatlab_check==True):
        sinad_ch1_matlab=eng.sinad(matlab.double(channel_volts[0]),float(FREQUENCY_INPUT))               
        sinad_ch2_matlab=eng.sinad(matlab.double(channel_volts[1]),float(FREQUENCY_INPUT)) 
        sinad_ch3_matlab=eng.sinad(matlab.double(channel_volts[2]),float(FREQUENCY_INPUT)) 
        sinad_ch4_matlab=eng.sinad(matlab.double(channel_volts[3]),float(FREQUENCY_INPUT))  
        sinad_ch_matlab=[sinad_ch1_matlab,sinad_ch2_matlab,sinad_ch3_matlab,sinad_ch4_matlab]
    
    else:
        sinad_ch_matlab='-inf'

    sinad_ch=[sinad_ch1,sinad_ch2,sinad_ch3,sinad_ch4]
    
    if (grafico_check==True):
        #Gráfico em volts com as harmônicas
        plt.plot(frequencia_fft_half,channel_fft_dBFS_half_with_harmonics[switch_port-1])
        plt.title('Gráfico utilizado no cálculo do SINAD/ENOB - Porta do AD:'+str(switch_port)+' #:'+str(n_media+1))
        plt.xlabel('FREQUENCY [Hz]')
        plt.ylabel('AMPLITUDE [dBFS]')
        plt.grid()
        plt.show()

  
    return (sinad_ch,sinad_ch_matlab)
    
    