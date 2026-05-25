# Unit 6 — Bonus: Nano Harness — Build Your Own Agent

Official chapter URL base: https://huggingface.co/learn/context-course/unit6/
NotebookLM source: [`notebooklm/unit_6.txt`](../notebooklm/unit_6.txt)

## Chapters (in order)

- **Introduction to Nano Harness** — https://huggingface.co/learn/context-course/unit6/introduction
- **The Agentic Loop Deep Dive** — https://huggingface.co/learn/context-course/unit6/agent-loop
- **Tools and Sandboxing in Detail** — https://huggingface.co/learn/context-course/unit6/tools-and-sandboxing
- **Hands-On: Extending Nano Harness** — https://huggingface.co/learn/context-course/unit6/hands-on
- **Quiz: Nano Harness and Agent Internals** — https://huggingface.co/learn/context-course/unit6/quiz1

## Status

- [x] Read all chapters (or listen via NotebookLM)
- [x] **Hands-on built** — [`nano-harness/`](nano-harness/) (`py_compile`-clean)
- [x] Practice quiz drafted — [`practice_quiz.md`](practice_quiz.md)
- [ ] Quiz: Nano Harness and Agent Internals (≥ 70% on the HF course site)

## The harness — `nano-harness/`

A single-file extended Nano Harness combining the base loop (`agent-loop.mdx`) with both extension tools (`hands-on.mdx` Extensions 1 and 2 — `web_fetch`, `hf_search`) **and** the three "Extend Further" exercise tools (`git_log`, `json_parse`, `compute_stats`) folded into one working script.

```
nano-harness/
├── nano_harness.py             # the loop + 10 tools + restricted exec()
├── requirements.txt            # openai>=1.0.0 (HF Inference Providers via /v1)
└── README.md
```

The loop is the one from `agent-loop.mdx`:

```
LLM call -> parse ```python``` block -> exec() with __builtins__={}
        -> observe stdout/stderr/error -> repeat (<= MAX_STEPS)
```

Safety lives **only at the tool boundary**:

- `safe_path()` resolves first, then `.relative_to(workspace)` rejects anything that escapes.
- `ALLOW_COMMANDS` allow-list; unknown commands → `PermissionError` → observation → adapt.
- `ALLOW_WRITE = False` gates `write_file`.
- Per-tool size caps (`MAX_CHARS`, `max_bytes`) keep one rogue observation from blowing the context window.
- `MAX_STEPS = 50` is the hard termination guarantee.
- All exceptions become structured `"Error: <Type>: <msg>"` strings the model reads on the next turn.

The model is told via the system prompt about every tool and constraint (workspace path, allow-list, char cap, `final_answer` termination signal).

## Run

```bash
pip install -r nano-harness/requirements.txt
export HF_TOKEN="hf_..."                  # Inference Providers token
export NANO_MODEL="zai-org/GLM-5.1"       # any IP-enabled HF model
export NANO_TASK="Find the README of huggingface/transformers."
python nano-harness/nano_harness.py
```

The OpenAI router is OpenAI-API-compatible (`/v1`), so the same loop runs unchanged against any HF model with Inference Providers turned on — only `NANO_MODEL` changes.

## Why this is the bonus unit

Unit 6 is **not required** for either certificate. It's a from-first-principles exercise in how the agents we've used so far actually work under the hood — the message-history-as-memory pattern, restricted `exec()`, allow-listed tools, errors-as-observations. Worth doing if you want a strong agent-internals story (Research Engineer roles, FDE interviews).
