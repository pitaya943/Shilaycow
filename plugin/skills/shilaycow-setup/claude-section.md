## shilaycow

This repository uses shilaycow. Read what a task needs, when it needs it; this section only says where things are.

**The owner's standing permission.** Agents may create and push `task/`, `work/`, `spike/` and `chore/` branches and the setup branch. Never push to `main`; only the owner merges into it. Every push to a `task/` or `work/` branch is a compare-and-swap on the commit fetched; the project's hook says how when it refuses one.

**Where the state is.**

| What | Where |
|---|---|
| Settings | `.shilaycow/config.yml` on `main` (`owner`, `bot`, `mode`, `test_command`, `fix_rounds`) |
| A task | branch `task/<slug>`, folder `docs/tasks/<slug>/` on it |
| Its brief and decisions | `docs/tasks/<slug>/brief.md`, `docs/tasks/<slug>/trail.tsv` |
| Its progress on GitHub | the issue titled `Task: <slug>` |
| A ticket's work | branch `work/<slug>/T-<nn>` |
| What the system does now | `docs/spec/`; the order of upcoming tasks in `docs/spec/roadmap.md` |
| Lessons from earlier tasks | `.shilaycow/pitfalls.md` |
| Left for later, or waiting on the owner | issues labelled `later`, `needs-owner` |

**Where to start.** `/shilaycow-chief` agrees a task, `/shilaycow-autopilot` runs it, `/shilaycow-status` says where things stand, or which skill fits a job when you are not sure.
