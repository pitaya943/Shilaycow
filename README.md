# shilaycow

Skills for Claude Code that take a task from a vague idea to a pull request you can trust, while a server-side boundary keeps the agent out of `main`. Built for Claude Code only, locally or in its cloud sessions; other hosts are not supported.

<p align="center">
  <img src="assets/task-flow.webp" alt="How a task flows through shilaycow. With you: /shilaycow says back what you asked and writes a brief, designing together is optional, then you type /shilaycow run and a gate checks setup and brief before handing over. Once the gate holds, unattended, the agent acting as a bot: planning tickets with a risk level each, building, finishing, judging, and fixing on FAIL until a new head gets a new verdict. PASS, then your call on GitHub: ready for you, you merge, merged; or you send it back. Underneath: the bot has Write only and a ruleset protects main, so only you can merge.">
</p>

- **Skills you can use on their own**, one for each practice in the development cycle.
- **Auto mode** composes them behind one command: `/shilaycow` agrees the task with you, then `/shilaycow run` checks that everything is ready and works unattended through fresh builder and verifier sessions. `/shilaycow` alone says where things stand.
- **A boundary on GitHub's servers**: the agent works as a bot with the Write role only, and a ruleset protects `main`, so only you can merge, and only a head an independent verifier passed: a required status turns red on any commit nobody judged. Claude Code's deny rules in your repository are the second lock: they stop `gh pr merge` and the GitHub merge tools even in a session connected as you.

Quality comes from checking results (an independent verifier, reading the code, breaking each behaviour to see its test fail), not from prescribing steps. How it all fits together, with diagrams: **[ARCHITECTURE.md](ARCHITECTURE.md)**.

## Requirements

**Manual mode** (you call each skill yourself) needs only Claude Code and `git`.

**Auto mode** (`/shilaycow`, then `/shilaycow run` working unattended) needs all of the following. `/shilaycow-setup` walks you through them and checks them again whenever you run it. Before every run, `/shilaycow run` checks what can change between runs (auto mode is on, one task, the brief you approved) and confirms it acts as the bot.

| Requirement | Why |
|---|---|
| A GitHub repository where rulesets are available: public, or private on a plan that offers them | the ruleset is what keeps the agent out of `main` |
| A second GitHub account for the agent (the bot), invited to the repository with the **Write** role, never Maintain or Admin | the agent can push branches and open pull requests, but cannot change the ruleset |
| The ruleset from `shilaycow-setup` active on the default branch, and, once the setup pull request is merged, the status `shilaycow/verdict` required in it with GitHub Actions as its source | `main` changes only through a pull request you merge, at a head that has a PASS |
| GitHub Actions enabled on the repository | the workflow `shilaycow-verdict` posts that status |
| The repository setting **Automatically delete head branches** turned on | a task's and its tickets' branches go once merged; tracking issues close when you merge the task, through `Closes #<n>` |
| Sessions that act as the bot: in a cloud environment, GitHub connected on claude.ai as the bot account, with the Claude GitHub App installed on the repository; on your own computer, `git` and `gh` logged in as the bot | acting as you would put the agent past the ruleset |
| Permission for sessions to push `task/`, `work/`, `spike/` and `chore/` branches. `/shilaycow-setup` writes it into your repository's `CLAUDE.md`, which every session reads when it starts, together with a short map of where each piece of state lives; a cloud session otherwise pushes only its own `claude/…` branch. If a session still asks, say so in your first message | the task's work lives on those branches |
| Network access to `github.com` (installing the skills, `git`) | |
| Python 3.9 or later in the session | the gate, `state.py`, is a Python script |
| Sessions able to start other sessions, for the independent verifier, and a setup script that installs the skills in every one of them from a source any session can reach, such as the script below. A verifier session carries only the repository it judges, so a script that copies the skills from another repository gives it none; it then stops and says so. Where the agent cannot start a session, it stops and says so: a verifier must never share a session with the work | the verifier must share nothing with whoever built the work |

Not meant for projects with production environments, real users or real data (see Limits).

## Install

**1. Claude Code (terminal)**

```bash
claude plugin marketplace add pitaya943/shilaycow
```

```bash
claude plugin install shilaycow@shilaycow
```

Plugin skills are namespaced, so you call them as `/shilaycow:shilaycow`, `/shilaycow:shilaycow-how`, and so on. In an open session, the same thing is `/plugin marketplace add pitaya943/shilaycow`, then `/plugin install shilaycow@shilaycow`.

**2. Claude Code cloud environment (setup script)**

Paste this into the environment's **Setup script**. Its network must reach `github.com`.

```bash
rm -rf /tmp/shilaycow-src
git -c advice.detachedHead=false clone -q --depth 1 --branch v0.6.0 https://github.com/pitaya943/shilaycow.git /tmp/shilaycow-src \
  && mkdir -p "${HOME:-/root}/.claude/skills" \
  && rm -rf "${HOME:-/root}"/.claude/skills/shilaycow "${HOME:-/root}"/.claude/skills/shilaycow-* \
  && cp -r /tmp/shilaycow-src/plugin/skills/. "${HOME:-/root}/.claude/skills/" \
  || echo "shilaycow skills were not installed" >&2
```

Every session started in that environment has the skills as `/shilaycow`, `/shilaycow-how`, and so on. Where this README names a command, a plugin install spells it `/shilaycow:shilaycow-…`. A plugin installed on your own computer is not available in cloud sessions, so use the script there. The script installs version 0.5.2 and removes the skills an earlier version left; to move to a later version, change the `--branch` tag. It does not stop the session from starting if the clone fails, so a session without the skills still opens and says the command is unknown.

**Upgrading from 0.3.x:** version 0.4 is not compatible. Follow the steps in [CHANGELOG.md](CHANGELOG.md) before your next task.

## Get started

1. **Once per repository**, if you want the agent to work unattended (auto mode): run `/shilaycow-setup`. Without it every skill still works in manual mode, where you call each one yourself. It walks you through the steps only you can do on github.com (invite a bot account as a Write collaborator, import the ruleset that protects `main`, turn on automatic deletion of merged branches, create the `needs-owner` and `later` labels), writes `.shilaycow/config.yml`, the deny rules in `.claude/settings.json` and the verdict workflow, and opens a pull request for you to merge. Once you merge it, make the status `shilaycow/verdict` required in the ruleset (it tells you how), then start your first task with `/shilaycow`.
2. **For every task**, start with `/shilaycow` and describe what you want. Discuss as long as you like; it writes the brief on the task's branch.
3. **When you approve the brief**, type `/shilaycow run`. It runs a gate first (auto mode is on, the brief is the version you approved, no other task is open; anything off in the brief's shape is a warning, not a stop), and the agent confirms with its own GitHub tools that it acts as the bot. Nothing starts unless every check holds; if one fails, it tells you what to fix. Nothing else starts the unattended part, whatever else you type.

Skipping step 1 is fine: every skill works on its own in your session, and nothing is merged for you.

## Usage

```text
/shilaycow add CSV export to the reports page
/shilaycow run
/shilaycow
/shilaycow I want to understand how billing retries work
/shilaycow-how how does a session token get refreshed?
/shilaycow-why why do we retry payments three times?
/shilaycow-prove the discount must never go below zero
/shilaycow-verify pull request #42
/shilaycow-blast-radius I changed the date parser that billing and reports share
/shilaycow-setup
```

## Which skill should I use?

**Most of the time: `/shilaycow`, then `/shilaycow run`.** Use them for anything that changes how your product behaves. `/shilaycow` sharpens the request into scenarios with you; `/shilaycow run` then plans, builds, verifies and reports on its own, calling the other skills as it needs them. Run `/shilaycow run` again to resume a run, or `/shilaycow` again to go on talking about the brief.

The rest are for when you want one practice on its own:

| You want to… | Use |
|---|---|
| Turn a vague idea into scenarios before anything is built | `/shilaycow` with the idea |
| Understand an area before touching it | `/shilaycow-how` |
| Know why something is the way it is | `/shilaycow-why` |
| Know where a task stands, or which skill fits a job | `/shilaycow` |
| Get a second, independent opinion on a pull request | `/shilaycow-verify` |
| Check what a change to shared code could break | `/shilaycow-blast-radius` |

## Skills

| Phase | Skill | Use it when |
|---|---|---|
| Early | [shilaycow-how](plugin/skills/shilaycow-how/SKILL.md) | you need to know how part of the system works now |
| Early | [shilaycow-why](plugin/skills/shilaycow-why/SKILL.md) | you need to know why something is the way it is, from the record |
| Throughout | [shilaycow-spec](plugin/skills/shilaycow-spec/SKILL.md) | `docs/spec/` should describe what the whole system does now |
| Middle | [shilaycow-plan](plugin/skills/shilaycow-plan/SKILL.md) | a brief is approved: design the shape when the scenarios leave it open, then cut the work into tickets |
| Middle | [shilaycow-prove](plugin/skills/shilaycow-prove/SKILL.md) | you change behaviour and must prove it, never with a test that cannot fail |
| Late | [shilaycow-verify](plugin/skills/shilaycow-verify/SKILL.md) | a pull request needs a PASS or FAIL from a session that built none of it |
| Late | [shilaycow-try-it](plugin/skills/shilaycow-try-it/SKILL.md) | your project needs its own skill for starting and driving the app |
| Late | [shilaycow-blast-radius](plugin/skills/shilaycow-blast-radius/SKILL.md) | a change to shared code could break something elsewhere |
| Composition | [shilaycow](plugin/skills/shilaycow/SKILL.md) | you hand over a whole task: agree its brief, then `run` it unattended to a pull request, with a decision log, a description you can check, and a Retro that keeps its mistakes from repeating; or you want to know where things stand |
| Setup | [shilaycow-setup](plugin/skills/shilaycow-setup/SKILL.md) | a repository needs the bot, the ruleset and the config, or a check that they still hold |
| Throughout | [shilaycow-principles](plugin/skills/shilaycow-principles/SKILL.md) | writing or reviewing code: the judgements a good engineer applies |

## Limits

- Not meant for projects with production environments, real users or real data.
- Every role acts as the same bot account. The verdict check confirms that the head has a PASS from the bot, not that an independent session wrote it; that rests on each verdict's `Session:` line and on the agent cooperating.
- The deny rules match commands by prefix and tools by name: `gh pr merge` inside a script, or a merge through `gh api`, is not refused, and a push you make yourself from a terminal is checked by the ruleset alone. They guard against mistakes; the ruleset and the required verdict are the lock.
- As admin you can still bypass the required verdict when merging; GitHub makes you tick that on purpose.
- The setup script replaces the `shilaycow` skill folder and every `shilaycow-*` one it finds, so a skill you made yourself under that name would be removed.

## Credits

The text is our own; these ideas are not.

- [pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT) and [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): the names and the questions behind `correct`, `blast-radius`, `how`, `why` and `sharpen`, and the ladder of evidence in `blast-radius`.
- [The Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) (Apache-2.0): reviews by a reader who knows least. The brief reader before you approve, the verifier saying the work back before it judges, and the spec checked against the code all come from it.
- Anthropic's engineering writing: [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), for loading a skill's detail only when a step needs it; [effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), for a run that rebuilds its state from the repository and a progress record; [effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); and [demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), for the scenarios the skills are tested against.
- OpenAI's [harness engineering](https://openai.com/index/harness-engineering/): a short map in the file every session reads, not an encyclopedia, and rules enforced by the environment rather than written down.
- Manus's [context engineering lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus): restating the goal in a record the run rereads, which the goal list does.
- Cognition's [Don't build multi-agents](https://cognition.ai/blog/dont-build-multi-agents): one agent decides, and others are handed whole, independent pieces of work.

## License

MIT, see [LICENSE](LICENSE).
