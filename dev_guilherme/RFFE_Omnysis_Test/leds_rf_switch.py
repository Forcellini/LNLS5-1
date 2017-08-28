from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication

def leds_rf_switch (sw1_port_1,sw1_port_2,sw2_port_1,sw2_port_2,tela_leds):
    
    
    #Verifica o led do switch 1 lado A
    if(sw1_port_1==1):
        tela_leds.ui.kled_CH1_A_SWITCH1.setState(1)
        tela_leds.ui.kled_CH2_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH1.setState(0)
    elif (sw1_port_1==2):
        tela_leds.ui.kled_CH1_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH1.setState(1)
        tela_leds.ui.kled_CH3_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH1.setState(0)
    elif (sw1_port_1==3):
        tela_leds.ui.kled_CH1_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH1.setState(1)
        tela_leds.ui.kled_CH4_A_SWITCH1.setState(0)
    elif (sw1_port_1==4):
        tela_leds.ui.kled_CH1_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH1.setState(1)
    elif (sw1_port_1==0):
        tela_leds.ui.kled_CH1_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH1.setState(0)
    
     
    #Verifica o led do switch 1 lado B   
    if(sw1_port_2==1):
        tela_leds.ui.kled_CH1_B_SWITCH1.setState(1)
        tela_leds.ui.kled_CH2_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH1.setState(0)
    elif (sw1_port_2==2):
        tela_leds.ui.kled_CH1_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH1.setState(1)
        tela_leds.ui.kled_CH3_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH1.setState(0)
    elif (sw1_port_2==3):
        tela_leds.ui.kled_CH1_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH1.setState(1)
        tela_leds.ui.kled_CH4_B_SWITCH1.setState(0)
    elif (sw1_port_2==4):
        tela_leds.ui.kled_CH1_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH1.setState(0)
    elif (sw1_port_2==0):
        tela_leds.ui.kled_CH1_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH1.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH1.setState(0)
        
        
    #Verifica o led do switch 2 lado A
    if(sw2_port_1==1):
        tela_leds.ui.kled_CH1_A_SWITCH2.setState(1)
        tela_leds.ui.kled_CH2_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH2.setState(0)
    elif (sw2_port_1==2):
        tela_leds.ui.kled_CH1_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH2.setState(1)
        tela_leds.ui.kled_CH3_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH2.setState(0)
    elif (sw2_port_1==3):
        tela_leds.ui.kled_CH1_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH2.setState(1)
        tela_leds.ui.kled_CH4_A_SWITCH2.setState(0)
    elif (sw2_port_1==4):
        tela_leds.ui.kled_CH1_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH2.setState(1)
    elif (sw2_port_1==0):
        tela_leds.ui.kled_CH1_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_A_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_A_SWITCH2.setState(0)    

    #Verifica o led do switch 2 lado B    
    if(sw2_port_2==1):
        tela_leds.ui.kled_CH1_B_SWITCH2.setState(1)
        tela_leds.ui.kled_CH2_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH2.setState(0)
    elif (sw2_port_2==2):
        tela_leds.ui.kled_CH1_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH2.setState(1)
        tela_leds.ui.kled_CH3_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH2.setState(0)
    elif (sw2_port_2==3):
        tela_leds.ui.kled_CH1_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH2.setState(1)
        tela_leds.ui.kled_CH4_B_SWITCH2.setState(0)
    elif (sw2_port_2==4):
        tela_leds.ui.kled_CH1_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH2.setState(1)
    elif (sw2_port_2==0):
        tela_leds.ui.kled_CH1_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH2_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH3_B_SWITCH2.setState(0)
        tela_leds.ui.kled_CH4_B_SWITCH2.setState(0)    
    
    tela_leds.repaint()
    QApplication.processEvents()
    print("Led switch chave rf",tela_leds.repaint())
    print("Led switch chave rf",QApplication.processEvents())
    
    
    