#!/bin/bash
set -euo pipefail

cd /Users/tom/astro-ph

git clean -f
curl -s "https://arxiv.org/list/astro-ph/new" -o arxiv_new.html
uv run python parse_arxiv.py > papers.txt

PROMPT=$(cat CLAUDE.md)

cat papers.txt | claude -p "$PROMPT" --model opus --output-format text | \
  mail -s "arXiv astro-ph digest $(date +%Y-%m-%d)" t@tmy.se
