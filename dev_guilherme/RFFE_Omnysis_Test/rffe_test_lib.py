#!/usr/bin/python3
# -*- coding: utf-8 -*-


# This library requires pySerial and other modules.

from scipy.interpolate import interp1d
import numpy
import serial
import socket
import struct
import time
import urllib.request

####################################################################################################
#
# Begin of configuration section
#
####################################################################################################

# Interval time for waiting between changing the vector network analyzer setup and reading data from
# it. Ideally, this sould be close to the network analyzer sweep time.

SLEEP_TIME = 1

###########urllib.request#########################################################################################
#
# End of configuration section
#
####################################################################################################


####################################################################################################
#
#
# This comment block contains notes about the development process of this library.
#
#
# Regarding class RFFEControllerBoard, methods listed below seems coded correctly, but none of them
# works. The RF front-end controller board always returns only one value of temperature: 0.0 °C.
# Tests revealed that the board has some hardware problem which makes the temperature read always
# equal to zero.
#
# get_temp1()
# get_temp2()
#
#
####################################################################################################

#SWITCH

class RF_switch_board_1:
    """Class used to send commands for the RF switch board."""
    
    def __init__(self, ip):
        """Class constructor. Here the socket connection to the board is initialized. The argument
        required is the IP adress of the instrument (string)."""
        rfsw_address = ((ip, 80))
        self.rfsw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rfsw_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.rfsw_socket.settimeout(5.0)
        self.rfsw_socket.connect(rfsw_address)
        #time.sleep(SLEEP_TIME)
        return

    def sw1_pos(self, ip, posChA_sw1, posChB_sw1):
        addr=urllib.request.urlopen("http://"+str(ip)+"/:SP4TA:STATE:"+str(posChA_sw1))
        addr=urllib.request.urlopen("http://"+str(ip)+"/:SP4TB:STATE:"+str(posChB_sw1))
        time.sleep(SLEEP_TIME)
        return

    def close_connection(self):
        """Close the serial connection to the mbed device."""
        self.rfsw_socket.close()
        return

class RF_switch_board_2:
    """Class used to send commands for the RF switch board."""
    
    def __init__(self, ip):
        """Class constructor. Here the socket connection to the board is initialized. The argument
        required is the IP adress of the instrument (string)."""
        rfsw_address = ((ip, 80))
        self.rfsw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rfsw_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.rfsw_socket.settimeout(5.0)
        self.rfsw_socket.connect(rfsw_address)
        #time.sleep(SLEEP_TIME)
        return

    def sw2_pos(self, ip, posChA_sw2, posChB_sw2):
        addr=urllib.request.urlopen("http://"+str(ip)+"/:SP4TA:STATE:"+str(posChA_sw2))
        addr=urllib.request.urlopen("http://"+str(ip)+"/:SP4TB:STATE:"+str(posChB_sw2))
        time.sleep(SLEEP_TIME)
        
        return

    def close_connection(self):
        """Close the serial connection to the mbed device."""
        self.rfsw_socket.close()
        return

#GERADOR DE SINAIS
class Agilent33521A:
    def __init__(self,ip):
        sgen_address = ((ip, 5025))
        self.sgen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sgen_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sgen_socket.settimeout(5.0)
        self.sgen_socket.connect(sgen_address)
        #time.sleep(SLEEP_TIME)

    def set_impedance(self,impedance):
        #self.sgen_socket.send("OUTPUT1:LOAD " + str(impedance) + "\n")
        self.sgen_socket.send("OUTPUT:LOAD " + str(impedance) + "\n")
        return

    def set_offset(self,offset):
        #self.sgen_socket.send("SOURCE1:VOLT:OFFSET " + str(offset) + "\n")
        self.sgen_socket.send(b"SOUR1:VOLT:OFFS " + format(offset).encode('utf-8') + b"\n")
        return

    def set_frequency(self,frequency):
        #self.sgen_socket.send("SOURCE1:FREQUENCY " + str(frequency) + "\n")
        self.sgen_socket.send(b"SOUR1:FREQ " + format(frequency).encode('utf-8') + b"\n") 
        return

    def set_unit(self,unit):
        self.sgen_socket.send("SOURCE1:VOLT:UNip_sw2IT " + str(unit) + "\n")
        return
    
    def set_signal_DC(self):
        self.sgen_socket.send(b"SOUR1:FUNC DC\n")
        return    

    def close_connection(self):
        self.sgen_socket.close()
        return
#verificar como o 0 volts é utilizado realmente no teste
    def set_pos(self, pos):
        #direct position
        if pos == "direct":
            #self.sgen_socket.send("VOLT:OFFS 3\n")
            self.sgen_socket.send(b"SOUR1:VOLT:OFFS 3\n")
            self.sgen_socket.send(b"OUTP1 ON\n")
        #inverted position
        elif pos == "inverted":
            #self.sgen_socket.send("SOURCE1:VOLT:OFFSET 0\n")
            self.sgen_socket.send(b"SOUR1:VOLT:OFFS 0\n")
            
#NETWORK ANALYZER
class AgilentE5061B:
    """Class used to send commands and acquire data from the Agilent E5061B vector network analyzer.
    """

    def __init__(self, ip):
        """Class constructor. Here the socket connection to the instrument is initialized. The
        argument required, a string, is the IP adress of the instrument."""
        vna_address = ((ip, 5025))
        self.vna_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.vna_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.vna_socket.settimeout(5.0)
        self.vna_socket.connect(vna_address)
        #self.vna_socket.send(b":DISP:WIND1:TRAC1:Y:RLEV -40\n")
        #self.vna_socket.send(b":DISP:WIND1:TRAC1:Y:PDIV 15\n")
        #elf.vna_socket.send(b":SENS1:SWE:TIME:AUTO ON\n")
        #self.vna_socket.send(b":SENS1:SWE:POIN 1601\n") # sets numbers of point for the curve
        #self.vna_socket.send(b":SENS1:SWE:TYPE LIN\n") # type curve
        #self.vna_socket.send(b":SOUR1:POW:ATT 30\n")
        #self.vna_socket.send(b":SOUR1:POW -25\n")
        self.vna_socket.send(b":DISP:WIND:TRAC:Y:RLEV -40\n")
        self.vna_socket.send(b":DISP:WIND:TRAC:Y:PDIV 15\n")
        self.vna_socket.send(b":SENS:SWE:TIME:AUTO ON\n")
        self.vna_socket.send(b":SENS:SWE:POIN 1601\n") # sets numbers of point for the curve
        self.vna_socket.send(b":SENS:SWE:TYPE LIN\n") # type curve
        self.vna_socket.send(b":SOUR:POW:ATT 30\n")
        self.vna_socket.send(b":SOUR:POW -25\n")

        #time.sleep(SLEEP_TIME)
    
    def set_power_range(self,power_range):
        
        if (power_range <= -30 ):
            self.vna_socket.send(b":SOUR1:POW:ATT 40\n")
        elif (power_range >-30 and power_range <=-20 ):
            self.vna_socket.send(b":SOUR1:POW:ATT 30\n")
        elif (power_range >-20 and power_range<=-10):
            self.vna_socket.send(b":SOUR1:POW:ATT 20\n")
            #print("Potência de Entrada do VNA maior que -20dB. Este cenário não é executado por medidas de segurança")
        elif (power_range >-10 and power_range<=0):
            #print("Potência de Entrada do VNA maior que -10dB. Este cenário não é executado por medidas de segurança")
            self.vna_socket.send(b":SOUR1:POW:ATT 10\n")
          
        return 
 
    def get_answer(self):
        
        """Get the instrument's answer after sending a command. It is returned as a string of bytes.
        """
        data = b""
        while (data[len(data) - 1:] != b"\n"):
            data += self.vna_socket.recv(5025)
        return(data)

    def get_frequency_data(self):
        """Get the list of frequencies of the instrument sweep, returning a sequence of floating
           point numbers."""
        #self.vna_socket.send(b":SENS1:FREQ:DATA?\n")
        self.vna_socket.send(b":SENS1:FREQ:DATA?\n")
        
        frequency_data = b""
        while (frequency_data[len(frequency_data) - 1:] != b"\n"):
            frequency_data += self.vna_socket.recv(5025)
        frequency_data = frequency_data[:len(frequency_data) - 1].split(b",")
        frequency_data = [float(i) for i in frequency_data]
        return(frequency_data)

    def get_s11_data(self):
        """Get the S11 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.send(b":CALC1:PAR1:DEF S11\n")
        time.sleep(SLEEP_TIME)
        self.vna_socket.send(b":CALC1:DATA:FDAT?\n")
        #self.vna_socket.send(b":CALC1:PAR:DEF test1, S11\n")
        #self.vna_socket.send(b":CALC1:PAR:SEL test1")
        #time.sleep(SLEEP_TIME)
        #self.vna_socket.send(b":CALC1:DATA? FDATA")
        s11_data = b""
        while (s11_data[len(s11_data) - 1:] != b"\n"):
            s11_data += self.vna_socket.recv(5025)
        s11_data = s11_data[:len(s11_data) - 1].split(b",")
        s11_data = s11_data[::2]
        s11_data = [round(float(i),2) for i in s11_data]
               
        return(s11_data)

    def get_s12_data(self):
        """Get the S12 trace data, returning a sequence of floating point numbers."""
        
        self.vna_socket.send(b":CALC1:PAR1:DEF S12\n")
        time.sleep(SLEEP_TIME)
        self.vna_socket.send(b":CALC1:DATA:FDAT?\n")
        #self.vna_socket.send(b":CALC1:PAR:DEF test2, S12\n")
        #time.sleep(SLEEP_TIME)
        #self.vna_socket.send(b":CALC1:DATA? FDATA")
        
        s12_data = b""
        while (s12_data[len(s12_data) - 1:] != b"\n"):
            s12_data += self.vna_socket.recv(5025)
        s12_data = s12_data[:len(s12_data) - 1].split(b",")
        s12_data = s12_data[::2]
        s12_data = [round(float(i),2) for i in s12_data]
        return(s12_data)

    def get_s21_data(self):
        """Get the S21 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.send(b":CALC1:PAR1:DEF S21\n")
        time.sleep(SLEEP_TIME)
        self.vna_socket.send(b":CALC1:DATA:FDAT?\n")
        #self.vna_socket.send(b":CALC1:PAR:DEF test3, S21\n")
        #time.sleep(SLEEP_TIME)
        #self.vna_socket.send(b":CALC1:DATA? FDATA")
        
        s21_data = b""
        while (s21_data[len(s21_data) - 1:] != b"\n"):
            s21_data += self.vna_socket.recv(5025)
        s21_data = s21_data[:len(s21_data) - 1].split(b",")
        s21_data = s21_data[::2]
        s21_data = [round(float(i),2) for i in s21_data]
        return(s21_data)

    def get_s22_data(self):
        """Get the S22 trace data, returning a sequence of floating point numbers."""
        self.vna_socket.send(b":CALC1:PAR1:DEF S22\n")
        time.sleep(SLEEP_TIME)
        self.vna_socket.send(b":CALC1:DATA:FDAT?\n")
        #self.vna_socket.send(b":CALC1:PAR:DEF test4, S22\n")
        #time.sleep(SLEEP_TIME)
        #self.vna_socket.send(b":CALC1:DATA? FDATA")
        
        s22_data = b""
        while (s22_data[len(s22_data) - 1:] != b"\n"):
            s22_data += self.vna_socket.recv(5025)
        s22_data = s22_data[:len(s22_data) - 1].split(b",")
        s22_data = s22_data[::2]
        s22_data = [round(float(i),2) for i in s22_data]
        return(s22_data)

    def set_marker_frequency(self,value):
        """set the center frequency of the VNA"""
        #self.vna_socket.send(b":CALC1:MARK1:X " + str(value) + b"\n")
        self.vna_socket.send(b":CALC1:DATA:FDAT?\n")
        return
    
    def set_avarage(self,value):
        """set the AVERAGE of the VNA"""
        time.sleep(5)
        
        #self.vna_socket.send(b":CALC1:MARK1:X " + str(value) + b"\n")
        self.vna_socket.send(b":SENSE1:AVER:COUN "+ str(value) + b"\n")
        self.vna_socket.send(b":SENSE1:AVER ON\n")
        return

    def check_avarage(self):
        """set the AVERAGE of the VNA"""
        #self.vna_socket.send(b":CALC1:MARK1:X " + str(value) + b"\n")
        time.sleep(SLEEP_TIME)
        self.vna_socket.send(b":SENS1:AVER:COUN?\n")
        #check=check.decode("utf-8")

        check = b""
        while (check[len(check) - 1:] != b"\n"):
            check += self.vna_socket.recv(5025)
        check = check[:len(check) - 1].split(b",")
        check = check[::2]
        check = [round(float(i),2) for i in check]
        print(check)
        
 
        return(check)

    def set_avarage_off(self,value):
        """set the AVERAGE of the VNA"""
        #self.vna_socket.send(b":CALC1:MARK1:X " + str(value) + b"\n")
        self.vna_socket.send(b":SENSE1:AVER OFF\n")
        return


    def get_marker_value(self,marker):
        """get the value of the marker 1 """
        
        self.vna_socket.send(b":CALC1:MARK" + str(marker) + ":Y?\n")
        
        ans=self.vna_socket.get_answer()
        #MUDEI A LINHA DE CIMA !!!!!
               
        index = ans.find(',')
        ans = ans[:index].strip()
        return(ans)

    def set_center_frequency(self,value):
        """set the center frequency of the VNA"""
       
        freq=int(value*1000000)
        self.vna_socket.send(":SENS1:FREQ:CENT " + str(freq) + "\n")
        return

    def set_span(self,value):
        """set the span of the VNA, in MHz"""
       
        freq=int(value*1000000)
        self.vna_socket.send(":SENS1:FREQ:SPAN " + str(freq) + "\n")
        return

    def send_command(self, text):
        """Sends a command to the instrument. The "text" argument must be a string of bytes."""
        self.vna_socket.send(text)
        time.sleep(SLEEP_TIME)
        return

    def set_power(self, power):
        self.vna_socket.send(b":SOUR1:POW" + str(power) + b"\n")
        return

    def close_connection(self):
        """Close the socket connection to the instrument."""
        self.vna_socket.close()


#FRONT END
class RFFEControllerBoard:
    """Class used to send commands and acquire data from the RF front-end controller board."""

    def __init__(self, ip):
        """Class constructor. Here the socket connection to the board is initialized. The argument
        required is the IP adress of the instrument (string)."""
        board_address = ((ip, 6791))
        self.board_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.board_socket.settimeout(5.0)
        self.board_socket.connect(board_address)
        time.sleep(SLEEP_TIME)
        

    def get_switching_mode(self):
        """This method returns the current switching mode. Its answers are one of the following
        integers:
        0: matched
        1: direct
        2: inverted
        3: switching"""
        self.board_socket.send(bytearray.fromhex("10 00 01 00"))
        temp = self.board_socket.recv(1024)
        return(temp[3])

    def set_switching_mode(self, mode):
        """Sets the switching mode of operation. The accepted arguments are the following integers:
        0: matched
        1: direct
        2: inverted
        3: switching
        Other arguments will be desconsidered."""
        if (mode in (0, 1, 2, 3)):
            #self.board_socket.send(bytes.fromhex("20 00 02 00 0" + str(mode)))
            self.board_socket.send(bytearray.fromhex("20 00 02 00 0" + str(mode)))
            temp = self.board_socket.recv(1024)

    def get_attenuator_value(self):
        """This method returns the current attenuation value (in dB) as a floating-point number.
           The attenuation value will be between 0 dB and 31.5 dB, with a 0.5 dB step size."""
        self.board_socket.send(bytearray.fromhex("10 00 01 00"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])
    

    def set_attenuator_value(self, value):
        """Sets the attenuation value of both front-ends. The argument should be a
        floating-point number representing the attenuation (in dB) between 0 dB and 31.5 dB, with a
        0.5 dB step size. Argument values other than these will be disconsidered."""
        #if (value in tuple(numpy.linspace(0, 31.5, 64))):
        self.board_socket.send(bytearray.fromhex("20 00 09 00") + struct.pack("<d", value))
        temp = self.board_socket.recv(1024)

    def get_temp1(self):
        """This method returns the temperature measured by the sensor present in the A/C
        front-end. The value returned is a floating-point number."""
        self.board_socket.send(bytearray.fromhex("10 00 01 01"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])

    def get_temp2(self):
        """This method returns the temperature measured by the sensor present in the B/D
        front-end. The value returned is a floating-point number."""
        self.board_socket.send(bytearray.fromhex("10 00 01 02"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])

    def get_temp1_setpoint(self):
        """This method returns the temperature set-point for the A/C front-end temperature
        controller. The returned value is a floating-point number in the Celsius degrees scale."""
        self.board_socket.send(bytearray.fromhex("10 00 01 07"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])

    def set_temp1_setpoint(self, value):
        """Sets the temperature set-point for the A/C front-end temperature controller. The value
        passed as the argument is a floating-point number."""
        self.board_socket.send(bytearray.fromhex("20 00 09 07") + struct.pack("<d", value))
        temp = self.board_socket.recv(1024)

    def get_temp2_setpoint(self):
        """This method returns the temperature set-point for the B/D front-end temperature
        controller. The returned value is a floating-point number in the Celsius degrees scale."""
        self.board_socket.send(bytearray.fromhex("10 00 01 08"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])

    def set_temp2_setpoint(self, value):
        """Sets the temperature set-point for the B/D front-end temperature controller. The value
        passed as the argument is a floating-point number."""
        self.board_socket.send(bytearray.fromhex("20 00 09 08") + struct.pack("<d", value))
        temp = self.board_socket.recv(1024)

    def get_temperature_control_status(self):
        """This method returns the temperature controller status as an integer. If this integer
        equals 0, it's because the temperature controller is off. Otherwise, if the value returned
        equals 1, this means the temperature controller is on."""
        self.board_socket.send(bytearray.fromhex("10 00 01 09"))
        temp = self.board_socket.recv(1024)
        return(temp[3])

    def set_temperature_control_status(self, status):
        """Method used to turn on/off the temperature controller. For turning the controller on, the
        argument should be the integer 1. To turn the controller off, the argument should be 0."""
        if (status in (0, 1)):
            self.board_socket.send(bytearray.fromhex("20 00 02 09 0" + str(status)))
            temp = self.board_socket.recv(1024)

    def get_software_version(self):
        """This method returns the RF front-end controller software version as a binary
    string of characters."""
        self.board_socket.send(bytearray.fromhex("10 00 01 0B"))
        temp = self.board_socket.recv(1024)
        return(temp[3:10])

    def get_output1_value(self):
        """This method returns the voltage signal to the heater in the A/C front-end as a
        floating-point number."""
        self.board_socket.send(bytearray.fromhex("10 00 01 0A"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])

    def set_output1_value(self, value):
        """Sets the voltage level to the heater in the A/C front-end. The value passed as the
        argument, a floating-point number, is the intended voltage for the heater."""
        self.board_socket.send(bytearray.fromhex("20 00 09 0A") + struct.pack("<d", value))
        temp = self.board_socket.recv(1024)

    def get_output2_value(self):
        """This method returns the voltage signal to the heater in the B/D front-end as a
        floating-point number."""
        self.board_socket.send(bytearray.fromhex("10 00 01 0B"))
        temp = self.board_socket.recv(1024)
        return(struct.unpack("<d", temp[3:])[0])

    def set_output2_value(self, value):
        """Sets the voltage level to the heater in the B/D front-end. The value passed as the
        argument, a floating-point number, is the intended voltage for the heater."""
        self.board_socket.send(bytearray.fromhex("20 00 09 0B") + struct.pack("<d", value))
        temp = self.board_socket.recv(1024)

    def reprogram(self, file_path):
        """This method reprograms the mbed device on the RF front-end controller board. The
        argument, a string, is the path to the binary file which corresponds to the mbed program
        that will be loaded in the device."""
        file = open(file_path, "rb")
        self.board_socket.send(bytearray.fromhex("20 00 02 0D 01"))
        temp = self.board_socket.recv(1024)
        while True:
            data = file.read(127)
            if (not data):
                break
            elif (len(data) < 127):
                data = data + (b"\n" * (127 - len(data)))
            self.board_socket.send(bytearray.fromhex("20 00 80 0E") + data)
            temp = self.board_socket.recv(1024)
        self.board_socket.send(bytearray.fromhex("20 00 02 0D 02"))
        temp = self.board_socket.recv(1024)
        file.close()

    def reset(self):
        """This method resets the board software."""
        self.board_socket.send(bytearray.fromhex("20 00 02 0C 01"))
        temp = self.board_socket.recv(1024)

    def close_connection(self):
        """Close the socket connection to the board."""
        self.board_socket.close()


        