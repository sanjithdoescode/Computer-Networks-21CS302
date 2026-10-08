# AGENTS.md — Global Autonomous Agent Directive & Repository Guidelines

## 🌟 Repository Mission & Identity
This workspace is the **Official Master Exam Preparation & Academic Repository** for:
- **Course Code & Title**: **21CS302 / Computer Networks**
- **Target Standard**: Autonomous Engineering College & Anna University Curriculum (Professional Core, CSE/IT).
- **Core Textbooks**:
  1. *Behrouz A. Forouzan*, "Data Communications and Networking", 5th Edition, McGraw-Hill.
  2. *Andrew S. Tanenbaum & David J. Wetherall*, "Computer Networks", 5th Edition, Pearson.
  3. *William Stallings*, "Data and Computer Communications", 10th Edition, Pearson.
  4. *James F. Kurose & Keith W. Ross*, "Computer Networking: A Top-Down Approach", 8th Edition.

This repository is designed to serve as an exhaustive, self-contained study portal and solution manual for students preparing for university semester-end and internal assessment examinations.

---

## 🏛️ Syllabus Architecture (Five Units)
Any agent operating in this repository must map topics strictly according to this five-unit breakdown:
1. **UNIT I — Introduction and Physical Layer**: Networks, Network Types (PAN, LAN, MAN, WAN), Protocol Layering, OSI 7-Layer Model, TCP/IP Suite, Physical Layer Performance (Throughput, Jitter, Latency, Bandwidth), Transmission Media (Guided: Twisted Pair Cat3–Cat8, Coaxial, Fiber Optic Single/Multi-mode; Unguided: Radio, Microwave, Infrared), Switching (Circuit Switching, Message Switching, Packet Switching: Datagram vs. Virtual Circuit).
2. **UNIT II — Data Link Layer**: Link-Layer Addressing (MAC), Error Detection and Correction (Parity, Checksum, CRC-32, Hamming Codes), DLC Services, Framing (Byte/Bit stuffing), Flow Control & ARQ (Stop-and-Wait, Go-Back-N, Selective Repeat), HDLC, PPP, Media Access Control (ALOHA, Slotted ALOHA, CSMA, CSMA/CD, CSMA/CA), Wired LANs (Ethernet IEEE 802.3), Wireless LANs (Wi-Fi IEEE 802.11), Connecting Devices (Hubs, Repeaters, Bridges, Layer 2 Switches, Routers, Gateways).
3. **UNIT III — Network Layer**: Network Layer Services (Host-to-Host Delivery, Packetizing, Routing vs. Forwarding), IPv4 Addresses (Classful Addressing Classes A–E, Classless Addressing / CIDR, Subnetting & Supernetting), DHCP, ICMPv4, IPv6 Addressing & Transition (Dual Stack, Tunneling, Header comparison), Unicast Routing Algorithms (Distance Vector / Bellman-Ford, Link State / Dijkstra SPF), Unicast Routing Protocols (RIPv1/v2, OSPFv2/v3, BGP-4).
4. **UNIT IV — Transport Layer**: Transport Services (Process-to-Process Delivery, Sockets, Port Numbers), User Datagram Protocol (UDP datagram header, applications), Transmission Control Protocol (TCP segment header, 3-way handshake, 4-way teardown, Sliding Window flow control, Silly Window Syndrome, Tahoe/Reno Congestion Control: Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery), SCTP.
5. **UNIT V — Application Layer**: Client-Server & P2P Paradigms, World Wide Web & HTTP/HTTPS (HTTP/1.1 vs HTTP/2 vs HTTP/3 over QUIC), File Transfer Protocol (FTP active/passive modes), Electronic Mail (SMTP, POP3, IMAP4, MIME), Network Virtual Terminal (Telnet, Secure Shell - SSH), Domain Name System (DNS hierarchy, resolution, resource records), Simple Network Management Protocol (SNMP).

---

## ✍️ The Mandatory 16-Mark University Exam Standard

When generating answers for **Long Questions (16 Marks each)**, agents **MUST NEVER** provide brief summaries or bulleted overviews. University evaluators expect **4 to 5 handwritten exam pages per question**. To give students sufficient technical depth, every long answer must be an exhaustive masterclass structured with the following components:

### 1. Foundational Introduction & Historical Context
- Rationale, motivation, engineering challenges that necessitated the technology, and IETF RFC standards or IEEE specifications.

### 2. Dedicated Publication-Grade Vector Figures (2 to 5 per Question)
- Every major concept, lifecycle, state transition, and architecture must have a clear visual figure.
- **Figure Architecture & Standard**:
  - Figures are rendered as native vector SVGs placed in `UNIT - X/figures/` and referenced via markdown: `![Figure Description](figures/fig_name.svg)`.
  - **D2 (Declarative Diagramming 2.0)** with academic themes (`--theme=1`) for network architectures, topologies, and multi-host exchange sequences.
  - **Python Vector SVG Engine** (`scripts/figures/svg_engine.py`) for exact 32-bit packet and frame headers with bit rulers (IPv4, IPv6, TCP, UDP, SCTP, DNS, Ethernet, ARP, ICMP).
  - **Matplotlib IEEE/ACM Engine** for scientific performance curves and dynamics (TCP Tahoe vs. Reno AIMD sawtooth, Offered load vs. delay, Congestion Collapse Knee/Cliff).
  - **Graphviz (`dot`)** for protocol Finite State Machines (TCP 11-State FSM, OSPF Adjacency, DHCP Leases) and hierarchical naming trees.
  - In-line Mermaid blocks are deprecated across this repository in favor of standalone, retina-ready vector SVGs. All diagram source generators are archived and version-controlled in `scripts/figures/`.

### 3. Bit-Level Packet & Header Layouts
- Provide complete ASCII text diagrams representing the 32-bit wide header formats (e.g., IPv4, TCP, UDP, OSPF, DHCP, RIP, Ethernet).
- Provide an exhaustive, field-by-field breakdown detailing bit lengths, functions, default values, and operational significance.

### 4. Mathematical Formulations & Concrete Numerical Examples
- Render all formulas in clear LaTeX markdown (e.g., Shannon Channel Capacity, Nyquist Bit Rate, Bellman-Ford equation, Dijkstra tentative relaxation, Fragment Offsets, Subnetting host counts $2^h - 2$, OSPF cost $\frac{10^8}{\text{Bandwidth}}$, Sliding Window utilization $\frac{N}{1 + 2a}$).
- Always accompany formulas with a concrete step-by-step numerical calculation.

### 5. Algorithmic State Machines & Workflows
- Detailed step-by-step procedural walkthroughs (e.g., DHCP 4-step DORA exchange, CSMA/CA IFS countdown and NAV backoff, TCP 3-way handshake, OSPF 7-state adjacency lifecycle).

### 6. Multi-Parameter Comparison Matrices
- Comprehensive comparison tables with **8 to 15 distinct parameters** evaluating competing technologies, protocols, or algorithmic approaches.

### 7. Failure Modes, Edge Cases & Real-World Deployments
- Analyze vulnerabilities, edge cases (e.g., Count-to-Infinity in Distance Vector, Head-of-Line blocking in TCP, Hidden/Exposed Terminals in Wi-Fi, Bridge Loops in Layer 2) and their mitigations (Split Horizon, Poison Reverse, QUIC, RTS/CTS, Spanning Tree).

---

## 📁 Repository Directory & File Placement Standards

```
├── 5.Syllabus - CN.pdf                  # Official curriculum syllabus
├── .agents/rules/
│   └── exam_answers_style.md           # Formal rules file
├── AGENTS.md                           # Master agent guidelines (this file)
├── README.md                           # Repository overview and syllabus index
├── UNIT - 1/
│   ├── short_questions.md              # 2/5-mark question bank
│   ├── short_questions_answers.md      # Short answers guide with diagrams
│   ├── long_questions.md               # 16-mark essay questions
│   ├── long_questions_answers.md       # Long answers master guide
│   └── UNIT 1.pdf                      # Reference textbook / lecture notes
├── UNIT - 2/
│   └── UNIT 2.pdf                      # Reference notes
├── UNIT - 3/
│   ├── questions.md                    # Question bank
│   └── long_questions_answers.md       # 16-mark long answers master guide
└── ... (Subsequent Units: UNIT - 4, UNIT - 5)
```

---

## 🔄 Agent Operational Workflow

Whenever a user requests exam answers or adds new questions:
1. **Read & Align**: Check `questions.md` / `long_questions.md` in the target unit directory.
2. **Execute Full Academic Standard**: Draft the solutions in `long_questions_answers.md` or `short_questions_answers.md` following the 16-mark university standard outlined above.
3. **Validate Mermaid Syntax**: Run verification scripts to ensure all diagrams use supported Mermaid syntax and contain no parse errors.
4. **Update README.md**: Synchronize the master table of contents and question lists in `README.md`.
5. **Git Version Control**: Stage, commit with descriptive academic messages, and push to GitHub on the `master` branch.
