# Agent Activity Dashboard — Unit 5 hands-on

A live dashboard that ingests hook events from Claude Code (and Codex /
OpenCode / Pi if you wire them) and renders them as a streaming table + a
tool-usage bar chart. One Python process, two surfaces:

- **`POST /event`** — FastAPI receiver. Hooks POST here; payload is
  normalised across the four agents into `{timestamp, platform, event, tool,
  args}` and appended to an in-memory `deque(maxlen=500)`.
- **`/`** — Gradio UI polling the buffer every second.

## Files

```
agent-activity-dashboard/
├── app.py                              # FastAPI + Gradio in one process
├── requirements.txt
├── .claude/
│   └── settings.json                   # Claude Code hooks (logger + Bash guardrail)
└── README.md
```

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open <http://localhost:8000>. The page loads empty until a hook POSTs an event.

## Connect Claude Code

`.claude/settings.json` in this directory already wires every relevant
lifecycle event to the dashboard with `"X-Platform": "claude-code"`, **and**
adds a `PreToolUse` guardrail that blocks obvious destructive patterns
(`rm -rf`, classic fork-bomb) with `exit 2` before the dashboard logger
fires.

Start `claude` in this directory and try:

> *"List the files in this directory, then read README.md and summarise it."*

You'll see `SessionStart`, `UserPromptSubmit`, multiple `PreToolUse`/
`PostToolUse` pairs, and a final `Stop`. The bar chart updates live as tools
accumulate.

To exercise the guardrail:

```bash
mkdir -p /tmp/hook-guardrail-demo-delete-me
```

then ask the agent:

> *"Run `rm -rf /tmp/hook-guardrail-demo-delete-me`."*

The hook denies it with `exit 2` and the dashboard logs the (now blocked)
event with `event=PreToolUse, tool=Bash`.

## Other platforms

The Gradio receiver is platform-agnostic — the normalizer in `_normalize()`
accepts any of:
- `platform` field (or `X-Platform` header) — `claude-code`, `codex`,
  `opencode`, `pi`, `unknown`.
- `event` or `hook_event_name`.
- `tool` or `tool_name`.
- `args`, `tool_input`, or `prompt`.

Codex / OpenCode / Pi hook snippets are in the course's `unit5/hands-on.mdx`
and can be copied into this project's `.codex/hooks.json`,
`.opencode/plugins/dashboard.ts`, or `.pi/extensions/dashboard.ts` as needed.

## Deploy (optional)

Add a Space `README.md` with `sdk: gradio` and push `app.py` +
`requirements.txt`. **Before doing so**, harden:

- Hook payloads can contain secrets (prompts, file contents, command
  lines). Redact sensitive fields in `_normalize` before appending.
- Make the Space private OR put auth in front of `POST /event` (custom
  header check + token), OR you're broadcasting your agent activity to
  anyone on the internet.
- The in-memory buffer dies on Space restart. For durable history, swap
  `deque` for SQLite or a Spaces persistent volume.
