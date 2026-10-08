#!/usr/bin/env python3
"""
scripts/figures/generate_unit1.py
Generates all publication-grade figures for UNIT 1 (Introduction & Physical Layer).
Produces SVGs in UNIT - 1/figures/
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_engine

OUTPUT_DIR = os.path.abspath("UNIT - 1/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating Unit 1 figures in: {OUTPUT_DIR}")

# ==============================================================================
# D2 Publication Diagrams (Long Questions: 29 Diagrams)
# ==============================================================================

def generate_long_diagrams():
    d2_long = {
        # 1. ISO Principles
        "fig1_01_iso_principles.svg": """
direction: right

p1: "1. Well-Defined Abstraction\\nLayer created where different level of abstraction is needed" { style.fill: "#dbeafe" }
p2: "2. Specific Boundary Function\\nEach layer performs a clearly defined function based on international standards" { style.fill: "#e0e7ff" }
p3: "3. Minimal Cross-Boundary Info\\nLayer interfaces minimize information flow across boundaries" { style.fill: "#dcfce7" }
p4: "4. Architectural Simplicity\\nNumber of layers kept large enough to isolate tasks, but small enough to remain simple" { style.fill: "#fef3c7" }

p1 -> p2 -> p3 -> p4
""",

        # 2. Peer-to-Peer Communication
        "fig1_02_peer_to_peer.svg": """
direction: right

host_a: "Host A (Sender)" {
  l7_a: "Application Layer" { style.fill: "#eff6ff" }
  l4_a: "Transport Layer" { style.fill: "#dbeafe" }
  l3_a: "Network Layer" { style.fill: "#dcfce7" }
  l2_a: "Data Link Layer" { style.fill: "#fef3c7" }
  l1_a: "Physical Layer" { style.fill: "#fee2e2" }
  l7_a -> l4_a -> l3_a -> l2_a -> l1_a
}

host_b: "Host B (Receiver)" {
  l7_b: "Application Layer" { style.fill: "#eff6ff" }
  l4_b: "Transport Layer" { style.fill: "#dbeafe" }
  l3_b: "Network Layer" { style.fill: "#dcfce7" }
  l2_b: "Data Link Layer" { style.fill: "#fef3c7" }
  l1_b: "Physical Layer" { style.fill: "#fee2e2" }
  l1_b -> l2_b -> l3_b -> l4_b -> l7_b
}

host_a.l7_a <-> host_b.l7_b: "Virtual Peer-to-Peer Dialogue (HTTP)" { style.stroke: "#2563eb"; style.stroke-dash: 4 }
host_a.l4_a <-> host_b.l4_b: "Virtual Peer-to-Peer Dialogue (TCP)" { style.stroke: "#1d4ed8"; style.stroke-dash: 4 }
host_a.l3_a <-> host_b.l3_b: "Virtual Peer-to-Peer Dialogue (IP)" { style.stroke: "#16a34a"; style.stroke-dash: 4 }
host_a.l1_a <-> host_b.l1_b: "Actual Physical Conduit (Bits on Wire)" { style.stroke: "#dc2626"; style.bold: true }
""",

        # 3. Encapsulation & Decapsulation
        "fig1_03_encapsulation_stack.svg": """
direction: down

app_pdu: "Application: Data Message (HTTP Body / Payload)" { style.fill: "#eff6ff" }
trans_pdu: "Transport: [TCP Header (H4) | Data Message] -> Segment" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
net_pdu: "Network: [IP Header (H3) | TCP Segment] -> Packet" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
link_pdu: "Data Link: [MAC Header (H2) | IP Packet | FCS Trailer (T2)] -> Frame" { style.fill: "#fef3c7"; style.stroke: "#d97706"; style.bold: true }
phy_pdu: "Physical Layer: 0110100101011100... (Raw Bitstream on Cable)" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }

app_pdu -> trans_pdu: "Add Port Numbers (TCP Header)"
trans_pdu -> net_pdu: "Add Logical IP Addresses (IP Header)"
net_pdu -> link_pdu: "Add Physical MAC Addresses & CRC Trailer"
link_pdu -> phy_pdu: "Encode into Physical Voltage / Light Pulses"
""",

        # 4. Complete 7-Layer OSI Architecture
        "fig1_04_osi_7layers.svg": """
direction: down

l7: "7. Application Layer: Network virtual terminal, file transfer, web, email (HTTP, DNS, SSH)" { style.fill: "#eff6ff" }
l6: "6. Presentation Layer: Syntax, semantics, translation, encryption (TLS), compression" { style.fill: "#e0e7ff" }
l5: "5. Session Layer: Dialogue control, token management, session checkpoint synchronization" { style.fill: "#ede9fe" }
l4: "4. Transport Layer: End-to-end reliability, segmenting, flow/congestion control (TCP, UDP)" { style.fill: "#dbeafe"; style.stroke: "#2563eb"; style.bold: true }
l3: "3. Network Layer: Host-to-host logical addressing, routing, forwarding, fragmentation (IPv4, IPv6)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
l2: "2. Data Link Layer: Hop-to-hop framing, 48-bit MAC addressing, error detection (Ethernet, Wi-Fi)" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
l1: "1. Physical Layer: Transmission of unstructured bit streams over physical media (Twisted Pair, Fiber)" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }

l7 -> l6 -> l5 -> l4 -> l3 -> l2 -> l1
""",

        # 5. OSI vs TCP/IP Comparison
        "fig1_05_osi_vs_tcpip.svg": """
direction: right

osi: "OSI 7-Layer Reference Model" {
  o7: "Application (Layer 7)" { style.fill: "#eff6ff" }
  o6: "Presentation (Layer 6)" { style.fill: "#eff6ff" }
  o5: "Session (Layer 5)" { style.fill: "#eff6ff" }
  o4: "Transport (Layer 4)" { style.fill: "#dbeafe" }
  o3: "Network (Layer 3)" { style.fill: "#dcfce7" }
  o2: "Data Link (Layer 2)" { style.fill: "#fef3c7" }
  o1: "Physical (Layer 1)" { style.fill: "#fee2e2" }
  o7 -> o6 -> o5 -> o4 -> o3 -> o2 -> o1
}

tcpip: "TCP/IP Protocol Suite (5 Layers)" {
  t5: "Application Layer (HTTP, FTP, DNS, SMTP)" { style.fill: "#eff6ff"; style.bold: true }
  t4: "Transport Layer (TCP, UDP, SCTP)" { style.fill: "#dbeafe"; style.bold: true }
  t3: "Network / Internet Layer (IPv4, IPv6, ICMP, ARP)" { style.fill: "#dcfce7"; style.bold: true }
  t2: "Data Link Layer (Ethernet, Wi-Fi, PPP)" { style.fill: "#fef3c7"; style.bold: true }
  t1: "Physical Layer (Cables, Fiber, Radio)" { style.fill: "#fee2e2"; style.bold: true }
  t5 -> t4 -> t3 -> t2 -> t1
}

osi.o7 -> tcpip.t5: "Consolidated"
osi.o6 -> tcpip.t5
osi.o5 -> tcpip.t5
osi.o4 -> tcpip.t4: "1:1 Match"
osi.o3 -> tcpip.t3: "1:1 Match"
osi.o2 -> tcpip.t2: "1:1 Match"
osi.o1 -> tcpip.t1: "1:1 Match"
""",

        # 6. Host Socket Demux
        "fig1_06_socket_demux.svg": """
direction: down

trans: "Transport Layer Sockets" {
  s_web: "Port 80 (Web Server)" { style.fill: "#dcfce7" }
  s_ssh: "Port 22 (SSH Server)" { style.fill: "#dbeafe" }
  s_dns: "Port 53 (DNS Server)" { style.fill: "#fef3c7" }
}

net: "Network Layer (IP Protocol Field)\\nProtocol 6 = TCP -> Demux to TCP\\nProtocol 17 = UDP -> Demux to UDP" {
  style.fill: "#f8fafc"
}

net -> trans.s_web
net -> trans.s_ssh
net -> trans.s_dns
""",

        # 7. TCP Connection Lifecycle
        "fig1_07_tcp_lifecycle.svg": """
shape: sequence_diagram

Client: "Host A (Client)"
Server: "Host B (Server)"

Note over Client,Server: Phase 1: Connection Establishment (3-Way Handshake)
Client -> Server: "SYN (Seq=1000)" { style.stroke: "#2563eb" }
Server -> Client: "SYN + ACK (Seq=5000, Ack=1001)" { style.stroke: "#16a34a" }
Client -> Server: "ACK (Seq=1001, Ack=5001)" { style.stroke: "#2563eb" }

Note over Client,Server: Phase 2: Bi-Directional Full-Duplex Data Transfer
Client -> Server: "Data PDU 1 (Seq=1001, 1000 Bytes)"
Server -> Client: "Data PDU 2 + ACK 2001 (Piggybacked)" { style.stroke: "#16a34a" }

Note over Client,Server: Phase 3: Graceful Teardown (4-Way Handshake)
Client -> Server: "FIN (Seq=2001)" { style.stroke: "#dc2626" }
Server -> Client: "ACK (Ack=2002)"
Server -> Client: "FIN (Seq=6001)" { style.stroke: "#dc2626" }
Client -> Server: "ACK (Ack=6002)"
Note over Client: Enters TIME_WAIT (2 * MSL)
""",

        # 8. Sliding Window Buffer Management
        "fig1_08_sliding_window_buffer.svg": """
direction: right

acked: "Bytes Sent & Acknowledged\\n(Can be deleted from sender memory)" { style.fill: "#f1f5f9" }
inflight: "Bytes Sent, Unacknowledged\\n(In transit / buffer held for retransmission)" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
usable: "Bytes Eligible to Send\\n(Within receiver advertised window credit rwnd)" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
unusable: "Bytes Outside Window\\n(Cannot transmit until window advances)" { style.fill: "#fee2e2" }

acked -> inflight -> usable -> unusable
""",

        # 9. TCP Congestion Control State Machine
        "fig1_09_congestion_control_fsm.svg": """
direction: down

ss: "Slow Start Phase\\ncwnd doubles every RTT: cwnd = cwnd * 2\\nProbes available link bandwidth rapidly" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
ca: "Congestion Avoidance Phase\\ncwnd grows linearly: cwnd = cwnd + 1 MSS/RTT\\nCautious additive increase (AI)" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
fr: "Fast Retransmit & Recovery (Reno)\\nUpon 3 Duplicate ACKs:\\nssthresh = cwnd / 2, cwnd = ssthresh + 3 MSS" { style.fill: "#fef3c7"; style.stroke: "#d97706"; style.bold: true }
timeout: "RTO Timeout (Severe Loss)\\nssthresh = cwnd / 2\\nReset cwnd = 1 MSS (Fall back to Slow Start)" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }

ss -> ca: "cwnd >= ssthresh"
ca -> fr: "3 Duplicate ACKs"
fr -> ca: "New ACK Arrives"
ca -> timeout: "Retransmission Timeout"
ss -> timeout: "Retransmission Timeout"
timeout -> ss: "Restart at 1 MSS"
""",

        # 10. Protocol Selection Decision Tree
        "fig1_10_protocol_selection_tree.svg": """
direction: down

req: "Application Requirements" { style.fill: "#f8fafc" }
q1: "Can the application tolerate packet loss?" { style.fill: "#fef3c7" }
tcp_choice: "Choose TCP\\n• 100% Reliability & In-Order Delivery\\n• Web (HTTP), File (FTP), Shell (SSH), Mail (SMTP)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
udp_choice: "Choose UDP\\n• Low latency, 0-RTT, Real-Time Streaming\\n• VoIP, Video Streaming, Gaming, DNS, DHCP" { style.fill: "#dbeafe"; style.stroke: "#2563eb"; style.bold: true }

req -> q1
q1 -> tcp_choice: "NO (Must be reliable)"
q1 -> udp_choice: "YES (Latency critical)"
""",

        # 11. Switching Methodologies Taxonomy
        "fig1_11_switching_taxonomy.svg": """
direction: right

circuit: "1. Circuit Switching\\n• Dedicated physical path\\n• Pre-allocated bandwidth\\n• No queueing delay\\n• Inefficient for bursty data (PSTN)" { style.fill: "#fee2e2"; style.stroke: "#dc2626" }
message: "2. Message Switching\\n• Entire message stored and forwarded\\n• Requires massive intermediate disk storage\\n• High store-and-forward latency" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
packet: "3. Packet Switching\\n• Packets chunked into MTU fragments\\n• Statistical multiplexing\\n• Datagram (Connectionless) vs Virtual Circuit" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

circuit -> message -> packet
""",

        # 12. Circuit Switching 3-Phase Lifecycle
        "fig1_12_circuit_switching_phases.svg": """
shape: sequence_diagram

HostA: "Calling Host A"
Switch1: "Switch 1"
Switch2: "Switch 2"
HostB: "Called Host B"

Note over HostA,HostB: Phase 1: Circuit Establishment (Setup Delay)
HostA -> Switch1: "Connection Request"
Switch1 -> Switch2: "Reserve Physical Time Slot / Frequency"
Switch2 -> HostB: "Connection Request"
HostB -> Switch2: "Connection Accepted (Circuit Locked)"
Switch2 -> Switch1: "Acknowledge"
Switch1 -> HostA: "Circuit Ready"

Note over HostA,HostB: Phase 2: Dedicated Data Transfer (Propagation Delay Only)
HostA -> HostB: "Continuous Real-Time Data Stream (Zero Queueing!)" { style.stroke: "#16a34a" }

Note over HostA,HostB: Phase 3: Circuit Teardown
HostA -> Switch1: "Teardown Request"
Switch1 -> Switch2: "Release Resources"
Switch2 -> HostB: "Circuit Terminated"
""",

        # 13. Message Switching Store and Forward
        "fig1_13_message_switching.svg": """
direction: right

host_a: "Host A\\n(Sends 10MB Message)" { style.fill: "#eff6ff" }
sw1: "Switch 1\\nBuffers ENTIRE 10MB\\nbefore transmitting" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
sw2: "Switch 2\\nBuffers ENTIRE 10MB\\nbefore transmitting" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
host_b: "Host B" { style.fill: "#ecfdf5" }

host_a -> sw1: "Entire Message Transit"
sw1 -> sw2: "Forward after 100% received"
sw2 -> host_b: "Delivery"
""",

        # 14. Datagram Packet Switching
        "fig1_14_datagram_packet_switching.svg": """
direction: right

src: "Source Host\\nChunks message into\\nPackets P1, P2, P3" { style.fill: "#dbeafe" }

r1: "Router R1" { style.fill: "#f8fafc" }
r2: "Router R2" { style.fill: "#f8fafc" }
r3: "Router R3" { style.fill: "#f8fafc" }

dst: "Destination Host\\nReassembles packets" { style.fill: "#dcfce7" }

src -> r1: "P1 (Path via R1)"
src -> r2: "P2 (Path via R2)"
src -> r3: "P3 (Path via R3)"
r1 -> dst: "P1 delivered"
r2 -> dst: "P2 delivered"
r3 -> dst: "P3 delivered"
""",

        # 15. Virtual Circuit Packet Switching
        "fig1_15_virtual_circuit_switching.svg": """
direction: right

src: "Source Host" { style.fill: "#dbeafe" }
sw1: "VC Switch 1\\n[VCI Table]" { style.fill: "#fef3c7" }
sw2: "VC Switch 2\\n[VCI Table]" { style.fill: "#fef3c7" }
dst: "Destination Host" { style.fill: "#dcfce7" }

src -> sw1: "Setup -> Fixed Path (VCI: 14)" { style.stroke: "#16a34a"; style.bold: true }
sw1 -> sw2: "Translates VCI: 14 -> 27" { style.stroke: "#16a34a"; style.bold: true }
sw2 -> dst: "Translates VCI: 27 -> 08" { style.stroke: "#16a34a"; style.bold: true }
""",

        # 16. Switching Delay Pipeline Comparison
        "fig1_16_switching_delay_pipeline.svg": """
direction: right

msg_sw: "1. Message Switching Timeline\\n|--- Tx Msg 1 ---||--- Tx Msg 2 ---||--- Tx Msg 3 ---|\\n(High total delay: Sequential full-store stages)" {
  style.fill: "#fee2e2"
}

pkt_sw: "2. Packet Switching Pipelined Timeline\\n|P1||P2||P3| (Link 1)\\n   |P1||P2||P3| (Link 2)\\n      |P1||P2||P3| (Link 3)\\n(Massive latency savings via simultaneous link pipelining!)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

msg_sw -> pkt_sw: "Pipelining Optimization"
""",

        # 17. Network Topology Classification
        "fig1_17_topology_classification.svg": """
direction: right

mesh: "Mesh: Full interconnectivity\\nLinks = N(N-1)/2\\nHigh fault tolerance, high cost" { style.fill: "#dbeafe" }
star: "Star: Central hub / switch\\nLinks = N\\nEasy install, central point of failure" { style.fill: "#dcfce7" }
bus: "Bus: Shared coaxial backbone\\nLow cost, CSMA/CD collisions" { style.fill: "#fef3c7" }
ring: "Ring: Unidirectional token ring\\nPredictable delay, break halts ring" { style.fill: "#fee2e2" }
tree: "Tree: Hierarchical star of stars\\nCisco Core/Dist/Access hierarchy" { style.fill: "#e0e7ff" }

mesh -> star -> bus -> ring -> tree
""",

        # 18. Mesh Topology Architecture
        "fig1_18_mesh_topology.svg": """
direction: right

n1: "Node 1" { style.fill: "#dbeafe" }
n2: "Node 2" { style.fill: "#dbeafe" }
n3: "Node 3" { style.fill: "#dbeafe" }
n4: "Node 4" { style.fill: "#dbeafe" }
n5: "Node 5" { style.fill: "#dbeafe" }

n1 <-> n2
n1 <-> n3
n1 <-> n4
n1 <-> n5
n2 <-> n3
n2 <-> n4
n2 <-> n5
n3 <-> n4
n3 <-> n5
n4 <-> n5
""",

        # 19. Star Topology Architecture
        "fig1_19_star_topology.svg": """
direction: right

hub: "Central Switch / Hub\\n(Central Arbiter)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

pc1: "Workstation 1" { style.fill: "#dbeafe" }
pc2: "Workstation 2" { style.fill: "#dbeafe" }
pc3: "Workstation 3" { style.fill: "#dbeafe" }
srv: "Server" { style.fill: "#fef3c7" }

pc1 <-> hub
pc2 <-> hub
pc3 <-> hub
srv <-> hub
""",

        # 20. Bus Topology Architecture
        "fig1_20_bus_topology.svg": """
direction: right

backbone: "Shared Coaxial Backbone Cable (Terminators 50 Ohm at ends)" {
  style.fill: "#f1f5f9"
  style.stroke: "#0f172a"
  style.bold: true
}

sta1: "Station 1" { style.fill: "#dbeafe" }
sta2: "Station 2" { style.fill: "#dbeafe" }
sta3: "Station 3" { style.fill: "#dbeafe" }

sta1 -> backbone: "Tap / Drop Cable"
sta2 -> backbone: "Tap / Drop Cable"
sta3 -> backbone: "Tap / Drop Cable"
""",

        # 21. Token Ring Topology
        "fig1_21_ring_topology.svg": """
direction: right

sta1: "Station A" { style.fill: "#dcfce7" }
sta2: "Station B" { style.fill: "#f8fafc" }
sta3: "Station C" { style.fill: "#f8fafc" }
sta4: "Station D" { style.fill: "#f8fafc" }

sta1 -> sta2: "Token Frame / Data"
sta2 -> sta3
sta3 -> sta4
sta4 -> sta1: "Unidirectional Ring Transit"
""",

        # 22. Self-Healing Dual-Ring
        "fig1_22_dual_ring_fddi.svg": """
direction: right

Normal: "1. Normal Operation" {
  R1_norm: "Primary Ring: Clockwise Data Flow" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
  R2_norm: "Secondary Ring: Counter-Clockwise Idle Backup" { style.fill: "#f1f5f9" }
}

Wrap: "2. Link Failure & Cable Wrap" {
  WrapNode: "Adjacent nodes wrap Primary into Secondary\\nRestores complete closed loop ring automatically!" {
    style.fill: "#fee2e2"
    style.stroke: "#dc2626"
    style.bold: true
  }
}
""",

        # 23. Cisco 3-Layer Hierarchical Tree
        "fig1_23_hierarchical_tree.svg": """
direction: down

core: "1. Core Layer (High-Speed Backbone)\\nNon-blocking high-speed switching fabric" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
  style.bold: true
}

dist: "2. Distribution Layer (Policy & Routing)\\nRouting between VLANs, Access Control Lists (ACL), packet filtering" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

access: "3. Access Layer (Workgroup Edge)\\nPort security, VLAN tagging, end-user PC connectivity" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

core -> dist -> access
""",

        # 24. Transmission Media Classification
        "fig1_24_transmission_media_tree.svg": """
direction: right

guided: "Guided (Wired / Bounded)\\n• Twisted Pair (Cat3 to Cat8)\\n• Coaxial Cable (Thinnet/Thicknet)\\n• Fiber Optic (SMF & MMF)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
  style.bold: true
}

unguided: "Unguided (Wireless / Unbounded)\\n• Radio Waves (Omnidirectional, 3kHz-1GHz)\\n• Microwaves (Unidirectional LOS, 1-300GHz)\\n• Infrared (Line of sight, cannot penetrate walls)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

guided -> unguided: "Physical Media Spectrum"
""",

        # 25. Twisted Pair Physics
        "fig1_25_twisted_pair_physics.svg": """
direction: right

diff: "Differential Signaling: Wire 1 (+V), Wire 2 (-V)\\nReceiver measures difference: (+V) - (-V) = 2V" { style.fill: "#dbeafe" }
twisting: "Regular Helical Twisting\\nExternal noise induces EQUAL voltage on both wires\\n(+V + noise) - (-V + noise) = 2V\\nNoise completely cancels out!" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

diff -> twisting
""",

        # 26. Fiber Optic TIR
        "fig1_26_fiber_optics_tir.svg": """
direction: right

core: "Fiber Core (High Refractive Index n1)" { style.fill: "#dbeafe" }
cladding: "Cladding (Lower Refractive Index n2 < n1)" { style.fill: "#f1f5f9" }

tir: "Total Internal Reflection (TIR):\\nAngle of incidence > Critical angle theta_c\\nLight wave trapped 100% inside core with minimal attenuation!" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

core -> cladding -> tir
""",

        # 27. SMF vs MMF
        "fig1_27_smf_vs_mmf.svg": """
direction: right

smf: "Single-Mode Fiber (SMF)\\n• Tiny core (8 – 10 micrometers)\\n• Single straight light mode\\n• Zero modal dispersion\\n• Long-haul backbones (up to 100 km)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
  style.bold: true
}

mmf: "Multi-Mode Fiber (MMF)\\n• Thick core (50 – 62.5 micrometers)\\n• Multiple light rays reflect at different angles\\n• High modal dispersion\\n• Short distance LANs / Data Centers (< 550 m)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

smf -> mmf
""",

        # 28. Wireless Propagation Mechanisms
        "fig1_28_wireless_propagation.svg": """
direction: right

gw: "1. Ground Wave (< 2 MHz)\\nFollows curvature of Earth (AM Radio)" { style.fill: "#dbeafe" }
sw: "2. Sky Wave (2 – 30 MHz)\\nReflects off Ionosphere layer (Shortwave Radio)" { style.fill: "#fef3c7" }
los: "3. Line-of-Sight (> 30 MHz)\\nDirect antenna-to-antenna beam (Satellite, Cellular, Wi-Fi)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

gw -> sw -> los
""",

        # 29. Unguided Electromagnetic Spectrum
        "fig1_29_em_spectrum.svg": """
direction: right

radio: "Radio Waves (3 kHz – 1 GHz)\\nOmnidirectional, penetrates walls\\nAM/FM, TV, Paging" { style.fill: "#dbeafe" }
micro: "Microwaves (1 GHz – 300 GHz)\\nUnidirectional, Line-of-Sight dish antennas\\nCellular 4G/5G, Wi-Fi, Satellite" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
ir: "Infrared (300 GHz – 400 THz)\\nShort-range, cannot penetrate walls\\nTV remote controls, IrDA" { style.fill: "#fee2e2" }

radio -> micro -> ir
"""
    }

    for filename, code in d2_long.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        svg_engine.compile_d2(code, out_path, theme=1)
    print(f"  Generated {len(d2_long)} D2 long-question diagrams.")

# ==============================================================================
# D2 Publication Diagrams (Short Questions: 11 Diagrams)
# ==============================================================================

def generate_short_diagrams():
    d2_short = {
        # S1. Network Environment
        "fig1_s01_network_definition.svg": """
direction: right

nodes: "Interconnected Autonomous Devices\\n(PCs, Servers, Smart Devices, Routers)" { style.fill: "#dbeafe" }
links: "Communication Links\\n(Ethernet, Fiber Optics, Wireless 802.11)" { style.fill: "#fef3c7" }
protocols: "Common Protocols\\n(TCP/IP, Rules governing syntax & timing)" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

nodes <-> links <-> protocols
""",

        # S2. Network Types by Scale
        "fig1_s02_network_types_scale.svg": """
direction: right

pan: "PAN (Personal Area Network)\\nCoverage: ~1 - 10 meters\\nBluetooth, Zigbee, Wearables" { style.fill: "#eff6ff" }
lan: "LAN (Local Area Network)\\nCoverage: Room, Office, Campus\\nEthernet, Wi-Fi (100m - 1km)" { style.fill: "#dbeafe" }
man: "MAN (Metropolitan Area Network)\\nCoverage: City-wide\\nCable TV network, Metro Ethernet" { style.fill: "#fef3c7" }
wan: "WAN (Wide Area Network)\\nCoverage: Country, Continent, Global\\nThe Global Internet, Submarine Cables" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

pan -> lan -> man -> wan
""",

        # S3. Layer Mapping
        "fig1_s03_osi_tcpip_layers.svg": """
direction: right

osi: "OSI 7 Layers\\n7. Application\\n6. Presentation\\n5. Session\\n4. Transport\\n3. Network\\n2. Data Link\\n1. Physical" { style.fill: "#dbeafe" }
tcpip: "TCP/IP 5 Layers\\n5. Application\\n4. Transport\\n3. Network\\n2. Data Link\\n1. Physical" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

osi -> tcpip: "Pragmatic Consolidation"
""",

        # S4. Transmission Media Summary
        "fig1_s04_transmission_media_summary.svg": """
direction: right

guided: "Guided (Wired): Twisted Pair (Cat3-8), Coaxial, Fiber Optics (SMF/MMF)" { style.fill: "#dbeafe" }
unguided: "Unguided (Wireless): Radio Waves, Microwaves, Infrared" { style.fill: "#dcfce7" }

guided <-> unguided
""",

        # S5. Throughput vs Bandwidth
        "fig1_s05_throughput_vs_bandwidth.svg": """
direction: right

bw: "Bandwidth (Physical Capacity)\\nTheoretical max bit rate (e.g. 1 Gbps link)" { style.fill: "#dbeafe" }
tp: "Throughput (Actual Delivery Rate)\\nActual data delivered successfully (e.g. 650 Mbps)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
jitter: "Jitter (Delay Variation)\\nFluctuation in end-to-end packet arrival times (ms)" { style.fill: "#fee2e2" }

bw -> tp -> jitter
""",

        # S6. TCP vs UDP Dialogue
        "fig1_s06_tcp_vs_udp_dialogue.svg": """
direction: right

tcp: "TCP (Connection-Oriented)\\n• Handshake establishment\\n• Cumulative ACKs\\n• Retransmissions upon loss\\n• Flow & Congestion Control" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
udp: "UDP (Connectionless)\\n• Fire-and-forget\\n• Zero handshake latency\\n• No retransmissions\\n• Lightweight (8B header)" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }

tcp <-> udp
""",

        # S7. Circuit vs Packet Switching
        "fig1_s07_circuit_vs_packet_switching.svg": """
direction: right

circuit: "Circuit Switching\\n• Dedicated physical line\\n• Constant transmission delay\\n• Idle capacity wasted\\n• Classic Telephone (PSTN)" { style.fill: "#fee2e2" }
packet: "Packet Switching\\n• Discrete packet chunks\\n• Statistical multiplexing\\n• Dynamic route adaptation\\n• The Modern Internet" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

circuit <-> packet
""",

        # S8. Switch vs Router
        "fig1_s08_switch_vs_router.svg": """
direction: right

switch: "Layer 2 Switch\\n• Forwards using 48-bit MAC addresses\\n• Operates within single broadcast domain\\n• Microsegmentation & port forwarding" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
router: "Layer 3 Router\\n• Forwards using 32-bit / 128-bit IP addresses\\n• Interconnects distinct network subnets\\n• Separates broadcast domains" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

switch <-> router
""",

        # S9. Network Topologies Overview
        "fig1_s09_topologies_overview.svg": """
direction: right

topologies: "Major Network Topologies" {
  m: "Mesh: All-to-all dedicated links" { style.fill: "#dbeafe" }
  s: "Star: Central switch hub" { style.fill: "#dcfce7" }
  b: "Bus: Single shared backbone" { style.fill: "#fef3c7" }
  r: "Ring: Closed circular token loop" { style.fill: "#fee2e2" }
  t: "Tree: Hierarchical branches" { style.fill: "#e0e7ff" }
}
""",

        # S10. Five Components of Data Communication
        "fig1_s10_five_components_communication.svg": """
direction: right

msg: "1. Message (Data to be communicated)" { style.fill: "#eff6ff" }
sender: "2. Sender (Device originating data)" { style.fill: "#dbeafe" }
medium: "3. Medium (Physical transmission channel)" { style.fill: "#fef3c7" }
receiver: "4. Receiver (Destination device)" { style.fill: "#dcfce7" }
protocol: "5. Protocol (Governing rules & syntax)" { style.fill: "#fee2e2"; style.stroke: "#dc2626"; style.bold: true }

sender -> msg -> medium -> receiver
protocol -> sender
protocol -> receiver
""",

        # S11. Line Configuration
        "fig1_s11_line_configuration.svg": """
direction: right

p2p: "Point-to-Point (Dedicated Link)\\nDedicated channel between exactly 2 devices\\n(e.g., Leased line, Microwave link)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
multipoint: "Multipoint (Shared / Multidrop Link)\\nMultiple devices share capacity of single link\\n(e.g., Bus coaxial LAN, Shared Wi-Fi)" { style.fill: "#fef3c7"; style.stroke: "#d97706" }

p2p <-> multipoint
"""
    }

    for filename, code in d2_short.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        svg_engine.compile_d2(code, out_path, theme=1)
    print(f"  Generated {len(d2_short)} D2 short-question diagrams.")

generate_long_diagrams()
generate_short_diagrams()
print("\nUnit 1 figure generation complete!")
