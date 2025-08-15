* D Flip-Flop (Master-Slave, positive-edge triggered)
* Example SPICE netlist

VDD   vdd 0 DC 1.8
VSS   gnd 0 DC 0

* Clock
VCLK  clk 0 PULSE(0 1.8 0 10p 10p 1n 2n)

* Data input (example waveform)
VD    d   0 PULSE(0 1.8 0 10p 10p 3n 6n)

* CMOS Inverter Subcircuit
.subckt inv in out vdd gnd Wp=1u Wn=0.5u L=0.18u
M1 out in vdd vdd PMOS W={Wp} L={L}
M2 out in gnd gnd NMOS W={Wn} L={L}
.ends inv

* Transmission Gate Subcircuit
.subckt tgate in out ctrl nctrl vdd gnd Wp=1u Wn=0.5u L=0.18u
M1 out in ctrl vdd PMOS W={Wp} L={L}
M2 out in nctrl gnd NMOS W={Wn} L={L}
.ends tgate

* Master Latch
Xinv1 d d_bar vdd gnd inv
Xtg1  d d_m clk clk_bar vdd gnd tgate
Xinv2 d_m q_m vdd gnd inv
Xinv3 q_m d_m_bar vdd gnd inv
Xtg2  d_m_bar q_m_bar clk clk_bar vdd gnd tgate

* Slave Latch
Xtg3  q_m q clk_bar clk vdd gnd tgate
Xinv4 q q_bar vdd gnd inv
Xinv5 q_bar qb vdd gnd inv
Xinv6 qb qb_bar vdd gnd inv
Xtg4  qb_bar qb clk_bar clk vdd gnd tgate

* Clock inverter
Xinv_clk clk clk_bar vdd gnd inv

* MOSFET Models (example level 1 models)
.model NMOS NMOS (LEVEL=1 VTO=0.7 KP=120e-6)
.model PMOS PMOS (LEVEL=1 VTO=-0.7 KP=50e-6)

.tran 0.1n 20n
.end
