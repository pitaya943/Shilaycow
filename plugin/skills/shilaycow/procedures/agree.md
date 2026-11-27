# Agree

Read this when the user brings a request, or anything about the open task's brief. **You own the brief until the user approves it**; your part here ends when an approved brief is on the task's branch. Nothing here starts unattended work: only the user does, by typing `/shilaycow run`.

## Done when

- `task/<slug>` exists on the remote, and `docs/tasks/<slug>/brief.md` on it has every heading `references/brief.md` names, the scenarios approved by the user; with a design too, if you designed together.
- A reader who was not in the conversation has said back what the brief asks for, the user has seen that and said it is what they mean, and the trail records it.
- `state.py` shows `approved` true: the trail's last `brief-approved <commit>` row names the commit that last changed `brief.md`.
- You told the user the one way to start: type `/shilaycow run` (`/shilaycow:shilaycow run` where the skills are installed as a plugin).

## Before the brief

A task still open comes first: `state.py` lists it, and one task runs at a time. With no request and a roadmap, propose its `next_task`.

Commit as the bot: before your first commit, set git's `user.name` to the bot's login and `user.email` to `<id>+<login>@users.noreply.github.com`, from `get_me`. Create `task/<slug>` when the task begins, with `docs/tasks/<slug>/trail.tsv` and its header row (`references/trail.md`), and keep everything about the task in `docs/tasks/<slug>/` on that branch from the first file you write; record each decision in the trail as you make it, so nothing depends on this conversation surviving. Every task becomes one pull request into `main`; work too large for one pull request a person can review closely becomes a chain of tasks (`references/brief.md`).

Bring in what earlier tasks left, so the user weighs it while approving:

- Fold into the pitfalls file on the task branch every `Retro:` comment and owner comment of a closed tracking issue whose link the file does not yet cite as a source (`references/learning.md`, "Folding it in"). Citing sources makes this safe to repeat.
- For each entry now counted twice or more and not yet guarded, propose its correction as scenarios of this task (`references/learning.md`, "Correcting a class"), unless it says `Correct: none possible at count <n>` and its count is still `<n>`.
- When the user asks, or what you read of the code disagrees with the spec, check the areas this task touches for drift (`shilaycow-spec`), and show the user what does not hold. For each item they decide whether the spec or the code is wrong; what this task will not settle becomes a `later` issue.
- List the open `later` issues in the areas this task touches and offer to fold them in. The user decides.

## The brief

Write it with the user as `references/brief.md` describes, and design together if they want to (`shilaycow-plan`, "When the shape is open"). Discuss as long as they like: nothing here dispatches a builder or a verifier. When they say "start", "go" or anything like it, do not start; give them the command.

When the task begins a chain (`references/brief.md`), the roadmap is approved like the brief: the user says it is right, you push it and add the trail row `roadmap-approved <commit>` for the commit that last changed `docs/roadmap.json`, which must go on to pass `state.py`. A project with no `docs/spec/` gets one in the first task of the chain, before anything is built (`shilaycow-spec`).

Before you ask for approval, have a reader who was not in this conversation read the brief: you read into it what the user meant, and builders will have only what it says.

1. Push the brief, so the reader reads the version on the task branch.
2. Start a subagent on `roles/reader.md` (SKILL.md, "Dispatching"), giving it the path of `brief.md` and nothing else: no summary, no hint of what you expect. If you cannot start a subagent, tell the user that a read in this conversation is not a fresh read, skip it, and record that in the trail.
3. Show the user its reply as it is, with one question: is this what you mean?
4. Where it is not, or where the reader found a gap that matters, change the brief with the user and run the reader once more. After that second read, what remains is the user's to accept or fix by hand.
5. Add a trail row: the brief's commit the reader read, and whether the user found it matched or the brief changed.

## Approval

When the user approves the brief as it stands, commit it, then add the trail row `brief-approved <commit>` for that commit in a second commit, and push the two together, so nobody reads the brief without its approval. Approval means the user said the brief is right; it is not the same as wanting to start, and when you cannot tell, ask. Change nothing in the brief after that row, not even its layout: any change needs the user's approval again and a new row, and until then `state.py` shows it unapproved and a run waits.

Typing `/shilaycow` again with the same task goes on with it: the branch is the state. While a run is working on the task (your session tools show it), write nothing to the task branch except an approved brief change, and do not give the start command again.
