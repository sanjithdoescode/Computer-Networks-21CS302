# Agent Rule: University Exam Comprehensive Answer Style (16-Mark Long Answers)

This rule defines the mandatory structure, depth, and formatting guidelines when generating exam answers for Computer Networks (21CS302) and similar engineering curriculum subjects.

## 🎯 Target Goal & Output Scope
- **Depth Target**: Each 16-mark long answer must provide enough rigorous, elaborate content to fill **4 to 5 handwritten exam pages** (approximately 200–300 lines of detailed markdown per question).
- **Tone & Rigor**: Highly academic, authoritative, detailed, and technically precise (following standard textbooks: Behrouz A. Forouzan, William Stallings, Andrew S. Tanenbaum, Kurose & Ross).
- **No Brief Summaries**: Avoid bulleted one-liners or high-level summaries for essay questions. Always elaborate underlying principles, step-by-step algorithms, packet header bit fields, edge cases, failure states, and real-world implementations.

---

## 📋 Mandatory Sectional Blueprint per Long Question

Every question MUST be structured with the following core components:

1. **Foundational Introduction & Motivation**:
   - Historical context, design rationale, and why the concept exists.
   - Formal definitions and core objectives.
2. **Architectural & Operational Diagrams (Mermaid)**:
   - Provide **at least 2 to 5 dedicated Mermaid diagrams** per question.
   - Use only strictly supported types: `flowchart TD`, `flowchart LR`, `sequenceDiagram`, `stateDiagram-v2`.
   - Quote node labels containing spaces, parentheses, or brackets (`id["Label (Extra)"]`).
   - Never use unsupported diagram types like `gantt`.
3. **Deep Structural Breakdown**:
   - Detailed subsections for every sub-technique, layer, class, or sub-protocol.
   - ASCII bit-level header formats for protocols (e.g., IPv4, TCP, UDP, OSPF, RIP) with bit-by-bit field explanations.
4. **Mathematical Formulations & Numerical Examples**:
   - Formal equations using LaTeX markdown ($\text{Delay}$, $\text{Capacity}$, subnet masks, link metrics, probability).
   - Step-by-step numerical examples (e.g., routing metric calculations, distance vector routing table iterations, CIDR subnetting, MTU fragmentation offsets).
5. **Step-by-Step Algorithmic Workflows**:
   - Sequential execution steps, state machines, pseudo-code, and exchange sequences.
6. **Exhaustive Multi-Parameter Comparison Matrices**:
   - Tables with **8 to 15 parameters** comparing competing protocols, algorithms, or classes.
7. **Strengths, Limitations, Vulnerabilities & Real-World Deployments**:
   - Trade-offs, loop vulnerabilities (e.g., Count-to-Infinity in Distance Vector), mitigation strategies (Split Horizon, Poison Reverse), and industry use-cases.

---

## 📂 File Placement Convention
- Short questions and answers: `UNIT - X/short_questions_answers.md`
- Long 16-mark questions and answers: `UNIT - X/long_questions_answers.md`
