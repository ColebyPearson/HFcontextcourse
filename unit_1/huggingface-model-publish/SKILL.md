---
name: "huggingface-model-publish"
description: "Publish fine-tuned models to the Hugging Face Hub end-to-end. Use when pushing PyTorch/transformers models with trainer.push_to_hub, setting model-card metadata (pipeline_tag, tags), or fixing model cards whose YAML frontmatter isn't being indexed."
license: "MIT"
compatibility: "Python 3.10+; huggingface_hub>=0.20, transformers>=4.40"
metadata:
  author: "VoicesColeby"
  version: "0.1.0"
  created: "2026-05-25"
allowed-tools: "Bash(hf:*) Bash(python:*) Read Write"
---

# Hugging Face Model Publish Skill

## Overview

Publish a fine-tuned model to the Hugging Face Hub the way it should be: only
after the eval metric clears its bar, with model-card metadata that actually
gets indexed (so `pipeline_tag` and `tags` show up on the Hub UI and search).

This skill captures the gotchas you hit if you do it the obvious way:
- Pushing during training (via `TrainingArguments(push_to_hub=True)`) pushes
  checkpoints whether or not the metric passed — fine for some flows, bad if
  you want a clean "the artifact only exists if it qualifies" guarantee.
- `trainer.push_to_hub(tasks="text-to-speech", ...)` correctly writes the
  model-card frontmatter, but HF's metadata parser silently fails on certain
  whitespace patterns the auto-generator emits — so the tag is in the README
  but **not on the Hub**.
- The fix is a tiny, repeatable rewrite of the YAML frontmatter, not a
  workaround at training time.

## Prerequisites Checklist

- [ ] `pip install -U huggingface_hub transformers`
- [ ] `hf auth login` (or `HF_TOKEN` env var set)
- [ ] You know your Hub username (`hf whoami` or `HfApi().whoami()['name']`)
- [ ] The training run has a verifiable metric (accuracy, WER, BLEU, …) and a
      pass threshold

## Step-by-Step Guide

### Step 1: Train without auto-pushing

Set `push_to_hub=False` so the Trainer doesn't publish unconditionally. Push
explicitly only after Step 2 passes.

```python
from transformers import TrainingArguments, Trainer

args = TrainingArguments(
    output_dir="runs/my-model",
    push_to_hub=False,          # << explicit push later
    report_to="none",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",  # whatever fits your task
    save_total_limit=2,
    # ... your other args
)
trainer = Trainer(model=model, args=args, train_dataset=tr, eval_dataset=ev,
                  compute_metrics=compute_metrics)
trainer.train()
```

### Step 2: Verify the metric, then push

The push is guarded — failures don't get a Hub artifact. The reusable script
[`scripts/push_with_verify.py`](scripts/push_with_verify.py) wraps this pattern
for any Trainer + metric combo.

```python
res = trainer.evaluate()
acc = res["eval_accuracy"]
print(f"[RESULT] eval_accuracy={acc:.4f} target>=0.87 "
      f"{'PASS' if acc >= 0.87 else 'FAIL'}", flush=True)

if acc >= 0.87:
    trainer.push_to_hub(
        dataset_tags="marsyas/gtzan",
        dataset="GTZAN",
        model_name="distilhubert-finetuned-gtzan",
        finetuned_from="ntu-spml/distilhubert",
        tasks="audio-classification",   # << drives pipeline_tag + tags
    )
```

### Step 3: Verify the model card actually got indexed

`trainer.push_to_hub(tasks=...)` *writes* a README.md with YAML frontmatter,
but that's not the same as HF *parsing* it. Confirm with the API:

```python
from huggingface_hub import HfApi
info = HfApi().model_info("VoicesColeby/distilhubert-finetuned-gtzan")
print("pipeline_tag:", info.pipeline_tag)
print("text-to-speech in tags:", "text-to-speech" in (info.tags or []))
print("tags:", info.tags)
```

[`scripts/check_card.py`](scripts/check_card.py) is the same call wrapped as a
CLI: exits 0 if the expected `pipeline_tag` is set, non-zero otherwise.

```bash
python scripts/check_card.py <repo_id> --expect text-to-speech
```

### Step 4: Fix the YAML frontmatter if Step 3 failed

If `pipeline_tag` is `None` or your expected tag isn't in `tags`, the README
frontmatter is present but the metadata parser couldn't read it (most often
because of double-spaced YAML — a blank line between every key, which the
auto-card writer sometimes emits and HF's validator rejects).

The repeatable fix: download the current README, strip the frontmatter,
prepend a clean one, upload back. See
[`scripts/fix_model_card.py`](scripts/fix_model_card.py):

```bash
python scripts/fix_model_card.py <repo_id> \
    --pipeline-tag text-to-speech \
    --tags text-to-speech,generated_from_trainer \
    --base-model microsoft/speecht5_tts \
    --dataset qmeeus/voxpopuli
```

Then re-run Step 3 to confirm it's indexed.

## Troubleshooting

### `pipeline_tag` is `None` even though the README has `pipeline_tag: …`

Almost always a YAML formatting issue. Two common patterns that HF will not
parse:

- **Double-spaced frontmatter** (a blank line between every key). Seen after
  `ModelCard.load(...).push_to_hub(...)` round-trips. Run
  `scripts/fix_model_card.py`.
- **Trailing whitespace** after the closing `---`. Less common; the fix is
  the same.

See [`references/tagging-pitfalls.md`](references/tagging-pitfalls.md) for the
exact case study from a SpeechT5 push.

### `OSError: You are not authenticated`

```bash
hf auth login          # or:
export HF_TOKEN=hf_xxx
```

### `EntryNotFoundError` while updating the card

You're uploading to a repo that doesn't exist. Either run `trainer.push_to_hub`
first (which creates it), or `HfApi().create_repo(repo_id)` explicitly.

## Helper Scripts

- [`scripts/push_with_verify.py`](scripts/push_with_verify.py) — guard push on
  a metric threshold (any Trainer + any metric).
- [`scripts/check_card.py`](scripts/check_card.py) — query `model_info` and
  assert `pipeline_tag` matches expectation.
- [`scripts/fix_model_card.py`](scripts/fix_model_card.py) — rewrite the
  README's YAML frontmatter cleanly and re-upload.

## References

- [`references/tagging-pitfalls.md`](references/tagging-pitfalls.md) — the
  SpeechT5 / `text-to-audio`-vs-`text-to-speech` case study.
- [Hugging Face Hub Python library docs](https://huggingface.co/docs/huggingface_hub)
- [Model card metadata spec](https://huggingface.co/docs/hub/model-cards)
