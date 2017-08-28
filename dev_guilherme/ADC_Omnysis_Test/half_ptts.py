def half_ptts (channel_fft,channel_fft_volts,frequencia_fft_half,FREQUENCY_INPUT,NUM_PONTS_FFT,canal):
    
        
    channel_1_fft_half_with_harmonics=[]
    channel_2_fft_half_with_harmonics=[]
    channel_3_fft_half_with_harmonics=[]
    channel_4_fft_half_with_harmonics=[]
    
    channel_1_fft_half_with_harmonics_volts=[]
    channel_2_fft_half_with_harmonics_volts=[]
    channel_3_fft_half_with_harmonics_volts=[]
    channel_4_fft_half_with_harmonics_volts=[]
     
    #Half WITH HAMORNICS
    i=0
    for i in range (0,len(frequencia_fft_half)):
        if (frequencia_fft_half[i]==0 or frequencia_fft_half[i]<20):
            channel_1_fft_half_with_harmonics.append(float('-inf'))
            channel_2_fft_half_with_harmonics.append(float('-inf'))
            channel_3_fft_half_with_harmonics.append(float('-inf'))
            channel_4_fft_half_with_harmonics.append(float('-inf'))
            
            channel_1_fft_half_with_harmonics_volts.append(float('-inf'))
            channel_2_fft_half_with_harmonics_volts.append(float('-inf'))
            channel_3_fft_half_with_harmonics_volts.append(float('-inf'))
            channel_4_fft_half_with_harmonics_volts.append(float('-inf'))
                        
        else:
            channel_1_fft_half_with_harmonics.append(channel_fft[0][i])
            channel_2_fft_half_with_harmonics.append(channel_fft[1][i])
            channel_3_fft_half_with_harmonics.append(channel_fft[2][i])
            channel_4_fft_half_with_harmonics.append(channel_fft[3][i])
            
            channel_1_fft_half_with_harmonics_volts.append(2*abs(channel_fft_volts[0][i])/(NUM_PONTS_FFT))
            channel_2_fft_half_with_harmonics_volts.append(2*abs(channel_fft_volts[1][i])/(NUM_PONTS_FFT))
            channel_3_fft_half_with_harmonics_volts.append(2*abs(channel_fft_volts[2][i])/(NUM_PONTS_FFT))
            channel_4_fft_half_with_harmonics_volts.append(2*abs(channel_fft_volts[3][i])/(NUM_PONTS_FFT))

   
    channel_fft_half_with_harmonics_list=[channel_1_fft_half_with_harmonics,channel_2_fft_half_with_harmonics,channel_3_fft_half_with_harmonics,channel_4_fft_half_with_harmonics]
    channel_fft_half_with_harmonics_volts_list=[channel_1_fft_half_with_harmonics_volts,channel_2_fft_half_with_harmonics_volts,channel_3_fft_half_with_harmonics_volts,channel_4_fft_half_with_harmonics_volts]
    
   
    #Encontra a frequencia fundamental em fft
    i=0
    amplitude_fund_input_freq_fund=-1000
    freq_amplitude_fund=0
    
    for i in range (0, len(frequencia_fft_half)):
        if (canal==1):
            if (channel_fft_half_with_harmonics_list[0][i]>amplitude_fund_input_freq_fund):
                amplitude_fund_input_freq_fund = channel_fft_half_with_harmonics_list[0][i]
                freq_amplitude_fund=i
        if (canal==2):
            if (channel_fft_half_with_harmonics_list[1][i]>amplitude_fund_input_freq_fund):
                amplitude_fund_input_freq_fund = channel_fft_half_with_harmonics_list[1][i]
                freq_amplitude_fund=i   
        if (canal==3):
            if (channel_fft_half_with_harmonics_list[2][i]>amplitude_fund_input_freq_fund):
                amplitude_fund_input_freq_fund = channel_fft_half_with_harmonics_list[2][i]
                freq_amplitude_fund=i
        if (canal==4):
            if (channel_fft_half_with_harmonics_list[3][i]>amplitude_fund_input_freq_fund):
                amplitude_fund_input_freq_fund = channel_fft_half_with_harmonics_list[3][i]
                freq_amplitude_fund=i   
    
    FREQUENCY_INPUT=freq_amplitude_fund
              
    
    #HALF WITHOUT HAMORNICS AND NO DC LEVEL
    
    channel_1_fft_half_no_harmonics=[]
    channel_2_fft_half_no_harmonics=[]
    channel_3_fft_half_no_harmonics=[]
    channel_4_fft_half_no_harmonics=[]
    
    channel_1_fft_half_no_harmonics_volts=[]
    channel_2_fft_half_no_harmonics_volts=[]
    channel_3_fft_half_no_harmonics_volts=[]
    channel_4_fft_half_no_harmonics_volts=[]
    
    
    i=0
    for i in range (0,len(frequencia_fft_half)):
        channel_1_fft_half_no_harmonics.append(channel_fft_half_with_harmonics_list[0][i])
        channel_2_fft_half_no_harmonics.append(channel_fft_half_with_harmonics_list[1][i])
        channel_3_fft_half_no_harmonics.append(channel_fft_half_with_harmonics_list[2][i])
        channel_4_fft_half_no_harmonics.append(channel_fft_half_with_harmonics_list[3][i])
        
        channel_1_fft_half_no_harmonics_volts.append(channel_fft_half_with_harmonics_volts_list[0][i])
        channel_2_fft_half_no_harmonics_volts.append(channel_fft_half_with_harmonics_volts_list[1][i])
        channel_3_fft_half_no_harmonics_volts.append(channel_fft_half_with_harmonics_volts_list[2][i])
        channel_4_fft_half_no_harmonics_volts.append(channel_fft_half_with_harmonics_volts_list[3][i])
        
        #Segunda Harmônica
        if (i==2*FREQUENCY_INPUT or (i<(2.001*FREQUENCY_INPUT) and i>(1.998*FREQUENCY_INPUT))):
            channel_1_fft_half_no_harmonics[i]=float('-inf')
            channel_2_fft_half_no_harmonics[i]=float('-inf')
            channel_3_fft_half_no_harmonics[i]=float('-inf')
            channel_4_fft_half_no_harmonics[i]=float('-inf')
            
            channel_1_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_2_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_3_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_4_fft_half_no_harmonics_volts[i]=float('-inf')
            
        #Terceira Harmônica
        elif (i==3*FREQUENCY_INPUT or (i<(3.001*FREQUENCY_INPUT) and i>(2.998*FREQUENCY_INPUT))):
            channel_1_fft_half_no_harmonics[i]=float('-inf')
            channel_2_fft_half_no_harmonics[i]=float('-inf')
            channel_3_fft_half_no_harmonics[i]=float('-inf')
            channel_4_fft_half_no_harmonics[i]=float('-inf')
            
            channel_1_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_2_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_3_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_4_fft_half_no_harmonics_volts[i]=float('-inf')
        #Quarta Harmônica
        elif (i==4*FREQUENCY_INPUT or (i<(4.001*FREQUENCY_INPUT) and i>(3.998*FREQUENCY_INPUT))):
            channel_1_fft_half_no_harmonics[i]=float('-inf')
            channel_2_fft_half_no_harmonics[i]=float('-inf')
            channel_3_fft_half_no_harmonics[i]=float('-inf')
            channel_4_fft_half_no_harmonics[i]=float('-inf')

            channel_1_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_2_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_3_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_4_fft_half_no_harmonics_volts[i]=float('-inf')
        #Quinta Harmônica
        elif (i==5*FREQUENCY_INPUT or (i<(5.001*FREQUENCY_INPUT) and i>(4.998*FREQUENCY_INPUT))):
            channel_1_fft_half_no_harmonics[i]=float('-inf')
            channel_2_fft_half_no_harmonics[i]=float('-inf')
            channel_3_fft_half_no_harmonics[i]=float('-inf')
            channel_4_fft_half_no_harmonics[i]=float('-inf')
            
            channel_1_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_2_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_3_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_4_fft_half_no_harmonics_volts[i]=float('-inf')
        #Elimina o Zero (Nível DC)
        elif (i==0 or i<10):
            channel_1_fft_half_no_harmonics[i]=float('-inf')
            channel_2_fft_half_no_harmonics[i]=float('-inf')
            channel_3_fft_half_no_harmonics[i]=float('-inf')
            channel_4_fft_half_no_harmonics[i]=float('-inf')
            
            channel_1_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_2_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_3_fft_half_no_harmonics_volts[i]=float('-inf')
            channel_4_fft_half_no_harmonics_volts[i]=float('-inf')
            
    channel_fft_half_no_harmonics_list=[channel_1_fft_half_no_harmonics,channel_2_fft_half_no_harmonics,channel_3_fft_half_no_harmonics,channel_4_fft_half_no_harmonics]
    channel_fft_half_no_harmonics_volts_list=[channel_1_fft_half_no_harmonics_volts,channel_2_fft_half_no_harmonics_volts,channel_3_fft_half_no_harmonics_volts,channel_4_fft_half_no_harmonics_volts]

    return (channel_fft_half_with_harmonics_list,channel_fft_half_no_harmonics_list,channel_fft_half_with_harmonics_volts_list,channel_fft_half_no_harmonics_volts_list)


    