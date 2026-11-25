---
name: shilaycow-correct
description: Use when the same class of mistake has happened twice in a project, to propose a change that makes it impossible instead of another note asking agents to be careful.
---

# Correct

A mistake that recurs is the repository's fault, not the agent's. Change the repository so the next agent cannot make it.

Write the fix for the next contributor at their least careful: an agent with a narrow view of the code, which imitates what is nearby and stops at the first thing that passes. If what is nearby is right, and the wrong thing fails before review, that contributor gets it right without knowing why.

## Inputs

Entries in `.shilaycow/pitfalls.md` with a count of 2 or more that are not yet under `## Guarded`, and the commits, pull requests, review comments and `later` issues behind them.

## Done when

For each such class there is a change that fixes it at the highest rung that works:

1. **Architecture**: one owner per piece of state, one supported way per task, internals hidden so the wrong import fails, old ways deleted so they cannot be copied.
2. **Types**: the bad state cannot be written.
3. **A lint or check** whose error names what to use instead. If the pattern is already common, fail only when a change adds more.
4. **A test** of the behaviour.
5. **Documentation**, last.

And the new guard is shown failing on every past instance the pitfall entry lists, then passing on the fix. Re-apply each past mistake in turn and run the guard; one it does not catch is not covered. If all of the entry is covered, move it under `## Guarded` as one line: what it was, its `Sources:`, and the guard. Never drop the sources: the next fold reads them to know a Retro is already in. Otherwise cut the entry down to the part that still rests on someone remembering.

## How

Write the proposal for the owner in plain words: how many times this happened (with links), what the change stops, and what it costs (build time, what it forbids).

## Stop when

- The fix needs a change under `.github/`. You cannot push workflow changes. Put the exact change in the proposal for the owner to apply, and stop there.
- No rung above documentation works. Say so, keep the pitfall entry, and add to it the line `Correct: none possible at count <n> (<link>)`, so it is not proposed again until it happens more.

## Outputs

Usually scenarios in the brief of the next task, proposed by `/shilaycow-chief` and built as that task's tickets, so the change is verified with it. Called on its own, a proposal and a pull request. Only the owner merges either.
