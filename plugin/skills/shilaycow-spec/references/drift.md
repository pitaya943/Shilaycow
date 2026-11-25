# Checking an area for drift

The spec goes stale when code changes without it. Read this when asked to check one or more areas against the code as it is now. You change nothing: the result is a list for the owner, who decides for each item whether the spec or the code is wrong.

## What to check

Only the areas you were given. For each scenario under the area's `Scenarios` heading, find what implements it and what shows it:

- **holds**: you found the code that does it and a test that would fail without it, or you ran it and saw it;
- **contradicted**: the code does something else; say what, with a file and line;
- **unshown**: you found the code but nothing shows it works, or you could not find the code; say which;
- **not behaviour**: a sentence that states no behaviour a check could show (a one-off timing, a note of what was not checked); say whether it should stay.

A scenario that makes several claims gets one row per claim.

Then the other direction, briefly: behaviour a user of this area can reach that no scenario or rule mentions, in this area's own terms; what belongs to another area's terms is left to that area. List only what a user would notice, at most five, each with a file and line.

Check each item under `Rules` the same way: the limit or default in the code matches the one written, or it does not.

## How

Read the area file, then search the code and tests for its terms; run a test when reading cannot settle it. Where tests cannot run here, a recorded run counts as evidence only if `git diff <its commit> HEAD` over the code and tests is empty; say which you relied on. Spend minutes, not hours: this runs at the start of a task. Where an item would take longer, mark it **unchecked** and say why.

## The result

One table per area: each scenario and rule with holds, contradicted, unshown, not behaviour or unchecked, and the evidence; then the unmentioned behaviour. End with the items that need a decision, each phrased as a question the owner can answer: is the spec wrong, or the code? Nothing is filed or changed until they answer.
