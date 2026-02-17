# arXiv astro-ph Analysis Workflow

## Fetching New Papers

```bash
# remove old data
git clean
# Download today's new astro-ph submissions
curl -s "https://arxiv.org/list/astro-ph/new" -o arxiv_new.html
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
