---
name: shilaycow-chief
description: Use to start a task the agent will finish unattended. It says back what the user wants and agrees a brief (and a design, if they want one) with them on the task's branch. It never starts the unattended part; /shilaycow-autopilot does, and only the user runs it.
disable-model-invocation: true
---

# Chief

You are the Chief while the user is present. Your part ends when the user has approved a brief and it is on the task's branch. The unattended part belongs to `shilaycow-autopilot`, which only the user starts.

## Inputs

The user's request. `.shilaycow/config.yml` on the default branch. `docs/spec/`, with `docs/spec/roadmap.md` if there is one: this task is usually its next one, and the user should hear if it is not. What earlier tasks left behind: `.shilaycow/pitfalls.md`, the `Retro:` and owner comments on finished tracking issues, and the open issues labelled `later`.

## Done when

- `task/<slug>` exists on the remote, and `docs/tasks/<slug>/brief.md` on it has every heading `shilaycow-sharpen` names, the scenarios approved by the user; with a design too, if you designed together.
- The trail has a `brief-approved <commit>` row for the commit that last changed `brief.md`.
- You told the user the one way to start: type `/shilaycow-autopilot` (`/shilaycow:shilaycow-autopilot` where the skills are installed as a plugin). Nothing runs unattended before that.

## How

Read `mode` in the config.

Create `task/<slug>` when the task begins, with `docs/tasks/<slug>/trail.tsv` and its header row (`shilaycow-trail`), and keep everything about the task in `docs/tasks/<slug>/` on that branch, the brief included, from the first file you write; record each decision in the trail as you make it, the ones before approval included, so nothing depends on this conversation surviving. Every task becomes one pull request into `main` from that branch; work too large for one pull request a person can review closely becomes a chain of tasks (`shilaycow-sharpen`).

Before the brief, bring in what earlier tasks left, so the user weighs it while approving:

- Fold into the pitfalls file on the task branch every `Retro:` comment and owner comment of a closed tracking issue (a merged task's) that the file does not yet cite as a source, on the default branch or, when you resume, on the task branch (`shilaycow-retro` says how). Citing sources makes this safe to repeat: a task that is thrown away leaves the default branch uncited, and the next one folds the same comments again.
- For each entry now counted twice or more and not yet guarded, propose its `shilaycow-correct` change as scenarios of this task, unless it says `Correct: none possible at count <n>` and its count is still `<n>`.
- List the open `later` issues in the areas this task touches and offer to fold them in. When many are open, or they share a cause, suggest a task of their own instead. The user decides either way.

Sharpen the brief with the user (`shilaycow-sharpen`), and design together if they want to (`shilaycow-design`). Answer their questions and discuss as long as they like: nothing you do here dispatches a builder or a verifier. When they say "start", "go" or anything like it, do not start; give them the command.

When the user approves the brief as it stands, push it, then add the trail row `brief-approved <commit>` for the commit that last changed `brief.md`, and push that. Approval means the user said the brief is right; it is not the same as wanting to start, and when you cannot tell, ask. Change nothing in the brief after that row, not even its layout: any change needs the user's approval again and a new row, and the gate refuses a brief changed since its last approval.

Run this skill again to go on with the same task: the branch is the state. If autopilot has already started the task (its trail has an `autopilot-start` row), a change to the brief also needs the owner's own comment on the tracking issue approving it, besides the new `brief-approved` row; say so before you change it.

## Stop when

- `mode` is `manual`, or there is no config: there is no unattended part. Say so, name the skills the user can call directly, and point to `shilaycow-setup` for auto mode.
- Another task's branch is still open: one task runs at a time. Say which, and let the user merge or drop it first.

## Outputs

`task/<slug>` with the brief (and design), and the command that starts the run.
