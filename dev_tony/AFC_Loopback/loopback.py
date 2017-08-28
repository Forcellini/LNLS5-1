from subprocess import Popen,PIPE

a = False
#b = True
#print("Escolha o teste de loopback a ser feito:\n")
#print("1- Pinos de alta velocidade\n")
#print("2- Pinos RTM\n")
if (a==True):
    comando2 = "sudo /opt/Xilinx/Vivado/2016.2/bin/vivado -source /home/engenharia/Project_Test/GTP.tcl\n"
    command_stdout = Popen(comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()

if (a==False):
    comando2 = "sudo /opt/Xilinx/Vivado/2016.2/bin/vivado -source /home/engenharia/Project_Test/RTM_IO.tcl\n"
    command_stdout = Popen(comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
    command_stdout=command_stdout.splitlines()