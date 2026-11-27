#!/bin/bash
# Install the shilaycow skills where Claude Code reads user-level skills.
# Use as a cloud environment's setup script, or run once on your own machine.
# Pinned to the release it ships with; it removes skills an earlier version left, then copies.
# A failed clone does not fail the script: a failing setup script would stop the session from starting.
rm -rf /tmp/shilaycow-src
git -c advice.detachedHead=false clone -q --depth 1 --branch v0.6.0 https://github.com/pitaya943/shilaycow.git /tmp/shilaycow-src \
  && mkdir -p "${HOME:-/root}/.claude/skills" \
  && rm -rf "${HOME:-/root}"/.claude/skills/shilaycow "${HOME:-/root}"/.claude/skills/shilaycow-* \
  && cp -r /tmp/shilaycow-src/plugin/skills/. "${HOME:-/root}/.claude/skills/" \
  || echo "shilaycow skills were not installed" >&2
