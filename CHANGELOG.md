# Changelog

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
