---
name: shilaycow-sharpen
description: Use at the start of any task, and whenever a goal is vague, large or new, to say back what the user wants and turn it into a task brief of plain-language scenarios they approve.
---

# Sharpen

Turn an idea into a brief that someone could check the finished work against. The brief is what the user approves, what `shilaycow-design` starts from and what `shilaycow-verify` accepts against.

## Inputs

The user's idea. The repository as it is. `docs/spec/` if it exists: read its index, `roadmap.md` if there is one (its next task is usually this one), and the areas the idea touches before asking anything.

## Done when

Before any question, you said back in your own words what the user wants: the goal, the problem behind it, the smallest change that would meet it, and one thing you are assuming that they did not say. They confirmed or corrected it.

Then `docs/tasks/<slug>/brief.md` exists with these headings filled in:

- **Goal**: what will be true for the user.
- **Out of scope**: what is deliberately left out. Never empty.
- **Scenarios**: scenarios `S-1`, `S-2`, ... as Given / When / Then, in the user's own vocabulary, with no class, table or file names. When the project has a spec, say for each scenario which area it belongs to and whether it is new, changes one that is there, or removes one.
- **How to try it**: how a person would try the result by hand.
- **Critical areas**: the parts of the system where any change is high risk whatever its size (money, permissions, the data model, ...), named as the user would or by path. The user's call; write None if there are none.
- **Assumptions**: what the scenarios leave open that a user will still run into, each with the default you chose. Think of limits (how long, how large, how many), empty and repeated input, several people at once, how long data is kept. Do not ask about each; decide, and lay the decisions out where the user will see them when approving.

And for every scenario you can name a test that would fail today (or, for one that keeps behaviour unchanged, a test that fails when that behaviour is broken), or a manual step that would show it. No scenario promises more than such a check can show: instead of "all", "any" or "wherever" for what a check covers, say what it looks at.

## How

- Restate first. Use your own words, not the user's phrasing rearranged, and prefer the narrow reading of the request: say what you would leave out. A misunderstanding caught here costs nothing.
- Write a first draft of the brief from what you already know, then ask about the gaps. Keep the file current as answers arrive.
- Ask the user about outcomes only: how they will use it, what counts as failure, what they would be upset to find missing. Offering your recommended answer with each question lets them accept in a word.
- Answer technical questions yourself by reading the repository (`shilaycow-how`, `shilaycow-why`). Do not ask the user what the code can tell you.
- Write the brief in the language set by `report_language`, English by default, keeping the headings in English.

## Stop when

- The user says it is enough. Write what is still unknown under the scenario it affects, as an assumption.
- The idea is several tasks: more than one pull request a person could review closely. Say so, propose the chain as `docs/spec/roadmap.md` (`shilaycow-spec`), and sharpen only the first. Order it so that what is hardest to change later comes first, nothing comes before what it depends on, and every task after the first leaves something a user can try. For a large system the first task's deliverable is the specification itself: documents only, its scenarios under Not yet built.

## Outputs

`docs/tasks/<slug>/brief.md`. The task does not proceed to unattended work until the user explicitly approves it.
