#!/usr/bin/env python3
"""Unit 6 — Extended Nano Harness.

Implements the agent loop from `agent-loop.mdx`:
  call LLM -> parse Python code -> exec() with restricted globals
  -> observe stdout/stderr/error -> repeat (up to MAX_STEPS)

Tools follow the course's `hands-on.mdx` "Extend Further" section:
  Base:       list_dir, read_file, write_file, exec_cmd, final_answer
  Network:    web_fetch, hf_search
  Exercises:  git_log, json_parse, compute_stats

Safety lives at the tool boundary: workspace path confinement, command
allowlist, output size limits, write gate, explicit timeouts, and
exec() with __builtins__={} so the model can only call tools we expose.

Run:  HF_TOKEN=hf_... NANO_MODEL=zai-org/GLM-5.1 python nano_harness.py
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from openai import OpenAI


# ---------- configuration -------------------------------------------------
TASK = os.getenv(
    "NANO_TASK",
    "Search for bert models on Hugging Face and summarize the top 3.",
)
MODEL = os.getenv("NANO_MODEL", "zai-org/GLM-5.1")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY", "")
WORKSPACE = str(Path.cwd())
MAX_STEPS = 50
TIMEOUT_S = 30
MAX_CHARS = 8000
ALLOW_WRITE = False
ALLOW_COMMANDS = ["ls", "cat", "pwd", "echo", "head", "tail", "wc", "rg", "git"]
TEMPERATURE = 0.2


SYSTEM_PROMPT = f"""You are a code-first agent.
Reply with executable Python only — no prose, no markdown outside of one
```python``` code block per turn.

Tools:
  - list_dir(path='.') -> list files in path (workspace-confined)
  - read_file(path, max_chars=4000) -> read file (size-capped)
  - write_file(path, content) -> write file (ALLOW_WRITE={ALLOW_WRITE})
  - exec_cmd(args) -> run an allowed shell command
  - web_fetch(url, max_bytes=10000) -> fetch a URL (size+timeout-capped)
  - hf_search(query, resource_type='models', limit=5) -> search HF Hub
  - git_log(limit=10) -> recent git commits
  - json_parse(text) -> parse JSON safely
  - compute_stats(numbers) -> {{min,max,mean,count}}
  - final_answer(value) -> signal completion

Allowed commands: {ALLOW_COMMANDS}
Workspace: {WORKSPACE}
Max chars per observation: {MAX_CHARS}

When done, call final_answer(result). Output only one Python code block."""


def clip(value, n: int = MAX_CHARS) -> str:
    s = str(value)
    return s[:n] + "\n...[truncated]" if len(s) > n else s


def main():
    ws = Path(WORKSPACE).resolve()
    done = False
    final_result = None

    # --- tool implementations (each enforces its own safety) --------------
    def safe_path(path: str) -> Path:
        p = (ws / path).resolve()
        try:
            p.relative_to(ws)
        except ValueError as e:
            raise ValueError(f"Path escapes workspace: {path}") from e
        return p

    def list_dir(path: str = "."):
        p = safe_path(path)
        if not p.is_dir():
            raise NotADirectoryError(str(p))
        return sorted(x.name + ("/" if x.is_dir() else "") for x in p.iterdir())

    def read_file(path: str, max_chars: int = 4000) -> str:
        p = safe_path(path)
        return clip(p.read_text(errors="replace"), min(max_chars, MAX_CHARS))

    def write_file(path: str, content: str) -> str:
        if not ALLOW_WRITE:
            raise PermissionError("write_file disabled")
        p = safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(str(content), encoding="utf-8")
        return f"Wrote {len(str(content))} bytes to {p}"

    def exec_cmd(args: list[str]) -> str:
        if not args or args[0] not in ALLOW_COMMANDS:
            raise PermissionError(
                f"Command {args[0] if args else '<empty>'} not allowed"
            )
        result = subprocess.run(
            args, capture_output=True, timeout=TIMEOUT_S, text=True, cwd=str(ws)
        )
        parts = []
        if result.stdout:
            parts.append(f"stdout:\n{result.stdout}")
        if result.stderr:
            parts.append(f"stderr:\n{result.stderr}")
        out = "\n\n".join(parts) or f"(exit code {result.returncode} with no output)"
        return clip(out)

    def web_fetch(url: str, max_bytes: int = 10000) -> str:
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT_S) as r:
                content = r.read(max_bytes + 1)
                if len(content) > max_bytes:
                    content = content[:max_bytes] + b"\n...[truncated]"
                return content.decode("utf-8", errors="replace")
        except urllib.error.URLError as e:
            return f"Error: Failed to fetch {url}: {e}"
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"

    def hf_search(query: str, resource_type: str = "models", limit: int = 5):
        if not API_KEY:
            return "Error: HF_TOKEN not set. Can't access Hugging Face API."
        try:
            url = f"https://huggingface.co/api/{resource_type}"
            req = urllib.request.Request(
                f"{url}?search={query}&limit={limit}",
                headers={"Authorization": f"Bearer {API_KEY}"},
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                data = json.loads(r.read())
                return [
                    {
                        "id": item.get("id"),
                        "downloads": item.get("downloads", 0),
                        "description": (item.get("description") or "")[:200],
                    }
                    for item in data[:limit]
                ]
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"

    def git_log(limit: int = 10) -> str:
        """Recent git commits — uses the allow-listed `git` command."""
        return exec_cmd(["git", "log", "--oneline", f"-{int(limit)}"])

    def json_parse(text: str):
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            return f"Error: JSONDecodeError: {e}"

    def compute_stats(numbers):
        nums = [float(x) for x in numbers]
        if not nums:
            return {"error": "empty input"}
        return {
            "min": min(nums),
            "max": max(nums),
            "mean": sum(nums) / len(nums),
            "count": len(nums),
        }

    def final_answer(value):
        nonlocal done, final_result
        done = True
        final_result = value
        return value

    # --- LLM client + message history ------------------------------------
    if not API_KEY:
        raise SystemExit(
            "Set HF_TOKEN (or OPENAI_API_KEY) before running this harness."
        )
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": TASK},
    ]

    # --- the loop ---------------------------------------------------------
    for step in range(MAX_STEPS):
        print(f"\n[Step {step + 1}]")

        response = client.responses.create(
            model=MODEL, temperature=TEMPERATURE, input=messages
        )
        content = response.output_text
        print(f"Model:\n{content[:300]}{'...' if len(content) > 300 else ''}")
        messages.append({"role": "assistant", "content": content})

        try:
            m = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
            if not m:
                raise ValueError("No ```python``` code block found")

            stdout_buffer, stderr_buffer = io.StringIO(), io.StringIO()
            exec_globals = {
                "__builtins__": {},  # restricted: only our tools + json
                "list_dir": list_dir,
                "read_file": read_file,
                "write_file": write_file,
                "exec_cmd": exec_cmd,
                "web_fetch": web_fetch,
                "hf_search": hf_search,
                "git_log": git_log,
                "json_parse": json_parse,
                "compute_stats": compute_stats,
                "final_answer": final_answer,
                "json": json,
            }
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exec(m.group(1), exec_globals)

            stdout_text = stdout_buffer.getvalue().strip()
            stderr_text = stderr_buffer.getvalue().strip()

            if done:
                result = f"Final answer: {clip(final_result)}"
            else:
                obs = []
                if stdout_text:
                    obs.append(f"stdout:\n{clip(stdout_text)}")
                if stderr_text:
                    obs.append(f"stderr:\n{clip(stderr_text)}")
                result = "\n\n".join(obs) or "Executed successfully (no output)"
        except FileNotFoundError as e:
            result = f"Error: FileNotFoundError: {e}"
        except PermissionError as e:
            result = f"Error: PermissionError: {e}"
        except subprocess.TimeoutExpired:
            result = "Error: TimeoutError: Command took too long"
        except Exception as e:
            result = f"Error: {type(e).__name__}: {str(e)}"

        if done:
            print(f"\n✓ Task complete: {final_result}")
            break

        messages.append({"role": "user", "content": result})
    else:
        print(f"\n✗ Max steps ({MAX_STEPS}) reached without final_answer()")


if __name__ == "__main__":
    main()
