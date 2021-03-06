##################################################################################################
## 
##  Xilinx, Inc. 2010            www.xilinx.com 
##  Mon Jan 9 08:26:59 2017
##  Generated by MIG Version 4.0
##  
##################################################################################################
##  File name :       example_top.sdc
##  Details :     Constraints file
##                    FPGA Family:       ARTIX7
##                    FPGA Part:         XC7A200TIFFG1156_PKG
##                    Speedgrade:        -1
##                    Design Entry:      VERILOG
##                    Frequency:         0 MHz
##                    Time Period:       2500 ps
##################################################################################################

##################################################################################################
## Controller 0
## Memory Device: DDR3_SDRAM->Components->MT41J512M8XX-125
## Data Width: 32
## Time Period: 2500
## Data Mask: 1
##################################################################################################

#create_clock -period 10 [get_ports sys_clk_i]
          
#create_clock -period 5 [get_ports clk_ref_i]
          
############## NET - IOSTANDARD ##################


