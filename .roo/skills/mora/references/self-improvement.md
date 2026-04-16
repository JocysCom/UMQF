# MORA Self-Improvement Prompt

Use this prompt when the user asks to simplify, audit, or improve the MORA process itself (parallel to the `## UMQ Improvement` prompt in `README.md`, which targets the formula rather than the process).

## TASK

Your task is to review, improve, and simplify the MORA process. The current process may be overcomplicated or failing to produce the desired results.

First, gain a complete understanding of the process by carefully reviewing **all** process-related files (skill instructions, README, scripts, and any other configuration or helper files that define behavior).

Simplify and update the process so that it produces high-quality, reliable final results. You may modify any file listed under "You can modify these files" below, but you must not alter existing final-result artifacts.

Be careful. Create a plan that gradually simplifies and updates the instructions, because this process can be restarted multiple times from a fresh context. Don't change too much at once. Clean up unused scripts or references if redundant — it reduces cognitive load. Provide the reason for each change.

Why simplify? Because each new sentence added waters down other rules and increases complexity. Avoid repeating the same ideas and maximize the meaning/words ratio. Stick to the single source of truth principle.

Think very hard — your and my future survival depends on it.

## CONTEXT

The main goal is simple:

1. Download the document specified by the user.
2. Analyze the document according to the morality formula described in `UMQF.md`.
3. Identify the main acting entities in the document.
4. Create a profile for each main acting entity that performed an action suitable for UMQF:

   - `MORA/analysis/{document}/entities/{entity}.md` — UMQ summary and evaluation of the entity.
   - `MORA/analysis/{document}/entities/{entity}-actions.md` — Detailed analysis of entity actions.

## HOW TO START

Read and analyze these documents:

1. The skill instructions: `.ai/skills/mora/SKILL.md`
2. The help file: `README.md`
3. The formula: `UMQF.md`
4. The example book: `MORA/analysis/exploration-team/source-document.md`
5. The expected actions output: `MORA/analysis/exploration-team/entities/huyghens-actions.md`
6. The expected summary output: `MORA/analysis/exploration-team/entities/huyghens.md`

Then review the remaining process files in `.ai/skills/mora/` (especially `scripts/` and `references/`) so you fully understand how the current process works before making any modifications.

## Protected files (do not modify)

- `UMQF.md`
- `MORA/analysis/exploration-team/source-document.md`
- `MORA/analysis/exploration-team/entities/huyghens-actions.md`
- `MORA/analysis/exploration-team/entities/huyghens.md`
- Any other already-produced final-result artifact under `MORA/analysis/`

## You can modify these files

- `.ai/skills/mora/SKILL.md`
- `.ai/skills/mora/references/entity.template.md`
- `.ai/skills/mora/references/self-improvement.md` (this file)
- Any script inside `.ai/skills/mora/scripts/`
- `README.md`

You may create, delete, merge, or restructure scripts and references if that simplifies the process and improves reliability — as long as you do not change the protected files or the already-produced final-result artifacts. After any change under `.ai/`, run the sync script to propagate to all agents:

```bash
python .ai/skills/ai-self-improvement/scripts/sync_agent_assets.py AUTO
```
