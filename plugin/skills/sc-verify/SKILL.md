---
name: sc-verify
description: "Use to judge a pull request into main, or a ticket that deserves its own verdict, from a session that built none of it; posts PASS or FAIL for one commit. Don't use on work you built: start a fresh session."
---

# Verify

Judge the work cold. You did not build it, you do not fix it, and nothing the builder claims counts until you have seen it yourself.

## Inputs

The pull request or task branch, its ticket, the scenarios and Critical areas in `docs/tasks/<slug>/brief.md`, and the project's `try-<app>` skill, if it has one. Where the trail, the config, the tracking issue and the test command live is in the shilaycow section of `CLAUDE.md`. Not the builder's conversation, and not a summary written for you. If you built any of this work, stop: someone else verifies it.

## Done when

One comment is posted with the verdict for one head commit, built in these steps. Steps 2 and 3 name the file beside this one to read when you reach them; read it then, not from memory.

1. **Paraphrase first.** Before checking anything, write in your own words, from the brief and the diff alone, what this work changes and why (two to five sentences). Compare it with the pull request's description: where they differ, or where part of the diff fits nothing you can paraphrase, note it; it belongs to the check on what went unsaid. In a fix round, paraphrase the whole work, then say what the new commits change. A reader who cannot say what a change does cannot judge it.
2. **Check.** If you are given the verdict before this one, read `references/fix-round.md` first: it narrows what you redo. Then read `references/checks.md` and run its checks at the depth each ticket's risk calls for, with the additions for a pull request into `main` or a documents-only task.
3. **Decide and write.** Read `references/verdict.md`: what makes a FAIL, how to mark each failed item a defect or a gap, what goes under Findings, and the shape of the comment.

## How

Work in a fresh worktree at the head commit, and break behaviours only in a throwaway copy. Evidence is a command and its output, a screenshot, a file and line: never a sentence. Write in English.

## Stop when

- `try-<app>` itself is broken: it fails before it reaches the brief's steps. Say "try-it is stale" in the verdict comment; that is not a FAIL of this work, unless this work is what created or changed it. If `try-<app>` runs and the steps give the wrong result, that is check 3 failing.
- You cannot run the project at all. Say what is missing.

## Outputs

One comment, never edited afterwards; a new head needs a new verdict. You push nothing to the branch you judge and you never merge.
