"""Rewrite a model card's YAML frontmatter cleanly and re-upload.

HF's metadata parser silently fails on certain whitespace patterns the
auto-generated cards emit (most often, a blank line between every YAML key).
This downloads the current README, strips the existing frontmatter, prepends a
clean one with the fields you specify, and uploads it back.

Usage:
    python fix_model_card.py <repo_id> \\
        --pipeline-tag text-to-speech \\
        --tags text-to-speech,generated_from_trainer \\
        --base-model microsoft/speecht5_tts \\
        --dataset qmeeus/voxpopuli \\
        --license mit
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download, upload_file

_FRONTMATTER = re.compile(r"^---.*?---", re.DOTALL)


def _build_frontmatter(args: argparse.Namespace) -> str:
    lines = ["---", "library_name: transformers"]
    if args.license:
        lines.append(f"license: {args.license}")
    if args.base_model:
        lines.append(f"base_model: {args.base_model}")
    if args.tags:
        lines.append("tags:")
        for t in args.tags.split(","):
            t = t.strip()
            if t:
                lines.append(f"- {t}")
    if args.dataset:
        lines.append("datasets:")
        lines.append(f"- {args.dataset}")
    if args.pipeline_tag:
        lines.append(f"pipeline_tag: {args.pipeline_tag}")
    if args.model_name:
        lines.append("model-index:")
        lines.append(f"- name: {args.model_name}")
        lines.append("  results: []")
    lines.append("---\n")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("repo_id")
    p.add_argument("--pipeline-tag")
    p.add_argument("--tags", help="comma-separated list of tags")
    p.add_argument("--base-model")
    p.add_argument("--dataset")
    p.add_argument("--license", default=None)
    p.add_argument("--model-name", default=None,
                   help="defaults to the last path segment of <repo_id>")
    args = p.parse_args()
    if not args.model_name:
        args.model_name = args.repo_id.split("/")[-1]

    path = hf_hub_download(args.repo_id, "README.md", force_download=True)
    raw = Path(path).read_text(encoding="utf-8")
    body = _FRONTMATTER.sub("", raw, count=1)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    new = _build_frontmatter(args) + "\n" + body + "\n"

    out = Path(path).with_suffix(".rewritten.md")
    out.write_text(new, encoding="utf-8", newline="\n")
    upload_file(path_or_fileobj=str(out), path_in_repo="README.md",
                repo_id=args.repo_id)
    print(f"uploaded clean README.md to {args.repo_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
