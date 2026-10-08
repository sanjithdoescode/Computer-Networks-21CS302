const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { marked } = require("marked");
const katex = require("katex");
const puppeteer = require("puppeteer-core");

const projectRoot = path.resolve(__dirname, "..");
const diagramsDir = path.resolve(__dirname, "diagrams");
const stylesDir = path.resolve(__dirname, "styles");
const manifestPath = path.join(diagramsDir, "manifest.json");

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));

// Read CSS files
const textbookCss = fs.readFileSync(path.join(stylesDir, "textbook.css"), "utf8");
const katexCss = fs.readFileSync(path.resolve(__dirname, "node_modules/katex/dist/katex.min.css"), "utf8");

// Configure marked
marked.setOptions({
  gfm: true,
  breaks: false
});

/**
 * Process math expressions with KaTeX safely using token placeholders
 */
function processMathAndMarkdown(mdContent, unitNum, figCounterState) {
  const mathTokens = [];
  const figTokens = [];
  
  // 1. Extract Display Math: $$ ... $$
  let processed = mdContent.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
    const token = `@@@MATH_DISPLAY_${mathTokens.length}@@@`;
    mathTokens.push({ token, formula: formula.trim(), display: true });
    return `\n\n${token}\n\n`;
  });

  // 2. Extract Inline Math: $ ... $ (avoid escaped \$ or empty $$)
  processed = processed.replace(/(?<!\$)\$([^\$\n]+?)\$(?!\$)/g, (match, formula) => {
    const token = `@@@MATH_INLINE_${mathTokens.length}@@@`;
    mathTokens.push({ token, formula: formula.trim(), display: false });
    return token;
  });

  // 3. Extract Vector SVG Figures into tokens
  processed = processed.replace(/!\[(.*?)\]\((?:figures\/)?([^)]+\.svg)\)/g, (match, caption, filename) => {
    figCounterState.count++;
    const figNum = figCounterState.count;
    const token = `@@@FIGURE_TOKEN_${figTokens.length}@@@`;
    const svgPath = path.join(projectRoot, `UNIT - ${unitNum}`, "figures", filename);
    let htmlContent = "";
    if (fs.existsSync(svgPath)) {
      let svg = fs.readFileSync(svgPath, "utf8");
      svg = svg.replace(/<\?xml[\s\S]*?\?>/i, "");
      svg = svg.replace(/<!DOCTYPE[\s\S]*?>/i, "");
      
      let formattedCaption = caption;
      const figPrefixMatch = caption.match(/^(Figure\s+\d+\.\d+:?)\s*(.*)$/i);
      if (figPrefixMatch) {
        formattedCaption = `<strong>${figPrefixMatch[1]}</strong> ${figPrefixMatch[2]}`;
      } else {
        formattedCaption = `<strong>Figure ${unitNum}.${figNum}:</strong> ${caption}`;
      }
      htmlContent = `\n\n<figure class="diagram-card">\n<div class="svg-container">\n${svg}\n</div>\n<figcaption>${formattedCaption}</figcaption>\n</figure>\n\n`;
    } else {
      console.warn(`Warning: SVG not found at ${svgPath}`);
      htmlContent = `\n\n<div class="callout callout-warning">Figure not found: ${filename}</div>\n\n`;
    }
    figTokens.push({ token, html: htmlContent });
    return `\n\n${token}\n\n`;
  });

  // Fallback: Process any remaining Mermaid Diagrams (if any)
  processed = processed.replace(/```mermaid\n([\s\S]*?)```/g, (match, code) => {
    const trimmed = code.trim();
    const hash = crypto.createHash("md5").update(trimmed).digest("hex");
    const info = manifest[hash];
    
    figCounterState.count++;
    const figNum = figCounterState.count;
    const token = `@@@FIGURE_TOKEN_${figTokens.length}@@@`;
    let caption = `Architectural flow and protocol state dynamics`;

    const titleMatch = trimmed.match(/subgraph\s+[A-Za-z0-9_]+\["([^"]+)"\]/) ||
                       trimmed.match(/title\s+([^\n]+)/) ||
                       trimmed.match(/accTitle:\s*([^\n]+)/);
    if (titleMatch) {
      caption = titleMatch[1];
    } else {
      const firstNodeMatch = trimmed.match(/\["([^"]{5,60})"/);
      if (firstNodeMatch) {
        caption = firstNodeMatch[1];
      }
    }

    let htmlContent = "";
    if (info && fs.existsSync(path.join(diagramsDir, info.svgPath))) {
      let svg = fs.readFileSync(path.join(diagramsDir, info.svgPath), "utf8");
      svg = svg.replace(/<\?xml[\s\S]*?\?>/i, "");
      svg = svg.replace(/<!DOCTYPE[\s\S]*?>/i, "");
      htmlContent = `\n\n<figure class="diagram-card">\n<div class="svg-container">\n${svg}\n</div>\n<figcaption><strong>Figure ${unitNum}.${figNum}:</strong> ${caption}</figcaption>\n</figure>\n\n`;
    } else {
      htmlContent = `\n\n<div class="callout callout-warning">Diagram ${unitNum}.${figNum} (Rendering placeholder)</div>\n\n`;
    }
    figTokens.push({ token, html: htmlContent });
    return `\n\n${token}\n\n`;
  });

  // 4. Process GitHub-style Alert Callouts
  processed = processed.replace(/^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:>.*(?:\n|$))*)/gim, (match, type, content) => {
    const cleanContent = content.replace(/^>\s?/gm, "").trim();
    const lowerType = type.toLowerCase();
    let alertClass = "callout-note";
    let alertTitle = "📌 Key Concept";
    if (lowerType === "tip") {
      alertClass = "callout-tip";
      alertTitle = "💡 Exam Tip";
    } else if (lowerType === "important") {
      alertClass = "callout-tip";
      alertTitle = "⭐ Important Core Principle";
    } else if (lowerType === "warning" || lowerType === "caution") {
      alertClass = "callout-warning";
      alertTitle = "⚠️ Common Trap & Pitfall";
    }
    return `\n\n<div class="callout ${alertClass}">\n<div class="callout-title">${alertTitle}</div>\n${marked.parse(cleanContent)}\n</div>\n\n`;
  });

  // 5. Render Markdown to HTML
  let html = marked.parse(processed);

  // 6. Restore Math via KaTeX
  for (const item of mathTokens) {
    try {
      const rendered = katex.renderToString(item.formula, {
        displayMode: item.display,
        throwOnError: false
      });
      html = html.replace(item.token, rendered);
    } catch (err) {
      html = html.replace(item.token, `<code>${item.formula}</code>`);
    }
  }

  // 6.5. Restore Figures safely
  for (const item of figTokens) {
    html = html.replace(new RegExp(`<p>\\s*${item.token}\\s*<\\/p>`, 'g'), item.html);
    html = html.replace(new RegExp(item.token, 'g'), item.html);
  }

  // 7. Enhance ASCII packet layouts
  html = html.replace(/<pre><code>([\s\S]*?)<\/code><\/pre>/g, (match, code) => {
    if (
      code.includes("+-+-+-+-+-+-+-+-+") ||
      code.includes("0                   1                   2                   3") ||
      code.includes("| Version |  IHL  |") ||
      code.includes("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+") ||
      code.includes("| Source Port") ||
      code.includes("| Destination Port")
    ) {
      return `<pre class="ascii-packet"><code>${code}</code></pre>`;
    }
    return match;
  });

  // 8. Style Question Headers with Badges
  html = html.replace(/<h1>Question (\d+):?\s*([^<]+)<\/h1>/gi, (match, qNum, qTitle) => {
    return `<div class="question-container"><div class="question-badge">16-MARK MASTER GUIDE</div><h1 id="unit${unitNum}-q${qNum}">Question ${qNum}: ${qTitle.trim()}</h1></div>`;
  });

  // Also catch "## Question X"
  html = html.replace(/<h2>Question (\d+):?\s*([^<]+)<\/h2>/gi, (match, qNum, qTitle) => {
    return `<div class="question-container"><div class="question-badge">16-MARK MASTER GUIDE</div><h2 id="unit${unitNum}-q${qNum}">Question ${qNum}: ${qTitle.trim()}</h2></div>`;
  });

  return html;
}

/**
 * Process Unit 1 short questions specifically
 */
function processShortQuestions(mdContent) {
  const mathTokens = [];
  
  let processed = mdContent.replace(/\$\$([\s\S]*?)\$\$/g, (match, formula) => {
    const token = `@@@MATH_DISPLAY_${mathTokens.length}@@@`;
    mathTokens.push({ token, formula: formula.trim(), display: true });
    return `\n\n${token}\n\n`;
  });

  processed = processed.replace(/(?<!\$)\$([^\$\n]+?)\$(?!\$)/g, (match, formula) => {
    const token = `@@@MATH_INLINE_${mathTokens.length}@@@`;
    mathTokens.push({ token, formula: formula.trim(), display: false });
    return token;
  });

  const figTokens = [];
  let shortFigCount = 0;
  processed = processed.replace(/!\[(.*?)\]\((?:figures\/)?([^)]+\.svg)\)/g, (match, caption, filename) => {
    shortFigCount++;
    const token = `@@@SHORT_FIG_${figTokens.length}@@@`;
    const svgPath = path.join(projectRoot, "UNIT - 1", "figures", filename);
    let htmlContent = "";
    if (fs.existsSync(svgPath)) {
      let svg = fs.readFileSync(svgPath, "utf8");
      svg = svg.replace(/<\?xml[\s\S]*?\?>/i, "");
      svg = svg.replace(/<!DOCTYPE[\s\S]*?>/i, "");
      let formattedCaption = caption;
      const figPrefixMatch = caption.match(/^(Figure\s+1\.S\d+:?)\s*(.*)$/i);
      if (figPrefixMatch) {
        formattedCaption = `<strong>${figPrefixMatch[1]}</strong> ${figPrefixMatch[2]}`;
      } else {
        formattedCaption = `<strong>Figure 1.S${shortFigCount}:</strong> ${caption}`;
      }
      htmlContent = `\n\n<figure class="diagram-card">\n<div class="svg-container">\n${svg}\n</div>\n<figcaption>${formattedCaption}</figcaption>\n</figure>\n\n`;
    }
    figTokens.push({ token, html: htmlContent });
    return `\n\n${token}\n\n`;
  });

  // Fallback Mermaid
  processed = processed.replace(/```mermaid\n([\s\S]*?)```/g, (match, code) => {
    const trimmed = code.trim();
    const hash = crypto.createHash("md5").update(trimmed).digest("hex");
    const info = manifest[hash];
    shortFigCount++;
    const token = `@@@SHORT_FIG_${figTokens.length}@@@`;

    let htmlContent = "";
    if (info && fs.existsSync(path.join(diagramsDir, info.svgPath))) {
      let svg = fs.readFileSync(path.join(diagramsDir, info.svgPath), "utf8");
      svg = svg.replace(/<\?xml[\s\S]*?\?>/i, "");
      svg = svg.replace(/<!DOCTYPE[\s\S]*?>/i, "");
      htmlContent = `\n\n<figure class="diagram-card">\n<div class="svg-container">\n${svg}\n</div>\n<figcaption><strong>Figure 1.S${shortFigCount}:</strong> Short Answer Concept Diagram</figcaption>\n</figure>\n\n`;
    }
    figTokens.push({ token, html: htmlContent });
    return `\n\n${token}\n\n`;
  });

  let html = marked.parse(processed);

  for (const item of mathTokens) {
    try {
      const rendered = katex.renderToString(item.formula, {
        displayMode: item.display,
        throwOnError: false
      });
      html = html.replace(item.token, rendered);
    } catch (err) {
      html = html.replace(item.token, `<code>${item.formula}</code>`);
    }
  }

  // Restore Figures safely
  for (const item of figTokens) {
    html = html.replace(new RegExp(`<p>\\s*${item.token}\\s*<\\/p>`, 'g'), item.html);
    html = html.replace(new RegExp(item.token, 'g'), item.html);
  }

  // Add short question badge to H2 headings
  html = html.replace(/<h2>(\d+)\.\s*([^<]+)<\/h2>/gi, (match, qNum, qTitle) => {
    return `<div class="question-container" style="page-break-before: auto;"><div class="question-badge short">2/5-MARK SHORT QUESTION</div><h2 id="unit1-sq${qNum}">${qNum}. ${qTitle.trim()}</h2></div>`;
  });

  return html;
}

async function buildMasterBook() {
  console.log("Assembling Master Computer Networks Textbook...");

  // Load markdown files
  const u1ShortMd = fs.readFileSync(path.join(projectRoot, "UNIT - 1/short_questions_answers.md"), "utf8");
  const u1LongMd = fs.readFileSync(path.join(projectRoot, "UNIT - 1/long_questions_answers.md"), "utf8");
  const u2LongMd = fs.readFileSync(path.join(projectRoot, "UNIT - 2/long_questions_answers.md"), "utf8");
  const u3LongMd = fs.readFileSync(path.join(projectRoot, "UNIT - 3/long_questions_answers.md"), "utf8");
  const u4LongMd = fs.readFileSync(path.join(projectRoot, "UNIT - 4/long_questions_answers.md"), "utf8");
  const u5LongMd = fs.readFileSync(path.join(projectRoot, "UNIT - 5/long_questions_answers.md"), "utf8");

  // Track figures per unit
  const figStateU1 = { count: 0 };
  const figStateU2 = { count: 0 };
  const figStateU3 = { count: 0 };
  const figStateU4 = { count: 0 };
  const figStateU5 = { count: 0 };

  console.log("Compiling Unit 1...");
  const u1ShortHtml = processShortQuestions(u1ShortMd);
  const u1LongHtml = processMathAndMarkdown(u1LongMd, 1, figStateU1);

  console.log("Compiling Unit 2...");
  const u2LongHtml = processMathAndMarkdown(u2LongMd, 2, figStateU2);

  console.log("Compiling Unit 3...");
  const u3LongHtml = processMathAndMarkdown(u3LongMd, 3, figStateU3);

  console.log("Compiling Unit 4...");
  const u4LongHtml = processMathAndMarkdown(u4LongMd, 4, figStateU4);

  console.log("Compiling Unit 5...");
  const u5LongHtml = processMathAndMarkdown(u5LongMd, 5, figStateU5);

  // Compile Front Matter and Appendices
  const frontMatterHtml = `
    <!-- COVER PAGE -->
    <div class="cover-page">
      <div class="cover-header">
        <div class="cover-course-code">21CS302 &bull; Computer Networks</div>
        <div class="cover-badge">Autonomous / Anna University Curriculum</div>
      </div>
      
      <div class="cover-main">
        <h1 class="cover-title">COMPUTER NETWORKS<span>THE MASTER EXAM TEXTBOOK</span></h1>
        <p class="cover-subtitle">Complete Question Bank, Architectural Blueprints & Exhaustive 16-Mark Solution Manual</p>
        <div class="cover-divider"></div>
        <p class="cover-desc">
          An exhaustive, mathematically rigorous, bit-level textbook engineered for university semester-end and internal assessment examinations. Features 163+ publication-grade vector architectural diagrams, bit-level packet layouts, and complete multi-parameter comparison matrices across all five curriculum units.
        </p>
        <div class="cover-standards">
          <div class="cover-standards-title">Authoritative Reference Textbooks</div>
          <p class="cover-standards-text">
            Behrouz A. Forouzan (5th Ed.) &bull; William Stallings (10th Ed.) &bull; Andrew S. Tanenbaum (5th Ed.) &bull; Larry L. Peterson &amp; Bruce S. Davie (6th Ed.) &bull; James F. Kurose &amp; Keith W. Ross (8th Ed.)
          </p>
        </div>
      </div>

      <div class="cover-footer">
        <div>
          <div class="cover-author-title">Curated &amp; Authored By</div>
          <div class="cover-author-name">Sanjith (@sanjithdoescode)</div>
        </div>
        <div class="cover-repo">
          Public Repository &bull; Open-Source Academic Portal<br>
          <a href="https://github.com/sanjithdoescode/Computer-Networks-21CS302.git">github.com/sanjithdoescode/Computer-Networks-21CS302</a>
        </div>
      </div>
    </div>

    <!-- ACADEMIC METADATA & COPYRIGHT -->
    <div class="front-matter">
      <h1>Academic Identity &amp; Repository Credits</h1>
      <table style="margin-top: 20px;">
        <tr><th style="width: 30%;">Course Code &amp; Title</th><td><strong>21CS302 / COMPUTER NETWORKS</strong></td></tr>
        <tr><th>Curriculum Regulation</th><td>Anna University Regulations 2021 / Autonomous Engineering Institutions</td></tr>
        <tr><th>Target Department</th><td>Department of Computer Science and Engineering (Professional Core)</td></tr>
        <tr><th>Instructional Credit</th><td>4 Credits (3 Lecture, 0 Tutorial, 2 Practical — 75 Total Contact Hours)</td></tr>
        <tr><th>Lead Curator / Author</th><td><strong>Sanjith</strong> (<a href="https://github.com/sanjithdoescode">@sanjithdoescode</a>)</td></tr>
        <tr><th>Official Public Repository</th><td><a href="https://github.com/sanjithdoescode/Computer-Networks-21CS302.git">https://github.com/sanjithdoescode/Computer-Networks-21CS302.git</a></td></tr>
        <tr><th>Academic License</th><td>MIT Open-Source Academic License (Free for study, reference, and educational citation)</td></tr>
        <tr><th>Edition &amp; Year</th><td>Master Examination Edition — 2026</td></tr>
      </table>

      <div class="callout callout-tip" style="margin-top: 25px;">
        <div class="callout-title">📖 Repository Mission</div>
        This volume eliminates the need for consulting multiple disparate textbooks or unverified internet websites during examination preparation. Every solution is written to the rigorous 16-mark university standard, guaranteeing complete coverage of historical context, mathematical proofs, state machines, and RFC-standard bit-level packet headers.
      </div>

      <hr>

      <h1>Preface &amp; The 16-Mark University Exam Scoring Blueprint</h1>
      <p>
        University evaluators in autonomous institutions and Anna University central valuation boards evaluate hundreds of answer scripts. To secure the maximum possible score (<strong>15/16 or 16/16</strong>) in essay questions, an engineering student's answer must never consist of superficial bullet points or brief summaries. Evaluators expect <strong>4 to 5 handwritten exam pages per question</strong> structured across seven mandatory pillars:
      </p>

      <table style="margin-top: 15px;">
        <thead>
          <tr>
            <th>Pillar</th>
            <th>Component</th>
            <th>Target Mark Allocation</th>
            <th>Evaluator Expectation</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1</strong></td>
            <td>Foundational Introduction &amp; RFC Standards</td>
            <td>2 Marks</td>
            <td>Explicit citation of governing RFC/IEEE standards, design motivations, and protocol bottlenecks.</td>
          </tr>
          <tr>
            <td><strong>2</strong></td>
            <td>Architectural &amp; Flow Visualizations</td>
            <td>4 Marks</td>
            <td>Clean topological flowcharts, sequence message handshakes, and state transition lifecycles.</td>
          </tr>
          <tr>
            <td><strong>3</strong></td>
            <td>32-Bit Frame &amp; Packet Header Formats</td>
            <td>3 Marks</td>
            <td>Complete ASCII diagrams with bit boundaries (0–31) and field-by-field functional breakdowns.</td>
          </tr>
          <tr>
            <td><strong>4</strong></td>
            <td>Mathematical Formulations &amp; Solved Traces</td>
            <td>3 Marks</td>
            <td>Formal LaTeX equations, dimensional units, and worked numerical walkthroughs with intermediate steps.</td>
          </tr>
          <tr>
            <td><strong>5</strong></td>
            <td>Algorithmic State Machines &amp; Workflows</td>
            <td>2 Marks</td>
            <td>Step-by-step procedural transitions (e.g. TCP 3-way handshake, DHCP DORA exchange, CSMA/CA NAV backoff).</td>
          </tr>
          <tr>
            <td><strong>6</strong></td>
            <td>Multi-Parameter Comparison Matrices</td>
            <td>1 Mark</td>
            <td>Comprehensive 8 to 15-parameter comparative matrices evaluating competing protocols.</td>
          </tr>
          <tr>
            <td><strong>7</strong></td>
            <td>Failure Modes, Edge Cases &amp; Mitigations</td>
            <td>1 Mark</td>
            <td>Critical vulnerabilities, race conditions (e.g. SYN floods, Count-to-Infinity), and real-world defenses.</td>
          </tr>
        </tbody>
      </table>

      <hr>

      <h1>Official Syllabus Specification (21CS302)</h1>
      <p><strong>Course Outcomes (COs):</strong> Upon successful completion of this course, students will be able to:</p>
      <ul>
        <li><strong>CO1 (K3 - Apply):</strong> Make use of evaluation metrics to measure the performance of packet-switched networks.</li>
        <li><strong>CO2 (K3 - Apply):</strong> Utilize the Link layer services for various IEEE standards.</li>
        <li><strong>CO3 (K3 - Apply):</strong> Experiment with subnetting to optimize network configuration and various routing algorithms for unicast routing.</li>
        <li><strong>CO4 (K3 - Apply):</strong> Choose protocols for Process-to-Process communication in various applications.</li>
        <li><strong>CO5 (K3 - Apply):</strong> Utilize application layer protocols for real-time scenarios.</li>
      </ul>
    </div>

    <!-- MASTER TABLE OF CONTENTS -->
    <div class="toc-container">
      <h1 class="toc-title">Master Table of Contents</h1>

      <div class="toc-unit-title">UNIT I: INTRODUCTION AND PHYSICAL LAYER (CO1)</div>
      <div style="font-weight: 700; color: #0f766e; margin-top: 6px; font-size: 9.5pt;">Part A: 2-Mark &amp; 5-Mark Short Questions &amp; Answers</div>
      <div class="toc-item"><a href="#unit1-sq1">1. Define Networks</a> <span>Core criteria &amp; 5 components</span></div>
      <div class="toc-item"><a href="#unit1-sq2">2. Types of Networks (PAN, LAN, MAN, WAN)</a> <span>Geographic spans &amp; data rates</span></div>
      <div class="toc-item"><a href="#unit1-sq3">3. Types of Layers (OSI vs. TCP/IP)</a> <span>Layer abstractions &amp; PDU mapping</span></div>
      <div class="toc-item"><a href="#unit1-sq4">4. Summarize Transmission Media</a> <span>Guided cables &amp; wireless propagation</span></div>
      <div class="toc-item"><a href="#unit1-sq5">5. Define Jitter and Throughput</a> <span>Delay variation &amp; channel metrics</span></div>
      <div class="toc-item"><a href="#unit1-sq6">6. Difference between TCP &amp; UDP</a> <span>Reliable stream vs. datagram</span></div>
      <div class="toc-item"><a href="#unit1-sq7">7. Circuit Switching vs. Packet Switching</a> <span>Dedicated circuits vs. store-and-forward</span></div>
      <div class="toc-item"><a href="#unit1-sq8">8. Contrast between Switch and Router</a> <span>Layer 2 MAC vs. Layer 3 IP routing</span></div>
      <div class="toc-item"><a href="#unit1-sq9">9. Network Topologies</a> <span>Mesh, Star, Bus, Ring, Tree comparison</span></div>
      <div class="toc-item"><a href="#unit1-sq10">10. Define Data Communication</a> <span>Simplex, Half-Duplex, Full-Duplex flow</span></div>
      <div class="toc-item"><a href="#unit1-sq11">11. Line Configuration</a> <span>Point-to-Point vs. Multipoint channels</span></div>
      
      <div style="font-weight: 700; color: #1e3a8a; margin-top: 12px; font-size: 9.5pt;">Part B: 16-Mark Long Essay Master Guides</div>
      <div class="toc-item"><a href="#unit1-q1">Question 1: The OSI 7-Layer Reference Model</a> <span>Exhaustive architecture of all 7 layers</span></div>
      <div class="toc-item"><a href="#unit1-q2">Question 2: TCP &amp; UDP Transport Architecture</a> <span>32-bit headers, handshakes &amp; Reno control</span></div>
      <div class="toc-item"><a href="#unit1-q3">Question 3: Switching Techniques in Computer Networks</a> <span>Space/Time division, pipelining proofs</span></div>
      <div class="toc-item"><a href="#unit1-q4">Question 4: Network Topologies</a> <span>Formulas, token dynamics &amp; hybrid designs</span></div>
      <div class="toc-item"><a href="#unit1-q5">Question 5: Transmission Media</a> <span>Nyquist, Shannon, optical TIR &amp; radio waves</span></div>

      <div class="toc-unit-title">UNIT II: DATA-LINK LAYER &amp; MAC SUBLAYER (CO2)</div>
      <div class="toc-item"><a href="#unit2-q1">Question 1: Duties of the Data Link Layer</a> <span>Framing stuffing, LLC/MAC, 48-bit MAC addressing</span></div>
      <div class="toc-item"><a href="#unit2-q2">Question 2: Unicast, Multicast, Broadcast &amp; Anycast</a> <span>32:1 MAC ambiguity &amp; broadcast storms</span></div>
      <div class="toc-item"><a href="#unit2-q3">Question 3: Address Resolution Protocol (ARP)</a> <span>RFC 826 header, cache aging &amp; Proxy ARP</span></div>
      <div class="toc-item"><a href="#unit2-q4">Question 4: Reverse Address Resolution Protocol (RARP)</a> <span>Diskless booting &amp; BOOTP/DHCP evolution</span></div>
      <div class="toc-item"><a href="#unit2-q5">Question 5: Error Detection and Correction</a> <span>Hamming codes, CRC modulo-2, 1's comp Checksum</span></div>

      <div class="toc-unit-title">UNIT III: NETWORK LAYER &amp; ROUTING ARCHITECTURE (CO3)</div>
      <div class="toc-item"><a href="#unit3-q1">Question 1: Duties of the Network Layer</a> <span>Host-to-host delivery, router crossbar, TCAM</span></div>
      <div class="toc-item"><a href="#unit3-q2">Question 2: Address Classes (Class A–E) &amp; CIDR</a> <span>Leading bits, subnetting, CIDR prefix matching</span></div>
      <div class="toc-item"><a href="#unit3-q3">Question 3: Routing Techniques (DV, LS, STP)</a> <span>Bellman-Ford, Dijkstra SPF &amp; 802.1D bridge loops</span></div>
      <div class="toc-item"><a href="#unit3-q4">Question 4: Carrier Sense Multiple Access / CA (CSMA/CA)</a> <span>Hidden/exposed terminals, IFS, NAV, RTS/CTS</span></div>
      <div class="toc-item"><a href="#unit3-q5">Question 5: Internet Protocol Version 4 (IPv4)</a> <span>32-bit header, MTU fragmentation walkthrough</span></div>
      <div class="toc-item"><a href="#unit3-q6">Question 6: Routing Protocols: OSPF, RIP, and BGP</a> <span>IGP vs. EGP, Dijkstra areas, AS-PATH loop immunity</span></div>
      <div class="toc-item"><a href="#unit3-q7">Question 7: Dynamic Host Configuration Protocol (DHCP)</a> <span>4-step DORA lifecycle, lease timers, Relay Agent</span></div>
      <div class="toc-item"><a href="#unit3-q8">Question 8: Congestion Control Algorithms</a> <span>Leaky Bucket vs. Token Bucket, ECN RFC 3168</span></div>
      <div class="toc-item"><a href="#unit3-q9">Question 9: Network Layer Protocols Overview Suite</a> <span>IPv6 40B header, ICMP diagnostics, IGMP snooping</span></div>

      <div class="toc-unit-title">UNIT IV: TRANSPORT LAYER PROTOCOLS &amp; SERVICES (CO4)</div>
      <div class="toc-item"><a href="#unit4-q1">Question 1: Duties of the Transport Layer</a> <span>Process-to-process delivery, 5-tuples, demuxing</span></div>
      <div class="toc-item"><a href="#unit4-q2">Question 2: User Datagram Protocol (UDP)</a> <span>8-byte header, pseudo-header 1's complement math</span></div>
      <div class="toc-item"><a href="#unit4-q3">Question 3: Transmission Control Protocol (TCP)</a> <span>3-way handshake, 11-state FSM, Tahoe vs. Reno</span></div>
      <div class="toc-item"><a href="#unit4-q4">Question 4: Stream Control Transmission Protocol (SCTP)</a> <span>Multi-homing, multi-streaming, 4-way cookie handshake</span></div>
      <div class="toc-item"><a href="#unit4-q5">Question 5: TCP Services &amp; Core Mechanics</a> <span>Ring buffers, full-duplex, BDP, sliding window eta</span></div>

      <div class="toc-unit-title">UNIT V: APPLICATION LAYER PROTOCOLS &amp; ARCHITECTURES (CO5)</div>
      <div class="toc-item"><a href="#unit5-q1">Question 1: HyperText Transfer Protocol (HTTP)</a> <span>HTTP/1.0, 1.1, 2, HTTP/3 over QUIC, caching, cookies</span></div>
      <div class="toc-item"><a href="#unit5-q2">Question 2: Simple Mail Transfer Protocol (SMTP)</a> <span>MUA/MTA, MIME, Base64 math, SPF/DKIM/DMARC</span></div>
      <div class="toc-item"><a href="#unit5-q3">Question 3: File Transfer Protocol (FTP)</a> <span>Dual-channel (:21/:20), Active vs. Passive PASV</span></div>
      <div class="toc-item"><a href="#unit5-q4">Question 4: Domain Name System (DNS)</a> <span>Hierarchical tree, recursive/iterative, DNSSEC</span></div>
      <div class="toc-item"><a href="#unit5-q5">Question 5: Post Office Protocol Version 3 (POP3)</a> <span>Auth/Transaction/Update states vs. IMAP4</span></div>
      <div class="toc-item"><a href="#unit5-q6">Question 6: TELNET (Teletype Network)</a> <span>Network Virtual Terminal (NVT), IAC byte negotiation</span></div>
      <div class="toc-item"><a href="#unit5-q7">Question 7: Secure Shell (SSH)</a> <span>Diffie-Hellman derivation, public keys, tunneling</span></div>
      <div class="toc-item"><a href="#unit5-q8">Question 8: Difference between HTTP and HTTPS</a> <span>TLS 1.3 handshake, cipher suites, X.509 PKI trust</span></div>

      <div class="toc-unit-title">ACADEMIC APPENDICES &amp; QUICK REFERENCE</div>
      <div class="toc-item"><a href="#appendix-a">Appendix A: Master Networking Acronym Dictionary</a> <span>75+ networking acronyms defined</span></div>
      <div class="toc-item"><a href="#appendix-b">Appendix B: Complete Port Numbers &amp; Protocols Matrix</a> <span>Well-known &amp; registered ports reference</span></div>
      <div class="toc-item"><a href="#appendix-c">Appendix C: Master Exam Formula Sheet</a> <span>Complete LaTeX formula cheat sheet</span></div>
    </div>
  `;

  // Compile Appendices
  const appendixHtml = `
    <div style="page-break-before: always; break-before: page;">
      <h1 class="appendix-title" id="appendix-a">APPENDIX A: MASTER NETWORKING ACRONYM DICTIONARY</h1>
      <p>Comprehensive glossary of 75+ fundamental networking acronyms covering Layers 1 through 7, standard RFC specifications, and architectural functions:</p>
      
      <table style="font-size: 8.5pt;">
        <thead>
          <tr>
            <th style="width: 12%;">Acronym</th>
            <th style="width: 25%;">Full Formal Term</th>
            <th style="width: 10%;">Layer</th>
            <th style="width: 13%;">Standard</th>
            <th>Operational Role &amp; Significance</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>AIMD</strong></td><td>Additive Increase Multiplicative Decrease</td><td>Transport</td><td>RFC 5681</td><td>Congestion control feedback principle used in TCP Reno and Tahoe.</td></tr>
          <tr><td><strong>ALOHA</strong></td><td>Additive Links On-line Hawaii Area</td><td>Data Link</td><td>Norm Abramson</td><td>Foundational random access broadcast protocol; pure and slotted forms.</td></tr>
          <tr><td><strong>AP</strong></td><td>Access Point</td><td>Data Link/Phy</td><td>IEEE 802.11</td><td>Layer 2 wireless central coordinator bridging 802.11 to 802.3 wired Ethernet.</td></tr>
          <tr><td><strong>APIPA</strong></td><td>Automatic Private IP Addressing</td><td>Network</td><td>RFC 3927</td><td>Link-local dynamic address assignment block (169.254.0.0/16).</td></tr>
          <tr><td><strong>ARP</strong></td><td>Address Resolution Protocol</td><td>Data Link/L3</td><td>RFC 826</td><td>Dynamic mapping from a known 32-bit logical IP to a 48-bit physical MAC address.</td></tr>
          <tr><td><strong>ARQ</strong></td><td>Automatic Repeat reQuest</td><td>Data Link/L4</td><td>General</td><td>Error-control feedback mechanism using ACKs, NACKs, timeouts, and retransmissions.</td></tr>
          <tr><td><strong>AS</strong></td><td>Autonomous System</td><td>Network</td><td>RFC 1930</td><td>Collection of connected IP routing prefixes under single administrative control.</td></tr>
          <tr><td><strong>ASBR</strong></td><td>Autonomous System Boundary Router</td><td>Network</td><td>RFC 2328</td><td>OSPF router connecting local AS to external routing domains (e.g. BGP).</td></tr>
          <tr><td><strong>BDP</strong></td><td>Bandwidth-Delay Product</td><td>Transport/Phy</td><td>General</td><td>Link data capacity in bits: Bandwidth (bps) &times; RTT (sec).</td></tr>
          <tr><td><strong>BGP</strong></td><td>Border Gateway Protocol (BGP-4)</td><td>Application/L3</td><td>RFC 4271</td><td>Path-vector inter-domain routing protocol powering the global Internet core.</td></tr>
          <tr><td><strong>BOOTP</strong></td><td>Bootstrap Protocol</td><td>Application</td><td>RFC 951</td><td>UDP-based predecessor to DHCP for booting diskless workstations.</td></tr>
          <tr><td><strong>BPDU</strong></td><td>Bridge Protocol Data Unit</td><td>Data Link</td><td>IEEE 802.1D</td><td>Control frames exchanged between Layer 2 switches to construct Spanning Trees.</td></tr>
          <tr><td><strong>CIDR</strong></td><td>Classless Inter-Domain Routing</td><td>Network</td><td>RFC 1519</td><td>Prefix-length subnetting scheme replacing rigid Class A/B/C addressing.</td></tr>
          <tr><td><strong>CRC</strong></td><td>Cyclic Redundancy Check</td><td>Data Link/L4</td><td>ISO 3309</td><td>Polynomial modulo-2 division error detection algorithm (e.g., CRC-32).</td></tr>
          <tr><td><strong>CSMA/CA</strong></td><td>Carrier Sense Multiple Access / CA</td><td>Data Link</td><td>IEEE 802.11</td><td>Random access scheme using IFS, NAV, and RTS/CTS handshake for Wi-Fi.</td></tr>
          <tr><td><strong>CSMA/CD</strong></td><td>Carrier Sense Multiple Access / CD</td><td>Data Link</td><td>IEEE 802.3</td><td>Ethernet arbitration scheme aborting transmission upon signal collision detection.</td></tr>
          <tr><td><strong>CTS</strong></td><td>Clear to Send</td><td>Data Link</td><td>IEEE 802.11</td><td>Control frame sent by receiver granting channel reservation to sender.</td></tr>
          <tr><td><strong>CWND</strong></td><td>Congestion Window</td><td>Transport</td><td>RFC 5681</td><td>Sender-side state variable bounding maximum in-flight unacknowledged bytes.</td></tr>
          <tr><td><strong>DHCP</strong></td><td>Dynamic Host Configuration Protocol</td><td>Application</td><td>RFC 2131</td><td>Client-server protocol dynamically assigning IP, mask, gateway, DNS parameters.</td></tr>
          <tr><td><strong>DIFS</strong></td><td>DCF Inter-Frame Space</td><td>Data Link</td><td>IEEE 802.11</td><td>Minimum delay required before a wireless station can transmit distributed frames.</td></tr>
          <tr><td><strong>DKIM</strong></td><td>DomainKeys Identified Mail</td><td>Application</td><td>RFC 6376</td><td>Cryptographic signature verification system preventing email spoofing.</td></tr>
          <tr><td><strong>DMARC</strong></td><td>Domain-based Message Auth., Reporting</td><td>Application</td><td>RFC 7489</td><td>Email authentication policy framework combining SPF and DKIM.</td></tr>
          <tr><td><strong>DNS</strong></td><td>Domain Name System</td><td>Application</td><td>RFC 1034/1035</td><td>Globally distributed hierarchical database translating FQDNs to IP addresses.</td></tr>
          <tr><td><strong>DSCP</strong></td><td>Differentiated Services Code Point</td><td>Network</td><td>RFC 2474</td><td>6-bit field in IPv4 ToS / IPv6 Traffic Class for packet QoS classification.</td></tr>
          <tr><td><strong>ECN</strong></td><td>Explicit Congestion Notification</td><td>Network/L4</td><td>RFC 3168</td><td>Router-to-endpoint feedback mechanism marking bits without dropping packets.</td></tr>
          <tr><td><strong>FTP</strong></td><td>File Transfer Protocol</td><td>Application</td><td>RFC 959</td><td>Client-server protocol utilizing out-of-band control (:21) &amp; data (:20) connections.</td></tr>
          <tr><td><strong>HDLC</strong></td><td>High-Level Data Link Control</td><td>Data Link</td><td>ISO 13239</td><td>Bit-oriented synchronous data link framing and flow control protocol.</td></tr>
          <tr><td><strong>HTTP</strong></td><td>HyperText Transfer Protocol</td><td>Application</td><td>RFC 9110</td><td>Application-level request-response protocol powering the World Wide Web.</td></tr>
          <tr><td><strong>HTTPS</strong></td><td>HyperText Transfer Protocol Secure</td><td>Application</td><td>RFC 2818</td><td>HTTP layered over Transport Layer Security (TLS) cryptographic tunnel.</td></tr>
          <tr><td><strong>IAC</strong></td><td>Interpret As Command</td><td>Application</td><td>RFC 854</td><td>Special escape byte (0xFF) used in Telnet for in-band command parsing.</td></tr>
          <tr><td><strong>ICMP</strong></td><td>Internet Control Message Protocol</td><td>Network</td><td>RFC 792</td><td>Layer 3 companion protocol for diagnostic reporting and error signaling.</td></tr>
          <tr><td><strong>IGMP</strong></td><td>Internet Group Management Protocol</td><td>Network</td><td>RFC 2236</td><td>Protocol used by IPv4 hosts to report multicast group memberships to routers.</td></tr>
          <tr><td><strong>IMAP4</strong></td><td>Internet Message Access Protocol v4</td><td>Application</td><td>RFC 3501</td><td>Stateful email access protocol maintaining folder synchronization on servers.</td></tr>
          <tr><td><strong>IP</strong></td><td>Internet Protocol</td><td>Network</td><td>RFC 791/8200</td><td>Best-effort, connectionless packet delivery across network boundaries.</td></tr>
          <tr><td><strong>LLC</strong></td><td>Logical Link Control</td><td>Data Link</td><td>IEEE 802.2</td><td>Upper sublayer of Data Link providing flow control and SAP multiplexing.</td></tr>
          <tr><td><strong>MAC</strong></td><td>Medium Access Control</td><td>Data Link</td><td>IEEE 802.3/11</td><td>Lower sublayer of Data Link managing physical addressing and channel arbitration.</td></tr>
          <tr><td><strong>MSS</strong></td><td>Maximum Segment Size</td><td>Transport</td><td>RFC 879</td><td>Maximum TCP payload bytes a host can receive without IP fragmentation.</td></tr>
          <tr><td><strong>MTU</strong></td><td>Maximum Transmission Unit</td><td>Data Link/L3</td><td>Hardware</td><td>Maximum frame payload size in bytes supported by underlying link layer.</td></tr>
          <tr><td><strong>NAT</strong></td><td>Network Address Translation</td><td>Network</td><td>RFC 1631/3022</td><td>Modifies source/destination IP addresses traversing a router gateway.</td></tr>
          <tr><td><strong>NAV</strong></td><td>Network Allocation Vector</td><td>Data Link</td><td>IEEE 802.11</td><td>Virtual carrier-sensing timer updated by overheard RTS/CTS duration fields.</td></tr>
          <tr><td><strong>NVT</strong></td><td>Network Virtual Terminal</td><td>Application</td><td>RFC 854</td><td>Standard imaginary terminal representation used to bridge heterogeneous Telnet hosts.</td></tr>
          <tr><td><strong>OSPF</strong></td><td>Open Shortest Path First</td><td>Network</td><td>RFC 2328</td><td>Link-state Interior Gateway Protocol using Dijkstra SPF algorithm.</td></tr>
          <tr><td><strong>POP3</strong></td><td>Post Office Protocol Version 3</td><td>Application</td><td>RFC 1939</td><td>Simple pull-based email retrieval protocol operating over TCP port 110.</td></tr>
          <tr><td><strong>QUIC</strong></td><td>Quick UDP Internet Connections</td><td>Transport</td><td>RFC 9000</td><td>Multiplexed, encrypted transport protocol over UDP; foundation of HTTP/3.</td></tr>
          <tr><td><strong>RARP</strong></td><td>Reverse Address Resolution Protocol</td><td>Data Link/L3</td><td>RFC 903</td><td>Bootstrap mapping 48-bit MAC to 32-bit IP via Layer 2 broadcast.</td></tr>
          <tr><td><strong>RIP</strong></td><td>Routing Information Protocol</td><td>Application/L3</td><td>RFC 1058/2453</td><td>Distance-vector IGP utilizing Bellman-Ford and hop-count metric (max 15).</td></tr>
          <tr><td><strong>RTO</strong></td><td>Retransmission Timeout</td><td>Transport</td><td>RFC 6298</td><td>Dynamic timer expiring when segment ACK fails to arrive in window.</td></tr>
          <tr><td><strong>RTS</strong></td><td>Request to Send</td><td>Data Link</td><td>IEEE 802.11</td><td>Control frame sent to initiate wireless reservation and mitigate hidden terminals.</td></tr>
          <tr><td><strong>RTT</strong></td><td>Round-Trip Time</td><td>Transport</td><td>Measurement</td><td>Time taken for a data packet to travel from source to destination and return.</td></tr>
          <tr><td><strong>RWND</strong></td><td>Receive Window</td><td>Transport</td><td>RFC 793</td><td>Receiver advertised buffer capacity preventing receive buffer overrun.</td></tr>
          <tr><td><strong>SACK</strong></td><td>Selective Acknowledgment</td><td>Transport</td><td>RFC 2018</td><td>TCP option permitting receiver to ACK non-contiguous blocks of bytes.</td></tr>
          <tr><td><strong>SCTP</strong></td><td>Stream Control Transmission Protocol</td><td>Transport</td><td>RFC 4960</td><td>Message-oriented reliable transport providing multi-homing &amp; multi-streaming.</td></tr>
          <tr><td><strong>SIFS</strong></td><td>Short Inter-Frame Space</td><td>Data Link</td><td>IEEE 802.11</td><td>Smallest IFS used for immediate response frames (ACK, CTS).</td></tr>
          <tr><td><strong>SMTP</strong></td><td>Simple Mail Transfer Protocol</td><td>Application</td><td>RFC 5321</td><td>Push-based email delivery and relay protocol operating over TCP.</td></tr>
          <tr><td><strong>SNMP</strong></td><td>Simple Network Management Protocol</td><td>Application</td><td>RFC 1157</td><td>Protocol for monitoring and configuring network devices via UDP 161/162.</td></tr>
          <tr><td><strong>SSH</strong></td><td>Secure Shell</td><td>Application</td><td>RFC 4251</td><td>Cryptographically secure protocol for remote terminal login and command execution.</td></tr>
          <tr><td><strong>STP</strong></td><td>Spanning Tree Protocol</td><td>Data Link</td><td>IEEE 802.1D</td><td>Loop-prevention protocol disabling redundant switch links in LANs.</td></tr>
          <tr><td><strong>TCP</strong></td><td>Transmission Control Protocol</td><td>Transport</td><td>RFC 793/9293</td><td>Connection-oriented, reliable, byte-stream, full-duplex protocol.</td></tr>
          <tr><td><strong>TFTP</strong></td><td>Trivial File Transfer Protocol</td><td>Application</td><td>RFC 1350</td><td>Lockstep UDP-based file transfer protocol with minimal overhead.</td></tr>
          <tr><td><strong>TLS</strong></td><td>Transport Layer Security</td><td>Security/L4</td><td>RFC 8446</td><td>Cryptographic protocol providing end-to-end encryption and integrity (TLS 1.3).</td></tr>
          <tr><td><strong>TTL</strong></td><td>Time To Live</td><td>Network</td><td>RFC 791</td><td>8-bit hop counter decremented by routers to prevent infinite routing loops.</td></tr>
          <tr><td><strong>UDP</strong></td><td>User Datagram Protocol</td><td>Transport</td><td>RFC 768</td><td>Minimalist, connectionless, unreliable datagram transport protocol.</td></tr>
          <tr><td><strong>VLAN</strong></td><td>Virtual Local Area Network</td><td>Data Link</td><td>IEEE 802.1Q</td><td>Logical broadcast domain partition configured on Layer 2 switches.</td></tr>
          <tr><td><strong>VLSM</strong></td><td>Variable Length Subnet Masking</td><td>Network</td><td>RFC 1878</td><td>Technique allowing arbitrary mask lengths within the same network prefix.</td></tr>
        </tbody>
      </table>

      <hr>

      <h1 class="appendix-title" id="appendix-b">APPENDIX B: COMPLETE PORT NUMBERS &amp; PROTOCOLS MASTER MATRIX</h1>
      <p>Master directory of Well-Known Ports (0–1023) and key Registered Ports (1024–49151) essential for university examinations and networking diagnostics:</p>

      <table style="font-size: 8.5pt;">
        <thead>
          <tr>
            <th style="width: 8%;">Port</th>
            <th style="width: 15%;">Protocol</th>
            <th style="width: 12%;">Transport</th>
            <th style="width: 15%;">Standard</th>
            <th>Functional Role &amp; Operational Rationale</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>20</strong></td><td>FTP-Data</td><td>TCP</td><td>RFC 959</td><td>Active mode data channel; server initiates outbound connection to client.</td></tr>
          <tr><td><strong>21</strong></td><td>FTP-Control</td><td>TCP</td><td>RFC 959</td><td>Control channel; persistent out-of-band channel for transmitting commands &amp; codes.</td></tr>
          <tr><td><strong>22</strong></td><td>SSH / SFTP</td><td>TCP</td><td>RFC 4251</td><td>Secure Shell encrypted remote terminal, SFTP file transfer, and encrypted port forwarding.</td></tr>
          <tr><td><strong>23</strong></td><td>Telnet</td><td>TCP</td><td>RFC 854</td><td>Unencrypted remote terminal session using NVT abstraction (deprecated).</td></tr>
          <tr><td><strong>25</strong></td><td>SMTP</td><td>TCP</td><td>RFC 5321</td><td>Simple Mail Transfer Protocol; server-to-server (MTA-to-MTA) email relaying.</td></tr>
          <tr><td><strong>53</strong></td><td>DNS</td><td>UDP &amp; TCP</td><td>RFC 1035</td><td>UDP for queries &lt; 512B; TCP for zone transfers (AXFR) and large responses.</td></tr>
          <tr><td><strong>67</strong></td><td>DHCP Server</td><td>UDP</td><td>RFC 2131</td><td>Listens for broadcast client DHCPDISCOVER and DHCPREQUEST messages.</td></tr>
          <tr><td><strong>68</strong></td><td>DHCP Client</td><td>UDP</td><td>RFC 2131</td><td>Client port receiving unicast/broadcast DHCPOFFER and DHCPACK responses.</td></tr>
          <tr><td><strong>69</strong></td><td>TFTP</td><td>UDP</td><td>RFC 1350</td><td>Trivial lockstep Stop-and-Wait file transfer for diskless PXE network bootloaders.</td></tr>
          <tr><td><strong>80</strong></td><td>HTTP</td><td>TCP</td><td>RFC 9110</td><td>World Wide Web unencrypted plaintext hypertext document transfer.</td></tr>
          <tr><td><strong>110</strong></td><td>POP3</td><td>TCP</td><td>RFC 1939</td><td>Pulls email from remote server to local mail spool; download &amp; delete/keep semantics.</td></tr>
          <tr><td><strong>123</strong></td><td>NTP</td><td>UDP</td><td>RFC 5905</td><td>Network Time Protocol; precision clock synchronization across network hierarchies.</td></tr>
          <tr><td><strong>143</strong></td><td>IMAP4</td><td>TCP</td><td>RFC 3501</td><td>Stateful remote mailbox access; preserves folder hierarchies and flags on server.</td></tr>
          <tr><td><strong>161</strong></td><td>SNMP Agent</td><td>UDP</td><td>RFC 1157</td><td>SNMP agent port polled by Network Management Stations (Get, Set, Next).</td></tr>
          <tr><td><strong>162</strong></td><td>SNMP Trap</td><td>UDP</td><td>RFC 1157</td><td>Management station (NMS) port receiving unsolicited alert notifications from agents.</td></tr>
          <tr><td><strong>179</strong></td><td>BGP-4</td><td>TCP</td><td>RFC 4271</td><td>Autonomous System path-vector inter-domain routing peer sessions.</td></tr>
          <tr><td><strong>443</strong></td><td>HTTPS / QUIC</td><td>TCP / UDP</td><td>RFC 2818 / 9000</td><td>Secure HTTP; TCP for TLS encrypted web traffic; UDP for HTTP/3 QUIC transport.</td></tr>
          <tr><td><strong>465</strong></td><td>SMTPS</td><td>TCP</td><td>RFC 8314</td><td>Implicit TLS mail submission from client to server.</td></tr>
          <tr><td><strong>520</strong></td><td>RIP</td><td>UDP</td><td>RFC 2453</td><td>Routing Information Protocol; periodic broadcast/multicast of Bellman-Ford tables.</td></tr>
          <tr><td><strong>587</strong></td><td>Submission</td><td>TCP</td><td>RFC 6409</td><td>Client-to-server mail submission (MUA to MSA) requiring mandatory authentication.</td></tr>
          <tr><td><strong>993</strong></td><td>IMAPS</td><td>TCP</td><td>RFC 8314</td><td>Implicit TLS-encrypted IMAP4 mailbox synchronization.</td></tr>
          <tr><td><strong>995</strong></td><td>POP3S</td><td>TCP</td><td>RFC 8314</td><td>Implicit TLS-encrypted POP3 mailbox retrieval.</td></tr>
          <tr><td><strong>1080</strong></td><td>SOCKS5</td><td>TCP</td><td>RFC 1928</td><td>Generic proxy protocol for client-server TCP/UDP tunneling (SSH dynamic proxy).</td></tr>
          <tr><td><strong>3306</strong></td><td>MySQL</td><td>TCP</td><td>IANA Assigned</td><td>MySQL / MariaDB relational database server daemon.</td></tr>
          <tr><td><strong>5004</strong></td><td>RTP</td><td>UDP</td><td>RFC 3550</td><td>Real-time Transport Protocol for streaming audio and video packets.</td></tr>
          <tr><td><strong>8080</strong></td><td>HTTP-Alt</td><td>TCP</td><td>RFC 7230</td><td>Secondary web server port / Apache Tomcat / Squid web caching proxy.</td></tr>
        </tbody>
      </table>

      <hr>

      <h1 class="appendix-title" id="appendix-c">APPENDIX C: MASTER EXAM FORMULA SHEET</h1>
      <p>Exhaustive mathematical reference compiling all formulas across Units 1 through 5:</p>

      <h2>1. Physical Layer &amp; Transmission Limits</h2>
      <ul>
        <li><strong>Nyquist Maximum Bit Rate (Noiseless):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>C</mi><mo>=</mo><mn>2</mn><mi>B</mi><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">(</mo><mi>M</mi><mo stretchy="false">)</mo><mspace width="1em"></mspace><mo stretchy="false">[</mo><mtext>bps</mtext><mo stretchy="false">]</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Shannon Channel Capacity (Noisy Channel):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>C</mi><mo>=</mo><mi>B</mi><msub><mi>log</mi><mn>2</mn></msub><mo stretchy="false">(</mo><mn>1</mn><mo>+</mo><mtext>SNR</mtext><mo stretchy="false">)</mo><mspace width="1em"></mspace><mo stretchy="false">[</mo><mtext>bps</mtext><mo stretchy="false">]</mo><mo separator="true">;</mo><mspace width="1em"></mspace><msub><mtext>SNR</mtext><mtext>dB</mtext></msub><mo>=</mo><mn>10</mn><msub><mi>log</mi><mn>10</mn></msub><mo stretchy="false">(</mo><mtext>SNR</mtext><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>End-to-End Latency:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>D</mi><mtext>total</mtext></msub><mo>=</mo><msub><mi>D</mi><mtext>tx</mtext></msub><mo>+</mo><msub><mi>D</mi><mtext>prop</mtext></msub><mo>+</mo><msub><mi>D</mi><mtext>queue</mtext></msub><mo>+</mo><msub><mi>D</mi><mtext>proc</mtext></msub><mo>=</mo><mfrac><mi>L</mi><mi>R</mi></mfrac><mo>+</mo><mfrac><mi>d</mi><mi>s</mi></mfrac><mo>+</mo><msub><mi>D</mi><mtext>queue</mtext></msub><mo>+</mo><msub><mi>D</mi><mtext>proc</mtext></msub></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Bandwidth-Delay Product (BDP):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>BDP (bits)</mtext><mo>=</mo><mtext>Bandwidth (bps)</mtext><mo>×</mo><msub><mi>D</mi><mtext>prop</mtext></msub><mtext> (s)</mtext></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Mesh Network Links &amp; Ports:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Links</mtext><mo>=</mo><mfrac><mrow><mi>N</mi><mo stretchy="false">(</mo><mi>N</mi><mo>−</mo><mn>1</mn><mo stretchy="false">)</mo></mrow><mn>2</mn></mfrac><mo separator="true">;</mo><mspace width="1em"></mspace><mtext>Ports per node</mtext><mo>=</mo><mi>N</mi><mo>−</mo><mn>1</mn></mrow></semantics></math></span></span></div>
        </li>
      </ul>

      <h2>2. Data Link Layer &amp; MAC Protocols</h2>
      <ul>
        <li><strong>Hamming Distance Detection/Correction Bounds:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>d</mi><mtext>min</mtext></msub><mo>≥</mo><mi>s</mi><mo>+</mo><mn>1</mn><mspace width="1em"></mspace><mo stretchy="false">(</mo><mtext>Detection of </mtext><mi>s</mi><mtext> errors</mtext><mo stretchy="false">)</mo><mo separator="true">;</mo><mspace width="1em"></mspace><msub><mi>d</mi><mtext>min</mtext></msub><mo>≥</mo><mn>2</mn><mi>t</mi><mo>+</mo><mn>1</mn><mspace width="1em"></mspace><mo stretchy="false">(</mo><mtext>Correction of </mtext><mi>t</mi><mtext> errors</mtext><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Hamming Code Inequality:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msup><mn>2</mn><mi>r</mi></msup><mo>≥</mo><mi>m</mi><mo>+</mo><mi>r</mi><mo>+</mo><mn>1</mn><mspace width="1em"></mspace><mo stretchy="false">(</mo><mi>m</mi><mo>=</mo><mtext>data bits</mtext><mo separator="true">,</mo><mspace width="0.3333em"></mspace><mi>r</mi><mo>=</mo><mtext>parity bits</mtext><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Sliding Window Protocol Utilization:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>U</mi><mo>=</mo><mi>min</mi><mrow><mo fence="true">(</mo><mn>1</mn><mo separator="true">,</mo><mspace width="0.3333em"></mspace><mfrac><mi>W</mi><mrow><mn>1</mn><mo>+</mo><mn>2</mn><mi>a</mi></mrow></mfrac><mo fence="true">)</mo></mrow><mspace width="1em"></mspace><mtext>where </mtext><mi>a</mi><mo>=</mo><mfrac><msub><mi>T</mi><mtext>prop</mtext></msub><msub><mi>T</mi><mtext>tx</mtext></msub></mfrac></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>ALOHA Throughput Limits:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>S</mi><mtext>Pure</mtext></msub><mo>=</mo><mi>G</mi><msup><mi>e</mi><mrow><mo>−</mo><mn>2</mn><mi>G</mi></mrow></msup><mspace width="0.2778em"></mspace><mo stretchy="false">(</mo><msub><mi>S</mi><mtext>max</mtext></msub><mo>=</mo><mn>18.4</mn><mi mathvariant="normal">%</mi><mo stretchy="false">)</mo><mo separator="true">;</mo><mspace width="1em"></mspace><msub><mi>S</mi><mtext>Slotted</mtext></msub><mo>=</mo><mi>G</mi><msup><mi>e</mi><mrow><mo>−</mo><mi>G</mi></mrow></msup><mspace width="0.2778em"></mspace><mo stretchy="false">(</mo><msub><mi>S</mi><mtext>max</mtext></msub><mo>=</mo><mn>36.8</mn><mi mathvariant="normal">%</mi><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>CSMA/CD Minimum Frame Length (IEEE 802.3 Ethernet):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>L</mi><mtext>min</mtext></msub><mo>≥</mo><mn>2</mn><mo>⋅</mo><mi>R</mi><mo>⋅</mo><mfrac><msub><mi>d</mi><mtext>max</mtext></msub><mi>s</mi></mfrac><mspace width="1em"></mspace><mo stretchy="false">(</mo><mtext>Standard Ethernet: </mtext><msub><mi>L</mi><mtext>min</mtext></msub><mo>=</mo><mn>64</mn><mtext> bytes</mtext><mo>=</mo><mn>512</mn><mtext> bits</mtext><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
      </ul>

      <h2>3. Network Layer &amp; Routing</h2>
      <ul>
        <li><strong>Bellman-Ford Shortest Path Equation:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>D</mi><mi>x</mi></msub><mo stretchy="false">(</mo><mi>y</mi><mo stretchy="false">)</mo><mo>=</mo><munder><mi>min</mi><mi>v</mi></munder><mo stretchy="false">{</mo><mi>c</mi><mo stretchy="false">(</mo><mi>x</mi><mo separator="true">,</mo><mi>v</mi><mo stretchy="false">)</mo><mo>+</mo><msub><mi>D</mi><mi>v</mi></msub><mo stretchy="false">(</mo><mi>y</mi><mo stretchy="false">)</mo><mo stretchy="false">}</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Token Bucket Maximum Burst Duration ($T$):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>T</mi><mo>=</mo><mfrac><mi>C</mi><mrow><mi>M</mi><mo>−</mo><mi>r</mi></mrow></mfrac><mspace width="1em"></mspace><mo stretchy="false">[</mo><mtext>seconds</mtext><mo stretchy="false">]</mo><mo separator="true">;</mo><mspace width="1em"></mspace><msub><mi>V</mi><mtext>burst</mtext></msub><mo>=</mo><mi>M</mi><mo>×</mo><mi>T</mi><mo>=</mo><mfrac><mrow><mi>C</mi><mo>⋅</mo><mi>M</mi></mrow><mrow><mi>M</mi><mo>−</mo><mi>r</mi></mrow></mfrac><mspace width="1em"></mspace><mo stretchy="false">[</mo><mtext>bytes</mtext><mo stretchy="false">]</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Subnetting Capacity:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>N</mi><mtext>subnets</mtext></msub><mo>=</mo><msup><mn>2</mn><mi>s</mi></msup><mo separator="true">;</mo><mspace width="1em"></mspace><msub><mi>N</mi><mtext>usable hosts</mtext></msub><mo>=</mo><msup><mn>2</mn><mrow><mi>h</mi><mo>−</mo><mi>s</mi></mrow></msup><mo>−</mo><mn>2</mn></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>IPv4 Fragmentation Offset:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Max Payload</mtext><mo>=</mo><mrow><mo fence="true">⌊</mo><mfrac><mrow><mtext>MTU</mtext><mo>−</mo><mn>20</mn></mrow><mn>8</mn></mfrac><mo fence="true">⌋</mo></mrow><mo>×</mo><mn>8</mn><mo separator="true">;</mo><mspace width="1em"></mspace><mtext>Offset</mtext><mo>=</mo><mfrac><mtext>Byte Offset</mtext><mn>8</mn></mfrac></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>OSPF Link Cost:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Cost</mtext><mo>=</mo><mfrac><msup><mn>10</mn><mn>8</mn></msup><mtext>Bandwidth (bps)</mtext></mfrac></mrow></semantics></math></span></span></div>
        </li>
      </ul>

      <h2>4. Transport Layer &amp; Congestion Control</h2>
      <ul>
        <li><strong>Jacobson's Dynamic RTO (RFC 6298):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>S</mi><mi>R</mi><mi>T</mi><msub><mi>T</mi><mtext>new</mtext></msub><mo>=</mo><mo stretchy="false">(</mo><mn>1</mn><mo>−</mo><mi>α</mi><mo stretchy="false">)</mo><mo>⋅</mo><mi>S</mi><mi>R</mi><mi>T</mi><msub><mi>T</mi><mtext>old</mtext></msub><mo>+</mo><mi>α</mi><mo>⋅</mo><mi>R</mi><mi>T</mi><msub><mi>T</mi><mi>m</mi></msub><mspace width="1em"></mspace><mo stretchy="false">(</mo><mi>α</mi><mo>=</mo><mn>0.125</mn><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>R</mi><mi>T</mi><mi>T</mi><mi>V</mi><mi>A</mi><msub><mi>R</mi><mtext>new</mtext></msub><mo>=</mo><mo stretchy="false">(</mo><mn>1</mn><mo>−</mo><mi>β</mi><mo stretchy="false">)</mo><mo>⋅</mo><mi>R</mi><mi>T</mi><mi>T</mi><mi>V</mi><mi>A</mi><msub><mi>R</mi><mtext>old</mtext></msub><mo>+</mo><mi>β</mi><mo>⋅</mo><mo stretchy="false">∣</mo><mi>S</mi><mi>R</mi><mi>T</mi><msub><mi>T</mi><mtext>new</mtext></msub><mo>−</mo><mi>R</mi><mi>T</mi><msub><mi>T</mi><mi>m</mi></msub><mo stretchy="false">∣</mo><mspace width="1em"></mspace><mo stretchy="false">(</mo><mi>β</mi><mo>=</mo><mn>0.25</mn><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>R</mi><mi>T</mi><mi>O</mi><mo>=</mo><mi>S</mi><mi>R</mi><mi>T</mi><msub><mi>T</mi><mtext>new</mtext></msub><mo>+</mo><mn>4</mn><mo>⋅</mo><mi>R</mi><mi>T</mi><mi>T</mi><mi>V</mi><mi>A</mi><msub><mi>R</mi><mtext>new</mtext></msub><mspace width="1em"></mspace><mo stretchy="false">(</mo><mi>R</mi><mi>T</mi><mi>O</mi><mo>≥</mo><mn>1.0</mn><mtext> s</mtext><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>TCP Reno Fast Recovery:</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mtext>Upon 3 Dup ACKs: </mtext><mi>s</mi><mi>s</mi><mi>t</mi><mi>h</mi><mi>r</mi><mi>e</mi><mi>s</mi><mi>h</mi><mo>=</mo><mfrac><mrow><mi>c</mi><mi>w</mi><mi>n</mi><mi>d</mi></mrow><mn>2</mn></mfrac><mo separator="true">;</mo><mspace width="1em"></mspace><mi>c</mi><mi>w</mi><mi>n</mi><mi>d</mi><mo>=</mo><mi>s</mi><mi>s</mi><mi>t</mi><mi>h</mi><mi>r</mi><mi>e</mi><mi>s</mi><mi>h</mi><mo>+</mo><mn>3</mn><mo>⋅</mo><mtext>MSS</mtext></mrow></semantics></math></span></span></div>
        </li>
      </ul>

      <h2>5. Application Layer &amp; Cryptography</h2>
      <ul>
        <li><strong>Base64 Character Expansion (MIME):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>N</mi><mtext>out</mtext></msub><mo>=</mo><mn>4</mn><mo>×</mo><mrow><mo fence="true">⌈</mo><mfrac><msub><mi>N</mi><mtext>in</mtext></msub><mn>3</mn></mfrac><mo fence="true">⌉</mo></mrow><mspace width="1em"></mspace><mo stretchy="false">(</mo><mtext>Bandwidth expansion overhead</mtext><mo>=</mo><mo>+</mo><mn>33.33</mn><mi mathvariant="normal">%</mi><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
        <li><strong>Diffie-Hellman Session Key Derivation (SSH):</strong>
          <div class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>e</mi><mo>=</mo><msup><mi>g</mi><mi>x</mi></msup><mspace width="0.4444em"></mspace><mo stretchy="false">(</mo><mrow><mi mathvariant="normal">m</mi><mi mathvariant="normal">o</mi><mi mathvariant="normal">d</mi></mrow><mspace width="0.3333em"></mspace><mi>p</mi><mo stretchy="false">)</mo><mo separator="true">;</mo><mspace width="1em"></mspace><mi>f</mi><mo>=</mo><msup><mi>g</mi><mi>y</mi></msup><mspace width="0.4444em"></mspace><mo stretchy="false">(</mo><mrow><mi mathvariant="normal">m</mi><mi mathvariant="normal">o</mi><mi mathvariant="normal">d</mi></mrow><mspace width="0.3333em"></mspace><mi>p</mi><mo stretchy="false">)</mo><mo separator="true">;</mo><mspace width="1em"></mspace><mi>K</mi><mo>=</mo><msup><mi>e</mi><mi>y</mi></msup><mspace width="0.4444em"></mspace><mo stretchy="false">(</mo><mrow><mi mathvariant="normal">m</mi><mi mathvariant="normal">o</mi><mi mathvariant="normal">d</mi></mrow><mspace width="0.3333em"></mspace><mi>p</mi><mo stretchy="false">)</mo><mo>=</mo><msup><mi>f</mi><mi>x</mi></msup><mspace width="0.4444em"></mspace><mo stretchy="false">(</mo><mrow><mi mathvariant="normal">m</mi><mi mathvariant="normal">o</mi><mi mathvariant="normal">d</mi></mrow><mspace width="0.3333em"></mspace><mi>p</mi><mo stretchy="false">)</mo><mo>=</mo><msup><mi>g</mi><mrow><mi>x</mi><mi>y</mi></mrow></msup><mspace width="0.4444em"></mspace><mo stretchy="false">(</mo><mrow><mi mathvariant="normal">m</mi><mi mathvariant="normal">o</mi><mi mathvariant="normal">d</mi></mrow><mspace width="0.3333em"></mspace><mi>p</mi><mo stretchy="false">)</mo></mrow></semantics></math></span></span></div>
        </li>
      </ul>
    </div>
  `;

  // Assemble the Complete Book HTML
  const masterHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Computer Networks (21CS302) — Master University Exam Preparation Textbook</title>
  <style>
    ${katexCss}
    ${textbookCss}
  </style>
</head>
<body>

  ${frontMatterHtml}

  <!-- UNIT 1 -->
  <div class="unit-divider">
    <div class="unit-divider-num">Curriculum Module &bull; Unit I</div>
    <div class="unit-divider-title">Introduction and Physical Layer</div>
    <div class="unit-divider-meta">
      <span><strong>Course Outcome:</strong> CO1 (Measure switched network performance)</span>
      <span><strong>Contact Hours:</strong> 9 Lecture Periods</span>
    </div>
  </div>
  ${u1ShortHtml}
  ${u1LongHtml}

  <!-- UNIT 2 -->
  <div class="unit-divider">
    <div class="unit-divider-num">Curriculum Module &bull; Unit II</div>
    <div class="unit-divider-title">Data-Link Layer and MAC Sublayer</div>
    <div class="unit-divider-meta">
      <span><strong>Course Outcome:</strong> CO2 (Utilize Link layer services &amp; IEEE standards)</span>
      <span><strong>Contact Hours:</strong> 9 Lecture Periods</span>
    </div>
  </div>
  ${u2LongHtml}

  <!-- UNIT 3 -->
  <div class="unit-divider">
    <div class="unit-divider-num">Curriculum Module &bull; Unit III</div>
    <div class="unit-divider-title">Network Layer and Routing Architecture</div>
    <div class="unit-divider-meta">
      <span><strong>Course Outcome:</strong> CO3 (Subnetting, IPv4/IPv6 &amp; Unicast routing)</span>
      <span><strong>Contact Hours:</strong> 9 Lecture Periods</span>
    </div>
  </div>
  ${u3LongHtml}

  <!-- UNIT 4 -->
  <div class="unit-divider">
    <div class="unit-divider-num">Curriculum Module &bull; Unit IV</div>
    <div class="unit-divider-title">Transport Layer Protocols and Services</div>
    <div class="unit-divider-meta">
      <span><strong>Course Outcome:</strong> CO4 (Process-to-process delivery &amp; congestion control)</span>
      <span><strong>Contact Hours:</strong> 9 Lecture Periods</span>
    </div>
  </div>
  ${u4LongHtml}

  <!-- UNIT 5 -->
  <div class="unit-divider">
    <div class="unit-divider-num">Curriculum Module &bull; Unit V</div>
    <div class="unit-divider-title">Application Layer Protocols and Architectures</div>
    <div class="unit-divider-meta">
      <span><strong>Course Outcome:</strong> CO5 (Utilize application protocols for real-time scenarios)</span>
      <span><strong>Contact Hours:</strong> 9 Lecture Periods</span>
    </div>
  </div>
  ${u5LongHtml}

  <!-- APPENDICES -->
  ${appendixHtml}

</body>
</html>`;

  const outputHtmlPath = path.resolve(__dirname, "master_textbook.html");
  fs.writeFileSync(outputHtmlPath, masterHtml, "utf8");
  console.log(`Master HTML written to ${outputHtmlPath} (${(masterHtml.length / 1024 / 1024).toFixed(2)} MB)`);

  // Launch Chromium to render the PDF
  console.log("Launching Chromium to generate publication-grade PDF...");
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-gpu",
      "--font-render-hinting=medium",
      "--enable-font-antialiasing"
    ]
  });

  const page = await browser.newPage();
  
  // Set viewport
  await page.setViewport({ width: 1200, height: 1600 });

  console.log("Loading HTML into Chromium...");
  await page.goto(`file://${outputHtmlPath}`, {
    waitUntil: "networkidle0",
    timeout: 120000
  });

  const pdfOutputPath = path.resolve(projectRoot, "Computer_Networks_21CS302_Master_Textbook.pdf");

  const { PDFDocument } = require("pdf-lib");

  console.log("Rendering Cover Page (full-bleed, no headers/footers)...");
  const coverPdfBuffer = await page.pdf({
    format: "A4",
    pageRanges: "1",
    printBackground: true,
    displayHeaderFooter: false,
    margin: { top: "0px", bottom: "0px", left: "0px", right: "0px" }
  });

  console.log("Rendering Content Pages (with running headers & footers)...");
  const contentPdfBuffer = await page.pdf({
    format: "A4",
    pageRanges: "2-",
    printBackground: true,
    displayHeaderFooter: true,
    margin: {
      top: "55px",
      bottom: "55px",
      left: "42px",
      right: "42px"
    },
    headerTemplate: `
      <div style="font-family: 'Inter', -apple-system, sans-serif; font-size: 8pt; color: #64748b; width: 100%; padding: 0 42px; display: flex; justify-content: space-between; border-bottom: 0.5px solid #cbd5e1; padding-bottom: 4px;">
        <span><strong>21CS302 &bull; Computer Networks</strong> &mdash; Master Exam Preparation Textbook</span>
        <span style="text-transform: uppercase; letter-spacing: 0.5px;">Anna University / Autonomous Curriculum</span>
      </div>
    `,
    footerTemplate: `
      <div style="font-family: 'Inter', -apple-system, sans-serif; font-size: 8pt; color: #64748b; width: 100%; padding: 0 42px; display: flex; justify-content: space-between; border-top: 0.5px solid #cbd5e1; padding-top: 4px;">
        <span>Public Repository: <span style="color: #2563eb;">github.com/sanjithdoescode/Computer-Networks-21CS302</span></span>
        <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
      </div>
    `,
    timeout: 180000
  });

  await browser.close();

  console.log("Merging Cover Page and Content Pages into Master Textbook PDF...");
  const mergedPdf = await PDFDocument.create();
  const coverDoc = await PDFDocument.load(coverPdfBuffer);
  const contentDoc = await PDFDocument.load(contentPdfBuffer);

  const [copiedCover] = await mergedPdf.copyPages(coverDoc, [0]);
  mergedPdf.addPage(copiedCover);

  const copiedContentPages = await mergedPdf.copyPages(contentDoc, contentDoc.getPageIndices());
  copiedContentPages.forEach(p => mergedPdf.addPage(p));

  const finalPdfBytes = await mergedPdf.save();
  fs.writeFileSync(pdfOutputPath, finalPdfBytes);

  const stats = fs.statSync(pdfOutputPath);
  console.log("\n=======================================================");
  console.log("🎉 MASTER TEXTBOOK PDF GENERATION COMPLETE!");
  console.log(`Path: ${pdfOutputPath}`);
  console.log(`Pages: ${mergedPdf.getPageCount()}`);
  console.log(`File Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
  console.log("=======================================================\n");
}

buildMasterBook().catch(err => {
  console.error("Compilation error:", err);
  process.exit(1);
});
