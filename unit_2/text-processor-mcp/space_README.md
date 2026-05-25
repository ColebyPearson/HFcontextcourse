---
title: Text Processor MCP
emoji: 📝
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.32.0
python_version: "3.12"
app_file: app.py
pinned: false
---

# Text Processor — MCP Server

Unit 2 hands-on for the [HuggingFace Context Course](https://huggingface.co/learn/context-course/unit2/).

A Gradio UI that doubles as an MCP server: the human-facing tabs and the
`/gradio_api/mcp/` endpoint expose the same three tools.

- **analyze_text** — character / word / sentence statistics
- **extract_keywords** — top-N keywords by frequency (stopwords removed)
- **check_reading_level** — Flesch-Kincaid-style grade + coarse label

Source: <https://github.com/ColebyPearson/HFcontextcourse/tree/main/unit_2/text-processor-mcp>
