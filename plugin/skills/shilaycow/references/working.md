# Working

Read this before you cut the work into tickets.

## The skills you will most often reach for

In the order they usually help: `sc-plan` to design the system's shape when the brief leaves it open (the owner may have skipped that while agreeing the brief) and to cut the work into tickets, `sc-prove` for every behaviour you build, `sc-try-it` to run the real app, `sc-blast-radius` for each ticket's risk and before the task goes to `main`, then `sc-spec`, the pull request's description (`procedures/finish.md`) and a steward's Retro (`roles/steward.md`) at the end. None is a step you must pass; skipping one is a decision, so put it in the trail. The task that adds the project's first test suite also sets `test_command` in `.shilaycow/config.yml`, in its own pull request.

## Risk decides how closely work is checked

How closely work is checked follows its risk, not the size of the task. Every ticket carries a risk level (`sc-blast-radius`), and work you do yourself goes in a ticket with a level like any other. A high ticket is designed before it is built, with a second shape weighed, and verified on its own before you merge it into the task branch; for the others, whether one deserves its own verification is your call. The brief's Critical areas are the owner's word on what is high in this project.

## Evidence

Builders prove their own work by seeing each test fail (`sc-prove`); they do not run mutation sweeps. Breaking every behaviour of a high ticket is the verifier's check, and doing it twice doubles the cost of every round. What is committed as evidence is the short record: the command, the commit, the result and the lines that show it. Long output goes in a collapsed block of the `Ready.` or verdict comment, or is not kept; transcripts and mutant logs on the task branch end up in `main`.

## Mistakes that repeat

Agreeing the brief has already folded what earlier tasks learned into `.shilaycow/pitfalls.md` on the task branch; builders read it there. A mistake of the same class found twice within this task is a pitfall already: add it to `.shilaycow/pitfalls.md` on the task branch and correct it as `references/learning.md` describes ("Correcting a class") before the next fix. If the owner defers a correction, open a `later` issue for it, so it is not lost.

## What you leave behind

Enough that the owner can follow and a restarted run can resume: the goal list kept current (`procedures/run.md`), a line on the tracking issue each time something lands or waits, and a trail (`references/trail.md`) of the decisions you made in place of asking.
