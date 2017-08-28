from rffe_test_lib import RFFEControllerBoard

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def temperature_test(rffe,temp_min,temp_max,temperature_test_log,tela_leds):
    
    
    print("\nRunning Temperature test ... \n")
    

    tela_leds.ui.progressBar.setValue(5)   
    tela_leds.repaint()
    QApplication.processEvents()
    print("barra temp",tela_leds.repaint())
    print("barra temp",QApplication.processEvents())
        
    #Data aquisition
    temperature=[]
    
    i=0
    while (i<5):
        aux=rffe.get_temp1()
        fail=0
        if (aux < 5 or aux >100):
            aux = rffe.get_temp2()
            if (aux < 5 or aux > 100):
                fail=fail+1
        temperature.append(round(aux,2))
        
        tela_leds.ui.progressBar.setValue((i+1)*100/5)   
        tela_leds.repaint()
        QApplication.processEvents()
        print("barra temp",tela_leds.repaint())
        print("barra temp",QApplication.processEvents())
        
        i=i+1

    #Calculations and Results
    for i in range (0, len(temperature)):
    
        if (temperature[i]<temp_min or temperature[i]>temp_max):
            fail=fail+1
    
    
    espacamento=15
    
    temperature_test_log.append("Measurement".ljust(espacamento)+"Temperature [°C]".ljust(espacamento))
    for i in range (0,len(temperature)):
        temperature_test_log.append(str(i+1).ljust(espacamento)+str(temperature[i]).ljust(espacamento))
    
    if (fail!=0):
        temp_test="Temperature Measurement Test: FAILED"
        print("Temperature Measurement Test: FAILED")
        print("Result: ", temperature)
    else:
        temp_test="Temperature Measurement Test: OK"
        print("Temperature Measurement Test: OK")
        print("Result: ", temperature)  
        
    temperature_test_log.append(temp_test)  
    
    return (temperature,temperature_test_log,fail)

 


