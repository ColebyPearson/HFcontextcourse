# Nano Harness — Unit 6 hands-on (bonus)

Minimal agent loop from the Context Course's bonus unit, extended with the
two network tools from `hands-on.mdx` (Extension 1 + 2) **and** the three
"Extend Further" exercise tools (`git_log`, `json_parse`, `compute_stats`)
folded in so it's a single working file.

## What it does

```
LLM call  ->  parse ```python``` block  ->  exec() with restricted globals
                                            (only our tool functions + json,
                                            __builtins__ = {})
        ->  observe stdout / stderr / structured error
        ->  feed observation back as the next user turn
        ->  repeat (up to MAX_STEPS)
```

Memory is the flat message history. Termination is whichever comes first:
`final_answer(...)` or `MAX_STEPS` (50). All safety lives at the **tool
boundary** — there is no separate sandbox.

## Tools

| Tool | What it does | Safety mechanism |
|------|--------------|------------------|
| `list_dir(path='.')` | List files | `safe_path` rejects anything that resolves outside the workspace |
| `read_file(path, max_chars=4000)` | Read text file | `safe_path` + `min(max_chars, MAX_CHARS)` cap |
| `write_file(path, content)` | Create/overwrite | `safe_path` + **gated by `ALLOW_WRITE=False`** |
| `exec_cmd(args)` | Run shell command | `args[0]` must be in `ALLOW_COMMANDS`; `subprocess` timeout |
| `web_fetch(url, max_bytes=10000)` | HTTP GET | Byte cap, timeout, errors returned as strings |
| `hf_search(query, …)` | Search HF Hub | `HF_TOKEN` required; `limit` cap |
| `git_log(limit=10)` | Recent commits | Routes through `exec_cmd` (allowlist) |
| `json_parse(text)` | Safe JSON parse | Errors returned as strings, never raised |
| `compute_stats(numbers)` | min/max/mean/count | Pure function |
| `final_answer(value)` | Terminate the loop | — |

## Run

```bash
pip install -r requirements.txt
export HF_TOKEN="hf_..."                # Inference Providers token
export NANO_MODEL="zai-org/GLM-5.1"     # any HF model on Inference Providers
export NANO_TASK="Find the README of huggingface/transformers."
python nano_harness.py
```

The Hugging Face router (`https://router.huggingface.co/v1`) is OpenAI-API-
compatible, so the same loop runs unchanged against any HF Inference-
Providers-enabled model. Flip `NANO_MODEL` and re-run.

## Why it's structured this way

- **Output Python, not JSON tool calls.** Python is precise where free-form
  JSON is ambiguous; the model writes intent directly as code.
- **`__builtins__ = {}` in `exec_globals`** removes the Python standard
  library from the model's reach. It can only call the names we explicitly
  expose.
- **`safe_path()` resolves first, then validates** against the workspace
  root — that's what makes `../etc/passwd` safe; the resolved absolute path
  is checked with `.relative_to(ws)`.
- **`ALLOW_COMMANDS` is an allowlist, not a denylist.** Anything not on the
  list raises `PermissionError`, which the agent reads as an observation
  and adapts.
- **Errors are observations, not crashes.** Every exception becomes a
  string that goes back into the message history; the model adjusts on the
  next turn.
- **`MAX_STEPS=50` and `MAX_CHARS=8000`** bound runtime and context growth.

## Caveats called out in the course

This is a **teaching** loop. Production agents add: short-term scratchpad
memory, semantic / episodic memory, retrieval-augmented context, compaction
to summarise older turns, structured note-taking, and file-system-mediated
context. The nano harness only demonstrates the minimal shape.
