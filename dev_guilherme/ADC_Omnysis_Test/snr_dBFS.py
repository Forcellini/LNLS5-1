from math import log10, sqrt
"import matlab.engine"
import matplotlib.pyplot as plt

def snr_dBFS(channel_fft_no_harmonics,channel_volts,channel_fft_dBFS_half_no_harmonics,
           frequencia_fft_half,FREQUENCY_INPUT,
           FUNDO_ESCALA_ADC,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,
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
        if (channel_fft_no_harmonics[0][i]>amplitude_fund_input_freq_ch_1):
            amplitude_fund_input_freq_ch_1 = channel_fft_no_harmonics[0][i]
            freq_amplitude_aux1=i
            
        if (channel_fft_no_harmonics[1][i]>amplitude_fund_input_freq_ch_2):
            amplitude_fund_input_freq_ch_2 = channel_fft_no_harmonics[1][i]
            freq_amplitude_aux2=i
            
        if (channel_fft_no_harmonics[2][i]>amplitude_fund_input_freq_ch_3):
            amplitude_fund_input_freq_ch_3 = channel_fft_no_harmonics[2][i]
            freq_amplitude_aux3=i
            
        if (channel_fft_no_harmonics[3][i]>amplitude_fund_input_freq_ch_4):
            amplitude_fund_input_freq_ch_4 = channel_fft_no_harmonics[3][i]
            freq_amplitude_aux4=i
    
    
    i=0
    aux1=0
    aux2=0
    aux3=0
    aux4=0
    
    for i in range (0,len(frequencia_fft_half)):

        if(i!=freq_amplitude_aux1 and (i>1.03*freq_amplitude_aux1 or i<0.97*freq_amplitude_aux1)):
            if(channel_fft_no_harmonics[0][i]!=float('-inf')):
                aux1=aux1+pow(channel_fft_no_harmonics[0][i],2)
        if(i!=freq_amplitude_aux2 and (i>1.03*freq_amplitude_aux2 or i<0.97*freq_amplitude_aux2)):
            if(channel_fft_no_harmonics[1][i]!=float('-inf')):
                aux2=aux2+pow(channel_fft_no_harmonics[1][i],2)
        if(i!=freq_amplitude_aux3 and (i>1.03*freq_amplitude_aux3 or i<0.97*freq_amplitude_aux3)):
            if(channel_fft_no_harmonics[2][i]!=float('-inf')):
                aux3=aux3+pow(channel_fft_no_harmonics[2][i],2)
        if(i!=freq_amplitude_aux4 and (i>1.03*freq_amplitude_aux4 or i<0.97*freq_amplitude_aux4)):
            if(channel_fft_no_harmonics[3][i]!=float('-inf')):
                aux4=aux4+pow(channel_fft_no_harmonics[3][i],2)


    
    #Cálculo do snr - método próprio
    snr_dB_ch1=10*log10(pow(amplitude_fund_input_freq_ch_1/sqrt(aux1),2))                
    snr_dB_ch2=10*log10(pow(amplitude_fund_input_freq_ch_2/sqrt(aux2),2))   
    snr_dB_ch3=10*log10(pow(amplitude_fund_input_freq_ch_3/sqrt(aux3),2))   
    snr_dB_ch4=10*log10(pow(amplitude_fund_input_freq_ch_4/sqrt(aux4),2))  
    
    snr_ch_dB=[snr_dB_ch1,snr_dB_ch2,snr_dB_ch3,snr_dB_ch4]
    
    #Cálculo do snr - método com Matlab
    if (utilizarMatlab_check==True):
        snr_dB_ch1_matlab=eng.snr(matlab.double(channel_volts[0]),float(FREQUENCY_INPUT),float(5))            
        snr_dB_ch2_matlab=eng.snr(matlab.double(channel_volts[1]),float(FREQUENCY_INPUT),float(5))
        snr_dB_ch3_matlab=eng.snr(matlab.double(channel_volts[2]),float(FREQUENCY_INPUT),float(5))
        snr_dB_ch4_matlab=eng.snr(matlab.double(channel_volts[3]),float(FREQUENCY_INPUT),float(5))
        snr_dB_matlab=[snr_dB_ch1_matlab,snr_dB_ch2_matlab,snr_dB_ch3_matlab,snr_dB_ch4_matlab]
 
    else:
        snr_dB_matlab='-inf'
 
        
    #Cálculo do snr - método com Python
   
    '''#Gráfico em volts sem as harmônicas
    eng.plot(matlab.double(frequencia_fft_half),matlab.double(channel_fft_dBFS_half_no_harmonics[switch_port-1]))
    eng.title('Gráfico utilizado no cálculo do SNR (sem harmônicas) - Porta do AD:'+str(switch_port)+' #:'+str(n_media+1))
    eng.xlabel('FREQUENCY [Hz]')
    eng.ylabel('AMPLITUDE [dBFS]')'''
    
    if (grafico_check==True):
        #Plota os gráficos via Python
        plt.plot(frequencia_fft_half,channel_fft_dBFS_half_no_harmonics[switch_port-1])
        plt.title('Gráfico utilizado no cálculo do SNR (sem harmônicas) - Porta do AD:'+str(switch_port)+' #:'+str(n_media+1))
        plt.xlabel('FREQUENCY [Hz]')
        plt.ylabel('AMPLITUDE [dBFS]')
        plt.grid()
        plt.show()
    
      
    
    
    return (snr_ch_dB,snr_dB_matlab)
    
    
    
    