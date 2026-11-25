---
name: shilaycow-blast-radius
description: "Use before shared code ships or a task branch goes to main: finds what the change could break elsewhere, proves the facts its safety rests on, and sets each ticket's risk level. Don't use to decide whether a pull request is ready to merge: use shilaycow-verify."
---

# Blast radius

Find what a change breaks somewhere else, beyond the diff. Listing callers is not the job; the job is the breakage a search will not show, and proving the one or two facts the change's safety depends on.

## Inputs

A diff: a pull request, or a task branch against `main`.

## Done when

You have named the facts this change is safe because of, and for each one recorded what backs it. From weakest to strongest:

- **Belief**: it seems true. Not evidence on its own.
- **Citation**: a file and line, here or in the dependency's source, that says so.
- **Argument**: the path to the failure traced through the code, with the step that blocks it.
- **Execution**: a script or test that calls the real code and would fail if the fact were false.
- **Observation**: the fact seen to hold in the running app.

Every fact is backed by an argument, an execution or an observation, or says why none was possible.

## How

Look where a search does not: implicit ordering, shared state, defaults, serialised formats, what other code assumes about a return shape, what runs at import or start-up. Step 4 is usually one short script that imports what the app ships and calls the exact function. When an implementation is swapped behind an interface that is meant to stay the same, the script sends ordinary and extreme inputs (very large, very small, empty, malformed) to the old code and the new and compares every answer; do it before the first ticket is verified, not only at the end.

Do not hand back an essay. Hand back the facts, the level each reached, and the output that proves it.

## Risk level

Every ticket, and any work the Chief does itself, gets one level from what it touches, never from how large it is. The highest that applies wins:

- **high**: a data model or migration, authentication or permissions, money, anything irreversible or external, concurrency, code that most of the system calls (count the callers), or anything in the brief's Critical areas;
- **medium**: code or an interface that something else calls;
- **low**: none of these, such as documents, tests, or code inside one module that nothing else calls.

Write it with the signal that set it: `Risk: high (writes the orders table)`. Planning estimates it from the ticket; the verifier sets it again from the actual diff, and may raise it but never lower it.

## Stop when

- A fact turns out false. That is the finding: report it with the reproduction and stop polishing the rest.

## Outputs

A short list in the conversation, or inside a `shilaycow-verify` verdict or a final report when called from there.
