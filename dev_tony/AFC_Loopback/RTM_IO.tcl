open_hw
connect_hw_server -url localhost:3121
open_hw_target
set_property PROGRAM.FILE {/home/engenharia/Project_Test/project_2/project_2.runs/impl_1/design_1_wrapper.bit} [lindex [get_hw_devices] 0]
set_property PROBES.FILE {/home/engenharia/Project_Test/project_2/project_2.runs/impl_1/debug_nets.ltx} [lindex [get_hw_devices] 0]
current_hw_device [lindex [get_hw_devices] 0]
refresh_hw_device [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0]
refresh_hw_device [lindex [get_hw_devices] 0]
display_hw_ila_data [ get_hw_ila_data hw_ila_data_1 -of_objects [get_hw_ilas -of_objects [get_hw_devices xc7a200t_0] -filter {CELL_NAME=~"design_1_i/returnflag_RnM"}]]

run_hw_ila [get_hw_ilas -of_objects [get_hw_devices xc7a200t_0] -filter {CELL_NAME=~"design_1_i/returnflag_RnM"}] -trigger_now

wait_on_hw_ila [get_hw_ilas -of_objects [get_hw_devices xc7a200t_0] -filter {CELL_NAME=~"design_1_i/returnflag_RnM"}]

display_hw_ila_data [upload_hw_ila_data [get_hw_ilas -of_objects [get_hw_devices xc7a200t_0] -filter {CELL_NAME=~"design_1_i/returnflag_RnM"}]]

