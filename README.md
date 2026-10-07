# Computer Networks (21CS302) — Comprehensive Exam Preparation & Study Guide

Repository containing study notes, question banks, university exam preparation material, and detailed visual solution guides for **Computer Networks (21CS302)**.

---

## 📕 Complete Master Exam Preparation Textbook (PDF)
> 🎓 **Official Publication**: **[`Computer_Networks_21CS302_Master_Textbook.pdf`](Computer_Networks_21CS302_Master_Textbook.pdf)**  
> **Pages**: 341 Pages (A4) &bull; **Vector Architectural Diagrams**: 162 SVG Figures &bull; **Math**: Typeset via KaTeX  
> **Target Standard**: Autonomous Engineering Institutions & Anna University Regulations 2021  
> **Complete Solution Manual**: Eliminates the need for multiple textbooks or internet searching during exam preparation.
> 
> * **Front Matter**: Official Syllabus (CO1–CO5), 16-Mark University Exam Scoring Blueprint, and Hyperlinked Master Table of Contents.
> * **Unit I**: 11 Short Questions (2/5 Marks) + 5 Long Essays (16 Marks) with 40 Diagrams.
> * **Unit II**: 5 Long Essays (16 Marks) with 22 Diagrams.
> * **Unit III**: 9 Long Essays (16 Marks) with 47 Diagrams.
> * **Unit IV**: 5 Comprehensive Thematic Chapters covering all Q1–Q11 with 29 Diagrams.
> * **Unit V**: 8 Long Essays (16 Marks) with 24 Diagrams.
> * **Appendices**: Master Acronym Dictionary (75+ terms), Complete Port Numbers & Protocols Master Matrix, and Comprehensive Exam Formula Sheet.

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
│   ├── question.md                     # Unit 2 question bank
│   ├── long_questions_answers.md       # Comprehensive 4-5 page long answers with 22 Mermaid diagrams
│   ├── UNIT 2.pdf                      # Unit 2 reference notes
│   └── UNIT 2 NOTES.pdf                # Supplementary unit notes
├── UNIT - 3/
│   ├── questions.md                    # Unit 3 question bank
│   └── long_questions_answers.md       # Comprehensive 4-5 page long answers with 47 Mermaid diagrams
├── UNIT - 4/
│   ├── questions.md                    # Unit 4 question bank
│   └── long_questions_answers.md       # Comprehensive 4-5 page long answers with 29 Mermaid diagrams
├── UNIT - 5/
│   ├── questions.md                    # Unit 5 question bank
│   └── long_questions_answers.md       # Comprehensive 4-5 page long answers with 24 Mermaid diagrams
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

## 📖 Unit 2 Coverage (Data Link Layer & MAC)

### 📑 16-Mark Long Questions Master Guide
Available in: [UNIT - 2/long_questions_answers.md](UNIT%20-%202/long_questions_answers.md)
1. **Duties of the Data Link Layer**: Hop-to-hop frame delivery; LLC (IEEE 802.2) vs. MAC (IEEE 802.3/802.11) sublayers; Framing methods (Byte Stuffing with ESC flags, Bit Stuffing with `01111110` flag delimiter); 48-bit physical MAC addressing; flow control & error control (ARQ); channel access arbitration.
2. **Unicast, Multicast, and Broadcast Transmission Modes**: Detailed examination of One-to-One, One-to-All (Limited `255.255.255.255` vs. Directed broadcast, broadcast storms), One-to-Many (Class D multicast, the 32:1 Ethernet MAC mapping ambiguity `01:00:5E`, IGMP), and One-to-Nearest (Anycast BGP routing).
3. **Address Resolution Protocol (ARP)**: Bridging logical IP and physical MAC addresses; complete 28-byte RFC 826 packet format; broadcast Request & unicast Reply; ARP cache table aging timers; ARP cache poisoning attacks; Gratuitous ARP and Proxy ARP.
4. **Reverse Address Resolution Protocol (RARP)**: Diskless workstation bootstrap dilemma; RFC 903 packet structure and EtherType `0x8035`; broadcast Request & unicast Reply; architectural flaws (Layer 2 non-routable, IP only, static allocation); evolution into BOOTP and DHCP.
5. **Error Detection and Correction**: Single-bit vs. burst errors; Hamming distance bounds ($d_{\text{min}} \ge s+1$ for detection, $d_{\text{min}} \ge 2t+1$ for correction); Simple (1D) vs. Two-Dimensional (2D) Parity; Internet Checksum (1's complement math); Cyclic Redundancy Check (CRC Modulo-2 polynomial division walkthrough); Hamming Code ($2^r \ge m + r + 1$) complete encoding, error injection, and syndrome correction trace.


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

---

## 📖 Unit 4 Coverage (Transport Layer Protocols & Services)

### 📑 16-Mark Long Questions Master Guide
Available in: [UNIT - 4/long_questions_answers.md](UNIT%20-%204/long_questions_answers.md)
1. **Duties of the Transport Layer**:
   - Architectural placement (OSI vs. TCP/IP) as the critical software-to-hardware boundary and liaison.
   - Process-to-Process delivery scope vs. Host-to-Host (IP) vs. Hop-to-Hop (Data Link).
   - Port number mechanisms and IANA allocations (Well-Known 0–1023, Registered 1024–49151, Ephemeral 49152–65535) and 5-tuple connection identifier.
   - Multiplexing at sender and demultiplexing at receiver (connectionless 2-tuple vs. connection-oriented 4-tuple).
   - End-to-end flow control (sliding window buffer management vs. link flow control).
   - End-to-end error control (checksums, sequence numbers, cumulative ACKs, duplicate suppression, out-of-order buffering).
   - Congestion control principles (detecting loss/delay, network core protection, $cwnd$).
   - Master comparison matrix: Transport Layer vs. Network Layer vs. Data Link Layer (10 parameters).
2. **User Datagram Protocol (UDP)**:
   - Design philosophy (RFC 768), minimalist overhead, stateless operation, un-throttled rate, message-oriented record preservation.
   - Bit-level 8-byte header format: Source Port (16b), Destination Port (16b), Length (16b), Checksum (16b).
   - UDP 12-byte IPv4 / 40-byte IPv6 Pseudo-Header layout and 1's complement checksum arithmetic walkthrough.
   - Complete step-by-step numerical checksum computation and verification trace with hexadecimal words.
   - Prominent applications (DNS :53, DHCP :67/68, TFTP :69, NTP :123, SNMP :161, RIP :520, RTP :5004, QUIC :443).
   - Vulnerabilities (IP spoofing, DNS amplification attacks) and mitigations (BCP 38 ingress filtering, Response Rate Limiting).
   - Master comparison matrix: UDP vs. TCP vs. Raw IP (14 parameters).
3. **Transmission Control Protocol (TCP)**:
   - Design philosophy (RFC 793, RFC 9293) and reliable full-duplex byte-stream virtual circuit abstraction.
   - Exhaustive 20–60 byte segment header bit breakdown (Seq Num, Ack Num, Data Offset, Flags [URG, ACK, PSH, RST, SYN, FIN, ECE, CWR], Window Size, Checksum, Urgent Pointer, Options: MSS, Window Scale, SACK, Timestamps).
   - Connection management: 3-way handshake (`SYN` $	o$ `SYN+ACK` $	o$ `ACK`), SYN flood vulnerability and cryptographic SYN Cookie defense.
   - Connection teardown: 4-way handshake (`FIN` $	o$ `ACK` $	o$ `FIN` $	o$ `ACK`), half-close state, `TIME_WAIT` state and $2	imes	ext{MSL}$ rationale.
   - Complete 11-state TCP Finite State Machine (FSM) state diagram.
   - Flow control sliding window dynamics; Silly Window Syndrome mitigations: Sender-side **Nagle's Algorithm** (RFC 896) vs. Receiver-side **Clark's Solution** (RFC 813).
   - Congestion control: Slow Start ($CWND$ exponential doubling), Congestion Avoidance (additive increase $+1	ext{ MSS}$/RTT), Fast Retransmit (3 duplicate ACKs), and Fast Recovery (**TCP Tahoe vs. TCP Reno**).
   - Error control and dynamic RTT estimation: **Jacobson's algorithm** ($SRTT$, $RTTVAR$, $RTO = SRTT + 4 	imes RTTVAR$) with numerical walkthrough, and **Karn's algorithm** for retransmissions.
4. **Stream Control Transmission Protocol (SCTP)**:
   - Historical motivation and IETF SIGTRAN roots (RFC 4960) for carrier-grade telephony signaling (SS7 over IP).
   - Two core architectural breakthroughs:
     - **Multi-Homing**: Binding multiple IP addresses to a single association, primary path transmission with automatic, transparent failover via heartbeat probes.
     - **Multi-Streaming**: Up to 65,536 independent streams per association, completely eliminating TCP Head-of-Line (HoL) blocking.
     - Message-oriented framing preserving application record boundaries.
   - Packet and Chunk architecture: 12-byte Common Header (Source/Dest Port, Verification Tag, 32-bit CRC-32c checksum) and control/data chunks (`INIT`, `INIT_ACK`, `COOKIE_ECHO`, `COOKIE_ACK`, `DATA`, `SACK`, `HEARTBEAT`, `SHUTDOWN`).
   - DATA chunk layout: TSN, Stream ID, Stream Sequence Number (SSN), U/B/E fragmentation flags, PPID.
   - Association lifecycle: 4-way handshake with cryptographic **State Cookie** (inherent immunity against SYN flood memory exhaustion attacks), and 3-way graceful association teardown.
   - Master comparison matrix: TCP vs. UDP vs. SCTP (12 parameters).
5. **TCP Services & Core Mechanics (Covers Q5–Q11)**:
   - Comprehensive ten-pillar architecture of TCP transport services.
   - Process-to-process delivery, stream delivery with circular send/receive ring buffers, MSS chunking.
   - Full-duplex communication and piggybacked acknowledgments.
   - 4-tuple socket demultiplexing supporting high-concurrency server daemons.
   - Connection-oriented stateful session tracking (TCB records).
   - Reliable delivery and error recovery services (cumulative ACKs, SACK RFC 2018, duplicate suppression, out-of-order reordering).
   - Flow control with Advertised Window ($rwnd$) and Zero Window probing via persistence timer.
   - Congestion control service via AIMD and rate adaptation.
   - Quality of service, priority, out-of-band data (`URG`), and immediate buffer flushing (`PSH`).
   - Mathematical formulations: Bandwidth-Delay Product ($BDP = \text{Bandwidth} \times RTT$), TCP Window Scale option ($2^{16} \to 2^{30}$ bytes), and sliding window protocol efficiency ($\eta = \min(1, \frac{W}{1+2a})$) with step-by-step numerical examples.
   - Master comparison matrix: Byte-Stream Service (TCP) vs. Message-Oriented Service (UDP / SCTP).

---

## 📖 Unit 5 Coverage (Application Layer Protocols & Architectures)

### 📑 16-Mark Long Questions Master Guide
Available in: [UNIT - 5/long_questions_answers.md](UNIT%20-%205/long_questions_answers.md)
1. **HyperText Transfer Protocol (HTTP)**:
   - Universal web architecture, statelessness, and request-response lifecycle.
   - Request methods (GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH, CONNECT) and 5-tier status code taxonomy (1xx–5xx).
   - Plaintext message framing: Request Line, Status Line, and RFC 5322 CRLF delimiters.
   - Architectural evolution: Non-persistent HTTP/1.0 (2 RTT per object), Persistent HTTP/1.1 (Keep-Alive, pipelining, and application HoL blocking), HTTP/2 (Binary Framing Layer, multiplexed streams, stream prioritization, HPACK compression, Server Push), and HTTP/3 (QUIC over UDP, zero transport HoL blocking, 0-RTT/1-RTT handshakes, connection migration).
   - Web caching mechanics, conditional GET validators (`ETag` / `Last-Modified`), and stateful cookie management (RFC 6265).
   - Master comparison matrix: HTTP/1.0 vs. HTTP/1.1 vs. HTTP/2 vs. HTTP/3 (10 parameters).
2. **Simple Mail Transfer Protocol (SMTP)**:
   - Electronic mail framework: Mail User Agent (MUA), Mail Submission Agent (MSA :587), Mail Transfer Agent (MTA :25), Mail Delivery Agent (MDA), and physical mailbox spools.
   - Three-phase interactive dialogue: Session Handshake (`HELO`/`EHLO`), Mail Transfer Dialogue (`MAIL FROM:`, `RCPT TO:`, `DATA`), and Graceful Teardown (`QUIT`).
   - Multipurpose Internet Mail Extensions (MIME - RFC 2045–2049) overcoming 7-bit ASCII constraints.
   - Step-by-step mathematical Base64 encoding walkthrough: 24-bit splitting, 6-bit grouping, alphabet lookup, and padding mechanics.
   - Modern anti-spoofing and security frameworks: SPF DNS TXT records, DKIM cryptographic signatures, DMARC policies, and opportunistic STARTTLS encryption.
   - Master comparison matrix: SMTP vs. POP3 vs. IMAP4 (7 parameters).
3. **File Transfer Protocol (FTP)**:
   - Out-of-band dual-connection architecture (RFC 959): Persistent Control Connection (TCP :21) vs. Ephemeral Data Connection (TCP :20 / ephemeral).
   - Active FTP Mode (`PORT`) mechanics and why client-side firewalls/NAT drop unsolicited inbound server connections.
   - Passive FTP Mode (`PASV`) mechanics resolving NAT traversal by having clients initiate outbound data connections.
   - Data representations (ASCII, Image/Binary, EBCDIC), file structures (File, Record, Page), and transmission modes (Stream, Block, Compressed).
   - Core command/response vocabulary and secure alternatives (FTPS over TLS vs. SFTP over SSH).
   - Master comparison matrix: Active FTP vs. Passive FTP vs. TFTP (8 parameters).
4. **Domain Name System (DNS)**:
   - Hierarchical naming tree: Root (`.`), Generic and Country-Code TLDs, Second-Level Domains, Subdomains, FQDNs, and administrative zones.
   - Comprehensive resolution mechanics: Client-to-Resolver Recursive resolution vs. Resolver-to-Hierarchy Iterative resolution.
   - Fixed 12-byte header bit layout (ID, QR, Opcode, AA, TC, RD, RA, RCODE, record counts).
   - Complete Resource Record (RR) taxonomy: `A`, `AAAA`, `CNAME`, `MX`, `NS`, `PTR`, `SOA`, and `TXT`.
   - Dual-transport rationale: UDP Port 53 (queries < 512 bytes) vs. TCP Port 53 (zone transfers and large responses when `TC=1`).
   - Vulnerabilities (Kaminsky cache poisoning, amplification attacks) and DNSSEC cryptographic protection.
5. **Post Office Protocol Version 3 (POP3)**:
   - Architectural role as a pull-based store-and-forward mail access protocol (TCP :110 / :995).
   - Three-state lifecycle finite state machine: **Authorization State** (`USER`, `PASS`, `APOP`), **Transaction State** (`STAT`, `LIST`, `RETR`, `DELE`, `NOOP`, `RSET`), and **Update State** (`QUIT` unlinking marked messages).
   - Operational modes: Download-and-Delete vs. Download-and-Keep.
   - Server status indicators (`+OK` / `-ERR`) and full session transcript walkthrough.
   - Architectural limitations and comprehensive comparison matrix: POP3 vs. IMAP4 (8 parameters).
6. **TELNET (Teletype Network)**:
   - ARPANET remote timesharing foundations and the Network Virtual Terminal (NVT) character/newline abstraction (RFC 854).
   - In-band signaling and the Interpret As Command (`IAC` = `0xFF`) escape byte mechanism.
   - Symmetric 4-verb option negotiation: `WILL`, `WONT`, `DO`, `DONT`, subnegotiation (`SB`/`SE`), and loop prevention.
   - Common negotiated options: Echo, Suppress Go Ahead, NAWS (terminal window size).
   - Plaintext credentials and packet-sniffing vulnerabilities leading to complete deprecation.
7. **Secure Shell (SSH)**:
   - Layered architecture (RFC 4251–4254): SSH Transport Layer, SSH User Authentication Layer, SSH Connection Layer on TCP Port 22.
   - Ephemeral Diffie-Hellman cryptographic handshake and mathematical session key derivation ($K = g^{xy} mod p$).
   - Host key authenticity verification (`~/.ssh/known_hosts`) and client authentication (Ed25519/RSA public keys, passwords).
   - SSH Port Forwarding / Tunneling: Local (`-L`), Remote (`-R`), and Dynamic SOCKS5 (`-D`) proxy mechanics.
   - Master comparison matrix: TELNET vs. SSH (10 parameters).
8. **Difference between HTTP and HTTPS**:
   - Architectural comparison: HTTP directly over TCP (:80) vs. HTTPS with TLS cryptographic sublayer (:443).
   - TLS Handshake lifecycle: Cipher suite negotiation, X.509 CA certificate verification, key exchange, symmetric session encryption (AES-GCM / ChaCha20).
   - Confidentiality, integrity, and authentication guarantees.
   - Performance impacts (TLS 1.3 1-RTT/0-RTT optimization, hardware AES-NI acceleration) and web browser security standards.
   - Master comparison matrix: HTTP vs. HTTPS (10 parameters).
