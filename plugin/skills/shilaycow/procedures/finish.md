# Finish

Read this when every ticket has landed on the task branch. **You own the verdicts on the pull request into `main`, never its merge**: that is the owner's.

## Before the pull request

First fetch and check that your checkout's head is the task branch's head on the remote: the spec, the description and blast radius must describe what the owner will merge, not an older state. Then, if the task changed the system's shape, bring `docs/spec/` up to date with what was built (`sc-spec`), copy into `docs/tasks/<slug>/spikes/` any file on a `spike/` branch that the trail cites (with a trail row saying where it now is). Everything the owner will merge is on the branch before the first verdict.

If a scenario is not met, for instance one still waiting on a `needs-owner` issue, do not open the pull request into `main`: post the description below on the tracking issue, its first sentence saying what is missing, set Waiting on to what holds it, cancel your timed checks and end. The decision is the owner's; once they answer, typing `/shilaycow run` continues.

## The pull request

Open the pull request into `main` with the description below. It says `Closes #<tracking issue>`, so the issue closes when the owner merges, and ends with what comes after the merge: the roadmap's next task and its command, `/shilaycow`, or that the roadmap is done. Then, in a chain, push this task's entry in `docs/roadmap.json` with this pull request as `pr` and `done` true (it is done exactly when the owner merges it), and only then have it verified (`references/sessions.md`): nothing is pushed while a verifier judges. If this task showed the roadmap's later tasks are in the wrong order, do not re-cut them: put it on the goal list as a question for the owner, who approved the roadmap.

## The description

It tells the owner what they are asked to accept, in a form they can check without reading the diff first; keep it to about 40 lines and link rather than copy. Gather it only from the branch, the brief, the plan, the trail, the Ready and verdict comments and CI; memory is not a source. Write it in English, its first sentence saying whether, by your own check, every scenario is met; then:

1. **What was done**: three to five plain sentences.
2. **How to try it**: from zero, for someone who has never seen the project: getting the code and the branch, installing, starting it, then each action with what they should see, and two or three things worth trying that the tests do not cover. Every step was run by you for this description; one you could not run says `not run`, never what it would show.
3. **Decisions made without asking**: from the trail, each with its reason in a line.
4. **Not done or in doubt**: never omitted; None if there is nothing.
5. **Scenarios and tickets**: a table of every scenario, met or not, with a link to its evidence; and every ticket with its final risk level and the signal that set it, so the owner sees where verification was light.
6. **Verification**: one line saying the independent verdict will be posted as a comment; claim no result.

A fix round that changes what the description says updates it before the next verdict.

## After each verdict

Read `references/verdicts.md`: it holds what to do with findings and gaps, fix rounds and their limit, for the pull request into `main` as for any ticket.

## When the last verdict is in

The last verdict is a PASS, or the one after which you stopped. Then, on the tracking issue:

- a `Retro:` comment, from a steward you start on `roles/steward.md` (SKILL.md, "Dispatching"), unless the issue already has one from this run (a resume after a crash must not post a second);
- the goal list in its final state (`procedures/run.md`);
- `Finished:`, whose first line says how many gaps the PASS lists (or none), and which ends like the pull request, with the roadmap's next task and `/shilaycow` or that the roadmap is done, and tells the owner two things: anything they find wrong after merging is worth one comment on this issue, closed or not, since it is how the next task learns what verification missed; and if they update the branch from `main` before merging, the new head was not judged, so they run `/shilaycow run` again for its verdict.

The next task's `/shilaycow` folds the Retro into the pitfalls file and proposes the corrections it makes due (`references/learning.md`). Push nothing more to the task branch: the commit the owner merges is the commit that was judged. Apart from a fix round's ticket, which lands with its trail rows as usual, decisions you make after the pull request into `main` is sent for verification (restarting a verifier, for instance) go in a comment on the tracking issue starting `Decision:`, not in the trail, so recording them never moves the judged head; the report's next version folds them in. Then cancel your timed checks. Delete the `spike/` branches this task opened; their decisions are in the trail and the files it cites are already copied. Delete the `work/` branches of merged tickets too: GitHub's automatic deletion may not apply to a pull request merged by a push. Where your tools cannot delete a branch (a cloud session's git access may refuse it), list those branches in `Finished:` for the owner to delete.
