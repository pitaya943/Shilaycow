# Learning from mistakes

Read this as the steward, after a task's last verdict; and when agreeing the next task's brief, before you fold in what earlier tasks left. A mistake that happens once is noted where the next builder will read it; a mistake that happens twice is the repository's fault, and the repository changes so the next agent cannot make it.

## After a task: the Retro

Find what went wrong in this task that would go wrong again. Read first what the owner found wrong after merging earlier tasks (their comments on closed tracking issues), since each is something verification missed. Then this task: FAIL verdicts, the findings attached to PASS verdicts, fix rounds, CI failures, the owner's corrections and send-backs, the `later` issues it opened, and `trail.tsv`, against `.shilaycow/pitfalls.md`.

Work out what the pitfalls file should say after this task:

- each new pitfall has four lines: what happened (with a pull request or commit), how to avoid it, how many times it has happened, and `Sources:`, the links of the comments it came from (a `Retro:` comment, an owner comment);
- a pitfall of a class already listed raises that entry's count and adds its source instead of adding an entry; so does a class of gap that `later` issues from two tasks share;
- every entry kept passes three tests: it will still hold in six months, it would change what the next agent does, and it is not a one-off detail such as a version, a hash or a count;
- an entry may carry `Correct: none possible at count <n> (<link>)`; keep it, and when the count rises past `<n>` say so, since the entry is due again;
- the file holds at most 30 entries above its `## Guarded` section: merge near-duplicates or drop what no longer holds before adding, keeping their sources.

Group by cause, not by symptom: if you cannot write how to avoid it, you have not found the cause. If the cause is an unclear instruction in the harness rather than something about this project, report that separately; it is not a project pitfall.

The task branch is frozen once judged, so post the result as one `Retro:` comment on the tracking issue: the new entries, the entries whose count rises, and the entries now counted twice or more, which are due for a correction. Nothing that meets the three tests means an empty Retro, which is a fine result.

## Folding it in

The next task's agreeing folds into the pitfalls file, on its own branch, every `Retro:` comment and owner comment of a closed tracking issue whose link the file on the default branch does not yet cite. Citing comments, not issues, keeps a comment from being counted twice and lets an owner comment that arrives later still be folded.

## Correcting a class

For each entry counted twice or more and not yet under `## Guarded`, propose a change to the repository, written for the next contributor at their least careful: an agent with a narrow view of the code, which imitates what is nearby and stops at the first thing that passes. Fix it at the highest rung that works:

1. **Architecture**: one owner per piece of state, one supported way per task, internals hidden so the wrong import fails, old ways deleted so they cannot be copied.
2. **Types**: the bad state cannot be written.
3. **A lint or check** whose error names what to use instead. If the pattern is already common, fail only when a change adds more.
4. **A test** of the behaviour.
5. **Documentation**, last.

The proposal says in plain words how many times this happened (with links), what the change stops, and what it costs. It becomes scenarios in the brief of the next task, built as its tickets, so the change is verified with it; only the owner approves it.

The new guard is shown failing on every past instance the entry lists, then passing on the fix: re-apply each past mistake in turn and run the guard; one it does not catch is not covered. If all of the entry is covered, move it under `## Guarded` as one line: what it was, its `Sources:`, and the guard. Never drop the sources: the next fold reads them to know a Retro is already in. Otherwise cut the entry down to the part that still rests on someone remembering.

A fix that needs a change under `.github/` goes to the owner as the exact change to apply. When no rung above documentation works, say so, keep the entry, and add `Correct: none possible at count <n> (<link>)`, so it is not proposed again until it happens more.
