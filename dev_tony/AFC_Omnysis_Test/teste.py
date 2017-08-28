from subprocess import Popen,PIPE
import time

proc1 = Popen(["gnome-terminal"])

#comando2="sh /home/engenharia/Desktop/APRESENTACAO___LNLS/TESTE_AUTOMATIZADO_DDR3/script2g.sh"
#Popen(comando2,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE).communicate()[0]
time.sleep(10)
proc1.kill()