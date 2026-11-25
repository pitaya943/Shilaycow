# The checks

Read this before you start checking. Record evidence for each check on a clean checkout of the head commit: a command and its output, a screenshot, a file and line, never a sentence. When a check fails, search at once for the same kind of mistake elsewhere in the work and record where you looked and what you found: the verdict reports it, and the fix round fixes the class, not only the one place you happened to see.

## The six checks

1. **Tests**: the full suite passes.
2. **Scenarios**: each scenario the work serves is shown by a test or by a driven action, and each behaviour the description reports as proven has one or the other. Note any property guarded only by a ticket's own check script and not by the suite. For a pull request into `main`, `docs/spec/` also says what the work now makes true: every scenario it adds or changes is under the spec's `Scenarios` heading, and nothing already there is made false.
3. **The real thing**: you followed the "how to try it" steps with `try-<app>` and they work as written. Where there is no `try-<app>` (a library with nothing to start, or work before the ticket that creates it), follow the brief's manual steps by hand instead, and say so. "How to try it" means the brief's steps for the scenarios this work serves.
4. **Tests that can fail**: for each scenario shown by a test, you broke the behaviour in a throwaway copy and the test failed; and its expected values come from the scenario, not from the code under test.
5. **What went unsaid**: anything the diff changes that neither the description nor the trail mentions, including any part of the diff your paraphrase could not account for. One that changes behaviour a user or another part of the system can see is significant, and fails this check. And what the brief never settled: try the extremes a user could reach (very long, very many, empty, repeated, two at once) and list what happens as `unspecified`, for the owner to decide. The `unspecified` items are not defects.
6. **The code itself**: read it as the person who will maintain it, against `shilaycow-principles`. Is there work no scenario asked for, a smaller change that would have done, a leftover of an abandoned attempt, state with two owners? Go through the diff file by file, and cite a file and line for every conclusion, the favourable ones too: a judgement with nothing cited was not made.

## How deep, by risk

What each risk level means is in `shilaycow-blast-radius`: load it with your Skill tool (`shilaycow-blast-radius`, or `shilaycow:shilaycow-blast-radius` for a plugin install) before you set levels. Before you start, set each ticket's level again from its diff: you may raise the level the plan gave it, never lower it, and say why when you raise it. Changes on the branch that came from no ticket, such as the Chief's own commits or a merge resolution, count as a ticket of at least medium.

- **Low**: every check, with two lighter ones. Check 4 breaks one behaviour per scenario, the one its main test guards. Check 6 scans the diff instead of reading it file by file: confirm it touches only what its level says, which is also how a level set too low is caught.
- **Medium**: every check; check 4 as for low, then as many other behaviours as the time allows, saying which you broke.
- **High**: every check; check 4 breaks every behaviour the ticket touches; and `shilaycow-blast-radius` on that ticket's diff. For a pull request into `main`, one run against `main` covers this too, as long as it lists each high ticket's facts under its own heading.

## A pull request into main, in addition

- If it changes the system's code, run `shilaycow-blast-radius` against `main`.
- Compare `brief.md` at the head with the commit of the trail's last `brief-approved` row. Any difference, a status line or layout included, is a defect unless the owner approved it in a comment on the tracking issue and a newer `brief-approved` row names it.
- Check that the pull request and the task's tracking issue were opened by the config's `bot`.

## A documents-only task

A task whose deliverable is documents only (a specification, a design, a roadmap) has nothing to run: say that checks 1, 3 and 4 do not apply. Check instead, with a file and line for each, that its scenarios are under Not yet built and none was added under Scenarios, that each matches the brief, that none contradicts a scenario already under Scenarios, that the design gives every scenario a place, and that the roadmap gives every Not yet built scenario exactly one task.
