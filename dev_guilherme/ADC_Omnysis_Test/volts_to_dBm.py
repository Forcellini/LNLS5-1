#não usa, pode deletar

from math import log10, sqrt
from transf_fft import transf_fft
#import matlab.engine

def volts_to_dBm(channel_volts_media,NUM_PONTS_FFT,
                 NUM_PONTS_CRATE,FREQUENCY_SAMPLE,eng):
  
    #Obtém a fft dos valores médios de tensão
    (channel_1_fft_vt,channel_2_fft_vt,channel_3_fft_vt,channel_4_fft_vt)=transf_fft(channel_volts_media[0],channel_volts_media[1],channel_volts_media[2],channel_volts_media[3],
                                                                                     NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,eng)
    
    channel_fft_vt_media=[channel_1_fft_vt,channel_2_fft_vt,channel_3_fft_vt,channel_4_fft_vt]
  
    #Converte em dBm
    channel_1_fft_dBm=[]
    channel_1_fft_dBm_2=[]
    
    channel_2_fft_dBm=[]
    channel_3_fft_dBm=[]
    channel_4_fft_dBm=[]

    i=0
    for i in range (0,NUM_PONTS_FFT):
        #Canal 1
        aux=channel_fft_vt_media[0][i]
        if (aux==0):
            aux=float('-inf')
            channel_1_fft_dBm.append(aux)
        else:
            #channel_1_fft_dBm.append(10*log10((((((pow((((abs(channel_fft_vt_media[0][i]))/sqrt(2))),2)))/50))/0.001)))
            channel_1_fft_dBm.append(20*log10(abs(2*channel_fft_vt_media[0][i]/NUM_PONTS_FFT)))


            #channel_1_fft_dBm_2.append(10*log10(abs(channel_fft_vt_media[0][i]/NUM_PONTS_FFT)*abs(channel_fft_vt_media[0][i]/NUM_PONTS_FFT)/50*0.001))

        
        #Canal 2    
        aux=channel_fft_vt_media[1][i]
        if (aux==0):
            aux=float('-inf')
            channel_2_fft_dBm.append(aux)
        else:
            #channel_2_fft_dBm.append(10*log10((((((pow((((abs(channel_fft_vt_media[1][i]))/sqrt(2))),2)))/50))/0.001)))
            channel_2_fft_dBm.append(20*log10(abs(2*channel_fft_vt_media[1][i]/NUM_PONTS_FFT)))
        
        #Canal 3
        aux=channel_fft_vt_media[2][i]
        if (aux==0):
            aux=float('-inf')
            channel_3_fft_dBm.append(aux)
        else:
            #channel_3_fft_dBm.append(10*log10((((((pow((((abs(channel_fft_vt_media[2][i]))/sqrt(2))),2)))/50))/0.001)))
            channel_3_fft_dBm.append(20*log10(abs(2*channel_fft_vt_media[2][i]/NUM_PONTS_FFT)))
            
        #Canal 4
        aux=channel_fft_vt_media[3][i]
        if (aux==0):
            aux=float('-inf')
            channel_4_fft_dBm.append(aux)
        else:
            #channel_4_fft_dBm.append(10*log10((((((pow((((abs(channel_fft_vt_media[3][i]))/sqrt(2))),2)))/50))/0.001)))
            channel_4_fft_dBm.append(20*log10(abs(2*channel_fft_vt_media[3][i]/NUM_PONTS_FFT)))
    #eng.plot(matlab.double(channel_1_fft_dBm))
    #input("Chegou 1")
    #eng.plot(matlab.double(channel_1_fft_dBm_2))
    #input("Chegou 2")
    channel_fft_dBm=[channel_1_fft_dBm,channel_2_fft_dBm,channel_3_fft_dBm,channel_4_fft_dBm]
    
    return(channel_fft_dBm)