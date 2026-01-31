from html.parser import HTMLParser
import re

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
        elif tag == "div" and attrs_dict.get("class") == "list-title mathjax":
            self.in_title = True
            self.capture_text = ""
        elif tag == "div" and attrs_dict.get("class") == "list-authors":
            self.in_authors = True
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
        elif tag == "div" and self.in_title:
            title = self.capture_text.replace("Title:", "").strip()
            title = re.sub(r'\s+', ' ', title)
            self.current_paper["title"] = title
            self.in_title = False
        elif tag == "div" and self.in_authors:
            authors = self.capture_text.replace("Authors:", "").strip()
            authors = re.sub(r'\s+', ' ', authors)
            self.current_paper["authors"] = authors
            self.in_authors = False
        elif tag == "p" and self.in_abstract:
            abstract = re.sub(r'\s+', ' ', self.capture_text).strip()
            self.current_paper["abstract"] = abstract
            self.in_abstract = False
            
    def handle_data(self, data):
        if self.in_title or self.in_abstract or self.in_authors:
            self.capture_text += data

with open("arxiv_new.html", "r") as f:
    html = f.read()

parser = ArxivParser()
parser.feed(html)

for i, p in enumerate(parser.papers, 1):
    print(f"\n{'='*80}")
    print(f"Paper {i}: {p.get('id', 'NO ID')}")
    print(f"Title: {p.get('title', 'NO TITLE')}")
    print(f"Authors: {p.get('authors', 'NO AUTHORS')[:100]}...")
    print(f"Abstract: {p.get('abstract', 'NO ABSTRACT')}")

print(f"\n\nTotal papers: {len(parser.papers)}")
