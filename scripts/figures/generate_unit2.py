#!/usr/bin/env python3
"""
scripts/figures/generate_unit2.py
Generates all publication-grade figures for UNIT 2 (Data Link Layer).
Produces SVGs in UNIT - 2/figures/
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_engine

OUTPUT_DIR = os.path.abspath("UNIT - 2/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating Unit 2 figures in: {OUTPUT_DIR}")

# ==============================================================================
# 1. Frame & Packet Headers (Python Vector SVG Engine)
# ==============================================================================

def generate_headers():
    # 1. IEEE 802.3 Ethernet Frame Layout
    eth_rows = [
        [("Preamble (7 Octets)", 7, "meta", "7 Bytes (10101010...)"),
         ("SFD", 1, "flag", "1B (10101011)"),
         ("Destination MAC Address", 6, "address", "6 Bytes (48 Bits)"),
         ("Source MAC Address", 6, "address", "6 Bytes (48 Bits)"),
         ("EtherType / Length", 2, "type", "2 Bytes (e.g. 0x0800 IPv4)"),
         ("Payload (46 to 1500 Octets)", 8, "seq", "MTU Data (Pad to 46B)"),
         ("FCS / CRC-32", 4, "checksum", "4 Bytes (CRC Polynomial)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "IEEE 802.3 Ethernet Frame Format",
        eth_rows,
        os.path.join(OUTPUT_DIR, "fig2_hdr_ethernet.svg"),
        total_bits=34,
        bit_ruler=False
    )

    # 2. RFC 826 ARP Packet Format (28 bytes = 7 rows of 32 bits)
    arp_rows = [
        [("Hardware Type (htype = 1 for Ethernet)", 16, "meta", "16 Bits (0x0001)"),
         ("Protocol Type (ptype = 0x0800 for IPv4)", 16, "type", "16 Bits (0x0800)")],
        [("Hardware Addr Len (hlen = 6)", 8, "length", "8 Bits (6 Octets)"),
         ("Protocol Addr Len (plen = 4)", 8, "length", "8 Bits (4 Octets)"),
         ("Operation (op: 1=Req, 2=Reply)", 16, "control", "16 Bits")],
        [("Sender Hardware Address (SHA: MAC) — Upper 32 Bits", 32, "address", "Upper 4 Octets of Sender MAC")],
        [("Sender MAC — Lower 16 Bits", 16, "address", "Lower 2 Octets"),
         ("Sender IP Address (SPA) — Upper 16 Bits", 16, "address", "Upper 2 Octets of Sender IP")],
        [("Sender IP Address (SPA) — Lower 16 Bits", 16, "address", "Lower 2 Octets"),
         ("Target Hardware Address (THA) — Upper 16 Bits", 16, "address", "Upper 2 Octets (0 in Request)")],
        [("Target Hardware Address (THA) — Lower 32 Bits", 32, "address", "Lower 4 Octets of Target MAC")],
        [("Target Protocol Address (TPA: IP)", 32, "address", "32 Bits (IP being queried)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 826: Address Resolution Protocol (ARP) 28-Byte Packet Format",
        arp_rows,
        os.path.join(OUTPUT_DIR, "fig2_hdr_arp.svg")
    )

generate_headers()
print("  Generated Ethernet and ARP frame/packet headers.")

# ==============================================================================
# 2. D2 Publication Diagrams (Architectures, Flows & Sequences)
# ==============================================================================

def generate_d2_diagrams():
    d2_diagrams = {
        # 1. Delivery Scopes Comparison
        "fig2_01_layer_responsibilities.svg": """
direction: down

l3: "Network Layer (Host-to-Host)\\nGlobal IP Addressing\\nRoutes across multiple intermediate routers" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

l2: "Data Link Layer (Hop-to-Hop)\\nPhysical MAC Addressing & Framing\\nTransfers frames directly across single link" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

l1: "Physical Layer (Bit Transmission)\\nConverts bits into electrical, optical, or radio signals" {
  style.fill: "#f8fafc"
  style.stroke: "#64748b"
}

l3 -> l2 -> l1
""",

        # 2. Hop-by-Hop Link Framing
        "fig2_02_hop_by_hop_framing.svg": """
direction: right

host_a: "Host A\\nMAC_A" { style.fill: "#eff6ff" }
sw1: "Switch 1\\n(Layer 2)" { style.fill: "#f8fafc" }
r1: "Router R1\\nMAC_R1" { style.fill: "#fef3c7" }
sw2: "Switch 2\\n(Layer 2)" { style.fill: "#f8fafc" }
host_b: "Host B\\nMAC_B" { style.fill: "#ecfdf5" }

host_a -> sw1: "Hop 1: [Src: MAC_A, Dst: MAC_R1 | IP Packet]"
sw1 -> r1: "L2 Forwarding"
r1 -> sw2: "Hop 2: [Src: MAC_R1_out, Dst: MAC_B | IP Packet]" {
  style.stroke: "#16a34a"
  style.bold: true
}
sw2 -> host_b: "L2 Forwarding"
""",

        # 3. LLC vs MAC Sublayers
        "fig2_03_llc_mac_sublayers.svg": """
direction: down

net: "Network Layer (IP, ARP, RARP)" { style.fill: "#f8fafc" }

llc: "LLC Sublayer (IEEE 802.2)\\n• Independent of physical media\\n• Flow control & error handling\\n• Multiplexes network protocols via SAP" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
  style.bold: true
}

mac: "MAC Sublayer (IEEE 802.3 Ethernet / 802.11 Wi-Fi)\\n• Media arbitration (CSMA/CD, CSMA/CA)\\n• Physical 48-bit MAC addressing\\n• Framing, preamble, and CRC-32 FCS" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

phy: "Physical Layer (Cables, Radios, Transceivers)" { style.fill: "#f8fafc" }

net -> llc -> mac -> phy
""",

        # 4. Framing Techniques
        "fig2_04_framing_techniques.svg": """
direction: right

f1: "1. Byte-Oriented (Byte Stuffing)\\nFlag: 0x7E (FLAG), Escape: 0x7D (ESC)\\nInserts ESC before embedded FLAG/ESC octets" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

f2: "2. Bit-Oriented (Bit Stuffing)\\nFlag Delimiter: 01111110 (6 contiguous 1s)\\nTransmitter inserts '0' after five consecutive '1's" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

f3: "3. Character / Byte Count\\nHeader contains length field in octets\\nHigh vulnerability to count corruption" {
  style.fill: "#fee2e2"
}

f1 -> f2 -> f3
""",

        # 5. Bit Stuffing Walkthrough
        "fig2_05_bit_stuffing_walkthrough.svg": """
direction: down

raw: "Original Payload Bitstream:\\n0 1 1 1 1 1 1 0 0 1 (Contains Flag Pattern 01111110!)" {
  style.fill: "#f8fafc"
}

stuffed: "Transmitter Stuffs '0' after five 1s:\\n0 1 1 1 1 1 [0] 1 0 0 1" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
  style.bold: true
}

frame: "Transmitted Frame with Delimiters:\\n[01111110] 0 1 1 1 1 1 0 1 0 0 1 [01111110]" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

destuff: "Receiver De-stuffs (Removes '0' following five 1s):\\n0 1 1 1 1 1 1 0 0 1 (Original payload restored perfectly!)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

raw -> stuffed -> frame -> destuff
""",

        # 6. MAC Arbitration Taxonomy
        "fig2_06_mac_protocols_taxonomy.svg": """
direction: right

random: "1. Random Access Protocols\\n• ALOHA / Slotted ALOHA\\n• CSMA (1-persistent, non-persistent)\\n• CSMA/CD (Ethernet collisions)\\n• CSMA/CA (Wi-Fi avoidance)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

controlled: "2. Controlled Access\\n• Reservation\\n• Polling (Primary/Secondary)\\n• Token Passing (Token Ring / FDDI)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

channel: "3. Channelization\\n• FDMA (Frequency Division)\\n• TDMA (Time Division)\\n• CDMA (Code Division)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

random -> controlled -> channel
""",

        # 7. Network Dissemination Paradigms
        "fig2_07_dissemination_paradigms.svg": """
direction: right

p_uni: "Unicast (One-to-One)\\nSingle sender to single destination" { style.fill: "#dbeafe" }
p_bcast: "Broadcast (One-to-All)\\nSingle sender to all hosts on link" { style.fill: "#fee2e2" }
p_mcast: "Multicast (One-to-Many)\\nSingle sender to subscribed group" { style.fill: "#dcfce7" }
p_any: "Anycast (One-to-Nearest)\\nSingle sender to nearest topologically" { style.fill: "#fef3c7" }

p_uni -> p_bcast -> p_mcast -> p_any
""",

        # 8. Unicast Transmission
        "fig2_08_unicast_flow.svg": """
direction: right

src: "Source Host A\\n192.168.1.10\\nMAC: AA:AA:AA:AA:AA:AA" { style.fill: "#dbeafe" }
sw: "Layer 2 Switch\\nForwards only to port 3" { style.fill: "#f8fafc" }
dst: "Target Host B\\n192.168.1.20\\nMAC: BB:BB:BB:BB:BB:BB" { style.fill: "#dcfce7" }
other: "Other Hosts (Ignored / No Copy)" { style.fill: "#f1f5f9" }

src -> sw: "Dedicated Frame: Dst MAC_B"
sw -> dst: "Direct Port Forwarding" { style.stroke: "#16a34a"; style.bold: true }
""",

        # 9. Broadcast Transmission
        "fig2_09_broadcast_flow.svg": """
direction: right

src: "Transmitting Host\\nSends to FF:FF:FF:FF:FF:FF" { style.fill: "#fee2e2" }
sw: "Layer 2 Switch\\nFloods to ALL active ports" { style.fill: "#fef3c7"; style.stroke: "#d97706" }
h1: "Host 1 (Processes Frame)" { style.fill: "#fee2e2" }
h2: "Host 2 (Processes Frame)" { style.fill: "#fee2e2" }
h3: "Host 3 (Processes Frame)" { style.fill: "#fee2e2" }

src -> sw: "Broadcast Frame"
sw -> h1
sw -> h2
sw -> h3
""",

        # 10. Multicast Transmission
        "fig2_10_multicast_flow.svg": """
direction: right

srv: "Video Streaming Server\\nStream to 224.1.2.3" { style.fill: "#dcfce7" }
sw: "IGMP Snooping Switch\\nForwards ONLY to joined group ports" { style.fill: "#dbeafe"; style.stroke: "#2563eb"; style.bold: true }
sub1: "Subscriber 1 (Joined)" { style.fill: "#dcfce7" }
sub2: "Subscriber 2 (Joined)" { style.fill: "#dcfce7" }
nonsub: "Non-Subscriber (No traffic delivered)" { style.fill: "#f1f5f9" }

srv -> sw: "Multicast Stream"
sw -> sub1
sw -> sub2
""",

        # 11. 32:1 Multicast Mapping Ambiguity
        "fig2_11_multicast_mac_ambiguity.svg": """
direction: down

class_d: "Class D Multicast IP: 1110 [5 Unmapped Bits] [23 Mapped Bits]\\nTotal 28-bit multicast group address" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

mac_prefix: "Ethernet MAC Multicast Prefix: 01:00:5E (Fixed 24 Bits)\\n+ 1 Bit set to 0 (25th bit)\\n+ 23 Lower Bits copied directly from IP" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

ambiguity: "The 32:1 Ambiguity:\\nBecause 5 IP bits (2^5 = 32) are discarded,\\n32 distinct IP multicast addresses map to the EXACT SAME Ethernet MAC!\\nNetwork interface card (NIC) accepts frame; host IP stack filters non-targets." {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
  style.bold: true
}

class_d -> mac_prefix -> ambiguity
""",

        # 12. Anycast Routing
        "fig2_12_anycast_routing.svg": """
direction: right

user: "User Client\\nQueries 8.8.8.8" { style.fill: "#dbeafe" }

r_isp: "ISP Core Router\\nBGP Shortest Path" { style.fill: "#f8fafc" }

dns_ny: "DNS Node (New York)\\nBGP Cost = 40ms" { style.fill: "#f1f5f9" }
dns_lon: "DNS Node (London)\\nBGP Cost = 12ms (Shortest Path)" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

user -> r_isp
r_isp -> dns_lon: "Auto-routed to topologically nearest node!"
""",

        # 13. Logical IP vs Physical MAC Duality
        "fig2_13_ip_vs_mac_addressing.svg": """
direction: right

ip_space: "Logical Addressing (Network Layer)\\n• 32-Bit IPv4 / 128-Bit IPv6\\n• Hierarchical: Identifies network location\\n• Changes when device moves subnets" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

mac_space: "Physical Addressing (Data Link Layer)\\n• 48-Bit IEEE MAC Address\\n• Flat: Globally unique hardware identity (OUI + NIC)\\n• Burned into ROM; permanent" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

arp_bridge: "ARP Protocol (RFC 826)\\nBridges the gap: Dynamically resolves IP -> MAC" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
  style.bold: true
}

ip_space <-> arp_bridge
arp_bridge <-> mac_space
""",

        # 14. ARP Resolution Cycle
        "fig2_14_arp_resolution_cycle.svg": """
shape: sequence_diagram

HostA: "Host A (192.168.1.10)"
Broadcast: "All Hosts (LAN)"
HostB: "Host B (192.168.1.20)"

HostA -> Broadcast: "1. ARP Request (Broadcast: FF:FF:FF:FF:FF:FF)\\n'Who has 192.168.1.20? Tell 192.168.1.10 (MAC_A)'" { style.stroke: "#2563eb" }
Note over Broadcast: Every station receives frame; non-target hosts drop silently
Note over HostB: Host B updates its ARP cache with MAC_A!
HostB -> HostA: "2. ARP Reply (Unicast to MAC_A)\\n'192.168.1.20 is at MAC_B'" { style.stroke: "#16a34a"; style.bold: true }
Note over HostA: Host A caches MAC_B; transmits queued IP packet immediately!
""",

        # 15. Complete ARP Protocol Flowchart
        "fig2_15_arp_flowchart.svg": """
direction: down

start: "Host wants to send packet to Target IP" { style.fill: "#f8fafc" }
check_cache: "Check local ARP cache: Is Target IP mapped?" { style.fill: "#fef3c7" }
found: "Target MAC Found in Cache\\nEncapsulate frame & transmit immediately" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
not_found: "Cache Miss: Queue IP datagram\\nBroadcast ARP Request (FF:FF:FF:FF:FF:FF)" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
wait_reply: "Wait for ARP Reply" { style.fill: "#f1f5f9" }
update_cache: "Receive Unicast ARP Reply\\nUpdate ARP table & transmit queued datagram" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }

start -> check_cache
check_cache -> found: "Yes (Hit)"
check_cache -> not_found: "No (Miss)"
not_found -> wait_reply -> update_cache
""",

        # 16. Diskless Boot Dilemma
        "fig2_16_diskless_boot_dilemma.svg": """
direction: right

diskless: "Diskless Workstation (Booting)\\n• Has 48-bit MAC in ROM\\n• Has NO hard drive / persistent storage\\n• Does NOT know its own IP address!" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

rarp_srv: "RARP Server\\nMaintains static database:\\n[MAC: 08:00:20:AA:BB:CC -> IP: 192.168.1.45]" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

diskless -> rarp_srv: "RARP Request: 'Here is my MAC, what is my IP?'"
""",

        # 17. RARP Request/Reply Workflow
        "fig2_17_rarp_workflow.svg": """
shape: sequence_diagram

Client: "Diskless Workstation"
Server: "RARP Server"

Client -> Server: "1. RARP Request (Broadcast: EtherType 0x8035)\\n'Sender MAC = Target MAC = MAC_Client, Target IP = 0.0.0.0'" { style.stroke: "#2563eb" }
Note over Server: Server matches MAC in /etc/ethers table
Server -> Client: "2. RARP Reply (Unicast: Target IP = 192.168.1.45)" { style.stroke: "#16a34a"; style.bold: true }
Note over Client: Workstation sets IP address and requests OS kernel via TFTP!
""",

        # 18. RARP Deprecation Reasons
        "fig2_18_rarp_deprecation.svg": """
direction: right

flaws: "Architectural Reasons Why RARP Was Deprecated" {
  f1: "1. Layer 2 Raw Frame: Non-routable; every subnet required a dedicated physical RARP server" { style.fill: "#fee2e2" }
  f2: "2. Returns ONLY IP: Does not return subnet mask, default gateway, or DNS servers" { style.fill: "#fee2e2" }
  f3: "3. Static Mapping: Requires manual administrator entry for every new workstation" { style.fill: "#fee2e2" }
}
""",

        # 19. Bootstrap Evolution Timeline
        "fig2_19_bootstrap_evolution.svg": """
direction: right

rarp: "RARP (1984)\\nRaw L2 Frame\\nIP address only\\nStatic binding" { style.fill: "#f8fafc" }
bootp: "BOOTP (1985)\\nUDP Port 67/68\\nRoutable via Relay\\nGateway + Subnet Mask" { style.fill: "#fef3c7" }
dhcp: "DHCP (1997)\\nDynamic IP Leasing\\nAutomatic Pool Management\\nRich Vendor Options" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }

rarp -> bootp -> dhcp
""",

        # 20. Error Taxonomy
        "fig2_20_transmission_error_taxonomy.svg": """
direction: right

single: "Single-Bit Error\\nOnly 1 bit in frame is flipped (e.g. white noise)\\nRare in high-speed links" { style.fill: "#dbeafe" }
burst: "Burst Error\\nMultiple contiguous bits corrupted (e.g. lightning, impulse noise)\\nDuration of noise > 1 bit period\\nMost common real-world error" { style.fill: "#fee2e2"; style.stroke: "#dc2626"; style.bold: true }

single -> burst
""",

        # 21. Two-Dimensional Parity Matrix
        "fig2_21_2d_parity_matrix.svg": """
direction: right

matrix: "Two-Dimensional (2D) Parity Generation Matrix (LRC + VRC)" {
  r1: "Byte 1: [1 0 0 1 1 0 1] -> Row Parity: 0" { style.fill: "#eff6ff" }
  r2: "Byte 2: [0 1 1 0 1 1 0] -> Row Parity: 0" { style.fill: "#eff6ff" }
  r3: "Byte 3: [1 1 0 1 0 0 1] -> Row Parity: 0" { style.fill: "#eff6ff" }
  col: "Col Parity (LRC): [0 0 1 0 0 1 0] -> Parity Bit: 0" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
}
""",

        # 22. CRC Modulo-2 Polynomial Division Flow
        "fig2_22_crc_polynomial_flow.svg": """
direction: right

msg: "Data Message M(x)\\nk bits" { style.fill: "#dbeafe" }
gen: "Generator Polynomial G(x)\\nDegree r (r+1 bits)" { style.fill: "#fef3c7" }
div: "Modulo-2 XOR Division\\nAppend r zeros: M(x) * 2^r / G(x)\\nRemainder R(x) = CRC Checksum" { style.fill: "#dcfce7"; style.stroke: "#16a34a"; style.bold: true }
frame: "Transmitted Codeword T(x)\\n[Data Message M(x) | CRC Remainder R(x)]" { style.fill: "#dbeafe" }

msg -> div
gen -> div
div -> frame
"""
    }

    for filename, code in d2_diagrams.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        svg_engine.compile_d2(code, out_path, theme=1)
    print(f"  Generated {len(d2_diagrams)} D2 publication diagrams.")

generate_d2_diagrams()
print("\nUnit 2 figure generation complete!")
