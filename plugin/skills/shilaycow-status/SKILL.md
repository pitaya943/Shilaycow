---
name: shilaycow-status
description: "Use to ask where things stand and what to type next, or which skill fits a job you describe. Read only: it points, never runs. Don't use to start or change a task: use shilaycow-chief."
disable-model-invocation: true
---

# Status

The entry point when the user is not sure what to do. Say where things are, or which skill fits the job, without changing or starting anything.

## Inputs

What the user typed after the command, if anything. `.shilaycow/config.yml`, `docs/spec/roadmap.md` if it exists, the task folder on `task/<slug>` (in manual mode, on whatever branch the user keeps it), open pull requests with their CI and verdicts, the tracking issue and its goal list (the comment marked `<!-- shilaycow:goal-list -->`), and open `needs-owner` and `later` issues. The descriptions of the installed skills, which say when each one applies and when another fits better.

## Done when

**Typed alone, or with a question about progress**, your reply gives, in this order:

1. **Waiting on**: the one thing blocking progress and who holds it (a pull request for the owner to merge, a `needs-owner` issue to answer, a session at work, nothing).
2. **Where the task is**: the phase, tickets done out of total, in a chain of tasks which task of the roadmap this is, and how many `later` issues are open.
3. **Next**: one step, with the command to type. If your session tools show an autopilot session working on the task, say which, and do not offer `/shilaycow-autopilot`: a second run cannot corrupt the task, but it duplicates the work. A brief with a `brief-approved` row and no `autopilot-start` row after it is waiting for `/shilaycow-autopilot`; one without a `brief-approved` row is waiting for the user to approve it with `/shilaycow-chief`. With no task open and a roadmap, list its tasks in order as done (with their pull requests), next and remaining, and give `/shilaycow-chief` to start the next one; with no roadmap, say nothing is open and the next task is the user's to name.

**Typed with a job** ("I want to understand the payment code", "I am about to change the retry logic"), your reply names the one to three skills that fit, in the order to use them, each with the command and one line on why it fits rather than the skill it is most easily confused with. Choose from the descriptions, which say when not to use each skill. Any skill but `/shilaycow-chief` and `/shilaycow-autopilot` can be typed directly in either mode. A whole task, meaning work that should end in a pull request, is `/shilaycow-chief` in auto mode. If the job could mean two different things, ask that one question and stop: do not answer both readings. If no skill fits, say so rather than stretching one.

With no config, or `mode: manual`, say the project is in manual mode, where `/shilaycow-chief` and `/shilaycow-autopilot` do not run, and that `shilaycow-setup` turns on auto mode. A whole task there goes by hand in this order: `/shilaycow-sharpen`, `/shilaycow-design` if the shape is open, `/shilaycow-plan`, building each ticket with `/shilaycow-prove`, and `/shilaycow-verify` from a fresh session.

## How

Read from the repository and GitHub each time; trust nothing remembered. Keep it to a few lines. Point, never run: the user types the command, so the choice stays theirs.

## Stop when

- GitHub cannot be reached. Report what the repository alone shows and say what is missing.

## Outputs

A reply in the conversation. Nothing is written, pushed, commented or started.
