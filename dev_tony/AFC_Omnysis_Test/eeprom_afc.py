from subprocess import PIPE, Popen
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def eeprom_afc(tela_leds,ip_crate):

    tela_leds.ui.progressBar.setValue(0)  
    tela_leds.repaint()
    QApplication.processEvents()

    #escrita!
    print("Iniciou o processo de Escrita!")
    posicao_memoria=[]
    valor_escrito=[]
    posicao_memoria_str=[]
    i=0
    while (i<256):
        posicao_memoria.append(format(i,'02x'))
        valor_escrito.append(format(i,'02x'))
        posicao_memoria_str.append("0x"+posicao_memoria[i])
        comando1="ipmitool -I lan -H "+str(ip_crate)+" -P '' -T 0x82 -m 0x20 -t 0x76 raw 0x30 0x00 0x03 0x00 0x08 0x02 0x"+str(valor_escrito[i])+" 0x"+str(valor_escrito[i])+""
        #teste manual de escrita  "  ipmitool -I lan -H 10.0.18.14 -P '' -T 0x82 -m 0x20 -t 0x76 raw 0x30 0x00 0x03 0x00 0x08 0x10 0x02 0x0f  "
        #teste manual de leitura!  " ipmitool -I lan -H 10.0.18.14 -P '' -T 0x82 -m 0x20 -t 0x76 raw 0x30 0x00 0x03 0x00 0x08 0x01 0x02 0x10 "
        command_stdout = Popen(comando1,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()

        tela_leds.ui.progressBar.setValue((i+1)*70/256)  
        tela_leds.repaint()
        QApplication.processEvents()  

        i=i+1
        
    print("Fim da Escrita")
    
    #Padrao a comparar com a memoria   
    comando_enviado=[]
    j=0
    while(j<241):
        posicao_memoria=" "+valor_escrito[0+j]+" "+valor_escrito[1+j]+" "+valor_escrito[2+j]+" "+valor_escrito[3+j]+" "+valor_escrito[4+j]+" "+valor_escrito[5+j]+" "+valor_escrito[6+j]+" "+valor_escrito[7+j]+" "+valor_escrito[8+j]+" "+valor_escrito[9+j]+" "+valor_escrito[10+j]+" "+valor_escrito[11+j]+" "+valor_escrito[12+j]+" "+valor_escrito[13+j]+" "+valor_escrito[14+j]+" "+valor_escrito[15+j]
        comando_enviado.append(posicao_memoria)
        j=j+16
    
    
    print("Iniciou o processo de LEITURA!")
    #leitura!
    c=[]
    resultado_lido=[]
    f=0
    i=0
    while (i<16):
        c.append(format(f,'02x'))
        comando1="ipmitool -I lan -H "+str(ip_crate)+" -P '' -T 0x82 -m 0x20 -t 0x76 raw 0x30 0x00 0x03 0x00 0x08 0x01 0x"+str(c[i])+" 0x10"
        command_stdout = Popen(comando1,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
        command_stdout=command_stdout.splitlines()
        s1 = command_stdout.pop(1).decode("utf-8")
        teste=str(command_stdout).replace("[","")
        teste=str(teste).replace("]","")
        teste=str(teste).replace("'","")
        teste=teste[4:]
        resultado_lido.append(str(teste)+str(s1))
        i=i+1
        f=f+16
        tela_leds.ui.progressBar.setValue((i+1)*30/16+70)  
        tela_leds.repaint()
        QApplication.processEvents()
    print("Fim da Leitura")
    
    
    aux_lido=[]
    for i in range (0,len(resultado_lido)):
        aux_lido.append(resultado_lido[i].split())
    
    valores_lidos=[]
    for i in range (0,len(aux_lido)):
        for j in range (0, len(aux_lido[i])):
            valores_lidos.append(aux_lido[i][j])
    
    aux_escrito_padrao=[]
    for i in range (0,len(comando_enviado)):
        aux_escrito_padrao.append(comando_enviado[i].split())
    
    valores_escrito_padrao=[]
    for i in range (0,len(aux_escrito_padrao)):
        for j in range (0, len(aux_escrito_padrao[i])):
            valores_escrito_padrao.append(aux_escrito_padrao[i][j])   
    
    eeprom_total_valores=len(valores_escrito_padrao)
    eeprom_valores_problemas=0
    
    if(resultado_lido==comando_enviado):
        print("MEMORY TEST SUCCESS!")
        eeprom_afc_aprovacao="OK"
        eeprom_afc_result="EEPROM_AFC - RESULTADO DO TESTE: OK"
    else:
        print("MEMORY TEST FAILED!")
        eeprom_afc_aprovacao="FAIL"
        eeprom_afc_result="EEPROM_AFC - RESULTADO DO TESTE: FAIL"
        for i in range (0, eeprom_total_valores):
            if(valores_escrito_padrao[i]!=valores_lidos[i]):
                eeprom_valores_problemas=eeprom_valores_problemas+1
    
    eeprom_valores_corretos= eeprom_total_valores-eeprom_valores_problemas     
        
        
    if (eeprom_afc_aprovacao=="OK"):
        tela_leds.ui.kled_EEPROM.setState(1)
        tela_leds.ui.kled_EEPROM.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led EEPROM_AFC",tela_leds.repaint())
        print("Led EEPROM_AFC",QApplication.processEvents())
    else:
        tela_leds.ui.kled_EEPROM.setState(1)
        tela_leds.ui.kled_EEPROM.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led EEPROM_AFC",tela_leds.repaint())
        print("Led EEPROM_AFC",QApplication.processEvents())
        
    tela_leds.ui.progressBar.setValue(100)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    #print("Memória Acessada")
    #print(posicao_memoria_str)
    #print("Valores Escritos")
    #print(valores_escrito_padrao)
    #print("Valores Lidos")
    #print(valores_lidos)

    return (eeprom_afc_aprovacao,eeprom_afc_result,eeprom_total_valores,eeprom_valores_corretos,eeprom_valores_problemas,posicao_memoria_str,valores_escrito_padrao,valores_lidos)
