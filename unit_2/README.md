# Unit 2 — MCP: The Model Context Protocol

Official chapter URL base: https://huggingface.co/learn/context-course/unit2/
NotebookLM source: [`notebooklm/unit_2.txt`](../notebooklm/unit_2.txt)

## Chapters (in order)

- **Introduction to Model Context Protocol** — https://huggingface.co/learn/context-course/unit2/introduction
- **MCP Key Concepts and Architecture** — https://huggingface.co/learn/context-course/unit2/key-concepts
- **Building MCP Servers with Python** — https://huggingface.co/learn/context-course/unit2/building-servers
- **Quiz 1: MCP Fundamentals** — https://huggingface.co/learn/context-course/unit2/quiz1
- **Configuring Agents as MCP Clients** — https://huggingface.co/learn/context-course/unit2/mcp-clients
- **Gradio MCP Integration: Web UIs + MCP Servers** — https://huggingface.co/learn/context-course/unit2/gradio-mcp
- **Hands-On: Build and Deploy an MCP Server** — https://huggingface.co/learn/context-course/unit2/hands-on
- **Quiz 2: MCP in Practice** — https://huggingface.co/learn/context-course/unit2/quiz2

## Status

- [x] Read all chapters (or listen via NotebookLM)
- [x] **Hands-on project built and deployed** — [`text-processor-mcp/`](text-processor-mcp/)
- [ ] Quiz 1: MCP Fundamentals (≥ 70% on the HF course site)
- [ ] Quiz 2: MCP in Practice (≥ 70% on the HF course site)

## Hands-on — `text-processor-mcp/`

Per `hands-on.mdx`: a text-processing MCP server built in three layers, all in `text-processor-mcp/`:

1. **Stdio FastMCP server** — `server.py`. Four `@mcp.tool()` functions: `analyze_text`, `extract_keywords`, `check_reading_level`, `reverse_text`. Run with `python server.py`; inspect with `mcp dev server.py`.
2. **Gradio dual-purpose server** — `app.py`. Same three of the four functions exposed as a web UI with three tabs **and** automatically as MCP tools at `/gradio_api/mcp/` via `demo.launch(mcp_server=True)`.
3. **Deployed Space** — published as **`VoicesColeby/text-processor-mcp`** (public). The MCP endpoint is at `https://voicescoleby-text-processor-mcp.hf.space/gradio_api/mcp/`.

Validated locally: server registers all 4 tools and each call returns the expected JSON (see the validation block in the build log). Space build status visible at the Space URL.

## Register the deployed MCP server with Claude Code

The course's `hands-on.mdx` (Part 3 Step 3) prints:

```bash
# ⚠️ DOES NOT WORK with gradio 5.32 — health check returns 404
claude mcp add --transport http --scope user text-processor \
  https://voicescoleby-text-processor-mcp.hf.space/gradio_api/mcp/
```

Gradio 5.32 actually serves MCP over **SSE** at `/gradio_api/mcp/sse` (with the
POST companion at `/messages`). The bare `/gradio_api/mcp/` returns 404 to a
plain GET, and Claude Code's HTTP-transport probe fails. The schema endpoint
at `/gradio_api/mcp/schema` is the only thing that responds 200 to a GET.

The working command is `--transport sse` + the `/sse` URL:

```bash
claude mcp add --transport sse --scope user text-processor \
  https://voicescoleby-text-processor-mcp.hf.space/gradio_api/mcp/sse
```

Verify: `claude mcp list` should show `✓ Connected`.

Then restart Claude Code and try prompts like:

- *"What's the reading level of this paragraph: …"*
- *"What are the top 5 keywords in this article: …"*
- *"Analyze this text and tell me the average sentence length: …"*

The agent will connect to your Space, call the tool, and return the result.

## Bonus — related stdio-only MCP server we already had

The [`mcp_audio_toolkit`](https://github.com/ColebyPearson/HFaudio/tree/main/mcp_audio_toolkit) in the HF Audio repo is the same FastMCP pattern wrapping the four audio-course models (genre classifier, ASR, Dutch TTS, speech-to-speech). Stdio-only, no Gradio UI, no Space — built before this course covered the Gradio + Spaces pattern. The text-processor here is the on-curriculum version that practices all three layers.
