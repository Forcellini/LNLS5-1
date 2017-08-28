def zeros_fft_volts(NUM_PONTS_FFT,NUM_PONTS_CRATE):
    
    
    #Cria vetores de fft para cálculo da média
    channel_1_fft_media_dBFS=[]
    channel_2_fft_media_dBFS=[]
    channel_3_fft_media_dBFS=[]
    channel_4_fft_media_dBFS=[]
    
    i=0
    for i in range (0,NUM_PONTS_FFT):
        channel_1_fft_media_dBFS.append(0)
        channel_2_fft_media_dBFS.append(0)
        channel_3_fft_media_dBFS.append(0)
        channel_4_fft_media_dBFS.append(0)

    #cria vetores de volts para cálculo da média
    channel_1_volts_media=[]
    channel_2_volts_media=[]
    channel_3_volts_media=[]
    channel_4_volts_media=[]

    i=0
    for i in range (0,NUM_PONTS_CRATE):
        channel_1_volts_media.append(0)
        channel_2_volts_media.append(0)
        channel_3_volts_media.append(0)
        channel_4_volts_media.append(0)
        
    channel_fft_media_dBFS=[channel_1_fft_media_dBFS,channel_2_fft_media_dBFS,channel_3_fft_media_dBFS,channel_4_fft_media_dBFS]
    channel_volts_media=[channel_1_volts_media,channel_2_volts_media,channel_3_volts_media,channel_4_volts_media]
   
    return (channel_fft_media_dBFS,channel_volts_media)