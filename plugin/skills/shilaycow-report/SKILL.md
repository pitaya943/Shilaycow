---
name: shilaycow-report
description: Use at the end of a task to write what was done for the person who will decide whether to merge it. Produces the final report that the pull request into main links to.
---

# Report

Tell the owner what they are being asked to accept, in a form they can check without reading the diff first.

## Inputs

The task branch, `docs/tasks/<slug>/brief.md`, `design.md`, `plan.md`, `trail.tsv`, the Ready comments, the verdict comments and the CI results. Gather only from these; memory and impressions are not sources.

## Done when

A report exists at `docs/tasks/<slug>/reports/final.md` whose first sentence says whether, by your own check, every scenario is met, followed by these sections:

1. **What was done**: three to five plain sentences.
2. **How to try it**: written from zero, for someone who has never seen the project: getting the code and the right branch, installing, starting it, then each action with what they should see. Add two or three things worth trying that the tests do not cover. Every step and every claim about what happens was run by you for this report; one you could not run says so (`not run`), never what it would show.
3. **Decisions I made**: from the trail: each decision made without asking, with its reason in a line.
4. **Not done or in doubt**: never omitted; write None if there is nothing.
5. **Verification**: one line saying the independent verdict is posted as a comment on this pull request. You write the report before it exists, so claim no result.

And a table of every scenario in the brief: met or not, and a link to the evidence. And every ticket with its final risk level and the signal that set it, so the owner sees where verification was light. Every claim links to a pull request, commit, verdict or trail row.

## How

Write in English. Lead with the conclusion. Say less, link more.

## Stop when

- A scenario is not met. Do not open a pull request into `main`: write what is missing where the owner will see it (the tracking issue, or the conversation) and leave the decision to them.

## Outputs

The report file. The description of the pull request into `main` is the report's first sentence and a link to the file, not a copy: two copies drift apart when a fix round changes one of them.
