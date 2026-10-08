#!/usr/bin/env python3
"""
scripts/figures/generate_unit3.py
Generates all publication-grade figures for UNIT 3 (Network Layer).
Produces SVGs in UNIT - 3/figures/
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_engine

OUTPUT_DIR = os.path.abspath("UNIT - 3/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating Unit 3 figures in: {OUTPUT_DIR}")

# ==============================================================================
# 1. 32-Bit Packet Headers (Python Vector SVG Engine)
# ==============================================================================

def generate_headers():
    # 1. IPv4 Packet Header (20-60 bytes)
    ipv4_rows = [
        [("Version", 4, "type", "4b (IPv4)"),
         ("IHL", 4, "length", "4b (Words)"),
         ("DSCP", 6, "control", "6b (ToS)"),
         ("ECN", 2, "control", "2b"),
         ("Total Length", 16, "length", "16 Bits (Header + Data Octets)")],
        [("Identification (ID)", 16, "seq", "16 Bits (Fragment Identifier)"),
         ("Flags", 3, "flag", "3b (DF, MF)"),
         ("Fragment Offset", 13, "meta", "13 Bits (8-Byte Units)")],
        [("Time to Live (TTL)", 8, "control", "8 Bits (Hop Limit)"),
         ("Protocol", 8, "type", "8 Bits (TCP:6, UDP:17, ICMP:1)"),
         ("Header Checksum", 16, "checksum", "16 Bits (1's Complement sum)")],
        [("Source IPv4 Address", 32, "address", "32 Bits (Originating Host IP)")],
        [("Destination IPv4 Address", 32, "address", "32 Bits (Final Destination Host IP)")],
        [("Options & Padding (0 to 40 Bytes: Record Route, Timestamp, Security)", 32, "options", "Variable (Padded to 32-bit boundary)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 791: Internet Protocol Version 4 (IPv4) Packet Header (20–60 Octets)",
        ipv4_rows,
        os.path.join(OUTPUT_DIR, "fig3_hdr_ipv4.svg")
    )

    # 2. IPv6 Fixed Base Header (40 bytes)
    ipv6_rows = [
        [("Version (6)", 4, "type", "4b (0110)"),
         ("Traffic Class", 8, "control", "8b (DiffServ & ECN)"),
         ("Flow Label", 20, "seq", "20 Bits (QoS / Real-Time Session Tag)")],
        [("Payload Length", 16, "length", "16 Bits (Bytes after 40B base header)"),
         ("Next Header", 8, "type", "8 Bits (Extension header or Upper protocol)"),
         ("Hop Limit", 8, "control", "8 Bits (Replaces IPv4 TTL)")],
        [("Source IPv6 Address (128 Bits / 16 Octets) — Part 1 / 2", 32, "address", "Upper 64 Bits (Global Routing Prefix + Subnet ID)")],
        [("Source IPv6 Address — Part 2 / 2", 32, "address", "Lower 64 Bits (Interface ID / EUI-64)")],
        [("Destination IPv6 Address (128 Bits / 16 Octets) — Part 1 / 2", 32, "address", "Upper 64 Bits (Routing Prefix + Subnet)")],
        [("Destination IPv6 Address — Part 2 / 2", 32, "address", "Lower 64 Bits (Interface ID)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 8200: Internet Protocol Version 6 (IPv6) Base Header (Fixed 40 Octets)",
        ipv6_rows,
        os.path.join(OUTPUT_DIR, "fig3_hdr_ipv6.svg")
    )

    # 3. ICMPv4 Message Header
    icmp_rows = [
        [("Type", 8, "type", "8 Bits (e.g. 0: Echo Reply, 3: Unreachable, 8: Echo Req, 11: TTL Exceeded)"),
         ("Code", 8, "control", "8 Bits (Diagnostic Sub-type code)"),
         ("Checksum", 16, "checksum", "16 Bits (1's Complement sum of ICMP message)")],
        [("Rest of Header (Identifier & Sequence for Ping; or Unused for Errors)", 32, "meta", "32 Bits (Context-dependent parameters)")],
        [("Internet Header + 64 Bits of Original Datagram Payload", 32, "address", "Quoted original packet causing the error")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 792: ICMPv4 Diagnostic Message Header Format",
        icmp_rows,
        os.path.join(OUTPUT_DIR, "fig3_hdr_icmp.svg")
    )

    # 4. DHCP Message Structure (240+ bytes)
    dhcp_rows = [
        [("op (1=BOOTREQUEST, 2=BOOTREPLY)", 8, "type", "8b"),
         ("htype (1=Ethernet)", 8, "meta", "8b"),
         ("hlen (6=MAC len)", 8, "length", "8b"),
         ("hops (Relay count)", 8, "control", "8b")],
        [("xid (Transaction ID)", 32, "seq", "32 Bits (Random transaction identifier)")],
        [("secs (Elapsed seconds)", 16, "meta", "16b"),
         ("flags (Broadcast flag B)", 16, "flag", "16 Bits (0x8000 = Broadcast)")],
        [("ciaddr (Client IP Address: if already bound)", 32, "address", "32 Bits")],
        [("yiaddr ('Your' (Client) IP Address assigned by server)", 32, "address", "32 Bits (Leased IP)")],
        [("siaddr (Next Server IP Address in bootstrap)", 32, "address", "32 Bits")],
        [("giaddr (Relay Agent IP Address)", 32, "address", "32 Bits (Cross-Subnet Gateway)")],
        [("chaddr (Client Hardware MAC Address: 16 Octets)", 32, "address", "Upper bytes of 48-bit MAC")],
        [("chaddr (Hardware Address Padding to 16 bytes)", 32, "reserved", "Padding to 16 octets")],
        [("sname (Server Host Name: 64 Octets optional)", 32, "meta", "64 Octets null-terminated string")],
        [("file (Boot file name: 128 Octets optional)", 32, "meta", "128 Octets boot image path")],
        [("Magic Cookie (0x63825363) + DHCP Options (Subnet, Router, DNS, Lease Time)", 32, "options", "Variable Options (TLV Format)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 2131: Dynamic Host Configuration Protocol (DHCP) Message Format",
        dhcp_rows,
        os.path.join(OUTPUT_DIR, "fig3_hdr_dhcp.svg")
    )

    # 5. OSPF Common Packet Header (24 bytes)
    ospf_rows = [
        [("Version = 2", 8, "type", "8b (0x02)"),
         ("Type (1:Hello, 2:DBD, 3:LSR, 4:LSU, 5:LSAck)", 8, "control", "8 Bits"),
         ("Packet Length", 16, "length", "16 Bits (Bytes including header)")],
        [("Router ID", 32, "address", "32 Bits (Originating Router IP / ID)")],
        [("Area ID", 32, "address", "32 Bits (0.0.0.0 = Backbone Area 0)")],
        [("Checksum", 16, "checksum", "16 Bits (Fletcher checksum)"),
         ("AuType (0:None, 1:Simple, 2:Cryptographic MD5)", 16, "type", "16 Bits")],
        [("Authentication Data / Key (64 Bits / 8 Octets) — Part 1", 32, "crypto", "32 Bits")],
        [("Authentication Data / Key — Part 2", 32, "crypto", "32 Bits (MD5 Digest / Key ID)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 2328: OSPF Common Packet Header (24 Octets)",
        ospf_rows,
        os.path.join(OUTPUT_DIR, "fig3_hdr_ospf.svg")
    )

generate_headers()
print("  Generated all 32-bit packet headers.")

# ==============================================================================
# 2. Matplotlib Publication Plots (IEEE/ACM Scientific Curves)
# ==============================================================================

def generate_scientific_plots():
    svg_engine.configure_matplotlib_style()

    # Fig 3.34: Network Congestion Collapse Curve (Offered Load vs Throughput and Delay)
    fig, ax1 = plt.subplots(figsize=(9, 4.8), dpi=300)

    load = np.linspace(0, 100, 500)
    # Ideal throughput: matches load up to capacity (50), then flat
    ideal_tp = np.minimum(load, 50)
    
    # Real throughput with Knee, Cliff, and Congestion Collapse
    real_tp = np.zeros_like(load)
    for i, x in enumerate(load):
        if x <= 40:
            real_tp[i] = x * 0.98 # Linear under Knee
        elif x <= 65:
            # Saturation between Knee and Cliff
            real_tp[i] = 40 * 0.98 + (x - 40) * 0.35
        else:
            # Congestion collapse beyond Cliff
            decay = np.exp(-(x - 65) / 12)
            real_tp[i] = 48 * decay

    # Delay curve
    delay = np.zeros_like(load)
    for i, x in enumerate(load):
        if x < 60:
            delay[i] = 5 / (1 - (x / 75))
        else:
            delay[i] = 25 + (x - 60) * 2.5

    ax2 = ax1.twinx()

    # Plot curves
    line1 = ax1.plot(load, ideal_tp, label='Ideal Throughput (Capacity = 50 Mbps)', color='#64748b', linestyle=':', linewidth=2)
    line2 = ax1.plot(load, real_tp, label='Actual Network Throughput', color='#2563eb', linewidth=2.8)
    line3 = ax2.plot(load, delay, label='Packet Delay (Queueing Latency)', color='#dc2626', linestyle='--', linewidth=2.2)

    # Shaded threshold zones
    ax1.axvspan(0, 40, color='#ecfdf5', alpha=0.5, label='Light Load (Optimal Zone)')
    ax1.axvspan(40, 65, color='#fef3c7', alpha=0.5, label='Congested (Moderate Queueing)')
    ax1.axvspan(65, 100, color='#fee2e2', alpha=0.5, label='Congestion Collapse Zone')

    ax1.axvline(x=40, color='#16a34a', linestyle='-.', alpha=0.8)
    ax1.axvline(x=65, color='#dc2626', linestyle='-.', alpha=0.8)

    ax1.annotate('Knee Threshold\n(Throughput starts saturating,\ndelay starts rising)', xy=(40, 39), xytext=(22, 45),
                 arrowprops=dict(facecolor='#16a34a', shrink=0.08, width=1, headwidth=5),
                 fontsize=8.5, fontweight='bold', color='#14532d',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#86efac'))

    ax1.annotate('Cliff Threshold\n(Buffer overflow,\nsevere packet drop,\nretransmission storm)', xy=(65, 48), xytext=(68, 38),
                 arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1, headwidth=5),
                 fontsize=8.5, fontweight='bold', color='#7f1d1d',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#fca5a5'))

    ax1.set_title('Figure 3.34: Network Congestion Collapse Dynamics (Throughput & Delay vs. Offered Load)',
                  fontsize=12, fontweight='bold', pad=12, color='#0f172a')
    ax1.set_xlabel('Offered Load (Traffic Injected into Network in Mbps)', fontsize=10, fontweight='bold', labelpad=8)
    ax1.set_ylabel('Effective Network Throughput (Mbps)', fontsize=10, fontweight='bold', color='#1e40af', labelpad=8)
    ax2.set_ylabel('End-to-End Packet Delay (ms)', fontsize=10, fontweight='bold', color='#991b1b', labelpad=8)

    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 55)
    ax2.set_ylim(0, 120)

    # Combine legends
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig3_34_congestion_collapse_curve.svg"), format='svg')
    plt.close()

generate_scientific_plots()
print("  Generated scientific performance curves.")

# ==============================================================================
# 3. Graphviz DOT State Machines
# ==============================================================================

def generate_dot_diagrams():
    # Fig 3.26: OSPF 7-State Adjacency Formation FSM
    ospf_fsm_dot = """
    digraph OSPF_FSM {
        graph [rankdir=TB, bgcolor="transparent", fontname="Helvetica", pad="0.2", nodesep="0.4", ranksep="0.5"];
        node [shape=box, style="filled,rounded", fontname="Helvetica-Bold", fontsize=9, margin="0.15,0.08", fillcolor="#f8fafc", color="#64748b", penwidth=1.3];
        edge [fontname="Helvetica", fontsize=8, color="#334155", penwidth=1.1, arrowsize=0.7];

        DOWN [label="1. DOWN STATE\\nNo Hello packets received from neighbor", fillcolor="#fee2e2", color="#dc2626", fontcolor="#991b1b"];
        INIT [label="2. INIT STATE\\nHello received, but local Router ID not in neighbor's list", fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        TWO_WAY [label="3. 2-WAY STATE\\nBi-directional communication established\\n(DR / BDR Election occurs here)", fillcolor="#e0e7ff", color="#4338ca", fontcolor="#312e81"];
        EXSTART [label="4. ExStart STATE\\nMaster / Slave negotiation & Initial DD sequence number chosen", fillcolor="#f3e8ff", color="#7e22ce", fontcolor="#581c87"];
        EXCHANGE [label="5. EXCHANGE STATE\\nDatabase Description (DBD) packets exchanged (LSA summaries)", fillcolor="#fef3c7", color="#b45309", fontcolor="#78350f"];
        LOADING [label="6. LOADING STATE\\nLink State Requests (LSR) and Link State Updates (LSU) sent", fillcolor="#ffedd5", color="#c2410c", fontcolor="#7c2d12"];
        FULL [label="7. FULL ADJACENCY\\nLink State Databases (LSDB) 100% synchronized\\nReady for Dijkstra SPF routing", fillcolor="#dcfce7", color="#16a34a", fontcolor="#14532d", penwidth=2.2];

        DOWN -> INIT [label=" Receive Hello Packet"];
        INIT -> TWO_WAY [label=" Receive Hello listing own Router ID"];
        TWO_WAY -> EXSTART [label=" Adjacency required (DR/BDR or Point-to-Point)"];
        EXSTART -> EXCHANGE [label=" Master/Slave negotiated & DD Seq agreed"];
        EXCHANGE -> LOADING [label=" DD exchange complete, missing LSAs identified"];
        EXCHANGE -> FULL [label=" No missing LSAs (LSDB already identical)"];
        LOADING -> FULL [label=" All missing LSAs received via LSU & confirmed with LSAck", color="#16a34a", fontcolor="#15803d", penwidth=1.6];
    }
    """
    svg_engine.compile_dot(ospf_fsm_dot, os.path.join(OUTPUT_DIR, "fig3_26_ospf_7state_fsm.svg"))

    # Fig 3.31: DHCP Lease Renewal State Machine
    dhcp_fsm_dot = """
    digraph DHCP_FSM {
        graph [rankdir=TB, bgcolor="transparent", fontname="Helvetica", pad="0.2", nodesep="0.4", ranksep="0.5"];
        node [shape=box, style="filled,rounded", fontname="Helvetica-Bold", fontsize=9, margin="0.15,0.08", fillcolor="#f8fafc", color="#64748b", penwidth=1.3];
        edge [fontname="Helvetica", fontsize=8, color="#334155", penwidth=1.1, arrowsize=0.7];

        INIT [label="INIT STATE\\nClient boots, has no IP\\nDispatches DHCPDISCOVER broadcast", fillcolor="#fee2e2", color="#dc2626", fontcolor="#991b1b"];
        SELECTING [label="SELECTING STATE\\nReceives DHCPOFFER packets\\nSelects best offer", fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        REQUESTING [label="REQUESTING STATE\\nBroadcasts DHCPREQUEST\\naccepting selected offer", fillcolor="#e0e7ff", color="#4338ca", fontcolor="#312e81"];
        BOUND [label="BOUND STATE\\nReceives DHCPACK\\nIP Address active & in use\\nTimers started (T1, T2, Expire)", fillcolor="#dcfce7", color="#16a34a", fontcolor="#14532d", penwidth=2.2];
        RENEWING [label="RENEWING STATE (T1 = 50% Lease)\\nUnicasts DHCPREQUEST to leasing server", fillcolor="#eff6ff", color="#2563eb", fontcolor="#1e40af"];
        REBINDING [label="REBINDING STATE (T2 = 87.5% Lease)\\nBroadcasts DHCPREQUEST to any server", fillcolor="#fef3c7", color="#b45309", fontcolor="#78350f"];

        INIT -> SELECTING [label=" Send DHCPDISCOVER"];
        SELECTING -> REQUESTING [label=" Select Offer & send DHCPREQUEST"];
        REQUESTING -> BOUND [label=" Recv DHCPACK (Config applied)"];
        REQUESTING -> INIT [label=" Recv DHCPNAK (Reject)"];
        
        BOUND -> RENEWING [label=" Timer T1 Expires (50% of lease)"];
        RENEWING -> BOUND [label=" Recv DHCPACK (Lease reset to 100%)", color="#16a34a", fontcolor="#15803d"];
        RENEWING -> REBINDING [label=" Timer T2 Expires (87.5% of lease, No ACK)"];
        REBINDING -> BOUND [label=" Recv DHCPACK from any server", color="#16a34a", fontcolor="#15803d"];
        REBINDING -> INIT [label=" Lease Expires (100% time up, IP released)", color="#dc2626", fontcolor="#b91c1c"];
        BOUND -> INIT [label=" Client Graceful Release (DHCPRELEASE)"];
    }
    """
    svg_engine.compile_dot(dhcp_fsm_dot, os.path.join(OUTPUT_DIR, "fig3_31_dhcp_lease_renewal_fsm.svg"))

generate_dot_diagrams()
print("  Generated Graphviz DOT state machines.")

# ==============================================================================
# 4. D2 Publication Diagrams (Architectures, Flows & Sequences)
# ==============================================================================

def generate_d2_diagrams():
    d2_diagrams = {
        # 1. Delivery Scopes
        "fig3_01_delivery_scopes.svg": """
direction: down

app_layer: "Application Layer\\nProcess-to-Process Delivery" {
  style.fill: "#eff6ff"
}

trans_layer: "Transport Layer (TCP / UDP)\\nProcess-to-Process Delivery (Ports / Sockets)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

net_layer: "Network Layer (IPv4 / IPv6)\\nHost-to-Host Delivery across Internet (IP Addresses)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

link_layer: "Data Link Layer (Ethernet / Wi-Fi)\\nHop-to-Hop Delivery across Single Link (MAC Addresses)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

app_layer -> trans_layer -> net_layer -> link_layer
""",

        # 2. Hop-by-Hop vs Host-to-Host
        "fig3_02_hop_vs_host_delivery.svg": """
direction: right

src: "Source Host A\\n10.1.1.5" {
  style.fill: "#dbeafe"
}

r1: "Router R1\\n(Hop 1)" {
  style.fill: "#f8fafc"
}

r2: "Router R2\\n(Hop 2)" {
  style.fill: "#f8fafc"
}

dst: "Destination Host B\\n172.16.2.20" {
  style.fill: "#dcfce7"
}

src -> r1: "Link 1: MAC_A -> MAC_R1"
r1 -> r2: "Link 2: MAC_R1 -> MAC_R2"
r2 -> dst: "Link 3: MAC_R2 -> MAC_B"

src -> dst: "Host-to-Host End-to-End Delivery: IP_A (10.1.1.5) -> IP_B (172.16.2.20)\\n(IP addresses remain constant throughout transit)" {
  style.stroke: "#16a34a"
  style.bold: true
}
""",

        # 3. Core Duties of Network Layer
        "fig3_03_network_layer_duties.svg": """
direction: right

duties: "Core Duties of the Network Layer" {
  d1: "1. Host-to-Host Logical Addressing (IPv4 / IPv6)"
  d2: "2. Routing: Calculating global optimal paths (OSPF, BGP)"
  d3: "3. Forwarding: Local switching fabric packet transfer"
  d4: "4. Packetizing & Encapsulation: Adding IP headers"
  d5: "5. Fragmentation & Reassembly across varying MTUs"
  d6: "6. Diagnostic Error Reporting: ICMPv4 / ICMPv6"
  d7: "7. Quality of Service (QoS) & Congestion Management"
}
""",

        # 4. Router Internal Architecture
        "fig3_04_router_architecture.svg": """
direction: right

inputs: "Input Ports\\n• Physical termination\\n• Data link decapsulation\\n• Lookup / Forwarding engine" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

fabric: "Switching Fabric\\n(High-Speed Crossbar / Shared Memory)\\nTransfers packets input -> output" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
  style.bold: true
}

outputs: "Output Ports\\n• Output queue buffer\\n• Link-layer framing\\n• Physical transmission" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

cpu: "Routing Processor (Control Plane)\\nExecutes OSPF, BGP, RIP\\nComputes Routing Information Base (RIB)\\nUpdates Forwarding Tables (FIB)" {
  style.fill: "#f1f5f9"
  style.stroke: "#475569"
}

inputs -> fabric -> outputs
cpu -> fabric: "Installs FIB Table"
""",

        # 5. Packet Fragmentation
        "fig3_05_fragmentation_flow.svg": """
direction: right

orig: "Original IP Datagram\\nTotal Length = 4000B\\n(20B Header + 3980B Data)\\nID = 54321, DF=0, MF=0, Offset=0" {
  style.fill: "#f8fafc"
}

f1: "Fragment 1 (MTU 1500)\\nTotal Length = 1500B\\n(20B Header + 1480B Data)\\nID=54321, MF=1, Offset=0" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

f2: "Fragment 2 (MTU 1500)\\nTotal Length = 1500B\\n(20B Header + 1480B Data)\\nID=54321, MF=1, Offset=185 (1480/8)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

f3: "Fragment 3 (MTU 1500)\\nTotal Length = 1040B\\n(20B Header + 1020B Data)\\nID=54321, MF=0, Offset=370 (2960/8)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

orig -> f1: "MTU = 1500B"
orig -> f2: "MTU = 1500B"
orig -> f3: "Final Fragment"
""",

        # 6. Classful Bit Patterns
        "fig3_06_classful_bit_patterns.svg": """
direction: right

ca: "Class A\\nBits: 0... (1 – 126)\\n/8 Netmask (255.0.0.0)\\n126 Networks, 16.7M Hosts each" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

cb: "Class B\\nBits: 10... (128 – 191)\\n/16 Netmask (255.255.0.0)\\n16,384 Networks, 65,534 Hosts each" {
  style.fill: "#e0e7ff"
  style.stroke: "#4338ca"
}

cc: "Class C\\nBits: 110... (192 – 223)\\n/24 Netmask (255.255.255.0)\\n2.09M Networks, 254 Hosts each" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

cd: "Class D\\nBits: 1110... (224 – 239)\\nMulticast Groups (No hosts)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

ce: "Class E\\nBits: 1111... (240 – 255)\\nReserved for Experimental Use" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

ca -> cb -> cc -> cd -> ce
""",

        # 7. Total Space Allocation
        "fig3_07_space_distribution.svg": """
direction: right

dist: "IPv4 32-Bit Address Space Distribution (4,294,967,296 Addresses)" {
  p_a: "Class A: 50% of Total Space (2,147,483,648 Addresses)" { style.fill: "#dbeafe" }
  p_b: "Class B: 25% of Total Space (1,073,741,824 Addresses)" { style.fill: "#e0e7ff" }
  p_c: "Class C: 12.5% of Total Space (536,870,912 Addresses)" { style.fill: "#dcfce7" }
  p_d: "Class D: 6.25% of Total Space (268,435,456 Multicast Addresses)" { style.fill: "#fef3c7" }
  p_e: "Class E: 6.25% of Total Space (268,435,456 Reserved Addresses)" { style.fill: "#fee2e2" }
}
""",

        # 8. Private IP Blocks
        "fig3_08_private_ip_blocks.svg": """
direction: right

rfc1918: "RFC 1918 Private IP Address Blocks (Non-Routable on Public Internet)" {
  block_a: "10.0.0.0/8 (10.0.0.0 – 10.255.255.255)\\nTotal: 16,777,216 IPs (Large Enterprises)" { style.fill: "#dbeafe" }
  block_b: "172.16.0.0/12 (172.16.0.0 – 172.31.255.255)\\nTotal: 1,048,576 IPs (Medium Enterprises)" { style.fill: "#e0e7ff" }
  block_c: "192.168.0.0/16 (192.168.0.0 – 192.168.255.255)\\nTotal: 65,536 IPs (Home / Small Office LANs)" { style.fill: "#dcfce7" }
}
""",

        # 9. Routing Methodologies Taxonomy
        "fig3_09_routing_taxonomy.svg": """
direction: right

dv: "Distance Vector Routing\\n• Bellman-Ford Algorithm\\n• Exchange full routing table with neighbors\\n• Periodic updates (RIP: 30s)\\n• Convergence delay & Count-to-Infinity" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

ls: "Link State Routing\\n• Dijkstra SPF Algorithm\\n• Floods Link State Packets (LSP) globally\\n• Synchronized complete topology map (LSDB)\\n• Rapid, loop-free convergence (OSPF)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

pv: "Path Vector Routing\\n• Advertises full AS-PATH sequences\\n• Policy-based inter-domain routing\\n• Eliminates loops between ASes (BGP-4)" {
  style.fill: "#e0e7ff"
  style.stroke: "#4338ca"
}
""",

        # 10. Distance Vector Network Topology
        "fig3_10_distance_vector_topology.svg": """
direction: right

A: "Router A" { style.fill: "#dbeafe" }
B: "Router B" { style.fill: "#dbeafe" }
C: "Router C" { style.fill: "#dbeafe" }
D: "Router D" { style.fill: "#dbeafe" }

A <-> B: "Cost = 2"
B <-> C: "Cost = 3"
A <-> C: "Cost = 7"
C <-> D: "Cost = 1"
B <-> D: "Cost = 6"
""",

        # 11. Distance Vector Convergence Iterations
        "fig3_11_dv_convergence.svg": """
direction: right

init: "Initialization\\nRouters know only direct neighbors" { style.fill: "#f8fafc" }
iter1: "Iteration 1\\nExchange vectors: Discover 2-hop paths" { style.fill: "#fef3c7" }
iter2: "Iteration 2\\nRelax paths via Bellman-Ford: D_x(y) = min(c(x,v) + D_v(y))" { style.fill: "#e0e7ff" }
conv: "Convergence Reached\\nAll routing tables stable and optimal" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

init -> iter1 -> iter2 -> conv
""",

        # 12. Count-to-Infinity Problem
        "fig3_12_count_to_infinity.svg": """
shape: sequence_diagram

RouterA: "Router A"
RouterB: "Router B"
NetX: "Network X (Fails)"

Note over NetX: Link between Router A and Network X FAILS!
RouterA -> RouterB: "A sets Cost(X) = Inf"
Note over RouterB: B has stale route: B thinks it reaches X via A (Cost 2)!\\nB advertises Cost(X) = 2 to A!
RouterB -> RouterA: "B advertises: X is reachable via B (Cost 2)"
Note over RouterA: A updates: I can reach X via B at Cost = 2 + 1 = 3!
RouterA -> RouterB: "A advertises: X reachable via A (Cost 3)"
Note over RouterB: B updates: Cost = 3 + 1 = 4!
Note over RouterA,RouterB: ROUTING LOOP: Metric counts up: 4 -> 5 -> 6 ... up to 16 (Infinity)!\\nMitigation: Split Horizon, Poison Reverse, Hold-Down Timers
""",

        # 13. Dijkstra SPF Cycle
        "fig3_13_dijkstra_flow.svg": """
direction: down

init: "1. Initialization\\nSet Dist[src]=0, Dist[v]=Inf\\nTentative set = all nodes" { style.fill: "#f8fafc" }
pick: "2. Extract Minimum\\nPick node u with smallest Dist[u] from Tentative set" { style.fill: "#fef3c7" }
relax: "3. Edge Relaxation\\nFor each neighbor v of u:\\nif Dist[u] + cost(u,v) < Dist[v]:\\n  Dist[v] = Dist[u] + cost(u,v)" { style.fill: "#e0e7ff" }
check: "4. Check Termination\\nIs Tentative set empty?" { style.fill: "#f1f5f9" }
done: "5. Shortest Path Tree (SPT) Complete\\nInstall optimal routes into FIB" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

init -> pick -> relax -> check
check -> pick: "No (More nodes)"
check -> done: "Yes (All nodes settled)"
""",

        # 14. Spanning Tree Loop Disaster
        "fig3_14_stp_loop_disasters.svg": """
direction: right

disasters: "Disasters Caused by Layer 2 Physical Loops without STP" {
  d1: "1. Broadcast Storms: Broadcast frames loop infinitely, consuming 100% bandwidth" { style.fill: "#fee2e2" }
  d2: "2. MAC Table Instability: Switch MAC tables thrash continuously as frames arrive from multiple ports" { style.fill: "#fee2e2" }
  d3: "3. Multiple Frame Copies: End hosts receive duplicate copies of unicast frames" { style.fill: "#fee2e2" }
}
""",

        # 15. Physical Loop to Logical Spanning Tree
        "fig3_15_stp_spanning_tree.svg": """
direction: right

PhysicalLoop: "1. Physical Redundant Mesh" {
  SW1: "Root Switch\\n(Bridge ID: 4096.AA)" { style.fill: "#dcfce7" }
  SW2: "Switch 2\\n(Bridge ID: 8192.BB)" { style.fill: "#f8fafc" }
  SW3: "Switch 3\\n(Bridge ID: 32768.CC)" { style.fill: "#f8fafc" }
  SW1 <-> SW2: "Link 1"
  SW2 <-> SW3: "Link 2 (Blocked by STP)" { style.stroke-dash: 4; style.stroke: "#dc2626" }
  SW1 <-> SW3: "Link 3"
}

LogicalTree: "2. Active Logical Tree" {
  LSW1: "Root Bridge" { style.fill: "#dcfce7" }
  LSW2: "Designated Port"
  LSW3: "Root Port"
  LSW1 <-> LSW2: "Forwarding"
  LSW1 <-> LSW3: "Forwarding"
}
""",

        # 16. Wireless Limitations of CSMA/CD
        "fig3_16_wireless_csma_cd_fails.svg": """
direction: right

reasons: "Why CSMA/CD Fails in Wireless Networks" {
  r1: "1. Massive Dynamic Range: Transmitted signal power is millions of times stronger than received signals; transmitters drown out collision detection on the same antenna" { style.fill: "#fee2e2" }
  r2: "2. Hidden Terminal Problem: Collision occurs at receiver, which sender cannot detect" { style.fill: "#fee2e2" }
  r3: "3. Inability to Abort Early: Wireless collisions waste entire frame transmission times" { style.fill: "#fee2e2" }
}
""",

        # 17. Hidden Terminal Problem
        "fig3_17_hidden_terminal.svg": """
direction: right

sta_a: "Station A\\nTransmitting to AP" { style.fill: "#dbeafe" }
ap: "Access Point (AP)\\nIn range of both A and C" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
sta_c: "Station C (Hidden from A)\\nCannot hear A's carrier" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }

sta_a -> ap: "Frame Transmission"
sta_c -> ap: "Simultaneous Transmission\\n(Carrier sense says idle!)"
ap -> ap: "COLLISION AT AP!\\nA and C cannot hear each other" { style.stroke: "#dc2626"; style.bold: true }
""",

        # 18. Exposed Terminal Problem
        "fig3_18_exposed_terminal.svg": """
direction: right

sta_b: "Station B\\n(Wants to send to A)" { style.fill: "#dbeafe" }
sta_c: "Station C\\n(Transmitting to D)" { style.fill: "#fef3c7" }
sta_a: "Station A"
sta_d: "Station D"

sta_c -> sta_d: "Active Transmission"
sta_b -> sta_a: "UNNECESSARY DELAY!\\nB hears C transmitting and defers,\\neven though B->A would NOT collide with C->D!" { style.stroke: "#d97706" }
""",

        # 19. Three Pillars of CSMA/CA
        "fig3_19_csmaca_three_pillars.svg": """
direction: right

p1: "1. Inter-Frame Spaces (IFS)\\nPrioritized waiting times:\\nSIFS < PIFS < DIFS < EIFS" { style.fill: "#dbeafe" }
p2: "2. Contention Window (CW)\\nRandomized binary exponential backoff:\\nBackoff = Rand(0, CW) * SlotTime" { style.fill: "#fef3c7" }
p3: "3. Positive ACKs\\nReceiver confirms every frame;\\nAbsence of ACK triggers backoff doubling" { style.fill: "#dcfce7" }

p1 -> p2 -> p3
""",

        # 20. RTS/CTS Handshake & NAV
        "fig3_20_rts_cts_nav.svg": """
shape: sequence_diagram

Sender: "Sender Station A"
AP: "Access Point"
Other: "Other Stations (C)"

Sender -> AP: "1. RTS (Request To Send: Duration = T)" { style.stroke: "#2563eb" }
AP -> Sender: "2. CTS (Clear To Send: Duration = T - RTS)" { style.stroke: "#16a34a" }
Note over Other: Other stations hear CTS and set Network Allocation Vector (NAV);\\nDefer all transmissions until NAV countdown reaches 0!
Sender -> AP: "3. DATA Frame (Collision Free)" { style.stroke: "#2563eb" }
AP -> Sender: "4. ACK Frame" { style.stroke: "#16a34a" }
""",

        # 21. Complete CSMA/CA Execution Flow
        "fig3_21_csmaca_execution_flow.svg": """
direction: down

start: "Station has frame to send" { style.fill: "#f8fafc" }
sense: "Sense Medium: Is Channel Busy?" { style.fill: "#fef3c7" }
wait_difs: "Wait DIFS duration" { style.fill: "#e0e7ff" }
backoff: "Random Backoff Countdown: Slot decrement while channel idle" { style.fill: "#fef3c7" }
tx: "Transmit RTS or DATA Frame" { style.fill: "#dbeafe" }
ack: "Wait for ACK: Did ACK arrive?" { style.fill: "#f1f5f9" }
success: "Transmission SUCCESS\\nReset CW = CWmin" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
double_cw: "Collision Detected (Timeout)\\nDouble CW = min(2*CW, CWmax)" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }

start -> sense
sense -> wait_difs: "Channel Idle"
sense -> sense: "Channel Busy (Wait)"
wait_difs -> backoff -> tx -> ack
ack -> success: "ACK Received"
ack -> double_cw: "Timeout (No ACK)"
double_cw -> backoff: "Retry"
""",

        # 22. MTU Fragmentation Walkthrough
        "fig3_22_fragmentation_table.svg": """
direction: right

summary: "MTU 1500-Byte IP Datagram Fragmentation Breakdown" {
  f1: "Fragment 1: Bytes 0 – 1479 (1480B Data)\\nTotal Length: 1500B, MF=1, Offset = 0 / 8 = 0" { style.fill: "#dbeafe" }
  f2: "Fragment 2: Bytes 1480 – 2959 (1480B Data)\\nTotal Length: 1500B, MF=1, Offset = 1480 / 8 = 185" { style.fill: "#dbeafe" }
  f3: "Fragment 3: Bytes 2960 – 3979 (1020B Data)\\nTotal Length: 1040B, MF=0, Offset = 2960 / 8 = 370" { style.fill: "#dcfce7" }
}
""",

        # 23. Subnet Division Hierarchy
        "fig3_23_subnet_division.svg": """
direction: right

base: "Class C Base Network\\n192.168.1.0/24 (256 Addresses)" { style.fill: "#f8fafc" }
sn1: "Subnet 1: 192.168.1.0/26\\nRange: .0 – .63 (62 Usable Hosts)\\nMask: 255.255.255.192" { style.fill: "#dbeafe" }
sn2: "Subnet 2: 192.168.1.64/26\\nRange: .64 – .127 (62 Usable Hosts)\\nMask: 255.255.255.192" { style.fill: "#e0e7ff" }
sn3: "Subnet 3: 192.168.1.128/26\\nRange: .128 – .191 (62 Usable Hosts)\\nMask: 255.255.255.192" { style.fill: "#fef3c7" }
sn4: "Subnet 4: 192.168.1.192/26\\nRange: .192 – .255 (62 Usable Hosts)\\nMask: 255.255.255.192" { style.fill: "#fee2e2" }

base -> sn1
base -> sn2
base -> sn3
base -> sn4
""",

        # 24. Autonomous System Hierarchy
        "fig3_24_as_routing_hierarchy.svg": """
direction: right

as1: "Autonomous System 100\\n(Enterprise ISP)\\nInternal: OSPF / IS-IS" { style.fill: "#dbeafe" }
as2: "Autonomous System 200\\n(Tier 1 Backbone)\\nInternal: OSPF / IS-IS" { style.fill: "#dcfce7" }

as1 <-> as2: "BGP-4 (Border Gateway Protocol)\\nInter-Domain Path Vector Peering (Port 179)" { style.stroke: "#dc2626"; style.bold: true }
""",

        # 25. OSPF Two-Tier Hierarchy
        "fig3_25_ospf_areas.svg": """
direction: down

bb: "Backbone Area 0 (0.0.0.0)\\nCore transit area interconnecting all sub-areas" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
  style.bold: true
}

a1: "Standard Area 1\\nInternal Routers" { style.fill: "#dbeafe" }
a2: "Standard Area 2\\nInternal Routers" { style.fill: "#dcfce7" }
abr: "Area Border Routers (ABR)\\nMaintains separate LSDB per area" { style.fill: "#fef3c7"; style.stroke: "#d97706" }

bb <-> abr
abr <-> a1
abr <-> a2
""",

        # 27. BGP Autonomous System Peering
        "fig3_27_bgp_peering.svg": """
direction: right

as_google: "AS 15169 (Google)\\nPrefix: 8.8.8.0/24" { style.fill: "#dbeafe" }
as_transit: "AS 3356 (Lumen / Level 3)\\nTransit Backbone" { style.fill: "#fef3c7" }
as_isp: "AS 7018 (AT&T)\\nAccess Provider" { style.fill: "#dcfce7" }

as_google -> as_transit: "BGP eBGP: AS-PATH: [15169]"
as_transit -> as_isp: "BGP eBGP: AS-PATH: [3356, 15169]"
""",

        # 28. Evolution of Configuration Protocols
        "fig3_28_dhcp_evolution.svg": """
direction: right

rarp: "RARP (RFC 903, 1984)\\n• Layer 2 broadcast only\\n• Cannot cross routers\\n• IP address only (no mask/gateway)" { style.fill: "#f8fafc" }
bootp: "BOOTP (RFC 951, 1985)\\n• UDP transport (:67/:68)\\n• Routable via BOOTP Relay\\n• Static IP mapping only" { style.fill: "#fef3c7" }
dhcp: "DHCP (RFC 2131, 1997)\\n• Dynamic IP leasing\\n• Automatic pool management\\n• Rich vendor options (DNS, NTP, Domain)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

rarp -> bootp -> dhcp
""",

        # 29. DHCP Allocation Modes
        "fig3_29_dhcp_allocation_modes.svg": """
direction: right

m1: "1. Dynamic Allocation\\nTemporary lease from IP pool\\nAuto-reclaimed after expiration" { style.fill: "#dbeafe" }
m2: "2. Automatic Allocation\\nPermanent IP assigned from pool\\nNo lease expiration" { style.fill: "#fef3c7" }
m3: "3. Static / Manual Allocation\\nFixed IP reservation bound to MAC\\nIdeal for servers, printers, gateways" { style.fill: "#dcfce7" }

m1 -> m2 -> m3
""",

        # 30. DHCP 4-Step DORA Exchange
        "fig3_30_dhcp_dora_lifecycle.svg": """
shape: sequence_diagram

Client: "Client (0.0.0.0:68)"
Server: "DHCP Server (255.255.255.255:67)"

Client -> Server: "1. DHCPDISCOVER (Broadcast: 255.255.255.255:67)\\nciaddr=0.0.0.0, chaddr=MAC_Client" { style.stroke: "#2563eb" }
Server -> Client: "2. DHCPOFFER (Unicast/Broadcast: yiaddr=192.168.1.50)\\nLease=86400s, Mask=255.255.255.0, Router=192.168.1.1" { style.stroke: "#16a34a" }
Client -> Server: "3. DHCPREQUEST (Broadcast: Confirm selected 192.168.1.50)" { style.stroke: "#2563eb" }
Server -> Client: "4. DHCPACK (Final Confirmation: Lease begins)" { style.stroke: "#16a34a" }
Note over Client: Client verifies IP via Gratuitous ARP (prevents duplicate IPs)!
""",

        # 32. Cross-Subnet DHCP Relay Architecture
        "fig3_32_dhcp_relay_agent.svg": """
direction: right

client: "DHCP Client\\nSubnet 10.0.1.0/24\\nBroadcasts DISCOVER" { style.fill: "#eff6ff" }
relay: "DHCP Relay Agent (Router)\\n'ip helper-address 10.0.2.100'\\nAdds giaddr = 10.0.1.1" { style.fill: "#fef3c7"; style.stroke: "#d97706"; style.bold: true }
server: "Central DHCP Server\\n10.0.2.100\\nAllocates from Subnet 1 pool" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

client -> relay: "1. Layer 2 Broadcast (:67)"
relay -> server: "2. Unicast UDP to 10.0.2.100:67"
server -> relay: "3. Unicast DHCPOFFER"
relay -> client: "4. Broadcast / Unicast to Client"
""",

        # 33. Root Causes of Congestion
        "fig3_33_congestion_causes.svg": """
direction: right

causes: "Root Causes of Network Congestion" {
  c1: "1. Output Port Buffer Exhaustion: Inflow rate > Link transmission capacity" { style.fill: "#fee2e2" }
  c2: "2. High Bursts of Traffic: Sudden traffic spikes exceed buffer depth" { style.fill: "#fee2e2" }
  c3: "3. Retransmission Cascades: Lost packets trigger aggressive retransmissions, worsening congestion" { style.fill: "#fee2e2" }
}
""",

        # 35. Congestion Control Taxonomy
        "fig3_35_congestion_taxonomy.svg": """
direction: right

open_loop: "Open-Loop (Preventative)\\n• Traffic Shaping (Leaky Bucket, Token Bucket)\\n• Admission Control\\n• Packet Discard Policies" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
closed_loop: "Closed-Loop (Reactive)\\n• Explicit Congestion Notification (ECN)\\n• Choke Packets\\n• Hop-by-Hop Backpressure" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

open_loop -> closed_loop
""",

        # 36. Leaky Bucket Algorithm
        "fig3_36_leaky_bucket.svg": """
direction: down

inflow: "Bursty Inbound Packets (Variable Rate)" { style.fill: "#fee2e2" }
bucket: "Leaky Bucket Buffer (FIFO Queue: Capacity C)\\nDiscards packets if queue full!" { style.fill: "#dbeafe"; style.stroke: "#2563eb"; style.bold: true }
outflow: "Constant Outflow Rate (Smooth Traffic Stream)" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

inflow -> bucket -> outflow
""",

        # 37. Token Bucket Algorithm
        "fig3_37_token_bucket.svg": """
direction: down

gen: "Token Generator (Generates r tokens / sec)" { style.fill: "#fef3c7" }
bucket: "Token Bucket (Holds up to Capacity C tokens)" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
tx: "Transmitter: Packet transmitted ONLY if sufficient tokens available!\\nPermits controlled bursts up to peak rate M" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

gen -> bucket -> tx
""",

        # 38. Closed Loop Feedback Methods
        "fig3_38_closed_loop_methods.svg": """
direction: right

m1: "1. Hop-by-Hop Backpressure\\nCongested router pauses upstream router node-by-node" { style.fill: "#fee2e2" }
m2: "2. Choke Packets\\nCongested router sends direct ICMP Source Quench / Choke to original source" { style.fill: "#fef3c7" }
m3: "3. ECN (Explicit Congestion Notification)\\nMarks CE bits (11) in IPv4/IPv6 header; receiver returns ECE in TCP ACK" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

m1 -> m2 -> m3
""",

        # 39. Hop by Hop Backpressure
        "fig3_39_backpressure_flow.svg": """
direction: right

src: "Source Host"
r1: "Router 1"
r2: "Router 2"
r3: "Router 3 (Congested!)" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }

r3 -> r2: "1. Backpressure Pause!" { style.stroke: "#dc2626"; style.bold: true }
r2 -> r1: "2. Buffers fill at R2 -> Backpressure to R1!" { style.stroke: "#dc2626" }
r1 -> src: "3. Source throttled at edge!" { style.stroke: "#dc2626" }
""",

        # 40. ECN Sequence (RFC 3168)
        "fig3_40_ecn_sequence.svg": """
shape: sequence_diagram

Sender: "TCP Sender"
Router: "Congested Core Router"
Receiver: "TCP Receiver"

Sender -> Router: "IP Packet: ECN-Capable (ECT=10)" { style.stroke: "#2563eb" }
Note over Router: RED queue exceeds threshold;\\nRouter sets CE bits: ECN = 11 (Congestion Encountered)!
Router -> Receiver: "IP Packet with CE=11 forwarded" { style.stroke: "#dc2626" }
Note over Receiver: Receiver detects CE=11;\\nSets ECE (ECN-Echo) flag in next TCP ACK!
Receiver -> Sender: "TCP ACK with ECE=1 flag" { style.stroke: "#dc2626"; style.bold: true }
Note over Sender: Sender receives ECE;\\nHalves cwnd (AIMD reduction without packet drop)!\\nSends CWR (Congestion Window Reduced) flag!
Sender -> Receiver: "Next TCP Segment with CWR=1" { style.stroke: "#16a34a" }
""",

        # 41. TCP/IP Network Layer Suite Overview
        "fig3_41_network_layer_suite.svg": """
direction: down

upper: "Upper Layers: Transport (TCP / UDP) & Application" { style.fill: "#f8fafc" }

Suite: "TCP/IP Network Layer Protocol Suite" {
  ip: "IPv4 / IPv6 (Host-to-Host Data Transfer)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
  icmp: "ICMP (Diagnostic Reporting & Ping)" { style.fill: "#fef3c7" }
  arp: "ARP / RARP (MAC <-> IP Resolution)" { style.fill: "#dbeafe" }
  igmp: "IGMP (Multicast Group Management)" { style.fill: "#f3e8ff" }
  bgp: "BGP / OSPF / RIP (Routing Protocols)" { style.fill: "#fee2e2" }
}

lower: "Data Link Layer: Ethernet / Wi-Fi" { style.fill: "#f8fafc" }

upper -> ip -> lower
ip <-> icmp
ip <-> arp
ip <-> igmp
ip <-> bgp
""",

        # 42. IPv6 Architectural Advantages
        "fig3_42_ipv6_advantages.svg": """
direction: right

adv: "Key Architectural Advantages of IPv6" {
  a1: "1. Vast 128-Bit Address Space (3.4 x 10^38 IPs: Eliminates NAT)" { style.fill: "#dcfce7" }
  a2: "2. Fixed 40-Byte Base Header: Faster router hardware processing" { style.fill: "#dbeafe" }
  a3: "3. Stateless Address Autoconfiguration (SLAAC): Plug-and-play" { style.fill: "#fef3c7" }
  a4: "4. Built-in Security: Mandatory IPsec support (AH & ESP)" { style.fill: "#f3e8ff" }
  a5: "5. Elimination of Broadcast: Replaced by efficient Multicast / Anycast" { style.fill: "#e0e7ff" }
}
""",

        # 43. Core Roles of ICMP
        "fig3_43_icmp_roles.svg": """
direction: right

roles: "Core Roles of ICMPv4 (RFC 792)" {
  r1: "1. Diagnostic Queries: Echo Request (Type 8) & Reply (Type 0) -> ping utility" { style.fill: "#dcfce7" }
  r2: "2. Error Reporting: Destination Unreachable (Type 3: Network, Host, Port unreachable)" { style.fill: "#fee2e2" }
  r3: "3. Hop Limit Expiration: Time Exceeded (Type 11) -> traceroute utility" { style.fill: "#fef3c7" }
  r4: "4. Parameter Problem: Corrupted header fields (Type 12)" { style.fill: "#e0e7ff" }
}
""",

        # 44. ARP Resolution Workflow
        "fig3_44_arp_workflow.svg": """
shape: sequence_diagram

HostA: "Host A (10.0.0.1)"
Broadcast: "All Hosts (Broadcast Domain)"
HostB: "Host B (10.0.0.2)"

HostA -> Broadcast: "1. ARP Request (Broadcast: FF:FF:FF:FF:FF:FF)\\n'Who has 10.0.0.2? Tell 10.0.0.1'" { style.stroke: "#2563eb" }
Note over Broadcast: All hosts inspect packet; non-targets discard silently
HostB -> HostA: "2. ARP Reply (Unicast to MAC_A)\\n'10.0.0.2 is at MAC_B'" { style.stroke: "#16a34a"; style.bold: true }
Note over HostA: Host A caches MAC_B in ARP table (TTL 20m) and transmits pending IP packet!
""",

        # 45. RARP Diskless Bootstrap
        "fig3_45_rarp_bootstrap.svg": """
shape: sequence_diagram

Client: "Diskless Workstation"
Server: "RARP Server"

Client -> Server: "1. RARP Request (Broadcast: FF:FF:FF:FF:FF:FF)\\n'My MAC is 08:00:20:01:02:03. What is my IP?'" { style.stroke: "#2563eb" }
Note over Server: Server consults static /etc/ethers table mapping MAC to IP
Server -> Client: "2. RARP Reply (Unicast: IP = 192.168.1.55)" { style.stroke: "#16a34a" }
Note over Client: Workstation configures network interface; loads OS via TFTP!
""",

        # 46. IGMP Multicast Membership
        "fig3_46_igmp_membership.svg": """
shape: sequence_diagram

Host: "Multicast Receiver"
Router: "Multicast Router (PIM/IGMP)"

Host -> Router: "1. IGMP Membership Report: Join Group 224.2.0.1" { style.stroke: "#2563eb" }
Note over Router: Router adds port to Multicast Forwarding Tree for 224.2.0.1
Router -> Host: "2. IGMP General Query (224.0.0.1): Are members still active?"
Host -> Router: "3. Membership Report (Delayed response confirms interest)" { style.stroke: "#16a34a" }
Host -> Router: "4. IGMP Leave Group (224.0.0.2): Leaving 224.2.0.1" { style.stroke: "#dc2626" }
""",

        # 47. BGP Inter-Domain Peering
        "fig3_47_bgp_interdomain.svg": """
direction: right

as10: "AS 10 (Enterprise LAN)\\nRouter A (BGP Speaker)" { style.fill: "#dbeafe" }
as20: "AS 20 (Internet Service Provider)\\nRouter B (BGP Speaker)" { style.fill: "#dcfce7" }

as10 <-> as20: "TCP Port 179 Peering\\nExchanges NLRI & AS-PATH Attributes\\nEnforces routing policy" { style.stroke: "#dc2626"; style.bold: true }
"""
    }

    for filename, code in d2_diagrams.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        svg_engine.compile_d2(code, out_path, theme=1)
    print(f"  Generated {len(d2_diagrams)} D2 publication diagrams.")

generate_d2_diagrams()
print("\nUnit 3 figure generation complete!")
