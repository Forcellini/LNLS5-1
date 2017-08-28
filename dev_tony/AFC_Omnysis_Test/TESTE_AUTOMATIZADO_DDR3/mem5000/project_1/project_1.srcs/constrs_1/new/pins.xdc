set_property PACKAGE_PIN AK7 [get_ports CLK_IN1_D_clk_p]
set_property PACKAGE_PIN AG26 [get_ports reset_rtl]
set_property IOSTANDARD LVCMOS15 [get_ports reset_rtl]
set_property IOSTANDARD DIFF_SSTL15 [get_ports CLK_IN1_D_clk_p]
set_property IOSTANDARD DIFF_SSTL15 [get_ports {DDR3_ck_n[0]}]

set_property CLOCK_DEDICATED_ROUTE BACKBONE [get_nets design_1_i/clk_wiz_0/inst/clk_in1_design_1_clk_wiz_0_0]
