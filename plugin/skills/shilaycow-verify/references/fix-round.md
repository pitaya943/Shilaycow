# A fix round

Read this when you are given the verdict before this one: a fix round, or a merge of `main` into the branch, which is judged the same way.

Judge what changed since then, not the whole branch again:

- run the full suite;
- redo every check that verdict failed, with the search for its class;
- read the diff between the two heads against `shilaycow-principles`;
- break the behaviours that diff touches.

Link the earlier verdict in yours. If the diff changes code the product runs, rather than tests, documents or developer tools, do every check again as for a first verdict. The additions for a pull request into `main` (the brief against its approval, who opened it, blast radius against `main`) are always redone: a fix can change any of them.

When a ticket was judged on its own and none of its files has changed since that verdict's commit (show the empty `git diff --stat <that commit>..<head> -- <its files>`), you may rely on that verdict for the ticket, with a link to it, instead of breaking its behaviours again, whatever its risk; run its tests in the full suite all the same. Everything else is judged as for a first verdict.
