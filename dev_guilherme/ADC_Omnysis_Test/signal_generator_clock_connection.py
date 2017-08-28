import socket
import time

SLEEP_TIME = 1.0

#GERADOR DE SINAIS
class Signal_Generator_Clock:
    def __init__(self,ip):
        sgen_address = ((ip, 5025))
        self.sgen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sgen_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sgen_socket.settimeout(5.0)
        self.sgen_socket.connect(sgen_address)
        self.sgen_socket.send(b"SYST:PRES\n")
        #time.sleep(SLEEP_TIME)

    def set_amplitude(self,amplitude):
        #self.sgen_socket.send(b"SOUR:POW:ATT " + format(amplitude).encode('utf-8') + b"\n")
        self.sgen_socket.send(b"SOUR:POW " + format(amplitude).encode('utf-8') + b"\n")
        self.sgen_socket.send(b"OUTP ON\n")
        
        return

    def set_frequency(self,frequency):
        #self.sgen_socket.send("SOURCE1:FREQUENCY " + str(frequency) + "\n")
        self.sgen_socket.send(b"SOUR:FREQ " + format(frequency).encode('utf-8') + b"\n") 
        return

    def close_connection(self):
        self.sgen_socket.close()
        return