open_hw
connect_hw_server
open_hw_target
disconnect_hw_server
connect_hw_server
disconnect_hw_server localhost:3121
connect_hw_server
open_hw_target
current_hw_device [lindex [get_hw_devices] 0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]
set_property PROBES.FILE {} [lindex [get_hw_devices] 0]    
set_property PROGRAM.FILE {/home/tadeu/workspace/AD_comunication/Fpga/vivado_fpga/afcv3-bpm-gw-fmc130m-v0.3-20160831.bit} [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0] 
refresh_hw_device [lindex [get_hw_devices] 0]
exit

