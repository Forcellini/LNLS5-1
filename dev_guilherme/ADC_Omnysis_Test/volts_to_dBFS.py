from math import log10, sqrt

def volts_to_dBFS(channel_fft_volts,
                  NUM_PONTS_FFT,FUNDO_ESCALA_ADC,eng):
  
    #Converte em dBFS
    channel_1_fft_dBFS=[]
    channel_2_fft_dBFS=[]
    channel_3_fft_dBFS=[]
    channel_4_fft_dBFS=[]
    
    #Os valores de fft_media e FUNDO_ESCALA_ADC precisam estar na mesma unidade
    #no caso deste programa, ambos estão em valores de Vpp, por tanto não precisamos converter 
    #nenhum dos dois para RMS, pois já estão em unidades equivalentes
    i=0
    for i in range (0,NUM_PONTS_FFT):
        if(abs(channel_fft_volts[0][i])==0):
            channel_1_fft_dBFS.append(float('-inf'))
        else:
            aux = 2*abs(channel_fft_volts[0][i])/(NUM_PONTS_FFT)
            #channel_1_fft_dBFS.append(20*log10(aux)/FUNDO_ESCALA_ADC)
            channel_1_fft_dBFS.append(20*log10(aux))
        
        if(abs(channel_fft_volts[1][i])==0):
            channel_2_fft_dBFS.append(float('-inf'))
        else:
            aux = 2*abs(channel_fft_volts[1][i])/(NUM_PONTS_FFT)
            channel_2_fft_dBFS.append(20*log10(aux))
        
        if(abs(channel_fft_volts[2][i])==0):
            channel_3_fft_dBFS.append(float('-inf'))
        else:
            aux = 2*abs(channel_fft_volts[2][i])/(NUM_PONTS_FFT)
            channel_3_fft_dBFS.append(20*log10(aux))
            
        if(abs(channel_fft_volts[3][i])==0):
            channel_4_fft_dBFS.append(float('-inf'))
        else:
            aux = 2*abs(channel_fft_volts[3][i])/(NUM_PONTS_FFT)
            channel_4_fft_dBFS.append(20*log10(aux))
            

    #print("Valores em dBFS: OK")
    
    channel_fft_dBFS=[channel_1_fft_dBFS,channel_2_fft_dBFS,channel_3_fft_dBFS,channel_4_fft_dBFS]
    
    return(channel_fft_dBFS)