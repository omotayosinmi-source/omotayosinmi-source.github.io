# -*- coding: utf-8 -*-
"""
Post-build checks for digitalautonomous.co.uk.

Verifies that every internal link resolves, every in-page anchor exists,
every JSON-LD block parses, and that no banned placeholder or unverifiable
claim slipped into the output.

Run:  python _src/check.py
Exit code 1 if anything fails.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []
WARNS = []


def fail(page, msg):
    FAILS.append("%s: %s" % (page, msg))


def warn(page, msg):
    WARNS.append("%s: %s" % (page, msg))


def html_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "_src", "node_modules")]
        for fn in filenames:
            if fn.endswith(".html") and not fn.endswith(".bak"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def url_for(fp):
    rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Collector(HTMLParser):
    """Collects ids, hrefs, images, labels and checks tag nesting."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.hrefs = []
        self.imgs = []
        self.stack = []
        self.nesting_errors = []
        self.labels = []          # (for)
        self.form_fields = []     # (id, has_name)
        self.buttons = 0
        self.h1 = 0
        self.headings = []
        self.scripts = []
        self._in_script = None
        self.title = None
        self._in_title = False
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if "id" in a:
            if a["id"] in self.ids:
                self.nesting_errors.append("duplicate id: %s" % a["id"])
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append((a["href"], a.get("aria-label"), a.get("target"), a.get("rel")))
        if tag == "img":
            self.imgs.append(a.get("alt"))
        if tag == "label" and "for" in a:
            self.labels.append(a["for"])
        if tag in ("input", "textarea", "select"):
            self.form_fields.append((a.get("id"), "name" in a, a.get("type", "text")))
        if tag == "button":
            self.buttons += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
            if tag == "h1":
                self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_script = []
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_script is not None:
            self.scripts.append("".join(self._in_script))
            self._in_script = None
        if tag in VOID:
            return
        if not self.stack:
            self.nesting_errors.append("stray </%s>" % tag)
            return
        if self.stack[-1] != tag:
            # tolerate optional-close elements we do not use; otherwise report
            self.nesting_errors.append(
                "mismatched </%s> (open: %s)" % (tag, self.stack[-1]))
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.stack.pop()
                if self.stack:
                    self.stack.pop()
            return
        self.stack.pop()

    def handle_data(self, data):
        if self._in_script is not None:
            self._in_script.append(data)
        if self._in_title:
            self.title = (self.title or "") + data


def resolve(href):
    """Map an internal path to the file that should serve it."""
    path = href.split("#")[0].split("?")[0]
    if not path:
        return None
    if path.endswith("/"):
        return os.path.join(ROOT, path.strip("/").replace("/", os.sep), "index.html")
    return os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))


def main():
    files = html_files()
    if not files:
        print("No HTML found."); sys.exit(1)

    all_pages = {}
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            src = f.read()
        c = Collector()
        c.feed(src)
        c.close()
        all_pages[url_for(fp)] = (fp, src, c)

    # --------------------------------------------------------------- structure
    for url, (fp, src, c) in sorted(all_pages.items()):
        if c.stack:
            fail(url, "unclosed tags: %s" % ", ".join(c.stack))
        for e in c.nesting_errors:
            fail(url, e)
        if c.h1 != 1:
            fail(url, "expected exactly one <h1>, found %d" % c.h1)
        if not c.title:
            fail(url, "missing <title>")
        elif len(c.title) > 65:
            warn(url, "title is %d chars (>65 may truncate in search): %s"
                 % (len(c.title), c.title))
        if c.lang != "en-GB":
            fail(url, 'html lang is %r, expected "en-GB"' % c.lang)

        # meta description
        m = re.search(r'<meta name="description" content="([^"]*)"', src)
        if not m:
            fail(url, "missing meta description")
        elif not (50 <= len(m.group(1)) <= 175):
            warn(url, "meta description is %d chars" % len(m.group(1)))

        # canonical (404 is exempt)
        if url != "/404.html":
            if '<link rel="canonical"' not in src:
                fail(url, "missing canonical")
            if 'property="og:title"' not in src:
                fail(url, "missing Open Graph title")
            if "noindex" in src:
                fail(url, "page carries noindex")
        if "#main" in src and "id=\"main\"" not in src:
            fail(url, "skip link target #main missing")

        # heading order — no level skipped
        prev = 0
        for h in c.headings:
            if prev and h > prev + 1:
                warn(url, "heading jumps from h%d to h%d" % (prev, h))
                break
            prev = h

    # ------------------------------------------------------------------- links
    for url, (fp, src, c) in sorted(all_pages.items()):
        for href, aria, target, rel in c.hrefs:
            if href.startswith(("mailto:", "tel:")):
                continue
            if href.startswith(("http://", "https://")):
                if target == "_blank" and (not rel or "noopener" not in rel):
                    fail(url, "external _blank link without rel=noopener: %s" % href)
                continue
            if href == "#" or href.strip() == "":
                fail(url, "dead link (href=%r)" % href)
                continue
            if href.startswith("#"):
                frag = href[1:]
                if frag not in c.ids:
                    fail(url, "anchor #%s not present on this page" % frag)
                continue
            if not href.startswith("/"):
                fail(url, "relative link (breaks on nested pages): %s" % href)
                continue
            target_file = resolve(href)
            if not target_file or not os.path.isfile(target_file):
                fail(url, "broken link: %s" % href)
                continue
            if "#" in href:
                frag = href.split("#", 1)[1]
                tgt_url = url_for(target_file)
                if tgt_url in all_pages and frag not in all_pages[tgt_url][2].ids:
                    fail(url, "cross-page anchor missing: %s" % href)

    # ------------------------------------------------------------------ assets
    for asset in ["assets/css/site.css", "assets/js/site.js", "favicon.svg",
                  "favicon.ico", "apple-touch-icon.png", "og-image.png",
                  "robots.txt", "sitemap.xml", "CNAME", ".nojekyll"]:
        if not os.path.exists(os.path.join(ROOT, asset)):
            fail("(repo)", "missing asset: %s" % asset)

    # ----------------------------------------------------------------- JSON-LD
    for url, (fp, src, c) in sorted(all_pages.items()):
        for blob in c.scripts:
            try:
                data = json.loads(blob)
            except Exception as e:
                fail(url, "invalid JSON-LD: %s" % e)
                continue
            if "@context" not in data or "@type" not in data:
                fail(url, "JSON-LD missing @context/@type")

    # ------------------------------------------------------------------- forms
    for url, (fp, src, c) in sorted(all_pages.items()):
        ids = {i for i, _n, _t in c.form_fields if i}
        for lf in c.labels:
            if lf not in ids:
                fail(url, "<label for=%r> has no matching field" % lf)
        for fid, has_name, ftype in c.form_fields:
            if ftype in ("submit", "button", "hidden"):
                continue
            if fid and fid not in c.labels:
                fail(url, "field #%s has no label" % fid)

    # -------------------------------------------------------------- alt & aria
    for url, (fp, src, c) in sorted(all_pages.items()):
        for alt in c.imgs:
            if alt is None:
                fail(url, "<img> without alt attribute")

    # ------------------------------------------------- honesty / claims guard
    #
    # These patterns are the specific failure modes this rebuild exists to fix.
    banned = [
        (r"Marcus Adeyemi|Northgate Property", "fake testimonial"),
        (r"acmefit|acme\s*fit", "fake demo lead data"),
        (r"\bISO\s*27001\b|\bSOC\s*2\b(?!.{0,40}not)", "unheld certification claim"),
        (r">\s*Sign in\s*<", "sign-in link with no client portal"),
        (r">\s*Careers\s*<", "careers link with no careers page"),
        (r"lorem ipsum", "placeholder text"),
        (r"trusted by \d+|\d+\+? (?:happy )?clients", "unverifiable client count"),
        (r"placehold\.co", "placeholder image service"),
        # Delivery vendors are our implementation detail, not the client's concern.
        (r"vapi|n8n|twilio|gohighlevel", "named delivery vendor"),
    ]
    # A certification named inside an explicit disclaimer is honest, not a claim.
    NEGATED = re.compile(r"do not (?:currently )?hold|does not hold|not certified|"
                         r"we do not claim|will not claim", re.I)

    for url, (fp, src, c) in sorted(all_pages.items()):
        for pat, why in banned:
            for m in re.finditer(pat, src, re.I):
                ctx = src[max(0, m.start() - 220):m.end() + 220]
                if "certification" in why and NEGATED.search(ctx):
                    continue
                fail(url, "%s - matched %r" % (why, m.group(0)[:60]))
                break

    # Numeric claims: any percentage or "N hours/x" outside a labelled context.
    claim_pat = re.compile(r"(?<![\w-])(\d{1,3}%|\d+×|\d+x more|\d+\s*hrs?\b|\d+\s*hours saved)",
                           re.I)
    for url, (fp, src, c) in sorted(all_pages.items()):
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        for m in claim_pat.finditer(text):
            ctx = text[max(0, m.start() - 90):m.end() + 90]
            if re.search(r"illustrative|example|width|height", ctx, re.I):
                continue
            fail(url, "possible unsupported metric %r in: …%s…"
                 % (m.group(0), " ".join(ctx.split())[:110]))

    # ----------------------------------------------------------------- sitemap
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    listed = set(re.findall(r"<loc>https://digitalautonomous\.co\.uk(/[^<]*)</loc>", sm))
    live = {u for u in all_pages if u != "/404.html"}
    for u in live - listed:
        fail("sitemap.xml", "page not listed: %s" % u)
    for u in listed - live:
        fail("sitemap.xml", "lists non-existent page: %s" % u)

    # ------------------------------------------------------------------ report
    print("Checked %d pages." % len(all_pages))
    if WARNS:
        print("\n%d warning(s):" % len(WARNS))
        for w in WARNS:
            print("  ~ %s" % w)
    if FAILS:
        print("\n%d FAILURE(S):" % len(FAILS))
        for f in FAILS:
            print("  x %s" % f)
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
