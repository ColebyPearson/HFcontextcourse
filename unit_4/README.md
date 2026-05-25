# Unit 4 — Subagents: Orchestrating Multi-Agent Workflows

Official chapter URL base: https://huggingface.co/learn/context-course/unit4/
NotebookLM source: [`notebooklm/unit_4.txt`](../notebooklm/unit_4.txt)

## Chapters (in order)

- **Unit 4: Subagents** — https://huggingface.co/learn/context-course/unit4/introduction
- **Subagent Patterns** — https://huggingface.co/learn/context-course/unit4/patterns
- **Using Subagents** — https://huggingface.co/learn/context-course/unit4/using-subagents
- **Quiz 1: Subagent Concepts** — https://huggingface.co/learn/context-course/unit4/quiz1
- **Hands-On: Multi-Agent Workflow** — https://huggingface.co/learn/context-course/unit4/hands-on
- **Quiz 2: Multi-Agent Workflows** — https://huggingface.co/learn/context-course/unit4/quiz2

## Status

- [x] Read all chapters (or listen via NotebookLM)
- [x] **Hands-on built** — [`code-quality-pipeline/`](code-quality-pipeline/)
- [x] Practice quiz drafted — [`practice_quiz.md`](practice_quiz.md)
- [ ] Quiz 1: Subagent Concepts (≥ 70% on the HF course site)
- [ ] Quiz 2: Multi-Agent Workflows (≥ 70% on the HF course site)

## The pipeline — `code-quality-pipeline/`

A research → implement → verify Claude Code project with four narrow sub-agents:

```
code-quality-pipeline/
├── .claude/
│   ├── CLAUDE.md                       # workflow policy: when to spawn each agent
│   └── agents/
│       ├── researcher.md               # Read / Grep / Glob              (read-only)
│       ├── implementer.md              # Read / Write / Edit / Glob / Bash
│       ├── security-reviewer.md        # Read / Grep                     (read-only)
│       └── performance-reviewer.md     # Read / Grep                     (read-only)
├── main.py                              # placeholder for the agents to act on
└── README.md
```

Patterns used (per `unit4/patterns.mdx`):
- **Pipeline** for stages 1 → 2 → 3 (researcher → implementer → reviewers).
- **Fan-out/fan-in** at stage 3 — security and performance reviewers run in parallel, parent aggregates.

The implementer is the only sub-agent with write access. The reviewers are read-only by design, which is both a safety boundary and what makes it safe to run them in parallel.

## Try it

In the `code-quality-pipeline/` directory, start `claude`. Then prompt the example from `hands-on.mdx`:

> *"Add OAuth2 authentication. Use the researcher sub-agent first to map our current auth system. Then have the implementer write the integration. Finally have security-reviewer and performance-reviewer review the result in parallel and report before we merge."*

Claude Code reads `.claude/CLAUDE.md`, sees the four sub-agent files, and follows the workflow.
