---
name: "check-reading-level"
description: "Estimate the reading difficulty / grade level of a piece of text via a Flesch-Kincaid-style score, by calling the text-processor MCP server's check_reading_level tool. Use when the user asks if writing is appropriate for an audience, what grade level it reads at, or whether it needs simplification."
license: "MIT"
metadata:
  version: "1.0.0"
---

# Check Reading Level

Wraps the `check_reading_level` tool from the `text-processor` MCP server.

## When to Use

- User asks about reading level, grade level, text difficulty, or audience fit.
- User wants to know if documentation/marketing/legal text is over-complex.
- User wants to compare two drafts on accessibility.

## How to Use

1. Call `text-processor:check_reading_level` with the full `text`.
2. The tool returns JSON:
   - `grade_level` — numeric Flesch-Kincaid-style grade (0 to ~16+).
   - `reading_level` — one of `Elementary School`, `Middle School`,
     `High School`, `College/Academic`.
3. Compare the grade to the user's stated target audience. If too high,
   suggest one or two concrete simplifications (shorter sentences, simpler
   words for the longest sentences) rather than a generic "make it simpler."

## Example

User: *"Is this documentation appropriate for beginners?"*

1. Call `check_reading_level`.
2. If grade > 10 and target is beginners, name the gap explicitly and point
   at 1–2 of the longest sentences as starting points for cuts.
