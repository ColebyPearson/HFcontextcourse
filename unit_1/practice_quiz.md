# Unit 1 — Practice Quiz

Self-study set drawn from the four Unit 1 chapters (`what-are-skills`,
`skill-format`, `using-skills`, `building-skills`). The first 7 questions
mirror the territory of **Quiz 1: Understanding Skills and the Specification**;
the last 8 mirror **Quiz 2: Building and Using Skills**.

> Phrasing on the HF site will differ. Don't memorize — make sure you can
> explain *why* the right answer is right. If you score < 12/15, re-skim the
> chapter the missed question came from before taking the real quiz.

---

## Quiz 1 territory — Understanding & the Specification

**1.** Which statement about a SKILL.md file is most accurate?
- a) A SKILL.md file can live anywhere inside the project; agents will find it by filename.
- b) A SKILL.md file must sit in the root of a `skill-name/` directory whose name matches the `name` frontmatter field.
- c) The Markdown body is optional; only the YAML frontmatter is required.
- d) The SKILL.md must be placed in a `scripts/` subdirectory.

**2.** Which of these directory names is **invalid** per the Agent Skills Spec?
- a) `dataset-validation`
- b) `hf-cli`
- c) `my--skill`
- d) `model-card-generator`

**3.** The two **required** SKILL.md frontmatter fields are:
- a) `name` and `license`
- b) `name` and `description`
- c) `name` and `version`
- d) `description` and `allowed-tools`

**4.** The `description` field has a maximum length of:
- a) 256 characters
- b) 512 characters
- c) 1024 characters
- d) Unlimited

**5.** Where should *runnable* helper code live inside a skill?
- a) Inline inside SKILL.md
- b) In the `references/` directory
- c) In the `scripts/` directory
- d) In the `assets/` directory

**6.** The recommended size for a single SKILL.md is roughly:
- a) Under 100 lines
- b) 400–800 lines
- c) 1,000–2,000 lines
- d) Any size; the spec has no recommendation

**7.** A skill links to a helper script as `scripts/validate.py`. How is this path resolved?
- a) Relative to the user's current working directory
- b) Relative to the agent binary
- c) Relative to the skill's root directory (where SKILL.md lives)
- d) As an absolute path; the link won't work without rewriting it

---

## Quiz 2 territory — Building & Using

**8.** In Claude Code, **project-scoped** skills live at which path (relative to the project root)?
- a) `skills/<name>/SKILL.md`
- b) `.claude/skills/<name>/SKILL.md`
- c) `~/.claude/skills/<name>/SKILL.md`
- d) `.agents/skills/<name>/SKILL.md`

**9.** A skill is installed but doesn't activate on a vague user request. The first thing to do is:
- a) Reinstall the skill
- b) Move it from project scope to personal scope
- c) Tighten the `description` so its keywords match the phrasing real users write
- d) Add an `allowed-tools` field

**10.** Claude Code plugin skills are namespaced as:
- a) `<plugin-name>.<skill-name>`
- b) `<plugin-name>:<skill-name>` (e.g. `/hf-cli:download-model`)
- c) `@<plugin>/<skill>`
- d) The plugin name is hidden; skills are always called by skill name only

**11.** To iterate on a skill **while** a Claude Code session is running, the recommended pattern is:
- a) Restart the agent after every edit
- b) Copy the SKILL.md into the project after each edit
- c) Symlink (or directory-junction on Windows) the skill source into `.claude/skills/` so edits take effect mid-session
- d) Push the skill to the Hugging Face skills repo and re-install

**12.** "Did your skill fire?" testing, per the course, means:
- a) Running a single obvious prompt and checking the agent's reasoning trace
- b) Running both an obvious prompt **and** a vaguer real-user prompt; tightening the description until both reliably fire
- c) Setting `allowed-tools: "*"`
- d) Adding example prompts inside the SKILL.md body

**13.** Which of these descriptions is most likely to activate reliably?
- a) `"A dataset skill"`
- b) `"Useful for working with data files"`
- c) `"Publish datasets to Hugging Face Hub. Use when uploading datasets, creating dataset cards, or managing dataset versions."`
- d) `"For datasets"`

**14.** Two installed skills cover overlapping work and the wrong one keeps firing. Cleanest fix:
- a) Delete one of the two skills
- b) Use `allowed-tools` to disable the wrong one
- c) Make each skill's `description` more specific about its scope so the agent can distinguish them
- d) Manually invoke the right skill every time

**15.** The `allowed-tools` frontmatter field is:
- a) Required for every skill
- b) Optional and currently experimental; not all agents support it
- c) A synonym for `compatibility`
- d) Used to declare Python package dependencies

---

## Answers

### Quiz 1 territory

1. **b** — SKILL.md must be at the root of a skill directory named exactly the `name` value (lowercase, hyphens, max 64 chars).
2. **c** — Consecutive hyphens (`my--skill`) are explicitly disallowed by the Agent Skills Spec.
3. **b** — `name` and `description` are required; `license`, `compatibility`, `metadata`, and `allowed-tools` are optional.
4. **c** — `description` is capped at 1024 characters. Aim for clear, verb-led; "Publish datasets to Hugging Face Hub. Use when …" pattern.
5. **c** — `scripts/` holds executable code. `references/` holds docs; `assets/` holds templates and data.
6. **b** — 400–800 lines, with long content moved to `references/` or `scripts/`. Total skill < 2 MB.
7. **c** — All relative paths in SKILL.md are resolved from the skill root, *not* the agent's working directory.

### Quiz 2 territory

8. **b** — `.claude/skills/<name>/SKILL.md` is project scope; `~/.claude/skills/...` is personal scope (all your projects).
9. **c** — The most common reason a skill doesn't fire is that its `description` keywords don't match the user's phrasing. Tighten it first.
10. **b** — Colon-namespaced: `/<plugin-name>:<skill-name>`. Used to avoid conflicts when multiple plugins ship skills.
11. **c** — A symlink (or directory junction on Windows) into `.claude/skills/` makes edits take effect immediately — Claude Code watches for changes mid-session. Copy works but loses live-reload.
12. **b** — Activation pressure-test: one obvious prompt + one vaguer real-user prompt. If only the obvious one fires, the description is too narrow.
13. **c** — Verb-led, names the specific task, and lists when-to-use cues ("uploading", "creating … cards", "managing … versions") that real prompts contain. (a), (b), and (d) are vague and won't trigger.
14. **c** — Improve both descriptions to make each skill's scope distinct. Disabling/deleting (a, b) loses functionality; manual invocation (d) defeats the purpose.
15. **b** — `allowed-tools` is an *experimental* opt-in field for restricting tool access; not yet honored by every agent.

---

## After the real quizzes

If you score ≥ 70% on both, you're done with Unit 1 — move on to Unit 2 (MCP),
the cert-critical unit with the hands-on. Update PLAN.md and `unit_1/README.md`
to mark the quizzes done.
