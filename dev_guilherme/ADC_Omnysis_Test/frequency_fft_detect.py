def frequency_fft_detect(NUM_PONTS_FFT,FREQUENCY_SAMPLE):
    
    frequencia_fft=[]
    i=0
    for i in range (0,NUM_PONTS_FFT):
        #frequencia_fft.append(i*18.5*FREQUENCY_SAMPLE/NUM_PONTS_FFT)
        frequencia_fft.append(i*FREQUENCY_SAMPLE/NUM_PONTS_FFT) #Conforme LNLS pediu
        
    return(frequencia_fft)