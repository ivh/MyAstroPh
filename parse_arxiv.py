from html.parser import HTMLParser
import re
import sys

# arXiv's /list/astro-ph/new page contains three sections: new submissions,
# cross-lists, and replacements. Replacements are papers already announced on an
# earlier day, so they must not reach the digest.
SECTION_RE = re.compile(
    r"<h3>(New|Cross|Replacement) submissions \(showing (\d+) of (\d+) entries\)</h3>"
)
SKIP_SECTIONS = {"Replacement"}


class ArxivParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.papers = []
        self.current_paper = {}
        self.in_title = False
        self.in_abstract = False
        self.in_authors = False
        self.capture_text = ""
        self.in_dt = False
        self.in_dd = False
        # arXiv nests no <div> inside list-title/list-authors today, but count
        # depth so a future nested tag cannot silently truncate the capture.
        self.div_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "dt":
            self.in_dt = True
        elif tag == "dd":
            self.in_dd = True
        elif tag == "a" and self.in_dt:
            href = attrs_dict.get("href", "")
            if "/abs/" in href:
                arxiv_id = href.split("/abs/")[-1]
                self.current_paper = {"id": arxiv_id}
        elif tag == "div":
            if self.in_title or self.in_authors:
                self.div_depth += 1
            elif attrs_dict.get("class") == "list-title mathjax":
                self.in_title = True
                self.div_depth = 0
                self.capture_text = ""
            elif attrs_dict.get("class") == "list-authors":
                self.in_authors = True
                self.div_depth = 0
                self.capture_text = ""
        elif tag == "p" and attrs_dict.get("class") == "mathjax":
            self.in_abstract = True
            self.capture_text = ""

    def handle_endtag(self, tag):
        if tag == "dt":
            self.in_dt = False
        elif tag == "dd":
            self.in_dd = False
            if self.current_paper.get("id") and self.current_paper.get("title"):
                self.papers.append(self.current_paper)
                self.current_paper = {}
        elif tag == "div" and (self.in_title or self.in_authors):
            if self.div_depth:
                self.div_depth -= 1
                return
            text = re.sub(r"\s+", " ", self.capture_text)
            if self.in_title:
                self.current_paper["title"] = text.replace("Title:", "").strip()
                self.in_title = False
            else:
                self.current_paper["authors"] = text.replace("Authors:", "").strip()
                self.in_authors = False
        elif tag == "p" and self.in_abstract:
            self.current_paper["abstract"] = re.sub(r"\s+", " ", self.capture_text).strip()
            self.in_abstract = False

    def handle_data(self, data):
        if self.in_title or self.in_abstract or self.in_authors:
            self.capture_text += data


def parse_section(body):
    parser = ArxivParser()
    parser.feed(body)
    return parser.papers


with open("arxiv_new.html") as f:
    html = f.read()

headings = list(SECTION_RE.finditer(html))
if not headings:
    sys.exit(
        "arxiv_new.html has no section headings -- the page was probably served "
        "stripped. Check that curl sent a browser User-Agent."
    )

sections = []
for i, m in enumerate(headings):
    end = headings[i + 1].start() if i + 1 < len(headings) else len(html)
    sections.append((m.group(1), int(m.group(2)), int(m.group(3)), html[m.end():end]))

papers = []
problems = []
counts = {}
for name, shown, total, body in sections:
    found = parse_section(body)
    counts[name] = len(found)
    if len(found) != shown:
        problems.append(f"{name}: heading says {shown} entries, parsed {len(found)}")
    if shown != total:
        problems.append(f"{name}: page shows only {shown} of {total} entries (paginated?)")
    if name in SKIP_SECTIONS:
        continue
    for p in found:
        p["section"] = name
        papers.append(p)

for line in problems:
    print(f"WARNING: {line}", file=sys.stderr)

for i, p in enumerate(papers, 1):
    label = " [cross-list]" if p["section"] == "Cross" else ""
    print(f"\n{'='*80}")
    print(f"Paper {i}: {p.get('id', 'NO ID')}{label}")
    print(f"Title: {p.get('title', 'NO TITLE')}")
    print(f"Authors: {p.get('authors', 'NO AUTHORS')}")
    print(f"Abstract: {p.get('abstract', 'NO ABSTRACT')}")

skipped = ", ".join(f"{n}: {counts.get(n, 0)}" for n in sorted(SKIP_SECTIONS))
print(f"\n\nTotal papers: {len(papers)}", end="")
print(f" (new: {counts.get('New', 0)}, cross-lists: {counts.get('Cross', 0)};"
      f" skipped {skipped})")
