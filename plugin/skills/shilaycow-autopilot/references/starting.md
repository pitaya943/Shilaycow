# Starting and resuming

Read this once the gate has no FAIL and every CHECK holds. The gate's `PASS start` line says which this is: a first start, or resuming.

## The WARN lines and the scenarios

The owner approved the brief as it is, so a WARN does not stop you: list every WARN at the top of the tracking issue's opening post.

Then one judgement the script cannot make: every scenario can be shown by a check that fails today (for one that keeps behaviour unchanged, fails when it is broken), or by a manual step. Where one cannot here, first try to make it runnable: start the service, install what the package managers allow (that is not the external call the boundary means), look for what the environment already has. If it still cannot be shown, open a `needs-owner` issue, once the tracking issue exists and before you build that scenario, and push the trail row `needs-owner #<n>` so any run reads its answer, with the options (the owner provides what is missing, the owner runs a manual step you write, the scenario leaves the brief) and your recommendation, and carry on with the scenarios it does not block. Never plan a scenario as a gap: a gap is something verification found, not something the run chose not to show.

## If two runs meet

Nothing here is a lock, and nothing needs one: every write that could lose work is a compare-and-swap that only one writer wins. Pushes to `task/` and `work/` branches are leased (the project's hook refuses any other), a ticket is claimed by creating its branch (`references/sessions.md`), the tracking issue is the one the trail names (below), and GitHub allows one open pull request per branch. Two first starts cannot both go on: the start row is pushed as a compare-and-swap on the head both fetched, and the run whose push is refused finds the other's row and stops. A second run on a resume only duplicates effort; to save that cost, before anything else on a resume, if your session tools show another autopilot session working on this task, tell the user and stop.

## A first start

1. Set git's identity to the bot's (SKILL.md, "Who you are"), then add the trail row `autopilot-start <commit>` the gate printed and push it, before anything else, as a compare-and-swap on the task branch's head as you fetched it. If it is refused, fetch: if the trail now has an `autopilot-start` row for the same brief commit, another run has started this task, so tell the user and stop; otherwise merge and push again.
2. Open the tracking issue titled exactly `Task: <slug>`. Its opening post lists the WARN lines first, then says the run started at that brief. Then push the trail row `tracking-issue #<n>`. If the push is refused, fetch and merge: if the trail now has a `tracking-issue` row, that issue is the task's: close yours as its duplicate and go on with that one, posting a goal list there only if it has none; otherwise push again.
3. Post the **goal list** (below) as the issue's first comment.

## A resume

Rebuild your picture from the repository and GitHub, not from memory. Find the tracking issue by the trail's `tracking-issue` row, or else by its exact title (a task started before that row existed has none: push the row now); if neither finds one, a first start stopped after its first row, so do its steps 2 and 3 now. Find the goal list by its marker line; if there is none, post it. Read the goal list first, then check it against the task branch: which `work/` branches are merged, each ticket's `Status:` line, whether each merged ticket's trail rows are in `trail.tsv`, the open pull requests and whether the head of each has a verdict, the sessions noted on the issue, and the owner's comments since `Read up to:`. Where the goal list is behind, correct it before you act: the repository is the truth, the goal list is the summary. Where the gate's CHECK on a changed brief holds (the owner approved the change on the tracking issue), add a new `autopilot-start` row for the brief's current commit, so the next resume does not ask again. Then go on with the run as SKILL.md orders it, reading `references/working.md` and `references/sessions.md` before the next ticket.

## The goal list

The tracking issue's comment whose first line is `<!-- shilaycow:goal-list -->`, normally its first comment; find it by that line, not by its place. Only autopilot edits it; builders and verifiers read the issue but never change it. Read it just before each edit and change only the lines that changed. It is a summary: if two runs ever edit it, the next resume corrects it from the repository. Under the marker:

- **Read up to**: for this issue and for each `needs-owner` issue the trail names, the link of the newest owner comment on it you have acted on.
- **Rounds**: fix rounds used so far, per ticket judged on its own and for the pull request into `main`.

Then three parts:

- **Goal**: the brief's Goal, in one sentence.
- **Left**: the tickets not yet merged into the task branch, each with its risk level, and what remains after them (spec, report, verification). Before the work is planned, say so; write the tickets in as soon as they are cut.
- **Waiting on**: what blocks progress now and who holds it, a `needs-owner` issue by its number included; or nothing.

Edit it each time a ticket lands, a plan changes or something starts or stops waiting, and read it again before each ticket. It is how a long run keeps its goal in view. The issue's other comments stay the history of what happened, one line per event; the goal list is only the current state, and the trail keeps the decisions. When the run ends, it ends as: Left empty, and Waiting on the owner's merge, the gaps handed to the owner, or the `needs-owner` issue that stopped the run.
