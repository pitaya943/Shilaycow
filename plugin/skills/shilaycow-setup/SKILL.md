---
name: shilaycow-setup
description: Use once per repository to make GitHub itself keep agents out of main and to write the shilaycow config, or again at any time to check that the real settings still match. Works in a cloud session acting as the bot, where the owner does two steps by hand, or in a local session with the owner's gh.
---

# Setup

Put the one boundary in place: `main` changes only through a pull request the owner approves, and the agent's account cannot approve its own. Then record the settings every other skill reads.

Manual mode needs none of this: with no config, every skill works in the user's own session and merges nothing. This skill turns on auto mode, where `/shilaycow-chief` agrees a brief with the user and `/shilaycow-autopilot` runs it unattended.

## Inputs

A GitHub repository and its owner in the conversation. Ask one question at a time: the owner's login, the bot's login, the test command.

First find out who you are on GitHub, because that decides who does what:

- **You act as the bot** (the usual case in a cloud session). You cannot change repository settings, and that is the point of the boundary. The owner does the two privileged steps by hand on github.com; you do everything else and check the result.
- **You act as the owner with admin rights** (a local session with the owner's `gh`). You can do all of it yourself.

## Done when

All of these hold, and you have shown the owner what you checked:

1. The bot account is a collaborator with the Write role, not Admin.
2. A ruleset on the default branch requires a pull request with one approval, dismisses stale approvals on push, and blocks force pushes and deletion. The only bypass is the repository admin role, for pull requests only: the owner can merge their own pull request without a second approver, and nobody can push to the branch directly. `ruleset.json` beside this file is that ruleset.
3. `.shilaycow/config.yml` exists with `owner`, `bot`, `mode: auto`, `test_command`, `parallel_builders`, `fix_rounds`, `report_language` (`en` unless the owner names another language).
4. `AGENTS.md` has a section pointing at `.shilaycow/`, naming the branch classes (`task/`, `work/`, `spike/`) and saying only the owner merges `main`; `.gitignore` ignores `.shilaycow/worktrees/`, where builders work.
5. Items 3 and 4 are on a branch with a pull request open, not pushed to `main`; the labels `needs-owner` and `later` exist on the repository (the bot's Write role can create them).
6. The owner has a cloud environment whose setup script is `install-skills.sh` beside this file, and knows to start this project's sessions in it. A repository's own plugin settings are not loaded in cloud sessions.
7. The autopilot gate can reach the GitHub API as the bot: a token of the bot is saved for `api.github.com` (step 3 of `by-hand.md`), and `gate.py --github-only`, the script beside `shilaycow-autopilot`'s `SKILL.md`, run from the repository root, shows `PASS` for identity, role and ruleset.

## How

**As the bot.** Walk the owner through items 1, 2 and 7 one step at a time, from `by-hand.md` beside this file, and wait for them to say each is done. Meanwhile write items 3 and 4 and open the pull request. Then check, and say for each item whether you confirmed it or the owner must look:

- who you are, and that you can push a branch but hold no admin role;
- the rules in force on the default branch. They can be read without admin rights (`GET /repos/<owner>/<repo>/rules/branches/<branch>`); compare them with `ruleset.json`. If you cannot reach that from here, say so and ask the owner to read the ruleset page to you.

Never test the boundary by trying to push to `main`.

**As the owner.** Do items 1 and 2 with `gh api`, sending `ruleset.json` as the body, then items 3 to 5. The owner still does what only a person can: accepting the invitation as the bot, and connecting GitHub on claude.ai to the bot account with the Claude GitHub App installed on this repository.

Either way: say why at each step, and never overwrite a file that exists; add a section or report the difference. If the project has a test command, propose a workflow that runs it as a required check; the owner adds it, since it lives under `.github/`.

To check an existing setup, compare each item with what GitHub reports and list actual against expected. Change nothing. A config written by version 0.3 has `merge_unit` in place of `mode`, and often a `budget`: that is the upgrade the CHANGELOG describes, so in the setup pull request put `mode: auto` in place of `merge_unit` and remove `budget`.

## Stop when

- The repository shows signs of production use (deploy configuration, real secrets, `.env` files). Say that this is outside what the harness guards and let the owner decide.
- Rulesets are unavailable on this repository's plan. Report it; do not substitute something weaker silently.
- You act as the owner in a cloud session. Stop: the sessions that will do the work must act as the bot, and switching the connection mid-session breaks a session's GitHub access. Have the owner connect the bot first.

## Outputs

A setup pull request and what you checked; when you act as the owner, also the ruleset and the collaborator invitation.
