#!/usr/bin/env python3
"""
scripts/figures/generate_unit4.py
Generates all publication-grade figures for UNIT 4 (Transport Layer).
Produces SVGs in UNIT - 4/figures/
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_engine

OUTPUT_DIR = os.path.abspath("UNIT - 4/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating Unit 4 figures in: {OUTPUT_DIR}")

# ==============================================================================
# 1. 32-Bit Packet Headers (Python Vector SVG Engine)
# ==============================================================================

def generate_headers():
    # 1. UDP Header (8 bytes = 2 rows of 32 bits)
    udp_rows = [
        [("Source Port", 16, "port", "16 Bits (Optional / Ephemeral)"),
         ("Destination Port", 16, "port", "16 Bits (Server Service Port)")],
        [("Length", 16, "length", "16 Bits (Header + Data Length in Octets)"),
         ("Checksum", 16, "checksum", "16 Bits (1's Complement Sum over Pseudo-Header)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 768: User Datagram Protocol (UDP) Header (8 Octets)",
        udp_rows,
        os.path.join(OUTPUT_DIR, "fig4_hdr_udp.svg")
    )

    # 2. UDP Pseudo-Header (IPv4)
    pseudo_rows = [
        [("Source IPv4 Address", 32, "address", "32 Bits (From IPv4 Packet Header)")],
        [("Destination IPv4 Address", 32, "address", "32 Bits (From IPv4 Packet Header)")],
        [("All Zeros", 8, "reserved", "8b (0x00)"),
         ("Protocol", 8, "type", "8b (0x11 = 17 for UDP)"),
         ("UDP Length", 16, "length", "16 Bits (Matches UDP Header Length)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "IPv4 / UDP Pseudo-Header Layout (12 Octets for Checksum Calculation)",
        pseudo_rows,
        os.path.join(OUTPUT_DIR, "fig4_hdr_pseudo_udp.svg")
    )

    # 3. TCP Segment Header (20-60 bytes)
    tcp_rows = [
        [("Source Port", 16, "port", "16 Bits (Calling Process)"),
         ("Destination Port", 16, "port", "16 Bits (Destination Service)")],
        [("Sequence Number", 32, "seq", "32 Bits (Initial Seq Num or First Byte in Segment)")],
        [("Acknowledgment Number", 32, "ack", "32 Bits (Next Expected In-Order Byte from Peer)")],
        [("Data Offset", 4, "meta", "4b (HLEN in 32b words)"),
         ("Reserved", 4, "reserved", "4b (Must be 0)"),
         ("Flags (C E U A P R S F)", 8, "flag", "8b (CWR, ECE, URG, ACK, PSH, RST, SYN, FIN)"),
         ("Window Size (rwnd)", 16, "length", "16 Bits (Flow Control Buffer Credit in Bytes)")],
        [("Checksum", 16, "checksum", "16 Bits (1's Complement with Pseudo-Header)"),
         ("Urgent Pointer", 16, "control", "16 Bits (Offset from Seq Num if URG=1)")],
        [("Options & Padding (0 to 40 Bytes: MSS, Window Scale, SACK, Timestamps)", 32, "options", "Variable (Padded to 32-bit boundary)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 793 / RFC 9293: Transmission Control Protocol (TCP) Header (20–60 Octets)",
        tcp_rows,
        os.path.join(OUTPUT_DIR, "fig4_hdr_tcp.svg")
    )

    # 4. SCTP Common Header (12 bytes)
    sctp_rows = [
        [("Source Port", 16, "port", "16 Bits (SCTP Sender Port)"),
         ("Destination Port", 16, "port", "16 Bits (SCTP Receiver Port)")],
        [("Verification Tag", 32, "crypto", "32 Bits (Association Integrity Key / Anti-Spoofing)")],
        [("Checksum", 32, "checksum", "32 Bits (CRC-32c Polynomial Calculation)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 4960: SCTP Common Packet Header (12 Octets)",
        sctp_rows,
        os.path.join(OUTPUT_DIR, "fig4_hdr_sctp_common.svg")
    )

    # 5. SCTP DATA Chunk Structure
    sctp_data_rows = [
        [("Chunk Type = 0 (DATA)", 8, "type", "8b (0x00)"),
         ("Flags (U B E I)", 8, "flag", "8b (Unordered, Begin, End)"),
         ("Chunk Length", 16, "length", "16 Bits (Header + User Data)")],
        [("Transmission Sequence Number (TSN)", 32, "seq", "32 Bits (Association-Wide Sequence)")],
        [("Stream Identifier (SID)", 16, "port", "16 Bits (0 to 65,535)"),
         ("Stream Sequence Number (SSN)", 16, "seq", "16 Bits (Stream-Local Sequence)")],
        [("Payload Protocol Identifier (PPID)", 32, "meta", "32 Bits (Upper Layer Protocol ID)")],
        [("User Application Data Payload", 32, "address", "Variable Length Data (Padded to 32 bits)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 4960: SCTP DATA Chunk Layout",
        sctp_data_rows,
        os.path.join(OUTPUT_DIR, "fig4_hdr_sctp_data.svg")
    )

generate_headers()
print("  Generated all 32-bit packet headers.")

# ==============================================================================
# 2. Matplotlib Publication Plots (IEEE/ACM Scientific Curves)
# ==============================================================================

def generate_scientific_plots():
    svg_engine.configure_matplotlib_style()

    # Fig 4.19: TCP Tahoe vs. Reno AIMD Congestion Control Curve
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
    
    rtts = np.arange(0, 24, 0.2)
    cwnd_reno = []
    cwnd_tahoe = []
    
    for time in rtts:
        if time <= 4:
            w_r = min(16, 2 ** time)
            w_t = w_r
        elif time < 12:
            w_r = 16 + (time - 4) * 1.5
            w_t = w_r
        elif time == 12:
            w_r = 14 + 3 # Reno Fast Recovery
            w_t = 1     # Tahoe resets to 1
        elif 12 < time < 16:
            w_r = 17 + (time - 12) * 1.5
            w_t = min(14, 2 ** (time - 12))
        else:
            w_r = 17 + (time - 12) * 1.5
            w_t = 14 + (time - 16) * 1.5
        cwnd_reno.append(w_r)
        cwnd_tahoe.append(w_t)

    # Shaded background regions
    ax.axvspan(0, 4, color='#f8fafc', alpha=0.8)
    ax.axvspan(4, 12, color='#f1f5f9', alpha=0.5)
    ax.axvspan(12, 16, color='#eff6ff', alpha=0.5)

    ax.plot(rtts, cwnd_reno, label='TCP Reno (Fast Recovery: Halves cwnd)', color='#2563eb', linewidth=2.5)
    ax.plot(rtts, cwnd_tahoe, label='TCP Tahoe (Slow Start upon Loss: Resets cwnd = 1)', color='#dc2626', linewidth=2.0, linestyle='--')

    ax.axhline(y=16, color='#64748b', linestyle=':', label='Initial ssthresh (16 MSS)')
    ax.axhline(y=14, color='#d97706', linestyle='-.', label='New ssthresh = cwnd / 2 (14 MSS)')
    ax.axvline(x=12, color='#ef4444', linestyle=':', alpha=0.9)

    ax.annotate('Slow Start\n(Exponential Doubling)', xy=(2, 4), xytext=(0.8, 18),
                arrowprops=dict(facecolor='#64748b', shrink=0.08, width=1, headwidth=5),
                fontsize=9, fontweight='bold', color='#334155',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#cbd5e1'))

    ax.annotate('Congestion Avoidance\n(Additive Increase: +1 MSS/RTT)', xy=(8, 22), xytext=(5.5, 27),
                arrowprops=dict(facecolor='#2563eb', shrink=0.08, width=1, headwidth=5),
                fontsize=9, fontweight='bold', color='#1e40af',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#bfdbfe'))

    ax.annotate('3 Duplicate ACKs\n(Loss Detected)', xy=(12, 28), xytext=(12.5, 30),
                arrowprops=dict(facecolor='#ef4444', shrink=0.08, width=1.2, headwidth=6),
                fontsize=9, fontweight='bold', color='#991b1b',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef2f2', edgecolor='#fca5a5'))

    ax.set_title('Figure 4.19: TCP Tahoe vs. Reno Congestion Window Dynamics (AIMD Phases)', 
                 fontsize=12, fontweight='bold', pad=12, color='#0f172a')
    ax.set_xlabel('Elapsed Transmission Time (Round Trip Times — RTT)', fontsize=10, fontweight='bold', labelpad=8)
    ax.set_ylabel('Congestion Window Size ($cwnd$ in MSS)', fontsize=10, fontweight='bold', labelpad=8)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 36)
    ax.legend(loc='upper left', frameon=True, framealpha=0.95, facecolor='#ffffff', edgecolor='#cbd5e1')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig4_19_tcp_congestion_curve.svg"), format='svg')
    plt.close()

generate_scientific_plots()
print("  Generated scientific performance curves.")

# ==============================================================================
# 3. Graphviz DOT State Machines
# ==============================================================================

def generate_dot_diagrams():
    # Fig 4.16: Complete TCP 11-State Finite State Machine (FSM)
    fsm_dot = """
    digraph TCP_FSM {
        graph [rankdir=TB, bgcolor="transparent", fontname="Helvetica", pad="0.2", nodesep="0.4", ranksep="0.5"];
        node [shape=box, style="filled,rounded", fontname="Helvetica-Bold", fontsize=9, margin="0.15,0.08", fillcolor="#f8fafc", color="#64748b", penwidth=1.3];
        edge [fontname="Helvetica", fontsize=8, color="#334155", penwidth=1.1, arrowsize=0.7];

        CLOSED [fillcolor="#fee2e2", color="#dc2626", fontcolor="#991b1b", penwidth=2.0];
        LISTEN [fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        SYN_SENT [fillcolor="#e0e7ff", color="#4338ca", fontcolor="#312e81"];
        SYN_RCVD [fillcolor="#e0e7ff", color="#4338ca", fontcolor="#312e81"];
        ESTABLISHED [fillcolor="#dcfce7", color="#16a34a", fontcolor="#14532d", penwidth=2.2];
        
        FIN_WAIT_1 [fillcolor="#f3e8ff", color="#7e22ce", fontcolor="#581c87"];
        FIN_WAIT_2 [fillcolor="#f3e8ff", color="#7e22ce", fontcolor="#581c87"];
        CLOSING [fillcolor="#fef3c7", color="#b45309", fontcolor="#78350f"];
        TIME_WAIT [fillcolor="#fee2e2", color="#b91c1c", fontcolor="#7f1d1d"];
        CLOSE_WAIT [fillcolor="#fef3c7", color="#b45309", fontcolor="#78350f"];
        LAST_ACK [fillcolor="#ffedd5", color="#c2410c", fontcolor="#7c2d12"];

        CLOSED -> LISTEN [label=" Passive Open (Server)"];
        CLOSED -> SYN_SENT [label=" Active Open / Send SYN"];
        LISTEN -> SYN_RCVD [label=" Recv SYN / Send SYN+ACK"];
        SYN_SENT -> ESTABLISHED [label=" Recv SYN+ACK / Send ACK", color="#16a34a", fontcolor="#15803d", penwidth=1.5];
        SYN_RCVD -> ESTABLISHED [label=" Recv ACK", color="#16a34a", fontcolor="#15803d", penwidth=1.5];
        
        ESTABLISHED -> FIN_WAIT_1 [label=" Active Close / Send FIN", color="#7e22ce"];
        ESTABLISHED -> CLOSE_WAIT [label=" Passive Close: Recv FIN / Send ACK", color="#d97706"];
        
        FIN_WAIT_1 -> FIN_WAIT_2 [label=" Recv ACK"];
        FIN_WAIT_1 -> CLOSING [label=" Simultaneous Close: Recv FIN"];
        FIN_WAIT_2 -> TIME_WAIT [label=" Recv FIN / Send ACK", color="#dc2626"];
        CLOSING -> TIME_WAIT [label=" Recv ACK"];
        
        TIME_WAIT -> CLOSED [label=" Timeout: 2 * MSL (Flush old dup packets)", style="dashed", color="#dc2626"];
        CLOSE_WAIT -> LAST_ACK [label=" App Close / Send FIN"];
        LAST_ACK -> CLOSED [label=" Recv ACK"];
    }
    """
    svg_engine.compile_dot(fsm_dot, os.path.join(OUTPUT_DIR, "fig4_16_tcp_fsm.svg"))

generate_dot_diagrams()
print("  Generated Graphviz DOT state machines.")

# ==============================================================================
# 4. D2 Publication Diagrams (Architectures, Flows & Sequences)
# ==============================================================================

def generate_d2_diagrams():
    d2_diagrams = {
        # 1. Delivery Hierarchy
        "fig4_01_delivery_hierarchy.svg": """
direction: down

app_layer: "Application Layer\\n(Process-to-Process: Ports)" {
  style.fill: "#eff6ff"
  style.stroke: "#2563eb"
}

trans_layer: "Transport Layer (TCP / UDP)\\nProcess Addressing & Socket Demux" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
  style.bold: true
}

net_layer: "Network Layer (IPv4 / IPv6)\\nHost-to-Host Delivery (IP Addresses)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

link_layer: "Data Link Layer (Ethernet / Wi-Fi)\\nHop-to-Hop Framing (MAC Addresses)" {
  style.fill: "#f1f5f9"
  style.stroke: "#64748b"
}

app_layer -> trans_layer: "Inter-Process Data Stream"
trans_layer -> net_layer: "Segments / Datagrams"
net_layer -> link_layer: "IP Packets"
""",

        # 2. Sockets and Addressing
        "fig4_02_sockets_addressing.svg": """
direction: right

host_a: "Host A (192.168.1.10)" {
  p1: "Browser (PID 1042)\\nPort 51234" {
    style.fill: "#e0e7ff"
  }
}

host_b: "Host B (203.0.113.80)" {
  p2: "Web Server (PID 800)\\nPort 80 (HTTP)" {
    style.fill: "#dcfce7"
  }
  p3: "SSH Daemon (PID 412)\\nPort 22 (SSH)" {
    style.fill: "#fee2e2"
  }
}

host_a.p1 -> host_b.p2: "TCP Socket Pair: (192.168.1.10:51234, 203.0.113.80:80)" {
  style.stroke: "#2563eb"
  style.bold: true
}
""",

        # 3. Port Number Ranges
        "fig4_03_port_ranges.svg": """
direction: right

well_known: "Well-Known Ports\\nRange: 0 – 1023\\nAssigned by IANA\\nPrivileged / System Services\\n(HTTP: 80, HTTPS: 443, SSH: 22)" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

registered: "Registered Ports\\nRange: 1024 – 49151\\nRegistered by Vendors\\nUser Applications\\n(MySQL: 3306, Redis: 6379)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

ephemeral: "Dynamic / Ephemeral Ports\\nRange: 49152 – 65535\\nOperating System Assigned\\nTemporary Client Sockets\\n(Auto-released upon close)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

well_known -> registered -> ephemeral
""",

        # 4. Multiplexing & Demultiplexing
        "fig4_04_multiplexing_demux.svg": """
direction: down

clients: "Concurrent Client Processes" {
  c1: "Browser Tab 1 (:51001)"
  c2: "Browser Tab 2 (:51002)"
  c3: "Email Client (:51003)"
}

mux: "Sender Transport Layer\\nMultiplexing into IP Datagrams" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
}

net: "Underlying IP Network (Host-to-Host)" {
  style.fill: "#f8fafc"
}

demux: "Receiver Transport Layer\\nDemultiplexing via Port Numbers" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

servers: "Server Daemons" {
  s1: "Web Server (:80)"
  s2: "Mail Server (:25)"
}

clients.c1 -> mux
clients.c2 -> mux
clients.c3 -> mux
mux -> net -> demux
demux -> servers.s1
demux -> servers.s2
""",

        # 5. Connection-Oriented vs Connectionless
        "fig4_05_connection_paradigms.svg": """
direction: right

connectionless: "Connectionless (UDP)\\n• No Handshake\\n• Stateless\\n• Message-Oriented\\n• Low Overhead (8B Header)\\n• Best for Real-Time / Streaming" {
  style.fill: "#eff6ff"
  style.stroke: "#3b82f6"
}

connection_oriented: "Connection-Oriented (TCP)\\n• 3-Way Handshake\\n• Stateful (TCB Records)\\n• Byte-Stream Abstraction\\n• Reliable Delivery & ARQ\\n• Congestion & Flow Control" {
  style.fill: "#ecfdf5"
  style.stroke: "#10b981"
}
""",

        # 6. Flow Control (Hop-by-Hop vs End-to-End)
        "fig4_06_flow_control_types.svg": """
shape: sequence_diagram

Sender: "Sender Process"
Receiver: "Receiver Process"

Sender -> Receiver: "Data Segment (1460 Bytes)"
Receiver -> Sender: "ACK + Advertised Window rwnd = 64KB"
Sender -> Receiver: "Burst Data Segments (64KB)"
Note over Receiver: Receiver Buffer Full!\\nApplication reading slowly
Receiver -> Sender: "ACK + Zero Window Update (rwnd = 0)"
Note over Sender: Sender pauses transmission;\\nStarts Persistence Timer probe
""",

        # 7. Error Control Pillars
        "fig4_07_error_control_pillars.svg": """
direction: right

p1: "1. Byte Sequence Numbers\\nOrder tracking & missing byte detection" {
  style.fill: "#e0e7ff"
}

p2: "2. Cumulative / Selective ACKs\\nConfirm received byte sequences" {
  style.fill: "#dcfce7"
}

p3: "3. Retransmission Timers (RTO)\\nAutomatic Repeat Request (ARQ)" {
  style.fill: "#fef3c7"
}

p4: "4. Checksums\\nHeader and payload corruption verification" {
  style.fill: "#fee2e2"
}
""",

        # 8. Congestion Collapse Dynamics
        "fig4_08_congestion_dynamics.svg": """
direction: right

senders: "Fast Senders\\nInjecting high load" {
  style.fill: "#e0f2fe"
}

switch: "Bottleneck Router\\nLimited buffer queue" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

receiver: "Receiver Host" {
  style.fill: "#ecfdf5"
}

senders -> switch: "Packet Arrival > Service Rate"
switch -> receiver: "Severe Packet Loss / Drops"
""",

        # 9. RFC 768 UDP Design Philosophy
        "fig4_09_udp_philosophy.svg": """
direction: right

udp_core: "UDP Design Rationale (RFC 768)\\n• Minimalist Transport Wrapper\\n• No Handshake Latency (0 RTT)\\n• No Head-of-Line Blocking\\n• Un-throttled Sending Rate\\n• Preserves Message Boundaries" {
  style.fill: "#eff6ff"
  style.stroke: "#2563eb"
  style.bold: true
}
""",

        # 10. UDP Message-Oriented Framing
        "fig4_10_udp_framing.svg": """
direction: right

app_msg: "Application Record\\n(e.g., 512-byte DNS Query)" {
  style.fill: "#f8fafc"
}

udp_pkt: "UDP Datagram\\n[8B Header | 512B Exact Payload]" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
}

ip_pkt: "IP Packet\\n[20B IP Header | UDP Datagram]" {
  style.fill: "#fef3c7"
}

app_msg -> udp_pkt: "1:1 Exact Record Preservation\\n(No segment chunking)"
udp_pkt -> ip_pkt: "Network Transit"
""",

        # 11. UDP Demultiplexing
        "fig4_11_udp_demux.svg": """
direction: right

client1: "Client 1\\n10.0.0.1:48210"
client2: "Client 2\\n10.0.0.2:59432"

dns_server: "DNS Server (Port 53)\\n2-Tuple Demux (Dest IP, Dest Port)" {
  style.fill: "#ecfdf5"
  style.stroke: "#059669"
}

client1 -> dns_server: "UDP Query to Port 53"
client2 -> dns_server: "UDP Query to Port 53"
""",

        # 12. UDP DNS Amplification Attack
        "fig4_12_udp_amplification.svg": """
direction: right

attacker: "Attacker (Botnet)\\nForged Source IP = Victim" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

open_dns: "Open DNS Resolvers\\n(Reflectors)" {
  style.fill: "#fef3c7"
}

victim: "Target Victim Server\\nOverwhelmed by Traffic" {
  style.fill: "#fee2e2"
  style.stroke: "#b91c1c"
  style.bold: true
}

attacker -> open_dns: "Small 60B Query (ANY type)"
open_dns -> victim: "Amplified 3000B+ Response\\n(50x - 70x Amplification)" {
  style.stroke: "#dc2626"
  style.bold: true
}
""",

        # 13. TCP Virtual Circuit
        "fig4_13_tcp_virtual_circuit.svg": """
direction: right

app_src: "Application Stream\\nByte 0 ... Byte N" {
  style.fill: "#eff6ff"
}

tcp_pipe: "TCP Full-Duplex Virtual Circuit\\nReliable, In-Order Byte-Stream Pipe" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

app_dst: "Application Stream\\nByte 0 ... Byte N" {
  style.fill: "#eff6ff"
}

app_src -> tcp_pipe -> app_dst
""",

        # 14. TCP 3-Way Handshake
        "fig4_14_tcp_3way_handshake.svg": """
shape: sequence_diagram

Client: "Host A (Client)"
Server: "Host B (Server)"

Note over Server: Server in LISTEN State
Client -> Server: "1. SYN (Seq = 1000, MSS = 1460, WScale = 7)" {
  style.stroke: "#2563eb"
}
Note over Server: Generates SYN Cookie / Pre-allocates TCB
Server -> Client: "2. SYN + ACK (Seq = 4000, Ack = 1001, MSS = 1460)" {
  style.stroke: "#16a34a"
}
Note over Client: Client enters ESTABLISHED
Client -> Server: "3. ACK (Seq = 1001, Ack = 4001, Window = 65535)" {
  style.stroke: "#2563eb"
}
Note over Server: Server enters ESTABLISHED\\nConnection ready for bidirectional data
""",

        # 15. TCP 4-Way Teardown
        "fig4_15_tcp_4way_teardown.svg": """
shape: sequence_diagram

Client: "Host A (Active Close)"
Server: "Host B (Passive Close)"

Client -> Server: "1. FIN (Seq = 2500, Ack = 6000)" {
  style.stroke: "#dc2626"
}
Note over Client: Enters FIN_WAIT_1
Server -> Client: "2. ACK (Ack = 2501)" {
  style.stroke: "#d97706"
}
Note over Client: Enters FIN_WAIT_2
Note over Server: Server completes pending writes (Half-Close)
Server -> Client: "3. FIN (Seq = 6000, Ack = 2501)" {
  style.stroke: "#dc2626"
}
Note over Server: Enters LAST_ACK
Client -> Server: "4. ACK (Ack = 6001)" {
  style.stroke: "#16a34a"
}
Note over Client: Enters TIME_WAIT (2 * MSL = 120s)
Note over Server: Enters CLOSED immediately
""",

        # 17. TCP Sliding Window Buffer
        "fig4_17_sliding_window_buffer.svg": """
direction: right

b1: "Bytes Sent & ACKed\\n(Flushed from Buffer)" {
  style.fill: "#f1f5f9"
}

b2: "Bytes Sent, UnACKed\\n(In-Flight on Network)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

b3: "Bytes Usable to Send\\n(Within rwnd Window Credit)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

b4: "Bytes Not Usable\\n(Outside Window Boundary)" {
  style.fill: "#fee2e2"
}

b1 -> b2 -> b3 -> b4
""",

        # 18. Silly Window Syndrome
        "fig4_18_silly_window_syndrome.svg": """
direction: right

problem: "Silly Window Syndrome (SWS)\\nWindow shrinks to tiny 1-byte increments\\nMassive 40-byte header overhead per 1-byte data" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

nagle: "Sender Mitigation: Nagle's Algorithm\\nBuffer data until full MSS or ACK received\\nAggregates small user writes" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
}

clark: "Receiver Mitigation: Clark's Solution\\nAdvertise rwnd = 0 until buffer has\\nmin(MSS, Buffer/2) free space" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

problem -> nagle
problem -> clark
""",

        # 20. Fast Recovery: Tahoe vs Reno
        "fig4_20_fast_recovery_comparison.svg": """
direction: right

tahoe: "TCP Tahoe (Aggressive Fallback)\\n• Set ssthresh = cwnd / 2\\n• Resets cwnd = 1 MSS\\n• Forces Slow Start restart\\n• Throughput penalty" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

reno: "TCP Reno (Fast Recovery)\\n• Set ssthresh = cwnd / 2\\n• Sets cwnd = ssthresh + 3 MSS\\n• Retransmits missing packet immediately\\n• Bypasses Slow Start entirely" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
  style.bold: true
}
""",

        # 21. SCTP Drivers & Architecture
        "fig4_21_sctp_drivers.svg": """
direction: right

telephony: "Carrier Signaling (SS7 / SIGTRAN)\\nDemands zero downtime and instant failover" {
  style.fill: "#fef3c7"
}

sctp_core: "SCTP Innovations (RFC 4960)\\n1. Multi-Homing: Automatic IP path failover\\n2. Multi-Streaming: Zero Head-of-Line Blocking\\n3. Message-Oriented Framing\\n4. 4-Way Cookie Handshake: Immune to SYN floods" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

telephony -> sctp_core
""",

        # 22. SCTP Multi-Homing & Multi-Streaming
        "fig4_22_sctp_multihoming.svg": """
direction: right

endpoint_a: "SCTP Endpoint A\\nIP1: 192.168.1.1 (Primary)\\nIP2: 10.0.0.1 (Backup)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

endpoint_b: "SCTP Endpoint B\\nIP1: 203.0.113.1 (Primary)\\nIP2: 198.51.100.1 (Backup)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

endpoint_a -> endpoint_b: "Primary Path (Active Data Flow)" {
  style.stroke: "#16a34a"
  style.bold: true
}

endpoint_a -> endpoint_b: "Secondary Path (Heartbeat Probes / Failover)" {
  style.stroke: "#d97706"
  style.stroke-dash: 4
}
""",

        # 23. SCTP 4-Way Handshake with State Cookie
        "fig4_23_sctp_cookie_handshake.svg": """
shape: sequence_diagram

Client: "SCTP Client"
Server: "SCTP Server"

Client -> Server: "1. INIT (Initiate Association)" {
  style.stroke: "#2563eb"
}
Note over Server: Server creates Cryptographic State Cookie;\\nALLOCATES ZERO BUFFER MEMORY! (Immune to SYN floods)
Server -> Client: "2. INIT_ACK (Contains State Cookie)" {
  style.stroke: "#d97706"
}
Client -> Server: "3. COOKIE_ECHO (Echoes State Cookie back)" {
  style.stroke: "#2563eb"
}
Note over Server: Server verifies cryptographic signature;\\nNow allocates Association TCB and buffers
Server -> Client: "4. COOKIE_ACK (Association Established)" {
  style.stroke: "#16a34a"
}
""",

        # 24. SCTP Teardown
        "fig4_24_sctp_shutdown.svg": """
shape: sequence_diagram

EndpointA: "SCTP Endpoint A"
EndpointB: "SCTP Endpoint B"

EndpointA -> EndpointB: "1. SHUTDOWN (Flushes pending outbound data)" {
  style.stroke: "#dc2626"
}
Note over EndpointB: Stops accepting new data; flushes buffered chunks
EndpointB -> EndpointA: "2. SHUTDOWN_ACK" {
  style.stroke: "#d97706"
}
EndpointA -> EndpointB: "3. SHUTDOWN_COMPLETE" {
  style.stroke: "#16a34a"
}
Note over EndpointA,EndpointB: Association cleanly terminated in both directions
""",

        # 25. TCP Services Architecture
        "fig4_25_tcp_services_taxonomy.svg": """
direction: right

tcp_services: "Ten-Pillar Architecture of TCP Services" {
  s1: "1. Process-to-Process Delivery (Sockets)"
  s2: "2. Stream Delivery (Circular Buffers)"
  s3: "3. Full-Duplex & Piggybacking"
  s4: "4. 4-Tuple Socket Demultiplexing"
  s5: "5. Connection-Oriented State (TCB)"
  s6: "6. Reliable Delivery & Error Control"
  s7: "7. Flow Control (rwnd & Persistence Timer)"
  s8: "8. Congestion Control (AIMD & Fast Recovery)"
  s9: "9. QoS & Control Flags (URG, PSH, RST)"
  s10: "10. Dynamic Timers (RTO, Keepalive, TIME_WAIT)"
}
""",

        # 26. Circular Buffer Model
        "fig4_26_circular_buffer_flow.svg": """
direction: right

app_write: "Sending Application\\nwrites continuous stream\\n(Bytes 1 ... 10000)" {
  style.fill: "#f8fafc"
}

send_ring: "Circular Send Ring Buffer\\nChunks into MSS Segments" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
}

recv_ring: "Circular Receive Ring Buffer\\nReorders out-of-order bytes" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

app_read: "Receiving Application\\nreads continuous stream" {
  style.fill: "#f8fafc"
}

app_write -> send_ring -> recv_ring -> app_read
""",

        # 27. Full Duplex & Piggybacking
        "fig4_27_full_duplex_piggybacking.svg": """
shape: sequence_diagram

HostA: "Host A"
HostB: "Host B"

HostA -> HostB: "Data Segment (Seq = 1000, Length = 500)" {
  style.stroke: "#2563eb"
}
Note over HostB: Host B has 300B data to return;\\nEmbeds ACK inside return data segment!
HostB -> HostA: "Data + ACK (Seq = 4000, Ack = 1500, Length = 300)" {
  style.stroke: "#16a34a"
}
Note over HostA: Confirms 500B delivered and receives 300B data
""",

        # 28. 4-Tuple Demultiplexing
        "fig4_28_socket_demux_4tuple.svg": """
direction: right

clients: "Concurrent Client Browsers" {
  c1: "Client 1: 10.0.0.5:51234"
  c2: "Client 2: 10.0.0.9:58432"
}

server: "Web Server (203.0.113.80)" {
  listen_sock: "Listening Socket (:80)"
  worker1: "Worker Thread 1\\n(10.0.0.5:51234, 203.0.113.80:80)" {
    style.fill: "#dcfce7"
  }
  worker2: "Worker Thread 2\\n(10.0.0.9:58432, 203.0.113.80:80)" {
    style.fill: "#dcfce7"
  }
}

clients.c1 -> server.worker1: "HTTP GET"
clients.c2 -> server.worker2: "HTTP GET"
""",

        # 29. Dynamic Timers
        "fig4_29_tcp_timers.svg": """
direction: right

rto: "1. Retransmission Timer (RTO)\\nJacobson / Karn dynamic estimation\\nRetransmits unACKed packets" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

persist: "2. Persistence Timer\\nProbes receiver during rwnd = 0\\nPrevents lost-ACK deadlocks" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

keepalive: "3. Keepalive Timer\\nVerifies client reachability (default 2h)\\nDetects crashed / disconnected peers" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

timewait: "4. TIME_WAIT Timer (2 * MSL)\\nHolds port closed (120s)\\nFlushes lingering network duplicates" {
  style.fill: "#f3e8ff"
  style.stroke: "#7e22ce"
}
"""
    }

    for filename, code in d2_diagrams.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        svg_engine.compile_d2(code, out_path, theme=1)
    print(f"  Generated {len(d2_diagrams)} D2 publication diagrams.")

generate_d2_diagrams()
print("\nUnit 4 figure generation complete!")
