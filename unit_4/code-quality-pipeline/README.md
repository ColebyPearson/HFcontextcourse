# Code Quality Pipeline — Unit 4 hands-on

A multi-agent **research → implement → verify** workflow for Claude Code,
per the Context Course Unit 4 `hands-on.mdx`.

## What's here

```
code-quality-pipeline/
├── .claude/
│   ├── CLAUDE.md                       # project-level workflow policy
│   └── agents/
│       ├── researcher.md               # Read/Grep/Glob (read-only)
│       ├── implementer.md              # Read/Write/Edit/Glob/Bash
│       ├── security-reviewer.md        # Read/Grep (read-only)
│       └── performance-reviewer.md     # Read/Grep (read-only)
├── main.py                              # placeholder for the agents to act on
└── README.md
```

`.claude/agents/*.md` are **per-project sub-agent definitions**: each has a
YAML frontmatter with `name`, `description`, `tools` (the narrow tool set
that sub-agent is allowed to use), and `model`, followed by a system-prompt
body that pins the sub-agent's role.

`.claude/CLAUDE.md` is the project-level policy file. It tells the main
Claude Code session: *for feature work, run researcher → implementer →
{security-reviewer, performance-reviewer in parallel}, then report.*

## Patterns used

- **Pipeline** for stages 1 → 2 → 3 (output of one stage feeds the next).
- **Fan-out/fan-in** at stage 3 (the two reviewers run in parallel; parent
  aggregates findings).

The implementer is the only sub-agent with write access. Making the
reviewers read-only is both a safety boundary and what lets them run in
parallel without merge conflicts.

## Try it

In this project directory, start `claude`. Then prompt:

> *"Add OAuth2 authentication. Use the researcher sub-agent first to map our
> current auth system. Then have the implementer write the integration based
> on its brief. Finally, have security-reviewer and performance-reviewer
> review the result in parallel and report before we merge."*

Claude Code reads `CLAUDE.md`, sees the four sub-agent files in
`.claude/agents/`, and follows the workflow.

## When not to use sub-agents

(From `unit4/patterns.mdx`, summarised in `CLAUDE.md`.) Skip sub-agents for:

- Sequential tightly-coupled work — one agent is faster.
- Same-file parallel edits — split by file or run serial.
- Tiny tasks — sub-agent spin-up beats the work.
- Too many specialists — group them.
