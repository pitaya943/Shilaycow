---
name: shilaycow-spec
description: "Use to read docs/spec/ when a task starts, to check an area against the code for drift, to fold a task's scenarios in before its pull request, or to build a spec for a project with none. Don't use to write one task's brief: use shilaycow-chief, or shilaycow-sharpen in manual mode."
---

# Spec

Keep one description of what the system does now, so that nobody has to rebuild it from the history of tasks. A task's brief says what is about to change; the spec says what is true.

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

While work is a chain of tasks, `docs/spec/roadmap.md` lists them in order, each with its slug, one line on what a user can do once it is merged, the Not yet built scenarios it will build, and its pull request once there is one. Every Not yet built scenario belongs to exactly one task in it. A later task whose scenarios are not agreed yet says so on its line instead, and its own brief adds them; then no area needs a Not yet built section for it. The owner approves the roadmap as they approve a brief: a `roadmap-approved <commit>` row in the trail. The index links to it.

And when a task has been folded in:

- every scenario it added is there, and every scenario it changed reads as the system now behaves, with the old wording gone;
- scenarios it removed are gone;
- the brief's assumptions that were built are under Rules;
- nothing left in the spec is made false by the work;
- in a chain, the task's line in the roadmap names its pull request, once that pull request is open; if this task showed the later tasks are in the wrong order, that is a question for the owner, who approved the roadmap, not a change to make.

The spec changes in the same pull request as the code, so the two are judged and merged together.

## How

Write in the present tense, with these headings in English. Scenarios holds only what is true now; the one place for what is agreed but not built is Not yet built. The spec has no history: that is in `docs/tasks/` and the trail. Fold by area, not by task: a section per task turns the spec back into a history.

Let the tree grow only when it has to. A small system is one area file. When an area grows past what a reader can hold at once (about 150 lines is a fair sign), make it a folder, `<area>/index.md` with a file for each part, and keep the links in the index working.

To build a first spec for a project that has none, write what you can show: read the tests, run the product (`shilaycow-how`, `try-<app>`), and mark anything you inferred and could not run as unverified. Write in English.

## Drift

A spec that is wrong misleads every task that starts from it, so it is checked as well as written. To check one or more areas against the code as it is now, read `references/drift.md` and follow it. The check changes nothing; the owner decides, item by item, whether the spec or the code is wrong.

## Stop when

- The code and the spec disagree and nothing in the task says which is right. Do not pick one silently: ask the user, or when unattended note it in the trail and under the report's doubts.
- A scenario fits no area without inventing structure the users would not recognise. Say so, and propose the new area.

## Outputs

`docs/spec/`. `shilaycow-sharpen` reads it before writing a brief, `shilaycow-verify` checks it against the work, and `shilaycow-how` starts from it.
