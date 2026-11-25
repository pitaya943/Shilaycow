# The brief reader

A reader who was not in the conversation reads the brief before the user approves it. You have heard everything the user said, so you read into the brief what they meant; the builders and the verifier will have only what it says. What this reader cannot say back, they will guess.

## For the Chief: starting the reader

When the brief is complete and before you ask for approval:

1. Push the brief, so the reader reads the version on the task branch.
2. Start a subagent with your subagent tool, giving it the path of this file and the path of `brief.md`, and nothing else: no summary, no conversation, no hint of what you expect it to find. If your tools cannot start a subagent, tell the user that a read in this same conversation is not a fresh read, skip it, and record that in the trail.
3. Show the user its reply as it is, with one question: is this what you mean?
4. Where it is not, or where the reader found a gap that matters, change the brief with the user and run the reader once more on the new version. After that second read, what remains is the user's to accept or fix by hand; do not run it a third time.
5. Add a trail row: the brief's commit the reader read, and whether the user found it matched or the brief changed.

## For the reader

You have not seen the conversation that produced this brief, and you will not see it. Read only `docs/tasks/<slug>/brief.md`, the index of `docs/spec/` if there is one, and the shilaycow section of `CLAUDE.md`. Change nothing.

Reply with these five parts, plainly, without praise:

1. **What this asks for**: in your own words, two to five sentences. Do not copy its sentences. If you cannot say what a part asks for, say which part.
2. **What a user can do once it is built**: one or two sentences.
3. **Words it does not explain**: terms particular to this project, team or task that the brief uses without saying what they mean, anywhere in the brief. Not general engineering terms, and not the harness's own words that the `CLAUDE.md` section explains (the trail, a ticket, the tracking issue).
4. **Scenarios that cannot be checked as written**: each with why: no observable result, an absolute word ("all", "any", "never") that no check can cover, or a result that depends on something the brief does not settle.
5. **What a builder would have to guess**: at most five questions the brief leaves open that would change what gets built.

Do not propose a design or a solution. Your job is to show what the brief says to someone who was not there.
