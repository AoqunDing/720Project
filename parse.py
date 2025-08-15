import re
from typing import List, Tuple, Dict

def parse_netlist(text: str) -> Tuple[List[Dict], List[Tuple[str, str, str]]]:
    V, E = [], []

    lines = text.splitlines()
    subckt_defs = {}
    current_subckt = None
    subckt_body = []

    # --- Pass 1: extract all subcircuits ---
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("*"):
            continue

        if line.lower().startswith(".subckt"):
            tokens = line.split()
            current_subckt = tokens[1]
            ports = tokens[2:]
            subckt_body = []
        elif line.lower().startswith(".ends"):
            if current_subckt:
                subckt_defs[current_subckt] = {"ports": ports, "body": subckt_body.copy()}
                current_subckt = None
        elif current_subckt:
            subckt_body.append(line)

    # --- Helper to parse MOSFET lines ---
    def parse_mos(inst_prefix, line, net_map):
        tokens = line.split()
        if not tokens[0].lower().startswith("m"):
            return None, None
        inst = inst_prefix + "_" + tokens[0]
        d, g, s, b, model = [net_map.get(n, n) for n in tokens[1:6]]
        mos_type = "PMOS" if model.upper().startswith("P") else "NMOS"
        return {"id": inst, "type": mos_type}, (d, g, s)

    # --- Pass 2: instantiate top-level transistors and subckt calls ---
    mos_line = re.compile(r"^[mM]\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+")
    x_line = re.compile(r"^[xX](\S+)\s+(.*)")

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("*") or line.lower().startswith("."):
            continue

        # Top-level MOSFET
        if mos_line.match(line):
            tokens = line.split()
            inst = tokens[0]
            d, g, s, b, model = tokens[1:6]
            mos_type = "PMOS" if model.upper().startswith("P") else "NMOS"
            V.append({"id": inst, "type": mos_type})
            E.append((d, g, s))

        # Subcircuit instantiation (X...)
        elif x_line.match(line):
            tokens = line.split()
            inst_name = tokens[0]  # e.g. Xinv1
            args = tokens[1:]
            subckt_name = args[-1]
            nets = args[:-1]

            if subckt_name not in subckt_defs:
                continue

            defn = subckt_defs[subckt_name]
            port_map = dict(zip(defn["ports"], nets))

            for sub_line in defn["body"]:
                mos, net = parse_mos(inst_name, sub_line, port_map)
                if mos:
                    V.append(mos)
                    E.append(net)

    return V, E
