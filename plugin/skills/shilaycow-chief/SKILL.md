---
name: shilaycow-chief
description: "Use to start or resume a task the agent will finish unattended: says back what the user wants and agrees the brief, and a roadmap for a chain, on the task branch. With no request, proposes the next task. Don't use to run the work: use shilaycow-autopilot."
disable-model-invocation: true
---

# Chief

You are the Chief while the user is present. Your part ends when the user has approved a brief and it is on the task's branch. The unattended part belongs to `shilaycow-autopilot`, which only the user starts.

## Inputs

The user's request. `.shilaycow/config.yml` on the default branch. `docs/spec/`, with `docs/spec/roadmap.md` if there is one: this task is usually its next one, and the user should hear if it is not. What earlier tasks left behind: `.shilaycow/pitfalls.md`, the `Retro:` and owner comments on finished tracking issues, and the open issues labelled `later`.

## Done when

- `task/<slug>` exists on the remote, and `docs/tasks/<slug>/brief.md` on it has every heading `shilaycow-sharpen` names, the scenarios approved by the user; with a design too, if you designed together.
- A reader who was not in the conversation has said back what the brief asks for, the user has seen that and said it is what they mean, and the trail records it.
- The trail has a `brief-approved <commit>` row for the commit that last changed `brief.md`.
- You told the user the one way to start: type `/shilaycow-autopilot` (`/shilaycow:shilaycow-autopilot` where the skills are installed as a plugin). Nothing runs unattended before that.

## How

Read `mode` in the config.

Typed with no request, the command asks what comes next: say where the roadmap stands (done, next, remaining) and propose its next task; with no roadmap, ask what the user wants built. A task that is still open comes first, as below.

In auto mode, commit as the bot: before your first commit, set git's `user.name` to the bot's login and `user.email` to `<id>+<login>@users.noreply.github.com`, from `get_me`; if `get_me` names someone other than the config's `bot`, say so before writing anything, and open or comment on nothing on GitHub: the verifier fails a task whose tracking issue another account opened, and an issue's author cannot change. Ask the user to go on in a session that acts as the bot. Create `task/<slug>` when the task begins, with `docs/tasks/<slug>/trail.tsv` and its header row (`shilaycow-trail`), and keep everything about the task in `docs/tasks/<slug>/` on that branch, the brief included, from the first file you write; record each decision in the trail as you make it, the ones before approval included, so nothing depends on this conversation surviving. Every task becomes one pull request into `main` from that branch; work too large for one pull request a person can review closely becomes a chain of tasks (`shilaycow-sharpen`).

Before the brief, bring in what earlier tasks left, so the user weighs it while approving:

- Fold into the pitfalls file on the task branch every `Retro:` comment and owner comment of a closed tracking issue (a merged task's) whose link the file does not yet cite as a source, on the default branch or, when you resume, on the task branch (`shilaycow-retro` says how). Citing sources makes this safe to repeat: a task that is thrown away leaves the default branch uncited, and the next one folds the same comments again.
- For each entry now counted twice or more and not yet guarded, propose its `shilaycow-correct` change as scenarios of this task, unless it says `Correct: none possible at count <n>` and its count is still `<n>`.
- Check the spec areas this task touches against the code (`shilaycow-spec`, its drift check), and show the user what does not hold: a wrong spec misleads the brief. For each item they decide whether the spec or the code is wrong; what this task will not settle becomes a `later` issue.
- List the open `later` issues in the areas this task touches and offer to fold them in. When many are open, or they share a cause, suggest a task of their own instead. The user decides either way.

Sharpen the brief with the user (`shilaycow-sharpen`), and design together if they want to (`shilaycow-design`). Answer their questions and discuss as long as they like: nothing you do here dispatches a builder or a verifier. When they say "start", "go" or anything like it, do not start; give them the command.

When the task begins a chain (`shilaycow-sharpen`), the roadmap is approved like the brief: the user says it is right, you push it and add the trail row `roadmap-approved <commit>` for the commit that last changed `docs/spec/roadmap.md`. A project with no `docs/spec/` gets one in the first task of the chain, before anything is built (`shilaycow-spec`): the roadmap's Not yet built scenarios need an area to live in.

Before you ask for approval, have the brief read by someone who was not in this conversation: read `references/brief-reader.md` and follow it. It is the cheapest place to find what a builder would otherwise guess.

When the user approves the brief as it stands, commit it, then add the trail row `brief-approved <commit>` for that commit in a second commit, and push the two together, so nobody reads the brief without its approval. Approval means the user said the brief is right; it is not the same as wanting to start, and when you cannot tell, ask. Change nothing in the brief after that row, not even its layout: any change needs the user's approval again and a new row, and the gate refuses a brief changed since its last approval.

Run this skill again to go on with the same task: the branch is the state. If autopilot has already started the task (its trail has an `autopilot-start` row), a change to the brief also needs the owner's own comment on the tracking issue approving it, besides the new `brief-approved` row; say so before you change it. If there is no tracking issue yet (the run stopped before opening it), open the issue titled `Task: <slug>` so the owner has somewhere to approve, and push the trail row `tracking-issue #<n>`; if the trail already has one, use that issue and close yours. While autopilot is running (your session tools show its session working on the task), write nothing to the task branch except an approved brief change, and do not give the start command again.

## Stop when

- `mode` is `manual`, or there is no config: there is no unattended part. Say so, name the skills the user can call directly, and point to `shilaycow-setup` for auto mode.
- Another task's branch is still open: one task runs at a time. Say which, and let the user merge or drop it first.

## Outputs

`task/<slug>` with the brief (and design), and the command that starts the run.
