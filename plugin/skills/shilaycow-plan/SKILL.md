---
name: shilaycow-plan
description: Use once a brief (and a design, when the task needs one) is approved, to cut the work into tickets before building.
---

# Plan

Cut the work into thin vertical tickets, say what must come before what, and mark what can run in parallel.

## Inputs

`docs/tasks/<slug>/brief.md`, `design.md` if it exists, and `.shilaycow/pitfalls.md` if it exists.

## Done when

The work is cut into pieces someone else could pick up cold, every scenario in the brief is covered by one of them, and it is clear what must come before what. Where you write that down, and in what form, is yours to judge; `docs/tasks/<slug>/plan.md` and `tickets/` is the usual place.

## How

None of this is required; it is what tends to help. Vertical slices work better than layers: when a piece is done, a scenario or part of one can be driven end to end. Say for each piece which scenarios it serves, what it depends on and which areas it touches, so pieces that share nothing can run at once. Size a piece so one session can finish it. Whatever form a ticket takes, it has a `Status:` line (`open` or `done`; the builder sets it) and a `Risk:` line (`shilaycow-blast-radius`). Work the Chief will do itself is a ticket too, with its own level. Put shared groundwork first. If the project has no `try-<app>` skill yet, the first ticket that leaves something runnable ends by creating it with `shilaycow-try-it`; it cannot be written before there is an app to start.

Write each ticket's check so that it fails every time without the change, never by timing or luck, and can actually be met: run it against the code as it is and see it fail before you hand the ticket over. A ticket meant to keep behaviour as it is (a refactor, an implementation swapped behind the same interface) has nothing to fail today: its check must fail when that behaviour is broken, so break it in a throwaway copy, see the check fail, and restore it. A check that already passes for a ticket meant to change behaviour, or that nothing could satisfy, is the plan's mistake, and the builder will lose time finding that out. A check guards the ticket only once; where it holds a property a later change could undo (one place for a value, an order, a limit), the ticket also adds a test of it to the suite, so the next task runs it too. Read the pitfalls and shape tickets to avoid them. A ticket that changes how a user starts or uses the product updates `try-<app>` in the same ticket, so the next verification still exercises everything.

## Stop when

- A scenario cannot be sliced without a design decision that was not made. Go back to `shilaycow-design`.

## Outputs

The plan, wherever you kept it. Re-cut it whenever the work shows it was wrong, and note that in the trail.
