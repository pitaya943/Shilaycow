# Changelog

## 0.5.0

### The boundary

- **GitHub refuses to merge a head nobody judged.** Setup adds the workflow `shilaycow-verdict`, which posts the status `shilaycow/verdict` on each pull request the bot opens into the default branch: green only when the newest verdict naming that exact commit is a PASS. Once the setup pull request is merged, make that status required in the ruleset, with GitHub Actions as its source (`by-hand.md` step 2). A push after the verdict, from any session, turns it red. The workflow runs from the default branch's copy and runs no code from the pull request, and the hook blocks posting a status or check by hand.
- **A second lock on `main`, in your repository.** `/shilaycow-setup` now adds a hook to `.claude/settings.json` that stops a push to the default branch, a push of every branch, and any merge Claude asks GitHub to make (through the API, `gh pr merge` or a GitHub tool), whoever the session acts as. Your own merge button on GitHub is untouched: the hook sees only what Claude runs. The ruleset still keeps the bot out; the hook also covers a session that is connected as you, which the ruleset lets through. It also stops Claude merging for you in this repository: you merge on GitHub. A merge on GitHub's side names only the pull request, not the branch it changes, so the hook cannot tell `main` from a task branch and blocks them all; a push names its target branch, so autopilot lands each ticket with a local `git merge` and a push of the task branch, which the hook allows. Projects set up before: run `/shilaycow-setup` again.
- **The hook is harder to get around.** It reads a push however it is wrapped (`env`, `command`, `sudo`, `bash -c`), follows a `git checkout`, `git switch` or `cd` earlier on the same line, blocks the API calls that merge, move a branch or write a file on the default branch, and blocks a push or merge built at run time. Pushes now name their branch (`git push origin <branch>`).
- **Two runs on one task cannot lose work, so there is no lock to get stuck.** Every push to a `task/` or `work/` branch is a compare-and-swap on the commit fetched (`--force-with-lease=<branch>:<commit>`), and a push to the task branch must also contain that commit; the hook refuses any other push and says how to do it. A ticket is claimed by creating its branch, which only one session can do; the tracking issue is the one the trail's `tracking-issue` row names. Two first starts cannot both go on: the start row is itself a compare-and-swap, and the run that loses stops. Setup adds `.gitattributes` with `docs/tasks/*/trail.tsv merge=union`, so trail rows appended at once by two sessions both survive a merge. A `needs-owner` issue is named in the trail, so any run reads its answer. A second run on a resume only duplicates effort. Autopilot never edits the brief; when `/shilaycow-chief` records a changed brief, the run checks the gate again and re-plans what is not landed.
- **The gate prunes deleted branches and reads only real approval rows.** A task branch deleted on GitHub no longer counts as an open task, and a trail row that only mentions `brief-approved` in a sentence is not taken for an approval.
- Once your project runs its tests in a workflow, setup asks you to make that check required in the ruleset, so a red suite cannot be merged.

### Unattended runs

- **A long run keeps its goal in view.** The tracking issue has a goal list, a comment marked `<!-- shilaycow:goal-list -->`: the session running the task, the newest owner comment acted on, the fix rounds used, the goal, what is left with each ticket's risk, and what the run is waiting on. Autopilot keeps it current and reads it again before each ticket and when it resumes.
- **You are heard during a run.** Before each ticket, each session it starts and each verdict it acts on, autopilot reads your new comments, so a `stop` or an answer to a `needs-owner` issue takes effect within one step. After a `stop`, typing `/shilaycow-autopilot` continues; a comment does not.
- **A verdict counts only for the head it judged.** Nothing is pushed while a verifier judges; a verdict for an older head is not used; fix rounds refresh the spec and the report; `Finished:` tells you to run `/shilaycow-autopilot` again if you update the branch before merging.
- Crashes and parallel work leave consistent state: the tracking issue is the one the trail names and the goal list is found by its marker; a ticket's trail rows land in the same commit as its work; pushes merge the latest task branch first and never rebase it; builders start from the current task branch; ticket status in a shared table is set by autopilot, not by parallel builders; pitfalls cite comment links, so a later owner comment is still folded and a Retro is never counted twice.
- Where a session cannot delete a `spike/` branch, the run lists it in `Finished:` for you to delete.

### Reviews by a fresh reader

- **A fresh reader checks the brief before you approve it.** `/shilaycow-chief` has a reader that was not in your conversation say back what the brief asks for, list the words it does not explain, the scenarios that cannot be checked as written and what a builder would have to guess. You see its reply and decide whether the brief says what you mean; it reads at most twice.
- **The verifier paraphrases before it judges.** Its verdict opens with what the work changes, in its own words, from the brief and the diff alone; a part of the diff it cannot account for is reported. The verifier also reports it when the message that started it describes the work, since it should see the work as you will.
- **The spec is checked, not only written.** `shilaycow-spec` can check an area against the code as it is now: each scenario and rule holds, is contradicted, is unshown or is not behaviour at all, with the evidence. `/shilaycow-chief` runs it on the areas a task touches before the brief, and you decide for each item whether the spec or the code is wrong.

### Loading only what a step needs

- **Sessions start with a map.** The section `/shilaycow-setup` writes into `CLAUDE.md` now also says where each piece of state lives (the config, a task's branch and folder, its tracking issue, the spec and roadmap, the pitfalls, the labels) and which command to start from. It names places only, so it stays the same from task to task. Projects set up before: run `/shilaycow-setup` again to update the section.
- **`/shilaycow-status` is the place to start when you are not sure.** Typed alone it says where things stand; typed with a job (`/shilaycow-status I want to understand the billing code`) it names the skills that fit, in order, and why each fits rather than its neighbour. It only points; you type the command. Only you can start it now: the model no longer calls it on its own.
- **Each skill says when not to use it.** Every description now names the case it does not cover and the skill that does, so the model picks the right one from the descriptions alone.
- `shilaycow-verify` is shorter: its checks, its verdict rules and its fix-round rules each live in a file beside it that it reads at the step that needs it. Nothing in what it checks has changed.
- `shilaycow-autopilot` is shorter: its body keeps the gate, the boundary and the order of the run, and it reads how to start, how to work, how to hand work to others and how to finish from files beside it when it reaches each part. The rules themselves are unchanged.

### Credits

- The README credits the work these changes build on: the Elephant-Goldfish Model, Anthropic's and OpenAI's writing on agent harnesses, Manus and Cognition, besides pstack and Matt Pocock's skills.

**Upgrading from 0.4.x:** run `/shilaycow-setup` again in each repository. It adds the hook, the verdict workflow and `.gitattributes` in a pull request; once you merge it, make the status `shilaycow/verdict` required in the ruleset, with GitHub Actions as its source (`by-hand.md` step 2). A task already running carries on: its tracking issue is found by its title and gains a `tracking-issue` row on the next resume. Update the `--branch` tag in your cloud environment's setup script.

## 0.4.3

- **Setup asks less.** `/shilaycow-setup` finds the owner and the bot itself and only asks you to confirm them. It no longer asks for a test command: it takes one the repository already runs, or leaves it empty in a new project, and the first task that adds tests sets it.
- Setup now asks you to create the `needs-owner` and `later` labels by hand, since a session's GitHub tools cannot create labels. Once you merge the setup pull request, it tells you to start your first task with `/shilaycow-chief`.
- **You always know what comes next.** In a chain of tasks, the final pull request and the `Finished:` comment name the roadmap's next task; `/shilaycow-chief` typed with no request proposes it; `/shilaycow-status` lists the roadmap as done, next and remaining.
- **The approved brief stays as approved.** A brief has no status line, since approval lives in the trail, and the verifier fails a pull request whose brief differs from the one you last approved.
- Commits are authored as the bot, not as the session's default identity. Files on a `spike/` branch that the trail cites are copied into the task folder before the branch is deleted. The trail's "who" column uses a fixed set of names, and tickets kept as a table in `plan.md` carry Status and Risk columns.
- `/shilaycow-autopilot` names the skills it usually reaches for (design, plan, prove, try-it, blast radius, spec, report, retro), so a run started straight after the brief still designs and plans where the task needs it. Skipping one is recorded in the trail.
- **A scenario this environment cannot run is raised before it is built.** The run first tries to make it runnable; if it still cannot, it opens a `needs-owner` issue with options instead of planning the scenario as a gap.
- **Cheaper rounds.** Builders no longer run mutation sweeps, which are the verifier's check on high-risk tickets, and only short evidence is committed: long transcripts go in a collapsed block of a comment, since the task branch is merged into `main`.
- `fix_rounds` limits each ticket judged on its own and, separately, the pull request into `main`; a fix that lands as a high-risk ticket is judged on its own too. A mistake of the same class found twice within one task becomes a pitfall and gets a guard straight away, and a correction you defer becomes a `later` issue.
- A roadmap is approved like a brief, with a `roadmap-approved` row, and a project with no `docs/spec/` gets one in the first task of the chain, before anything is built.
- **The cloud setup script installs one version.** It pins the release it ships with and removes skills an earlier version left before copying. Update the script in your environment from the README.
- `/shilaycow-autopilot` says where `gate.py` is (the skill's own directory, which for a plugin install is the plugin cache). Tickets that change the same files are built one after the other. Several skill descriptions are narrower, so they load when they apply rather than on every turn.
- The README says plainly that the toolkit is for Claude Code only, and credits the projects whose ideas several skills build on.

## 0.4.2

- **Branch permission is set once.** `/shilaycow-setup` writes into your repository's `CLAUDE.md` that agents may push `task/`, `work/`, `spike/` and `chore/` branches and never `main`, so you no longer grant it at the start of each session. Projects set up before: run `/shilaycow-setup` again to add it.
- Fixes from a review of the whole toolkit: builders work on `work/<slug>/T-<nn>` branches, named now, so a resume never takes one for a second task; the gate tells you to merge or drop extra open tasks; an approval row keeps its word and commit in one cell; a resume after an approved brief change records a new start and does not ask again; tickets carry `Status:` and `Risk:` lines; the README describes what the gate checks each run and what setup checks.
- `parallel_builders` is gone from the config: how many builders run at once is the Chief's call. An existing key is ignored.
- **A run leaves no session behind.** Each verifier session is closed once it has posted its verdict; one that stops without a verdict or stops answering is closed and replaced once, then reported to you. Builders' worktrees are removed once their tickets merge.

## 0.4.1

- **English only.** Briefs, specs, reports and verdicts are written in English, whatever language you talk in; `report_language` is gone from the config. To use another language, fork the skills and change them.
- **The gate stops a run only for the boundary and the handover**: auto mode, old skill copies in the repository, one task at a time, and the brief you approved. A brief's shape (missing headings, scenarios not as Given / When / Then, absolute wording) is now a warning, listed on the tracking issue. A task started before 0.4.0 is told to finish with its own version.
- The verifier loads its skill with the Skill tool under either name (`shilaycow-verify`, or `shilaycow:shilaycow-verify` for a plugin install), so a plugin install is no longer mistaken for a missing skill. A ticket judged on its own and unchanged since may keep that verdict at final verification.
- **A finished task leaves nothing open.** The final pull request says `Closes #<tracking issue>`, so the issue closes when you merge it; the run deletes its `spike/` branches; and `/shilaycow-setup` asks you to turn on **Automatically delete head branches**. Issues are closed, never deleted: the next task reads their `Retro:` comments.
- A ticket whose check guards a lasting property also adds a test of it to the suite; the verifier lists a property guarded only by a ticket's script. A pitfall that `shilaycow-correct` cannot guard records `Correct: none possible at count <n>` and is not proposed again until it happens more. The trail starts when the task branch does, so decisions before approval carry their own time.
- **No token.** The gate no longer calls the GitHub API, so auto mode needs no token of the bot and no network secret; if you saved one for `api.github.com`, you can delete it. A token could only prove who owns the token, not which account the session's own GitHub tools act as. The agent now asks its own tools (`get_me`) before a run starts, and the verifier fails a pull request or tracking issue the bot did not open. `/shilaycow-setup` compares the ruleset with the one it ships, setting by setting. Upgrading from 0.3 straight to 0.4.1, follow the 0.4.0 steps below and skip the token in step 6.

## 0.4.0

**Not compatible with 0.3.x.** The skills no longer read the formats version 0.3 wrote, and `/shilaycow-autopilot` starts nothing in a project that has not been upgraded: its gate names what is left. Follow **Upgrading from 0.3** below before your next task.

### What changed

- **Two modes instead of four levels.** `mode: manual | auto` replaces `merge_unit`. Per-ticket and per-milestone pull requests are gone: in auto mode every task is one branch, `task/<slug>`, created when the task begins, and one pull request into `main`.
- **Starting a run is a command.** `/shilaycow-chief` only agrees the brief with you; saying "start" to it starts nothing. The new `/shilaycow-autopilot` runs the task unattended, and only after a gate script has checked the config, the brief, the bot's identity and role, and the ruleset. Neither skill can be started by the model on its own.
- **A run starts only on the brief you approved.** When you approve it, `/shilaycow-chief` records a `brief-approved` row in the trail; the gate refuses a brief without one, or changed since.
- **The gate compares the ruleset in force with the one setup ships.** No pull request, or no required approval, stops the run; any other difference is a warning that names the setting.
- **The gate asks GitHub itself.** It needs a read-only token of the bot: see Requirements in the README.
- **Verification depth follows each ticket's risk** (low, medium, high), set from what the change touches. The brief's Care level is replaced by **Critical areas**, the parts of your system where any change counts as high.
- **Large work is a chain of tasks** written down in `docs/spec/roadmap.md`, and a documents-only first task can now pass verification.
- **Headings are English only** in briefs, specs and reports.
- The pull request into `main` links to the final report instead of copying it.
- **Final verification converges.** Each failed item is a defect or a gap; a FAIL names where else the same kind of mistake was searched for; a fix round is judged on what changed since the last verdict; `fix_rounds` now stops a run when a defect survives it, and a run with only gaps left hands the pull request to you instead of fixing on.
- **The learning loop runs at the start of the next task.** `/shilaycow-chief` folds earlier Retros into `.shilaycow/pitfalls.md` (each entry now cites its sources, so a fold is never counted twice), and proposes due `shilaycow-correct` changes as scenarios of the new task. A guarded entry moves under `## Guarded` instead of being deleted.
- **The independent verifier starts with the repository it judges** and stops with a message, never judging from memory, when its session has no skills; your setup script must install them in every session of the environment.
- **Gaps and findings become `later` issues** instead of fix rounds; the next task in their area is offered them, and a class seen twice becomes a pitfall. A defect whose cause is already a pitfall gets a guard before its fix.
- **No budget.** The brief has no Budget section and the config no `budget`: how much a run may spend is set by your Claude plan or API account. A run still ends when a defect survives `fix_rounds` or you say stop.
- A ticket that keeps behaviour unchanged (a refactor, a swapped implementation) is checked by breaking that behaviour, since nothing fails before it is built.
- Low-risk work still gets its diff scanned; a project with no app to start is verified by the brief's manual steps.
- Builders work under `.shilaycow/worktrees/`, which `/shilaycow-setup` adds to `.gitignore`; setup also creates the `needs-owner` and `later` labels.
- A trail's header row is its format, and its timestamps come from the clock. A report's "How to try it" says `not run` for anything not actually run. Finishing starts by checking the checkout is the task branch's head.

### Upgrading from 0.3

1. **Finish or drop any task in progress** with the version that started it. A task is in progress while its `task/<slug>` branch is not merged into `main`: merge it, or delete the branch. The tracking issues and `work/` branches of merged tasks can stay.
2. **Update the installed skills.** With the plugin, refresh the marketplace and then update the plugin:

   ```bash
   claude plugin marketplace update shilaycow
   ```

   ```bash
   claude plugin update shilaycow@shilaycow
   ```

   The new version loads in your next session, or after `/reload-plugins` in a running one. Inside a session the same is `/plugin`, the **Installed** tab, the plugin, **Update now**.

   With the cloud setup script: the script copies and never deletes, so first remove the old folders from the environment, for example by adding `rm -rf "${HOME:-/root}"/.claude/skills/shilaycow-*` before the `cp` line once.
3. **Delete any copy of the skills inside your repository.** Some projects copied them into `.claude/skills/` (`go`, `setup`, `sharpen`, `verify` and the rest, or `shilaycow-*`). A copy there is loaded beside the installed skills, and the old `go` can start unattended work by itself. Keep your project's own try-it skill, renaming `drive-<app>` to `try-<app>`.
4. **Give every entry in `.shilaycow/pitfalls.md` a `Sources:` line** naming the tracking issues whose `Retro:` or owner comments are already folded into that entry, for example `Sources: #2, #6`. Leave out a tracking issue whose Retro is not in the file yet: the next task folds it, and only if no entry cites it. If 0.3's `shilaycow-correct` deleted an entry and no other entry cites its source, add one line for it under a `## Guarded` heading at the end, with its `Sources:`, so it is not folded back in.
5. **Bring old headings up to date** in `docs/spec/` and in any brief you will reuse, and delete any budget section from them; nothing reads it any more. Merged reports can stay as they are. If you have no `docs/spec/` and no brief to reuse, skip this step. The 0.4 headings are:

   - in `docs/spec/`: Scenarios, Rules, Not yet built;
   - in a brief: Goal, Out of scope, Scenarios, How to try it, Critical areas, Assumptions. Critical areas replaces Care level: list the areas where any change matters, or write None.

   Steps 3 to 5 are renames and deletions; any session can do them in manual mode, in one pull request you merge.
6. **Run `/shilaycow-setup` again.** Its pull request replaces `merge_unit` and `budget` with `mode: auto` in `.shilaycow/config.yml`, adds `.shilaycow/worktrees/` to `.gitignore`, and walks you through the one new step: a read-only token of the bot for the gate. It checks the token by running the gate on its own branch, before you merge it.
7. **Merge the pull request of steps 3 to 5 and the setup pull request into `main`**, then start the next task with `/shilaycow-chief`. If anything is left, `/shilaycow-autopilot` says what.
