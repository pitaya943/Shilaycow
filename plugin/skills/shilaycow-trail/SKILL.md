---
name: shilaycow-trail
description: Use during a task in auto mode, or when the user asks for a decision log, to record each decision as it is made, so a reviewer who stepped away can trust the result without rebuilding the process.
---

# Trail

Keep one log, one row per decision. It is the other half of not asking on reversible work: you do not ask, and you always leave a record.

## Inputs

The decision you just made, and where its evidence is.

## Done when

`docs/tasks/<slug>/trail.tsv` has a row for every point where another reasonable person might have chosen differently: above all an assumption made in place of a question, and anything the owner would be surprised to learn only afterwards.

Each row says what was decided, why in plain words, and where the evidence is: a pointer (commit, pull request, `file:line`), never a paragraph. With a timestamp and who decided: `owner`, `chief`, `autopilot`, `builder T-<nn>` (a fix round's builder too) or `verifier`, and no other names. Rows stay in the order they were added; a builder's rows keep the times it decided them. The file's first line is a header naming its columns; the first writer chooses them, and every row after follows that header, whoever writes it. Take timestamps from the clock (`date -u +%Y-%m-%dT%H:%MZ`), never write them by hand. A row the gate reads, `brief-approved <commit>` or `autopilot-start <commit>`, keeps the word and its commit together in one cell, with nothing between.

## How

Write the row when you decide, not at the end. Append only: to reverse a decision, add a row. Routine steps are not decisions; do not log them.

A builder is given the header and posts its rows, in those columns, in its pull request's `Ready.` comment; the Chief adds them to the file when it merges that pull request into the task branch, fitting any that do not match.

## Stop when

Nothing stops this skill; it runs alongside the others.

## Outputs

`trail.tsv`. `shilaycow-report` builds the "decisions I made myself" section from it, and `shilaycow-verify` treats a significant change nobody mentioned as a failure.
