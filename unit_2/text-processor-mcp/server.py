"""Text-processor MCP server (stdio).

Unit 2 hands-on of the Hugging Face Context Course. Exposes four tools to any
MCP-compatible code agent (Claude Code, Codex, OpenCode, Pi):
  - analyze_text(text)             -> JSON text statistics
  - extract_keywords(text, count)  -> JSON top-N keywords by frequency
  - check_reading_level(text)      -> JSON Flesch-Kincaid grade + label
  - reverse_text(text)             -> reversed string

Run:  python server.py        (stdio transport — what MCP clients connect to)
Dev:  mcp dev server.py       (launches the MCP Inspector in the browser)
"""
from __future__ import annotations

import json
from collections import Counter

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("text-processor")

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "by", "from",
}


@mcp.tool()
def analyze_text(text: str) -> str:
    """Analyze text and return statistics.

    Args:
        text: The input text to analyze.

    Returns:
        JSON string with character, word, sentence, and uniqueness stats.
    """
    words = text.split()
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    sentences = max(text.count(".") + text.count("!") + text.count("?"), 1)
    avg_word_length = round(chars_no_spaces / len(words), 2) if words else 0
    avg_sentence_length = round(len(words) / sentences, 2) if words else 0
    return json.dumps({
        "total_characters": chars,
        "characters_without_spaces": chars_no_spaces,
        "total_words": len(words),
        "total_sentences": sentences,
        "average_word_length": avg_word_length,
        "average_sentence_length": avg_sentence_length,
        "unique_words": len({w.lower() for w in words}),
    })


@mcp.tool()
def extract_keywords(text: str, count: int = 5) -> str:
    """Extract keywords (most common non-stopword words) from text.

    Args:
        text: The input text.
        count: Number of keywords to return (default 5).

    Returns:
        JSON string with the top-N keywords and frequencies.
    """
    filtered = [
        w.strip(".,!?;:") for w in text.lower().split() if w not in STOPWORDS
    ]
    top = Counter(filtered).most_common(max(1, count))
    return json.dumps({
        "keywords": [{"word": w, "frequency": f} for w, f in top]
    })


@mcp.tool()
def check_reading_level(text: str) -> str:
    """Estimate reading difficulty via a Flesch-Kincaid-style grade.

    Args:
        text: The input text.

    Returns:
        JSON string with the numeric grade and a coarse label.
    """
    sentences = max(text.count(".") + text.count("!") + text.count("?"), 1)
    words = len(text.split())
    if words == 0:
        return json.dumps({"error": "No text to analyze"})
    syllables = sum(1 for c in text.lower() if c in "aeiou")
    grade = (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59
    grade = max(0.0, round(grade, 1))
    if grade < 6:
        label = "Elementary School"
    elif grade < 9:
        label = "Middle School"
    elif grade < 13:
        label = "High School"
    else:
        label = "College/Academic"
    return json.dumps({"grade_level": grade, "reading_level": label})


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse a string.

    Args:
        text: The input text.

    Returns:
        The reversed text.
    """
    return text[::-1]


if __name__ == "__main__":
    mcp.run()
