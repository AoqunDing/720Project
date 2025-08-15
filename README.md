Overview

This notebook uses an evolutionary algorithm (EA) to generate standard-cell style placements and diffusion-sharing for a small custom cell. We demonstrate on a positive-edge D flip-flop. The EA outputs:

a 2×N placement matrix (PMOS row, NMOS row),

a 2×N flip-bit matrix (per device, per row),

derived sharing groups (contiguous, net-consistent),

and a stick diagram renderer for visualization.

Files

flipflop.sp — SPICE netlist for the DFF (provided).

parse.py — netlist parser that returns V (devices) and E (nets per device).

project.ipynb — the Colab notebook with:

EA problem & solver,

feasibility repair,

result checker,

stick-diagram plotter.

How to Run

Upload flipflop.sp and parse.py to the Colab workspace.

Run the notebook top-to-bottom. The notebook:

parses the netlist to create V and E,

sets up the EA search space (placement + flip),

evaluates feasibility and objectives,

prints the Placement, Flip Bits, Derived Groups, and Breaks,

draws the stick diagram.

Expected numbers (for the provided DFF netlist and a typical run):

PMOS breaks ≈ 5, NMOS breaks ≈ 7, Total = 12
(with unique x-positions and multiple disjoint sharing chains).

Outputs to Look For

Console:

Placement: (2×N integers)

Flip Bits: (2×N integers 0/1)

Derived Groups: (2×N labels from contiguity + net consistency)

Breaks: PMOS = 5 , NMOS = 7 , Total = 12

Figure:

Stick diagram with diffusion strips (hatched), poly sticks (vertical), and interface tags (SHARE / break / gap).