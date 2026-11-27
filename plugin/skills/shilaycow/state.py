#!/usr/bin/env python3
"""Where the project stands, computed from git: which task is open, whether its brief is approved,
which tickets have landed, how many fix rounds are used, and which task the roadmap names next.

Run from the root of the project's repository:

    python3 <this skill's folder>/state.py [slug]

It prints one JSON object and changes nothing. Trust it over your memory: it is recomputed from the
repository every time. It reads git only, so it cannot see GitHub: verdicts, the tracking issue and
the owner's comments are for your GitHub tools. That includes who you act as.

`problems` lists what must not be worked past; the exit status is 1 when it is not empty. Each check
says, in a comment, the failure it grew from or what it protects.
`warnings` are the brief's shape: the owner approved it as it is, so they never stop a run.

Standard library only; Python 3.9.
"""

import json
import re
import subprocess
import sys

BRIEF_HEADINGS = ["Goal", "Out of scope", "Scenarios", "How to try it", "Critical areas", "Assumptions"]
ABSOLUTE = re.compile(r"\b(all|any|every|always|never|wherever|no matter)\b", re.I)
ROADMAP = "docs/roadmap.json"
ROADMAP_FIELDS = {"slug": str, "goal": str, "depends_on": list, "pr": (str, type(None)), "done": bool}


def git(*args):
    """Run git; return its stdout, or None when it fails."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def read_config(text):
    """The flat `key: value` lines of config.yml."""
    config = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z_]+):\s*([^#]*)", line)
        if match:
            config[match.group(1)] = match.group(2).strip().strip("\"'")
    return config


def trail_cells(trail, token, argument):
    """The argument after the token on each trail row, in order.

    A row records a token in one cell that is exactly '<token> <argument>', or, when a model split
    them, in a cell that is exactly the token followed later by a cell that is the argument (models
    have written both). A token inside prose ("the earlier brief-approved 1a2b3c4 is superseded")
    is not a record: reading it would take an old commit for the current one."""
    whole = re.compile(rf"^{re.escape(token)}\s+({argument})$")
    alone = re.compile(rf"^(?:{argument})$")
    found = []
    for row in trail.splitlines():
        cells = [c.strip() for c in row.split("\t")]
        for i, cell in enumerate(cells):
            match = whole.match(cell)
            if match:
                found.append(match.group(1))
                break
            if cell == token:
                later = next((c for c in cells[i + 1:] if alone.match(c)), None)
                if later:
                    found.append(later)
                break
    return found


def brief_warnings(brief):
    """The brief's shape. Grew from: the headings the other skills read, and a scenario that
    promised more than a finite check could show."""
    warnings, lines = [], brief.splitlines()
    heads = [(i, len(m.group(1)), m.group(2)) for i, line in enumerate(lines) if (m := re.match(r"^(#{1,4})\s+(.+?)\s*$", line))]
    body = {}
    for n, (start, level, name) in enumerate(heads):
        end = next((i for i, lv, _ in heads[n + 1:] if lv <= level), len(lines))
        body.setdefault(name.lower(), "\n".join(lines[start + 1:end]))
    for name in BRIEF_HEADINGS:
        text = next((t for h, t in body.items() if h.startswith(name.lower())), None)
        if text is None or not text.strip():
            warnings.append(f"brief: '{name}' is {'missing' if text is None else 'empty'}")
    scenarios = next((t for h, t in body.items() if h.startswith("scenarios")), "")
    if scenarios.strip() and (not re.search(r"\bS-\d+", scenarios)
                              or not all(w in scenarios.lower() for w in ("given", "when", "then"))):
        warnings.append("brief: scenarios are clearest numbered S-1, S-2, ... as Given / When / Then")
    for line in scenarios.splitlines():
        if ABSOLUTE.search(line) and re.search(r"\bthen\b", line, re.I):
            warnings.append(f"brief: '{line.strip()[:80]}' -> does a finite check really show this?")
    return warnings


def roadmap(text):
    """(tasks, problems) for docs/roadmap.json: {"tasks": [{slug, goal, depends_on, pr, done}, ...]}.
    A new session must compute the next task, not guess it."""
    try:
        tasks = json.loads(text)["tasks"]
        assert isinstance(tasks, list)
    except (ValueError, KeyError, TypeError, AssertionError):
        return [], [f"{ROADMAP} is not an object with a list 'tasks'"]
    problems, slugs = [], []
    for n, task in enumerate(tasks):
        if not isinstance(task, dict):
            problems.append(f"{ROADMAP}: entry {n + 1} is not an object")
            continue
        for field, kind in ROADMAP_FIELDS.items():
            if not isinstance(task.get(field), kind):
                problems.append(f"{ROADMAP}: entry {n + 1} needs '{field}' ({'string or null' if field == 'pr' else kind.__name__})")
        slugs.append(task.get("slug"))
    if problems:
        return [], problems
    deps = {t["slug"]: t["depends_on"] for t in tasks}
    if len(deps) != len(tasks):
        problems.append(f"{ROADMAP}: a slug is listed twice")
    for task in tasks:
        unknown = [d for d in task["depends_on"] if d not in deps]
        if unknown:
            problems.append(f"{ROADMAP}: '{task['slug']}' depends on unknown {', '.join(unknown)}")
        if task["done"] and not task["pr"]:
            problems.append(f"{ROADMAP}: '{task['slug']}' is done but names no pull request")
    seen, path = set(), []

    def cycle(slug):
        if slug in path:
            return path[path.index(slug):] + [slug]
        if slug in seen or slug not in deps:
            return None
        seen.add(slug)
        path.append(slug)
        found = next((c for d in deps[slug] if (c := cycle(d))), None)
        path.pop()
        return found

    loop = next((c for s in deps if (c := cycle(s))), None)
    if loop:
        problems.append(f"{ROADMAP}: the dependencies loop: {' -> '.join(loop)}")
    return (tasks if not problems else []), problems


def next_task(tasks):
    """The first task not done whose dependencies are all done."""
    done = {t["slug"] for t in tasks if t["done"]}
    return next((t["slug"] for t in tasks if not t["done"] and set(t["depends_on"]) <= done), None)


def state(argv):
    out = {"task": None, "approved": False, "brief_commit": None, "open_tasks": [], "tickets": {},
           "fix_rounds": {"limit": 2, "used": {}, "exhausted": []}, "next_task": None, "bot": None, "problems": [], "warnings": []}
    problems = out["problems"]
    # --prune: a task branch deleted on GitHub must not linger here as an open task.
    if git("fetch", "--prune", "--quiet", "origin") is None:
        problems.append("cannot fetch from origin -> check the network and the repository access")
        return out
    head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD") or "origin/main"

    # The config asks for auto mode. Grew from: the boundary; without setup there is no bot and no
    # ruleset to keep an unattended run out of main.
    text = git("show", f"{head}:.shilaycow/config.yml")
    config = read_config(text or "")
    out["bot"] = config.get("bot")
    if config.get("fix_rounds", "").isdigit():
        out["fix_rounds"]["limit"] = int(config["fix_rounds"])
    if text is None:
        problems.append("no .shilaycow/config.yml on the default branch: manual mode -> run /sc-setup")
    elif config.get("mode") != "auto":
        problems.append(f"mode is '{config.get('mode')}', not 'auto' -> run /sc-setup again (see the CHANGELOG)")

    tasks = []
    road = git("show", f"{head}:{ROADMAP}")
    if road is not None:
        tasks, found = roadmap(road)
        problems.extend(found)
        out["next_task"] = next_task(tasks)

    # One task at a time: the next starts from the merged main.
    out["open_tasks"] = sorted(b.strip().removeprefix("origin/task/") for b in
                               (git("branch", "-r", "--no-merged", head, "--list", "origin/task/*") or "").splitlines() if b.strip())
    slug = argv[0] if argv else (out["open_tasks"][0] if len(out["open_tasks"]) == 1 else None)
    if slug is None:
        if len(out["open_tasks"]) > 1:
            problems.append(f"several open tasks ({', '.join(out['open_tasks'])}) -> one runs at a time: merge or delete all but one")
        return out
    out["task"] = slug
    others = [t for t in out["open_tasks"] if t != slug]
    if others:
        problems.append(f"task/{', task/'.join(others)} not merged -> merge it, or delete its branch if it was abandoned")
    branch = f"origin/task/{slug}"
    if git("rev-parse", "--verify", "--quiet", branch) is None:
        problems.append(f"no task/{slug} on the remote -> agree a brief first")
        return out
    # A roadmap task starts only once what it depends on is done.
    entry = next((t for t in tasks if t["slug"] == slug), None)
    waiting = [d for d in (entry or {}).get("depends_on", []) if not any(t["slug"] == d and t["done"] for t in tasks)]
    if waiting:
        problems.append(f"'{slug}' depends on {', '.join(waiting)}, not done in {ROADMAP}")

    # The approval names the commit that last changed the brief. Grew from: a gate that
    # opened on a draft brief, and a brief changed after it was approved.
    brief = git("show", f"{branch}:docs/tasks/{slug}/brief.md")
    if brief is None:
        problems.append(f"no docs/tasks/{slug}/brief.md on task/{slug} -> agree it first")
        return out
    out["warnings"] = brief_warnings(brief)
    out["brief_commit"] = git("log", "-1", "--format=%h", branch, "--", f"docs/tasks/{slug}/brief.md")
    trail = git("show", f"{branch}:docs/tasks/{slug}/trail.tsv") or ""
    approvals = trail_cells(trail, "brief-approved", r"[0-9a-f]{7,40}")
    out["approved"] = bool(approvals) and approvals[-1][:7] == (out["brief_commit"] or "")[:7]

    # Tickets: the work/ branches on the remote, landed or not on the task branch.
    for ref in (git("branch", "-r", "--list", f"origin/work/{slug}/*") or "").splitlines():
        ref = ref.strip()
        landed = git("merge-base", "--is-ancestor", ref, branch) is not None
        out["tickets"][ref.rsplit("/", 1)[-1]] = "landed" if landed else "open"

    # Fix rounds: one trail row `fix-round <T-nn or main>` per round, counted here so a
    # loop that never passes stops at the limit instead of running on.
    rounds = out["fix_rounds"]
    for scope in trail_cells(trail, "fix-round", r"T-\d+|main"):
        rounds["used"][scope] = rounds["used"].get(scope, 0) + 1
    rounds["exhausted"] = sorted(s for s, n in rounds["used"].items() if n >= rounds["limit"])
    return out


def main(argv):
    out = state(argv)
    print(json.dumps(out, indent=2))
    return 1 if out["problems"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
