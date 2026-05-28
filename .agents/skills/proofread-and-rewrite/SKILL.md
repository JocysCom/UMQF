---
name: proofread-and-rewrite
description: |
  Proofread and improve text so it is correct, clear, concise, and easy to read aloud.
  Use whenever the user asks to proofread, edit, fix grammar, improve wording, polish, rewrite
  for clarity, tighten, clean up, or make text easier to read or speak — including titles,
  fragments, single sentences, paragraphs, emails, scripts, talking points, and longer passages.
  Also use when the user pastes text and asks "does this make sense?" or "make this better"
  without naming a specific action.
allowed-tools:
  - Read
  - Edit
  - Write
  - AskUserQuestion
---

# Proofread and Rewrite

Improve the given text so it is correct, clear, concise, and easy to read aloud. Preserve the
original intended meaning. Match effort to the input — short text gets a direct fix, longer
or layered text gets a brief analytical pass first.

## Goals

- Correct spelling, grammar, punctuation, and awkward wording.
- Make the text easier to understand and easier for a listener to follow.
- Improve logical flow; remove repetition that is not deliberate.
- Use common, precise, literal words. Avoid corporate buzzwords.
- Keep every idea the author put in; never invent new ones.
- Serve truth, not diplomacy: preserve the original directness and rhetorical force; do not
  soften, sanitise, or hedge a claim for politeness.

## Hard rule: do not add facts

Do not introduce claims, motivations, causes, conclusions, or details that the original text
and the surrounding conversation do not support. If meaning is strongly implied, you may label
it as an inference in the analysis — do not promote it to a stated fact in the rewritten text.

If meaning is ambiguous and a faithful correction is not possible, ask one targeted question
instead of guessing.

## Hard rule: preserve list and noun-phrase structure

A list inside a sentence carries structure beyond the words: a head noun, a number of
elements, and what each element attaches to. Smoothing awkward list phrasing is high-risk —
it is easy to silently change the count or the attachment and produce text that sounds
better but means something different.

Before rewriting any list or coordinated noun phrase:

- Identify the **head noun** (the thing the sentence is about) and the **modifier** (what
  is being said about it). In "folders that hold skills for creating tools, skills, and
  workflows", the head is *skills* and the modifier is *for creating [three outputs]* —
  the folder holds **one** kind of thing, not three.
- Count the distinct entities in the source list. The rewrite must have the same count.
- Confirm each list element attaches to the same parent it did in the source. Do not
  promote a modifier to a coordinate, or vice versa.

Common silent-drift patterns to watch for:

- "X for creating A, B, and C" (one X, three outputs) silently becoming "X, A, B, and C"
  (four things) — or vice versa.
- Two adjacent lists ("skills and tools" plus "tools and skills") collapsed into one tidier
  pair, dropping a category.
- Awkward repetition that looks like a typo but is actually recursive ("skills that create
  skills") flattened into a single category.
- Re-scoping the head noun with a prepositional phrase ("the skills I use for n8n work")
  when the source said something broader ("skills, tools, and other things").

Awkward phrasing in a list is a signal, not noise — the writer may be expressing an unusual
structure that the obvious paraphrase erases. A correct-but-awkward rewrite is better than
a fluent rewrite that lies about the shape of the idea. When in doubt, ask which structure
was intended rather than guessing.

## Hard rule: preserve truth and force

The goal is truth-seeking, not diplomacy. Do not replace direct words with euphemisms, insert
hedges that weaken assertions, or smooth out pointed phrasing for politeness or political
correctness — that distorts the information. If the source is sharp, blunt, critical, or
making a hard claim, the rewrite must land with the same force.

Signals that carry rhetorical weight and must be preserved: blunt word choice, short emphatic
sentences, contrast, repetition for emphasis, deliberate brevity, calling something by its
plain name. A polished rewrite that erases these is a worse rewrite, not a better one.

## Hard rule: check the source's factual premises

Before rewriting, identify any verifiable real-world claim the source asserts or assumes —
especially "X has not happened", "Y does not exist", "no one has built Z", anything about
products, releases, versions, dates, prices, people's roles, or the current state of the
outside world. Training data goes stale. Polishing a false premise produces a more convincing
false premise — that is worse than the messy original.

If such a claim is load-bearing for the rewrite and you cannot verify it from the conversation
or from confident, current knowledge, web-search it or ask the user before producing the
rewrite. Never silently preserve the source's factual claim just because it was in the source.
When a check changes the picture, surface what you found and offer rewrite options that fit
the corrected facts instead of guessing which one the user wants.

## Approach — match effort to the input

Use judgment, not a rigid rule:

- **Short or simple input** — one or two distinct ideas with no reordering needed: correct it
  directly, then list the changes briefly. Skip the analysis table. Sentence count is not the
  trigger — a one-sentence comma-spliced compound thought with five ideas is *not* short.
- **Longer or layered input** — three or more distinct ideas, dependent ideas, or any case
  where order or logic may need to shift: do the analytical pass below before rewriting.
- **Reaching or imprecise input** — the source circles an idea without landing on it, or the
  user signals they cannot express what they mean: offer 2–3 candidate phrasings that capture
  different plausible intents, briefly note what each one assumes, and ask which fits. Do not
  silently pick one.

### Analytical pass (only when warranted)

1. **Map the meaning.** For each original sentence or fragment (IDs O1, O2, …) note what it
   explicitly says and any idea it strongly implies (clearly marked as inference). Add A-rows
   (A1, A2, …) for ideas that only emerge from combining sentences. When a sentence contains
   a list or coordinated noun phrase, record the **head noun**, the **count** of list
   elements, and **what each element attaches to** — this is where silent drift sneaks in
   (see *preserve list and noun-phrase structure*).

2. **Identify real relationships.** Look for condition→outcome, cause→consequence,
   problem→solution, claim→explanation, past→present→future, general→specific. Two sentences
   sitting next to each other are not automatically cause and effect — call it a "possible
   link" when uncertain.

3. **Reorder for clarity.** A useful default is context → main point → explanation → result →
   next step, or problem → solution, or past → present → future. Keep deliberate emphasis,
   tone, or rhetorical order when reordering would weaken the message.

4. **Rewrite.** Split long sentences when splitting clarifies. Combine sentences only when
   combining does not hide a distinction. Cut repetition unless it is deliberate. Prefer short
   ordinary words and literal phrasing. Avoid attaching physical verbs or adjectives to abstract
   subjects when it makes meaning vague — say what actually happens.

5. **Verify against both tables.** This is the discipline that prevents silent drift; do not
   skip it. Cross-check the meaning map and the revised plan against the final text:
   - **Every O-row coverage.** Every O-row in the meaning map must appear in the "From" column
     of the revised plan, or be explicitly listed below the plan as `intentionally cut: <one-
     line reason>`. No silent drops.
   - **No orphan revised ideas.** Every R-row in the plan must reference at least one O (or A)
     row. A revised sentence carrying an idea with no source row is an invented fact — remove
     it or trace it back to the source.
   - **Inferences declared.** Any "implied (inferred)" idea promoted into the rewrite must be
     flagged in the revised plan's "Change made" column as a deliberate inference. Inferences
     are never silently treated as explicit source content.
   - **Force preserved.** Re-read the source and the rewrite side by side. If the source had
     blunt phrasing, short emphatic sentences, contrast, repetition for emphasis, or a sharp
     claim, confirm each survived. Politeness creep is a defect.
   - **Reads aloud.** Speak the rewrite. If you stumble, rephrase. A listener should follow
     it on first hearing.

   If any check fails, fix the rewrite — do not paper over it in the explanation.

## Output format

### For short or simple input

````
### Fully corrected text

```text
{corrected text}
```

### Corrections made

- {brief change}, or "no correction needed"
````

### For longer or layered input

````
### 1. Meaning map of the original text

| ID | Original sentence or fragment | Explicit ideas | Implied ideas (inferred) | Depends on | Supports | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| O1 | … | … | … | … | … | … |

A single sentence can carry several ideas. Split them in the cell (one per line, or numbered)
so each one can be tracked separately through the rewrite.

### 2. Revised sentence plan

| Revised ID | From | Revised sentence | Ideas preserved | Depends on | Supports | Change made |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | O1 | … | … | … | … | … |

### 3. Fully corrected text

```text
{corrected text}
```

### 4. Corrections and reasoning

- spelling / grammar / punctuation fixes
- wording simplifications
- sentences split, combined, removed, or reordered
- repetition removed or compressed
- ambiguities or inferences intentionally left out of the final text
````

Always wrap the final corrected text in a `text` fenced code block so the user can copy it
cleanly.

## Style guidance

- Aim for a high idea-to-word ratio: keep meaning, cut wording.
- Prefer active verbs and concrete subjects.
- Use a casual, conversational tone when the source allows it.
- Write so a listener can follow it on first hearing — no rereading required.
