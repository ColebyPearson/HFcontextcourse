# Unit 5 — Hooks: Observing and Guarding the Agent Lifecycle

Official chapter URL base: https://huggingface.co/learn/context-course/unit5/
NotebookLM source: [`notebooklm/unit_5.txt`](../notebooklm/unit_5.txt)

## Chapters (in order)

- **Unit 5: Hooks** — https://huggingface.co/learn/context-course/unit5/introduction
- **Hook Events and the Agent Lifecycle** — https://huggingface.co/learn/context-course/unit5/hook-events
- **Quiz 1: Hook Fundamentals** — https://huggingface.co/learn/context-course/unit5/quiz1
- **Hands-On: Agent Activity Dashboard with Gradio** — https://huggingface.co/learn/context-course/unit5/hands-on
- **Quiz 2: Hooks in Practice** — https://huggingface.co/learn/context-course/unit5/quiz2

## Status

- [x] Read all chapters (or listen via NotebookLM)
- [x] **Hands-on built** — [`agent-activity-dashboard/`](agent-activity-dashboard/)
- [x] Practice quiz drafted — [`practice_quiz.md`](practice_quiz.md)
- [ ] Quiz 1: Hook Fundamentals (≥ 70% on the HF course site)
- [ ] Quiz 2: Hooks in Practice (≥ 70% on the HF course site)

## The dashboard — `agent-activity-dashboard/`

A live agent-activity dashboard following `hands-on.mdx`:

```
agent-activity-dashboard/
├── app.py                              # FastAPI + Gradio in one process
├── requirements.txt
├── .claude/settings.json               # Claude Code hooks (logger + Bash guardrail)
└── README.md
```

`app.py` mounts a FastAPI `POST /event` receiver on port 8000 and a Gradio dashboard at `/` (with `gr.Timer(1.0).tick(...)` polling the in-memory `deque(maxlen=500)`). The receiver normalizes Claude Code / Codex / OpenCode / Pi payload shapes to one `{timestamp, platform, event, tool, args}` record so the UI renders consistently regardless of source.

`.claude/settings.json` ships **two** behaviours on `PreToolUse`:
- A **guardrail**: `jq` extracts the Bash command; `grep -Eq 'rm -rf|…fork-bomb…'` denies it with `exit 2` + a stderr reason.
- A **logger** that POSTs every event to the dashboard (also on `PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart`).

Run + connect:

```bash
pip install -r agent-activity-dashboard/requirements.txt
python agent-activity-dashboard/app.py            # http://localhost:8000

# in another terminal:
cd agent-activity-dashboard && claude
> List the files in this directory, then read README.md and summarize it.
```

You'll see `SessionStart`, `UserPromptSubmit`, multiple `PreToolUse`/`PostToolUse` pairs, and a final `Stop` stream into the dashboard. The bar chart updates live.
