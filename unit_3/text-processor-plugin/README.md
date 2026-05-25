# Text Processor Plugin

Unit 3 hands-on for the [HuggingFace Context Course](https://huggingface.co/learn/context-course/unit3/).
Bundles three skills + a `.mcp.json` reference to the deployed `text-processor`
MCP server from Unit 2.

## What's in the bundle

```
text-processor-plugin/
├── .claude-plugin/
│   └── plugin.json                       # Claude Code manifest
├── .mcp.json                             # references the deployed Space (SSE)
├── README.md                             # this file
└── skills/
    ├── analyze-text/SKILL.md
    ├── extract-keywords/SKILL.md
    └── check-reading-level/SKILL.md
```

- **`.claude-plugin/plugin.json`** — name, version, description, author.
- **`.mcp.json`** — points at `https://voicescoleby-text-processor-mcp.hf.space/gradio_api/mcp/sse` with `"type": "sse"` (gradio 5.32's actual transport).
- **`skills/`** — three skill wrappers (`analyze-text`, `extract-keywords`, `check-reading-level`) that teach the agent *when* and *how* to call each tool.

No server code lives here — the plugin **references** the deployed MCP server. That separation is the whole point of Unit 3: skills describe *when to use tools*, MCP servers *provide* the tools, and plugins *package the reusable behaviour* in the form each agent platform expects.

## Install + test (Claude Code)

The plugin is exposed via a tiny local marketplace file at the parent unit folder ([`unit_3/marketplace.json`](../marketplace.json)). Inside a `claude` session:

```text
/plugin marketplace add C:\Repos\HF Context Course\unit_3\marketplace.json
/plugin install text-processor-plugin@local-context-course
```

Then test conversationally — e.g.:

> *"What's the reading level of: 'The mitochondria is the powerhouse of the cell. It provides energy through oxidative phosphorylation.'"*

Or with explicit namespacing:

```text
/text-processor-plugin:check-reading-level
```

After editing any plugin file, toggle the plugin off/on via `/plugin` to reload.

## A note on the deployed-Space MCP URL

The course's `anatomy.mdx` example shows `"url": "https://…/gradio_api/mcp/"` with no `type` field. With gradio 5.32 that URL **404s** on a plain GET (the transport is SSE at `/gradio_api/mcp/sse`). This plugin's `.mcp.json` uses the working `/sse` URL and an explicit `"type": "sse"` for clarity. See `../README.md` and the Unit 2 README for the full case study.
