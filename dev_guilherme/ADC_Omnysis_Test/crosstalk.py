"import matlab.engine"
import time
import matplotlib.pyplot as plt

def crosstalk(channel_fft_dBFS_half_with_harmonics,frequencia_fft_half,
              NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,FREQUENCY_INPUT,
              eng,switch_port,n_media,grafico_check):
    
    if(grafico_check==True):
        plt.plot(frequencia_fft_half,channel_fft_dBFS_half_with_harmonics[0],
                 frequencia_fft_half,channel_fft_dBFS_half_with_harmonics[1],
                 frequencia_fft_half,channel_fft_dBFS_half_with_harmonics[2],
                 frequencia_fft_half,channel_fft_dBFS_half_with_harmonics[3])
        plt.title('Gráfico utilizado no cálculo do CROSSTALK - Porta do AD:'+str(switch_port)+' #:'+str(n_media+1))
        plt.xlabel('FREQUENCY [Hz]')
        plt.ylabel('AMPLITUDE [dBFS]')
        plt.grid()
        plt.show()
        #time.sleep(5)
    
    #Encontra o pico de amplitude do sinal
    aux=-1000
    for i in range (0,len(frequencia_fft_half)):
        if (aux<channel_fft_dBFS_half_with_harmonics[switch_port-1][i]):
            aux=channel_fft_dBFS_half_with_harmonics[switch_port-1][i]
            freq_fundamental=i
    amplitude_fund_input=aux

    
    #Analisa-se o crosstalk dos demais canais

    
    '''aux1=-1000
    aux2=-1000
    aux3=-1000

    i=0
    for i in range (0,len(frequencia_fft_half)):

        if (switch_port==1):
            canal1="2"
            canal2="3"
            canal3="4"
            if(aux1<channel_fft_dBFS_half_with_harmonics[1][i]):
                aux1=channel_fft_dBFS_half_with_harmonics[1][i]
            if(aux2<channel_fft_dBFS_half_with_harmonics[2][i]):
                aux2=channel_fft_dBFS_half_with_harmonics[2][i]
            if(aux3<channel_fft_dBFS_half_with_harmonics[3][i]):
                aux3=channel_fft_dBFS_half_with_harmonics[3][i]
     
        if (switch_port==2):
            canal1="1"
            canal2="3"
            canal3="4"
            if(aux1<channel_fft_dBFS_half_with_harmonics[0][i]):
                aux1=channel_fft_dBFS_half_with_harmonics[0][i]
            if(aux2<channel_fft_dBFS_half_with_harmonics[2][i]):
                aux2=channel_fft_dBFS_half_with_harmonics[2][i]
            if(aux3<channel_fft_dBFS_half_with_harmonics[3][i]):
                aux3=channel_fft_dBFS_half_with_harmonics[3][i]
       
        if (switch_port==3):
            canal1="1"
            canal2="2"
            canal3="4"
            if(aux1<channel_fft_dBFS_half_with_harmonics[0][i]):
                aux1=channel_fft_dBFS_half_with_harmonics[0][i]
            if(aux2<channel_fft_dBFS_half_with_harmonics[1][i]):
                aux2=channel_fft_dBFS_half_with_harmonics[1][i]
            if(aux3<channel_fft_dBFS_half_with_harmonics[3][i]):
                aux3=channel_fft_dBFS_half_with_harmonics[3][i]
       
        if (switch_port==4):
            canal1="1"
            canal2="2"
            canal3="3"
            if(aux1<channel_fft_dBFS_half_with_harmonics[0][i]):
                aux1=channel_fft_dBFS_half_with_harmonics[0][i]
            if(aux2<channel_fft_dBFS_half_with_harmonics[1][i]):
                aux2=channel_fft_dBFS_half_with_harmonics[1][i]
            if(aux3<channel_fft_dBFS_half_with_harmonics[2][i]):
                aux3=channel_fft_dBFS_half_with_harmonics[2][i] '''
     
    
    if (switch_port==1):
        canal1="2"
        canal2="3"
        canal3="4"
        aux1=channel_fft_dBFS_half_with_harmonics[1][freq_fundamental]
        aux2=channel_fft_dBFS_half_with_harmonics[2][freq_fundamental]
        aux3=channel_fft_dBFS_half_with_harmonics[3][freq_fundamental]
            
    if (switch_port==2):
        canal1="1"
        canal2="3"
        canal3="4"
        aux1=channel_fft_dBFS_half_with_harmonics[0][freq_fundamental]
        aux2=channel_fft_dBFS_half_with_harmonics[2][freq_fundamental]
        aux3=channel_fft_dBFS_half_with_harmonics[3][freq_fundamental]

    if (switch_port==3):
        canal1="1"
        canal2="2"
        canal3="4"
        aux1=channel_fft_dBFS_half_with_harmonics[0][freq_fundamental]
        aux2=channel_fft_dBFS_half_with_harmonics[1][freq_fundamental]
        aux3=channel_fft_dBFS_half_with_harmonics[3][freq_fundamental]
    
    if (switch_port==4):
        canal1="1"
        canal2="2"
        canal3="3"
        aux1=channel_fft_dBFS_half_with_harmonics[0][freq_fundamental]
        aux2=channel_fft_dBFS_half_with_harmonics[1][freq_fundamental]
        aux3=channel_fft_dBFS_half_with_harmonics[2][freq_fundamental]
    
    crosstalk_values=[amplitude_fund_input-aux1,amplitude_fund_input-aux2,amplitude_fund_input-aux3]
    crosstalk_canal=[canal1,canal2,canal3]
    crosstalk_dBFS=[crosstalk_values,crosstalk_canal]
        
    return (crosstalk_dBFS)
