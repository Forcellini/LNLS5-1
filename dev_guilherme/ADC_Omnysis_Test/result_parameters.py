from list_rw_file2 import list_to_file_aux

def result_parameters(snr_result_values,snr_result_values_matlab,snr_dB_criterio,
                      sfdr_result_values,sfdr_result_values_matlab,sfdr_dBFS_criterio,
                      enob_result_values,enob_result_values_matlab,enob_criterio,
                      crosstalk_result_values,crosstalk_canal_analisado,crosstalk_criterio,
                      missingcodes_result_value_final,missingcodes_detected_positions,missingcodes_result_final,missingcodes_result_aprovacao,sinal_entrada_crate,
                      dif_amp_result_values,dif_amp_criterio,AMPLITUDE_SINAL_ENTRADA_DIF_AMP,
                      utilizarMatlab_check,
                      eeprom_result,eeprom_write_check_result,eeprom_read_check_result,
                      ics854s01i_result,ics854s01i_write_check_result,ics854s01i_read_check_result,
                      si571_result,si571_write_check_result,si571_read_check_result,
                      ad9510_result,ad9510_write_check_result,ad9510_read_check_result,
                      start_time_general_str,stop_time_general_str,duracao_teste_general_str,serial_number,
                      fpga_str_result,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result,
                      FREQUENCY_INPUT,FREQUENCY_SAMPLE,FREQUENCY_INPUT_MISSINGCODES,FREQUENCY_SAMPLE_MISSINGCODES,
                      AMPLITUDE_SINAL_ENTRADA,AMPLITUDE_SINAL_CLOCK,AMPLITUDE_SINAL_ENTRADA_MISSINGCODES,AMPLITUDE_SINAL_CLOCK_MISSINGCODES,
                      NUM_PONTS_CRATE,NUM_PONTS_CRATE_MISSINGCODES,NUM_PONTS_FFT,
                      operador,n_serie_adc):
    
    snr_result_final=[]
    sfdr_result_final=[]
    enob_result_final=[]
    crosstalk_result_final=[]

    
    snr_result_aprovacao=[]
    sfdr_result_aprovacao=[]
    enob_result_aprovacao=[]
    crosstalk_result_aprovacao=[]
    missing_code_result_aprovacao=[]
    dif_amp_result_aprovacao=[]
    
    snr_result_value_final=[]
    sfdr_result_value_final=[]
    enob_result_value_final=[]
    crosstalk_result_value_final=[]
    missing_code_result_value_final=[]
    dif_amp_result_value_final=[]
    

    i=0
    for i in range (0,4):
        
        #Avaliação do SNR
        if (str(snr_result_values)=="Teste não realizado"):
            aux = "SNR do Canal "+str(i+1)+": Teste não realizado "
            snr_result_aprovacao.append(aux)
            snr_result_value_final.append(aux)
            snr_result_final.append(aux)
        else:
            #Avaliação do SNR
            if (utilizarMatlab_check==True):
                if (snr_result_values[i]>snr_result_values_matlab[i]):
                    aux = snr_result_values[i]
                else:
                    aux = snr_result_values_matlab[i]
            else:
                aux = snr_result_values[i]
        
            snr_result_value_final.append(aux)
            if (aux < snr_dB_criterio):
                aux2=("SNR do Canal "+str(i+1)+" Falhou - Valor Medido: "+str(round(aux,2))+" [dB] [Critério >= "+str(snr_dB_criterio)+" [dB] ]")
                snr_result_final.append(aux2)
                snr_result_aprovacao.append("Falhou")
            else:
                aux2=("SNR do Canal "+str(i+1)+"OK - Valor Medido: "+str(round(aux,2))+" [dB] [Critério >= "+str(snr_dB_criterio)+" [dB] ]")
                snr_result_final.append(aux2)
                snr_result_aprovacao.append("OK")
        
        #Avaliação do SFDR
        if (str(sfdr_result_values)=="Teste não realizado"):
            aux = "SFDR do Canal "+str(i+1)+": Teste não realizado "
            sfdr_result_aprovacao.append(aux)
            sfdr_result_value_final.append(aux)
            sfdr_result_final.append(aux)
        else:
            if(utilizarMatlab_check==True):
                if (sfdr_result_values[i]>sfdr_result_values_matlab[i]):
                    aux = sfdr_result_values[i]
                else:
                    aux = sfdr_result_values_matlab[i]
            else:
                aux = sfdr_result_values[i]
            sfdr_result_value_final.append(aux)
        
            if (aux < sfdr_dBFS_criterio or str(aux) == "nan" or str(aux)=="inf"):
                aux2=("SFDR do Canal "+str(i+1)+" Falhou - Valor Medido: "+str(round(aux,2))+" [dBFS] [Critério >= "+str(sfdr_dBFS_criterio)+" [dBFS] ]")
                sfdr_result_final.append(aux2)
                sfdr_result_aprovacao.append("Falhou")
            else:
                aux2=("SFDR do Canal "+str(i+1)+" OK - Valor Medido: "+str(round(aux,2))+" [dBFS] [Critério >= "+str(sfdr_dBFS_criterio)+" [dBFS] ]")
                sfdr_result_final.append(aux2)
                sfdr_result_aprovacao.append("OK")

        #Avaliação do ENOB
        if (str(enob_result_values)=="Teste não realizado"):
            aux = "ENOB do Canal "+str(i+1)+": Teste não realizado "
            enob_result_aprovacao.append(aux)
            enob_result_value_final.append(aux)
            enob_result_final.append(aux)
        else:
            if (utilizarMatlab_check==True):
                if (enob_result_values[i]>enob_result_values_matlab[i]):
                    aux = enob_result_values[i]
                else:
                    aux = enob_result_values_matlab[i]
            else:
                aux = enob_result_values[i]
            enob_result_value_final.append(aux)
        
            if (aux < enob_criterio):
                aux2=("ENOB do Canal "+str(i+1)+" Falhou - Valor Medido: "+str(round(aux,2))+" [bits] [Critério >= "+str(enob_criterio)+" [bits] ]")
                enob_result_final.append(aux2)
                enob_result_aprovacao.append("Falhou")
            else:
                aux2=("ENOB do Canal "+str(i+1)+" OK - Valor Medido: "+str(round(aux,2))+" [bits] [Critério >= "+str(enob_criterio)+" [bits] ]")
                enob_result_final.append(aux2)
                enob_result_aprovacao.append("OK")

        #Avaliação do CROSSTALK
        
        if (str(crosstalk_result_values)=="Teste não realizado"):
            j=0
            for j in range (0,3):
                aux = "CROSSTALK do Canal "+str(i+1)+"-"+str(crosstalk_canal_analisado[i][j])+": Teste não realizado "
                crosstalk_result_aprovacao.append(aux)
                crosstalk_result_value_final.append(aux)
                crosstalk_result_final.append(aux)
        else:
            j=0
            teste=0
            for j in range (0,3):
                aux = crosstalk_result_values[i][j]
                if (aux < crosstalk_criterio):
                    aux2=("CROSSTALK do Canal "+str(i+1)+"-"+str(crosstalk_canal_analisado[i][j])+" Falhou - Valor Medido: "+str(round(aux,2))+" [dBFS] [Critério >= "+str(crosstalk_criterio)+" [dBFS] ]")
                    crosstalk_result_final.append(aux2)
                    teste=1
                else:
                    aux2=("CROOSTALK do Canal "+str(i+1)+"-"+str(crosstalk_canal_analisado[i][j])+" OK - Valor Medido: "+str(round(aux,2))+" [dBFS] [Critério >= "+str(crosstalk_criterio)+" [dBFS] ]")
                    crosstalk_result_final.append(aux2)
                
            if (teste==1):
                crosstalk_result_aprovacao.append("Falhou")
            else:
                crosstalk_result_aprovacao.append("OK")
                      
        
    #Avaliação do Missing Codes
    
    if(str(missingcodes_result_final)=="Teste não realizado"):
        missingcodes_result_final="Missing Codes: Teste não realizado"
        missingcodes_result_value_final="Missing Codes: Teste não realizado"
        missingcodes_detected_positions="Missing Codes: Teste não realizado"
        missingcodes_aux="MISSING CODES: Teste não realizado"
        
    else:
        missingcodes_aux=[]
        if(missingcodes_result_aprovacao[0]=="OK"):
            missingcodes_aux.append("MISSING CODES: Canal 1: OK [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        else:
            missingcodes_aux.append("MISSING CODES: Canal 1: FAIL [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        
        if(missingcodes_result_aprovacao[1]=="OK"):
            missingcodes_aux.append("MISSING CODES: Canal 2: OK [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        else:
            missingcodes_aux.append("MISSING CODES: Canal 2: FAIL [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        
        if(missingcodes_result_aprovacao[2]=="OK"):
            missingcodes_aux.append("MISSING CODES: Canal 3: OK [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        else:
            missingcodes_aux.append("MISSING CODES: Canal 3: FAIL [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        
        if(missingcodes_result_aprovacao[3]=="OK"):
            missingcodes_aux.append("MISSING CODES: Canal 4: OK [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
        else:
            missingcodes_aux.append("MISSING CODES: Canal 4: FAIL [Range: -"+str(sinal_entrada_crate)+" até "+str(sinal_entrada_crate)+"] [Número de Posições: "+str(2*sinal_entrada_crate)+"]")
    
        
    #Avaliação da DIFERENÇA DAS AMPLITUDES
    if (str(dif_amp_result_values)=="Teste não realizado"):
        aux1 = "DIF. AMP. do Canal 1-3: Teste não realizado"
        aux2 = "DIF. AMP. do Canal 2-4: Teste não realizado"
        aux1_aprovacao = "Teste não realizado"
        aux2_aprovacao = "Teste não realizado"
        dif_amp_result_values=["Teste não realizado","Teste não realizado"]
    else:
        i=0
        aux1_aprovacao=[]
        aux2_aprovacao=[]
        aux1=[]
        aux2=[]
        teste_1=0
        teste_2=0
        
        for i in range (0,11):
            #Canal 1-3
            if (abs(dif_amp_result_values[0][i])<dif_amp_criterio):
                aux1.append("DIF. AMP. do Canal 1-3: [Pot.de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] RESULTADO: OK")
                aux1.append("DIF. AMP. do Canal 1-3: [Pot. de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] VALOR MEDIDO: "+ str(abs(round(dif_amp_result_values[0][i],5))) + " - CRITÉRIO: <=" + str(dif_amp_criterio))
            else:
                aux1.append("DIF. AMP. do Canal 1-3: [Pot.de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] RESULTADO: FAIL")
                aux1.append("DIF. AMP. do Canal 1-3: [Pot. de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] VALOR MEDIDO: "+ str(abs(round(dif_amp_result_values[0][i],5))) + " - CRITÉRIO: <=" + str(dif_amp_criterio))
                teste_1=teste_1+1
            #Canal 2-4
            if (abs(dif_amp_result_values[1][i])<dif_amp_criterio):
                aux2.append("DIF. AMP. do Canal 2-4: [Pot.de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] RESULTADO: OK")
                aux2.append("DIF. AMP. do Canal 2-4: [Pot. de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] VALOR MEDIDO: "+ str(abs(round(dif_amp_result_values[1][i],5))) + " - CRITÉRIO: <=" + str(dif_amp_criterio))
            else:
                aux2.append("DIF. AMP. do Canal 2-4: [Pot.de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] RESULTADO: FAIL")
                aux2.append("DIF. AMP. do Canal 2-4: [Pot. de Ent.: "+ str(round(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+i*2,4)) + " dBm] VALOR MEDIDO: "+ str(abs(round(dif_amp_result_values[1][i],5))) + " - CRITÉRIO: <=" + str(dif_amp_criterio))
                teste_2=teste_2+1
                
        if(teste_1==0):
            aux1_aprovacao="OK"
        else:
            aux1_aprovacao="Falhou"
        if(teste_2==0):
            aux2_aprovacao="OK"
        else:
            aux2_aprovacao="Falhou"
        
        
    dif_amp_result_final=[aux1,aux2]
    dif_amp_result_aprovacao=[aux1_aprovacao,aux2_aprovacao]
    dif_amp_result_value_final=[dif_amp_result_values[0],dif_amp_result_values[1]]
        


    #Teste da EEPROM 
    eeprom_result_final=[]   
    eeprom_result_final.append("EEPROM - RESULTADO FINAL Teste do Componente: "+eeprom_result)
    eeprom_result_final.append("EEPROM - Acesso ao metodo de ESCRITA: " + eeprom_write_check_result)
    eeprom_result_final.append("EEPROM - Acesso ao metodo de LEITURA:"+ eeprom_read_check_result)
    
    #Teste do ICS854S01I 
    ics854s01i_result_final=[]   
    ics854s01i_result_final.append("ICS854S01I - RESULTADO FINAL Teste do Componente: "+ics854s01i_result)
    ics854s01i_result_final.append("ICS854S01I - Acesso ao metodo de ESCRITA: " + ics854s01i_write_check_result)
    ics854s01i_result_final.append("ICS854S01I - Acesso ao metodo de LEITURA:"+ ics854s01i_read_check_result)

    #Teste do SI571    
    si571_result_final=[]
    si571_result_final.append("SI571 - RESULTADO FINAL Teste do Componente: "+si571_result)
    si571_result_final.append("SI571 - Acesso ao metodo de ESCRITA: " + si571_write_check_result)
    si571_result_final.append("SI571 - Acesso ao metodo de LEITURA:"+ si571_read_check_result)

    #Teste do AD9510    
    ad9510_result_final=[]
    ad9510_result_final.append("AD9510 - RESULTADO FINAL Teste do Componente: "+ad9510_result)
    ad9510_result_final.append("AD9510 - Acesso ao metodo de ESCRITA: " + ad9510_write_check_result)
    ad9510_result_final.append("AD9510 - Acesso ao metodo de LEITURA:"+ ad9510_read_check_result)    
        
    result=[]
   
    result.append("Teste da Placa: ADC\n\n")
    result.append("Operador: "+str(operador))
    result.append("Número de Série: "+str(n_serie_adc))
    result.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
    result.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
    result.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
    result.append("Gravação da FPGA:")
    result.append(fpga_str_result+"\n")
    result.append("Comunicação/Aquisicao de Dados:")
    result.append(crate_str_result[0])
    result.append(crate_str_result[1])
    result.append("Numero de PTS Coletados: "+str(NUM_PONTS_CRATE))
    result.append("Numero de PTS Coletados [MissingCodes]: "+str(NUM_PONTS_CRATE_MISSINGCODES))
    result.append("Numero de PTS de FFT: "+str(NUM_PONTS_FFT))
    result.append(switch_str_result[0])
    result.append(switch_str_result[1])
    result.append(sig_gen_in_str_result[0])
    result.append(sig_gen_in_str_result[1])
    result.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA)+" [dBm]")
    result.append("GERADOR DE SINAIS INPUT [MissingCodes] - Frequencia: "+str(FREQUENCY_INPUT_MISSINGCODES)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA_MISSINGCODES)+" [dBm]")
    result.append(sig_gen_clock_str_result[0])
    result.append(sig_gen_clock_str_result[1])
    result.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK)+" [dBm]")
    result.append("GERADOR DE SINAIS CLOCK [MissingCodes] - Frequencia: "+str(FREQUENCY_SAMPLE_MISSINGCODES)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK_MISSINGCODES)+" [dBm]")
    result.append(matlab_str_result+"\n")
    
    
    result.append("Resultados:")
    i=0
    for i in range (0,4):
        result.append(snr_result_final[i])
    i=0
    for i in range (0,4):
        result.append(sfdr_result_final[i])
    i=0
    for i in range (0,4):
        result.append(enob_result_final[i])  
    i=0
    for i in range (0,12):
        result.append(crosstalk_result_final[i])    

    if(str(dif_amp_result_values[0])=="Teste não realizado"):
        i=0
        for i in range (0,len(dif_amp_result_final)):
            result.append(dif_amp_result_final[i])
    else:
        i=0
        for i in range (0,len(dif_amp_result_final[0])):
            result.append(dif_amp_result_final[0][i])
        i=0
        for i in range (0,len(dif_amp_result_final[1])):
            result.append(dif_amp_result_final[1][i])

    if(str(missingcodes_aux)=="MISSING CODES: Teste não realizado"):    
        result.append("MISSING CODES CH1: Teste não realizado")
        result.append("MISSING CODES CH2: Teste não realizado")
        result.append("MISSING CODES CH3: Teste não realizado")
        result.append("MISSING CODES CH4: Teste não realizado")
    else:
        i=0
        for i in range (0,len(missingcodes_result_final)):
            result.append(missingcodes_aux[i])
            result.append(missingcodes_result_final[i]) 
            j=0
            if(missingcodes_result_aprovacao[i]!="OK"):
                result.append("MISSING CODES CH"+str(i+1)+": Posições do AD com MissingCodes:")
                for j in range (0, len(missingcodes_detected_positions[i])):
                    result.append(missingcodes_detected_positions[i][j])
                            

    i=0
    for i in range (0,3):
        result.append(eeprom_result_final[i])
    i=0
    for i in range (0,3):
        result.append(ics854s01i_result_final[i])
    i=0
    for i in range (0,3):
        result.append(si571_result_final[i])
    i=0
    for i in range (0,3):
        result.append(ad9510_result_final[i])   
    
    
    
           

    
    return(snr_result_final,sfdr_result_final,enob_result_final,crosstalk_result_final,dif_amp_result_final,
           eeprom_result_final,ics854s01i_result_final,si571_result_final,ad9510_result_final,
           snr_result_aprovacao,sfdr_result_aprovacao,enob_result_aprovacao,crosstalk_result_aprovacao,dif_amp_result_aprovacao,
           snr_result_value_final,sfdr_result_value_final,enob_result_value_final,crosstalk_result_values,dif_amp_result_value_final,
           result)
    
    
    
    
    
def result_data(aquisition_nivel_1,aquisition_nivel_2,aquisition_nivel_3,
                serial_number,datapath_save,
                crate_data_list,crate_data_list_missingcodes,crate_data_dif_amp_list,
                numero_media,NUM_PONTS_CRATE,NUM_PONTS_CRATE_MISSINGCODES,
                start_time_general_str,stop_time_general_str,duracao_teste_general_str,
                fpga_str_result,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result,
                FREQUENCY_INPUT,FREQUENCY_SAMPLE,FREQUENCY_INPUT_MISSINGCODES,FREQUENCY_SAMPLE_MISSINGCODES,
                AMPLITUDE_SINAL_ENTRADA,AMPLITUDE_SINAL_CLOCK,AMPLITUDE_SINAL_ENTRADA_MISSINGCODES,AMPLITUDE_SINAL_CLOCK_MISSINGCODES,AMPLITUDE_SINAL_ENTRADA_DIF_AMP):
    
    #Salva os dados adquiridos para realizar o cálculo do MissingCodes
    #list_to_file(0,crate_data_list_missingcodes, datapath_save + serial_number + "_missingcodes_data_crate.txt")
    
    num_canal_switch_ativo=4   
    espacamento =17    
         
    #Salva os dados adquiridos para os demais testes
    result_crate_data=[]
    if(aquisition_nivel_1==0):
            result_crate_data.append("Teste da Placa: ADC\n\n")
            result_crate_data.append("Dados Coletados Diretamente do CRATE\n")
            result_crate_data.append("Descricao dos Dados Coletados neste arquivo...")
            result_crate_data.append("NENHUM DADO ADQUIRIDO\n")
            result_crate_data.append("Número de Série: "+str(serial_number))
            result_crate_data.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
            result_crate_data.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
            result_crate_data.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
            result_crate_data.append("Gravação da FPGA:")
            result_crate_data.append(fpga_str_result+"\n")
            result_crate_data.append("Comunicação/Aquisicao de Dados:")
            result_crate_data.append(crate_str_result[0])
            result_crate_data.append(crate_str_result[1])
            result_crate_data.append(switch_str_result[0])
            result_crate_data.append(switch_str_result[1])
            result_crate_data.append(sig_gen_in_str_result[0])
            result_crate_data.append(sig_gen_in_str_result[1])
            result_crate_data.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA)+" [dBm]")
            result_crate_data.append(sig_gen_clock_str_result[0])
            result_crate_data.append(sig_gen_clock_str_result[1])
            result_crate_data.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK)+" [dBm]")
            result_crate_data.append(matlab_str_result+"\n")       
            list_to_file_aux(0,result_crate_data, datapath_save+"crate_data/regular_data/"+ serial_number + "_crateData.txt")

        
    else:
        for k in range (0,num_canal_switch_ativo):
            for j in range (0, numero_media):
                result_crate_data=[]
                result_crate_data.append("Teste da Placa: ADC\n\n")
                result_crate_data.append("Dados Coletados Diretamente do CRATE\n")
                result_crate_data.append("Descricao dos Dados Coletados neste arquivo...")
                result_crate_data.append("Numero de Pontos Adquiridos: "+str(NUM_PONTS_CRATE))
                result_crate_data.append("Canal do Switch Ativo: "+str(k+1))
                result_crate_data.append("Num. da Requisicao: "+str(j+1)+"\n")
                result_crate_data.append("Número de Série: "+str(serial_number))
                result_crate_data.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
                result_crate_data.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
                result_crate_data.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
                result_crate_data.append("Gravação da FPGA:")
                result_crate_data.append(fpga_str_result+"\n")
                result_crate_data.append("Comunicação/Aquisicao de Dados:")
                result_crate_data.append(crate_str_result[0])
                result_crate_data.append(crate_str_result[1])
                result_crate_data.append(switch_str_result[0])
                result_crate_data.append(switch_str_result[1])
                result_crate_data.append(sig_gen_in_str_result[0])
                result_crate_data.append(sig_gen_in_str_result[1])
                result_crate_data.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA)+" [dBm]")
                result_crate_data.append(sig_gen_clock_str_result[0])
                result_crate_data.append(sig_gen_clock_str_result[1])
                result_crate_data.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK)+" [dBm]")
                result_crate_data.append(matlab_str_result+"\n")  
                result_crate_data.append("Canal_ADC_1".ljust(espacamento)+"Canal_ADC_2".ljust(espacamento)+"Canal_ADC_3".ljust(espacamento)+"Canal_ADC_4".ljust(espacamento))        
                for i in range (0, NUM_PONTS_CRATE):
                    result_crate_data.append(str(crate_data_list[k][j][0][i]).ljust(espacamento)+
                                             str(crate_data_list[k][j][1][i]).ljust(espacamento)+
                                             str(crate_data_list[k][j][2][i]).ljust(espacamento)+
                                             str(crate_data_list[k][j][3][i]).ljust(espacamento))
    
                list_to_file_aux(0,result_crate_data, datapath_save +"crate_data/regular_data/"+ serial_number + "_crateData_nMedia_"+str(j+1)+"_chSwitchAt_"+str(k+1)+".txt")


    #Salva os dados para o teste de MISSINGCODES
    result_crate_data_missingcodes=[]
    if(aquisition_nivel_2==0):
            result_crate_data_missingcodes.append("Teste da Placa: ADC\n\n")
            result_crate_data_missingcodes.append("Dados Coletados Diretamente do CRATE - Teste do MISSING CODES\n")
            result_crate_data_missingcodes.append("Descricao dos Dados Coletados neste arquivo...")
            result_crate_data_missingcodes.append("NENHUM DADO ADQUIRIDO\n")
            result_crate_data_missingcodes.append("Número de Série: "+str(serial_number))
            result_crate_data_missingcodes.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
            result_crate_data_missingcodes.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
            result_crate_data_missingcodes.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
            result_crate_data_missingcodes.append("Gravação da FPGA:")
            result_crate_data_missingcodes.append(fpga_str_result+"\n")
            result_crate_data_missingcodes.append("Comunicação/Aquisicao de Dados:")
            result_crate_data_missingcodes.append(crate_str_result[0])
            result_crate_data_missingcodes.append(crate_str_result[1])
            result_crate_data_missingcodes.append(switch_str_result[0])
            result_crate_data_missingcodes.append(switch_str_result[1])
            result_crate_data_missingcodes.append(sig_gen_in_str_result[0])
            result_crate_data_missingcodes.append(sig_gen_in_str_result[1])
            result_crate_data_missingcodes.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT_MISSINGCODES)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA_MISSINGCODES)+" [dBm]")
            result_crate_data_missingcodes.append(sig_gen_clock_str_result[0])
            result_crate_data_missingcodes.append(sig_gen_clock_str_result[1])
            result_crate_data_missingcodes.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE_MISSINGCODES)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK_MISSINGCODES)+" [dBm]")
            result_crate_data_missingcodes.append(matlab_str_result+"\n")        
            list_to_file_aux(0,result_crate_data_missingcodes, datapath_save +"crate_data/missingcode_data/"+ serial_number + "_crateDataMissingCodes.txt")

        
    else:
        for k in range (0,num_canal_switch_ativo):
            for j in range (0, numero_media):
                result_crate_data_missingcodes=[]
                result_crate_data_missingcodes.append("Teste da Placa: ADC\n\n")
                result_crate_data_missingcodes.append("Dados Coletados Diretamente do CRATE - Teste do MISSING CODES\n")
                result_crate_data_missingcodes.append("Descricao dos Dados Coletados neste arquivo...")
                result_crate_data_missingcodes.append("Numero de Pontos Adquiridos: "+str(NUM_PONTS_CRATE))
                result_crate_data_missingcodes.append("Canal do Switch Ativo: "+str(k+1))
                result_crate_data_missingcodes.append("Num. da Requisicao: "+str(j+1)+"\n")
                result_crate_data_missingcodes.append("Número de Série: "+str(serial_number))
                result_crate_data_missingcodes.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
                result_crate_data_missingcodes.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
                result_crate_data_missingcodes.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
                result_crate_data_missingcodes.append("Gravação da FPGA:")
                result_crate_data_missingcodes.append(fpga_str_result+"\n")
                result_crate_data_missingcodes.append("Comunicação/Aquisicao de Dados:")
                result_crate_data_missingcodes.append(crate_str_result[0])
                result_crate_data_missingcodes.append(crate_str_result[1])
                result_crate_data_missingcodes.append(switch_str_result[0])
                result_crate_data_missingcodes.append(switch_str_result[1])
                result_crate_data_missingcodes.append(sig_gen_in_str_result[0])
                result_crate_data_missingcodes.append(sig_gen_in_str_result[1])
                result_crate_data_missingcodes.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT_MISSINGCODES)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA_MISSINGCODES)+" [dBm]")
                result_crate_data_missingcodes.append(sig_gen_clock_str_result[0])
                result_crate_data_missingcodes.append(sig_gen_clock_str_result[1])
                result_crate_data_missingcodes.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE_MISSINGCODES)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK_MISSINGCODES)+" [dBm]")
                result_crate_data_missingcodes.append(matlab_str_result+"\n") 
                result_crate_data_missingcodes.append("Canal_ADC_1".ljust(espacamento)+"Canal_ADC_2".ljust(espacamento)+"Canal_ADC_3".ljust(espacamento)+"Canal_ADC_4".ljust(espacamento))        
                for i in range (0, NUM_PONTS_CRATE_MISSINGCODES):
                    result_crate_data_missingcodes.append(str(crate_data_list_missingcodes[k][j][0][i]).ljust(espacamento)+
                                                          str(crate_data_list_missingcodes[k][j][1][i]).ljust(espacamento)+
                                                          str(crate_data_list_missingcodes[k][j][2][i]).ljust(espacamento)+
                                                          str(crate_data_list_missingcodes[k][j][3][i]).ljust(espacamento))
    
                list_to_file_aux(0,result_crate_data_missingcodes, datapath_save +"crate_data/missingcode_data/"+ serial_number + "_crateDataMissingCodes_nMedia_"+str(j+1)+"_chSwitchAt_"+str(k+1)+".txt")
    

    #Salva os dados para o teste de DIF. AMPLITUDE
    #Salva os dados adquiridos para os demais testes
    result_crate_data_dif_amp=[]
    if(aquisition_nivel_3==0):
        result_crate_data_dif_amp.append("Teste da Placa: ADC\n\n")
        result_crate_data_dif_amp.append("Dados Coletados Diretamente do CRATE - Teste de DIFERENCA DE AMPLITUDE\n")
        result_crate_data_dif_amp.append("Descricao dos Dados Coletados neste arquivo...")
        result_crate_data_dif_amp.append("NENHUM DADO ADQUIRIDO\n")
        result_crate_data_dif_amp.append("Número de Série: "+str(serial_number))
        result_crate_data_dif_amp.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_crate_data_dif_amp.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_crate_data_dif_amp.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_crate_data_dif_amp.append("Gravação da FPGA:")
        result_crate_data_dif_amp.append(fpga_str_result+"\n")
        result_crate_data_dif_amp.append("Comunicação/Aquisicao de Dados:")
        result_crate_data_dif_amp.append(crate_str_result[0])
        result_crate_data_dif_amp.append(crate_str_result[1])
        result_crate_data_dif_amp.append(switch_str_result[0])
        result_crate_data_dif_amp.append(switch_str_result[1])
        result_crate_data_dif_amp.append(sig_gen_in_str_result[0])
        result_crate_data_dif_amp.append(sig_gen_in_str_result[1])
        result_crate_data_dif_amp.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT)+" [Hz]- Amplitude: -22.5 ate -2.5 [dBm]")
        result_crate_data_dif_amp.append(sig_gen_clock_str_result[0])
        result_crate_data_dif_amp.append(sig_gen_clock_str_result[1])
        result_crate_data_dif_amp.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK)+" [dBm]")
        result_crate_data_dif_amp.append(matlab_str_result+"\n")       
        list_to_file_aux(0,result_crate_data_dif_amp, datapath_save +"crate_data/dif_amp_data/"+ serial_number + "_crateDataDifAmp.txt")

        
    else:
        num_media=1
        num_nivel_pot=11
        print("tem que ser 11",len(crate_data_dif_amp_list))
        print("tem que ser 4",len(crate_data_dif_amp_list[0]))
        print("tem que ser 1",len(crate_data_dif_amp_list[0][0]))
        print("tem que ser 4",len(crate_data_dif_amp_list[0][0][0]))   
        print("tem que ser 100",len(crate_data_dif_amp_list[0][0][0][0]))      
        
        
        
        for z in range (0,num_nivel_pot):
            for k in range (0,num_canal_switch_ativo):
                for j in range (0, num_media):
                    result_crate_data_dif_amp=[]
                    result_crate_data_dif_amp.append("Teste da Placa: ADC\n\n")
                    result_crate_data_dif_amp.append("Dados Coletados Diretamente do CRATE - Teste de DIFERENCA DE AMPLITUDE\n")
                    result_crate_data_dif_amp.append("Descricao dos Dados Coletados neste arquivo...")
                    result_crate_data_dif_amp.append("Numero de Pontos Adquiridos: "+str(NUM_PONTS_CRATE))
                    result_crate_data_dif_amp.append("Canal do Switch Ativo: "+str(k+1))
                    result_crate_data_dif_amp.append("Num. da Requisicao: "+str(j+1)+"\n")
                    result_crate_data_dif_amp.append("Número de Série: "+str(serial_number))
                    result_crate_data_dif_amp.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
                    result_crate_data_dif_amp.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
                    result_crate_data_dif_amp.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
                    result_crate_data_dif_amp.append("Gravação da FPGA:")
                    result_crate_data_dif_amp.append(fpga_str_result+"\n")
                    result_crate_data_dif_amp.append("Comunicação/Aquisicao de Dados:")
                    result_crate_data_dif_amp.append(crate_str_result[0])
                    result_crate_data_dif_amp.append(crate_str_result[1])
                    result_crate_data_dif_amp.append(switch_str_result[0])
                    result_crate_data_dif_amp.append(switch_str_result[1])
                    result_crate_data_dif_amp.append(sig_gen_in_str_result[0])
                    result_crate_data_dif_amp.append(sig_gen_in_str_result[1])
                    result_crate_data_dif_amp.append("GERADOR DE SINAIS INPUT - Frequencia: "+str(FREQUENCY_INPUT)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_ENTRADA_DIF_AMP+z*2)+"[dBm]")
                    result_crate_data_dif_amp.append(sig_gen_clock_str_result[0])
                    result_crate_data_dif_amp.append(sig_gen_clock_str_result[1])
                    result_crate_data_dif_amp.append("GERADOR DE SINAIS CLOCK - Frequencia: "+str(FREQUENCY_SAMPLE)+" [Hz]- Amplitude: "+str(AMPLITUDE_SINAL_CLOCK)+" [dBm]")
                    result_crate_data_dif_amp.append(matlab_str_result+"\n")  
                    result_crate_data_dif_amp.append("Canal_ADC_1".ljust(espacamento)+"Canal_ADC_2".ljust(espacamento)+"Canal_ADC_3".ljust(espacamento)+"Canal_ADC_4".ljust(espacamento))        
                    for i in range (0, NUM_PONTS_CRATE):
                        result_crate_data_dif_amp.append(str(crate_data_dif_amp_list[z][k][j][0][i]).ljust(espacamento)+
                                                         str(crate_data_dif_amp_list[z][k][j][1][i]).ljust(espacamento)+
                                                         str(crate_data_dif_amp_list[z][k][j][2][i]).ljust(espacamento)+
                                                         str(crate_data_dif_amp_list[z][k][j][3][i]).ljust(espacamento))
        
                    list_to_file_aux(0,result_crate_data_dif_amp, datapath_save +"crate_data/dif_amp_data/"+ serial_number + "_crateDataDifAmp_nMedia_"+str(j+1)+"_chSwitchAt_"+str(k+1)+"_"+str(abs(AMPLITUDE_SINAL_ENTRADA_DIF_AMP)-z*2)+"_dBm.txt")

    

def results_components(eeprom_check,serial_number,datapath_save,
                       start_time_general_str,stop_time_general_str,duracao_teste_general_str,
                       fpga_str_result,crate_str_result,switch_str_result,sig_gen_in_str_result,sig_gen_clock_str_result,matlab_str_result,
                       all_values_dec,all_values_hex,
                       memory_position_standard_dec,memory_position_standard_hex,
                       value_write,value_read,
                       ics854s01i_check,ics854s01i_log,
                       si571_check,si571_log,
                       ad9510_check,ad9510_log):

    #EEPROM
    result_eeprom=[]
    if(eeprom_check==False):
        result_eeprom.append("Teste da Placa: ADC - Teste do Componente EEPROM\n\n")
        result_eeprom.append("Descricao dos Dados Coletados neste arquivo...")
        result_eeprom.append("NENHUM DADO ADQUIRIDO\n")
        result_eeprom.append("Número de Série: "+str(serial_number))
        result_eeprom.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_eeprom.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_eeprom.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_eeprom.append("Gravação da FPGA:")
        result_eeprom.append(fpga_str_result+"\n")
        result_eeprom.append("Comunicação/Aquisicao de Dados:")
        result_eeprom.append(crate_str_result[0])
        result_eeprom.append(crate_str_result[1])
        result_eeprom.append(switch_str_result[0])
        result_eeprom.append(switch_str_result[1])
        result_eeprom.append(sig_gen_in_str_result[0])
        result_eeprom.append(sig_gen_in_str_result[1])
        result_eeprom.append(sig_gen_clock_str_result[0])
        result_eeprom.append(sig_gen_clock_str_result[1])
        result_eeprom.append(matlab_str_result+"\n")       
        list_to_file_aux(0,result_eeprom, datapath_save+"components/eeprom/"+ serial_number + "_eeprom.txt")

    else:
        espacamento=20
        result_eeprom.append("Teste da Placa: ADC - Teste do Componente EEPROM\n\n")
        result_eeprom.append("Descriação dos Dados Coletados neste arquivo...")
        result_eeprom.append("Dados adquiridos!\n")
        result_eeprom.append("Número de Série: "+str(serial_number))
        result_eeprom.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_eeprom.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_eeprom.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_eeprom.append("Gravação da FPGA:")
        result_eeprom.append(fpga_str_result+"\n")
        result_eeprom.append("Comunicação/Aquisicao de Dados:")
        result_eeprom.append(crate_str_result[0])
        result_eeprom.append(crate_str_result[1])
        result_eeprom.append(switch_str_result[0])
        result_eeprom.append(switch_str_result[1])
        result_eeprom.append(sig_gen_in_str_result[0])
        result_eeprom.append(sig_gen_in_str_result[1])
        result_eeprom.append(sig_gen_clock_str_result[0])
        result_eeprom.append(sig_gen_clock_str_result[1])
        result_eeprom.append(matlab_str_result+"\n") 
        result_eeprom.append("Medicoes Realizadas:") 
        result_eeprom.append("Pos. Memória [dec]".ljust(espacamento)+"Pos. Memória [hex]".ljust(espacamento)+
                             "Valor Escrito [dec]".ljust(espacamento)+"Valor Escrito [hex]".ljust(espacamento)+
                             "Valor Lido [hex]".ljust(espacamento)) 
        for i in range(0,len(all_values_dec)):
            result_eeprom.append(str(memory_position_standard_dec[i]).ljust(espacamento)+str(memory_position_standard_hex[i]).ljust(espacamento)+
                                 str(all_values_dec[i]).ljust(espacamento)+str(all_values_hex[i]).ljust(espacamento)+
                                 str(value_read[i]).ljust(espacamento)) 
        list_to_file_aux(0,result_eeprom, datapath_save+"components/eeprom/"+ serial_number + "_eeprom.txt")

    
    #ics854s01i
    result_ics854s01i=[]
    if(ics854s01i_check==False):
        result_ics854s01i.append("Teste da Placa: ADC - Teste do Componente ICS854S01I\n\n")
        result_ics854s01i.append("Descricao dos Dados Coletados neste arquivo...")
        result_ics854s01i.append("NENHUM DADO ADQUIRIDO\n")
        result_ics854s01i.append("Número de Série: "+str(serial_number))
        result_ics854s01i.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_ics854s01i.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_ics854s01i.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_ics854s01i.append("Gravação da FPGA:")
        result_ics854s01i.append(fpga_str_result+"\n")
        result_ics854s01i.append("Comunicação/Aquisicao de Dados:")
        result_ics854s01i.append(crate_str_result[0])
        result_ics854s01i.append(crate_str_result[1])
        result_ics854s01i.append(switch_str_result[0])
        result_ics854s01i.append(switch_str_result[1])
        result_ics854s01i.append(sig_gen_in_str_result[0])
        result_ics854s01i.append(sig_gen_in_str_result[1])
        result_ics854s01i.append(sig_gen_clock_str_result[0])
        result_ics854s01i.append(sig_gen_clock_str_result[1])
        result_ics854s01i.append(matlab_str_result+"\n")       
        list_to_file_aux(0,result_ics854s01i, datapath_save+"components/ics854s01i/"+ serial_number + "_ics854s01i.txt")

    else:
        result_ics854s01i.append("Teste da Placa: ADC - Teste do Componente ICS854S01I\n\n")
        result_ics854s01i.append("Descricao dos Dados Coletados neste arquivo...")
        result_ics854s01i.append("Dados adquiridos!\n")
        result_ics854s01i.append("Número de Série: "+str(serial_number))
        result_ics854s01i.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_ics854s01i.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_ics854s01i.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_ics854s01i.append("Gravação da FPGA:")
        result_ics854s01i.append(fpga_str_result+"\n")
        result_ics854s01i.append("Comunicação/Aquisicao de Dados:")
        result_ics854s01i.append(crate_str_result[0])
        result_ics854s01i.append(crate_str_result[1])
        result_ics854s01i.append(switch_str_result[0])
        result_ics854s01i.append(switch_str_result[1])
        result_ics854s01i.append(sig_gen_in_str_result[0])
        result_ics854s01i.append(sig_gen_in_str_result[1])
        result_ics854s01i.append(sig_gen_clock_str_result[0])
        result_ics854s01i.append(sig_gen_clock_str_result[1])
        result_ics854s01i.append(matlab_str_result+"\n")  
        result_ics854s01i.append("Medicoes Realizadas:")   
        for i in range (0,len(ics854s01i_log)):
            result_ics854s01i.append(ics854s01i_log[i])
 
        list_to_file_aux(0,result_ics854s01i, datapath_save+"components/ics854s01i/"+ serial_number + "_ics854s01i.txt")
        

    #si571
    result_si571=[]
    if(si571_check==False):
        result_si571.append("Teste da Placa: ADC - Teste do Componente SI571\n\n")
        result_si571.append("Descricao dos Dados Coletados neste arquivo...")
        result_si571.append("NENHUM DADO ADQUIRIDO\n")
        result_si571.append("Número de Série: "+str(serial_number))
        result_si571.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_si571.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_si571.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_si571.append("Gravação da FPGA:")
        result_si571.append(fpga_str_result+"\n")
        result_si571.append("Comunicação/Aquisicao de Dados:")
        result_si571.append(crate_str_result[0])
        result_si571.append(crate_str_result[1])
        result_si571.append(switch_str_result[0])
        result_si571.append(switch_str_result[1])
        result_si571.append(sig_gen_in_str_result[0])
        result_si571.append(sig_gen_in_str_result[1])
        result_si571.append(sig_gen_clock_str_result[0])
        result_si571.append(sig_gen_clock_str_result[1])
        result_si571.append(matlab_str_result+"\n")       
        list_to_file_aux(0,result_si571, datapath_save+"components/si571/"+ serial_number + "_si571.txt")

    else:
        result_si571.append("Teste da Placa: ADC - Teste do Componente SI571\n\n")
        result_si571.append("Descricao dos Dados Coletados neste arquivo...")
        result_si571.append("Dados adquiridos!\n")
        result_si571.append("Número de Série: "+str(serial_number))
        result_si571.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_si571.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_si571.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_si571.append("Gravação da FPGA:")
        result_si571.append(fpga_str_result+"\n")
        result_si571.append("Comunicação/Aquisicao de Dados:")
        result_si571.append(crate_str_result[0])
        result_si571.append(crate_str_result[1])
        result_si571.append(switch_str_result[0])
        result_si571.append(switch_str_result[1])
        result_si571.append(sig_gen_in_str_result[0])
        result_si571.append(sig_gen_in_str_result[1])
        result_si571.append(sig_gen_clock_str_result[0])
        result_si571.append(sig_gen_clock_str_result[1])
        result_si571.append(matlab_str_result+"\n")  
        result_si571.append("Medicoes Realizadas:")   
        for i in range (0,len(si571_log)):
            result_si571.append(si571_log[i])
 
        list_to_file_aux(0,result_si571, datapath_save+"components/si571/"+ serial_number + "_si571.txt")


    #ad9510
    result_ad9510=[]
    if(ad9510_check==False):
        result_ad9510.append("Teste da Placa: ADC - Teste do Componente AD9510\n\n")
        result_ad9510.append("Descricao dos Dados Coletados neste arquivo...")
        result_ad9510.append("NENHUM DADO ADQUIRIDO\n")
        result_ad9510.append("Número de Série: "+str(serial_number))
        result_ad9510.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_ad9510.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_ad9510.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_ad9510.append("Gravação da FPGA:")
        result_ad9510.append(fpga_str_result+"\n")
        result_ad9510.append("Comunicação/Aquisicao de Dados:")
        result_ad9510.append(crate_str_result[0])
        result_ad9510.append(crate_str_result[1])
        result_ad9510.append(switch_str_result[0])
        result_ad9510.append(switch_str_result[1])
        result_ad9510.append(sig_gen_in_str_result[0])
        result_ad9510.append(sig_gen_in_str_result[1])
        result_ad9510.append(sig_gen_clock_str_result[0])
        result_ad9510.append(sig_gen_clock_str_result[1])
        result_ad9510.append(matlab_str_result+"\n")       
        list_to_file_aux(0,result_ad9510, datapath_save+"components/ad9510/"+ serial_number + "_ad9510.txt")

    else:
        result_ad9510.append("Teste da Placa: ADC - Teste do Componente AD9510\n\n")
        result_ad9510.append("Descricao dos Dados Coletados neste arquivo...")
        result_ad9510.append("Dados adquiridos!\n")
        result_ad9510.append("Número de Série: "+str(serial_number))
        result_ad9510.append("Data/Horário do Início do Teste:"+str(start_time_general_str))
        result_ad9510.append("Data/Horário do Fim do Teste: "+str(stop_time_general_str))
        result_ad9510.append("Duração do Teste: "+str(duracao_teste_general_str)+" min\n")
        result_ad9510.append("Gravação da FPGA:")
        result_ad9510.append(fpga_str_result+"\n")
        result_ad9510.append("Comunicação/Aquisicao de Dados:")
        result_ad9510.append(crate_str_result[0])
        result_ad9510.append(crate_str_result[1])
        result_ad9510.append(switch_str_result[0])
        result_ad9510.append(switch_str_result[1])
        result_ad9510.append(sig_gen_in_str_result[0])
        result_ad9510.append(sig_gen_in_str_result[1])
        result_ad9510.append(sig_gen_clock_str_result[0])
        result_ad9510.append(sig_gen_clock_str_result[1])
        result_ad9510.append(matlab_str_result+"\n")  
        result_ad9510.append("Medicoes Realizadas:")   
        for i in range (0,len(ad9510_log)):
            result_ad9510.append(ad9510_log[i])
 
        list_to_file_aux(0,result_ad9510, datapath_save+"components/ad9510/"+ serial_number + "_ad9510.txt")

      
    
    
        