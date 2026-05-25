# Tagging pitfalls — case study

A concrete walk-through of the problem this skill exists to solve.

## Setup

Fine-tuned `microsoft/speecht5_tts` on Dutch VoxPopuli, then:

```python
trainer.push_to_hub(
    dataset_tags="qmeeus/voxpopuli",
    dataset="VoxPopuli",
    dataset_args="config: nl, split: train",
    finetuned_from="microsoft/speecht5_tts",
    tasks="text-to-speech",
)
```

Expected: the model shows up tagged `text-to-speech` on the Hub.

## Observed (broken)

```python
>>> info = HfApi().model_info("VoicesColeby/speecht5-finetuned-voxpopuli-nl")
>>> info.pipeline_tag
'text-to-audio'                # auto-detected from SpeechT5, NOT what we set
>>> 'text-to-speech' in (info.tags or [])
False
>>> info.tags
['safetensors', 'speecht5', 'region:us']
```

So our `tasks="text-to-speech"` reached the README but *not* the index.

## What actually happened

`trainer.push_to_hub(...)` does write `pipeline_tag: text-to-speech` and
`tags: [generated_from_trainer, text-to-speech]` into the README frontmatter.
But the frontmatter the auto-card writer produced was **double-spaced** —
a blank line between every YAML line:

```
---

library_name: transformers

license: mit

tags:

- generated_from_trainer

- text-to-speech

pipeline_tag: text-to-speech

---
```

HF's metadata validator emits a "empty or missing yaml metadata in repo card"
warning on this shape and refuses to index it. The README is correct from a
human-reading perspective; the parser can't pick it up.

## The fix that worked

A two-line rewrite: download the README, replace the (broken) frontmatter
block with a clean one, upload back.

```python
import re
from pathlib import Path
from huggingface_hub import hf_hub_download, upload_file

rid = "VoicesColeby/speecht5-finetuned-voxpopuli-nl"
p = hf_hub_download(rid, "README.md", force_download=True)
raw = Path(p).read_text(encoding="utf-8")
body = re.sub(r"^---.*?---", "", raw, count=1, flags=re.DOTALL)
body = re.sub(r"\n{3,}", "\n\n", body).strip()
clean = '''---
library_name: transformers
license: mit
base_model: microsoft/speecht5_tts
tags:
- generated_from_trainer
- text-to-speech
datasets:
- qmeeus/voxpopuli
pipeline_tag: text-to-speech
model-index:
- name: speecht5-finetuned-voxpopuli-nl
  results: []
---
'''
Path(p).write_text(clean + "\n" + body + "\n", encoding="utf-8", newline="\n")
upload_file(path_or_fileobj=p, path_in_repo="README.md", repo_id=rid)
```

After the rewrite:

```python
>>> info = HfApi().model_info(rid)
>>> info.pipeline_tag
'text-to-speech'
>>> 'text-to-speech' in info.tags
True
```

`scripts/fix_model_card.py` in this skill is the same logic as a reusable CLI.

## Why this matters

Course assessments (and the Hub's own search/filter UI) read the *indexed*
metadata, not the README text. A model that's correctly trained, pushed, and
documented can still fail a grading bot purely because its card YAML was
formatted in a way HF's parser silently rejects. Always run
`scripts/check_card.py` immediately after `push_to_hub` to catch this before
something downstream depends on the tag being present.
