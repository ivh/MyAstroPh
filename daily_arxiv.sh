#!/bin/bash
set -euo pipefail

export PATH="/Users/tom/.local/bin:/opt/homebrew/bin:$PATH"
exec 2>&1

cd /Users/tom/astro-ph

echo "$(date): starting"
git clean -f
curl -s "https://arxiv.org/list/astro-ph/new" -o arxiv_new.html
echo "$(date): parsing"
uv run python parse_arxiv.py > papers.txt
echo "$(date): running claude ($(wc -l < papers.txt) lines)"

PROMPT=$(cat CLAUDE.md)

RESULT=$(cat papers.txt | claude -p "$PROMPT" --model sonnet --output-format text)
echo "$(date): claude done, sending mail"
/opt/homebrew/bin/msmtp -t <<EOF
To: t@tmy.se
Subject: arXiv astro-ph digest $(date +%Y-%m-%d)
From: ivh@fastmail.se

$RESULT
EOF
echo "$(date): done"
