# HuggingFace Context Course

## Project Overview
This repo contains hands-on work for the HuggingFace Context Course — context engineering for code agents (skills, MCP, plugins, sub-agents, hooks, nano harness).
Course URL: https://huggingface.co/learn/context-course/unit0/introduction
GitHub source: https://github.com/huggingface/context-course

## Certification
- **Context Fundamentals**: pass Unit 1–2 quizzes ≥ 70%
- **Context Engineering**: pass Unit 1–5 quizzes ≥ 70% + complete the capstone project

## Hands-on Assignments
- **Unit 2** — Build and deploy an MCP server (Python, with a Gradio variant)
- **Unit 4** — Multi-agent workflow with sub-agents
- **Unit 5** — Agent activity dashboard with Gradio + hooks
- **Unit 6** — Extend the Nano Harness (bonus)

## Structure
- `unit_*/` — per-unit hands-on artifacts and notes
- `notebooklm/unit_*.txt` — concatenated MDX per unit (NotebookLM-ready)
- `_source/` — local clone of `huggingface/context-course` (gitignored; used to build `notebooklm/`)

## Key Libraries
- `mcp` (the Model Context Protocol SDK)
- `anthropic` (for Nano Harness in Unit 6)
- `gradio` (Gradio MCP / dashboards in Units 2 & 5)
- `pydantic`

## Reference Agent
This repo treats **Claude Code** as the primary agent for skills, plugins, sub-agents, and hooks. The course also covers Codex and OpenCode; equivalents are noted in the unit READMEs where they differ.
