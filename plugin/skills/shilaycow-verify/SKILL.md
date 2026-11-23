---
name: shilaycow-verify
description: Use to judge the pull request the owner is about to merge, from a session that built none of it; also any ticket that deserves a second look before it is merged into the task branch. Posts PASS or FAIL for one commit.
---

# Verify

Judge the work cold. You did not build it, you do not fix it, and nothing the builder claims counts until you have seen it yourself.

## Inputs

The pull request or task branch, its ticket, the scenarios and Critical areas in `docs/tasks/<slug>/brief.md`, and the project's `try-<app>` skill, if it has one. Not the builder's conversation, and not a summary written for you. If you built any of this work, stop: someone else verifies it.

## Done when

You have checked, on a clean checkout of the head commit, and recorded evidence for each:

1. **Tests**: the full suite passes.
2. **Scenarios**: each scenario the work serves is shown by a test or by a driven action. For a pull request into `main`, `docs/spec/` also says what the work now makes true (a documents-only task is checked as described below): every scenario it adds or changes is under Scenarios as built, and nothing under it is made false.
3. **The real thing**: you followed the "how to try it" steps with `try-<app>` and they work as written. Where there is no `try-<app>` (a library with nothing to start, or work before the ticket that creates it), follow the brief's manual steps by hand instead, and say so.
4. **Tests that can fail**: for each scenario shown by a test, you broke the behaviour in a throwaway copy and the test failed; and its expected values come from the scenario, not from the code under test.
5. **What went unsaid**: anything the diff changes that neither the description nor the trail mentions. And what the brief never settled: try the extremes a user could reach (very long, very many, empty, repeated, two at once) and list what happens as `unspecified`, for the owner to decide. These are not defects.
6. **The code itself**: read it as the person who will maintain it, against `shilaycow-principles`. Is there work no scenario asked for, a smaller change that would have done, a leftover of an abandoned attempt, state with two owners? Go through the diff file by file, and cite a file and line for every conclusion, the favourable ones too: a judgement with nothing cited was not made. For low-risk work, scan the diff instead of reading it closely: confirm it touches only what its level says, which is also how a level set too low is caught.

How deep you go follows risk (`shilaycow-blast-radius`). Before you start, set each ticket's level again from its diff: you may raise the level the plan gave it, never lower it, and say why when you raise it. Changes on the branch that came from no ticket, such as the Chief's own commits or a merge resolution, count as a ticket of at least medium. Low only scans the diff for check 6; medium does every check; high also breaks every behaviour instead of a sample and runs `shilaycow-blast-radius` on that ticket's diff.

For a pull request into `main` that changes the system's code, also run `shilaycow-blast-radius` against `main`.

A task whose deliverable is documents only (a specification, a design, a roadmap) has nothing to run: say that checks 1, 3 and 4 do not apply. Check instead, with a file and line for each, that its scenarios are under Not yet built and none was added under Scenarios, that each matches the brief, that none contradicts a scenario already under Scenarios, that the design gives every scenario a place, and that the roadmap gives every Not yet built scenario exactly one task.

Then one comment is posted that starts `## Verification: PASS` or `## Verification: FAIL`, names the full head commit, and lists the checks with their evidence. With no pull request yet, post it on the tracking issue.

## The verdict

It is a **FAIL** when any of these is true:

- the suite fails, or a scenario this work serves is not shown;
- for a pull request into `main`, the spec contradicts what the work does, or lacks a scenario the work added;
- the "how to try it" steps do not work as written;
- a test still passes with its behaviour broken, or takes its expected value from the code it tests;
- a behaviour is reported as proven with neither a test nor a recorded driven check;
- the diff makes a significant change nobody mentioned;
- the same state has two owners that can disagree, or leftover code changes behaviour beyond the scenarios;
- for a pull request into `main`, a `shilaycow-blast-radius` fact is false and something existing depends on it;
- for a documents-only task, any of its checks above is false.

Mark each failed item **defect** or **gap**. It is a gap only when users can already do what its scenario says, you saw it work, and what falls short is the proof or the documents around it: a test missing or unable to fail at low or medium risk, a report or repeated figure out of step, a spec that leaves something out. A spec whose Scenarios say something the work makes false is a defect: the next task starts from it. Anything else is a defect, and at high risk every failed item is a defect. Gaps still make the verdict a FAIL; they tell the Chief when to stop fixing.

Otherwise it is a **PASS**. Anything else you found (a defect outside the scenarios, an unspecified input, a weak spot, everything else from reading the code) goes under a `### Findings` heading in the same comment, each with how to reproduce it. A finding never turns a PASS into a FAIL, and is never left out to keep a PASS clean.

## How

Evidence is a command and its output, a screenshot, a file and line: never a sentence. A FAIL says which check failed (and which scenario, when one is involved), how to reproduce it and what you saw, so the builder need not guess. For each failed item it also says where else you searched for the same kind of mistake and what you found there: the fix round fixes the class, not only the one place you happened to see.

Work in a fresh worktree at the head commit, and break behaviours only in a throwaway copy. On a large change, sample the low and medium tickets: every scenario's main test, then as many others as the time allows, and say what you sampled. "How to try it" means the brief's steps for the scenarios this work serves, run through `try-<app>`. Write in the language set by `report_language`, keeping the heading line in English.

## A fix round

When you are given the verdict before this one, judge what changed since then, not the whole branch again: run the full suite; redo every check that verdict failed, with the search for its class; read the diff between the two heads against `shilaycow-principles`; and break the behaviours that diff touches. Name the earlier verdict in yours. If the diff changes code the product runs, rather than tests, documents or developer tools, do every check again as for a first verdict. A merge of `main` into the branch is judged the same way.

## Stop when

- `try-<app>` no longer works as written. Report "try-it is stale"; that is not a FAIL of this work, unless this work is what created or changed it.
- You cannot run the project at all. Say what is missing.

## Outputs

One comment, never edited afterwards; a new head needs a new verdict. You push nothing to the branch you judge and you never merge.
