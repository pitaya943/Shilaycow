---
name: shilaycow-plan
description: "Use once a brief is approved, to design the system's shape when its scenarios leave it open, then cut the work into tickets with an order and a risk level each. Don't use before the brief is approved: use /shilaycow to agree one."
---

# Plan

Cut the work into thin vertical tickets, say what must come before what, and mark what can run in parallel.

## Inputs

`docs/tasks/<slug>/brief.md`, `design.md` if it exists, and `.shilaycow/pitfalls.md` if it exists.

## Done when

The work is cut into pieces someone else could pick up cold, every scenario in the brief is covered by one of them, and it is clear what must come before what. Where you write that down, and in what form, is yours to judge; `docs/tasks/<slug>/plan.md` and `tickets/` is the usual place.

## How

None of this is required; it is what tends to help. Vertical slices work better than layers: when a piece is done, a scenario or part of one can be driven end to end. Say for each piece which scenarios it serves, what it depends on and which areas it touches, so pieces that share nothing can run at once; pieces that change the same files go one after the other, since builders working in parallel cannot see each other's decisions. Size a piece so one session can finish it. Whatever form a ticket takes, it has a `Status:` line (`open` or `done`: the builder sets it in the ticket's own file; for tickets kept as rows of one shared table, the orchestrator sets it when it lands the ticket, so parallel builders never edit the same file) and a `Risk:` line (`shilaycow-blast-radius`); tickets kept as rows of a table in `plan.md` have a column for each. Work the orchestrator will do itself is a ticket too, with its own level. Put shared groundwork first. If the project has no `try-<app>` skill yet, the first ticket that leaves something runnable ends by creating it with `shilaycow-try-it`; it cannot be written before there is an app to start.

Write each ticket's check so that it fails every time without the change, never by timing or luck, and can actually be met: run it against the code as it is and see it fail before you hand the ticket over. A ticket meant to keep behaviour as it is (a refactor, an implementation swapped behind the same interface) has nothing to fail today: its check must fail when that behaviour is broken, so break it in a throwaway copy, see the check fail, and restore it. A check that already passes for a ticket meant to change behaviour, or that nothing could satisfy, is the plan's mistake, and the builder will lose time finding that out. A check guards the ticket only once; where it holds a property a later change could undo (one place for a value, an order, a limit), the ticket also adds a test of it to the suite, so the next task runs it too. Read the pitfalls and shape tickets to avoid them. A ticket that changes how a user starts or uses the product updates `try-<app>` in the same ticket, so the next verification still exercises everything.

## When the shape is open

When the scenarios leave the system's shape open (new parts, new data, a new boundary, a high-risk ticket), work backward from them to that shape first, so the plan and the code follow from what the user asked for and nothing else, and write it as `docs/tasks/<slug>/design.md`: someone could build from it without asking what you meant, and every scenario has a place in it. Views worth considering, a table or a diagram each: the parts and the boundaries between them; what data enters, what transforms it and where it rests; the types and signatures at each boundary; one scenario traced end to end; who must learn that something happened; and which single owner holds each piece of state. Anything that points back to no scenario is probably extra. Sketching a second, different shape before committing often shows what the first one costs; a good shape has one owner per piece of state, one supported way to do each thing, and asks the least of its callers. With the user present, design in conversation. When implementation later proves the design wrong, change it and add a trail row; never change the scenarios to match.

## Stop when

- A scenario cannot be met without changing the brief. Go back to the user; the scenarios are theirs.
- The design needs a fact only running something can settle. Settle it with a throwaway prototype on a `spike/` branch, record the result in the trail, and bring back the decision, not the code.

## Outputs

The plan, wherever you kept it. Re-cut it whenever the work shows it was wrong, and note that in the trail.
