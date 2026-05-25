# Unit 2 — Practice Quiz

Self-study set drawn from the six Unit 2 chapters (`introduction`, `key-concepts`,
`building-servers`, `mcp-clients`, `gradio-mcp`, `hands-on`). Q1–Q7 mirror the
territory of **Quiz 1: MCP Fundamentals**; Q8–Q15 mirror **Quiz 2: MCP in Practice**.

> Phrasing on the HF site will differ. Don't memorise — make sure you can
> explain *why* the right answer is right. If you score < 12/15, re-skim the
> chapter the missed question came from before taking the real quiz.

---

## Quiz 1 territory — MCP Fundamentals

**1.** Without a standard protocol, integrating **N** code agents with **M** external data sources requires:
- a) `N + M` custom integrations
- b) `N × M` custom integrations
- c) `max(N, M)` custom integrations
- d) Zero — agents call APIs directly

**2.** Which of the following is **NOT** one of the three MCP roles?
- a) Host
- b) Client
- c) Server
- d) Proxy

**3.** Of the three MCP capability types, which is **model-controlled** (the agent decides whether to invoke it at runtime)?
- a) Tools
- b) Resources
- c) Prompts
- d) All three are model-controlled

**4.** Which statement about **resources** is correct?
- a) They mutate server state when invoked.
- b) They're identified by a URI, are read-only, and are application-controlled (the host decides what to expose).
- c) They have the same control model as tools but a different transport.
- d) They require parameters in the same way tools do.

**5.** MCP messages are encoded using:
- a) REST over JSON
- b) gRPC / Protobuf
- c) JSON-RPC 2.0
- d) GraphQL

**6.** Which best describes the trade-off between **stdio** and **streamable HTTP** transports?
- a) Stdio is faster but only for remote servers; HTTP is local-only.
- b) Stdio runs the server as a local subprocess via stdin/stdout (no network); HTTP carries the same JSON-RPC over the network for remote/cloud servers.
- c) Stdio is encrypted by default; HTTP is plaintext.
- d) Stdio uses XML; HTTP uses JSON.

**7.** In the MCP wire protocol, the method name a client uses to invoke a tool is:
- a) `call_tool`
- b) `tools.invoke`
- c) `tools/run`
- d) `tools/call`

---

## Quiz 2 territory — MCP in Practice

**8.** The recommended install command for FastMCP **plus** the `mcp dev` inspector CLI is:
- a) `pip install fastmcp`
- b) `pip install mcp-cli`
- c) `pip install "mcp[cli]"`
- d) `npm install -g @modelcontextprotocol/server`

**9.** With FastMCP, the JSON schema for a tool's input parameters is generated from:
- a) An explicit `schema=` argument on `@mcp.tool()`
- b) A separate `tool.json` file alongside the script
- c) The function's type hints, plus the `Args:` section of the docstring
- d) FastMCP doesn't generate schemas; clients infer them at runtime

**10.** To open the **MCP Inspector** in a browser, connected to your local `server.py`:
- a) `python -m mcp.inspect server.py`
- b) `mcp dev server.py`
- c) `mcp test server.py`
- d) Open the file in VS Code; the Inspector is an extension

**11.** Calling `demo.launch(mcp_server=True)` in a Gradio app exposes the MCP endpoint at:
- a) `http://localhost:7860/mcp`
- b) `http://localhost:7860/gradio_api/mcp/`
- c) `http://localhost:7860/api/v1/mcp`
- d) `http://localhost:7860/.well-known/mcp`

**12.** Gradio's `auth` argument on `launch()`:
- a) Protects both the web UI and the MCP endpoint with HTTP basic auth
- b) Protects only the MCP endpoint; the UI stays open
- c) Protects only the web UI; the MCP endpoint at `/gradio_api/mcp/` remains reachable without auth
- d) Has no effect when `mcp_server=True`

**13.** Claude Code's `--scope user` means the MCP server you're adding is:
- a) Visible only inside the current `claude` session
- b) Available across all your projects (stored in `~/.claude.json`)
- c) Shared with your team via the project's `.mcp.json`
- d) Sandboxed to a single Python virtual environment

**14.** To expose a function as an MCP tool **but** hide it from the Gradio web UI:
- a) Set `visible=False` on the Gradio component
- b) Wrap it in `@gr.api()` and don't bind it to any UI widget
- c) Move it to a separate `server.py` and run two processes
- d) Set `mcp_only=True` on `demo.launch()`

**15.** A Gradio function fails to appear as an MCP tool. Most likely cause:
- a) Gradio version is too new
- b) The function is missing type hints, a docstring, an `Args:` section, or a return-type annotation
- c) The Space isn't deployed yet
- d) `mcp_server=True` is set explicitly (you should let Gradio auto-detect)

---

## Answers

### Quiz 1 territory

1. **b** — `N × M`. Each agent ↔ each data source needs custom glue, which is precisely why MCP exists.
2. **d** — There is no "proxy" role in the MCP architecture. The three are **host** (the agent environment), **client** (the protocol handler inside the host), and **server** (the external program exposing capabilities).
3. **a** — Tools are **model-controlled** (the agent decides when to call them). Resources are **application-controlled** (the host decides what's exposed). Prompts are **user-controlled** (deployed and updated independently).
4. **b** — Resources are read-only, URI-addressed, and application-controlled. They're "always available" without being called; tools are different because the agent must explicitly invoke them.
5. **c** — JSON-RPC 2.0 is the wire format. It's transport-agnostic; the same messages travel over stdio or streamable HTTP.
6. **b** — Stdio = local subprocess, no network exposure (fastest, most secure, dev-friendly). Streamable HTTP = remote across the internet, supports auth headers — the standard for cloud-deployed servers.
7. **d** — `tools/call`. Other defined methods include `tools/list`, `resources/list`, `resources/read`, and `prompts/get`.

### Quiz 2 territory

8. **c** — `pip install "mcp[cli]"`. The `mcp` package includes FastMCP; the `[cli]` extra adds the `mcp dev` command used by the Inspector.
9. **c** — FastMCP infers the schema automatically: parameter types from type hints, parameter descriptions from the `Args:` section of the docstring, and the tool description from the first line of the docstring.
10. **b** — `mcp dev server.py` (provided by the `mcp[cli]` extra). Equivalent: `npx @modelcontextprotocol/inspector python server.py`.
11. **b** — `/gradio_api/mcp/`. (Note: gradio 5.32 actually serves SSE under that path at `/gradio_api/mcp/sse`; the course's `--transport http` registration snippet is outdated — see `unit_2/README.md` for the working command.)
12. **c** — `auth` protects only the **web UI** with HTTP basic auth. The MCP endpoint at `/gradio_api/mcp/` remains open by design (agents need to reach it without logging in). For real protection, put the app behind a reverse proxy or use a private Space / MCP gateway.
13. **b** — `user` scope = `~/.claude.json`, available across all your projects. `local` (default) = current project only, private. `project` = shared with the team via `.mcp.json` in the repo.
14. **b** — `@gr.api()` registers a function as an MCP tool **without** binding it to any UI widget — i.e., MCP-only.
15. **b** — Type hints + docstring with `Args:` section + return-type annotation are the contract Gradio uses to generate the MCP tool schema. Missing any of them and the function is skipped.

---

## After the real quizzes

If you score ≥ 70% on both Quiz 1 and Quiz 2, you've satisfied the **Context
Fundamentals certificate** requirement (Unit 1 + Unit 2 quizzes both passed).
Update `PLAN.md` and `unit_2/README.md` checkboxes, then move on to Unit 3 (Plugins).
