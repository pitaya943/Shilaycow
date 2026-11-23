#!/bin/bash
# Install the shilaycow skills where Claude Code reads user-level skills.
# Use as a cloud environment's setup script, or run once on your own machine.
# To stay on one version, add `--branch <tag>` to the clone.
rm -rf /tmp/shilaycow-src
git clone -q --depth 1 https://github.com/pitaya943/shilaycow.git /tmp/shilaycow-src \
  && mkdir -p "${HOME:-/root}/.claude/skills" \
  && cp -r /tmp/shilaycow-src/plugin/skills/. "${HOME:-/root}/.claude/skills/" \
  || echo "shilaycow skills were not installed"
