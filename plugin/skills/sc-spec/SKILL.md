---
name: sc-spec
description: "Use when a task changes the system's shape, to fold its scenarios into docs/spec/ before its pull request; to keep the roadmap of a chain of tasks; or when asked, to check an area against the code for drift or build a first spec. Don't use to write one task's brief: use /shilaycow."
---

# Spec

Keep one description of the system's shape and behaviour as they are now, so that nobody has to rebuild it from the history of tasks. A task's brief says what is about to change; the spec says what is true.

## When it changes

A task updates the spec when it changes the system's shape: a new part, new data, a new boundary, or behaviour a user can see that the spec does not describe yet. A fix that makes the system do what the spec already says, a refactor, or an internal change leaves the spec alone. A project with no spec gets one when a task first changes its shape, or when the owner asks.

## Inputs

`docs/spec/` if it exists. When folding a task in: its `brief.md`, its `design.md`, and what was actually built. For a project with no spec yet: the code, the tests and any `docs/tasks/`.

## Done when

`docs/spec/index.md` says what the system is in two or three sentences, lists each area on one line with a link, defines once each term the scenarios use, and says what the system deliberately does not do.

An area is a part of the system as its users would name it (accounts, billing, search), never a layer (API, database, front end). `docs/spec/<area>.md` holds:

- one sentence on what the area is for;
- **Scenarios**: every scenario that holds now, as Given / When / Then in the user's words, each under a heading that names what the user does. Not a number: every task's brief numbers from one again;
- **Rules**: the limits and defaults that were decided (lengths, counts, empty and repeated input, several people at once, how long data is kept), each with the task that decided it;
- the tasks that last changed the area;
- **Not yet built**, only while a larger plan is agreed and not finished: scenarios the owner approved that are not built yet. The task that builds one moves it up to Scenarios.

While work is a chain of tasks, `docs/roadmap.json` lists them, so that any session computes the next one instead of guessing it:

```json
{"tasks": [{"slug": "store", "goal": "what a user can do once it is merged", "depends_on": [], "pr": null, "done": false}]}
```

`state.py` reads it from the default branch: it names the first task not done whose dependencies are done, and refuses a roadmap with a missing field, an unknown dependency, a loop, a done task with no `pr`, or an open task whose dependencies are not done. Every Not yet built scenario belongs to exactly one task: write the task's slug beside it in its area. A later task whose scenarios are not agreed yet has none there, and its own brief adds them. The owner approves the roadmap as they approve a brief: a `roadmap-approved <commit>` row in the trail, for the commit that last changed `docs/roadmap.json`. The index links to it.

And when a task has been folded in:

- every scenario it added is there, and every scenario it changed reads as the system now behaves, with the old wording gone;
- scenarios it removed are gone;
- the brief's assumptions that were built are under Rules;
- nothing left in the spec is made false by the work;
- in a chain, the task's entry in `docs/roadmap.json` has its pull request as `pr` and `done` true, in that same pull request, so the roadmap is done exactly when the task is merged; if this task showed the later tasks are in the wrong order, that is a question for the owner, who approved the roadmap, not a change to make.

The spec changes in the same pull request as the code, so the two are judged and merged together.

## How

Write in the present tense, with these headings in English. Scenarios holds only what is true now; the one place for what is agreed but not built is Not yet built. The spec has no history: that is in `docs/tasks/` and the trail. Fold by area, not by task: a section per task turns the spec back into a history.

Let the tree grow only when it has to. A small system is one area file. When an area grows past what a reader can hold at once (about 150 lines is a fair sign), make it a folder, `<area>/index.md` with a file for each part, and keep the links in the index working.

To build a first spec for a project that has none, write what you can show: read the tests, run the product (`sc-how`, `try-<app>`), and mark anything you inferred and could not run as unverified. Write in English.

## Drift

A spec that is wrong misleads every task that starts from it. When the owner asks for areas to be checked against the code as it is now, or a task finds the spec and the code disagree, read `references/drift.md` and follow it; it is not a step of every task. The check changes nothing; the owner decides, item by item, whether the spec or the code is wrong.

## Stop when

- The code and the spec disagree and nothing in the task says which is right. Do not pick one silently: ask the user, or when unattended note it in the trail and under the pull request description's doubts.
- A scenario fits no area without inventing structure the users would not recognise. Say so, and propose the new area.

## Outputs

`docs/spec/`. `/shilaycow` reads it before writing a brief, `sc-verify` checks it against the work, and `sc-how` starts from it.
