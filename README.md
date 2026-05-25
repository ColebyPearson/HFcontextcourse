# HuggingFace Context Course

Working through the [HuggingFace Context Course](https://huggingface.co/learn/context-course/unit0/introduction) — context engineering for AI code agents: skills, MCP, plugins, sub-agents, hooks, and a minimal agent harness.

## Course Units

| Unit | Topic | Type |
|------|-------|------|
| 0 | Welcome & Onboarding | Theory |
| 1 | Skills — Portable Knowledge | Theory + Quizzes |
| 2 | Model Context Protocol (MCP) | Theory + **Hands-on** + Quizzes |
| 3 | Plugins | Theory + Quizzes |
| 4 | Sub-agents | Theory + **Hands-on** + Quizzes |
| 5 | Hooks | Theory + **Hands-on** + Quizzes |
| 6 | Bonus: Nano Harness | Theory + **Hands-on** + Quiz |

## Certification

| Level | Requirement |
|-------|-------------|
| **Context Fundamentals** | Pass Unit 1–2 quizzes ≥ 70% |
| **Context Engineering** | Pass Unit 1–5 quizzes ≥ 70% + complete the capstone project |

## Structure

- `unit_*/` — per-unit work (hands-on project artifacts and notes land here).
- `notebooklm/unit_*.txt` — concatenated unit text from the official MDX source, formatted for [NotebookLM](https://notebooklm.google.com/) (audio overviews + flashcards).
- `_source/` — shallow clone of [`huggingface/context-course`](https://github.com/huggingface/context-course) used to build the notebooklm files. **Gitignored.**

## Setup

```bash
pip install -r requirements.txt
```

You'll also want at least one code agent installed — this repo uses **Claude Code** as the reference. See the course's Unit 0 for setup instructions.
