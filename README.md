# Computer Networks (21CS302) — Comprehensive Exam Preparation & Study Guide

Repository containing study notes, question banks, university exam preparation material, and detailed visual solution guides for **Computer Networks (21CS302)**.

---

## 📚 Repository Structure

```
├── 5.Syllabus - CN.pdf                  # Official Course Syllabus & Curriculum
├── UNIT - 1/
│   ├── short_questions.md              # 2-mark & 5-mark short questions
│   ├── short_questions_answers.md      # Detailed solutions with diagrams and comparison tables
│   ├── long_questions.md               # 16-mark essay questions
│   ├── long_questions_answers.md       # Comprehensive 4-5 page long answers with 29 Mermaid diagrams
│   └── UNIT 1.pdf                      # Lecture slides and unit reference notes
├── UNIT - 2/
│   └── UNIT 2.pdf                      # Unit 2 reference notes & materials
├── UNIT - 3/
│   ├── questions.md                    # Unit 3 question bank
│   └── long_questions_answers.md       # Comprehensive 4-5 page long answers with 27 Mermaid diagrams
├── .agents/rules/
│   └── exam_answers_style.md           # 16-mark long answers academic style rule
├── AGENTS.md                           # Global agent behavior & repository standards
└── README.md
```

---

## 📖 Unit 1 Coverage

### 📝 Short Questions & Answers
Available in: [UNIT - 1/short_questions_answers.md](UNIT%20-%201/short_questions_answers.md)
1. Define Networks
2. Types of Networks (PAN, LAN, MAN, WAN)
3. Types of Layers (OSI 7-Layer & TCP/IP 5-Layer Models)
4. Summarize Transmission Media (Guided & Unguided)
5. Define Jitter and Throughput
6. Difference between TCP & UDP
7. Difference between Circuit Switching and Packet Switching
8. Contrast between Switch and Router
9. Explain about Topology (Mesh, Star, Bus, Ring, Tree)
10. Define Data Communication
11. Type of Line Configuration (Point-to-Point vs. Multipoint)

### 📑 16-Mark Long Questions Master Guide
Available in: [UNIT - 1/long_questions_answers.md](UNIT%20-%201/long_questions_answers.md)
1. **The OSI 7-Layer Reference Model**: ISO principles, peer-to-peer processes, encapsulation/decapsulation, in-depth analysis of all 7 layers, master summary table, and OSI vs. TCP/IP comparison.
2. **TCP & UDP Transport Architecture**: Bit-level header formats, 3-way handshake, 4-way teardown, sliding window flow control, Tahoe/Reno congestion control, and QUIC/HTTP-3 case studies.
3. **Switching Techniques**: Space/Time division circuit switching, message switching store-and-forward, datagram vs. virtual circuit packet switching, and mathematical delay pipelining proofs.
4. **Network Topologies**: Physical vs. logical topologies, Mesh, Star, Bus, Ring, Tree, formulas ($N(N-1)/2$), CSMA/CD, and token passing dynamics.
5. **Transmission Media**: Nyquist and Shannon channel capacity theorems, twisted pair physics & categories (Cat 3 to Cat 8), coaxial types, fiber optics (TIR, SMF vs. MMF), and wireless electromagnetic propagation (ground wave, sky wave, line-of-sight).

---

## 📖 Unit 3 Coverage (Network Layer & Routing)

### 📑 16-Mark Long Questions Master Guide
Available in: [UNIT - 3/long_questions_answers.md](UNIT%20-%203/long_questions_answers.md)
1. **Duties of the Network Layer**: Host-to-host delivery, packetizing, hierarchical logical addressing, routing vs. forwarding, fragmentation/reassembly, ICMP error reporting, and QoS/traffic shaping.
2. **Different Address Classes (Class A, B, C, D, E)**: Dotted-decimal notation, leading-bit rules, network/host splits, usable hosts, private IP blocks (RFC 1918), reserved blocks (loopback, APIPA, broadcast), and CIDR evolution.
3. **Routing Techniques**:
   - *Distance Vector Routing*: Bellman-Ford algorithm, convergence walkthrough, Count-to-Infinity problem, Split Horizon, Poison Reverse, and hold-down timers.
   - *Link State Routing*: Dijkstra's algorithm, shortest path tree (SPT), reliable flooding of LSPs, and LSDB synchronization.
   - *Spanning Tree Protocol (IEEE 802.1D)*: Bridge loop disasters (broadcast storms, MAC table instability), root bridge election, port states (blocking $\to$ forwarding).
4. **Carrier Sense Multiple Access with Collision Avoidance (CSMA/CA)**: Physical reasons why CSMA/CD fails in wireless, Hidden/Exposed terminal problems, tiered IFS (SIFS, PIFS, DIFS, EIFS), randomized exponential backoff ($CW$), 4-way RTS/CTS handshake, and NAV virtual carrier sensing.
5. **Internet Protocol Version 4 (IPv4)**: Complete 32-bit header field breakdown (Version, IHL, DSCP, ECN, Total Length, ID, Flags, Offset, TTL, Protocol, Checksum), mathematical MTU fragmentation walkthrough, subnetting formulas ($2^s$, $2^h - 2$), and IPv4 vs. IPv6 comparison.
6. **Routing Protocols (OSPF, RIP, and BGP)**:
   - *RIP (v1/v2)*: Hop count metric, 15-hop limit, 30s updates over UDP 520, classful vs. classless.
   - *OSPF (v2/v3)*: Inverse bandwidth cost, 2-tier area hierarchy (Backbone Area 0, ABR, ASBR), 5 packet types, DR/BDR election, Dijkstra SPF over IP protocol 89.
   - *BGP-4*: Path Vector EGP, AS-PATH loop prevention, policy routing attributes (NEXT_HOP, LOCAL_PREF, MED), reliable peering over TCP 179.
7. **Dynamic Host Configuration Protocol (DHCP)**:
   - Evolutionary progression (RARP $\to$ BOOTP $\to$ DHCP), 3 allocation modes (Dynamic, Automatic, Static MAC reservation).
   - 32-bit header field breakdown (op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file, options with magic cookie).
   - 4-step DORA lifecycle (Discover, Offer, Request, Acknowledge) and Gratuitous ARP verification.
   - Lease renewal state machine ($T_1$ 50% unicast, $T_2$ 87.5% broadcast, expiration 100%).
   - Cross-subnet DHCP Relay Agent architecture (`ip helper-address`), DHCP Starvation & Rogue Server attacks.
8. **Congestion Control Algorithms**:
   - Network congestion root causes, offered load vs. throughput curve, Knee and Cliff thresholds, congestion collapse.
   - Open-Loop vs. Closed-Loop taxonomy.
   - Traffic Shaping: **Leaky Bucket** (FIFO queue, constant output rate) vs. **Token Bucket** (token accumulation, controlled bursts).
   - Mathematical proof of Maximum Burst Duration ($T = \frac{C}{M - r}$) and burst volume with numerical calculations.
   - Closed-Loop feedback: Hop-by-Hop Backpressure, Choke Packets, and Explicit Congestion Notification (ECN - RFC 3168 with RED marking and TCP ECE/CWR flags).
9. **Network Layer Protocols (Overview Suite)**:
   - *IPv6 (RFC 8200)*: 128-bit addresses, colon-hexadecimal notation, fixed 40-byte base header, extension headers, and transition mechanisms (Dual Stack, Tunneling, NAT64).
   - *ICMP (RFC 792)*: Diagnostic error reporting (Destination Unreachable, Time Exceeded, Parameter Problem) and query mechanisms (`ping` Echo Request/Reply and `traceroute` TTL expiration).
   - *ARP (RFC 826)*: Dynamic Layer 3 Logical IP to Layer 2 Physical MAC resolution, broadcast Request, unicast Reply, ARP cache table, Gratuitous ARP, and Proxy ARP.
   - *RARP (RFC 903)*: Reverse resolution (Physical MAC to Logical IP) for diskless workstations, broadcast Request, unicast Reply, and deprecation reasons.
   - *IGMP (RFC 2236)*: Managing multicast group memberships on local subnets, General Query (`224.0.0.1`), Membership Report, Leave Group (`224.0.0.2`), and switch IGMP Snooping.
   - *BGP (RFC 4271)*: Path Vector inter-domain routing between Autonomous Systems, AS-PATH loop immunity, peering over TCP Port 179, and eBGP vs. iBGP.
   - Master Comparison Matrix: 10-parameter evaluation across all 6 companion protocols.



