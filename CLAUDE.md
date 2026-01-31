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

## Evaluation Criteria

Papers are assessed using these criteria:
- being correct
  - does the claim make sense with the available data / assumptions?
  - no crontradictions
  - no overclaiming
  - no signs of AI slop
- likelyhood of mattering
  - significant step forward
  - will likely be cited well

Make sure to read *all* abstracts, before forming an opinion.

## Known authors

Watch for papers whose author list includes one of the names in `authors.md`.

## Output

The top 5 papers according to the critera above. Title and authors,
and why you think it made the cut.

List of papers by known authors.

Bust of the day, the paper that you think has the largest bullshit-factor, in the
sense that you don't believe what is claimed. Explain why

For every paper mentioned, include a link to https://arxiv.org/abs/<arxiv_id>
