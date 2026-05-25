# Unit 4 — Practice Quiz

Drawn from `introduction`, `patterns`, `using-subagents`, `hands-on`. Q1–Q7
mirror **Quiz 1: Subagent Concepts**; Q8–Q15 mirror **Quiz 2: Multi-Agent
Workflows**.

> Phrasing on the HF site will differ — explain *why* the right answer is
> right. Target ≥ 12/15.

---

## Quiz 1 territory — Subagent Concepts

**1.** Which is **not** one of the four sub-agent orchestration patterns named in the unit?
- a) Fan-Out / Fan-In
- b) Pipeline
- c) Supervisor (Hierarchical)
- d) Round-Robin

**2.** "Run 5 independent benchmarks against 5 different models" is best modelled as:
- a) Pipeline
- b) Fan-Out / Fan-In
- c) Swarm
- d) Single-agent

**3.** "Extract → clean → analyse → report on a dataset" is best modelled as:
- a) Pipeline
- b) Fan-Out / Fan-In
- c) Supervisor
- d) Swarm

**4.** Which scenario is a classic **anti-pattern** for sub-agents?
- a) Two sub-agents both writing to `app.py` in parallel
- b) Five reviewers each reading a different module
- c) One implementer following one researcher
- d) A read-only security-reviewer and a read-only performance-reviewer running in parallel

**5.** A swarm (collaborative) pattern is most useful when:
- a) The task is small and easy
- b) Multiple perspectives converging on the same artefact improve its quality (design review, RFC)
- c) Stages have hard sequential dependencies
- d) Each sub-task is fully independent

**6.** Making the security- and performance-reviewer sub-agents **read-only** is valuable because:
- a) It hides the codebase from them
- b) It makes them faster
- c) It removes merge-conflict risk so they can safely run in parallel, and bounds their blast radius
- d) Read-only sub-agents have access to the production database

**7.** The Pipeline pattern's main downside is:
- a) No parallelism — each stage waits for the previous one
- b) Total time = slowest sub-agent
- c) High coordination overhead
- d) Requires more than four sub-agents

---

## Quiz 2 territory — Multi-Agent Workflows

**8.** In **Claude Code**, per-project sub-agent definitions live at:
- a) `.claude/agents/<name>.md`
- b) `.claude/subagents/<name>.json`
- c) `subagents/<name>.yaml`
- d) `~/.claude/agents/<name>.md` only — there's no project-scope path

**9.** Which frontmatter fields appear on a Claude Code sub-agent file in the course's example?
- a) `name`, `description`, `tools`, `model`
- b) `name`, `version`, `permissions`, `runtime`
- c) `slug`, `prompt`, `temperature`
- d) `id`, `entrypoint`, `scope`

**10.** **Codex** sub-agents are defined in:
- a) `.codex/agents/<name>.toml`
- b) `.codex/subagents/<name>.json`
- c) Inline in `config.toml`
- d) `codex.yaml`

**11.** The project-level instruction file that pins the workflow ("for feature work, do research → implement → verify") is:
- a) `CLAUDE.md` (Claude Code) / `AGENTS.md` (Codex, Pi)
- b) `workflow.json`
- c) `.subagent-rc`
- d) `package.json`

**12.** A common reason to **avoid** spawning a sub-agent:
- a) The work is genuinely independent
- b) The task is small and tightly coupled — sub-agent spin-up dominates the work
- c) You want parallel reviewers
- d) You want a narrow tool surface for safety

**13.** In the hands-on pipeline, which sub-agent is **not** read-only?
- a) researcher
- b) implementer
- c) security-reviewer
- d) performance-reviewer

**14.** The two reviewers (security + performance) are invoked:
- a) Sequentially — security first, then performance
- b) In parallel; parent aggregates the two reports before reporting to the user
- c) Inside a single combined "reviewer" sub-agent
- d) Only after the user requests them explicitly

**15.** Hooks, extensions, and runtime settings (as opposed to sub-agent definitions) are intended for:
- a) Driving sub-agent orchestration via a custom DSL
- b) Automation *around* the workflow (linters, test runners, guard rails) — not for orchestrating sub-agents themselves
- c) Storing API keys for sub-agents
- d) Replacing `CLAUDE.md`/`AGENTS.md`

---

## Answers

### Quiz 1 territory
1. **d** — Round-Robin isn't named; the four are Fan-Out/Fan-In, Pipeline, Supervisor, Swarm.
2. **b** — Fully independent ⇒ Fan-Out/Fan-In maximises parallelism.
3. **a** — Sequential staged data flow ⇒ Pipeline.
4. **a** — Two sub-agents editing the same file in parallel = guaranteed conflicts. Split by file or serialise.
5. **b** — Swarm = multiple perspectives converging on a single artefact; great for design review.
6. **c** — Removing write privileges removes conflict risk and bounds blast radius; that's *why* parallel review is safe.
7. **a** — Pipeline has **no** parallelism by definition. Compare to Fan-Out/Fan-In whose downside (b) is "total time = slowest sub-agent."

### Quiz 2 territory
8. **a** — `.claude/agents/<name>.md` (project scope). Also `~/.claude/agents/` exists for personal scope.
9. **a** — `name`, `description`, `tools`, `model` — the four fields used in the hands-on examples.
10. **a** — `.codex/agents/<name>.toml`. Codex uses TOML; Claude Code uses Markdown with YAML frontmatter.
11. **a** — `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex, Pi). These pin the *workflow*, not the per-agent definitions.
12. **b** — Sub-agent spin-up adds 1–2 s; for tiny tightly-coupled tasks, a single agent is faster.
13. **b** — The implementer gets Write/Edit/Bash; researcher and the two reviewers are intentionally read-only.
14. **b** — Parallel; the parent aggregates both reports. That's the fan-out/fan-in stage of the pipeline.
15. **b** — Hooks/extensions/settings are for automation around the workflow. Sub-agent orchestration belongs in `CLAUDE.md`/`AGENTS.md` plus the agent files themselves.

---

## After the real quizzes

Pass both ≥ 70% → check the Unit 4 boxes, update PLAN.md. One more cert-critical
unit (Unit 5) to go before Context Engineering needs the capstone.
