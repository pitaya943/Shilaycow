# The steps only the owner can do

Relay these to the owner one at a time, in their language, and wait for each. They are done in a browser on github.com, signed in as the owner. Menu names are GitHub's own English labels.

## 1. Invite the bot with the Write role

1. Open the repository, then **Settings**, then **Collaborators** (under Access).
2. Choose **Add people**, enter the bot's login, and pick the role **Write**. Not Maintain, not Admin: with either of those the bot could change the rule in step 2.
3. Sign in to GitHub as the bot (a private browser window keeps the owner signed in) and accept the invitation, from the email or from `https://github.com/<owner>/<repo>/invitations`.

Why: the bot needs to push branches and open pull requests, and must not be able to change settings.

## 2. Protect the default branch

The quick way is to import the ruleset this harness ships:

1. Save `plugin/skills/shilaycow-setup/ruleset.json` from the shilaycow repository to your computer (open the file on github.com and use **Download raw file**).
2. In your repository open **Settings**, then **Rules**, then **Rulesets**.
3. Choose **New ruleset**, then **Import a ruleset**, and select the file.
4. Check that **Enforcement status** is **Active**, then **Create**.

If the import is refused, create it by hand: **New ruleset**, then **New branch ruleset**, and set

- Ruleset name: `protect-main`; Enforcement status: **Active**;
- Bypass list: add **Repository admin**, and set it to **For pull requests only**;
- Target branches: **Include default branch**;
- Rules: tick **Restrict deletions**, **Block force pushes**, and **Require a pull request before merging** with Required approvals **1** and **Dismiss stale pull request approvals when new commits are pushed**.

Leave everything else off, and **Create**.

Why: after this, the only way into the default branch is a pull request. The bot opens it and cannot approve its own; the owner merges it. The owner can still merge their own pull requests without a second person.

## 3. Give the gate a read-only way to ask GitHub

`/shilaycow-autopilot` starts nothing until a script has confirmed, through the GitHub API, who the session acts as, that the bot holds the Write role and no more, and that the default branch requires a pull request. That needs a token of the bot.

1. Signed in as the bot, make the token. A fine-grained token can only select repositories its own account owns, and this one belongs to you, so:
   - **A public repository:** **Settings**, **Developer settings**, **Personal access tokens**, **Fine-grained tokens**, **Generate new token**. Repository access: **Public repositories**. Add no permissions. It can read public repositories and change nothing, which is all the gate needs.
   - **A private repository:** the same page, but **Tokens (classic)**, with the `repo` scope. It can do no more than the bot's Write role allows, and it stays in the network secret, out of the session's sight.
2. In a Claude Code cloud environment: open the environment's settings and add a **network secret** for the host `api.github.com`, sent in the `Authorization` header as `Bearer <token>`. Saving it also lets sessions reach that host; the session never sees the token, the network proxy adds it to each request. On your own computer instead: set `GITHUB_TOKEN` to the token, or log `gh` in as the bot.

Why: the gate's answers come from GitHub itself, not from the agent's reading of a page, so a session connected as the wrong account cannot start an unattended run.

## After all three

Tell the session they are done. It reads the rules in force, compares them with `ruleset.json`, and runs the gate.
