from subprocess import Popen, PIPE
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def sensores_ipmi(tela_leds):
    #executa o pyimpi criado na versão py
    
    tela_leds.ui.progressBar.setValue(0)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    local = "cd IPMI_PY27/criado_pyinstaller_py27/dist/ipmi_py27\n"
    comando = "./ipmi_py27"
    command_stdout = Popen(local+comando,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()
    
    print(command_stdout)

    tela_leds.ui.progressBar.setValue(90)  
    tela_leds.repaint()
    QApplication.processEvents()
    
    if (len(command_stdout)<1):
        sensores_ipmi_aprovacao="FAIL"
        sensores_ipmi_result="SENSORES IPMI - RESULTADO DO TESTE: FAIL"
    else:
        sensores_ipmi_aprovacao="OK"
        sensores_ipmi_result="SENSORES IPMI - RESULTADO DO TESTE: OK"    
    i=0
    cont=0
    outputs=[]
    
    while (i<len(command_stdout)):
        if(str(command_stdout[i].decode("utf-8"))!=""):
            outputs.append(command_stdout[i].decode("utf-8"))
            cont=cont+1
        i=i+1
    
    sensores_ipmi_data_type=[]
    sensores_ipmi_data_value=[]
    sensores_ipmi_data_units=[]
    sensores_ipmi_medicao=[]
    text_reading_type_aux="Reading Type: "
    text_reading_value_aux="Reading Value: "
    text_reading_units_aux="Reading Units: "
    
    i=0
    for i in range (0,len(outputs)-2,3):
        sensores_ipmi_data_type.append(outputs[i].replace(text_reading_type_aux,""))
        sensores_ipmi_data_value.append(outputs[i+1].replace(text_reading_value_aux,""))
        sensores_ipmi_data_units.append(outputs[i+2].replace(text_reading_units_aux,""))
    
    i=0
    for i in range (0,len(sensores_ipmi_data_type)):    
        sensores_ipmi_medicao.append(i+1)
        
    tela_leds.ui.progressBar.setValue(100)  
    
    if (sensores_ipmi_aprovacao=="OK"):
        tela_leds.ui.kled_SENSORES_IPMI.setState(1)
        tela_leds.ui.kled_SENSORES_IPMI.setColor(QtGui.QColor(0, 255, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led SENSORES_IPMI",tela_leds.repaint())
        print("Led SENSORES_IPMI",QApplication.processEvents())
    else:
        tela_leds.ui.kled_SENSORES_IPMI.setState(1)
        tela_leds.ui.kled_SENSORES_IPMI.setColor(QtGui.QColor(255, 0, 0))
        tela_leds.repaint()
        QApplication.processEvents()
        print("Led SENSORES_IPMI",tela_leds.repaint())
        print("Led SENSORES_IPMI",QApplication.processEvents())
    
    return(sensores_ipmi_data_type,sensores_ipmi_data_value,sensores_ipmi_data_units,sensores_ipmi_medicao,sensores_ipmi_aprovacao,sensores_ipmi_result)

