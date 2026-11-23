---
name: shilaycow-status
description: Use to find out where a task stands, who it is waiting on and what to do next. Read only.
---

# Status

Say where things are, without changing anything.

## Inputs

`.shilaycow/config.yml`, `docs/spec/roadmap.md` if it exists, the task folder on `task/<slug>` (in manual mode, on whatever branch the user keeps it), open pull requests with their CI and verdicts, the tracking issue, and open `needs-owner` and `later` issues.

## Done when

Your reply gives, in this order:

1. **Waiting on**: the one thing blocking progress and who holds it (a pull request for the owner to merge, a `needs-owner` issue to answer, a session at work, nothing).
2. **Where the task is**: the phase, tickets done out of total, in a chain of tasks which task of the roadmap this is, and how many `later` issues are open.
3. **Next**: one step, with the command to type. A brief with a `brief-approved` row and no `autopilot-start` row after it is waiting for `/shilaycow-autopilot`; one without a `brief-approved` row is waiting for the user to approve it with `/shilaycow-chief`.

With no config, or `mode: manual`, say the project is in manual mode, name the skills that can be used directly, and say that `shilaycow-setup` turns on auto mode.

## How

Read from the repository and GitHub each time; trust nothing remembered. Keep it to a few lines.

## Stop when

- GitHub cannot be reached. Report what the repository alone shows and say what is missing.

## Outputs

A reply in the conversation. Nothing is written, pushed, commented or started.
