---
name: "analyze-text"
description: "Compute text statistics (word/character/sentence counts, vocabulary diversity, average sentence length) by calling the text-processor MCP server's analyze_text tool. Use when the user asks how long, how complex, how varied, or how dense a piece of text is."
license: "MIT"
metadata:
  version: "1.0.0"
---

# Analyze Text

Wraps the `analyze_text` tool from the `text-processor` MCP server (bundled
with this plugin) so the agent has clear guidance on when and how to use it.

## When to Use

- User asks about text statistics (word count, char count, sentence count).
- User asks about vocabulary diversity or text complexity.
- User wants to compare two pieces of writing on structural properties.

## How to Use

1. Call the MCP tool `text-processor:analyze_text` (or
   `text_processor_mcp_analyze_text` on the Gradio MCP namespace) with the
   full text as the `text` argument.
2. The tool returns JSON with:
   - `total_characters`, `characters_without_spaces`
   - `total_words`, `total_sentences`
   - `average_word_length`, `average_sentence_length`
   - `unique_words`
3. Interpret the numbers in plain language. High `unique_words / total_words`
   ratio = diverse vocabulary. Long `average_sentence_length` = dense prose.

## Example

User: *"How complex is this paragraph?"*

1. Call `analyze_text` with the paragraph.
2. Compute the lexical-diversity ratio yourself from the returned counts.
3. Reply with a 2–3 sentence summary that names specific numbers (don't just
   echo the JSON).
