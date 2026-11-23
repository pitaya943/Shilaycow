# The two steps only the owner can do

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

## After both

Tell the session they are done. It reads the rules in force and compares them with `ruleset.json`.
