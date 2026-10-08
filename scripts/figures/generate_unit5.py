#!/usr/bin/env python3
"""
scripts/figures/generate_unit5.py
Generates all publication-grade figures for UNIT 5 (Application Layer).
Produces SVGs in UNIT - 5/figures/
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_engine

OUTPUT_DIR = os.path.abspath("UNIT - 5/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating Unit 5 figures in: {OUTPUT_DIR}")

# ==============================================================================
# 1. Packet & Message Headers (Python Vector SVG Engine)
# ==============================================================================

def generate_headers():
    # 1. DNS 12-Byte Message Header (6 rows of 16 bits = 3 rows of 32 bits)
    dns_rows = [
        [("Identification (ID)", 16, "seq", "16 Bits (Transaction ID for Query-Response Matching)"),
         ("QR", 1, "flag", "1b"),
         ("Opcode", 4, "type", "4b"),
         ("AA", 1, "flag", "1b"),
         ("TC", 1, "flag", "1b"),
         ("RD", 1, "flag", "1b"),
         ("RA", 1, "flag", "1b"),
         ("Z", 3, "reserved", "3b"),
         ("RCODE", 4, "control", "4b")],
        [("Total Questions (QDCOUNT)", 16, "length", "16 Bits (Number of Question Entries)"),
         ("Total Answer RRs (ANCOUNT)", 16, "length", "16 Bits (Number of Resource Records)")],
        [("Total Authority RRs (NSCOUNT)", 16, "length", "16 Bits (Authoritative Name Servers)"),
         ("Total Additional RRs (ARCOUNT)", 16, "length", "16 Bits (Additional Records: e.g. A records)")]
    ]
    svg_engine.draw_32bit_packet_header(
        "RFC 1035: Domain Name System (DNS) 12-Byte Message Header",
        dns_rows,
        os.path.join(OUTPUT_DIR, "fig5_hdr_dns.svg")
    )

generate_headers()
print("  Generated DNS message headers.")

# ==============================================================================
# 2. Graphviz DOT State Machines & Trees
# ==============================================================================

def generate_dot_diagrams():
    # Fig 5.12: DNS Hierarchical Tree
    dns_tree_dot = """
    digraph DNS_Tree {
        graph [rankdir=TB, bgcolor="transparent", fontname="Helvetica", pad="0.2", nodesep="0.3", ranksep="0.5"];
        node [shape=box, style="filled,rounded", fontname="Helvetica-Bold", fontsize=10, margin="0.15,0.08", fillcolor="#f8fafc", color="#64748b", penwidth=1.3];
        edge [fontname="Helvetica", fontsize=8, color="#334155", penwidth=1.1, arrowsize=0.7];

        ROOT [label="Root Domain (.)\\n[13 Root Server Clusters: A.root ... M.root]", fillcolor="#fee2e2", color="#dc2626", fontcolor="#991b1b", penwidth=2.0];
        
        COM [label=".com (gTLD)\\n[VeriSign]", fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        ORG [label=".org (gTLD)\\n[PIR]", fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        EDU [label=".edu (gTLD)\\n[Educause]", fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        IN [label=".in (ccTLD)\\n[NIXI - India]", fillcolor="#e0e7ff", color="#4338ca", fontcolor="#312e81"];
        UK [label=".uk (ccTLD)\\n[Nominet - UK]", fillcolor="#e0e7ff", color="#4338ca", fontcolor="#312e81"];

        ROOT -> {COM; ORG; EDU; IN; UK};

        GOOGLE [label="google.com\\n[Authoritative NS]", fillcolor="#dcfce7", color="#16a34a", fontcolor="#14532d"];
        ANNAUNIV [label="annauniv.edu\\n[Authoritative NS]", fillcolor="#dcfce7", color="#16a34a", fontcolor="#14532d"];

        COM -> GOOGLE;
        EDU -> ANNAUNIV;

        WWW [label="www.google.com\\n(A: 142.250.190.46)", fillcolor="#eff6ff", color="#2563eb", fontcolor="#1e40af"];
        MAIL [label="mail.google.com\\n(CNAME: google.com)", fillcolor="#eff6ff", color="#2563eb", fontcolor="#1e40af"];

        GOOGLE -> {WWW; MAIL};
    }
    """
    svg_engine.compile_dot(dns_tree_dot, os.path.join(OUTPUT_DIR, "fig5_12_dns_hierarchy_tree.svg"))

    # Fig 5.15: POP3 3-State Finite State Machine
    pop3_dot = """
    digraph POP3_FSM {
        graph [rankdir=LR, bgcolor="transparent", fontname="Helvetica", pad="0.3", nodesep="0.6", ranksep="0.8"];
        node [shape=box, style="filled,rounded", fontname="Helvetica-Bold", fontsize=10, margin="0.2,0.1", fillcolor="#f8fafc", color="#64748b", penwidth=1.5];
        edge [fontname="Helvetica", fontsize=9, color="#334155", penwidth=1.2, arrowsize=0.8];

        START [shape=circle, width=0.3, style=filled, fillcolor="#0f172a", label=""];
        AUTH [label="AUTHORIZATION STATE\\n• USER <username>\\n• PASS <password>\\n• APOP (MD5 Challenge)", fillcolor="#fef3c7", color="#d97706", fontcolor="#92400e"];
        TRANS [label="TRANSACTION STATE\\n• STAT (Total msgs & bytes)\\n• LIST (Message sizes)\\n• RETR <msg> (Fetch)\\n• DELE <msg> (Mark delete)\\n• RSET (Undo marks)", fillcolor="#dcfce7", color="#16a34a", fontcolor="#14532d", penwidth=2.2];
        UPDATE [label="UPDATE STATE\\n• Server deletes marked msgs\\n• Releases mailbox lock\\n• Closes TCP :110 session", fillcolor="#fee2e2", color="#dc2626", fontcolor="#991b1b"];
        END [shape=doublecircle, width=0.3, style=filled, fillcolor="#0f172a", label=""];

        START -> AUTH [label=" TCP Port 110 Open\\n(+OK Server Ready)"];
        AUTH -> TRANS [label=" Valid Credentials\\n(+OK Mailbox Locked)"];
        AUTH -> END [label=" QUIT (Abort) / Failed Auth"];
        TRANS -> UPDATE [label=" QUIT (Graceful Exit)"];
        UPDATE -> END [label=" Session Terminated"];
    }
    """
    svg_engine.compile_dot(pop3_dot, os.path.join(OUTPUT_DIR, "fig5_15_pop3_fsm.svg"))

generate_dot_diagrams()
print("  Generated Graphviz DOT state machines and hierarchy trees.")

# ==============================================================================
# 3. D2 Publication Diagrams (Architectures, Flows & Sequences)
# ==============================================================================

def generate_d2_diagrams():
    d2_diagrams = {
        # 1. Universal Web Architecture
        "fig5_01_web_architecture.svg": """
direction: right

client: "Client Web Browser\\n(Chrome / Firefox)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

cache: "Forward Proxy / CDN Cache\\n(Cloudflare / Fastly)\\nLocal Cache Check" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

origin: "Origin Web Server\\n(Nginx / Apache)\\nDatabase & App Logic" {
  style.fill: "#ecfdf5"
  style.stroke: "#059669"
}

client -> cache: "1. HTTP Request\\n(GET /index.html)"
cache -> origin: "2. Cache Miss: Fetch from Origin" {
  style.stroke-dash: 3
}
origin -> cache: "3. HTTP 200 OK + Content"
cache -> client: "4. Return Cached Object"
""",

        # 2. HTTP Request-Response Lifecycle
        "fig5_02_http_lifecycle.svg": """
shape: sequence_diagram

Client: "Browser"
Server: "Web Server"

Client -> Server: "1. TCP 3-Way Handshake (SYN -> SYN+ACK -> ACK)" {
  style.stroke: "#64748b"
}
Client -> Server: "2. HTTP GET /api/data HTTP/1.1\\nHost: example.com\\nUser-Agent: Mozilla/5.0" {
  style.stroke: "#2563eb"
}
Note over Server: Server processes request & queries database
Server -> Client: "3. HTTP/1.1 200 OK\\nContent-Type: application/json\\nContent-Length: 420" {
  style.stroke: "#16a34a"
}
Client -> Server: "4. Connection: keep-alive (Reuses socket for next request)" {
  style.stroke: "#059669"
}
""",

        # 3. HTTP Status Code Taxonomy
        "fig5_03_http_status_codes.svg": """
direction: right

c1: "1xx: Informational\\n100 Continue\\n101 Switching Protocols" {
  style.fill: "#f1f5f9"
}

c2: "2xx: Success\\n200 OK\\n201 Created\\n204 No Content" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

c3: "3xx: Redirection\\n301 Moved Permanently\\n304 Not Modified" {
  style.fill: "#e0e7ff"
  style.stroke: "#4338ca"
}

c4: "4xx: Client Error\\n400 Bad Request\\n403 Forbidden\\n404 Not Found" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

c5: "5xx: Server Error\\n500 Internal Error\\n502 Bad Gateway\\n503 Unavailable" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

c1 -> c2 -> c3 -> c4 -> c5
""",

        # 4. Generational Evolution
        "fig5_04_http_evolution.svg": """
direction: right

h10: "HTTP/1.0 (1996)\\n• Non-persistent\\n• 1 TCP handshake per file\\n• 2 RTT overhead per asset" {
  style.fill: "#f8fafc"
}

h11: "HTTP/1.1 (1997)\\n• Persistent connections (Keep-Alive)\\n• Pipelining (rarely deployed)\\n• Head-of-Line (HoL) blocking" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

h20: "HTTP/2 (2015)\\n• Binary Framing Layer\\n• Multiplexed streams over 1 TCP\\n• HPACK header compression\\n• Server Push" {
  style.fill: "#e0e7ff"
  style.stroke: "#4338ca"
}

h30: "HTTP/3 (2022)\\n• QUIC over UDP\\n• Zero Transport HoL Blocking\\n• 0-RTT Connection Resumption\\n• Connection Migration" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

h10 -> h11 -> h20 -> h30
""",

        # 5. HTTP/2 Binary Framing & Multiplexing
        "fig5_05_http2_multiplexing.svg": """
shape: sequence_diagram

Client: "Browser"
Server: "HTTP/2 Server"

Note over Client,Server: Single Shared TCP Connection (Port 443)
Client -> Server: "Stream 1: HEADERS (GET /style.css)" {
  style.stroke: "#2563eb"
}
Client -> Server: "Stream 3: HEADERS (GET /script.js)" {
  style.stroke: "#7c3aed"
}
Server -> Client: "Stream 1: DATA (CSS payload chunk 1)" {
  style.stroke: "#2563eb"
}
Server -> Client: "Stream 3: DATA (JS payload chunk 1 - INTERLEAVED)" {
  style.stroke: "#7c3aed"
}
Server -> Client: "Stream 1: DATA (CSS payload chunk 2 - END_STREAM)" {
  style.stroke: "#2563eb"
}
Note over Client: Zero Head-of-Line Blocking at Application Layer!
""",

        # 6. SMTP Architecture
        "fig5_06_smtp_mail_architecture.svg": """
direction: right

sender: "Alice (MUA)\\nEmail Client" {
  style.fill: "#eff6ff"
}

msa: "Sender MSA / MTA\\n(Port 587 STARTTLS)\\nsmtp.example.com" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
}

mx: "Receiver MX / MTA\\n(Port 25 Relay)\\nmx.recipient.com" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

mda: "Receiver MDA & Spool\\nMaildir / Dovecot" {
  style.fill: "#ecfdf5"
}

receiver: "Bob (MUA)\\n(POP3 / IMAP4)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

sender -> msa: "1. Submission (Port 587)"
msa -> mx: "2. Internet Relay (Port 25)" {
  style.bold: true
}
mx -> mda: "3. Local Delivery"
mda -> receiver: "4. Mail Retrieval (Port 993/995)"
""",

        # 7. SMTP 3-Phase Dialogue
        "fig5_07_smtp_transaction.svg": """
shape: sequence_diagram

Client: "Client MTA"
Server: "Server MTA (Port 25)"

Server -> Client: "220 mail.example.com ESMTP Postfix"
Client -> Server: "EHLO client.org"
Server -> Client: "250-mail.example.com Hello\\n250-SIZE 20480000\\n250 OK"
Client -> Server: "MAIL FROM:<alice@client.org>"
Server -> Client: "250 2.1.0 Ok"
Client -> Server: "RCPT TO:<bob@example.com>"
Server -> Client: "250 2.1.5 Ok"
Client -> Server: "DATA"
Server -> Client: "354 End data with <CR><LF>.<CR><LF>"
Client -> Server: "Subject: Exam Prep Guide\\n\\nHello Bob, here is the solution manual.\\n."
Server -> Client: "250 2.0.0 Ok: queued as 4FA908"
Client -> Server: "QUIT"
Server -> Client: "221 2.0.0 Bye"
""",

        # 8. Email Security (SPF, DKIM, DMARC)
        "fig5_08_email_security.svg": """
direction: right

spf: "1. SPF (Sender Policy Framework)\\nDNS TXT Record listing authorized\\nsending IP addresses for domain" {
  style.fill: "#e0e7ff"
  style.stroke: "#4338ca"
}

dkim: "2. DKIM (DomainKeys Identified Mail)\\nCryptographic public/private key signature\\nverifying message body integrity" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

dmarc: "3. DMARC (Auth & Reporting Policy)\\nEnforces alignment of SPF & DKIM\\nSpecifies reject / quarantine actions" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

spf -> dkim -> dmarc
""",

        # 9. FTP Dual-Connection Architecture
        "fig5_09_ftp_architecture.svg": """
direction: right

client: "FTP Client Host\\nUser Interface & Disk" {
  style.fill: "#eff6ff"
}

server: "FTP Server Host\\nFilesystem Repository" {
  style.fill: "#ecfdf5"
}

client -> server: "Control Connection (TCP Port 21)\\nPersistent: Commands (USER, PASS, LIST, RETR)" {
  style.stroke: "#2563eb"
  style.bold: true
}

client -> server: "Data Connection (TCP Port 20 / Ephemeral)\\nTemporary: Byte Streams per File Transfer" {
  style.stroke: "#16a34a"
  style.stroke-dash: 4
}
""",

        # 10. FTP Active Mode
        "fig5_10_ftp_active_mode.svg": """
shape: sequence_diagram

Client: "FTP Client (Port 51234)"
Server: "FTP Server (Port 21 / 20)"

Client -> Server: "1. Control: PORT 192,168,1,10,200,10 (Client opens :51210)" {
  style.stroke: "#2563eb"
}
Server -> Client: "2. Control: 200 Command okay" {
  style.stroke: "#2563eb"
}
Client -> Server: "3. Control: RETR syllabus.pdf" {
  style.stroke: "#2563eb"
}
Note over Server: Server INITIATES inbound data connection from :20 to :51210!
Server -> Client: "4. Data: TCP SYN from Server :20 to Client :51210" {
  style.stroke: "#dc2626"
  style.bold: true
}
Note over Client: BLOCKED! Client-side NAT/Firewall drops unsolicited inbound SYN!
""",

        # 11. FTP Passive Mode
        "fig5_11_ftp_passive_mode.svg": """
shape: sequence_diagram

Client: "FTP Client (Behind NAT)"
Server: "FTP Server (Public IP)"

Client -> Server: "1. Control: PASV" {
  style.stroke: "#2563eb"
}
Server -> Client: "2. Control: 227 Entering Passive Mode (203,0,113,80,195,80) [Port 50000]" {
  style.stroke: "#16a34a"
}
Client -> Server: "3. Control: RETR syllabus.pdf" {
  style.stroke: "#2563eb"
}
Note over Client: Client INITIATES outbound connection to Server :50000!
Client -> Server: "4. Data: TCP SYN to Server :50000" {
  style.stroke: "#16a34a"
  style.bold: true
}
Server -> Client: "5. Data: 200 OK + File Bytes streamed" {
  style.stroke: "#16a34a"
}
Note over Client,Server: Firewall Friendly: Both connections initiated outbound by client!
""",

        # 13. DNS Resolution Trace
        "fig5_13_dns_resolution_trace.svg": """
shape: sequence_diagram

Client: "Client Stub"
Resolver: "Local DNS Resolver"
Root: "Root Server (.)"
TLD: "TLD Server (.com)"
Authoritative: "Authoritative NS"

Client -> Resolver: "1. Recursive: Query www.example.com" {
  style.stroke: "#2563eb"
}
Resolver -> Root: "2. Iterative: Query www.example.com"
Root -> Resolver: "3. Refer to .com TLD Servers"
Resolver -> TLD: "4. Iterative: Query www.example.com"
TLD -> Resolver: "5. Refer to ns1.example.com"
Resolver -> Authoritative: "6. Iterative: Query www.example.com"
Authoritative -> Resolver: "7. Return A Record: 93.184.216.34 (TTL: 3600)" {
  style.stroke: "#16a34a"
}
Resolver -> Client: "8. Return Resolved IP to Client" {
  style.stroke: "#2563eb"
}
""",

        # 14. Mail Access vs Mail Transfer
        "fig5_14_mail_access_vs_transfer.svg": """
direction: right

smtp: "SMTP (Push Protocol)\\nTransfers mail from client to server,\\nand relays between intermediate servers\\nPort 25 / 587" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

retrieval: "POP3 / IMAP4 (Pull Protocols)\\nRetrieves mail from permanent mailbox spool\\nto personal user computer\\nPort 110/995 (POP3), Port 143/993 (IMAP)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}

smtp -> retrieval: "Mailbox Spool Liaison"
""",

        # 16. POP3 Session Transcript
        "fig5_16_pop3_session.svg": """
shape: sequence_diagram

Client: "Mail Client (MUA)"
Server: "POP3 Server (Port 110)"

Server -> Client: "+OK POP3 server ready"
Client -> Server: "USER alice"
Server -> Client: "+OK User accepted"
Client -> Server: "PASS secretpassword"
Server -> Client: "+OK 2 messages (3200 octets)"
Client -> Server: "STAT"
Server -> Client: "+OK 2 3200"
Client -> Server: "RETR 1"
Server -> Client: "+OK 1200 octets\\n[Message Content Stream]\\n."
Client -> Server: "DELE 1"
Server -> Client: "+OK Message 1 marked for deletion"
Client -> Server: "QUIT"
Server -> Client: "+OK POP3 server signing off (Message 1 unlinked)"
""",

        # 17. TELNET NVT Abstraction
        "fig5_17_telnet_nvt.svg": """
direction: right

local_term: "Local Terminal\\nCustom OS Keycodes" {
  style.fill: "#f8fafc"
}

nvt: "Network Virtual Terminal (NVT)\\nStandard 7-bit ASCII & CR-LF" {
  style.fill: "#dbeafe"
  style.stroke: "#1d4ed8"
  style.bold: true
}

remote_srv: "Remote Server Shell\\nTranslates NVT to Unix TTY" {
  style.fill: "#ecfdf5"
}

local_term -> nvt: "Local Mapping"
nvt -> remote_srv: "TCP Stream (Port 23)"
""",

        # 18. TELNET Option Negotiation
        "fig5_18_telnet_negotiation.svg": """
direction: right

will: "WILL: Sender offers to enable option" {
  style.fill: "#dcfce7"
}

do: "DO: Sender requests receiver to enable option" {
  style.fill: "#dbeafe"
}

wont: "WONT: Sender refuses / disables option" {
  style.fill: "#fee2e2"
}

dont: "DONT: Sender demands receiver disable option" {
  style.fill: "#fef3c7"
}

will -> do
wont -> dont
""",

        # 19. TELNET Insecurity
        "fig5_19_telnet_vulnerabilities.svg": """
direction: right

user: "User Logging in via Telnet\\nTyping: user 'admin' pass 'secret'" {
  style.fill: "#fee2e2"
}

sniffer: "Packet Sniffer (Wireshark / Ettercap)\\nReads cleartext credentials in plain ASCII" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
  style.bold: true
}

server: "Remote Server (:23)" {
  style.fill: "#f8fafc"
}

user -> server: "Plaintext TCP Packets"
sniffer -> user: "Eavesdrops Credentials!"
""",

        # 20. SSH Layered Architecture
        "fig5_20_ssh_architecture.svg": """
direction: down

app_layer: "SSH Connection Layer (RFC 4254)\\nMultiplexes multiple logical channels: Interactive Shells, SFTP, Port Forwarding" {
  style.fill: "#eff6ff"
  style.stroke: "#2563eb"
}

auth_layer: "SSH User Authentication Layer (RFC 4252)\\nAuthenticates client to server: Public Key (Ed25519/RSA), Passwords, Hostbased" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

trans_layer: "SSH Transport Layer (RFC 4251 / 4253)\\nConfidentiality (AES-GCM/ChaCha20), Integrity (HMAC/AEAD), Diffie-Hellman Key Exchange" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}

tcp_layer: "TCP Layer (Port 22)" {
  style.fill: "#f1f5f9"
}

app_layer -> auth_layer -> trans_layer -> tcp_layer
""",

        # 21. SSH Diffie-Hellman Handshake
        "fig5_21_ssh_handshake.svg": """
shape: sequence_diagram

Client: "SSH Client"
Server: "SSH Server (Port 22)"

Client -> Server: "1. TCP 3-Way Handshake"
Client -> Server: "2. SSH-2.0-OpenSSH_9.0 (Version Exchange)"
Server -> Client: "3. SSH-2.0-OpenSSH_8.9 (Version Exchange)"
Client -> Server: "4. SSH_MSG_KEXINIT (Cipher Suite & Algorithm Proposal)"
Server -> Client: "5. SSH_MSG_KEXINIT (Selected: curve25519-sha256, aes256-gcm)"
Client -> Server: "6. SSH_MSG_KEX_ECDH_INIT (Client Public Key e = g^x mod p)" {
  style.stroke: "#2563eb"
}
Server -> Client: "7. SSH_MSG_KEX_ECDH_REPLY (Server Key f = g^y mod p, Host Key K_S, Signature)" {
  style.stroke: "#16a34a"
}
Note over Client,Server: Both derive identical Shared Secret K = g^(xy) mod p!\\nAll subsequent traffic encrypted with symmetric keys!
Client -> Server: "8. SSH_MSG_NEWKEYS"
Server -> Client: "9. SSH_MSG_NEWKEYS"
""",

        # 22. SSH Port Forwarding
        "fig5_22_ssh_port_forwarding.svg": """
direction: right

local_fw: "Local Port Forwarding (-L 8080:db.internal:3306)\\nLocal App (:8080) -> SSH Client ===> SSH Gateway -> DB (:3306)" {
  style.fill: "#dbeafe"
  style.stroke: "#2563eb"
}

remote_fw: "Remote Port Forwarding (-R 9000:localhost:80)\\nExternal User -> Cloud Host (:9000) ===> SSH Client -> Local Web (:80)" {
  style.fill: "#fef3c7"
  style.stroke: "#d97706"
}

dynamic_fw: "Dynamic SOCKS5 Proxy (-D 1080)\\nBrowser SOCKS5 (:1080) ===> SSH Server -> Target Web Destinations" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
}
""",

        # 23. HTTP vs HTTPS Stack
        "fig5_23_http_vs_https_stack.svg": """
direction: right

http_stack: "Plaintext HTTP Stack (Port 80)\\n[Application: HTTP]\\n[Transport: TCP]\\n[Network: IP]\\n(Cleartext: Subject to eavesdropping & tampering)" {
  style.fill: "#fee2e2"
  style.stroke: "#dc2626"
}

https_stack: "Secure HTTPS Stack (Port 443)\\n[Application: HTTP]\\n[Security: TLS 1.3 Sublayer]\\n[Transport: TCP]\\n[Network: IP]\\n(End-to-End Encrypted: AES-GCM / ChaCha20)" {
  style.fill: "#dcfce7"
  style.stroke: "#16a34a"
  style.bold: true
}
""",

        # 24. TLS 1.3 Handshake
        "fig5_24_tls_handshake.svg": """
shape: sequence_diagram

Client: "Web Browser"
Server: "HTTPS Server"

Client -> Server: "1. ClientHello (Supported Ciphers, Client Key Share g^x)" {
  style.stroke: "#2563eb"
}
Server -> Client: "2. ServerHello (Selected Cipher, Server Key Share g^y)\\n{EncryptedExtensions}\\n{Certificate: X.509 CA Chain}\\n{CertVerify: Signature}\\n{Finished: HMAC}" {
  style.stroke: "#16a34a"
}
Note over Client: Client verifies X.509 Certificate against Root CAs;\\nCalculates symmetric Master Secret in 1 RTT!
Client -> Server: "3. {Finished}\\nHTTP GET /index.html (Encrypted Application Data)" {
  style.stroke: "#2563eb"
}
Server -> Client: "4. HTTP 200 OK (Encrypted Application Data)" {
  style.stroke: "#16a34a"
}
"""
    }

    for filename, code in d2_diagrams.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        svg_engine.compile_d2(code, out_path, theme=1)
    print(f"  Generated {len(d2_diagrams)} D2 publication diagrams.")

generate_d2_diagrams()
print("\nUnit 5 figure generation complete!")
