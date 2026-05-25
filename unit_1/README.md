# Unit 1 — Skills: Portable Knowledge for Code Agents

Official chapter URL base: https://huggingface.co/learn/context-course/unit1/
NotebookLM source: [`notebooklm/unit_1.txt`](../notebooklm/unit_1.txt)

## Chapters (in order)

- **Unit 1: Agent Skills** — https://huggingface.co/learn/context-course/unit1/introduction
- **What Are Agent Skills?** — https://huggingface.co/learn/context-course/unit1/what-are-skills
- **The SKILL.md Format** — https://huggingface.co/learn/context-course/unit1/skill-format
- **Quiz 1: Understanding Skills and the Specification** — https://huggingface.co/learn/context-course/unit1/quiz1
- **Using Skills with Code Agents** — https://huggingface.co/learn/context-course/unit1/using-skills
- **Building Your First Skill** — https://huggingface.co/learn/context-course/unit1/building-skills
- **Quiz 2: Building and Using Skills** — https://huggingface.co/learn/context-course/unit1/quiz2

## Status

- [x] Read all chapters (or listen via NotebookLM)
- [x] **First skill built** — [`huggingface-model-publish/`](huggingface-model-publish/)
- [ ] Quiz 1 (≥ 70% on the HF course site)
- [ ] Quiz 2 (≥ 70% on the HF course site)

## The skill

**[`huggingface-model-publish/`](huggingface-model-publish/)** — captures the
publishing workflow executed four times during the HF Audio Course
(train → verify metric → push), including the **model-card YAML pitfall** that
caused the SpeechT5 model's `text-to-speech` tag to silently not index. The
reusable bits:

- `scripts/push_with_verify.py` — guard `trainer.push_to_hub()` on a metric
  threshold (any Trainer + any metric).
- `scripts/check_card.py` — assert `pipeline_tag` / `tags` are indexed on the
  Hub (CLI, exits non-zero if not).
- `scripts/fix_model_card.py` — rewrite a card's YAML frontmatter cleanly
  and re-upload (the actual fix used on `speecht5-finetuned-voxpopuli-nl`).
- `references/tagging-pitfalls.md` — the SpeechT5 case study, written down.

Validated: `SKILL.md` frontmatter parses cleanly; `check_card.py` works live
against `VoicesColeby/distilhubert-finetuned-gtzan`.

## Making Claude Code discover this skill

Source of truth is **`unit_1/huggingface-model-publish/`** (in git). Claude
Code discovers project-scoped skills under `.claude/skills/<name>/`, which is
gitignored. Set up the local junction once (Windows, no admin needed):

```powershell
$skills = "$PWD\.claude\skills"
New-Item -ItemType Directory -Force -Path $skills | Out-Null
New-Item -ItemType Junction -Path "$skills\huggingface-model-publish" `
                            -Target "$PWD\unit_1\huggingface-model-publish" | Out-Null
```

(macOS/Linux equivalent:
`mkdir -p .claude/skills && ln -s "$PWD/unit_1/huggingface-model-publish" .claude/skills/huggingface-model-publish`.)

Then `claude` in this repo will auto-discover it. Activation pressure-test
prompts (per the course's "Did Your Skill Fire?" section):

- *"I just trained a model — push it to the Hub if the eval accuracy clears 0.85."*
- *"My model's `pipeline_tag` is wrong on the Hub even though my README says otherwise. Fix it."*

Both should match the description and load the skill.
