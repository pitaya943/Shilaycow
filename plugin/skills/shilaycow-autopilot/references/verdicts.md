# After a verdict

Read this whenever a verdict arrives, on a ticket judged on its own or on the pull request into `main`, before you act on it.

## Is it the verdict for this head?

Rely on a verdict only when the commit it names is the branch's head as it is now: fetch and compare. While a verifier is judging a branch, push nothing to it; if something had to be pushed, the verdict is for an older head and the new head needs its own. A verdict whose `Session:` is yours or a Ready comment's is not independent: start another verifier.

## Findings and gaps

On the pull request, one comment saying what becomes of each finding and each gap: left for the owner, or a `later` issue (labelled `later`, saying whether it is a gap or a finding, its area, and how to reproduce it). Gaps and findings are not fixed in this run: patched one at a time they scatter small fixes across the repository, while gathered they show their shared cause to a later task. Defects do not go in that comment: they go to a fix round.

## A fix round

Fix the whole class each defect names, not only the place named, and give the builder the verdict.

- **A ticket not yet merged** is fixed on its own `work/<slug>/T-<nn>` branch and pull request, with a new Ready comment.
- **The pull request into `main`** is fixed by a new ticket on `work/<slug>/T-<nn>` off the task branch, landed on it like any other ticket. Then bring the spec and the report up to date for the new head (`shilaycow-spec`, `shilaycow-report`) before the next verdict: a stale spec is itself a defect.

Then give a new verifier the new head and the verdict before it. A fix keeps its ticket's risk level (a fix ticket for the pull request into `main` is given its own), so a high one is judged on its own too, on what changed since its last verdict. When a defect's cause matches an entry in `.shilaycow/pitfalls.md`, it has happened again despite the note: first do what `shilaycow-correct` asks, listing every instance of the class and adding a guard that fails on each, then fix. Merging `main` into the branch also makes a new head that needs a verdict, but it is not a fix round.

## The limit

`fix_rounds` (in the config; 2 if unset) limits each ticket judged on its own and, separately, the pull request into `main`: the first verdict is not a round, so with 2 there are at most three verdicts. A fix ticket made for the pull request into `main` belongs to that round: its own verdicts do not start a count of their own, and the round ends with the next verdict on the pull request. Keep the count for each on the goal list. A merge of `main` is not a round. When a defect is still there after that many rounds, stop: open a `needs-owner` issue with the failing item and your options. When only gaps are left on the pull request into `main`, stop: hand it to the owner with the gaps listed.
