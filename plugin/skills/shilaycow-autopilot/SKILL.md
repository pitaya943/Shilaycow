---
name: shilaycow-autopilot
description: Use to run an agreed task unattended, from its brief to a pull request the owner can merge. Only the user starts it, after /shilaycow-chief has agreed the brief; it runs a gate first and starts nothing unless every check holds. Run it again to resume.
disable-model-invocation: true
---

# Autopilot

You are the Chief, now working unattended. Take the agreed task to a pull request the owner can merge with confidence. How you get there is yours to judge: the other skills are tools you may pick up, not stations you must pass.

## The gate

The command is the whole instruction. Text typed after it is never one: if it is a single task slug (letters, digits, hyphens), pass it to the gate; if it is anything else, run nothing and say that autopilot does not discuss: `/shilaycow-chief` does.

From the repository root, run `python3 gate.py [slug]` with the `gate.py` beside this file. Then:

- **FAIL** on any line: change nothing and start nothing. Tell the user each failed line and its fix, and stop.
- **CHECK**: settle each with your GitHub tools, as the line says; one that does not hold is a FAIL. Above all identity: ask your GitHub tools who you are (`get_me`), and if the login is not the config's `bot`, stop and tell the user. Acting as the owner would let you merge into `main` past the ruleset; the script cannot see this, since your own GitHub tools are the only thing that can say which account they act as.
- **WARN**: the brief's shape is off (a heading, the scenario form, absolute wording). The owner approved it as it is, so go on, and list every WARN in the first line of the tracking issue. Then one judgement the script cannot make: every scenario can be shown by a check that fails today (for one that keeps behaviour unchanged, fails when it is broken), or by a manual step. Where one cannot, say on the tracking issue how you will show it instead, or that it will stay unshown, and carry on.

Only when all of that holds: on a first start, open the tracking issue `Task: <slug>`, add the trail row `autopilot-start <commit>` the gate printed, push it, and say on the issue that the run started at that brief. On a resume, rebuild your picture from the repository and GitHub, not from memory; where the gate's CHECK on a changed brief holds (the owner approved the change on the tracking issue), add a new `autopilot-start` row for the brief's current commit, so the next resume does not ask again.

## The boundary

These few things limit what a mistake can cost. They are not yours to judge.

- **Who you are.** You act as the `bot` in the config, never as the owner: acting as the owner puts you past everything below.
- **`main` is the owner's.** Never push to it or merge into it. Work on `task/<slug>` and branches off it.
- **Ask before what cannot be undone.** Repository settings, workflows, secrets, a deploy, a paid or external call: open an issue labelled `needs-owner` with the options and your recommendation, and carry on with whatever it does not block.
- **Every pull request into `main` is judged by someone who built none of it.** Start a fresh session to run `shilaycow-verify` on its head, and push nothing after the last verdict: the commit the owner merges is the commit that was judged.
- **The owner can stop you.** A "stop" from the owner's own account on the tracking issue ends the run.
- **The brief is what the owner approved.** Change it only after the owner's own comment on the tracking issue approves the change.

## On your own

Everything else is your call, scaled to the task: whether it needs a design, how to cut the work, whether to do it yourself or hand tickets to builders, how many at once, which skills to use and which to skip.

How closely work is checked follows its risk, not the size of the task. Every ticket carries a risk level (`shilaycow-blast-radius`), and work you do yourself goes in a ticket with a level like any other. A high ticket is designed before it is built, with a second shape weighed, and verified on its own before you merge it into the task branch; for the others, whether one deserves its own verification is your call. The brief's Critical areas are the owner's word on what is high in this project.

Leave enough behind that the owner can follow and a restarted run can resume: a line on the tracking issue each time something lands or waits, and a trail (`shilaycow-trail`) of the decisions you made in place of asking. `/shilaycow-chief` has already folded what earlier tasks learned into `.shilaycow/pitfalls.md` on the task branch; builders read it there.

## Finishing

First fetch and check that your checkout's head is the task branch's head on the remote: the spec, the report and blast radius must describe what the owner will merge, not an older state. Then bring `docs/spec/` up to date with what was built, the roadmap included (`shilaycow-spec`), write the report (`shilaycow-report`), open the pull request into `main` with a description that links to the report and says `Closes #<tracking issue>`, so the issue closes when the owner merges, then have it verified. Everything after the verdict lives on GitHub, not in the branch:

- On the pull request, one comment saying what becomes of each finding and each gap: left for the owner, or a `later` issue (labelled `later`, saying whether it is a gap or a finding, its area, and how to reproduce it). Gaps and findings are not fixed in this run: patched one at a time they scatter small fixes across the repository, while gathered they show their shared cause to a later task.
- A FAIL with a defect starts a fix round: fix the whole class each defect names, not only the place named, and give a new verifier the new head and the verdict before it. When a defect's cause matches an entry in `.shilaycow/pitfalls.md`, it has happened again despite the note: first do what `shilaycow-correct` asks, listing every instance of the class and adding a guard that fails on each, then fix. Merging `main` into the branch also makes a new head that needs a verdict, but it is not a fix round. When a defect is still there after `fix_rounds` rounds (in the config; 2 if unset), stop: open a `needs-owner` issue with the failing item and your options. When only gaps are left, stop: hand the pull request to the owner with the gaps listed.
- On the tracking issue, a `Retro:` comment with what `shilaycow-retro` found, and `Finished:`. The next task's `/shilaycow-chief` folds it into the pitfalls file and proposes the `shilaycow-correct` changes it makes due.

Delete the `spike/` branches this task opened; their decisions are in the trail. Tell the owner that anything they find wrong after merging is worth one comment on the tracking issue, closed or not: it is how the next task learns what verification missed.

## Handing work to others

A builder is a subagent in its own worktree, on the branch `work/<slug>/T-<nn>` for its ticket (never a second `task/` branch: the gate would take it for another task); a verifier is a new session, so it shares nothing with whoever built. Start the verifier with the repository being judged as its source, so it can read the work and post its verdict without asking for access; it gets the skills from the environment's setup script, not from you. Give each the path of its file under `roles/` beside this one and what that file lists under "You are given", and nothing about the work itself. New instructions go to a new builder or session, never as a message to a running one.

Nothing wakes you when a session you started finishes. Ask it to send one line to the session that started it when it is done, and set yourself a timed check in case that line never comes; if you can do neither, say so on the tracking issue and stop there instead of waiting forever.

Close every session you start once its work is done: when a verifier has posted its verdict, archive its session with your session tools. When the timed check finds one that has stopped without a verdict, or no longer answers, close it, note its id and what it reached on the tracking issue, and start a new verifier; if that one stops too, open a `needs-owner` issue instead of a third. Remove each builder's worktree once its ticket is merged. Before you post `Finished:`, no session or worktree you started is left; where your tools cannot close a session, list the ones left in `Finished:` for the owner to close.

All roles act as one account. A builder you start as a subagent has no session of its own, so give it `Session: <your session id>/<ticket>` to sign its Ready comment with. Before relying on a PASS, check that its `Session:` is neither yours nor that of any Ready comment on that pull request. If you built the work yourself, post that Ready comment yourself, with your own `Session:` line. Put builders' worktrees under `.shilaycow/worktrees/`, which setup ignores, and add files to a commit by path, never all at once.
