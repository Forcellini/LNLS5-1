from crate_data_acquisition import crate_data_acquisition
from transf_fft import transf_fft
#import matlab.engine


def crate_to_volts_and_fft(eng,IP_CRATE,USERNAME,PASSWORD,
                           POSITION_CRATE,POSITION_ADC,NUM_PONTS_CRATE,
                           FUNDO_ESCALA_ADC,MAX_CONTAGEM_ADC,
                           NUM_PONTS_FFT,FREQUENCY_SAMPLE,FREQUENCY_INPUT):

        
    #Realiza a aquisição dos dados de AD do Crate e converte em Volts
    (crate_data,volts_data)=crate_data_acquisition(IP_CRATE,POSITION_CRATE,POSITION_ADC,NUM_PONTS_CRATE,MAX_CONTAGEM_ADC)
    #Calcula a Transformada Rápida de Fourier do sinal (FFT)
    (fft_vt_data)=transf_fft(volts_data,NUM_PONTS_FFT,NUM_PONTS_CRATE,FREQUENCY_SAMPLE,eng)

    return (volts_data,fft_vt_data,crate_data)