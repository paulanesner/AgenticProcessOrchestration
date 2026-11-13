# Orchestration Options Comparison for Ideation Process Example

The framework compares three distinct orchestration styles:
1. **OO1 (Autonomous):** Unconstrained runtime-decided agentic orchestration.
2. **OO2 (Agentic + Frame):** Hybrid approach using structured prompts (`process_description.md`), process framing, and standardized logging templates.
3. **OO3 (BPM-based):** Deterministic, rule-based execution using a CPEE engine.

---

## Repository Structure

```text
├── oo1/
│   └── oo1_prompt               # Prompt for autonomous agents
├── oo2/
│   ├── oo2_prompt               # Framed prompt for the hybrid agent setup
│   ├── logging_template.md      # Standardized template for process mining-friendly logging
│   └── process_description.md   # Upfront structural process description and guidelines
├── eval/
│   ├── sample_logs_*/           # Sample logs for the execution of OO1,OO2 and OO3
│   └── *.py                     # Python evaluation scripts for Exact Parity (EP) and Semantic Parity (SP)
├── tool_description             # Documentation for available tools/endpoints
└── tools.py                     # Mock/Implementation of the tools
