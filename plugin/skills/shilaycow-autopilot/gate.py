#!/usr/bin/env python3
"""The gate in front of an unattended run: check that the repository is ready, change nothing.

Run from the root of the project's repository:

    python3 <this skill's folder>/gate.py [slug]

Each line of output is one check:

    PASS   it holds
    FAIL   it does not; the line says what to do about it
    CHECK  a judgement only you can make, with what to look at
    WARN   it does not quite hold, but nothing irreversible follows; say so and go on

What may FAIL: only the boundary (auto mode, the old skill copies that could start work on
their own) and the handover (which task, one at a time, the brief the owner approved). The
shape of the brief is a WARN: the owner has read and approved it, and its form being off
cannot cost what an unwanted unattended run can. Each check names, in a comment, the real
failure it grew from; a check that cannot is removed.

The last line says whether the gate is open. Exit status 1 when anything FAILed, else 0.

Why a script: a check written only as prose can be "judged" to roughly pass. These are
facts about the repository with one right answer, so they are computed, not weighed.
It uses git only. Who the session acts as is left to a CHECK on purpose: a script can only
ask GitHub with a credential of its own, which says nothing about the account the session's
own GitHub tools and pushes use. Only those tools can answer that.
"""

import re
import subprocess
import sys

# The brief's headings.
BRIEF_HEADINGS = ["Goal", "Out of scope", "Scenarios", "How to try it", "Critical areas", "Assumptions"]

# A heading version 0.3 wrote that 0.4 replaced. It is not read as the new one: finding it means
# the project has not been upgraded, and the gate says so instead of guessing.
OLD_HEADINGS = {"Care level": "Critical areas"}
UPGRADE = "written by version 0.3 -> follow 'Upgrading from 0.3' in the shilaycow CHANGELOG"

# Names the harness's skills had before 0.4, when some projects copied them into the repository.
# A copy there is loaded beside the installed skills; the old `go` can start unattended work by
# itself. A folder is taken for such a copy only when its SKILL.md mentions `.shilaycow`, so a
# project's own skill that happens to share a name is left alone.
OLD_SKILL_NAMES = {"blast-radius", "correct", "design", "drive", "go", "how", "plan", "principles", "prove",
                   "report", "retro", "setup", "sharpen", "spec", "status", "trail", "try-it", "verify", "why"}

# Words that often mark a scenario promising more than a finite check can show.
ABSOLUTE = re.compile(r"\b(all|any|every|always|never|wherever|no matter)\b", re.I)

# The tokens in trail.tsv, each followed by the commit that last changed the brief: the Chief
# writes the first when the owner approves the brief, autopilot the second when a run starts.
APPROVED_TOKEN = "brief-approved"
START_TOKEN = "autopilot-start"


class Report:
    def __init__(self):
        self.lines = []
        self.failed = 0
        self.unchecked = 0

    def add(self, kind, check, text=""):
        self.lines.append(f"{kind:<6} {check}" + (f": {text}" if text else ""))
        self.failed += kind == "FAIL"
        self.unchecked += kind == "CHECK"


def git(*args):
    """Run git; return its stdout, or None when it fails."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def read_config(text):
    """Read the flat `key: value` lines of config.yml; nested keys are not needed here."""
    config = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z_]+):\s*([^#]*)", line)
        if match:
            config[match.group(1)] = match.group(2).strip().strip("\"'")
    return config


def sections(markdown):
    """Map each heading's text to everything under it, sub-headings included, up to the
    next heading of the same or a higher level (scenarios usually sit under `### S-1`)."""
    lines = markdown.splitlines()
    headings = [(i, len(m.group(1)), m.group(2)) for i, line in enumerate(lines)
                if (m := re.match(r"^(#{1,4})\s+(.+?)\s*$", line))]
    found = {}
    for n, (start, level, name) in enumerate(headings):
        end = next((i for i, lv, _ in headings[n + 1:] if lv <= level), len(lines))
        found.setdefault(name, "\n".join(lines[start + 1:end]) + "\n")
    return found


def find_section(found, name):
    """The text under a heading; None when absent."""
    for heading, body in found.items():
        if heading.lower().startswith(name.lower()):
            return heading, body
    return None


def old_headings(markdown):
    """Headings of version 0.3 found in a file, as 'old -> new'."""
    return [f"'{h}' -> '{OLD_HEADINGS[k]}'" for h in sections(markdown) for k in OLD_HEADINGS if h.startswith(k)]


def check_brief(report, brief):
    old = old_headings(brief)
    if old:
        # Grew from: 0.4.0 replacing Care level (CHANGELOG, Upgrading from 0.3).
        report.add("WARN", "brief", f"headings {', '.join(old)}: {UPGRADE}")
    # Grew from: a scenario that promised more than a check could show, and the headings the
    # other skills read. Shape only: a WARN.
    found = sections(brief)
    for name in BRIEF_HEADINGS:
        hit = find_section(found, name)
        if hit is None:
            report.add("WARN", f"brief: {name}", "heading missing -> worth filling in with /shilaycow-chief")
        elif not hit[1].strip():
            report.add("WARN", f"brief: {name}", "heading is empty -> worth filling in with /shilaycow-chief")
        else:
            report.add("PASS", f"brief: {name}")
    scenarios = find_section(found, "Scenarios")
    if scenarios and scenarios[1].strip():
        body = scenarios[1]
        if not re.search(r"\bS-\d+", body) or not all(w in body.lower() for w in ("given", "when", "then")):
            report.add("WARN", "brief: scenarios", "scenarios are clearest numbered S-1, S-2, ... as Given / When / Then")
        for line in body.splitlines():
            if ABSOLUTE.search(line) and re.search(r"\bthen\b", line, re.I):
                report.add("WARN", "brief: absolute wording", f"'{line.strip()[:90]}' -> does a finite check really show this?")


def commits_after(trail, token):
    """The commit on each trail row that carries the token, in order. The commit is the first
    hash after the token on that row, so a model that put the word and the commit in two cells
    of one row is still read right."""
    found = []
    for row in trail.splitlines():
        at = row.find(token)
        if at < 0:
            continue
        match = re.search(r"\b([0-9a-f]{7,40})\b", row[at + len(token):])
        if match:
            found.append(match.group(1))
    return found


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    report = Report()

    if git("fetch", "--quiet", "origin") is None:
        report.add("FAIL", "remote", "cannot fetch from origin -> check the network and the repository access")
        return finish(report)
    head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD") or "origin/main"
    default = head.split("/", 1)[1]

    # 1. The config on the default branch asks for auto mode. Grew from: the boundary itself;
    # without setup there is no bot and no ruleset to keep an unattended run out of main.
    text = git("show", f"{head}:.shilaycow/config.yml")
    if text is None:
        report.add("FAIL", "config", "no .shilaycow/config.yml on the default branch: this is manual mode -> run /shilaycow-setup")
        return finish(report)
    config = read_config(text)
    mode = config.get("mode")
    if mode is None and "merge_unit" in config:
        report.add("FAIL", "config", f"merge_unit instead of mode: {UPGRADE}")
        return finish(report)
    if mode != "auto":
        report.add("FAIL", "config", f"mode is '{mode}', not 'auto' -> run /shilaycow-setup")
        return finish(report)
    report.add("PASS", "config", "mode is auto")

    # No copy of the harness's skills inside the repository: they would be loaded beside these.
    # Grew from: an old `go` copy, still in a repository after an upgrade, that could be called
    # and start unattended work by itself.
    copies = [name for name in (git("ls-tree", "--name-only", f"{head}:.claude/skills") or "").splitlines()
              if (name in OLD_SKILL_NAMES or name.startswith("shilaycow-"))
              and ".shilaycow" in (git("show", f"{head}:.claude/skills/{name}/SKILL.md") or "")]
    if copies:
        report.add("FAIL", "skill copies", f".claude/skills/{{{','.join(copies)}}} in the repository {UPGRADE}")
    else:
        report.add("PASS", "skill copies", "no copy of the harness's skills in the repository")

    # 2. Exactly one open task, and it has a branch. Grew from: one task at a time (the next
    # starts from the merged main), and autopilot needing to know which brief it runs.
    open_tasks = [b.strip().removeprefix("origin/") for b in
                  (git("branch", "-r", "--no-merged", head, "--list", "origin/task/*") or "").splitlines() if b.strip()]
    if args:
        slug = args[0]
    elif len(open_tasks) == 1:
        slug = open_tasks[0].removeprefix("task/")
    elif not open_tasks:
        report.add("FAIL", "task", "no unmerged task/<slug> branch -> agree a brief with /shilaycow-chief first")
        return finish(report)
    else:
        report.add("FAIL", "task", f"several open tasks ({', '.join(open_tasks)}) -> one task runs at a time: "
                   "merge or delete all but one")
        return finish(report)
    branch = f"task/{slug}"
    if git("rev-parse", "--verify", "--quiet", f"origin/{branch}") is None:
        report.add("FAIL", "task", f"no {branch} on the remote -> agree a brief with /shilaycow-chief first")
        return finish(report)
    report.add("PASS", "task", f"{branch} exists on the remote")
    others = [b for b in open_tasks if b != branch]
    if others:
        report.add("FAIL", "one task at a time", f"{', '.join(others)} not merged into {default} -> merge it, or delete its branch if it was abandoned")
    else:
        report.add("PASS", "one task at a time")

    # 3. The brief exists (a FAIL: nothing to run without it) and is in shape (WARNs).
    brief = git("show", f"origin/{branch}:docs/tasks/{slug}/brief.md")
    if brief is None:
        report.add("FAIL", "brief", f"no docs/tasks/{slug}/brief.md on {branch} -> agree it with /shilaycow-chief")
        return finish(report)
    check_brief(report, brief)

    # 4. The owner approved this very brief; on a resume, has it changed since the run started?
    # Grew from: a gate that opened on a draft brief, and a start recorded against a later commit
    # than the one approved.
    brief_commit = git("log", "-1", "--format=%h", f"origin/{branch}", "--", f"docs/tasks/{slug}/brief.md") or ""
    trail = git("show", f"origin/{branch}:docs/tasks/{slug}/trail.tsv") or ""
    approvals = commits_after(trail, APPROVED_TOKEN)
    starts = commits_after(trail, START_TOKEN)
    if not approvals and starts:
        # Grew from: a task started before 0.4.0, which has a start and no approval, and which the
        # plain message below called unapproved.
        report.add("FAIL", "approval", f"this task started under a version before 0.4.0 ('{START_TOKEN}' with no "
                   f"'{APPROVED_TOKEN}') -> finish it with that version, or drop it: step 1 of 'Upgrading from 0.3' "
                   "in the shilaycow CHANGELOG")
    elif not approvals:
        report.add("FAIL", "approval", f"no '{APPROVED_TOKEN}' row in trail.tsv: the owner has not approved this brief "
                   "-> approve it with /shilaycow-chief")
    elif approvals[-1][:7] != brief_commit[:7]:
        report.add("FAIL", "approval", f"the brief changed after it was approved ({approvals[-1][:7]} -> {brief_commit}) "
                   "-> have the owner approve this version with /shilaycow-chief")
    else:
        report.add("PASS", "approval", f"the owner approved the brief at {brief_commit}")
    if not starts:
        report.add("PASS", "start", f"first start -> record '{START_TOKEN} {brief_commit}' in trail.tsv before anything else")
    elif brief_commit and starts[-1][:7] == brief_commit[:7]:
        report.add("PASS", "start", f"resuming; the brief is unchanged since {starts[-1][:7]}")
    else:
        report.add("CHECK", "start", f"the brief changed after the run started ({starts[-1][:7]} -> {brief_commit}): "
                   "go on only if the owner approved the change in a comment on the tracking issue, from their own account")

    # 5. Who this session acts as: only its own GitHub tools can say. Grew from: the boundary;
    # acting as the owner would let the agent merge into main past the ruleset.
    report.add("CHECK", "identity", f"ask your GitHub tools who you are (get_me): the login must be the bot "
               f"'{config.get('bot', '')}'. Anything else, the owner above all, and stop: change nothing")
    return finish(report)


def finish(report):
    print("\n".join(report.lines))
    if report.failed:
        print(f"gate: closed ({report.failed} failed). Change nothing; tell the user what to fix.")
        return 1
    if report.unchecked:
        print(f"gate: open once the {report.unchecked} CHECK item(s) hold")
    else:
        print("gate: open")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
