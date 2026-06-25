# arXiv astro-ph Analysis Workflow

## Fetching New Papers

```bash
# remove old data
git clean
# Download today's new astro-ph submissions
# A browser User-Agent is required; a bare curl gets served a stripped page with only 1 entry.
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" "https://arxiv.org/list/astro-ph/new" -o arxiv_new.html
```

## Parsing Papers

Run the parser script to extract titles, authors, and abstracts:

```bash
uv run python parse_arxiv.py > papers.txt
```

The parser (`parse_arxiv.py`) extracts:
- arXiv ID
- Title
- Authors
- Full abstract

## Analysis

The evaluation criteria and output format are in `PROMPT.md`, which is used together with the parsed papers for the daily digest.
