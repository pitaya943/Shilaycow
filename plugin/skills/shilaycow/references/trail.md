# The trail

Read this before you write the task's first trail row, and give a builder its rule on rows. Keep one log, one row per decision. It is the other half of not asking on reversible work: you do not ask, and you always leave a record.

## Inputs

The decision you just made, and where its evidence is.

## Done when

`docs/tasks/<slug>/trail.tsv` has a row for every point where another reasonable person might have chosen differently: above all an assumption made in place of a question, and anything the owner would be surprised to learn only afterwards.

Each row says what was decided, why in plain words, and where the evidence is: a pointer (commit, pull request, `file:line`), never a paragraph. With a timestamp and who decided: `owner`, `orchestrator`, `builder T-<nn>` (a fix round's builder too) or `verifier`, and no other names. Rows stay in the order they were added; a builder's rows keep the times it decided them. The file's first line is a header naming its columns; the first writer chooses them, and every row after follows that header, whoever writes it. Take timestamps from the clock (`date -u +%Y-%m-%dT%H:%MZ`), never write them by hand. A row `state.py` reads, `brief-approved <commit>` or `fix-round <T-nn or main>`, keeps the word and its argument together in one cell, with nothing between.

## How

Write the row when you decide, not at the end. Append only: to reverse a decision, add a row. Routine steps are not decisions; do not log them. The only rows anything reads are `brief-approved <commit>` and `fix-round <T-nn or main>`; do not copy other kinds of marker row from an earlier task's trail.

A builder is given the header and posts its rows, in those columns, in its pull request's `Ready.` comment; the orchestrator adds them to the file when it lands that pull request on the task branch, fitting any that do not match.

## Outputs

`trail.tsv`. The description of the pull request into `main` lists the decisions made without asking from it (`procedures/finish.md`), and the verifier treats a significant change nobody mentioned as a failure.
