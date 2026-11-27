# Run

Read this when the user typed `/shilaycow run`, `state.py` shows no problems and `approved` is true, and `get_me` says you are the bot. **You own the run until the pull request into `main` has its last verdict**: take the approved task to a pull request the owner can merge with confidence. How you get there is your call, scaled to the task: whether it needs a design, how to cut the work, how many builders at once (one at a time unless the tickets share nothing), which skills to use and which to skip.

## Starting or resuming

A task has one run. Before anything else, if your session tools show another run working on this task, tell the user and stop: a second run only duplicates the work. Set git's identity to the bot's (`procedures/agree.md`, "Before the brief").

**A first start** is one whose tracking issue, titled exactly `Task: <slug>`, does not exist yet. Open it: its opening post lists `state.py`'s warnings first, then says the run started at the brief commit `state.py` printed. Then post the **goal list** (below) as its first comment.

**A resume** rebuilds its picture from the repository and GitHub, not from memory. Find the tracking issue by its title and the goal list by its marker line (post one if there is none). Read the goal list, then check it against `state.py` and GitHub: which tickets have landed, whether each landed ticket's trail rows are in `trail.tsv`, the open pull requests and whether the head of each has a verdict, the sessions noted on the issue, and the owner's comments since `Read up to:`. Where the goal list is behind, correct it first: the repository is the truth, the goal list the summary.

Then one judgement the script cannot make: every scenario can be shown by a check that fails today (for one that keeps behaviour unchanged, fails when it is broken), or by a manual step. Where one cannot here, first try to make it runnable: start the service, install what the package managers allow, look for what the environment already has. If it still cannot be shown, open a `needs-owner` issue before you build that scenario, with the options (the owner provides what is missing, runs a manual step you write, or drops the scenario) and your recommendation, push the trail row `needs-owner #<n>` so any run reads its answer, and carry on with what it does not block. Never plan a scenario as a gap: a gap is something verification found, not something the run chose not to show.

## The order of the run

1. **Before you cut the work into tickets, and before the next ticket after a resume**, read `references/working.md`: the skills you will reach for, how risk decides how closely each ticket is checked, what counts as evidence, and mistakes that repeat.
2. **Before you start a builder or a verifier**, read `references/sessions.md`: what each is given, landing a ticket, how you learn one is done, and closing every session you start.
3. **Whenever a verdict arrives**, on a ticket or on the pull request into `main`, read `references/verdicts.md`: whether it is for this head, findings and gaps, fix rounds and their limit.
4. **When every ticket has landed on the task branch**, read `procedures/finish.md`.

## Throughout

- **Read the owner first.** Before each ticket, each agent you start, each wait and each verdict you act on, read the owner's comments newer than the goal list's `Read up to:`, on the tracking issue and on the `needs-owner` issues the trail names, then move `Read up to:` on. A `stop` from the owner's own account ends the run: close the sessions you started, set Waiting on to the owner's stop, say on the issue that the run has stopped and that `/shilaycow run` continues it, cancel your timed checks, and end. Nothing watches the issue after that; only the command restarts a run.
- **The brief can change under you.** When `brief.md` has a new commit, run `state.py` again; go on only once `approved` is true again, and re-plan the tickets not yet landed against the new brief.
- **Write on top of what is there.** When a push is refused, fetch, `git merge` what moved, and push again; never rebase the task branch, since the approval rows `state.py` reads must keep their hashes. If the pull request into `main` has been merged, push nothing: end as `procedures/finish.md` describes.
- **Distrust your own summary.** After your context is compacted, or whenever you cannot say for certain where the run stands, run `state.py` and do the resume check above before the next action.

## The goal list

The tracking issue's comment whose first line is `<!-- shilaycow:goal-list -->`, normally its first comment; find it by that line, not by its place. Write it in the form below only, even where an earlier task's issue shows more lines: fix rounds are counted from the trail, not here. Only you edit it; builders and verifiers read the issue but never change it. Read it just before each edit and change only the lines that changed. Under the marker:

- **Read up to**: for this issue and for each `needs-owner` issue the trail names, the link of the newest owner comment on it you have acted on.

Then three parts:

- **Goal**: the brief's Goal, in one sentence.
- **Left**: the tickets not yet landed, each with its risk level, and what remains after them (the spec when the shape changed, the pull request's description, verification). Before the work is planned, say so; write the tickets in as soon as they are cut.
- **Waiting on**: what blocks progress now and who holds it, a `needs-owner` issue by its number included; or nothing.

Edit it each time a ticket lands, a plan changes or something starts or stops waiting, and read it again before each ticket: it is how a long run keeps its goal in view. The issue's other comments stay the history, one line per event, and the trail keeps the decisions. When the run ends, Left is empty and Waiting on names the owner's merge, the gaps handed to the owner, or the `needs-owner` issue that stopped the run.
