"""Build notebooklm/unit_N.txt and unit_N/README.md from the cloned MDX source.

Reads _source/units/en/_toctree.yml for the canonical chapter order.
Concatenates each unit's MDX chapters into one NotebookLM-friendly .txt and
emits a per-unit README that mirrors the chapter list.

Re-run any time the upstream course updates (after `git -C _source pull`).
"""
from __future__ import annotations
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).parent
SRC = ROOT / "_source" / "units" / "en"
NLM = ROOT / "notebooklm"
NLM.mkdir(exist_ok=True)

toc = yaml.safe_load((SRC / "_toctree.yml").read_text(encoding="utf-8"))

FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
IMPORTS = re.compile(r"^import\s+.*$", re.MULTILINE)


def clean(mdx: str) -> str:
    mdx = FRONTMATTER.sub("", mdx, count=1)   # drop YAML frontmatter if any
    mdx = IMPORTS.sub("", mdx)                # drop JSX/MDX `import ...` lines
    # collapse runs of blank lines
    return re.sub(r"\n{3,}", "\n\n", mdx).strip() + "\n"


for unit_idx, unit in enumerate(toc):
    title = unit["title"]
    sections = unit["sections"]
    folder = ROOT / f"unit_{unit_idx}"
    folder.mkdir(exist_ok=True)

    # --- notebooklm/unit_N.txt
    parts = [f"# {title}\n"]
    for s in sections:
        local = s["local"]                                    # e.g. "unit2/key-concepts"
        sec_title = s["title"]
        path = SRC / f"{local}.mdx"
        if not path.exists():
            parts.append(f"\n## {sec_title}\n\n[missing source: {local}.mdx]\n")
            continue
        parts.append(f"\n\n## {sec_title}\n\n{clean(path.read_text(encoding='utf-8'))}")
    (NLM / f"unit_{unit_idx}.txt").write_text("".join(parts), encoding="utf-8")

    # --- unit_N/README.md
    lines = [
        f"# Unit {unit_idx} — {title.split('. ',1)[-1]}",
        "",
        f"Official chapter URL base: https://huggingface.co/learn/context-course/unit{unit_idx}/",
        f"NotebookLM source: [`notebooklm/unit_{unit_idx}.txt`](../notebooklm/unit_{unit_idx}.txt)",
        "",
        "## Chapters (in order)",
        "",
    ]
    for s in sections:
        anchor = s["local"].split("/", 1)[1]
        lines.append(f"- **{s['title']}** — https://huggingface.co/learn/context-course/unit{unit_idx}/{anchor}")
    lines += [
        "",
        "## Status",
        "",
        "- [ ] Read all chapters (or listen via NotebookLM)",
    ]
    has_hands_on = any(s["local"].endswith("/hands-on") for s in sections)
    if has_hands_on:
        lines.append("- [ ] Hands-on project (artifacts in this folder)")
    quizzes = [s for s in sections if "/quiz" in s["local"]]
    for q in quizzes:
        lines.append(f"- [ ] {q['title']} (≥ 70% on the HF course site)")
    lines.append("")
    (folder / "README.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"unit_{unit_idx}: {len(sections)} chapters -> notebooklm/unit_{unit_idx}.txt + unit_{unit_idx}/README.md")
