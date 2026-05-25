"""Gradio UI that doubles as an MCP server.

`demo.launch(mcp_server=True)` exposes each function wrapped in a click handler
as an MCP tool at /gradio_api/mcp/. The same code thus serves a human web UI
AND any MCP-compatible code agent (Claude Code, Codex, OpenCode, Pi).

Run locally: python app.py        -> http://localhost:7860
                                   -> MCP at http://localhost:7860/gradio_api/mcp/
Deployed:    same on HF Spaces    -> /gradio_api/mcp/
"""
from __future__ import annotations

import json
from collections import Counter

import gradio as gr

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "by", "from",
}


def analyze_text(text: str) -> str:
    """Analyze text and return statistics.

    Args:
        text: The input text to analyze.

    Returns:
        JSON string with character, word, and sentence statistics.
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
    }, indent=2)


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
    top = Counter(filtered).most_common(max(1, int(count)))
    return json.dumps(
        {"keywords": [{"word": w, "frequency": f} for w, f in top]},
        indent=2,
    )


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
    grade = max(
        0.0,
        (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59,
    )
    if grade < 6:
        label = "Elementary School"
    elif grade < 9:
        label = "Middle School"
    elif grade < 13:
        label = "High School"
    else:
        label = "College/Academic"
    return json.dumps(
        {"grade_level": round(grade, 1), "reading_level": label},
        indent=2,
    )


with gr.Blocks(title="Text Processor (MCP)") as demo:
    gr.Markdown("# Text Processing Tools")
    gr.Markdown(
        "Analyze text statistics, extract keywords, and check reading "
        "difficulty. Also exposed as an MCP server at `/gradio_api/mcp/`."
    )

    with gr.Tab("Analyze"):
        text_in1 = gr.Textbox(label="Enter text", lines=8,
                              placeholder="Paste your text here…")
        out1 = gr.Textbox(label="Analysis", lines=10)
        gr.Button("Analyze", variant="primary").click(
            analyze_text, text_in1, out1
        )

    with gr.Tab("Extract Keywords"):
        text_in2 = gr.Textbox(label="Enter text", lines=8)
        count_in = gr.Slider(1, 20, value=5, step=1, label="Number of keywords")
        out2 = gr.Textbox(label="Keywords", lines=10)
        gr.Button("Extract", variant="primary").click(
            extract_keywords, [text_in2, count_in], out2
        )

    with gr.Tab("Reading Level"):
        text_in3 = gr.Textbox(label="Enter text", lines=8)
        out3 = gr.Textbox(label="Reading level", lines=5)
        gr.Button("Check", variant="primary").click(
            check_reading_level, text_in3, out3
        )

if __name__ == "__main__":
    demo.launch(mcp_server=True)
