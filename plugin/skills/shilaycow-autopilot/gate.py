#!/usr/bin/env python3
"""The gate in front of an unattended run: check that the repository is ready, change nothing.

Run from the root of the project's repository:

    python3 <this skill's folder>/gate.py [slug]
    python3 <this skill's folder>/gate.py --github-only    (for shilaycow-setup: no task yet)

Each line of output is one check:

    PASS   it holds
    FAIL   it does not; the line says what to do about it
    CHECK  a judgement only you can make, with what to look at
    WARN   a hint for a judgement only you can make

The last line says whether the gate is open. Exit status 1 when anything FAILed, else 0.

Why a script: a check written only as prose can be "judged" to roughly pass. These are
facts about the repository with one right answer, so they are computed, not weighed.
It uses git, and the GitHub REST API for what only GitHub knows (who the session acts as,
the rules on the default branch, the bot's role). The API needs a token for the bot: in a
cloud environment a network secret for api.github.com that the proxy adds to each request,
elsewhere GITHUB_TOKEN, GH_TOKEN or a logged-in `gh`. The toolkit README says how to set it up.
SHILAYCOW_GITHUB_API points the script at another API base URL (the tests use a local one).
"""

import json
import os
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path
import subprocess
import sys

# The brief's headings.
BRIEF_HEADINGS = ["Goal", "Out of scope", "Scenarios", "How to try it", "Critical areas", "Assumptions"]

# Headings version 0.3 wrote. They are not read as the new ones: finding one means the project
# has not been upgraded, and the gate says so instead of guessing.
OLD_HEADINGS = {"目標": "Goal", "不做什麼": "Out of scope", "情境": "Scenarios", "怎麼試": "How to try it",
                "謹慎程度": "Critical areas", "Care level": "Critical areas", "假設": "Assumptions",
                "規則": "Rules", "尚未建置": "Not yet built"}
UPGRADE = "written by version 0.3 -> follow 'Upgrading from 0.3' in the shilaycow CHANGELOG"

# Names the harness's skills had before 0.4, when some projects copied them into the repository.
# A copy there is loaded beside the installed skills; the old `go` can start unattended work by
# itself. A folder is taken for such a copy only when its SKILL.md mentions `.shilaycow`, so a
# project's own skill that happens to share a name is left alone.
OLD_SKILL_NAMES = {"blast-radius", "correct", "design", "drive", "go", "how", "plan", "principles", "prove",
                   "report", "retro", "setup", "sharpen", "spec", "status", "trail", "try-it", "verify", "why"}

# Words that often mark a scenario promising more than a finite check can show.
ABSOLUTE = re.compile(r"\b(all|any|every|always|never|wherever|no matter)\b|全部|任何|所有|不論|一律", re.I)

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
        report.add("FAIL", "brief", f"headings {', '.join(old)}: {UPGRADE}")
        return
    found = sections(brief)
    for name in BRIEF_HEADINGS:
        hit = find_section(found, name)
        if hit is None:
            report.add("FAIL", f"brief: {name}", "heading missing -> fill it in with /shilaycow-chief")
        elif not hit[1].strip():
            report.add("FAIL", f"brief: {name}", "heading is empty -> fill it in with /shilaycow-chief")
        else:
            report.add("PASS", f"brief: {name}")
    scenarios = find_section(found, "Scenarios")
    if scenarios and scenarios[1].strip():
        body = scenarios[1]
        if not re.search(r"\bS-\d+", body) or not all(w in body.lower() for w in ("given", "when", "then")):
            report.add("FAIL", "brief: scenarios", "need numbered scenarios S-1, S-2, ... written as Given / When / Then")
        for line in body.splitlines():
            if ABSOLUTE.search(line) and re.search(r"\bthen\b|那麼", line, re.I):
                report.add("WARN", "brief: absolute wording", f"'{line.strip()[:90]}' -> does a finite check really show this?")


SETUP_HINT = "see Requirements in the shilaycow README"


def github_token():
    """A token from the environment or the GitHub CLI; None when there is none, which is
    normal in a cloud environment, where the proxy adds the network secret instead."""
    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() or None if result.returncode == 0 else None


def api(path, token):
    """GET one GitHub API path. Returns (status, parsed body); status None means no answer."""
    base = os.environ.get("SHILAYCOW_GITHUB_API", "https://api.github.com").rstrip("/")
    request = urllib.request.Request(base + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "shilaycow-gate",
        **({"Authorization": f"Bearer {token}"} if token else {})})
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    context = ssl.create_default_context(cafile=cafile) if cafile else None
    try:
        with urllib.request.urlopen(request, timeout=15, context=context) as response:
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as error:
        return error.code, None
    except (urllib.error.URLError, OSError, ValueError) as error:
        return None, str(error)


def github_checks(report, owner_repo, branch, bot):
    """Who the session acts as, the rules on the default branch, and the bot's role."""
    token = github_token()
    status, user = api("/user", token)
    if status is None:
        report.add("FAIL", "GitHub API", f"no answer from the GitHub API ({user}) -> allow api.github.com; {SETUP_HINT}")
        return
    if status in (401, 403) or not isinstance(user, dict):
        report.add("FAIL", "GitHub API", f"the API refused the request ({status}): no token for the bot -> {SETUP_HINT}")
        return
    login = user.get("login")
    if login != bot:
        report.add("FAIL", "identity", f"the token belongs to '{login}', not the bot '{bot}' -> "
                   "use a token of the bot; never run unattended as the owner")
        return
    report.add("PASS", "identity", f"acting as the bot '{bot}'")

    status, repo = api(f"/repos/{owner_repo}", token)
    permissions = repo.get("permissions", {}) if status == 200 and isinstance(repo, dict) else None
    if permissions is None:
        report.add("FAIL", "role", f"cannot read {owner_repo} ({status}) -> the bot must be a collaborator, and its token must reach this repository")
    elif permissions.get("admin") or permissions.get("maintain"):
        report.add("FAIL", "role", "the bot holds an admin or maintain role, so it could change the ruleset -> give it Write only")
    elif not permissions.get("push"):
        report.add("FAIL", "role", "the bot cannot push -> give it the Write role")
    else:
        report.add("PASS", "role", "the bot can push and cannot change settings")

    status, rules = api(f"/repos/{owner_repo}/rules/branches/{branch}", token)
    if status != 200 or not isinstance(rules, list):
        report.add("FAIL", "ruleset", f"cannot read the rules on {branch} ({status}) -> {SETUP_HINT}")
        return
    check_rules(report, branch, rules)


def check_rules(report, branch, rules):
    """Compare the rules in force with the ruleset shilaycow-setup ships.

    Two things are the boundary and FAIL: a pull request is required, and it needs at least
    one approval (with none, the bot could merge its own pull request into the branch). The
    rest narrows what a mistake can cost without being the boundary, so a difference is a WARN
    naming the setting. Several rulesets can apply to one branch; the strictest value counts."""
    shipped = Path(__file__).resolve().parent.parent / "shilaycow-setup" / "ruleset.json"
    expected = json.loads(shipped.read_text(encoding="utf-8"))["rules"] if shipped.exists() else []
    types = {r.get("type") for r in rules}
    pull_requests = [r.get("parameters") or {} for r in rules if r.get("type") == "pull_request"]
    if not pull_requests:
        report.add("FAIL", "ruleset", f"{branch} does not require a pull request -> run /shilaycow-setup")
        return
    approvals = max(p.get("required_approving_review_count", 0) for p in pull_requests)
    if approvals < 1:
        report.add("FAIL", "ruleset", f"{branch} requires {approvals} approvals, so the bot could merge its own "
                   "pull request -> set Required approvals to 1 (shilaycow-setup)")
        return
    report.add("PASS", "ruleset", f"{branch} requires a pull request with {approvals} approval(s)")
    if not expected:
        report.add("WARN", "ruleset", "ruleset.json is not beside shilaycow-setup, so the other settings were not compared")
    for rule in expected:
        if rule["type"] != "pull_request" and rule["type"] not in types:
            report.add("WARN", "ruleset", f"{branch} has no '{rule['type']}' rule, which ruleset.json has -> see shilaycow-setup")
        for key, want in (rule.get("parameters") or {}).items():
            if key == "required_approving_review_count":
                continue
            have = any(p.get(key) for p in pull_requests) if isinstance(want, bool) else max(p.get(key, 0) for p in pull_requests)
            if have != want:
                report.add("WARN", "ruleset", f"{key} is {json.dumps(have)} on {branch}, {json.dumps(want)} in ruleset.json "
                           "-> see shilaycow-setup")


def owner_repo_of_origin():
    """owner/repo from the origin URL, whatever its form (ssh, https, or a session proxy)."""
    remote = git("remote", "get-url", "origin") or ""
    match = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", remote)
    return f"{match.group(1)}/{match.group(2)}" if match else "<owner>/<repo>"


def main(argv):
    use_github = "--no-github" not in argv
    github_only = "--github-only" in argv
    args = [a for a in argv if not a.startswith("--")]
    report = Report()

    if git("fetch", "--quiet", "origin") is None:
        report.add("FAIL", "remote", "cannot fetch from origin -> check the network and the repository access")
        return finish(report)
    head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD") or "origin/main"
    default = head.split("/", 1)[1]

    # 1. The config asks for auto mode. It is read from the default branch, except with
    # --github-only: setup runs that on its own branch, before its pull request is merged.
    local = Path(".shilaycow/config.yml")
    if github_only and local.exists():
        text = local.read_text(encoding="utf-8")
    else:
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
    if github_only:
        github_checks(report, owner_repo_of_origin(), default, config.get("bot", ""))
        return finish(report)

    # No copy of the harness's skills inside the repository: they would be loaded beside these.
    copies = [name for name in (git("ls-tree", "--name-only", f"{head}:.claude/skills") or "").splitlines()
              if (name in OLD_SKILL_NAMES or name.startswith("shilaycow-"))
              and ".shilaycow" in (git("show", f"{head}:.claude/skills/{name}/SKILL.md") or "")]
    if copies:
        report.add("FAIL", "skill copies", f".claude/skills/{{{','.join(copies)}}} in the repository {UPGRADE}")
    else:
        report.add("PASS", "skill copies", "no copy of the harness's skills in the repository")

    # The living spec on the default branch must have been upgraded too.
    spec_files = [f for f in (git("ls-tree", "-r", "--name-only", head, "docs/spec") or "").splitlines() if f.endswith(".md")]
    stale = [f for f in spec_files if old_headings(git("show", f"{head}:{f}") or "")]
    if stale:
        report.add("FAIL", "spec", f"{', '.join(stale)} {UPGRADE}")
    elif spec_files:
        report.add("PASS", "spec", "docs/spec/ uses the current headings")

    # 2. Exactly one open task, and it has a branch.
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
        report.add("FAIL", "task", f"several open tasks ({', '.join(open_tasks)}) -> name one: /shilaycow-autopilot <slug>")
        return finish(report)
    branch = f"task/{slug}"
    if git("rev-parse", "--verify", "--quiet", f"origin/{branch}") is None:
        report.add("FAIL", "task", f"no {branch} on the remote -> agree a brief with /shilaycow-chief first")
        return finish(report)
    report.add("PASS", "task", f"{branch} exists on the remote, so this session can push task branches")
    others = [b for b in open_tasks if b != branch]
    if others:
        report.add("FAIL", "one task at a time", f"{', '.join(others)} not merged into {default} -> merge it, or delete its branch if it was abandoned")
    else:
        report.add("PASS", "one task at a time")

    # 3. The brief is complete.
    brief = git("show", f"origin/{branch}:docs/tasks/{slug}/brief.md")
    if brief is None:
        report.add("FAIL", "brief", f"no docs/tasks/{slug}/brief.md on {branch} -> agree it with /shilaycow-chief")
        return finish(report)
    check_brief(report, brief)

    # 4. The owner approved this very brief; on a resume, has it changed since the run started?
    brief_commit = git("log", "-1", "--format=%h", f"origin/{branch}", "--", f"docs/tasks/{slug}/brief.md") or ""
    trail = git("show", f"origin/{branch}:docs/tasks/{slug}/trail.tsv") or ""
    approvals = re.findall(rf"{APPROVED_TOKEN}\s+([0-9a-f]{{7,40}})", trail)
    starts = re.findall(rf"{START_TOKEN}\s+([0-9a-f]{{7,40}})", trail)
    if not approvals:
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

    # 5. What only GitHub knows.
    if use_github:
        github_checks(report, owner_repo_of_origin(), default, config.get("bot", ""))
    else:
        report.add("CHECK", "GitHub", "skipped (--no-github): identity, role and ruleset were not checked")
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
