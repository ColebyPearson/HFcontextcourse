# Unit 5 — Practice Quiz

Drawn from `introduction`, `hook-events`, `hands-on`. Q1–Q7 mirror **Quiz 1:
Hook Fundamentals**; Q8–Q15 mirror **Quiz 2: Hooks in Practice**.

> Phrasing on the HF site will differ. ≥ 12/15 on the practice = comfortable
> margin on the real quizzes.

---

## Quiz 1 territory — Hook Fundamentals

**1.** The shared agent lifecycle the unit lays out is roughly:
- a) Start → Prompt → ToolCall → Stop → End
- b) `SessionStart` → (`UserPromptSubmit` → `PreToolUse` / `PostToolUse` → `Stop`) per turn → `SessionEnd`
- c) `Init` → `Reason` → `Act` → `Reflect` → `Shutdown`
- d) The lifecycle is platform-specific; there is no shared shape.

**2.** In **Claude Code**, hook events are configured in:
- a) `.claude/hooks.yaml`
- b) `.claude/settings.json` (or `hooks/hooks.json` inside a plugin)
- c) `~/.claude.json` only
- d) Inline in `CLAUDE.md`

**3.** Hooks are best described as:
- a) Purely observational — they can log but never alter behaviour.
- b) Required for every agent session.
- c) Both observational *and* able to influence what happens next (block a tool call, inject context, rewrite arguments, etc.).
- d) Only useful in unit tests.

**4.** "Run a linter after every code edit" maps best to which Claude Code event + matcher?
- a) `PreToolUse`, `matcher: "Read"`
- b) `PostToolUse`, `matcher: "Edit|Write"`
- c) `Stop`
- d) `SessionStart`

**5.** "Block clearly destructive shell commands before they run" maps best to:
- a) `PostToolUse` with `matcher: "Bash"`
- b) `PreToolUse` with `matcher: "Bash"`, then exit code `2` + stderr message
- c) `Stop`
- d) `SessionEnd`

**6.** Pi's hook event names follow which convention?
- a) `PascalCase` like Claude Code
- b) `camelCase`
- c) `lower_snake_case` (e.g. `tool_call`, `before_agent_start`)
- d) `kebab-case`

**7.** Which platform configures hooks **as code** (TypeScript modules) rather than via a JSON event-config file?
- a) Claude Code
- b) Codex
- c) OpenCode (plugin module exports an object whose keys are event names)
- d) None — all four use JSON.

---

## Quiz 2 territory — Hooks in Practice

**8.** A Claude Code command hook receives its payload via:
- a) JSON on **stdin** (and an environment variable for the project dir)
- b) Command-line arguments
- c) A file written to `/tmp/`
- d) An HTTP POST regardless of `type`

**9.** Exit code `0` vs `2` from a Claude Code command hook means:
- a) `0` = allow / no change; `2` = block-or-continue per event semantics (e.g. deny the tool call on `PreToolUse`) with the stderr message as the reason.
- b) `0` = error; `2` = success.
- c) Both are equivalent — the exit code is ignored.
- d) `2` always aborts the entire session.

**10.** For finer control than exit codes alone, a Claude Code hook can print to stdout:
- a) A free-form English explanation
- b) JSON with a `hookSpecificOutput` object (e.g. `{"permissionDecision":"deny","permissionDecisionReason":"…"}`) or the legacy `{"decision":"block","reason":"…"}`
- c) The next prompt for the user
- d) A new system prompt as raw text

**11.** In **OpenCode**, the equivalent of "block this tool call" is:
- a) `exit(2)` from a Bash script
- b) `throw new Error("blocked: …")` inside `"tool.execute.before"`
- c) Setting `block: true` in `opencode.json`
- d) Removing the plugin file at runtime

**12.** A `matcher` like `"Edit|Write"` on a Claude Code hook is:
- a) A SQL clause
- b) A regex matching `tool_name` for tool events (or `source` for `SessionStart`), so this hook fires for both Edit and Write tools.
- c) A glob over file paths
- d) A Python expression

**13.** In the hands-on dashboard, the FastAPI route `/event` is mounted **before** the Gradio UI because:
- a) Otherwise the Gradio app fails to load.
- b) Route order determines precedence — defining `/event` before Gradio is mounted at `/` ensures POSTs hit the receiver instead of the Gradio handler.
- c) FastAPI requires alphabetical route order.
- d) Gradio cannot serve any POST routes at all.

**14.** Why the dashboard `_normalize()` function exists:
- a) To validate JSON Schemas
- b) Claude Code / Codex / OpenCode / Pi emit payloads with different field names (`hook_event_name` vs `event`, `tool_name` vs `tool`, `tool_input` vs `args`); the normalizer collapses them to one shape so the dashboard renders consistently.
- c) To sign payloads for security
- d) Performance only — it doesn't change shape

**15.** A reasonable failure-mode protection for command hooks calling the dashboard via `curl`:
- a) Drop `curl` entirely
- b) Use `--max-time 2` and append `|| true` so a slow/offline dashboard never blocks the agent's tool execution
- c) Run the agent in a separate VM
- d) Disable the hook on every error

---

## Answers

### Quiz 1 territory

1. **b** — `SessionStart` → (`UserPromptSubmit` → `PreToolUse` / `PostToolUse` → `Stop`) per turn → `SessionEnd`. Each platform uses different vocabulary but the shape is shared.
2. **b** — `.claude/settings.json` for project-scope or `hooks/hooks.json` inside a plugin. Personal scope lives in `~/.claude/settings.json`.
3. **c** — Hooks observe **and** influence. Exit code `2`, JSON `hookSpecificOutput`, thrown errors (OpenCode), or returned `{block:true}` (Pi) all change the next step.
4. **b** — `PostToolUse` (after the edit happened) with a matcher selecting the file-mutating tools. `PreToolUse` would fire too early; `Stop` is the wrong granularity.
5. **b** — Inspect the tool input on `PreToolUse` (`matcher: "Bash"`), exit `2` with a stderr reason to deny.
6. **c** — Pi uses lower_snake_case (`session_start`, `tool_call`, etc.). Claude Code/Codex are PascalCase.
7. **c** — OpenCode plugins are TS/JS modules; hook events are object keys (`"tool.execute.before"`, etc.). No JSON event-config file.

### Quiz 2 territory

8. **a** — JSON payload on stdin; `CLAUDE_PROJECT_DIR` env var for project root. HTTP hooks get the same payload as the POST body.
9. **a** — `0` = allow; `2` + stderr = block-or-continue (event-specific semantics; e.g. on `PreToolUse` the message becomes the deny reason).
10. **b** — `hookSpecificOutput` is the structured channel; legacy `{decision, reason}` is still supported.
11. **b** — Throw an error inside `"tool.execute.before"`. There's no exit-code surface; influence is purely through code (throwing or mutating `output.args`).
12. **b** — Regex matching `tool_name`. `"Edit|Write"` fires for both tools.
13. **b** — Route order. Defining `/event` before mounting Gradio at `/` makes the POST route win.
14. **b** — Payload field names differ across the four agents; the normalizer collapses them to one shape.
15. **b** — `--max-time 2` plus `|| true` makes the logging best-effort. A hook that hangs blocks the agent's tool execution; we never want that.

---

## After the real quizzes

Passing Unit 5's two quizzes ≥ 70% completes the **Context Engineering**
cert's *quizzes* requirement (Unit 1–5). The remaining gate is the capstone
project, which is announced separately. Bonus Unit 6 has its own single quiz.
