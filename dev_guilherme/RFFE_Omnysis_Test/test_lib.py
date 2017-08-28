from rffe_test_lib import AgilentE5061B
import time

SLEEP_TIME = 0.5

def list_to_file(self, data, filename):
    length=len(data)
    file = open(str(filename), "w")
    for i in range (0,length):
        str1 = ''.join(str(data[i]))
        str1=str1.replace("]], ","");
        str1=str1.replace("[","");
        str1=str1.replace("]","");
        str1=str1.replace(",","");
        str1=str1.replace(")","");
        str1=str1.replace("(","");
        str1=str1.replace("'","");
        str1=str1.replace("\n"," ");
        file.write(str1+"\n")
    file.close()
    
def list_to_file_aux(self, data, filename):
    length=len(data)
    file = open(str(filename), "w")
    for i in range (0,length):
        str1 = ''.join(str(data[i]))
        file.write(str1+"\n")
    file.close()

def marker_value(self, frequency, s_param, interface):
    vna=interface
    if s_param=="s11":
        s11=vna.get_s11_data()
    elif s_param=="s12":
        s12=vna.get_s12_data()
    elif s_param=="s21":
        s21=vna.get_s21_data()
    elif s_param=="s22":
        s22=vna.get_s22_data()
    vna.send_command(b":CALC1:MARK1:X " + format(frequency).encode('utf-8') + b"\n")
    time.sleep(SLEEP_TIME)
    vna.send_command(b":CALC1:MARK1:Y?\n")
    response=vna.get_answer()
    index = response.find(b',')
    response = response[:index].strip()
    return(response)

#NETWORK ANALYZER

#remover este após as correções
def set_vna2(self, freq_center, freq_span, freq_start, freq_stop, autoscale, interface):
    ##frequency in MHz, Span in MHz, and autoscale =0 or autoscale =1.
    vna=interface
    vna.send_command(b":SENS1:FREQ:CENT " + format(freq_center).encode('utf-8') + b"\n")  
    vna.send_command(b":SENS1:FREQ:SPAN " + format(freq_span).encode('utf-8') + b"\n")
    vna.send_command(b":SENS1:FREQ:STAR " + format(freq_start).encode('utf-8') + b"\n")
    vna.send_command(b":SENS1:FREQ:STOP " + format(freq_stop).encode('utf-8') + b"\n")
    if autoscale == 1:
        vna.send_command(b":DISP:WIND1:TRAC1:Y:AUTO\n")#isso ainda não foi feito
    return

#NETWORK ANALYZER
def set_vna(self, freq_center, freq_span, autoscale, interface):
    ##frequency in MHz, Span in MHz, and autoscale =0 or autoscale =1.
    vna=interface
    vna.send_command(b":SENS1:FREQ:CENT " + format(freq_center).encode('utf-8') + b"\n")  
    vna.send_command(b":SENS1:FREQ:SPAN " + format(freq_span).encode('utf-8') + b"\n")
    if autoscale == 1:
        vna.send_command(b":DISP:WIND1:TRAC1:Y:AUTO\n")#isso ainda não foi feito
    return