'''#import paramiko
import matlab.engine
from start_communication import start_communication
from sfdr_dBFS import sfdr_dBFS
from enob import enob
from zeros_fft_volts import zeros_fft_volts
from zeros_snr_sinad import zeros_snr_sinad
from medias_fft_volts import medias_fft_volts
from medias_snr_sinad import medias_snr_sinad
from frequency_fft_detect import frequency_fft_detect
from get_data_plus_snr_sinad import get_data_plus_snr_sinad
from switch_connection import switch_connection
from result_parameters import result_parameters
from list_rw_file2 import list_to_file
from crosstalk import crosstalk
from missing_codes import missing_codes

#CONSTANTS
FUNDO_ESCALA_ADC = 2.25 #volts
AMPLITUDE_SINAL_ENTRADA=0.670 #Vpp
MAX_CONTAGEM_ADC = 32768 #2^15 --> ADC de 16 bits
NUM_PONTS_CRATE = 10 #100000
NUM_PONTS_FFT = 10 #99995
IP_SWITCH='10.0.18.20'
IP_CRATE='10.0.18.18'
USERNAME = 'root'
PASSWORD = 'root'
POSITION_CRATE=4 #Posição do slot do crate
POSITION_ADC=1 #(1 ou 0) - 1 para em baixo,0 para em cima
FREQUENCY_SAMPLE= 118230000 #fs -> frequeência de amostragem = frequência do clock 118230000 (5dBm)
FREQUENCY_INPUT = 499944000 #fin -> frequência do sinal de entrada 499944000 (9.5dBm com filtro passa baixa com perda de 3dBm)
numero_media=5
snr_dB_criterio=65 #>= 65dB
sfdr_dBFS_criterio=60 #>=60dBFS
enob_criterio=10 #>= 10 bits
crosstalk_criterio=100 #>=100dB
datapath_save="result/"
serial_number="111111111"


print("Iniciou Teste do AD")

#Configura a comunicação com o Crate e o MATLAB
(eng,ssh)=start_communication(IP_CRATE,USERNAME,PASSWORD,POSITION_CRATE,IP_SWITCH)

#Variáveis para armazenar os resultados
snr_result_values=[]
sfdr_result_values=[]
enob_result_values=[]

snr_result_values_matlab=[]
sfdr_result_values_matlab=[]
enob_result_values_matlab=[]

crosstalk_values=[]
missing_codes_total=[]


#[0,1,2,3]= [Porta 1, Porta 2, Porta 3 e Porta 4]
i=0
while (i<4):
    
    #Aciona a porta PORT do SWITCH
    switch_port=i+1
    switch_connection(IP_SWITCH,switch_port)
    print("Realizando medição AD do Canal", i+1)
    
    ##Calcula as frequências para plotar no gráfico
    frequencia_fft=frequency_fft_detect(NUM_PONTS_FFT, FREQUENCY_SAMPLE)

    #Cria zeros para fft e volts - Servem para o cálculo das médias
    (channel_fft_media_dBFS,channel_volts_media,channel_fft_media_dBm)=zeros_fft_volts(NUM_PONTS_FFT, NUM_PONTS_CRATE)
    
    #Cria zeros para snr e sinad - Servem para o cálculo das médias
    (snr_dB_media,snr_dB_media_matlab,sinad_media,sinad_media_matlab)=zeros_snr_sinad()

    #Realiza a aquisição de dados para os cálculos de SNR, SINAD, SFDR e ENOB
    (channel_fft_media_dBFS,channel_volts_media,channel_fft_media_dBm,
     snr_dB_media,snr_dB_media_matlab,
     sinad_media,sinad_media_matlab,
     frequencia_fft_with_harmonics,missing_codes_crate)= get_data_plus_snr_sinad(eng, ssh,switch_port,
                                                                                 IP_CRATE, USERNAME, PASSWORD,
                                                                                 POSITION_CRATE, POSITION_ADC, NUM_PONTS_CRATE,
                                                                                 FUNDO_ESCALA_ADC, MAX_CONTAGEM_ADC,
                                                                                 NUM_PONTS_FFT, FREQUENCY_SAMPLE, FREQUENCY_INPUT,
                                                                                 numero_media, frequencia_fft,
                                                                                 channel_fft_media_dBFS,channel_volts_media,channel_fft_media_dBm,
                                                                                 snr_dB_media,snr_dB_media_matlab,
                                                                                 sinad_media,sinad_media_matlab)
     
    #Cálcula as médias para fft e volts
    (channel_fft_media_dBFS,channel_volts_media,channel_fft_media_dBm)=medias_fft_volts(channel_fft_media_dBFS,channel_volts_media,channel_fft_media_dBm,
                                                                                        NUM_PONTS_FFT, NUM_PONTS_CRATE, numero_media)

    #Cálcula as médias do SNR e do SINAD
    (snr_dB_media,snr_dB_media_matlab,sinad_media,sinad_media_matlab)=medias_snr_sinad(snr_dB_media,snr_dB_media_matlab,
                                                                                       sinad_media,sinad_media_matlab,
                                                                                       numero_media)  
    #Cálculo do SFDR (Spurious Free Dynamic Range): Desconsidera as harmônicas da placa, conforme sugestão do LNLS
    (sfdr_dBFS_ch,sfdr_dBFS_matlab)=sfdr_dBFS(channel_fft_media_dBFS,channel_volts_media,switch_port,
                                              frequencia_fft_with_harmonics,frequencia_fft,
                                              FREQUENCY_INPUT,NUM_PONTS_FFT,eng)

    #Cálcula o snr_dB_media_matlabulo do ENOB (Effective number of bits)
    (enob_ch,enob_ch_matlab)=enob(sinad_media,sinad_media_matlab)
    

    #Cálcula o crosstalk em dB
    (crosstalk_db)=crosstalk(channel_fft_media_dBm,frequencia_fft_with_harmonics,frequencia_fft,
                             NUM_PONTS_FFT,switch_port,
                             NUM_PONTS_CRATE,FREQUENCY_SAMPLE,FREQUENCY_INPUT,eng)
    
    #Armazena os valores de tensão para calcular o Missing Codes dos 4 canais - cada canal tem NUM_PONTS_CRATE*numero_media pontos
    missing_codes_total.append(missing_codes_crate)

    print("SNR MÉDIO- Método próprio: ",snr_dB_media[switch_port-1],"SNR MÉDIO- Método MATLAB: ",snr_dB_media_matlab[switch_port-1])
    print("SINAD MÉDIO- Método próprio: ",sinad_media[switch_port-1],"SINAD MÉDIO- Método MATLAB: ",sinad_media_matlab[switch_port-1])
    print("SFDR - Método Próprio: ",sfdr_dBFS_ch[switch_port-1],"SFDR - Método MATLAB: ",sfdr_dBFS_matlab[switch_port-1])
    print("ENOB - Método próprio: ",enob_ch[switch_port-1],"ENOB - Método MATLAB: ",enob_ch_matlab[switch_port-1])
    print("CROSSTALK - Método próprio: ",crosstalk_db[0],"Pior valor ocorreu em: ",crosstalk_db[1])
    
    #Armazena Resultados (Valores)
    snr_result_values.append(snr_dB_media[switch_port-1])
    snr_result_values_matlab.append(snr_dB_media_matlab[switch_port-1])
    sfdr_result_values.append(sfdr_dBFS_ch[switch_port-1])
    sfdr_result_values_matlab.append(sfdr_dBFS_matlab[switch_port-1])
    enob_result_values.append(enob_ch[switch_port-1])
    enob_result_values_matlab.append(enob_ch_matlab[switch_port-1])
    crosstalk_values.append(crosstalk_db)
    
    i=i+1

##Calcula o Missing Codes
(missing_code_values)=missing_codes(missing_codes_total,NUM_PONTS_CRATE,AMPLITUDE_SINAL_ENTRADA,
                                    numero_media,MAX_CONTAGEM_ADC,eng)

#Analisa os resultados obtidos
(snr_result_final,sfdr_result_final,enob_result_final,crosstalk_result_final,missing_code_result_final,
snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao, crosstalk_result_aprovacao,missing_code_result_aprovacao,
snr_result_value_final,sfdr_result_value_final,enob_result_value_final,crosstalk_result_value_final,missing_code_result_value_final,
result)=result_parameters(snr_result_values, snr_result_values_matlab, snr_dB_criterio,
                          sfdr_result_values, sfdr_result_values_matlab, sfdr_dBFS_criterio,
                          enob_result_values, enob_result_values_matlab, enob_criterio,
                          crosstalk_values,crosstalk_criterio,
                          missing_code_values)

print(snr_result_final)
print(sfdr_result_final)
print(enob_result_final)
print(crosstalk_result_final)
print(missing_code_result_final)

#Salva os resultados finais
list_to_file(0,result, datapath_save + serial_number + "_result_values.txt")


ssh.close()
print("Conexão Encerrada")


'''