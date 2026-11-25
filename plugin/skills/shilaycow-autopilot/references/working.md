# Working

Read this before you cut the work into tickets.

## The skills you will most often reach for

In the order they usually help: `shilaycow-design` when the brief leaves the system's shape open (the owner may have skipped it with the Chief), `shilaycow-plan` to cut the work into tickets, `shilaycow-prove` for every behaviour you build, `shilaycow-try-it` to run the real app, `shilaycow-blast-radius` for each ticket's risk and before the task goes to `main`, then `shilaycow-spec`, `shilaycow-report` and `shilaycow-retro` at the end. None is a step you must pass; skipping one is a decision, so put it in the trail. The task that adds the project's first test suite also sets `test_command` in `.shilaycow/config.yml`, in its own pull request.

## Risk decides how closely work is checked

How closely work is checked follows its risk, not the size of the task. Every ticket carries a risk level (`shilaycow-blast-radius`), and work you do yourself goes in a ticket with a level like any other. A high ticket is designed before it is built, with a second shape weighed, and verified on its own before you merge it into the task branch; for the others, whether one deserves its own verification is your call. The brief's Critical areas are the owner's word on what is high in this project.

## Evidence

Builders prove their own work by seeing each test fail (`shilaycow-prove`); they do not run mutation sweeps. Breaking every behaviour of a high ticket is the verifier's check, and doing it twice doubles the cost of every round. What is committed as evidence is the short record: the command, the commit, the result and the lines that show it. Long output goes in a collapsed block of the `Ready.` or verdict comment, or is not kept; transcripts and mutant logs on the task branch end up in `main`.

## Mistakes that repeat

`/shilaycow-chief` has already folded what earlier tasks learned into `.shilaycow/pitfalls.md` on the task branch; builders read it there. A mistake of the same class found twice within this task is a pitfall already: add it to `.shilaycow/pitfalls.md` on the task branch and do what `shilaycow-correct` asks before the next fix. If the owner defers a correction, open a `later` issue for it, so it is not lost.

## What you leave behind

Enough that the owner can follow and a restarted run can resume: the goal list kept current (`references/starting.md`), a line on the tracking issue each time something lands or waits, and a trail (`shilaycow-trail`) of the decisions you made in place of asking.
