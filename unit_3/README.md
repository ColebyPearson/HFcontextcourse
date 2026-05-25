# Unit 3 — Plugins: Bundling Tools for Distribution

Official chapter URL base: https://huggingface.co/learn/context-course/unit3/
NotebookLM source: [`notebooklm/unit_3.txt`](../notebooklm/unit_3.txt)

## Chapters (in order)

- **Unit 3: Plugins** — https://huggingface.co/learn/context-course/unit3/introduction
- **Plugin Anatomy** — https://huggingface.co/learn/context-course/unit3/anatomy
- **Building Your Own Plugin** — https://huggingface.co/learn/context-course/unit3/building-plugins
- **Quiz 1: Plugin Fundamentals** — https://huggingface.co/learn/context-course/unit3/quiz1
- **Using Plugins** — https://huggingface.co/learn/context-course/unit3/using-plugins
- **Quiz 2: Building and Distributing Plugins** — https://huggingface.co/learn/context-course/unit3/quiz2

## Status

- [x] Read all chapters (or listen via NotebookLM)
- [x] **Plugin built** — [`text-processor-plugin/`](text-processor-plugin/) + a local marketplace at [`marketplace.json`](marketplace.json)
- [x] Practice quiz drafted — [`practice_quiz.md`](practice_quiz.md)
- [ ] Quiz 1: Plugin Fundamentals (≥ 70% on the HF course site)
- [ ] Quiz 2: Building and Distributing Plugins (≥ 70% on the HF course site)

## The plugin — `text-processor-plugin/`

Packages Unit 2's deployed text-processor MCP server as a Claude Code plugin:

```
text-processor-plugin/
├── .claude-plugin/
│   └── plugin.json                # name, version, description, author
├── .mcp.json                      # SSE config -> the deployed Space (Unit 2)
├── README.md
└── skills/
    ├── analyze-text/SKILL.md
    ├── extract-keywords/SKILL.md
    └── check-reading-level/SKILL.md
```

No server code is bundled — the plugin **references** the deployed server via `.mcp.json`. Each skill teaches the agent *when* and *how* to call its corresponding tool.

## Install + test (Claude Code)

A tiny local marketplace at [`marketplace.json`](marketplace.json) makes this installable without publishing:

```text
/plugin marketplace add "C:\Repos\HF Context Course\unit_3\marketplace.json"
/plugin install text-processor-plugin@local-context-course
```

Then try:
- *"What's the reading level of: 'The mitochondria is the powerhouse of the cell. It provides energy through oxidative phosphorylation.'"*
- *"Extract the top 8 keywords from this article: …"*

After editing any plugin file, toggle the plugin off/on in `/plugin` to reload.

## Note on the `.mcp.json` URL

The course's `anatomy.mdx`/`building-plugins.mdx` example uses `"url": "https://…/gradio_api/mcp/"` (no transport, no `/sse` suffix). With gradio 5.32 that 404s. This plugin's `.mcp.json` uses `"type": "sse"` + the `/sse` URL, which actually works — same correction as Unit 2's README.
