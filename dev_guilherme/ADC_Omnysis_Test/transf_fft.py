#import matlab.engine
from scipy.fftpack import fft

def transf_fft(volts_data,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,eng):
    
    #list_to_file(0,channel_1_crate_to_volts,'/home/tadeu/Desktop/output.csv')
   
    #Reliza o FFT (Transformada de Fourier Rápida) do sinal do ADC (via Matlab)
    '''channel_1_fft=eng.fft(matlab.double(volts_data[0]),float(NUM_PONTS_FFT))
    channel_2_fft=eng.fft(matlab.double(volts_data[1]),float(NUM_PONTS_FFT))
    channel_3_fft=eng.fft(matlab.double(volts_data[2]),float(NUM_PONTS_FFT))
    channel_4_fft=eng.fft(matlab.double(volts_data[3]),float(NUM_PONTS_FFT))'''
   
    channel_1_fft=fft((volts_data[0]),float(NUM_PONTS_FFT))
    channel_2_fft=fft((volts_data[1]),float(NUM_PONTS_FFT))
    channel_3_fft=fft((volts_data[2]),float(NUM_PONTS_FFT))
    channel_4_fft=fft((volts_data[3]),float(NUM_PONTS_FFT))

    channel_1_fft_vt=[]
    channel_2_fft_vt=[]
    channel_3_fft_vt=[]
    channel_4_fft_vt=[]

    i = 0
    for i in range (0, NUM_PONTS_FFT):
        
        aux=channel_1_fft[i]
        channel_1_fft_vt.append(aux)
        aux=channel_2_fft[i]
        channel_2_fft_vt.append(aux)
        aux=channel_3_fft[i]
        channel_3_fft_vt.append(aux)
        aux=channel_4_fft[i]
        channel_4_fft_vt.append(aux)
        
    fft_vt_data=[channel_1_fft_vt,channel_2_fft_vt,channel_3_fft_vt,channel_4_fft_vt]

    return(fft_vt_data)