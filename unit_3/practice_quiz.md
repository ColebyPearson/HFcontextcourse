# Unit 3 — Practice Quiz

Self-study set drawn from the four Unit 3 chapters (`introduction`, `anatomy`,
`building-plugins`, `using-plugins`). Q1–Q7 mirror **Quiz 1: Plugin
Fundamentals** territory; Q8–Q15 mirror **Quiz 2: Building and Distributing
Plugins**.

> Phrasing on the HF site will differ. Don't memorise — make sure you can
> explain *why* the right answer is right. ≥ 12/15 on the practice gives a
> comfortable margin for the real quizzes.

---

## Quiz 1 territory — Plugin Fundamentals

**1.** Which best describes the **manifest-first** vs **code-first** plugin distinction?
- a) Manifest-first plugins are JSON-only; code-first plugins always require Rust.
- b) Manifest-first (Claude Code, Codex) declare what the plugin provides via a `plugin.json`; code-first (OpenCode) ship a JS/TS module that exports hooks or custom tools.
- c) The two terms are interchangeable; both produce the same on-disk layout.
- d) Manifest-first plugins can only contain skills; code-first plugins can only contain MCP servers.

**2.** In a Claude Code plugin, where does the plugin manifest live?
- a) At the plugin root, as `plugin.json`
- b) Inside `.claude-plugin/plugin.json`
- c) Inside `skills/plugin.json`
- d) Anywhere — the agent searches recursively

**3.** Which fields does the course's `plugin.json` example for Claude Code show?
- a) `name`, `version`, `description`, `author`
- b) `name`, `entrypoint`, `permissions`, `dependencies`
- c) `id`, `slug`, `runtime`, `manifest_version`
- d) `name` and `apiKey` only

**4.** A Claude Code plugin connects to an MCP server by:
- a) Embedding the server's Python source under `server/`
- b) Pointing at the server (local `command` or remote `url`) in a `.mcp.json` at the plugin root
- c) Compiling it into a `.wasm` file
- d) Listing it in the manifest's `dependencies` array

**5.** When invoked explicitly, a plugin skill is namespaced as:
- a) `<plugin-name>.<skill-name>`
- b) `<plugin-name>/<skill-name>`
- c) `<plugin-name>:<skill-name>` — e.g. `/text-processor-plugin:check-reading-level`
- d) `@<plugin-name> <skill-name>`

**6.** OpenCode's plugin model is best described as:
- a) Identical to Claude Code's, with the same `.claude-plugin/` directory layout
- b) A JS/TS module that exports hooks and/or custom tools, loaded from `.opencode/plugins/` or `npm`
- c) A Docker image referenced by URL
- d) A YAML manifest plus a binary executable

**7.** Which of the following does **not** belong inside a manifest-first Claude Code or Codex plugin?
- a) Skills (`skills/<name>/SKILL.md`)
- b) MCP server *configuration* (`.mcp.json`)
- c) The plugin manifest (`.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`)
- d) The MCP server *source code* itself

---

## Quiz 2 territory — Building & Distributing

**8.** To make a local Claude Code plugin installable for testing, you create a small marketplace file that points at the plugin directory and then run:
- a) `claude plugin install ./my-plugin`
- b) `/plugin marketplace add <path-to-marketplace.json>` then `/plugin install <name>@<marketplace-name>`
- c) `npm install -g ./my-plugin`
- d) Drop the folder in `~/.claude/plugins/`; it auto-loads on next session

**9.** A `marketplace.json` describes:
- a) A single plugin only
- b) A named collection of plugins with `source` paths and short descriptions, suitable for serving multiple plugins
- c) Only npm-published plugins
- d) The agent's transport configuration

**10.** After editing a plugin's files (e.g. tweaking a SKILL.md description), the fastest way to make Claude Code pick up the change is:
- a) Restart your operating system
- b) Reinstall the plugin from scratch
- c) Open `/plugin` and toggle the plugin off and back on
- d) Edits never take effect until the next major Claude Code release

**11.** A plugin needs an API key. The recommended pattern is:
- a) Hardcode the key in `plugin.json`
- b) Set it as a shell environment variable; Claude Code reads it when the plugin loads
- c) Commit it to `marketplace.json`
- d) Send it as a request parameter to every tool call

**12.** Codex's `.codex-plugin/plugin.json` typically declares the path to bundled skills with the field:
- a) `"skills": "./skills/"`
- b) `"skillsDir": "skills"`
- c) `"include_skills": true`
- d) Codex auto-discovers skills — the manifest has no `skills` field

**13.** Codex caches an installed plugin under:
- a) `/tmp/codex/plugins/`
- b) `~/.agents/plugins/cache/`
- c) `~/.codex/plugins/cache/$MARKETPLACE/$PLUGIN/$VERSION/`
- d) Codex does not cache plugins; it re-downloads each session

**14.** A Pi package is declared in:
- a) `pi.toml`
- b) `package.json` with `"keywords": ["pi-package"]` and a `pi` block listing `skills`, `extensions`, etc.
- c) `.pi-plugin/plugin.json`
- d) Plain `pi.json` at the project root

**15.** A key design principle stated in the unit is that, in manifest-first plugins:
- a) The plugin must include its own MCP server source code for portability
- b) Skills describe *when* to use tools, MCP servers *provide* the tools, and plugins package the reusable behaviour — the three are deliberately separated
- c) Skills and MCP servers must always live in the same package
- d) Plugins should be tightly coupled to a specific agent runtime version

---

## Answers

### Quiz 1 territory

1. **b** — Manifest-first (Claude Code, Codex) declare components via `plugin.json` and ship `skills/`, `.mcp.json`, etc. Code-first (OpenCode) is a JS/TS module that exports hooks/custom tools.
2. **b** — `.claude-plugin/plugin.json`. *Only* the manifest lives in `.claude-plugin/`; skills, `.mcp.json`, hooks etc. stay at the plugin root.
3. **a** — `name`, `version`, `description`, `author` (the manifest is intentionally small).
4. **b** — `.mcp.json` at the plugin root, same format as project-scoped MCP config from Unit 2 (`command`+`args` for local, `url` for remote).
5. **c** — Colon-namespaced, e.g. `/text-processor-plugin:check-reading-level`. Matches the agent skill namespacing rule from Unit 1.
6. **b** — OpenCode is code-first: a JS/TS plugin module loaded from `.opencode/plugins/` or installed via the `plugin` array in `opencode.json`.
7. **d** — Plugin bundles reference the MCP server (via `.mcp.json`); they do **not** ship its source. That separation is the entire design point.

### Quiz 2 territory

8. **b** — `/plugin marketplace add <path>` registers a marketplace; `/plugin install <plugin>@<marketplace>` installs from it. `/plugin` is the in-session browser.
9. **b** — Marketplace files describe collections; a single marketplace can list many plugins, each with a `source` pointer and metadata.
10. **c** — Toggle off/on in `/plugin` is the documented reload step. The plugin watches for changes; toggling forces re-discovery.
11. **b** — Shell environment variables. Claude Code reads them when plugins load — no in-app key store, and absolutely don't put keys in the manifest.
12. **a** — `"skills": "./skills/"` is the Codex pattern. The same manifest may also have `"mcpServers": "./.mcp.json"` and `"apps": "./.app.json"`.
13. **c** — `~/.codex/plugins/cache/$MARKETPLACE/$PLUGIN/$VERSION/`. The cache key includes marketplace, plugin, and version so multiple versions coexist cleanly.
14. **b** — Pi's "plugin equivalent" is a Pi package: `package.json` with `"keywords": ["pi-package"]` plus a `pi:` block pointing at `skills/`, `extensions/`, etc.
15. **b** — Skills, MCP servers, and plugins are deliberately separate layers: skills describe *when* to use tools, MCP servers *provide* the tools, and plugins package reusable behaviour.

---

## After the real quizzes

If you score ≥ 70% on Quiz 1 and Quiz 2, mark Unit 3 done and update PLAN.md.
Capstone counts toward the **Context Engineering certificate** (Unit 1–5 quizzes
+ project), so finishing Unit 3 quizzes is one ratchet closer.
