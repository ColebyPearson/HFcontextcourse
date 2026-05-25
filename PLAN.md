# Plan: Complete the Context Course (Fundamentals → Engineering Cert)

## Progress Tracker

**Overall: 1/7 units fully done (Unit 0). Unit 1 hands-on built; 2 quizzes pending on the HF site.**

| Done | Unit | Topic | Has hands-on? | Has quizzes? |
|:----:|------|-------|:-------------:|:------------:|
| ✅ | 0 | Onboarding | — | — |
| 🟡 | 1 | Skills (built `huggingface-model-publish` skill in `unit_1/`) | — | quiz1, quiz2 (pending) |
| ☐ | 2 | MCP | ✅ build + deploy MCP server | quiz1, quiz2 |
| ☐ | 3 | Plugins | — | quiz1, quiz2 |
| ☐ | 4 | Sub-agents | ✅ multi-agent workflow | quiz1, quiz2 |
| ☐ | 5 | Hooks | ✅ activity dashboard (Gradio) | quiz1, quiz2 |
| ☐ | 6 | Nano Harness (bonus) | ✅ extend the harness | quiz1 |

**Certs**
- **Context Fundamentals** = Unit 1 + Unit 2 quizzes ≥ 70%.
- **Context Engineering** = Unit 1–5 quizzes ≥ 70% + capstone project.

---

## Workflow per unit

1. **Read** the official chapters online or via the `notebooklm/unit_N.txt` companion file (audio overviews + flashcards via NotebookLM).
2. **Do** the hands-on project under `unit_N/` (this repo) — the source artifact (skill / MCP server / plugin / sub-agent / hook / harness extension) lives in that folder.
3. **Take the quizzes** on the HF course site — score ≥ 70% to count toward certification.
4. **Mark done** in the tracker above and update the unit's local README with the result.

---

## Recommended order

Units 0 → 1 → 2 are the spine for the **Context Fundamentals** cert. After Unit 2, the order is flexible (3, 4, 5 stand alone). Unit 6 is bonus.

### Unit 0 — Welcome & Onboarding
- Confirm Claude Code is installed and authenticated; create an HF account if needed.
- Skim the unit text for vocabulary.

### Unit 1 — Skills
- Read `what-are-skills`, `skill-format`, `using-skills`, `building-skills`.
- **Build a first skill** (e.g., one tied to a workflow already in `C:\Repos`).
- Pass quiz1 and quiz2 on the HF site.

### Unit 2 — MCP (cert-critical)
- Read `key-concepts`, `building-servers`, `mcp-clients`, `gradio-mcp`.
- **Hands-on**: build + deploy an MCP server (per `hands-on.mdx`). The `mcp_audio_toolkit` server in `C:\Repos\HF Audio\HF Audio` is a real existing artifact and may be a strong basis — confirm course-specific requirements before reusing.
- Pass quiz1 and quiz2 → unlocks **Context Fundamentals**.

### Unit 3 — Plugins
- Read `anatomy`, `building-plugins`, `using-plugins`.
- Build a plugin that bundles one of the existing skills + an MCP server.
- Pass quiz1 and quiz2.

### Unit 4 — Sub-agents
- Read `patterns`, `using-subagents`.
- **Hands-on**: multi-agent workflow.
- Pass quiz1 and quiz2.

### Unit 5 — Hooks
- Read `hook-events`.
- **Hands-on**: Gradio activity dashboard.
- Pass quiz1 and quiz2.

### Capstone
- Project will be announced in the course live stream. Tracking via the [Context Course HF org](https://huggingface.co/organizations/context-course).

### Unit 6 (bonus)
- Read `agent-loop`, `tools-and-sandboxing`.
- **Hands-on**: extend Nano Harness with a custom tool (anthropic SDK).
- Quiz.

---

## Verification

After each quiz, the HF course page records your score on your profile. Track the cert state at:
- Context Fundamentals: visible on your HF profile once Unit 1 + 2 quizzes pass.
- Context Engineering: same, plus the capstone submission flow.
