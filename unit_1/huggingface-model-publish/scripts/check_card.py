"""Verify that a model's card metadata is indexed on the Hub.

Usage:
    python check_card.py <repo_id> [--expect <pipeline_tag>] [--require-tag <tag>]...

Exits 0 if all expectations are met; 1 otherwise. Prints what it found.
"""
from __future__ import annotations
import argparse
import sys

from huggingface_hub import HfApi


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("repo_id")
    p.add_argument("--expect", dest="pipeline_tag", default=None,
                   help="expected pipeline_tag (e.g. text-to-speech)")
    p.add_argument("--require-tag", action="append", default=[],
                   help="tag that must appear in info.tags (repeatable)")
    args = p.parse_args()

    info = HfApi().model_info(args.repo_id)
    pt = info.pipeline_tag
    tags = info.tags or []
    print(f"repo: {args.repo_id}")
    print(f"  pipeline_tag: {pt}")
    print(f"  tags:         {tags}")

    failures: list[str] = []
    if args.pipeline_tag and pt != args.pipeline_tag:
        failures.append(
            f"pipeline_tag = {pt!r}, expected {args.pipeline_tag!r}"
        )
    for t in args.require_tag:
        if t not in tags:
            failures.append(f"missing tag: {t!r}")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
