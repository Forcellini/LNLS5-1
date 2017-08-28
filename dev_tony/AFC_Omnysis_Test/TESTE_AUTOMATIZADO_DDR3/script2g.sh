#!/bin/bash
#xinput set-prop 12 "Device Enabled" 1
sleep 2
xdotool key f11
xdotool type 'script' 
xdotool key space  
xdotool key minus
xdotool type 'f'
xdotool key space  
xdotool type 'TESTE_AUTOMATIZADO_DDR3/history.log'
xdotool key Return  
xdotool type /opt/Xilinx/SDK/2016.2/bin/xmd
xdotool key Return  
xdotool type 'xfpga_isconfigured -cable type xilinx_tcf url TCP'
xdotool key colon
xdotool type "127.0.0.1"
xdotool key colon
xdotool type "3121"
xdotool key Return  
xdotool type 'xconnect mb mdm -cable type xilinx_tcf url TCP'
xdotool key colon
xdotool type "127.0.0.1"
xdotool key colon
xdotool type "3121"
xdotool key Return  
xdotool type "set_cur_target 0"
xdotool key Return  
xdotool type "set_cur_system"
xdotool key Return  
xdotool type "xreset 0 0x80"
xdotool key Return  echo end
xdotool type "terminal -jtag_uart_server"
xdotool key Return  
xdotool type "xdownload 0 /AFC_Omnysis_Test/TESTE_AUTOMATIZADO_DDR3/mem5000/project_1/project_1.sdk/Mem/Debug/Mem.elf"
xdotool key Return  
xdotool type "xsafemode 0 off"
xdotool key Return  
xdotool type "xremove 0 all"
xdotool key Return  
xdotool type "xbreakpoint 0 exit sw"
xdotool key Return
xdotool type "xelf_start_address /AFC_Omnysis_Test/TESTE_AUTOMATIZADO_DDR3/mem5000/project_1/project_1.sdk/Mem/Debug/Mem.elf"
xdotool key Return
xdotool type  "xrun 0"
xdotool key Return








