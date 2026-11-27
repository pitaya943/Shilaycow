# Status

Read this when the user typed `/shilaycow` alone, asked about progress, or described a job and wants to know which skill fits. Say where things are, or which skill fits, without changing or starting anything.

## Where things stand

From `state.py` and your GitHub tools (open pull requests with their checks and verdicts, the tracking issue `Task: <slug>` and its goal list, open `needs-owner` and `later` issues), reply in this order, in a few lines:

1. **Waiting on**: the one thing blocking progress and who holds it: a pull request for the owner to merge, a `needs-owner` issue to answer, a session at work, or nothing.
2. **Where the task is**: approved or not, tickets landed out of those cut, fix rounds used, in a chain which task of the roadmap this is, and how many `later` issues are open.
3. **Next**: one step, with the command to type.
   - A task whose brief is not approved: the user approves it with `/shilaycow`.
   - An approved task with no tracking issue yet, or a run that stopped: `/shilaycow run`. If your session tools show a run already working on the task, say which, and do not offer the command: a second run only duplicates the work.
   - No task open: with a roadmap, list its tasks as done (with their pull requests), next (`next_task`) and remaining, and offer `/shilaycow` to agree the next one; with none, the next task is the user's to name.

Anything in `problems` comes first, with its fix.

## Which skill fits a job

For a job ("I want to understand the payment code", "I am about to change the retry logic"), name the one to three skills that fit, in the order to use them, each with its command and one line on why it fits rather than the skill it is most easily confused with. Choose from the skills' descriptions, which say when not to use each. Any skill but `/shilaycow` can be typed directly in either mode; a whole task, meaning work that should end in a pull request, is `/shilaycow` in auto mode. If the job could mean two things, ask that one question and stop. If no skill fits, say so rather than stretching one.

In manual mode (no config, or `mode` not `auto`) a whole task goes by hand: write the scenarios with the user, then `/shilaycow-plan` (which designs first when the shape is open), each ticket with `/shilaycow-prove`, and `/shilaycow-verify` from a fresh session. `/shilaycow-setup` turns on auto mode.

Point, never run: the user types the command, so the choice stays theirs. Nothing is written, pushed, commented or started.
