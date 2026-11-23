# shilaycow

Skills for Claude Code that take a task from a vague idea to a pull request you can trust, while a server-side boundary keeps the agent out of `main`.

<p align="center">
  <img src="assets/task-flow.webp" alt="How a task flows through shilaycow. With you: sharpening, designing together, you say start. Approved, then unattended, the agent acting as a bot: planning, building, finishing, judging, and fixing on FAIL until a new head gets a new verdict. PASS, then your call on GitHub: ready for you, you merge, merged; or you send it back. Underneath: the bot has Write only and a ruleset protects main, so only you can merge.">
</p>

- **18 skills you can use on their own**, one for each practice in the development cycle.
- **Chief mode** (`/shilaycow-chief`) composes them: it agrees the task with you, then works unattended through fresh builder and verifier sessions.
- **A boundary on GitHub's servers**: the agent works as a bot with the Write role only, and a ruleset protects `main`, so only you can merge.

Quality comes from checking results (an independent verifier, reading the code, breaking each behaviour to see its test fail), not from prescribing steps. How it all fits together, with diagrams: **[ARCHITECTURE.md](ARCHITECTURE.md)**.

## Install

**1. Claude Code (terminal)**

```bash
claude plugin marketplace add pitaya943/shilaycow
```

```bash
claude plugin install shilaycow@shilaycow
```

Plugin skills are namespaced, so you call them as `/shilaycow:shilaycow-chief`, `/shilaycow:shilaycow-sharpen`, and so on. In an open session, the same thing is `/plugin marketplace add pitaya943/shilaycow`, then `/plugin install shilaycow@shilaycow`.

**2. Claude Code cloud environment (setup script)**

Paste this into the environment's **Setup script**. Its network must reach `github.com`.

```bash
rm -rf /tmp/shilaycow-src
git clone -q --depth 1 https://github.com/pitaya943/shilaycow.git /tmp/shilaycow-src \
  && mkdir -p "${HOME:-/root}/.claude/skills" \
  && cp -r /tmp/shilaycow-src/plugin/skills/. "${HOME:-/root}/.claude/skills/" \
  || echo "shilaycow skills were not installed"
```

Every session started in that environment has the skills as `/shilaycow-chief`, `/shilaycow-sharpen`, and so on. A plugin installed on your own computer is not available in cloud sessions, so use the script there. To stay on one version, add `--branch v0.3.2` to the `git clone`.

## Get started

1. **Once per repository**, if you want the agent to work unattended: run `/shilaycow-setup`. It walks you through the two steps only you can do on github.com (invite a bot account as a Write collaborator, import the ruleset that protects `main`), writes `.shilaycow/config.yml`, and opens a pull request for you to merge.
2. **For every task**, start with `/shilaycow-chief` and describe what you want. Nothing runs unattended until you approve its brief and say start.

Skipping step 1 is fine: every skill works on its own in your session, and nothing is merged for you.

## Usage

```text
/shilaycow-chief add CSV export to the reports page
/shilaycow-chief resume csv-export
/shilaycow-status
/shilaycow-sharpen users keep asking for dark mode
/shilaycow-how how does a session token get refreshed?
/shilaycow-why why do we retry payments three times?
/shilaycow-prove the discount must never go below zero
/shilaycow-verify pull request #42
/shilaycow-blast-radius I changed the date parser that billing and reports share
/shilaycow-correct the same timezone bug has come back twice
/shilaycow-setup
```

## Which skill should I use?

**Most of the time: `/shilaycow-chief`.** Use it for anything that changes how your product behaves. It sharpens the request into scenarios with you, then plans, builds, verifies and reports on its own, calling the other skills as it needs them. Start it again with the same task to resume.

The rest are for when you want one practice on its own:

| You want to… | Use |
|---|---|
| Turn a vague idea into scenarios before anything is built | `/shilaycow-sharpen` |
| Understand an area before touching it | `/shilaycow-how` |
| Know why something is the way it is | `/shilaycow-why` |
| Know where a task stands and what it is waiting on | `/shilaycow-status` |
| Get a second, independent opinion on a pull request | `/shilaycow-verify` |
| Check what a change to shared code could break | `/shilaycow-blast-radius` |
| Stop a mistake that keeps coming back | `/shilaycow-correct` |

## Skills

| Phase | Skill | Use it when |
|---|---|---|
| Early | [shilaycow-sharpen](plugin/skills/shilaycow-sharpen/SKILL.md) | a goal is vague, large or new: say it back, write a brief of scenarios you approve |
| Early | [shilaycow-how](plugin/skills/shilaycow-how/SKILL.md) | you need to know how part of the system works now |
| Early | [shilaycow-why](plugin/skills/shilaycow-why/SKILL.md) | you need to know why something is the way it is, from the record |
| Throughout | [shilaycow-spec](plugin/skills/shilaycow-spec/SKILL.md) | `docs/spec/` should describe what the whole system does now |
| Middle | [shilaycow-design](plugin/skills/shilaycow-design/SKILL.md) | a brief is approved and the system's shape should come from its scenarios |
| Middle | [shilaycow-plan](plugin/skills/shilaycow-plan/SKILL.md) | the work should be cut into tickets and milestones |
| Middle | [shilaycow-prove](plugin/skills/shilaycow-prove/SKILL.md) | you change behaviour and must prove it, never with a test that cannot fail |
| Late | [shilaycow-verify](plugin/skills/shilaycow-verify/SKILL.md) | a pull request needs a PASS or FAIL from a session that built none of it |
| Late | [shilaycow-try-it](plugin/skills/shilaycow-try-it/SKILL.md) | your project needs its own skill for starting and driving the app |
| Late | [shilaycow-blast-radius](plugin/skills/shilaycow-blast-radius/SKILL.md) | a change to shared code could break something elsewhere |
| Late | [shilaycow-trail](plugin/skills/shilaycow-trail/SKILL.md) | long or unattended work should log each decision made in place of asking |
| Late | [shilaycow-report](plugin/skills/shilaycow-report/SKILL.md) | someone has to decide whether to merge |
| End of cycle | [shilaycow-retro](plugin/skills/shilaycow-retro/SKILL.md) | a task is finishing and its pitfalls should not repeat |
| End of cycle | [shilaycow-correct](plugin/skills/shilaycow-correct/SKILL.md) | the same class of mistake has happened twice |
| Composition | [shilaycow-chief](plugin/skills/shilaycow-chief/SKILL.md) | you hand over a whole task |
| Setup | [shilaycow-setup](plugin/skills/shilaycow-setup/SKILL.md) | a repository needs the bot, the ruleset and the config, or a check that they still hold |
| Setup | [shilaycow-status](plugin/skills/shilaycow-status/SKILL.md) | you want to know where a task stands, without changing anything |
| Throughout | [shilaycow-principles](plugin/skills/shilaycow-principles/SKILL.md) | writing or reviewing code: the judgements a good engineer applies |

## Limits

- Not meant for projects with production environments, real users or real data.
- The setup script copies and never deletes: if a later version removes or renames a skill, delete its old folder from `~/.claude/skills/` yourself.

## Credits

Everything here is written from scratch; no text is copied from other projects. Some ideas come from [pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT) and [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT).

## License

MIT, see [LICENSE](LICENSE).
