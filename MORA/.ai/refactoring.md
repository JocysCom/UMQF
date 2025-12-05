## TASK

Your task is to review, improve, and simplify the whole process. The current process is overcomplicated and is failing to produce the desired results.

First, you must gain a complete understanding of the process by carefully reviewing **all** process-related files (instructions, README, agents, tools, and any other configuration or helper files that define behavior).

Simplify and update the process to make sure that it produces high-quality, reliable final results.
You can modify any part of the process files described in the "You can modify these files" section below, but you must not alter existing final result artifacts.

Be very careful, and create a plan that gradually simplifies and updates the instructions, because this process can be restarted multiple times from fresh. Don't change too much at once. Clean up unused agents or tools if redundant, because it will reduce your cognitive load. Provide the reason for each change.

Why simplify? Because each new sentence added waters down other rules and increases complexity. You must avoid repeating the same ideas and have the maximum possible meaning/words ratio. Stick to the single source of truth principle.

Think very hard - your and my future survival depends on it.

## CONTEXT

The main goal was simple:

1. Download the document specified by the user.
2. Analyze the document according to the morality formula described in the `UMQF.md` file.
3. Identify the main acting entities in the document.
3. Create a profile for each main acting entity in the document that performed an action suitable for UMQF:

   `analysis\{document}\entities\{entity}.md` - UMQ summary and evaluation of the entity.  
   `analysis\{document}\entities\{entity}-actions.md` - More detailed analysis of entity actions.

## HOW TO START

First, you need to read and analyze these documents:

1. Read your original system instructions: `.ai\instructions.md`
2. Read the help file: `README.md`
3. Analyze the `UMQF.md` file.
4. Read the example book: `analysis\exploration-team\source-document.md`
5. Identify all primary entities (action doers) involved and actions that can be evaluated from a UMQ point of view.
6. Read the entity UMQ actions example file (expected results): `analysis\exploration-team\entities\huyghens-actions.md`
7. Read the entity UMQ summary example file (expected results): `analysis\exploration-team\entities\huyghens.md`

Now you have a full understanding of what the main goal is, the starting instructions (1), and what result is expected (6–7).

After this, systematically review all remaining process-related files (especially in `.ai\`, `agents\`, and `tools\` folders) so you fully understand how the current process works before making any modifications.

You can't modify the `UMQF.md`, `source-document.md`, `huyghens-actions.md` and `huyghens.md` files.

You can modify these files:

- Any part of the `.ai\instructions.md` file
- Any part of the `README.md` file
- Any part of all files inside the `agents\` folder
- Any part of all files inside the `tools\` folder

You may also create, delete, merge, or restructure agents and tools files if that simplifies the process and improves reliability, as long as you do not change the protected files listed above or the already-produced final result artifacts.
