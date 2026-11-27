# Handing work to others

Read this before you start a builder or a verifier.

## Who does what

A builder is a subagent in its own worktree, on the branch `work/<slug>/T-<nn>` for its ticket (never a second `task/` branch: `state.py` would take it for another task); a verifier is a new session, so it shares nothing with whoever built. Start the verifier with the repository being judged as its source, so it can read the work and post its verdict without asking for access; it gets the skills from the environment's setup script, not from you. Give each the path of its file under `roles/` in this skill's directory and what that file lists under "You are given", and nothing about the work itself. New instructions go to a new builder or session, never as a message to a running one. Create each ticket's branch from the task branch's head before its builder starts; on a resume, a ticket whose branch exists is continued on it unless a builder noted for it is still working. Before you restart a builder, merge the task branch into its branch, so it reads the pitfalls, design and guards the run has added since. Note each session and each builder you start on the tracking issue, with its id, its job, and for a builder its ticket, branch and worktree, so a resume can find them. On a resume, before you restart a builder, check whether the one noted is still working. Worktrees live under `.shilaycow/worktrees/T-<nn>/`, one per ticket; remove one once its ticket is merged.

## Knowing when one is done

Nothing wakes you when a session you started finishes. Ask it to send one line to the session that started it when it is done, and set yourself a timed check in case that line never comes; if you can do neither, say so on the tracking issue and stop there instead of waiting forever.

## Closing what you started

Close every session you start once its work is done: when a verifier has posted its verdict, archive its session with your session tools. When the timed check finds one that has stopped without a verdict, or no longer answers, close it, note its id and what it reached on the tracking issue, and start a new verifier; if that one stops too, open a `needs-owner` issue instead of a third. Remove each builder's worktree once its ticket is merged. Before you post `Finished:`, no session or worktree you started is left; where your tools cannot close a session, list the ones left in `Finished:` for the owner to close.

## Landing a ticket

Merge a ticket's pull request into the task branch with a local `git merge`, then a push, never by asking GitHub to merge it (the API, `gh pr merge` or a GitHub tool's merge): on the task branch, `git merge --no-ff --no-commit work/<slug>/T-<nn>`, add to `trail.tsv` the trail rows from every Ready comment on the ticket's pull request (a fix round adds one), each row once, commit, then push the task branch (SKILL.md, "Write on top of what is there"). If the merge conflicts with work that landed meanwhile, the two tickets were not independent: abort it, merge the task branch into the ticket's branch, have its builder resolve it there, and land it again. The rows then land in the same commit as the work, so a crash cannot leave one without the other. If the ticket's `Status:` lives in a shared table rather than its own file, set it to `done` in that commit too. GitHub records the pull request as merged once its commits are on its base; a squash or a rebase would not count, so use `--no-ff`. The project's settings deny GitHub's merge tools, since a merge on GitHub's side names only the pull request, and a session connected as the owner could merge into `main` with it; a local merge ends in a push that names the branch it writes, and the ruleset refuses `main`. After the push, check that the pull request shows as merged.

## Signing and committing

All roles act as one account. A builder you start as a subagent has no session of its own, so give it `Session: <your session id>/<ticket>` to sign its Ready comment with. Before relying on a PASS, check that its `Session:` is neither yours nor that of any Ready comment on that pull request. If you built the work yourself, post that Ready comment yourself, with your own `Session:` line. Trail rows you write yourself have `orchestrator` as who decided (`references/trail.md`). Put builders' worktrees under `.shilaycow/worktrees/`, which setup ignores, and add files to a commit by path, never all at once.
