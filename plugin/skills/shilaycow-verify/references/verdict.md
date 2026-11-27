# The verdict

Read this when the checks are done, before you write the comment.

## FAIL

It is a **FAIL** when any of these is true:

- the suite fails, or a scenario this work serves is not shown;
- for a pull request into `main`, the spec contradicts what the work does, or lacks a scenario for behaviour a user can see that the work added (a fix or a refactor that leaves that behaviour as the spec says needs no spec change; for a documents-only task, its scenarios belong under Not yet built: `references/checks.md`);
- the "how to try it" steps do not work as written;
- a test still passes with its behaviour broken, or takes its expected value from the code it tests;
- a behaviour is reported as proven with neither a test nor a recorded driven check;
- the diff makes a significant change nobody mentioned;
- the same state has two owners that can disagree, or leftover code changes behaviour beyond the scenarios;
- for a pull request into `main`, a `shilaycow-blast-radius` fact is false and something existing depends on it;
- for a pull request into `main`, it or the task's tracking issue was opened by an account other than the config's `bot`: the run acted as someone else, which no other check can see;
- for a pull request into `main`, `brief.md` differs from the last approved brief without the owner's approval;
- for a documents-only task, any of its checks is false.

## Defect or gap

Mark each failed item **defect** or **gap**. Its risk is that of the ticket it belongs to. It is a gap only when users can already do what its scenario says, you saw it work, and what falls short is the proof or the documents around it: a test missing or unable to fail at low or medium risk, a report or repeated figure out of step, a spec that leaves something out. A spec whose Scenarios say something the work makes false is a defect: the next task starts from it. Anything else is a defect, and at high risk every failed item is a defect. The verdict is a **FAIL** only when at least one failed item is a defect. When every failed item is a gap, the verdict is a **PASS** and the comment lists them under a `### Gaps` heading: a gap is not fixed in this run, and a FAIL would only make the owner override the required check to merge.

For each failed item, say which check failed (and which scenario, when one is involved), how to reproduce it and what you saw, so the builder need not guess, and where else you searched for the same kind of mistake and what you found there.

## PASS and findings

Otherwise it is a **PASS**. Anything else you found (a defect outside the scenarios, an unspecified input, a weak spot, a property guarded only by a ticket's own check script and not by the suite, everything else from reading the code) goes under a `### Findings` heading in the same comment, each with how to reproduce it. A finding never turns a PASS into a FAIL, and is never left out to keep a PASS clean.

## The comment

One comment, in this order: the heading `## Verification: PASS` or `## Verification: FAIL`; a line `Session: <your session id>`; the full head commit; in a fix round, a link to the verdict before this one; your paraphrase; the checks with their evidence, failed items marked defect or gap; then `### Gaps`, when any item is a gap; then `### Findings`. With no pull request yet, post it where you were told to, which is normally the tracking issue. Never edit it afterwards; a new head needs a new verdict.
