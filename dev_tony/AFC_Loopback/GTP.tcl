open_hw
connect_hw_server -url localhost:3121
open_hw_target
set_property PROGRAM.FILE {/home/engenharia/Project_Test/project_3/project_3.runs/impl_1/example_ibert_7series_gtp_0.bit} [lindex [get_hw_devices] 0]
current_hw_device [lindex [get_hw_devices] 0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]
set_property PROBES.FILE {} [lindex [get_hw_devices] 0]
set_property PROGRAM.FILE {/home/engenharia/Project_Test/project_3/project_3.runs/impl_1/example_ibert_7series_gtp_0.bit} [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0]
refresh_hw_device [lindex [get_hw_devices] 0]

