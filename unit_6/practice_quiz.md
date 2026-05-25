# Unit 6 — Practice Quiz (Bonus: Nano Harness)

Drawn from `introduction`, `agent-loop`, `tools-and-sandboxing`, `hands-on`.
Unit 6 has a **single** quiz on the HF site ("Quiz: Nano Harness and Agent
Internals"), so this practice set is one continuous block of 12 questions.

> Phrasing on the HF site will differ. ≥ 10/12 = comfortable margin.

---

**1.** The Nano Harness loop, in one sentence, is:
- a) Plan → Act → Reflect → Stop
- b) Call the LLM → parse the Python code block → `exec()` with restricted globals → observe stdout/stderr/error → repeat, up to `MAX_STEPS`, until `final_answer()` is called
- c) JSON tool calls → server-side execution → return tool results
- d) Stream tokens, run shell commands as they appear

**2.** The harness asks the model to output **Python code**, not JSON tool calls. Why?
- a) Python files are smaller to transmit
- b) Python is precise where free-form JSON or English is ambiguous; the model writes intent directly as code
- c) JSON tool calls don't exist as a feature
- d) Performance — exec() is faster than json.loads

**3.** Inside `exec_globals`, `"__builtins__": {}` is set. The effect is:
- a) Faster startup
- b) The model can only call the names we explicitly expose; standard-library functions and `open()`/`__import__`/etc. are unreachable
- c) It enables typed dispatch
- d) Nothing — `__builtins__` is overridden by Python at runtime

**4.** `safe_path(path)` works by:
- a) Stripping `..` from the string before opening
- b) Resolving `(ws / path).resolve()` and then calling `.relative_to(ws)` — if the resolved absolute path doesn't live under the workspace, it raises
- c) Blocking all `..` and `/` characters in the input
- d) Using a chroot

**5.** `ALLOW_COMMANDS = ["ls", "cat", "pwd", ...]` is an **allowlist**, not a denylist. The practical consequence:
- a) Any new command must be added explicitly; unknown commands raise `PermissionError` and become observations the model adapts to
- b) Anything not in the list is silently allowed
- c) The agent can edit the list at runtime
- d) `subprocess.run` ignores it

**6.** `MAX_STEPS = 50` exists primarily to:
- a) Optimise token usage
- b) Guarantee termination — without an explicit step cap, an agent can loop indefinitely on a never-quite-done task
- c) Match the OpenAI rate limit
- d) Force the agent to think for at least 50 turns

**7.** When `exec()` raises (e.g., `FileNotFoundError`, `PermissionError`, `subprocess.TimeoutExpired`), the harness:
- a) Crashes the whole loop
- b) Catches the exception, formats it as a structured `"Error: <Type>: <msg>"` string, and feeds it back to the model as the next user turn so the agent can adapt
- c) Retries silently
- d) Returns to the user immediately

**8.** The Hugging Face router (`https://router.huggingface.co/v1`) is used because:
- a) It's the only place that hosts GLM-5.1
- b) It exposes an OpenAI-compatible `/v1` API across Inference Providers, so the same loop runs unchanged against any enabled HF model — just change `NANO_MODEL`
- c) It's cheaper than OpenAI
- d) It bypasses the system prompt

**9.** Memory in the Nano Harness is:
- a) A SQLite database
- b) A flat message history that accumulates system prompt + user task + alternating assistant/observation turns; the LLM sees the whole thing on each call
- c) A vector store
- d) Per-turn — only the previous step is visible to the model

**10.** `final_answer(value)` is necessary because:
- a) The OpenAI API requires it
- b) The harness needs an explicit signal — set via a nonlocal flag — that distinguishes "the task is complete" from "the model returned text and there are no observations"
- c) It returns the value to the user via stdout
- d) Without it the model can't produce output at all

**11.** The course explicitly calls the Nano Harness a **teaching** loop. Production agents differ by adding:
- a) GPU acceleration
- b) Things like compaction / summarisation of old context, structured scratchpads, episodic + semantic memory, retrieval-augmented context, file-system-mediated context, and richer tool selection — not just a flat history
- c) Different exit codes
- d) HTTPS

**12.** Output bounds (`MAX_CHARS`, `read_file(max_chars=4000)`, `web_fetch(max_bytes=…)`) exist mainly to:
- a) Save bandwidth
- b) Cap each tool's contribution to context, so a single overlong observation can't blow the model's window and crash the loop
- c) Speed up disk reads
- d) Make output deterministic

---

## Answers

1. **b** — That's the loop in one line; the system prompt names the constraints, `MAX_STEPS` caps the iterations, `final_answer` terminates.
2. **b** — Python is unambiguous and immediately executable; the model writes intent directly. (a/c/d are wrong.)
3. **b** — Empty `__builtins__` removes the standard library from the model's reach. It can only call names exposed in `exec_globals` (our tool functions + `json`).
4. **b** — Resolve first, then validate via `.relative_to(ws)`. String-stripping `..` is naive and unsafe (symlinks, double-encodings, etc.).
5. **a** — Allowlist semantics: unknown commands raise `PermissionError`, the agent reads the error string, and adapts on the next turn.
6. **b** — Hard step cap = guaranteed termination, independent of model behaviour.
7. **b** — Errors become observations. The agent sees the error as text and tries something else (different file, allowed command, smaller chunk, etc.).
8. **b** — OpenAI-compatible router → swap `NANO_MODEL` to any HF model with Inference Providers enabled, no other changes.
9. **b** — Flat message history. (The course flags this explicitly as a simplification vs production agents.)
10. **b** — Without an explicit termination signal, the harness can't distinguish "done" from "another step." `final_answer` flips a nonlocal `done` flag the loop checks each turn.
11. **b** — The course's own "this is a simplification" callout names compaction, scratchpads, episodic/semantic memory, retrieval, file-system-mediated context, and richer tool selection.
12. **b** — Output bounds protect context. One overlong observation can blow the window; clipping at the tool boundary keeps the message history sustainable.

---

## After the real quiz

Unit 6 is the **bonus** unit — its quiz isn't required for either certificate.
It's a strong rung for the Research Engineer story (you've built and reasoned
about a minimal agent loop from first principles).
