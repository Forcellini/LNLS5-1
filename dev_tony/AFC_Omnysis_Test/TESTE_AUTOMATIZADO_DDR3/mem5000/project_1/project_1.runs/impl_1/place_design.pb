
�
�No debug cores found in the current design.
Before running the implement_debug_core command, either use the Set Up Debug wizard (GUI mode)
or use the create_debug_core and connect_debug_core Tcl commands to insert debug cores into the design.
154*	chipscopeZ16-241h px� 
Q
Command: %s
53*	vivadotcl2 
place_design2default:defaultZ4-113h px� 
�
@Attempting to get a license for feature '%s' and/or device '%s'
308*common2"
Implementation2default:default2
xc7a200t2default:defaultZ17-347h px� 
�
0Got license for feature '%s' and/or device '%s'
310*common2"
Implementation2default:default2
xc7a200t2default:defaultZ17-349h px� 
P
Running DRC with %s threads
24*drc2
42default:defaultZ23-27h px� 
V
DRC finished with %s
79*	vivadotcl2
0 Errors2default:defaultZ4-198h px� 
e
BPlease refer to the DRC report (report_drc) for more information.
80*	vivadotclZ4-199h px� 
p
,Running DRC as a precondition to command %s
22*	vivadotcl2 
place_design2default:defaultZ4-22h px� 
P
Running DRC with %s threads
24*drc2
42default:defaultZ23-27h px� 
�
Rule violation (%s) %s - %s
20*drc2
PLIDC-142default:default2C
/IDELAYCTRL REFCLK should be same as ISERDES CLK2default:default2�
�The BITSLICE cell IDELAYCTRL design_1_i/mig_7series_0/u_design_1_mig_7series_0_0_mig/u_iodelay_ctrl/u_idelayctrl_200 REFCLK pin should be driven by the same clock net as the associated ISERDES design_1_i/mig_7series_0/u_design_1_mig_7series_0_0_mig/u_memc_ui_top_axi/mem_intfc0/ddr_phy_top0/u_ddr_mc_phy_wrapper/u_ddr_mc_phy/ddr_phy_4lanes_0.u_ddr_phy_4lanes/ddr_byte_lane_A.ddr_byte_lane_A/ddr_byte_group_io/input_[0].iserdes_dq_.iserdesdq CLK or CLKDIV pin.2default:defaultZ23-20h px� 
b
DRC finished with %s
79*	vivadotcl2(
0 Errors, 1 Warnings2default:defaultZ4-198h px� 
e
BPlease refer to the DRC report (report_drc) for more information.
80*	vivadotclZ4-199h px� 
U

Starting %s Task
103*constraints2
Placer2default:defaultZ18-103h px� 
}
BMultithreading enabled for place_design using a maximum of %s CPUs12*	placeflow2
42default:defaultZ30-611h px� 
v

Phase %s%s
101*constraints2
1 2default:default2)
Placer Initialization2default:defaultZ18-101h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2.
Netlist sorting complete. 2default:default2
00:00:00.092default:default2
00:00:00.092default:default2
2248.7542default:default2
0.0002default:default2
12562default:default2
49082default:defaultZ17-722h px� 
E
%Done setting XDC timing constraints.
35*timingZ38-35h px� 
u
)Pushed %s inverter(s) to %s load pin(s).
98*opt2
02default:default2
02default:defaultZ31-138h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2.
Netlist sorting complete. 2default:default2
00:00:00.052default:default2
00:00:00.042default:default2
2248.7542default:default2
0.0002default:default2
12562default:default2
49082default:defaultZ17-722h px� 
�

Phase %s%s
101*constraints2
1.1 2default:default2F
2IO Placement/ Clock Placement/ Build Placer Device2default:defaultZ18-101h px� 
�

Phase %s%s
101*constraints2
1.1.1 2default:default22
ParallelPlaceIOClockAndInitTop2default:defaultZ18-101h px� 
v

Phase %s%s
101*constraints2
1.1.1.1 2default:default2#
Pre-Place Cells2default:defaultZ18-101h px� 
H
3Phase 1.1.1.1 Pre-Place Cells | Checksum: 835be54f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:05 ; elapsed = 00:00:04 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1255 ; free virtual = 49082default:defaulth px� 
�

Phase %s%s
101*constraints2
1.1.1.2 2default:default2/
Constructing HAPIClkRuleMgr2default:defaultZ18-101h px� 
T
?Phase 1.1.1.2 Constructing HAPIClkRuleMgr | Checksum: 835be54f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:06 ; elapsed = 00:00:05 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1255 ; free virtual = 49082default:defaulth px� 
E
%Done setting XDC timing constraints.
35*timingZ38-35h px� 
z

Phase %s%s
101*constraints2
1.1.1.3 2default:default2'
IO and Clk Clean Up2default:defaultZ18-101h px� 
�

Phase %s%s
101*constraints2

1.1.1.3.1 2default:default2/
Constructing HAPIClkRuleMgr2default:defaultZ18-101h px� 
V
APhase 1.1.1.3.1 Constructing HAPIClkRuleMgr | Checksum: 835be54f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:12 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1251 ; free virtual = 49082default:defaulth px� 
L
7Phase 1.1.1.3 IO and Clk Clean Up | Checksum: 835be54f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:13 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1251 ; free virtual = 49082default:defaulth px� 
�

Phase %s%s
101*constraints2
1.1.1.4 2default:default2>
*Implementation Feasibility check On IDelay2default:defaultZ18-101h px� 
c
NPhase 1.1.1.4 Implementation Feasibility check On IDelay | Checksum: 835be54f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:13 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1251 ; free virtual = 49082default:defaulth px� 
z

Phase %s%s
101*constraints2
1.1.1.5 2default:default2'
Commit IO Placement2default:defaultZ18-101h px� 
L
7Phase 1.1.1.5 Commit IO Placement | Checksum: f28c8345
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:13 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1251 ; free virtual = 49082default:defaulth px� 
U
@Phase 1.1.1 ParallelPlaceIOClockAndInitTop | Checksum: f28c8345
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:13 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1251 ; free virtual = 49082default:defaulth px� 
h
SPhase 1.1 IO Placement/ Clock Placement/ Build Placer Device | Checksum: 1c7e7595b
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:19 ; elapsed = 00:00:13 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1251 ; free virtual = 49082default:defaulth px� 
}

Phase %s%s
101*constraints2
1.2 2default:default2.
Build Placer Netlist Model2default:defaultZ18-101h px� 
v

Phase %s%s
101*constraints2
1.2.1 2default:default2%
Place Init Design2default:defaultZ18-101h px� 
r

Phase %s%s
101*constraints2
1.2.1.1 2default:default2
Make Others2default:defaultZ18-101h px� 
E
0Phase 1.2.1.1 Make Others | Checksum: 19d40fa94
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:21 ; elapsed = 00:00:15 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1248 ; free virtual = 49072default:defaulth px� 
~

Phase %s%s
101*constraints2
1.2.1.2 2default:default2+
Init Lut Pin Assignment2default:defaultZ18-101h px� 
Q
<Phase 1.2.1.2 Init Lut Pin Assignment | Checksum: 19d40fa94
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:21 ; elapsed = 00:00:15 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1248 ; free virtual = 49072default:defaulth px� 
I
4Phase 1.2.1 Place Init Design | Checksum: 1bd321259
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:43 ; elapsed = 00:00:23 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1243 ; free virtual = 49032default:defaulth px� 
P
;Phase 1.2 Build Placer Netlist Model | Checksum: 1bd321259
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:43 ; elapsed = 00:00:24 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1243 ; free virtual = 49032default:defaulth px� 
z

Phase %s%s
101*constraints2
1.3 2default:default2+
Constrain Clocks/Macros2default:defaultZ18-101h px� 
M
8Phase 1.3 Constrain Clocks/Macros | Checksum: 1bd321259
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:43 ; elapsed = 00:00:24 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1243 ; free virtual = 49032default:defaulth px� 
I
4Phase 1 Placer Initialization | Checksum: 1bd321259
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:00:43 ; elapsed = 00:00:24 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1243 ; free virtual = 49032default:defaulth px� 
q

Phase %s%s
101*constraints2
2 2default:default2$
Global Placement2default:defaultZ18-101h px� 
D
/Phase 2 Global Placement | Checksum: 163b0988e
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:29 ; elapsed = 00:00:48 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 
q

Phase %s%s
101*constraints2
3 2default:default2$
Detail Placement2default:defaultZ18-101h px� 
}

Phase %s%s
101*constraints2
3.1 2default:default2.
Commit Multi Column Macros2default:defaultZ18-101h px� 
P
;Phase 3.1 Commit Multi Column Macros | Checksum: 163b0988e
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:30 ; elapsed = 00:00:48 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 


Phase %s%s
101*constraints2
3.2 2default:default20
Commit Most Macros & LUTRAMs2default:defaultZ18-101h px� 
R
=Phase 3.2 Commit Most Macros & LUTRAMs | Checksum: 1a978fac9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:47 ; elapsed = 00:00:56 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 
y

Phase %s%s
101*constraints2
3.3 2default:default2*
Area Swap Optimization2default:defaultZ18-101h px� 
L
7Phase 3.3 Area Swap Optimization | Checksum: 1e0b22e2f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:48 ; elapsed = 00:00:57 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 
x

Phase %s%s
101*constraints2
3.4 2default:default2)
updateClock Trees: DP2default:defaultZ18-101h px� 
K
6Phase 3.4 updateClock Trees: DP | Checksum: 1e0b22e2f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:48 ; elapsed = 00:00:57 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 
x

Phase %s%s
101*constraints2
3.5 2default:default2)
Timing Path Optimizer2default:defaultZ18-101h px� 
K
6Phase 3.5 Timing Path Optimizer | Checksum: 16ec79295
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:53 ; elapsed = 00:00:59 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 
t

Phase %s%s
101*constraints2
3.6 2default:default2%
Fast Optimization2default:defaultZ18-101h px� 
G
2Phase 3.6 Fast Optimization | Checksum: 1c8471a2e
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:01:55 ; elapsed = 00:01:01 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1304 ; free virtual = 49662default:defaulth px� 


Phase %s%s
101*constraints2
3.7 2default:default20
Small Shape Detail Placement2default:defaultZ18-101h px� 
R
=Phase 3.7 Small Shape Detail Placement | Checksum: 15d6ce5bf
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:02:05 ; elapsed = 00:01:11 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1303 ; free virtual = 49662default:defaulth px� 
u

Phase %s%s
101*constraints2
3.8 2default:default2&
Re-assign LUT pins2default:defaultZ18-101h px� 
H
3Phase 3.8 Re-assign LUT pins | Checksum: 185f285ea
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:02:07 ; elapsed = 00:01:12 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1303 ; free virtual = 49662default:defaulth px� 
�

Phase %s%s
101*constraints2
3.9 2default:default22
Pipeline Register Optimization2default:defaultZ18-101h px� 
S
>Phase 3.9 Pipeline Register Optimization | Checksum: a0184204
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:02:07 ; elapsed = 00:01:12 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1303 ; free virtual = 49662default:defaulth px� 
u

Phase %s%s
101*constraints2
3.10 2default:default2%
Fast Optimization2default:defaultZ18-101h px� 
H
3Phase 3.10 Fast Optimization | Checksum: 13aceccc1
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:02:19 ; elapsed = 00:01:18 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1292 ; free virtual = 49632default:defaulth px� 
D
/Phase 3 Detail Placement | Checksum: 13aceccc1
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:02:19 ; elapsed = 00:01:19 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1291 ; free virtual = 49632default:defaulth px� 
�

Phase %s%s
101*constraints2
4 2default:default2<
(Post Placement Optimization and Clean-Up2default:defaultZ18-101h px� 
{

Phase %s%s
101*constraints2
4.1 2default:default2,
Post Commit Optimization2default:defaultZ18-101h px� 
E
%Done setting XDC timing constraints.
35*timingZ38-35h px� 
}

Phase %s%s
101*constraints2
4.1.1 2default:default2,
updateClock Trees: PCOPT2default:defaultZ18-101h px� 
P
;Phase 4.1.1 updateClock Trees: PCOPT | Checksum: 1500c8726
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:02:39 ; elapsed = 00:01:26 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1281 ; free virtual = 49552default:defaulth px� 
�

Phase %s%s
101*constraints2
4.1.2 2default:default2/
Post Placement Optimization2default:defaultZ18-101h px� 
�
hPost Placement Timing Summary WNS=%s. For the most accurate timing information please run report_timing.610*place2
-5.7962default:defaultZ30-746h px� 
S
>Phase 4.1.2 Post Placement Optimization | Checksum: 227ab72b9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:03 ; elapsed = 00:01:49 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
N
9Phase 4.1 Post Commit Optimization | Checksum: 227ab72b9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:03 ; elapsed = 00:01:49 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
�

Phase %s%s
101*constraints2
4.2 2default:default25
!Sweep Clock Roots: Post-Placement2default:defaultZ18-101h px� 
W
BPhase 4.2 Sweep Clock Roots: Post-Placement | Checksum: 227ab72b9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:03 ; elapsed = 00:01:50 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
�

Phase %s%s
101*constraints2
4.3 2default:default27
#Uram Pipeline Register Optimization2default:defaultZ18-101h px� 
Y
DPhase 4.3 Uram Pipeline Register Optimization | Checksum: 227ab72b9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:03 ; elapsed = 00:01:50 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
y

Phase %s%s
101*constraints2
4.4 2default:default2*
Post Placement Cleanup2default:defaultZ18-101h px� 
L
7Phase 4.4 Post Placement Cleanup | Checksum: 227ab72b9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:04 ; elapsed = 00:01:50 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
s

Phase %s%s
101*constraints2
4.5 2default:default2$
Placer Reporting2default:defaultZ18-101h px� 
F
1Phase 4.5 Placer Reporting | Checksum: 227ab72b9
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:04 ; elapsed = 00:01:50 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
z

Phase %s%s
101*constraints2
4.6 2default:default2+
Final Placement Cleanup2default:defaultZ18-101h px� 
M
8Phase 4.6 Final Placement Cleanup | Checksum: 1f915832f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:04 ; elapsed = 00:01:51 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
\
GPhase 4 Post Placement Optimization and Clean-Up | Checksum: 1f915832f
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:04 ; elapsed = 00:01:51 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
>
)Ending Placer Task | Checksum: 146480f74
*commonh px� 
�

%s
*constraints2�
�Time (s): cpu = 00:03:04 ; elapsed = 00:01:51 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1280 ; free virtual = 49532default:defaulth px� 
Z
Releasing license: %s
83*common2"
Implementation2default:defaultZ17-83h px� 
�
G%s Infos, %s Warnings, %s Critical Warnings and %s Errors encountered.
28*	vivadotcl2
452default:default2
12default:default2
02default:default2
02default:defaultZ4-41h px� 
^
%s completed successfully
29*	vivadotcl2 
place_design2default:defaultZ4-42h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2"
place_design: 2default:default2
00:03:092default:default2
00:01:532default:default2
2248.7542default:default2
0.0002default:default2
12802default:default2
49532default:defaultZ17-722h px� 
D
Writing placer database...
1603*designutilsZ20-1893h px� 
=
Writing XDEF routing.
211*designutilsZ20-211h px� 
J
#Writing XDEF routing logical nets.
209*designutilsZ20-209h px� 
J
#Writing XDEF routing special nets.
210*designutilsZ20-210h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2)
Write XDEF Complete: 2default:default2
00:00:082default:default2
00:00:032default:default2
2248.7542default:default2
0.0002default:default2
12402default:default2
49532default:defaultZ17-722h px� 
�
r%sTime (s): cpu = %s ; elapsed = %s . Memory (MB): peak = %s ; gain = %s ; free physical = %s ; free virtual = %s
480*common2&
write_checkpoint: 2default:default2
00:00:152default:default2
00:00:082default:default2
2248.7542default:default2
0.0002default:default2
12692default:default2
49532default:defaultZ17-722h px� 
�
�report_io: Time (s): cpu = 00:00:00.42 ; elapsed = 00:00:00.48 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1268 ; free virtual = 4952
*commonh px� 
�
�report_utilization: Time (s): cpu = 00:00:00.44 ; elapsed = 00:00:00.49 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1267 ; free virtual = 4951
*commonh px� 
�
�report_control_sets: Time (s): cpu = 00:00:00.27 ; elapsed = 00:00:00.31 . Memory (MB): peak = 2248.754 ; gain = 0.000 ; free physical = 1267 ; free virtual = 4951
*commonh px� 


End Record