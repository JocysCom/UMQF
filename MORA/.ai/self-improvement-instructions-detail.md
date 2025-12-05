## Self-Improvement Detailed Instructions

This file contains detailed instructions for self-improvement. It is read only when the user requests self-improvement to avoid watering down main instructions.

### Editable Instruction Files

You can update your own instruction files:
- `.ai/instructions.md` – the main system instructions file
- `.ai/*instructions.md` – additional instruction files (auto-included)
- `.ai/*instructions-detail.md` – detailed instruction files (read only when needed)

### Single Source of Truth

**NEVER embed template content in instructions - reference template files instead.**

Example:
- ✅ "Template maintained in pr/checklist.template.md"
- ❌ Pasting template content into instructions

### Activation Process

After editing instruction files, run from repository root:

```powershell
.\.ai\Update-AgentInstructions.ps1 AUTO
```

This command updates and activates the modified instruction files in `.roo/rules/`.
