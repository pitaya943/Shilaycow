#!/usr/bin/env python3
"""A PreToolUse hook that stops an agent from changing the default branch itself.

The ruleset on GitHub already keeps the bot out of main. This is the second lock, for the case the
ruleset cannot see: a session that acts as the owner, whose account the ruleset lets through. It runs
in Claude Code before each Bash command and each GitHub tool call, and blocks:

  - a git push to the default branch (main, master, or whatever origin/HEAD names), or of every branch,
    however it is wrapped (env, command, sudo, bash -c), and a push that names no branch after the same
    command changed branch or directory;
  - a merge on GitHub's side (a GitHub tool's merge, gh pr merge, the API), whatever its base. Such a
    call names only the pull request, not the branch it changes, so the hook cannot tell main from a
    task branch. A local git merge changes nothing on GitHub; the push that follows names its target,
    and is checked like any push. That is how a ticket lands on the task branch;
  - writing a file or moving a ref on the default branch through the GitHub tools or the API;
  - a push or merge built at run time ($(...), backticks, eval), which cannot be read here;
  - posting a commit status or a check run, which could make the verdict check the ruleset requires
    look green without a verdict;
  - a push to a shared branch (task/ or work/) that is not a compare-and-swap: it must carry
    --force-with-lease=<branch>:<the commit fetched> (empty when creating the branch), and a push to
    task/ must also be a fast-forward of that commit. Two sessions writing the same branch then cannot
    lose each other's commits: the second push is refused, and the fix is to fetch, merge and push again.

Blocking exits 2 with the reason on stderr, which Claude Code shows the agent. It fails closed: input
it cannot read is blocked too, since a lock that opens when confused is not a lock. Standard library only.
"""

import json
import re
import shlex
import subprocess
import sys

PROTECTED = {"main", "master"}
# Git options that take a value, so the word after them is not the subcommand.
GIT_VALUE_OPTIONS = {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
OWNER_ONLY = "only the owner merges into the default branch; open or update a pull request instead"
SHARED = ("task/", "work/")
CAS = "shared branch"  # reasons that start with this are about task/ and work/, not the default branch


def protected_branches():
    names = set(PROTECTED)
    try:
        head = subprocess.run(["git", "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
        if head:
            names.add(head.rsplit("/", 1)[-1])
    except (OSError, subprocess.SubprocessError):
        pass
    return names


def current_branch():
    try:
        return subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def segments(command):
    """Split a shell command into simple commands, at ;, &&, ||, | and newlines."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
    lexer.whitespace_split = True
    lexer.commenters = ""
    current = []
    for token in lexer:
        if token and set(token) <= set(";&|"):
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current


def git_subcommand(words):
    """For a git command line, the subcommand and its arguments; None if this is not git."""
    if not words or words[0].rsplit("/", 1)[-1] != "git":
        return None
    i = 1
    while i < len(words) and words[i].startswith("-"):
        i += 2 if words[i] in GIT_VALUE_OPTIONS else 1
    return words[i:] if i < len(words) else None


def refspec_target(spec):
    """The branch a push refspec writes to: 'a:b' writes b, 'a' writes a."""
    spec = spec.lstrip("+")
    target = spec.split(":", 1)[1] if ":" in spec else spec
    return target.removeprefix("refs/heads/")


# Words that run the command after them, so the real command starts later on the line.
WRAPPERS = {"env", "command", "sudo", "nohup", "time", "exec", "nice", "builtin"}
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def unwrap(words):
    """Drop leading wrappers, their options and VAR=value assignments: `env X=1 git push` is git."""
    i = 0
    while i < len(words):
        word = words[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", word):
            i += 1
        elif word.rsplit("/", 1)[-1] in WRAPPERS:
            i += 1
            while i < len(words) and words[i].startswith("-"):
                i += 2 if words[i] in ("-u", "-g", "-n") else 1
        else:
            break
    return words[i:]


def lease(flags, target):
    """The expected commit a --force-with-lease=<target>:<commit> flag names ('' to create), or None."""
    for flag in flags:
        if flag.startswith("--force-with-lease="):
            ref, sep, expect = flag.split("=", 1)[1].partition(":")
            if sep and ref.removeprefix("refs/heads/") == target:
                return expect
    return None


def fast_forward(expect, source):
    """True when the commit pushed contains the commit fetched, so nothing on the remote is dropped."""
    try:
        return subprocess.run(["git", "merge-base", "--is-ancestor", expect, source],
                              capture_output=True, timeout=5).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def how_to_push(target):
    return (f"{CAS} {target}: push it as a compare-and-swap. Run `git fetch origin`, merge origin/{target} if it "
            f"moved, then `git push --force-with-lease={target}:<the commit origin/{target} names> origin {target}`, "
            f"with that commit written out (empty after the colon when creating the branch)")


def check_shared(spec, target, flags, branch):
    if spec.startswith("+") or any(f in ("-f", "--force") for f in flags):
        return f"{CAS} {target}: a forced push could drop another session's commits"
    expect = lease(flags, target)
    if expect is None:
        return how_to_push(target)
    if target.startswith("task/") and expect:
        source = spec.split(":", 1)[0] if ":" in spec else spec
        if branch is None:
            return f"{CAS} {target}: run the push from the checkout itself, so the hook can check it"
        if not fast_forward(expect, source or "HEAD"):
            return (f"{CAS} {target}: what you push does not contain {expect}; fetch, merge origin/{target} "
                    f"(never rebase it) and push again")
    return None


def check_push(args, protected, branch):
    """branch is the branch checked out when this push runs, or None when the command made that unknowable."""
    flags = [a for a in args if a.startswith("-")]
    if any(f in ("--all", "--mirror") for f in flags):
        return "pushing every branch would include the default branch"
    if any(f in ("--delete", "-d") for f in flags):
        rest = [a for a in args if not a.startswith("-")]
        if any(refspec_target(r) in protected for r in rest[1:]):
            return "deleting the default branch"
        return None
    positional = [a for a in args if not a.startswith("-")]
    refspecs = positional[1:]  # the first positional word is the remote
    if not refspecs or any(refspec_target(s) == "HEAD" for s in refspecs):
        if branch is None:
            return "this push names no branch, and the command changes where it runs; name the branch to push"
        if branch in protected:
            return f"a push of HEAD from {branch} pushes to the default branch"
    for spec in refspecs:
        if refspec_target(spec) in protected:
            return f"pushing to {refspec_target(spec)}"
    if not refspecs and branch and branch.startswith(SHARED):
        return how_to_push(branch)
    for spec in refspecs:
        target = refspec_target(spec)
        if target == "HEAD":
            if branch is None or not branch.startswith(SHARED):
                continue
            target, spec = branch, "HEAD:" + branch
        if target.startswith(SHARED):
            reason = check_shared(spec, target, flags, branch)
            if reason:
                return reason
    return None


def api_write(words, tool):
    """For a gh api or curl call: (method, the request path, the -f/-d fields) when it writes, else None."""
    method, fields, path = None, [], None
    i = 1
    while i < len(words):
        word = words[i]
        if word in ("-X", "--method", "--request") and i + 1 < len(words):
            method = words[i + 1].upper()
            i += 2
            continue
        if word in ("-f", "-F", "--field", "--raw-field", "-d", "--data", "--data-raw", "--input") and i + 1 < len(words):
            fields.append(words[i + 1])
            i += 2
            continue
        if not word.startswith("-") and ("/" in word or word.startswith("repos")) and path is None:
            path = word
        i += 1
    if method is None:
        method = "POST" if fields else "GET"
    if method not in WRITE_METHODS or path is None:
        return None
    return method, path, fields


def check_api(words, protected):
    call = api_write(words, words[0])
    if call is None:
        return None
    method, path, fields = call
    joined = " ".join(fields)
    if re.search(r"/merges\b", path) or re.search(r"/pulls/\d+/merge\b", path):
        return OWNER_ONLY
    if re.search(r"/statuses/|/check-runs\b|/check-suites\b", path):
        return "posting a commit status or check by hand; the verdict check is the workflow's to post"
    ref = re.search(r"/git/refs/heads/([^?\s]+)", path)
    if ref and ref.group(1) in protected:
        return f"changing {ref.group(1)} through the API"
    if re.search(r"/git/refs\b", path) and any(f"refs/heads/{b}" in joined for b in protected):
        return "changing the default branch through the API"
    if re.search(r"/contents/", path):
        branch = re.search(r"branch=([^\s&]+)", joined)
        if branch is None or branch.group(1) in protected:
            return "writing a file to the default branch through the API (no branch, or the default branch)"
    return None


def check_bash(command, protected, branch=...):
    """Check every simple command on the line, following which branch each one runs on."""
    if branch is ...:
        branch = current_branch()
    # Commands built at run time cannot be read here; when they could push or merge, fail closed.
    if re.search(r"\$\(|`", command) and re.search(r"\b(push|merge)\b", command):
        return "a push or merge inside a command substitution cannot be checked"
    for words in segments(command):
        words = unwrap(words)
        if not words:
            continue
        name = words[0].rsplit("/", 1)[-1]
        if name == "eval" and re.search(r"\b(git|gh|curl)\b", " ".join(words)):
            return "eval of a git, gh or curl command cannot be checked"
        if name in SHELLS and "-c" in words:
            inner = words[words.index("-c") + 1] if words.index("-c") + 1 < len(words) else ""
            reason = check_bash(inner, protected, branch)
            if reason:
                return reason
            continue
        if name in ("cd", "pushd", "popd"):
            branch = None  # another directory may be another checkout, on another branch
            continue
        sub = git_subcommand(words)
        if sub is not None:
            elsewhere = any(w in ("-C", "--git-dir", "--work-tree") for w in words[1:words.index(sub[0])])
            if sub[0] in ("checkout", "switch"):
                rest = [a for a in sub[1:] if a not in ("-q", "--quiet", "-f", "--force")]
                new = next((rest[i + 1] for i, a in enumerate(rest) if a in ("-b", "-B", "-c", "-C") and i + 1 < len(rest)), None)
                target = new or next((a for a in rest if not a.startswith("-")), None)
                branch = None if elsewhere else (target if target and target != "-" else None)
            elif sub[0] == "push":
                reason = check_push(sub[1:], protected, None if elsewhere else branch)
                if reason:
                    return reason
        # A local `git merge` is harmless until it is pushed, and the push is checked above.
        if name == "gh" and words[1:3] == ["pr", "merge"]:
            return OWNER_ONLY
        if (name == "gh" and words[1:2] == ["api"]) or name == "curl":
            reason = check_api(words if name == "curl" else [words[0]] + words[2:], protected)
            if reason:
                return reason
    return None


def check_github_tool(tool, tool_input, protected):
    if re.search(r"merge_pull_request|enable_pr_auto_merge", tool):
        return OWNER_ONLY
    if re.search(r"push_files|create_or_update_file|delete_file", tool):
        if str(tool_input.get("branch", "")) in protected:
            return "writing to the default branch through the GitHub tools"
    return None


def main():
    try:
        data = json.load(sys.stdin)
        tool = data.get("tool_name", "")
        tool_input = data.get("tool_input") or {}
    except (ValueError, AttributeError) as error:
        print(f"shilaycow guard: could not read the tool call ({error}); blocked to be safe", file=sys.stderr)
        return 2
    protected = protected_branches()
    try:
        if tool == "Bash":
            reason = check_bash(str(tool_input.get("command", "")), protected)
        else:
            reason = check_github_tool(tool, tool_input, protected)
    except ValueError as error:  # an unbalanced quote: shlex cannot split it
        reason = f"could not parse the command ({error})"
    if reason:
        tail = "" if reason.startswith(CAS) else (" The default branch changes only through a pull request "
                                                  "the owner merges.")
        print(f"shilaycow guard: blocked: {reason}.{tail}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
