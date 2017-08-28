from crate_to_volts_and_fft import crate_to_volts_and_fft

def get_data(eng,switch_port,
             IP_CRATE,USERNAME,PASSWORD,
             POSITION_CRATE,POSITION_ADC,NUM_PONTS_CRATE,
             FUNDO_ESCALA_ADC,MAX_CONTAGEM_ADC,
             NUM_PONTS_FFT,FREQUENCY_SAMPLE,FREQUENCY_INPUT,
             numero_media,frequencia_fft,
             channel_fft_media_dBFS,channel_volts_media):
    
    channel_volts_list=[]
    channel_fft_volts_list=[]
    crate_data_list=[]
    
    i=0
    while i<numero_media:
        print("Realizando a medição número ",i+1," de ",numero_media)
        #Obtém os valores em tensão diretamente do Crate, tanto no domínio do tempo (volts) quanto no domínio da frequência (fft)
        (channel_volts,channel_fft_volts,crate_data)=crate_to_volts_and_fft(eng,IP_CRATE,USERNAME,PASSWORD,
                                                                            POSITION_CRATE,POSITION_ADC,NUM_PONTS_CRATE,
                                                                            FUNDO_ESCALA_ADC,MAX_CONTAGEM_ADC,
                                                                            NUM_PONTS_FFT,FREQUENCY_SAMPLE,FREQUENCY_INPUT)
        
        
        channel_volts_list.append(channel_volts)
        channel_fft_volts_list.append(channel_fft_volts)
        crate_data_list.append(crate_data)
        
        
        i=i+1
    
    return(channel_volts_list,channel_fft_volts_list,crate_data_list) 