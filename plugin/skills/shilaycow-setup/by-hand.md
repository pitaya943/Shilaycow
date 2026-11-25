# The steps only the owner can do

Relay these to the owner one at a time, and wait for each. They are done in a browser on github.com, signed in as the owner. Menu names are GitHub's own English labels.

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

**Once the setup pull request is merged**, so the verdict workflow is on the default branch: GitHub lists a check here only after it has run once, so first have a session open a pull request into the default branch that changes one line, wait until it shows a red `shilaycow/verdict`, and close it without merging. Then edit the same ruleset, tick **Require status checks to pass**, add the check `shilaycow/verdict`, set its source to **GitHub Actions**, so only the workflow can turn it green, not a status posted by an account, and tick **Require branches to be up to date before merging**, so the commit you merge is the commit that was judged: updating a branch from the default branch makes a new head, whose status is red until it is judged again. The setup pull request itself has no verdict: merge it before this step. From then on a task's pull request can be merged only at a head with a PASS; you can still bypass the rule as admin, deliberately, for a pull request you made yourself.

**Later, once the project runs its tests in a workflow on pull requests:** edit the same ruleset, tick **Require status checks to pass**, and add that workflow's check. From then on a pull request whose tests fail cannot be merged, whatever a verdict says. Run `/shilaycow-setup` again afterwards; it reads the rules in force and confirms the check.

## 3. Delete branches once they are merged

1. In the repository open **Settings**, then **General**, and scroll to **Pull Requests**.
2. Tick **Automatically delete head branches**.

Why: every task and ticket works on its own branch, merged by a pull request. With this on, each one goes as soon as it is merged, and only open work is left.

## 4. Create two labels

1. In the repository open **Issues**, then **Labels**, then **New label**.
2. Create `needs-owner` (for a decision only the owner can make), then `later` (for a gap or finding left for a later task).

Why: a run files issues under these labels, and the session's GitHub tools can label an issue but cannot create a label. Skip this step if the session says it created them.

## After all four

Tell the session they are done. It reads the rules in force and compares them with `ruleset.json`, setting by setting.
