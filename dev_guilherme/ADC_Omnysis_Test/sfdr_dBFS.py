"import matlab.engine"
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def sfdr_dBFS(channel_fft_media_dBFS,channel_volts_list,switch_port,
              frequencia_fft_with_harmonics,frequencia_fft,
              FREQUENCY_INPUT,NUM_PONTS_FFT,eng,numero_media,utilizarMatlab_check,tela_leds):
    
    amplitude_fund_input_freq_ch_1=-1000
    amplitude_fund_input_freq_ch_2=-1000
    amplitude_fund_input_freq_ch_3=-1000
    amplitude_fund_input_freq_ch_4=-1000
    
    freq_amplitude_aux1=0
    freq_amplitude_aux2=0
    freq_amplitude_aux3=0
    freq_amplitude_aux4=0
    
    i=0
    for i in range (0, len(frequencia_fft_with_harmonics)):
        
        if (channel_fft_media_dBFS[0][i]>amplitude_fund_input_freq_ch_1):
            amplitude_fund_input_freq_ch_1 = channel_fft_media_dBFS[0][i]
            freq_amplitude_aux1=i
            
        if (channel_fft_media_dBFS[1][i]>amplitude_fund_input_freq_ch_2):
            amplitude_fund_input_freq_ch_2 = channel_fft_media_dBFS[1][i]
            freq_amplitude_aux2=i
            
        if (channel_fft_media_dBFS[2][i]>amplitude_fund_input_freq_ch_3):
            amplitude_fund_input_freq_ch_3 = channel_fft_media_dBFS[2][i]
            freq_amplitude_aux3=i
            
        if (channel_fft_media_dBFS[3][i]>amplitude_fund_input_freq_ch_4):
            amplitude_fund_input_freq_ch_4 = channel_fft_media_dBFS[3][i]
            freq_amplitude_aux4=i

    amplitude_spurious_ch_1=-1000
    amplitude_spurious_ch_2=-1000
    amplitude_spurious_ch_3=-1000
    amplitude_spurious_ch_4=-1000
    
    tela_leds.ui.progressBar.setValue(i*40/len(frequencia_fft_with_harmonics)+10)
    tela_leds.repaint()
    QApplication.processEvents()
   
    i=0
    for i in range (0,len(frequencia_fft_with_harmonics)):
        if (channel_fft_media_dBFS[0][i]>amplitude_spurious_ch_1):
            if (i!=freq_amplitude_aux1 and (i>1.03*freq_amplitude_aux1 or i<0.97*freq_amplitude_aux1)):
                amplitude_spurious_ch_1=channel_fft_media_dBFS[0][i]
                freq_spurious_aux1=i

        if (channel_fft_media_dBFS[1][i]>amplitude_spurious_ch_2):
            if (i!=freq_amplitude_aux2 and (i>1.03*freq_amplitude_aux2 or i<0.97*freq_amplitude_aux2)):
                amplitude_spurious_ch_2=channel_fft_media_dBFS[1][i]
                freq_spurious_aux2=i
                
        if (channel_fft_media_dBFS[2][i]>amplitude_spurious_ch_3):
            if (i!=freq_amplitude_aux3 and (i>1.03*freq_amplitude_aux3 or i<0.97*freq_amplitude_aux3)):
                amplitude_spurious_ch_3=channel_fft_media_dBFS[2][i]
                freq_spurious_aux3=i

        if (channel_fft_media_dBFS[3][i]>amplitude_spurious_ch_4):
            if (i!=freq_amplitude_aux4 and (i>1.03*freq_amplitude_aux4 or i<0.97*freq_amplitude_aux4)):
                amplitude_spurious_ch_4=channel_fft_media_dBFS[3][i]
                freq_spurious_aux4=i
    
    
    #Cálculo do SFDR - Método Próprio        
    sfdr_dBFS_ch1=amplitude_fund_input_freq_ch_1-amplitude_spurious_ch_1
    sfdr_dBFS_ch2=amplitude_fund_input_freq_ch_2-amplitude_spurious_ch_2
    sfdr_dBFS_ch3=amplitude_fund_input_freq_ch_3-amplitude_spurious_ch_3
    sfdr_dBFS_ch4=amplitude_fund_input_freq_ch_4-amplitude_spurious_ch_4

    tela_leds.ui.progressBar.setValue(60)
    tela_leds.repaint()
    QApplication.processEvents()
    #Cálculo do SFDR - Matlab
    if(utilizarMatlab_check==True):
        aux1=0
        aux2=0
        aux3=0
        aux4=0
    
        i=0
        while (i< numero_media):
            aux1=aux1+eng.sfdr(matlab.double(channel_volts_list[0][i][0]),float(FREQUENCY_INPUT),float(1000000))
            aux2=aux2+eng.sfdr(matlab.double(channel_volts_list[1][i][1]),float(FREQUENCY_INPUT),float(1000000))
            aux3=aux3+eng.sfdr(matlab.double(channel_volts_list[2][i][2]),float(FREQUENCY_INPUT),float(1000000))
            aux4=aux4+eng.sfdr(matlab.double(channel_volts_list[3][i][3]),float(FREQUENCY_INPUT),float(1000000))
            i=i+1
 
        sfdr_dBFS_ch1_matlab=aux1/numero_media
        sfdr_dBFS_ch2_matlab=aux2/numero_media
        sfdr_dBFS_ch3_matlab=aux3/numero_media
        sfdr_dBFS_ch4_matlab=aux4/numero_media
        sfdr_dBFS_matlab=[sfdr_dBFS_ch1_matlab,sfdr_dBFS_ch2_matlab,sfdr_dBFS_ch3_matlab,sfdr_dBFS_ch4_matlab]
        
    else:
            sfdr_dBFS_matlab=['-inf']

        
    sfdr_dBFS_ch=[sfdr_dBFS_ch1,sfdr_dBFS_ch2,sfdr_dBFS_ch3,sfdr_dBFS_ch4]

    tela_leds.ui.progressBar.setValue(80)
    tela_leds.repaint()
    QApplication.processEvents()
    
    return (sfdr_dBFS_ch,sfdr_dBFS_matlab)
    
    