---
name: "extract-keywords"
description: "Extract the most frequent meaningful words from a piece of text by calling the text-processor MCP server's extract_keywords tool. Use when the user asks for keywords, key terms, topic extraction, or a quick content summary by frequency."
license: "MIT"
metadata:
  version: "1.0.0"
---

# Extract Keywords

Wraps the `extract_keywords` tool from the `text-processor` MCP server.

## When to Use

- User asks for keywords, key terms, top words, main topics.
- User wants a rough content summary by frequency before reading a long doc.
- User wants to compare two texts by their highest-frequency terms.

## How to Use

1. Call `text-processor:extract_keywords` with the `text` argument and an
   optional `count` argument (default 5; raise to 10–15 for richer summaries).
2. The tool returns JSON: `{"keywords": [{"word": ..., "frequency": ...}, ...]}`.
3. Group obviously-related keywords into themes when you present them — the
   tool returns frequencies, not themes; that's your job.

## Example

User: *"What are the main topics in this article?"*

1. Call `extract_keywords` with `count=10`.
2. Group the 10 keywords into 2–4 themes.
3. Present each theme with its supporting keywords and frequencies.
