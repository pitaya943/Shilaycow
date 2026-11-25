# Finishing

Read this when the last ticket is merged into the task branch.

## Before the pull request

First fetch and check that your checkout's head is the task branch's head on the remote: the spec, the report and blast radius must describe what the owner will merge, not an older state. Then bring `docs/spec/` up to date with what was built (`shilaycow-spec`), copy into `docs/tasks/<slug>/spikes/` any file on a `spike/` branch that the trail cites (with a trail row saying where it now is), and write the report (`shilaycow-report`). Everything the owner will merge is on the branch before the first verdict.

If a scenario is not met, for instance one still waiting on a `needs-owner` issue, do not open the pull request into `main`: post the report on the tracking issue, saying what is missing (`shilaycow-report`), set Waiting on to what holds it, cancel your timed checks and end. The decision is the owner's; once they answer, typing `/shilaycow-autopilot` continues.

## The pull request

Open the pull request into `main` with a description that links to the report, says `Closes #<tracking issue>`, so the issue closes when the owner merges, and ends with what comes after the merge: the roadmap's next task and its command, `/shilaycow-chief`, or that the roadmap is done. Then push the roadmap's line for this task, naming the pull request, and only then have it verified (`references/sessions.md`): nothing is pushed while a verifier judges. If this task showed the roadmap's later tasks are in the wrong order, do not re-cut them: put it on the goal list as a question for the owner, who approved the roadmap.

## After each verdict

Read `references/verdicts.md`: it holds what to do with findings and gaps, fix rounds and their limit, for the pull request into `main` as for any ticket.

## When the last verdict is in

The last verdict is a PASS, or the one after which you stopped. Then, on the tracking issue:

- a `Retro:` comment with what `shilaycow-retro` found, unless the issue already has one from this run (a resume after a crash must not post a second);
- the goal list in its final state (`references/starting.md`);
- `Finished:`, which ends like the pull request, with the roadmap's next task and `/shilaycow-chief` or that the roadmap is done, and tells the owner two things: anything they find wrong after merging is worth one comment on this issue, closed or not, since it is how the next task learns what verification missed; and if they update the branch from `main` before merging, the new head was not judged, so they run `/shilaycow-autopilot` again for its verdict.

The next task's `/shilaycow-chief` folds the Retro into the pitfalls file and proposes the `shilaycow-correct` changes it makes due. Push nothing more to the task branch: the commit the owner merges is the commit that was judged. Apart from a fix round's ticket, which lands with its trail rows as usual, decisions you make after the pull request into `main` is sent for verification (restarting a verifier, for instance) go in a comment on the tracking issue starting `Decision:`, not in the trail, so recording them never moves the judged head; the report's next version folds them in. Then cancel your timed checks. Delete the `spike/` branches this task opened; their decisions are in the trail and the files it cites are already copied. Delete the `work/` branches of merged tickets too: GitHub's automatic deletion may not apply to a pull request merged by a push. Where your tools cannot delete a branch (a cloud session's git access may refuse it), list those branches in `Finished:` for the owner to delete.
