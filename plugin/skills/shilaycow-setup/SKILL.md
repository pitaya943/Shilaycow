---
name: shilaycow-setup
description: "Use once per repository to put the boundary on GitHub (a bot account, a ruleset) and write the shilaycow config, or again to check the real settings still match. Don't use to start a task: use shilaycow-chief."
---

# Setup

Put the one boundary in place: `main` changes only through a pull request the owner approves, and the agent's account cannot approve its own. Then record the settings every other skill reads.

Manual mode needs none of this: with no config, every skill works in the user's own session and merges nothing. This skill turns on auto mode, where `/shilaycow-chief` agrees a brief with the user and `/shilaycow-autopilot` runs it unattended.

## Inputs

A GitHub repository and its owner in the conversation. Ask as little as you can find out yourself: the owner is the repository's owner in its remote URL, and the bot is who your GitHub tools say you are when you act as the bot; ask the owner only to confirm both. Do not ask for a test command: take it from what the repository already runs (`package.json`, `pyproject.toml`, `Makefile`, a CI workflow), or leave it empty in a new project. The first task that adds a test suite sets it, in its own pull request.

First find out who you are on GitHub, because that decides who does what:

- **You act as the bot** (the usual case in a cloud session). You cannot change repository settings, and that is the point of the boundary. The owner does the privileged steps by hand on github.com; you do everything else and check the result.
- **You act as the owner with admin rights** (a local session with the owner's `gh`). You can do all of it yourself.

## Done when

All of these hold, and you have shown the owner what you checked:

1. The bot account is a collaborator with the Write role, not Admin.
2. A ruleset on the default branch requires a pull request with one approval, dismisses stale approvals on push, and blocks force pushes and deletion. The only bypass is the repository admin role, for pull requests only: the owner can merge their own pull request without a second approver, and nobody can push to the branch directly. `ruleset.json` beside this file is that ruleset.
3. The repository setting **Automatically delete head branches** is on, so a branch goes once its pull request is merged. Where your GitHub tools do not show the setting, the owner confirms it.
4. `.shilaycow/config.yml` exists with `owner`, `bot`, `mode: auto`, `test_command` (empty while the project has no tests), `fix_rounds`.
5. `CLAUDE.md`, which sessions read when they start, has the section in `claude-section.md` beside this file, copied as it is: the owner's standing permission to push branches, and where each piece of state lives. It names places, never one task's details, so it stays the same from task to task. An existing section is updated to match. Where the project keeps its rules in `AGENTS.md`, the section goes there and `CLAUDE.md` imports it with a line `@AGENTS.md`; `.gitignore` ignores `.shilaycow/worktrees/`, where builders work, and `__pycache__/`, which running the hook or a test leaves behind. Add the setup files to the commit by path, never all at once.
6. `.github/workflows/shilaycow-verdict.yml` is a copy of `workflows/shilaycow-verdict.yml` beside this file. It posts the status `shilaycow/verdict` on the head of each pull request into the default branch, whoever opened it: green only when the newest verdict naming that exact commit is a PASS, so a push after the verdict turns it red again. Once it is on the default branch, the ruleset requires that status from GitHub Actions, with branches up to date (`by-hand.md` step 2), and GitHub refuses to merge a head nobody judged. `.gitattributes` has the line `docs/tasks/*/trail.tsv merge=union`, so trail rows that two sessions append at once both survive a merge instead of conflicting. `.claude/hooks/shilaycow-guard.py` is a copy of `hooks/shilaycow-guard.py` beside this file, and `.claude/settings.json` runs it as the `PreToolUse` hooks in `hooks/settings.json`. It blocks a push to the default branch and a merge, whoever the session acts as: the second lock, for a session the ruleset would let through. Where `.claude/settings.json` exists, add the two entries to its `PreToolUse` list and keep everything else.
7. Items 4 to 6 are on a branch with a pull request open, not pushed to `main`; the labels `needs-owner` and `later` exist on the repository. Read each with your GitHub tools; where they cannot create a label, the owner creates it by hand (`by-hand.md`).
8. The owner has a cloud environment whose setup script is `install-skills.sh` beside this file, and knows to start this project's sessions in it. A repository's own plugin settings are not loaded in cloud sessions.

## How

**As the bot.** Walk the owner through items 1 to 3 and the labels one step at a time, from `by-hand.md` beside this file, and wait for them to say each is done. Meanwhile write items 4 to 6 and open the pull request. Then check, and say for each item whether you confirmed it or the owner must look:

- who you are, and that you can push a branch but hold no admin role;
- the rules in force on the default branch. They can be read without admin rights (`GET /repos/<owner>/<repo>/rules/branches/<branch>`); compare them with `ruleset.json`. If you cannot reach that from here, say so and ask the owner to read the ruleset page to you.

Never test the boundary by trying to push to `main`.

**As the owner.** Do items 1 to 3 with `gh api`, sending `ruleset.json` as the body, then items 4 to 7, the labels included. The owner still does what only a person can: accepting the invitation as the bot, and connecting GitHub on claude.ai to the bot account with the Claude GitHub App installed on this repository.

Either way: say why at each step. Two files are the harness's own: `.claude/hooks/shilaycow-guard.py` and `.github/workflows/shilaycow-verdict.yml`. When either differs from this version's copy, replace it in the setup pull request, so an upgrade reaches them. Never overwrite any other file that exists; add a section or report the difference. Once the project has a workflow that runs its test command on pull requests, the ruleset also requires that check to pass (`required_status_checks`, `by-hand.md` step 2), so a red suite cannot be merged whatever a verdict says; until then, passing tests rest on the verifier's run, and the setup check says so. Propose that workflow; the owner adds it, since it lives under `.github/`.

To check an existing setup, compare each item with what GitHub reports and list actual against expected. Change nothing. A config written by version 0.3 has `merge_unit` in place of `mode`, and often a `budget`: that is the upgrade the CHANGELOG describes, so in the setup pull request put `mode: auto` in place of `merge_unit` and remove `budget`.

When every item holds, the owner merges the setup pull request. Once they say it is merged, fetch and check that the config is on the default branch, then end with the next step in plain words: setup is done, and the first task starts by typing `/shilaycow-chief` (`/shilaycow:shilaycow-chief` for a plugin install) with what they want built, in this session or a new one in the same environment. Do not start a session for them: the Chief needs them present, and a session nobody opens is left behind.

## Stop when

- The repository shows signs of production use (deploy configuration, real secrets, `.env` files). Say that this is outside what the harness guards and let the owner decide.
- Rulesets are unavailable on this repository's plan. Report it; do not substitute something weaker silently.
- You act as the owner in a cloud session. Stop: the sessions that will do the work must act as the bot, and switching the connection mid-session breaks a session's GitHub access. Have the owner connect the bot first.

## Outputs

A setup pull request and what you checked; when you act as the owner, also the ruleset and the collaborator invitation.
