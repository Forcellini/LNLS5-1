from subprocess import Popen, PIPE
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication



PLL_CLK_SEL_MAX = 2
PLL_CLK_SEL_MIN=1
    
A_DIV_MAX = 63
A_DIV_MIN=0
    
B_DIV_MAX=8191
B_DIV_MIN=3
    
R_DIV_MIN=0
R_DIV_MAX=16383
    
PRESCALER_DIV_MIN=0
PRESCALER_DIV_MAX=8
    
PLL_CLK_SEL_RUN = "yes"
A_DIV_RUN = "yes"
B_DIV_RUN = "yes"
R_DIV_RUN = "yes"
PRESCALER_DIV_RUN = "yes"

def ad9510(IP_CRATE,POSITION_CRATE,POSITION_ADC,tela_leds):
    
    local = "cd CRATE_ACESSO/bpm-app/.halcs-libs/examples\n"
    
    tela_leds.ui.progressBar.setValue(0)  
    tela_leds.repaint()
    QApplication.processEvents() 
       
    print("Iniciou o Teste do AD9510")
    start_time=datetime.datetime.now()
    start_time_str=start_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Start_write_time:",start_time_str)
    ad9510_log=[]
   
    write_text="WRITTEN VALUE: "
    read_text="READ VALUE: "
    write_verification_text="WRITE CHECK: "
    read_verification_text="READ CHECK: "
    ad9510_write_check=0
    ad9510_read_check=0
    
    
    #Teste do PLL_CLK_SEL
    if(PLL_CLK_SEL_RUN=="yes"):
        print("Iniciou o Teste do PLL_CLK_SEL")
        ad9510_log.append("Iniciou o Teste do PLL_CLK_SEL")
        start_pll_clk_sel_time=datetime.datetime.now()
        start_pll_clk_sel_time_str=start_pll_clk_sel_time.strftime("%Y-%m-%d %H:%M:%S")
        print("start_pll_clk_sel: ",start_pll_clk_sel_time_str)
        i=PLL_CLK_SEL_MIN
        read_text="READ VALUE OF PLL_CLK_SEL: "
        write_text="WRITTEN VALUE OF PLL_CLK_SEL: "
        pll_clk_sel_write=[]
        pll_clk_sel_read=[]
        #Realiza a escrita e leitura no mesmo loop, pois a funcao ./THALES_ad9510_ctl realiza ambos os processos automaticamente
        while(i<PLL_CLK_SEL_MAX+1):
            command = "./THALES_ad9510_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -pll_clk_sel "+str(i)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_value=command_stdout[len(command_stdout)-2].decode("utf-8")
            read_value=command_stdout[len(command_stdout)-1].decode("utf-8")
            write_aux=str(write_value).replace(write_text,"")
            read_aux=str(read_value).replace(read_text,"")
            pll_clk_sel_write.append(write_aux)
            pll_clk_sel_read.append(read_aux)
            
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
    
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   

            i=i+1
    
        #Teste de verificação
        print("Verificando resultado...")
        i=0
        check_pll_clk_sel=0
        while (i<PLL_CLK_SEL_MAX-PLL_CLK_SEL_MIN+1):
            ad9510_log.append("Valor Escrito: "+str(pll_clk_sel_write[i])+" - Valor lido: "+str(pll_clk_sel_read[i]))
            if(pll_clk_sel_write[i]!=pll_clk_sel_read[i]):
                ad9510_log.append("Fail Detected - Valor Escrito: "+str(pll_clk_sel_write[i])+" Valor lido: "+str(pll_clk_sel_read[i]))
                print("Fail Detected - Valor Escrito: ",pll_clk_sel_write[i]," Valor lido: ",pll_clk_sel_read[i])
                check_pll_clk_sel=check_pll_clk_sel+1
            i=i+1
    
        if (check_pll_clk_sel==0):
            print("PLL_CLK_SEL TEST: OK")
            ad9510_log.append("PLL_CLK_SEL TEST: OK")
        else:
            print("PLL_CLK_SEL TEST: FAIL")
            ad9510_log.append("PLL_CLK_SEL TEST: FAIL")
        
        print("Fim do Teste do PLL_CLK_SEL")
        ad9510_log.append("Fim do Teste do PLL_CLK_SEL\n")
        end_pll_clk_sel_time=datetime.datetime.now()
        end_pll_clk_sel_time_str=end_pll_clk_sel_time.strftime("%Y-%m-%d %H:%M:%S")
        print("end_pll_clk_sel_time: ",end_pll_clk_sel_time_str)
        duration_pll_clk_sel=((end_pll_clk_sel_time - start_pll_clk_sel_time).total_seconds())/60 #desprezível
        print("Duração do Teste PLL_CLK_SEL [min]: ",round(duration_pll_clk_sel,4))    
    else:
        print("PLL_CLK_SEL WILL NOT BE PERFORMED")
        ad9510_log.append("PLL_CLK_SEL WILL NOT BE PERFORMED\n")
        #FIXME: ESTA PARTE SÓ SERVE PARA DEBUG
        check_pll_clk_sel=0
        ad9510_write_check=0
        ad9510_read_check=0
        
    #Teste do A_DIV
    if(A_DIV_RUN=="yes"):
        print("Iniciou o Teste do A_DIV")
        ad9510_log.append("Iniciou o Teste do A_DIV")
        start_a_div_time=datetime.datetime.now()
        start_a_div_time_str=start_a_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("start_a_div_time: ",start_a_div_time_str)
        i=A_DIV_MIN
        read_text="READ VALUE OF A_DIV: "
        write_text="WRITTEN VALUE OF A_DIV: "
        a_div_write=[]
        a_div_read=[]
        #Realiza a escrita e leitura no mesmo loop, pois a funcao ./THALES_ad9510_ctl realiza ambos os processos automaticamente
        while(i<A_DIV_MAX+1):
            command = "./THALES_ad9510_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -a_div "+str(i)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_value=command_stdout[len(command_stdout)-2].decode("utf-8")
            read_value=command_stdout[len(command_stdout)-1].decode("utf-8")
            write_aux=str(write_value).replace(write_text,"")
            read_aux=str(read_value).replace(read_text,"")
            a_div_write.append(write_aux)
            a_div_read.append(read_aux)
            #print(write_aux)

            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
    
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1   
                
            i=i+1
    
        #Teste de verificação
        print("Verificando resultado...")
        i=0
        check_a_div=0
        while (i<A_DIV_MAX-A_DIV_MIN+1):
            ad9510_log.append("Valor Escrito: "+str(a_div_write[i])+" - Valor lido: "+str(a_div_read[i]))
            if(a_div_write[i]!=a_div_read[i]):
                ad9510_log.append("Fail Detected - Valor Escrito: "+str(a_div_write[i])+" - Valor lido: "+str(a_div_read[i]))
            
                print("Fail Detected - Valor Escrito: ",a_div_write[i]," Valor lido: ",a_div_read[i])
                check_a_div=check_a_div+1
            i=i+1
    
        if (check_a_div==0):
            print("A_DIV TEST: OK")
            ad9510_log.append("A_DIV TEST: OK")
        else:
            print("A_DIV TEST: FAIL")
            ad9510_log.append("A_DIV TEST: FAIL")
        
        print("Fim do Teste do A_DIV")
        ad9510_log.append("Fim do Teste do A_DIV\n")
        
        end_a_div_time=datetime.datetime.now()
        end_a_div_time_str=end_a_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("end_a_div_time: ",end_a_div_time_str)
        duration_a_div=((end_a_div_time - start_a_div_time).total_seconds())/60 #desprezível
        print("Duração do Teste A_DIV [min]: ",round(duration_a_div,4))   
    
    else:
        print("A_DIV WILL NOT BE PERFORMED")
        ad9510_log.append("A_DIV WILL NOT BE PERFORMED\n")
        #FIXME: ESTA PARTE SÓ SERVE PARA DEBUG
        check_a_div=0
        ad9510_write_check=0
        ad9510_read_check=0

    
    #Teste do B_DIV
    if(B_DIV_RUN=="yes"):
        print("Iniciou o Teste do B_DIV")
        ad9510_log.append("Iniciou o Teste do B_DIV")
        start_b_div_time=datetime.datetime.now()
        start_b_div_time_str=start_b_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("start_b_div_time: ",start_b_div_time_str)
        i=B_DIV_MIN
        read_text="READ VALUE OF B_DIV: "
        write_text="WRITTEN VALUE OF B_DIV: "
        b_div_write=[]
        b_div_read=[]
        #Realiza a escrita e leitura no mesmo loop, pois a funcao ./THALES_ad9510_ctl realiza ambos os processos automaticamente
        while(i<B_DIV_MAX+1):
            command = "./THALES_ad9510_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -b_div "+str(i)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_value=command_stdout[len(command_stdout)-2].decode("utf-8")
            read_value=command_stdout[len(command_stdout)-1].decode("utf-8")
            write_aux=str(write_value).replace(write_text,"")
            read_aux=str(read_value).replace(read_text,"")
            b_div_write.append(write_aux)
            b_div_read.append(read_aux)
            #print(write_aux)
            #print(read_aux)
            
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
    
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1  
                
            tela_leds.ui.progressBar.setValue((i+B_DIV_MIN)*40/B_DIV_MAX)  
            tela_leds.repaint()
            QApplication.processEvents() 
                
            i=i+1
    
        #Teste de verificação
        print("Verificando resultado...")
        i=0
        check_b_div=0
        while (i<B_DIV_MAX-B_DIV_MIN+1):
            ad9510_log.append("Valor Escrito: "+str(b_div_write[i])+" - Valor lido: "+str(b_div_read[i]))
            if(b_div_write[i]!=b_div_read[i]):
                print("Fail Detected - Valor Escrito: ",b_div_write[i]," Valor lido: ",b_div_read[i])
                ad9510_log.append("Fail Detected - Valor Escrito: "+str(b_div_write[i])+" - Valor lido: "+str(b_div_read[i]))
                check_b_div=check_b_div+1
            i=i+1
            
        if (check_b_div==0):
            print("B_DIV TEST: OK")
            ad9510_log.append("B_DIV TEST: OK")
        else:
            print("B_DIV TEST: FAIL")
            ad9510_log.append("B_DIV TEST: FAIL")
        
        print("Fim do Teste do B_DIV")
        ad9510_log.append("Fim do Teste do B_DIV\n")
        end_b_div_time=datetime.datetime.now()
        end_b_div_time_str=end_b_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("end_b_div_time: ",end_b_div_time_str)
        duration_b_div=((end_b_div_time - start_b_div_time).total_seconds())/60 #demora 4.5 minutos
        print("Duração do Teste B_DIV [min]: ",round(duration_b_div,4))   
        
    else:
        print("B_DIV WILL NOT BE PERFORMED")
        ad9510_log.append("B_DIV WILL NOT BE PERFORMED\n")
        #FIXME: ESTA PARTE SÓ SERVE PARA DEBUG
        check_b_div=0
        ad9510_write_check=0
        ad9510_read_check=0
    
    tela_leds.ui.progressBar.setValue(40)  
    tela_leds.repaint()
    QApplication.processEvents()     
    
    
    #Teste do R_DIV
    if(R_DIV_RUN=="yes"):
        print("Iniciou o Teste do R_DIV")
        ad9510_log.append("Iniciou o Teste do R_DIV")
        start_r_div_time=datetime.datetime.now()
        start_r_div_time_str=start_r_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("start_r_div_time: ",start_r_div_time_str)
        i=R_DIV_MIN
        read_text="READ VALUE OF R_DIV: "
        write_text="WRITTEN VALUE OF R_DIV: "
        r_div_write=[]
        r_div_read=[]
        #Realiza a escrita e leitura no mesmo loop, pois a funcao ./THALES_ad9510_ctl realiza ambos os processos automaticamente
        while(i<R_DIV_MAX+1):
            command = "./THALES_ad9510_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -r_div "+str(i)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_value=command_stdout[len(command_stdout)-2].decode("utf-8")
            read_value=command_stdout[len(command_stdout)-1].decode("utf-8")
            write_aux=str(write_value).replace(write_text,"")
            read_aux=str(read_value).replace(read_text,"")
            r_div_write.append(write_aux)
            r_div_read.append(read_aux)
            #print(write_aux)
            #print(read_aux)
            #print(i+1," de ", R_DIV_MAX," ",read_aux)
            
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
    
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1  
                
            tela_leds.ui.progressBar.setValue((i+R_DIV_MIN)*60/R_DIV_MAX+40)  
            tela_leds.repaint()
            QApplication.processEvents() 
                
            i=i+1
    
        #Teste de verificação
        print("Verificando resultado...")
        i=0
        check_r_div=0
        while (i<R_DIV_MAX-R_DIV_MIN+1):
            ad9510_log.append("Valor Escrito: "+str(r_div_write[i])+" - Valor lido: "+str(r_div_read[i]))
            if(r_div_write[i]!=r_div_read[i]):
                ad9510_log.append("Fail Detected - Valor Escrito: "+str(r_div_write[i])+" - Valor lido: "+str(r_div_read[i]))
                print("Fail Detected - Valor Escrito: "+str(r_div_write[i])+" - Valor lido: "+str(r_div_read[i]))
                check_r_div=check_r_div+1
            i=i+1
            
        if (check_r_div==0):
            print("R_DIV TEST: OK")
            ad9510_log.append("R_DIV TEST: OK")
        else:
            print("R_DIV TEST: FAIL")
            ad9510_log.append("R_DIV TEST: FAIL")
        
        print("Fim do Teste do R_DIV")
        ad9510_log.append("Fim do Teste do R_DIV\n")
        end_r_div_time=datetime.datetime.now()
        end_r_div_time_str=end_r_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("end_r_div_time: ",end_r_div_time_str)
        duration_r_div=((end_r_div_time - start_r_div_time).total_seconds())/60
        print("Duração do Teste R_DIV [min]: ",round(duration_r_div,4))  #8.7 minutos 
        
    else:
        print("R_DIV WILL NOT BE PERFORMED")
        ad9510_log.append("R_DIV WILL NOT BE PERFORMED\n")
        #FIXME: ESTA PARTE SÓ SERVE PARA DEBUG
        check_r_div=0
        ad9510_write_check=0
        ad9510_read_check=0
    
   
    #Teste do PRESCALER_DIV
    if(PRESCALER_DIV_RUN=="yes"):
        print("Iniciou o Teste do PRESCALER_DIV")
        ad9510_log.append("Iniciou o Teste do PRESCALER_DIV")
        start_prescaler_div_time=datetime.datetime.now()
        start_prescaler_div_time_str=start_prescaler_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("start_prescaler_div_time: ",start_prescaler_div_time_str)
        i=PRESCALER_DIV_MIN
        read_text="READ VALUE OF PRESCALER_DIV: "
        write_text="WRITTEN VALUE OF PRESCALER_DIV: "
        prescaler_div_write=[]
        prescaler_div_read=[]
        #Realiza a escrita e leitura no mesmo loop, pois a funcao ./THALES_ad9510_ctl realiza ambos os processos automaticamente
        while(i<PRESCALER_DIV_MAX+1):
            command = "./THALES_ad9510_ctl -b tcp://"+str(IP_CRATE)+":8978 -board "+str(POSITION_CRATE)+" -halcs "+str(POSITION_ADC)+" -prescaler_div "+str(i)
            command_stdout = Popen(local+command,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
            command_stdout=command_stdout.splitlines()
            write_value=command_stdout[len(command_stdout)-2].decode("utf-8")
            read_value=command_stdout[len(command_stdout)-1].decode("utf-8")
            write_aux=str(write_value).replace(write_text,"")
            read_aux=str(read_value).replace(read_text,"")
            prescaler_div_write.append(write_aux)
            prescaler_div_read.append(read_aux)
            #print(write_aux)
            #print(read_aux)
            #print(i+1," de ", R_DIV_MAX," ",read_aux)
            
            #Verifica se foi capaz de enviar comandos através do método de escrita
            write_verification_aux=command_stdout[len(command_stdout)-4].decode("utf-8")
            write_verification_aux=write_verification_aux.replace(write_verification_text,"")
            if (write_verification_aux!=str(0)):
                ad9510_write_check=ad9510_write_check+1
    
            #Verifica se foi capaz de enviar comandos através do método de leitura
            read_verification_aux=command_stdout[len(command_stdout)-3].decode("utf-8")
            read_verification_aux=read_verification_aux.replace(read_verification_text,"")
            if (read_verification_aux!=str(0)):
                ad9510_read_check=ad9510_read_check+1  
                
            i=i+1
    
        #Teste de verificação
        print("Verificando resultado...")
        i=0
        check_prescaler_div=0
        while (i<PRESCALER_DIV_MAX-PRESCALER_DIV_MIN+1):
            ad9510_log.append("Valor Escrito: "+str(prescaler_div_write[i])+" - Valor lido: "+str(prescaler_div_read[i]))
            if(prescaler_div_write[i]!=prescaler_div_read[i]):
                ad9510_log.append("Fail Detected -Valor Escrito: "+str(prescaler_div_write[i])+" - Valor lido: "+str(prescaler_div_read[i]))
                print("Fail Detected - Valor Escrito: ",prescaler_div_write[i]," Valor lido: ",prescaler_div_read[i])
                check_prescaler_div=check_prescaler_div+1
            i=i+1
            
        if (check_prescaler_div==0):
            print("PRESCALER_DIV TEST: OK")
            ad9510_log.append("PRESCALER_DIV TEST: OK")
        else:
            print("PRESCALER_DIV TEST: FAIL")
            ad9510_log.append("PRESCALER_DIV TEST: FAIL")
        
        print("Fim do Teste do PRESCALER_DIV")
        ad9510_log.append("Fim do Teste do PRESCALER_DIV\n")
        end_prescaler_div_time=datetime.datetime.now()
        end_prescaler_div_time_str=end_prescaler_div_time.strftime("%Y-%m-%d %H:%M:%S")
        print("end_prescaler_div_time: ",end_prescaler_div_time_str)
        duration_prescaler_div=((end_prescaler_div_time - start_prescaler_div_time).total_seconds())/60
        print("Duração do Teste PRESCALER_DIV [min]: ",round(duration_prescaler_div,4))  #desprezível 
        
    else:
        print("PRESCALER_DIV WILL NOT BE PERFORMED")
        ad9510_log.append("PRESCALER_DIV WILL NOT BE PERFORMED\n")
        #FIXME: ESTA PARTE SÓ SERVE PARA DEBUG
        check_prescaler_div=0
        ad9510_write_check=0
        ad9510_read_check=0
    

    if (check_pll_clk_sel==0 and check_a_div==0 and check_b_div==0 and check_prescaler_div == 0 and check_r_div ==0):
        ad9510_result="OK"
        print("AD9510 OK")
    else:
        ad9510_result="FAIL"
        print("AD9510 FAIL")
        
    if(ad9510_write_check!=0):
        ad9510_write_check_result = "FAIL"
        print("Utilizacao do método de Escrita: ",ad9510_write_check_result)
    else:
        ad9510_write_check_result = "OK"  
        print("Utilizacao do método de Escrita: ",ad9510_write_check_result)
 
    if(ad9510_read_check!=0):
        ad9510_read_check_result = "FAIL"
        print("Utilizacao do método de Leitura: ",ad9510_read_check_result)
    else:
        ad9510_read_check_result = "OK"  
        print("Utilizacao do método de Leitura: ",ad9510_read_check_result)  

    ad9510_log.append("Utilizacao do método de Escrita: "+str(ad9510_write_check_result))
    ad9510_log.append("Utilizacao do método de Leitura: "+str(ad9510_read_check_result))
    ad9510_log.append("FINAL RESULT: "+str(ad9510_result))
    end_time=datetime.datetime.now()
    duracao=((end_time - start_time).total_seconds())/60
    print("Duração do Teste: ",round(duracao,4))
    
    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents()    


    return (ad9510_result,ad9510_write_check_result,ad9510_read_check_result,ad9510_log)