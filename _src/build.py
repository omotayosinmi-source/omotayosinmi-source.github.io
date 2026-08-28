# -*- coding: utf-8 -*-
"""
Static site generator for digitalautonomous.co.uk.

Run:  python _src/build.py
Emits plain HTML into the repo root. There is no runtime build step — GitHub
Pages serves exactly what this writes.

CLAIMS RULE
-----------
Nothing this generator emits may state a client result, a performance metric,
a certification, a named customer or a founder biography that has not been
verified. There are no clients yet, so there are no case studies and no
numbers. Illustrative material is labelled as illustrative, in the markup, at
the point the visitor sees it.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import (  # noqa: E402
    SITE, EMAIL, BRAND, DESCRIPTOR, TAGLINE, FOUNDER, LOCATION,
    FORM_ENDPOINT, SHEET_ENDPOINT, COMPANY_TYPES, OTHER_OPTION,
    DIAL_CODES, DIAL_DIVIDER,
    PHONE, LINKEDIN, LINKEDIN_FOUNDER, COMPANY_NAME, COMPANY_NUMBER,
    REGISTERED_OFFICE, LEGAL_UPDATED, ICONS, INTEGRATIONS, PROBLEMS,
    SERVICES, SERVICE_BY_SLUG, INDUSTRIES, INDUSTRY_BY_SLUG, PROCESS,
    SECURITY, AUDIT_STEPS, FAQ,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = []          # (url_path, <title>, priority, changefreq) for the sitemap


# ==========================================================================
# Primitives
# ==========================================================================
def icon(name, cls="", stroke="1.8", size=20):
    """Inline icon.

    Always emits width/height. An SVG with only a viewBox falls back to
    300x150, which silently blows out any flex row it sits in — CSS then has
    to remember to size every single one. Attributes give a sane default that
    a stylesheet can still override.
    """
    body = ICONS[name]
    c = ' class="%s"' % cls if cls else ""
    return ('<svg%s width="%d" height="%d" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (c, size, size, stroke, body))


ARROW = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
         'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')

CHEV = ('<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>')

LOGO_SVG = (
    '<svg viewBox="0 0 40 40" fill="none" aria-hidden="true">'
    '<polyline points="5,31 15,23 22,27 33,10" stroke="#00a6fb" stroke-width="2.6" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M33 10 L26.5 10.5 M33 10 L32 16.5" stroke="#66d2f9" stroke-width="2.6" '
    'stroke-linecap="round"/>'
    '<circle cx="5" cy="31" r="2.7" fill="#66d2f9"/>'
    '<circle cx="15" cy="23" r="2.7" fill="#fff"/>'
    '<circle cx="22" cy="27" r="2.7" fill="#66d2f9"/>'
    '<circle cx="33" cy="10" r="3.1" fill="#00a6fb"/></svg>'
)


def logo(sub=True, label="Digital Autonomous home"):
    tag = '<span>%s</span>' % TAGLINE if sub else ''
    return ('<a href="/" class="logo" aria-label="%s">'
            '<span class="logo-mark">%s</span>'
            '<span class="logo-text">%s%s</span></a>'
            % (label, LOGO_SVG, BRAND, tag))


def btn(href, text, kind="primary", track=None, loc=None, arrow=False, extra=""):
    attrs = ''
    if track:
        attrs += ' data-track="%s"' % track
        if loc:
            attrs += ' data-track-location="%s"' % loc
    return '<a href="%s" class="btn btn-%s"%s%s>%s%s</a>' % (
        href, kind, attrs, (" " + extra if extra else ""), text, ARROW if arrow else "")


def audit_href(home=False):
    """Where a "Book a free audit" button goes.

    On the homepage the audit form is on the page, so scroll to it. Everywhere
    else the contact page *is* that form, which beats bouncing the reader back
    to the homepage mid-read. Both destinations land on a form.
    """
    return "#audit" if home else "/contact/"


def anchor(frag, home=False):
    return ("#" + frag) if home else ("/#" + frag)


# ==========================================================================
# Document chrome
# ==========================================================================
def head(title, desc, path, jsonld=None, og_type="website"):
    """`path` is the canonical path, e.g. '/ai-receptionist/'."""
    url = SITE + path
    ld = ""
    if jsonld:
        ld = "\n".join(
            '<script type="application/ld+json">\n%s\n</script>' % b for b in jsonld)
    return """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#05101f">
<meta name="format-detection" content="telephone=no">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="%(brand)s">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(site)s/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Digital Autonomous — AI automation solutions.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(site)s/og-image.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Lato:wght@400;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Lato:wght@400;700&display=swap">
<script>document.documentElement.className+=" js"</script>
<link rel="stylesheet" href="/assets/css/site.css">
%(ld)s
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""" % dict(title=title, desc=desc, url=url, brand=BRAND, site=SITE,
           og_type=og_type, ld=ld)


def nav_panel(items):
    rows = "".join(
        '<a href="%s">%s<small>%s</small></a>' % (h, t, s) for h, t, s in items)
    return '<div class="nav-panel">%s</div>' % rows


SOLUTION_LINKS = [("/%s/" % s["slug"], s["nav"], s["nav_sub"]) for s in SERVICES]
INDUSTRY_LINKS = ([("/industries/%s/" % i["slug"], i["nav"],
                    i["blurb"].split(".")[0].replace("&amp;", "&") + ".")
                   for i in INDUSTRIES]
                  + [("/industries/", "All industries", "Every sector we work with")])
COMPANY_LINKS = [
    ("/about/", "About us", "Who is behind Digital Autonomous"),
    ("/case-studies/", "Case studies", "How we document real results"),
    ("/contact/", "Contact", "Talk to us about your business"),
]


def header(home=False):
    mob = []
    mob.append('<div class="mm-group">Solutions</div>')
    for h, t, _ in SOLUTION_LINKS:
        mob.append('<a class="mm-sub" href="%s">%s</a>' % (h, t))
    mob.append('<div class="mm-group">Industries</div>')
    for h, t, _ in INDUSTRY_LINKS:
        mob.append('<a class="mm-sub" href="%s">%s</a>' % (h, t))
    mob.append('<div class="mm-group">Company</div>')
    mob.append('<a class="mm-sub" href="%s">How it works</a>' % anchor("how-it-works", home))
    for h, t, _ in COMPANY_LINKS:
        mob.append('<a class="mm-sub" href="%s">%s</a>' % (h, t))
    mob.append(btn(audit_href(home), "Book a free automation audit",
                   track="book_audit_click", loc="mobile_nav"))

    return """<header id="hdr">
  <div class="wrap nav">
    %(logo)s
    <nav class="nav-links" aria-label="Primary">
      <div class="nav-item">
        <button type="button" aria-expanded="false">Solutions %(chev)s</button>
        %(sol)s
      </div>
      <div class="nav-item">
        <button type="button" aria-expanded="false">Industries %(chev)s</button>
        %(ind)s
      </div>
      <a href="%(how)s">How it works</a>
      <div class="nav-item">
        <button type="button" aria-expanded="false">Company %(chev)s</button>
        %(com)s
      </div>
    </nav>
    <div class="nav-cta">
      %(cta)s
      <button class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">%(mob)s</div>
</header>
""" % dict(
        logo=logo(), chev=CHEV,
        sol=nav_panel(SOLUTION_LINKS), ind=nav_panel(INDUSTRY_LINKS),
        com=nav_panel(COMPANY_LINKS), how=anchor("how-it-works", home),
        cta=btn(audit_href(home),
                '<span class="cta-full">Book a free audit</span>'
                '<span class="cta-short">Book audit</span>',
                track="book_audit_click", loc="header"),
        mob="".join(mob))


def footer(home=False):
    detail = ['<a href="mailto:%s">%s</a>' % (EMAIL, EMAIL)]
    if PHONE:
        detail.append('<a href="tel:%s">%s</a>' % (re.sub(r"[^\d+]", "", PHONE), PHONE))
    if LOCATION:
        detail.append(LOCATION)
    # Registered company details are printed only once verified.
    reg = []
    if COMPANY_NAME:
        reg.append(COMPANY_NAME)
    if COMPANY_NUMBER:
        reg.append("Company no. %s" % COMPANY_NUMBER)
    if REGISTERED_OFFICE:
        reg.append(REGISTERED_OFFICE)

    social = ""
    if LINKEDIN:
        social += ('<a href="%s" aria-label="Digital Autonomous on LinkedIn" '
                   'rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true">'
                   '<path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zM8.3 18.3v-7H6v7zM7.15 10a1.3 1.3 0 1 0 0-2.6 1.3 1.3 0 0 0 0 2.6zM18 18.3v-3.9c0-2.1-1.1-3-2.6-3-1.2 0-1.75.66-2.05 1.13v-.97h-2.28v7h2.28v-3.9c0-.2.02-.4.08-.55.16-.4.53-.82 1.14-.82.8 0 1.13.62 1.13 1.5v3.77z"/>'
                   '</svg></a>' % LINKEDIN)
    social += ('<a href="mailto:%s" aria-label="Email Digital Autonomous">'
               '<svg viewBox="0 0 24 24" aria-hidden="true">'
               '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm8 7L4.5 6.5v.8L12 12l7.5-4.7v-.8z"/>'
               '</svg></a>' % EMAIL)

    sol_col = "".join('<a href="/%s/">%s</a>' % (s["slug"], s["nav"]) for s in SERVICES[:5])
    sol_col2 = "".join('<a href="/%s/">%s</a>' % (s["slug"], s["nav"]) for s in SERVICES[5:])
    ind_col = "".join('<a href="/industries/%s/">%s</a>' % (i["slug"], i["nav"]) for i in INDUSTRIES)

    return """<footer>
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        %(logo)s
        <p>We build the systems that answer enquiries, recover missed calls, book appointments and take repetitive admin off your team.</p>
        <span class="foot-tag">%(tagline)s</span>
        <div class="foot-detail">%(detail)s%(reg)s</div>
      </div>
      <div class="foot-col">
        <h2>Solutions</h2>
        %(sol)s
      </div>
      <div class="foot-col">
        <h2>More</h2>
        %(sol2)s
        <a href="%(how)s">How it works</a>
      </div>
      <div class="foot-col">
        <h2>Industries</h2>
        %(ind)s
        <a href="/industries/">All industries</a>
      </div>
      <div class="foot-col">
        <h2>Company</h2>
        <a href="/about/">About</a>
        <a href="/case-studies/">Case studies</a>
        <a href="/contact/">Contact</a>
        <a href="%(audit)s">Free automation audit</a>
      </div>
    </div>
    <div class="foot-bot">
      <p>&copy; 2026 %(brand)s. %(descriptor)s.</p>
      <div class="foot-legal">
        <a href="/privacy/">Privacy Policy</a>
        <a href="/cookies/">Cookie Policy</a>
        <a href="/terms/">Terms &amp; Conditions</a>
      </div>
      <div class="foot-social">%(social)s</div>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
""" % dict(
        logo=logo(sub=False), tagline=TAGLINE,
        detail="<br>".join(detail),
        reg=("<br><br>" + "<br>".join(reg)) if reg else "",
        sol=sol_col, sol2=sol_col2, ind=ind_col,
        how=anchor("how-it-works", home), audit=audit_href(home),
        brand=BRAND, descriptor=DESCRIPTOR, social=social)


def crumbs(trail):
    """trail: list of (href|None, label). Last item is the current page."""
    out = []
    for i, (href, label) in enumerate(trail):
        if i:
            out.append('<span class="sep" aria-hidden="true">/</span>')
        if href:
            out.append('<a href="%s">%s</a>' % (href, label))
        else:
            out.append('<span aria-current="page">%s</span>' % label)
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % "".join(out)


def breadcrumb_ld(trail_urls):
    items = []
    for i, (url, name) in enumerate(trail_urls, 1):
        items.append('    {"@type":"ListItem","position":%d,"name":"%s","item":"%s%s"}'
                     % (i, name.replace('"', ''), SITE, url))
    return ('{\n  "@context":"https://schema.org",\n  "@type":"BreadcrumbList",\n'
            '  "itemListElement":[\n%s\n  ]\n}' % ",\n".join(items))


# ==========================================================================
# Shared sections
# ==========================================================================
def _relative_luminance(hex_colour):
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def lin(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _readable_on(hex_colour):
    """Pick whichever of ink-navy or white clears 4.5:1 on this tile colour."""
    bg = _relative_luminance(hex_colour)
    navy, white = _relative_luminance("#05101f"), 1.0
    against = lambda fg: ((max(fg, bg) + 0.05) / (min(fg, bg) + 0.05))
    return "#05101f" if against(navy) >= against(white) else "#ffffff"


def integrations_section():
    tiles = "".join(
        '<div class="integ"><span class="mark" style="background:%s;color:%s" '
        'aria-hidden="true">%s</span><span class="nm">%s</span></div>'
        % (bg, _readable_on(bg), mark, name)
        for name, mark, bg in INTEGRATIONS)
    return """<section class="band integ-strip" id="integrations" aria-labelledby="integ-h">
  <div class="wrap">
    <p class="integ-lede" id="integ-h">Your systems. Finally working together.</p>
    <div class="integ-grid reveal">%s</div>
    <p style="text-align:center;color:var(--muted);font-size:.9rem;margin-top:1.6rem;max-width:64ch;margin-left:auto;margin-right:auto">
      We build around the tools you already pay for rather than asking you to replace them.
      Not on the list? If it has an API or a webhook, we can almost certainly connect it.
    </p>
  </div>
</section>
""" % tiles


def process_section(home=False):
    steps = "".join(
        '<div class="pstep reveal"><div class="idx">STEP %02d</div><div class="bar"></div>'
        '<h3>%s</h3><p>%s</p></div>' % (n, t, d)
        for n, (t, d) in enumerate(PROCESS, 1))
    return """<section class="block band" id="how-it-works" aria-labelledby="how-h">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">How it works</span>
      <h2 id="how-h">Audit, design, build, deploy, optimise.</h2>
      <p>A clear path with a decision point before anything gets built. You see what is worth automating — and what is not — before you commit.</p>
    </div>
    <div class="steps">%s</div>
  </div>
</section>
""" % steps


def security_section():
    cards = "".join(
        '<div class="sec reveal"><div class="sico">%s</div><h3>%s</h3><p>%s</p></div>'
        % (icon(ic), t, d) for ic, t, d in SECURITY)
    return """<section class="block" id="security" aria-labelledby="sec-h">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Security &amp; reliability</span>
      <h2 id="sec-h">Built for real businesses, not just demos.</h2>
      <p>A demo only has to work once. A system that answers your customers has to work at 2am on a bank holiday, and fail safely when it cannot.</p>
    </div>
    <div class="sec-grid">%s</div>
    <p class="sec-note reveal"><strong>On certifications:</strong> we build to these practices as standard.
      We do not currently hold ISO 27001, Cyber Essentials or SOC 2 certification, and we will not claim
      otherwise. If your procurement process requires a specific certification, tell us early and we will
      be straight with you about what we can and cannot meet.</p>
  </div>
</section>
"""  % cards


def ownership_section():
    items = [
        ("Your accounts, in your name",
         "The CRM, the phone number, the calendar and the customer data are yours. "
         "We work inside your accounts, not a wrapper you cannot see into."),
        ("Export whenever you want",
         "Your data is exportable at any time, in a usable format. Nothing is held back "
         "to make leaving difficult."),
        ("No lock-in contract",
         "The monthly management fee buys monitoring, support and improvement. "
         "If it stops being worth it, you stop paying it."),
        ("Documented, not mysterious",
         "You get documentation of what was built and how it works, so the system is "
         "not a black box only we understand."),
    ]
    lis = "".join('<li>%s<span><b>%s</b> — %s</span></li>' % (icon("check", stroke="2.4"), t, d)
                  for t, d in items)
    return """<section class="block tight">
  <div class="wrap">
    <div class="own reveal">
      <div>
        <span class="eyebrow">Ownership</span>
        <h2>No lock-in. Your data stays yours.</h2>
        <p>We build the automation infrastructure and then manage, monitor, maintain and
           improve it as an ongoing service — a setup fee for the build, a monthly fee for
           keeping it working. What we do not do is hold your business hostage to keep you
           paying it.</p>
      </div>
      <ul class="own-list">%s</ul>
    </div>
  </div>
</section>
""" % lis


def audit_section(home=False):
    items = "".join(
        '<li class="audit-item reveal"><span class="n">%02d</span><p>%s</p></li>' % (n, t)
        for n, t in enumerate(AUDIT_STEPS, 1))

    return """<section class="block" id="audit" aria-labelledby="audit-h">
  <div class="wrap">
    <div class="audit reveal">
      <div class="audit-in audit-cols">
        <div class="audit-copy">
          <span class="eyebrow">Start here</span>
          <h2 id="audit-h">Free Automation Audit</h2>
          <p class="sub">Thirty minutes on your business, not a sales pitch. We look at how enquiries
            reach you, what happens to them, and where your team's time actually goes.</p>
          <ul class="audit-list">%(items)s</ul>
          <p class="audit-out">%(map)s <span>Leave with a clear automation roadmap for your business —
            yours to keep, whether you work with us or not.</span></p>
          <div class="audit-meta">
            <div>%(clock)s 30 minutes</div>
            <div>%(check)s No cost, no obligation</div>
            <div>%(doc)s Written roadmap afterwards</div>
          </div>
        </div>

        <div class="audit-form">
          <h3>Book your free audit</h3>
          <p class="audit-form-lede">A few details and we will get back to you to find a time.</p>
          <form id="auditForm" data-endpoint="%(endpoint)s" data-sheet="%(sheet)s" novalidate>
            <div class="field">
              <label for="aName">Your name <span aria-hidden="true">*</span></label>
              <input type="text" id="aName" name="name" autocomplete="name" required
                     aria-describedby="aNameErr" placeholder="Jane Bennett">
              <div class="field-error" id="aNameErr">Please tell us your name.</div>
            </div>
            <div class="field">
              <label for="aEmail">Email <span aria-hidden="true">*</span></label>
              <input type="email" id="aEmail" name="email" autocomplete="email" required
                     aria-describedby="aEmailErr" placeholder="jane@yourcompany.co.uk">
              <div class="field-error" id="aEmailErr">Please enter a valid email address.</div>
            </div>
            <div class="field">
              <label for="aPhone">Telephone number <span aria-hidden="true">*</span></label>
              <div class="phone-row">%(adial)s
                <input type="tel" id="aPhone" name="phone" autocomplete="tel" required
                       aria-describedby="aPhoneHint aPhoneErr" placeholder="07700 900000">
              </div>
              <p class="hint" id="aPhoneHint">With or without the leading 0 — either works.</p>
              <div class="field-error" id="aPhoneErr">Please enter a telephone number we can reach you on.</div>
            </div>
            <div class="field">
              <label for="aType">What type of company is this? <span aria-hidden="true">*</span></label>
              %(atype)s
              <div class="field-error" id="aTypeErr">Please pick the closest match.</div>
            </div>
            %(aother)s
            <button type="submit" class="btn btn-primary" style="width:100%%"
                    data-track="book_audit_submit" data-track-location="audit_section">
              Book My Free Automation Audit</button>
            <div class="form-status" id="auditStatus" role="status" aria-live="polite"></div>
            <p class="form-note">We use these details to arrange your audit and for nothing else.
              No newsletter, no list, no passing them on. Prefer email? %(mail)s</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>
""" % dict(items=items, map=icon("map"), clock=icon("clock"),
           check=icon("check", stroke="2.4"), doc=icon("doc"),
           adial=dial_select("aCode"), atype=company_type_select("aType", "aOther"), aother=company_type_other("aOther"),
           endpoint=FORM_ENDPOINT, sheet=SHEET_ENDPOINT,
           mail='<a href="mailto:%s" style="color:var(--cyan)">%s</a>' % (EMAIL, EMAIL))


def faq_section(items, title="Frequently asked questions", eyebrow="FAQ", lede=None, hid="faq"):
    rows = "".join(
        '<details><summary>%s%s</summary><div class="answer">%s</div></details>'
        % (q, CHEV, a) for q, a in items)
    lede_html = '<p>%s</p>' % lede if lede else ''
    return """<section class="block band" id="%(hid)s" aria-labelledby="%(hid)s-h">
  <div class="wrap">
    <div class="head center reveal">
      <span class="eyebrow center">%(eyebrow)s</span>
      <h2 id="%(hid)s-h">%(title)s</h2>
      %(lede)s
    </div>
    <div class="faq reveal">%(rows)s</div>
  </div>
</section>
""" % dict(hid=hid, eyebrow=eyebrow, title=title, lede=lede_html, rows=rows)


def faq_ld(items):
    qs = []
    for q, a in items:
        clean = re.sub(r"<[^>]+>", "", a).replace('"', "'")
        qs.append('    {"@type":"Question","name":"%s",'
                  '"acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                  % (q.replace('"', "'"), clean))
    return ('{\n  "@context":"https://schema.org",\n  "@type":"FAQPage",\n'
            '  "mainEntity":[\n%s\n  ]\n}' % ",\n".join(qs))


def cta_band(title, body, home=False, primary="Book a free automation audit"):
    return """<section class="block">
  <div class="wrap">
    <div class="cta reveal">
      <div class="cta-in">
        <span class="eyebrow center">Next step</span>
        <h2>%(title)s</h2>
        <p>%(body)s</p>
        <div class="btn-row center">
          %(a)s
          %(b)s
        </div>
      </div>
    </div>
  </div>
</section>
""" % dict(title=title, body=body,
           a=btn("/contact/", primary, track="book_audit_click", loc="cta_band", arrow=True),
           b=btn("mailto:%s" % EMAIL, "Email %s" % EMAIL, kind="ghost",
                 track="email_click", loc="cta_band"))


def related_section(slugs, heading="Related automations"):
    cards = []
    for s in slugs:
        svc = SERVICE_BY_SLUG[s]
        cards.append('<a class="rel" href="/%s/"><div class="k">%s</div>'
                     '<div class="d">%s</div></a>' % (svc["slug"], svc["title"], svc["nav_sub"]))
    return """<section class="block tight">
  <div class="wrap">
    <div class="head reveal" style="margin-bottom:1.8rem">
      <h2 style="font-size:clamp(1.4rem,2.8vw,1.8rem);margin-top:0">%s</h2>
    </div>
    <div class="rel-grid reveal">%s</div>
  </div>
</section>
""" % (heading, "".join(cards))


# ==========================================================================
# Homepage
# ==========================================================================
HERO_FLOW = [
    ("mail", "New Enquiry", "Web form, call or message arrives"),
    ("check", "Instant Response", "Acknowledged in seconds, any hour"),
    ("target", "Qualification", "Matched against your criteria"),
    ("database", "CRM", "Contact created, pipeline updated"),
    ("calendar", "Appointment Booked", "Real slot held and confirmed"),
    ("send", "Follow-Up", "Reminder and next steps queued"),
]

DEMO_STEPS = [
    ("Customer calls", "A prospective customer rings your main number."),
    ("Call missed", "Nobody is free. The system sees the unanswered call the moment it ends."),
    ("SMS sent", "A personalised text goes out from your number within seconds."),
    ("Customer replies", "They answer by text — the conversation is alive again."),
    ("AI qualifies the lead", "It asks your qualifying questions and works out what they need."),
    ("Appointment booked", "A real slot is offered from your live calendar and confirmed."),
    ("CRM updated", "Contact created, transcript attached, pipeline moved, follow-up scheduled."),
]


def home_hero():
    steps = "".join(
        '<div class="step" data-i="%d"><div class="node">%s</div>'
        '<div class="body"><div class="t">%s</div><div class="d">%s</div></div></div>'
        % (n, icon(ic, stroke="2"), t, d)
        for n, (ic, t, d) in enumerate(HERO_FLOW))

    return """<section class="hero">
  <div class="hero-bg" aria-hidden="true">
    <div class="hero-grid"></div>
    <div class="hero-glow"></div>
  </div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <span class="eyebrow">%(tagline)s</span>
      <h1>More Revenue.<br>Lower Costs.<br><em>Time Back.</em></h1>
      <p class="lead">Digital Autonomous builds intelligent systems that respond to enquiries,
        qualify prospects, book appointments and automate follow-up — so you win more of the
        business you already attract, and spend far less time doing it.</p>
      <div class="btn-row">
        %(a)s
        %(b)s
      </div>
      <p class="hero-note"><span class="dot"></span> No lock-in. Built around the tools you already use.</p>
    </div>

    <div class="panel reveal">
      <div class="panel-top">
        <span class="panel-title">%(pico)s Example Automation</span>
        <span class="tag-illustrative">Illustrative</span>
      </div>
      <div class="flow" role="img" aria-label="Example automation: a new enquiry is acknowledged instantly, qualified, written to the CRM, an appointment is booked and a follow-up is queued.">
        <div class="flow-line"><span class="flow-fill"></span></div>
        %(steps)s
      </div>
      <div class="panel-foot">
        <p class="f-note">An example of a lead-capture flow. Not live client data.</p>
        <span class="f-chip">Runs unattended</span>
      </div>
    </div>
  </div>
</section>
""" % dict(
        tagline=TAGLINE, steps=steps, pico=icon("route", stroke="2"),
        a=btn("#audit", "Book a Free Automation Audit", track="book_audit_click",
              loc="hero", arrow=True),
        b=btn("#demo", "See How It Works", kind="ghost", track="see_how_click", loc="hero"))


def problem_section():
    cards = "".join(
        '<div class="prob reveal"><div class="pico">%s</div><h3>%s</h3><p>%s</p></div>'
        % (icon(ic), t, d) for ic, t, d in PROBLEMS)
    return """<section class="block" id="problem" aria-labelledby="prob-h">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">The problem</span>
      <h2 id="prob-h">Most businesses don't need more leads. They need to stop losing the ones they already have.</h2>
      <p>You have already paid for those enquiries — in advertising, in referrals, in years of reputation.
         Here is where they usually go.</p>
    </div>
    <div class="prob-grid">%s</div>
    <div class="prob-close reveal">%s
      <p><strong>None of this is a people problem.</strong> It is what happens when a small team is
        busy doing the actual work. Systems do not get busy.</p>
    </div>
  </div>
</section>
""" % (cards, icon("sparkle"))


def services_section():
    cards = []
    for s in SERVICES:
        cards.append(
            '<article class="card reveal">'
            '<div class="ico">%s</div>'
            '<h3><a href="/%s/">%s</a></h3>'
            '<p>%s</p>'
            '<div class="result">%s</div>'
            '<span class="link-arrow">Learn more %s</span>'
            '</article>' % (icon(s["icon"]), s["slug"], s["title"], s["blurb"],
                            s["result"], ARROW))
    return """<section class="block" id="solutions" aria-labelledby="sol-h">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Automation solutions</span>
      <h2 id="sol-h">Systems you can actually buy, not vague "AI transformation".</h2>
      <p>Each one solves a specific way businesses lose leads, time or revenue.
         Start with one. Add the rest when it has paid for itself.</p>
    </div>
    <div class="cards">%s</div>
  </div>
</section>
""" % "".join(cards)


def dial_select(field_id):
    """Country dialling code picker, common destinations pinned to the top."""
    top = "".join('<option value="%s">%s &nbsp;%s</option>' % (c, c, n)
                  for n, c in DIAL_CODES[:DIAL_DIVIDER])
    rest = "".join('<option value="%s">%s &nbsp;%s</option>' % (c, c, n)
                   for n, c in DIAL_CODES[DIAL_DIVIDER:])
    return ('<label class="sr-only" for="%s">Country dialling code</label>'
            '<select id="%s" name="dial_code" class="dial">'
            '<optgroup label="Common">%s</optgroup>'
            '<optgroup label="All countries">%s</optgroup>'
            '</select>' % (field_id, field_id, top, rest))


def company_type_select(field_id, other_id):
    opts = "".join('<option value="%s">%s</option>' % (t, t) for t in COMPANY_TYPES)
    return ('<select id="%s" name="company_type" required aria-describedby="%sErr" '
            'data-other="%s" data-other-value="%s">'
            '<option value="" selected disabled>Please choose…</option>%s</select>'
            % (field_id, field_id, other_id, OTHER_OPTION, opts))


def company_type_other(field_id):
    """Free-text box, revealed only when the picker lands on the catch-all."""
    return ('<div class="field field-other" id="%sWrap" hidden>'
            '<label for="%s">Tell us what kind <span aria-hidden="true">*</span></label>'
            '<input type="text" id="%s" name="company_type_other" '
            'aria-describedby="%sErr" placeholder="e.g. veterinary practice">'
            '<div class="field-error" id="%sErr">Please tell us what kind of company this is.</div>'
            '</div>' % (field_id, field_id, field_id, field_id, field_id))


def demo_section():
    steps = "".join(
        '<div class="dstep" tabindex="0" role="button" aria-label="Step %d: %s">'
        '<span class="dnum">%d</span>'
        '<div class="dbody"><h3>%s</h3><p>%s</p></div></div>'
        % (n, t, n, t, d) for n, (t, d) in enumerate(DEMO_STEPS, 1))

    return """<section class="block band" id="demo" aria-labelledby="demo-h">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">See automation in action</span>
      <h2 id="demo-h">See Automation in Action</h2>
      <p>This is missed-call recovery, start to finish. Step through it, or let it play.</p>
    </div>

    <div class="demo-stage reveal" id="demoStage">
      <div class="demo-head">
        <span class="demo-title">Missed call &rarr; booked appointment</span>
        <span class="tag-illustrative">Illustrative example</span>
      </div>
      <div class="demo-track">%(steps)s</div>
      <div class="demo-controls">
        <button type="button" class="btn-sm" id="demoPlay" aria-pressed="false">
          <svg class="icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
          <svg class="icon-pause" viewBox="0 0 24 24" aria-hidden="true" style="display:none"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>
          <span class="label">Play</span>
        </button>
        <button type="button" class="btn-sm" id="demoReset">Reset</button>
        <div class="demo-progress" role="presentation"><i id="demoProgress"></i></div>
      </div>
    </div>

    <p class="demo-foot reveal">This is one of several systems we build.
      %(cta)s</p>
  </div>
</section>
""" % dict(steps=steps,
           cta='<a class="link-arrow" href="#solutions">See the full range %s</a>' % ARROW)


def case_studies_section():
    slots = [
        ("Client / Industry", "Who they are and what sector they operate in."),
        ("Problem", "What was being lost, and roughly what it was costing."),
        ("Automation built", "Exactly which systems were built and connected."),
        ("Result", "The measured change, with the measurement method stated."),
        ("Client quote", "In the client's own words, with their permission."),
    ]
    cells = "".join('<div class="cs-slot"><div class="k">%s</div><div class="v">%s</div></div>'
                    % (k, v) for k, v in slots)
    return """<section class="block" id="results" aria-labelledby="res-h">
  <div class="wrap">
    <div class="head center reveal">
      <span class="eyebrow center">Results</span>
      <h2 id="res-h">We would rather show you nothing than show you something invented.</h2>
      <p>Plenty of agencies fill this space with stock photography, round percentages and
         testimonials from people who do not exist. We publish results to a fixed standard
         instead — real numbers, from named clients, with their permission.</p>
    </div>
    <div class="cs-empty reveal">
      <h3>The reporting standard</h3>
      <p>Every result we publish states where the number came from and over what period,
         so you can judge it for yourself rather than take our word for it.</p>
      <div class="cs-template">%(cells)s</div>
      <div class="btn-row center">
        %(a)s
        %(b)s
      </div>
    </div>
  </div>
</section>
""" % dict(cells=cells,
           a=btn("/case-studies/", "How we report results", kind="ghost"),
           b=btn("#audit", "Book a free automation audit", track="book_audit_click",
                 loc="case_studies", arrow=True))


def industries_section():
    cards = []
    for i, ind in enumerate(INDUSTRIES):
        chips = "".join('<span class="chip">%s</span>' % c for c in ind["chips"][:4])
        feature = " feature" if i == 0 else ""
        cards.append(
            '<article class="ind reveal%s"><div class="itop"><span class="iico">%s</span>'
            '<h3><a href="/industries/%s/">%s</a></h3></div>'
            '<p>%s</p><div class="chips">%s</div>'
            '<span class="link-arrow">See how it works here %s</span></article>'
            % (feature, icon(ind["icon"]), ind["slug"], ind["title"],
               ind["blurb"], chips, ARROW))
    return """<section class="block" id="industries" aria-labelledby="ind-h">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Industries</span>
      <h2 id="ind-h">Where we have gone deepest so far.</h2>
      <p>We know these sectors' enquiry patterns well enough to be specific about what to fix first.</p>
    </div>
    <div class="ind-grid">%s</div>
    <p class="ind-foot reveal">If your business generates enquiries, <span>there's probably something we can automate.</span></p>
  </div>
</section>
""" % "".join(cards)


def about_section():
    points = [
        ("search", "We start with where the money leaks",
         "Not with a technology. The audit finds the specific places your business loses "
         "enquiries, time and revenue, and we build around those."),
        ("plug", "We work with what you have",
         "Your CRM, your calendar, your phone number, your inbox. Ripping out working "
         "software to sell you a platform is somebody else's business model."),
        ("scale", "We would rather turn work down",
         "If automating something will not pay for itself, we say so during the audit. "
         "A system nobody needed is worse than no system."),
    ]
    pts = "".join(
        '<div class="about-point"><span class="wm">%s</span><div><h3>%s</h3><p>%s</p></div></div>'
        % (icon(ic), t, d) for ic, t, d in points)

    li_html = ""
    if LINKEDIN_FOUNDER:
        li_html = ('<div class="founder-links">'
                   '<a class="btn btn-ghost" href="%s" rel="noopener" target="_blank">Connect on LinkedIn</a>'
                   '</div>' % LINKEDIN_FOUNDER)
    else:
        li_html = ('<div class="placeholder-note">Reserved for the founder’s photograph, '
                   'professional background, LinkedIn profile and a statement in their own '
                   'words. Deliberately empty: nothing on this page is invented, so it stays '
                   'sparse until the real details are supplied.</div>')

    return """<section class="block" id="about" aria-labelledby="about-h">
  <div class="wrap">
    <div class="about-grid">
      <div class="reveal">
        <span class="eyebrow">About us</span>
        <h2 id="about-h" style="font-family:'Montserrat';font-weight:700;font-size:clamp(1.85rem,4vw,2.7rem);color:var(--white);letter-spacing:-.02em;line-height:1.14;margin:1.2rem 0 1rem">About Digital Autonomous</h2>
        <p style="color:var(--muted);font-size:1.05rem">Digital Autonomous is an automation studio working with businesses across the UK and internationally.
          We find where a business is losing leads, time and revenue, and then build automation around
          those specific problems — rather than selling a general-purpose "AI solution" and hoping it lands.</p>
        <div class="about-points">%(pts)s</div>
      </div>

      <div class="founder reveal">
        <div class="founder-top">
          <span class="founder-photo">%(avatar)s</span>
          <div>
            <h3>%(founder)s</h3>
            <div class="role">Founder</div>
          </div>
        </div>
        <div class="founder-body">
          <p>Digital Autonomous was set up around a specific, unglamorous observation:
            businesses spend heavily to generate enquiries and then lose a share of them to
            a ringing phone and a follow-up nobody sent.</p>
          <p>That gap is fixable with systems that already work — a voice agent that
            answers, a text that goes out in seconds, a CRM that updates itself — and most
            of the businesses losing money to it have no interest in becoming automation
            experts. They want it handled.</p>
        </div>
        %(li)s
      </div>
    </div>
  </div>
</section>
""" % dict(pts=pts, founder=FOUNDER, li=li_html,
           avatar=icon("users", stroke="1.5"))


def build_home():
    ld = [
        """{
  "@context":"https://schema.org",
  "@type":"ProfessionalService",
  "@id":"%(site)s/#organisation",
  "name":"%(brand)s",
  "url":"%(site)s/",
  "email":"%(email)s",
  "logo":"%(site)s/og-image.png",
  "image":"%(site)s/og-image.png",
  "description":"%(brand)s builds AI automation systems that answer enquiries, recover missed calls, qualify leads, book appointments and remove repetitive admin.",
  "slogan":"More revenue, lower costs, time back.",
  "areaServed":"Worldwide",
  "knowsAbout":["AI receptionist","Missed call recovery","Lead follow-up automation","Lead reactivation","CRM automation","Appointment automation","Business process automation"],
  "founder":{"@type":"Person","name":"%(founder)s"}
}""" % dict(site=SITE, brand=BRAND, email=EMAIL, founder=FOUNDER),
        """{
  "@context":"https://schema.org",
  "@type":"WebSite",
  "url":"%s/",
  "name":"%s",
  "inLanguage":"en-GB"
}""" % (SITE, BRAND),
        faq_ld(FAQ),
    ]

    html = (
        head("Grow Revenue, Cut Costs, Save Time | Digital Autonomous",
             "AI systems that win more business, cut operating costs and give your team "
             "hours back — answering enquiries, qualifying leads, booking appointments "
             "and automating follow-up.",
             "/", jsonld=ld)
        + header(home=True)
        + '<main id="main">'
        + home_hero()
        + integrations_section()
        + problem_section()
        + services_section()
        + demo_section()
        + case_studies_section()
        + industries_section()
        + process_section(home=True)
        + security_section()
        + ownership_section()
        + about_section()
        + faq_section(FAQ)
        + audit_section(home=True)
        + '</main>'
        + footer(home=True)
    )
    write("/", html, "Homepage", 1.0, "monthly")


# ==========================================================================
# Service pages
# ==========================================================================
def build_service(s):
    path = "/%s/" % s["slug"]
    build = "".join(
        '<div class="card reveal"><h3>%s</h3><p>%s</p></div>' % (t, d)
        for t, d in s["build"])
    outcomes = "".join('<li>%s%s</li>' % (icon("check", stroke="2.4"), o) for o in s["outcomes"])

    ld = [
        """{
  "@context":"https://schema.org",
  "@type":"Service",
  "name":"%(name)s",
  "serviceType":"%(name)s",
  "url":"%(site)s%(path)s",
  "description":"%(desc)s",
  "provider":{"@type":"ProfessionalService","name":"%(brand)s","url":"%(site)s/"},
  "areaServed":"Worldwide"
}""" % dict(name=s["title"], site=SITE, path=path, brand=BRAND,
            desc=s["meta_desc"].replace('"', "'")),
        breadcrumb_ld([("/", "Home"), (path, s["title"])]),
    ]

    body = """<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="hero-glow"></div></div>
  <div class="wrap" style="position:relative;z-index:1">
    %(crumbs)s
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="btn-row">%(a)s%(b)s</div>
  </div>
</section>

<section class="block band">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">%(ph)s</span>
      <h2>%(pt)s</h2>
    </div>
    <div class="prob-close reveal" style="margin-top:0">%(sparkle)s<p>%(problem)s</p></div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">What we build</span>
      <h2>What is actually included.</h2>
      <p>Every build is scoped to your business, but this is the shape of it.</p>
    </div>
    <div class="cards">%(build)s</div>
  </div>
</section>

<section class="block tight">
  <div class="wrap">
    <div class="own reveal">
      <div>
        <span class="eyebrow">Business outcome</span>
        <h2>What changes for you.</h2>
        <p>Written as outcomes rather than percentages, because we will not publish a number
           we cannot evidence. When we have measured results from clients, they will appear on
           the <a href="/case-studies/" style="color:var(--cyan)">case studies</a> page with the
           method stated.</p>
      </div>
      <ul class="own-list">%(outcomes)s</ul>
    </div>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), (None, s["title"])]),
           h1=s["h1"], lead=s["lead"], ph=s["problem_h"], pt=s["title"],
           problem=s["problem"], build=build, outcomes=outcomes,
           sparkle=icon("alert"),
           a=btn("/contact/", "Book a Free Automation Audit", track="book_audit_click",
                 loc="service_hero", arrow=True),
           b=btn("/#demo", "See how it works", kind="ghost"))

    html = (head(s["meta_title"], s["meta_desc"], path, jsonld=ld)
            + header()
            + '<main id="main">'
            + body
            + related_section(s["related"])
            + process_section()
            + cta_band("Find out whether this is the right first automation.",
                       "The free audit tells you where you are actually losing enquiries — "
                       "which may or may not be here. You get the roadmap either way.")
            + '</main>'
            + footer())
    write(path, html, s["title"], 0.8, "monthly")


# ==========================================================================
# Industry pages
# ==========================================================================
def build_industry(ind):
    path = "/industries/%s/" % ind["slug"]
    pains = "".join(
        '<div class="prob reveal"><div class="pico">%s</div><h3>%s</h3><p>%s</p></div>'
        % (icon("alert"), t, d) for t, d in ind["pains"])
    stack = "".join(
        '<a class="rel" href="/%s/"><div class="k">%s</div><div class="d">%s</div></a>'
        % (sl, SERVICE_BY_SLUG[sl]["title"], SERVICE_BY_SLUG[sl]["nav_sub"])
        for sl in ind["stack"])

    ld = [
        """{
  "@context":"https://schema.org",
  "@type":"Service",
  "name":"Automation for %(name)s",
  "url":"%(site)s%(path)s",
  "description":"%(desc)s",
  "provider":{"@type":"ProfessionalService","name":"%(brand)s","url":"%(site)s/"},
  "areaServed":"Worldwide",
  "audience":{"@type":"BusinessAudience","name":"%(name)s"}
}""" % dict(name=re.sub(r"&amp;", "and", ind["title"]), site=SITE, path=path,
            brand=BRAND, desc=ind["meta_desc"].replace('"', "'")),
        breadcrumb_ld([("/", "Home"), ("/industries/", "Industries"),
                       (path, re.sub(r"&amp;", "and", ind["title"]))]),
    ]

    body = """<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="hero-glow"></div></div>
  <div class="wrap" style="position:relative;z-index:1">
    %(crumbs)s
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="btn-row">%(a)s%(b)s</div>
  </div>
</section>

<section class="block band">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Where the leads go</span>
      <h2>The four leaks we see most often.</h2>
    </div>
    <div class="prob-grid">%(pains)s</div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">What we would build</span>
      <h2>The stack that usually fixes it.</h2>
      <p>Not all at once. The audit decides the order, and it starts with whichever one is
         costing you the most right now.</p>
    </div>
    <div class="rel-grid reveal">%(stack)s</div>
    <p class="ind-foot reveal" style="margin-top:2.4rem">Not in this sector?
      <span>If your business generates enquiries, there's probably something we can automate.</span></p>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), ("/industries/", "Industries"),
                          (None, ind["title"])]),
           h1=ind["h1"], lead=ind["lead"], pains=pains, stack=stack,
           a=btn("/contact/", "Book a Free Automation Audit", track="book_audit_click",
                 loc="industry_hero", arrow=True),
           b=btn("/industries/", "All industries", kind="ghost"))

    html = (head(ind["meta_title"], ind["meta_desc"], path, jsonld=ld)
            + header()
            + '<main id="main">'
            + body
            + process_section()
            + cta_band("See where your practice is losing enquiries.",
                       "Thirty minutes, no cost, and a written roadmap at the end of it.")
            + '</main>'
            + footer())
    write(path, html, re.sub(r"&amp;", "and", ind["title"]), 0.7, "monthly")


def build_industries_hub():
    path = "/industries/"
    cards = []
    for ind in INDUSTRIES:
        chips = "".join('<span class="chip">%s</span>' % c for c in ind["chips"])
        cards.append(
            '<article class="ind reveal"><div class="itop"><span class="iico">%s</span>'
            '<h2><a href="/industries/%s/">%s</a></h2></div><p>%s</p>'
            '<div class="chips">%s</div>'
            '<span class="link-arrow">See how it works here %s</span></article>'
            % (icon(ind["icon"]), ind["slug"], ind["title"], ind["blurb"], chips, ARROW))

    body = """<section class="page-hero wide">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="hero-glow"></div></div>
  <div class="wrap" style="position:relative;z-index:1">
    %(crumbs)s
    <h1>Industries we know well enough to be specific about.</h1>
    <p class="lead">Every business loses enquiries in slightly different places. These are the
      sectors whose patterns we know best — but the list is where we have gone deepest, not a
      limit on who we work with.</p>
    <div class="btn-row">%(a)s</div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="ind-grid">%(cards)s</div>
    <p class="ind-foot reveal">If your business generates enquiries,
      <span>there's probably something we can automate.</span></p>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), (None, "Industries")]),
           cards="".join(cards),
           a=btn("/contact/", "Book a Free Automation Audit", track="book_audit_click",
                 loc="industries_hub", arrow=True))

    html = (head("Industries We Automate For | Digital Autonomous",
                 "Automation for private dental clinics, healthcare and aesthetics, home "
                 "services and professional services — and any business that generates enquiries.",
                 path, jsonld=[breadcrumb_ld([("/", "Home"), (path, "Industries")])])
            + header()
            + '<main id="main">' + body
            + cta_band("Find the leaks in your business.",
                       "The free automation audit is sector-agnostic. It looks at how enquiries "
                       "reach you and what happens next.")
            + '</main>' + footer())
    write(path, html, "Industries", 0.7, "monthly")


# ==========================================================================
# Company pages
# ==========================================================================
def build_about():
    path = "/about/"
    ld = [
        """{
  "@context":"https://schema.org",
  "@type":"AboutPage",
  "url":"%(site)s%(path)s",
  "name":"About Digital Autonomous",
  "mainEntity":{"@type":"ProfessionalService","name":"%(brand)s","url":"%(site)s/","founder":{"@type":"Person","name":"%(founder)s"}}
}""" % dict(site=SITE, path=path, brand=BRAND, founder=FOUNDER),
        breadcrumb_ld([("/", "Home"), (path, "About")]),
    ]

    body = """<section class="page-hero wide">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="hero-glow"></div></div>
  <div class="wrap" style="position:relative;z-index:1">
    %(crumbs)s
    <h1>Built by people who have to live with the results.</h1>
    <p class="lead">Digital Autonomous designs, builds and runs automation for businesses that
      cannot afford to lose an enquiry. We work inside our clients' own systems, on their own
      data, wherever in the world they operate — and we stay responsible for the automation long
      after it goes live.</p>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), (None, "About")]))

    html = (head("About Digital Autonomous | AI Automation Studio",
                 "Digital Autonomous is an automation studio that finds where businesses lose "
                 "leads, time and revenue, then builds automation around those specific problems.",
                 path, jsonld=ld)
            + header()
            + '<main id="main">' + body
            + about_section()
            + process_section()
            + security_section()
            + ownership_section()
            + cta_band("Talk to us about your business.",
                       "The free automation audit is the easiest way to find out whether any of "
                       "this is worth doing for you.")
            + '</main>' + footer())
    write(path, html, "About", 0.6, "yearly")


def build_case_studies():
    path = "/case-studies/"
    slots = [
        ("Client / Industry", "Who they are and what sector they operate in — named where they "
                              "are happy to be named, described generically where they are not."),
        ("Problem", "What was being lost before, and what it was costing. Stated as we found it, "
                    "not as a dramatic before-picture."),
        ("Automation built", "Exactly which systems were built, which platforms were connected, "
                             "and what the automation does and does not handle."),
        ("Result", "The measured change — what was measured, over what period, and how. "
                   "If a number cannot be attributed to the automation, we say so."),
        ("Client quote", "In the client's own words, reviewed and approved by them before "
                         "publication."),
    ]
    cells = "".join('<div class="cs-slot"><div class="k">%s</div><div class="v">%s</div></div>'
                    % (k, v) for k, v in slots)

    body = """<section class="page-hero wide">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="hero-glow"></div></div>
  <div class="wrap" style="position:relative;z-index:1">
    %(crumbs)s
    <h1>How we report results.</h1>
    <p class="lead">Most agency case studies are unfalsifiable: a round percentage, a stock
      headshot, no method. We hold ours to a fixed standard instead, so you can weigh a result
      rather than simply believe it. That standard is published here in advance.</p>
    <div class="btn-row">%(a)s</div>
  </div>
</section>

<section class="block band">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">The format</span>
      <h2>What every case study contains.</h2>
      <p>Five sections, every time, so results are comparable rather than cherry-picked.</p>
    </div>
    <div class="cs-template reveal">%(cells)s</div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Our standard</span>
      <h2>What we will not do.</h2>
    </div>
    <div class="cards">
      <div class="card reveal"><h3>No unattributable numbers</h3>
        <p>If revenue went up while three other things also changed, we will not claim the
          automation caused it. Where we can only show a directional result, we say that.</p></div>
      <div class="card reveal"><h3>No invented quotes</h3>
        <p>Every quote comes from a named person who has read and approved it. No composites,
          no "a client in the dental sector said".</p></div>
      <div class="card reveal"><h3>No stock faces</h3>
        <p>If we cannot show the client, we show nothing. A generated headshot next to a
          testimonial is a lie with extra steps.</p></div>
    </div>
    <div class="empty-state reveal" style="margin-top:2.5rem">
      <div class="eico">%(eico)s</div>
      <h2>Client confidentiality comes first</h2>
      <p>Much of this work sits inside systems our clients would rather not discuss in public.
        Results appear here only once the client has reviewed and approved them. If you would
        like to speak to a reference, ask us during the audit.</p>
      <div class="btn-row center">%(b)s</div>
    </div>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), (None, "Case studies")]), cells=cells,
           eico=icon("shield"),
           a=btn("/contact/", "Book a free automation audit", track="book_audit_click",
                 loc="case_studies_hero", arrow=True),
           b=btn("/contact/", "Book a free automation audit", track="book_audit_click",
                 loc="case_studies_empty", arrow=True))

    html = (head("Case Studies | Digital Autonomous",
                 "The standard every Digital Autonomous case study is held to — client, problem, "
                 "automation built, measured result and client quote. No invented figures.",
                 path, jsonld=[breadcrumb_ld([("/", "Home"), (path, "Case studies")])])
            + header() + '<main id="main">' + body + '</main>' + footer())
    write(path, html, "Case studies", 0.5, "monthly")


def build_contact():
    path = "/contact/"
    methods = ['<a class="cmethod" href="mailto:%s"><span class="cico">%s</span>'
               '<span><span class="k">Email</span><span class="v">%s</span></span></a>'
               % (EMAIL, icon("mail"), EMAIL)]
    if PHONE:
        methods.append('<a class="cmethod" href="tel:%s"><span class="cico">%s</span>'
                       '<span><span class="k">Telephone</span><span class="v">%s</span></span></a>'
                       % (re.sub(r"[^\d+]", "", PHONE), icon("phone"), PHONE))
    if LINKEDIN:
        methods.append('<a class="cmethod" href="%s" rel="noopener" target="_blank">'
                       '<span class="cico">%s</span><span><span class="k">LinkedIn</span>'
                       '<span class="v">Digital Autonomous</span></span></a>'
                       % (LINKEDIN, icon("users")))

    audit_items = "".join('<li>%s%s</li>' % (icon("check", stroke="2.4"), t) for t in AUDIT_STEPS)

    body = """<section class="page-hero wide">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="hero-glow"></div></div>
  <div class="wrap" style="position:relative;z-index:1">
    %(crumbs)s
    <h1>Book your free automation audit.</h1>
    <p class="lead">Thirty minutes on your business. We map where enquiries are lost and where
      time goes, and you leave with a written roadmap whether or not you work with us.</p>
  </div>
</section>

<section class="block tight">
  <div class="wrap contact-grid">
    <div class="contact-card reveal">
      <h2 style="font-family:'Montserrat';font-weight:700;font-size:1.5rem;color:var(--white);margin-bottom:.5rem">Tell us about your business</h2>
      <p style="color:var(--muted);font-size:.95rem;margin-bottom:1.8rem">The more you tell us
        about how enquiries reach you, the more useful the audit will be.</p>
      <form id="contactForm" data-endpoint="%(endpoint)s" data-sheet="%(sheet)s" novalidate>
        <div class="field">
          <label for="cName">Your name <span aria-hidden="true">*</span></label>
          <input type="text" id="cName" name="name" autocomplete="name" required
                 aria-describedby="cNameErr" placeholder="Jane Bennett">
          <div class="field-error" id="cNameErr">Please tell us your name.</div>
        </div>
        <div class="field">
          <label for="cEmail">Email <span aria-hidden="true">*</span></label>
          <input type="email" id="cEmail" name="email" autocomplete="email" required
                 aria-describedby="cEmailErr" placeholder="jane@yourcompany.co.uk">
          <div class="field-error" id="cEmailErr">Please enter a valid email address.</div>
        </div>
        <div class="field">
          <label for="cPhone">Telephone number <span aria-hidden="true">*</span></label>
          <div class="phone-row">%(cdial)s
            <input type="tel" id="cPhone" name="phone" autocomplete="tel" required
                   aria-describedby="cPhoneHint cPhoneErr" placeholder="07700 900000">
          </div>
          <p class="hint" id="cPhoneHint">With or without the leading 0 — either works.</p>
          <div class="field-error" id="cPhoneErr">Please enter a number we can reach you on.</div>
        </div>
        <div class="field">
          <label for="cType">What type of company is this? <span aria-hidden="true">*</span></label>
          %(ctype)s
          <div class="field-error" id="cTypeErr">Please pick the closest match.</div>
        </div>
        %(cother)s
        <div class="field">
          <label for="cCompany">Company</label>
          <input type="text" id="cCompany" name="company" autocomplete="organization"
                 placeholder="Your company">
        </div>
        <div class="field">
          <label for="cMessage">Where do you think you are losing enquiries? <span aria-hidden="true">*</span></label>
          <textarea id="cMessage" name="message" required aria-describedby="cMessageErr"
            placeholder="We miss a lot of calls during clinic hours, and quotes go out without anyone chasing them."></textarea>
          <div class="field-error" id="cMessageErr">A sentence or two is plenty.</div>
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%%"
                data-track="contact_form_submit_click" data-track-location="contact_page">
          Book My Free Automation Audit</button>
        <div class="form-status" id="contactStatus" role="status" aria-live="polite"></div>
        <p class="form-note">Sent straight to us the moment you submit. We use your details to
          answer your enquiry and for nothing else. Prefer to write directly?
          <a href="mailto:%(email)s" style="color:var(--cyan)">%(email)s</a>.</p>
      </form>
    </div>

    <div class="reveal">
      <span class="eyebrow">Get in touch</span>
      <h2 style="font-family:'Montserrat';font-weight:700;font-size:1.35rem;color:var(--white);margin:1rem 0 .5rem">Other ways to reach us</h2>
      <div class="contact-methods">%(methods)s</div>

      <h2 style="font-family:'Montserrat';font-weight:700;font-size:1.35rem;color:var(--white);margin:2.5rem 0 .8rem">What the audit covers</h2>
      <ul class="own-list">%(audit)s</ul>
      <p style="color:var(--muted);font-size:.9rem;margin-top:1.2rem">No cost, no obligation, and
        the roadmap is yours to keep.</p>
    </div>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), (None, "Contact")]),
           methods="".join(methods), audit=audit_items, email=EMAIL,
           cdial=dial_select("cCode"), ctype=company_type_select("cType", "cOther"), cother=company_type_other("cOther"),
           endpoint=FORM_ENDPOINT, sheet=SHEET_ENDPOINT)

    ld = [
        """{
  "@context":"https://schema.org",
  "@type":"ContactPage",
  "url":"%(site)s%(path)s",
  "name":"Contact Digital Autonomous",
  "mainEntity":{"@type":"ProfessionalService","name":"%(brand)s","email":"%(email)s","url":"%(site)s/"}
}""" % dict(site=SITE, path=path, brand=BRAND, email=EMAIL),
        breadcrumb_ld([("/", "Home"), (path, "Contact")]),
    ]

    html = (head("Contact | Book a Free Automation Audit | Digital Autonomous",
                 "Book a free 30-minute automation audit. We map where your business loses "
                 "enquiries and time, and you leave with a written roadmap.",
                 path, jsonld=ld)
            + header() + '<main id="main">' + body
            + faq_section(FAQ[:6], title="Before you get in touch",
                          eyebrow="Common questions", hid="contact-faq")
            + '</main>' + footer())
    write(path, html, "Contact", 0.9, "monthly")


# ==========================================================================
# Legal pages
# ==========================================================================
def legal_page(slug, title, meta_desc, sections):
    path = "/%s/" % slug
    parts = []
    for h, paras in sections:
        parts.append("<h2>%s</h2>" % h)
        parts.extend(paras)
    body = """<section class="page-hero wide">
  <div class="wrap">
    %(crumbs)s
    <h1>%(title)s</h1>
  </div>
</section>
<section class="block tight">
  <div class="wrap">
    <div class="prose reveal">
      <p class="doc-meta">Last updated %(updated)s</p>
      %(body)s
    </div>
  </div>
</section>
""" % dict(crumbs=crumbs([("/", "Home"), (None, title)]), title=title,
           updated=LEGAL_UPDATED, body="".join(parts))

    html = (head("%s | Digital Autonomous" % title, meta_desc, path,
                 jsonld=[breadcrumb_ld([("/", "Home"), (path, title)])])
            + header() + '<main id="main">' + body + '</main>' + footer())
    write(path, html, title, 0.2, "yearly")


def company_line():
    bits = []
    if COMPANY_NAME:
        bits.append(COMPANY_NAME)
    if COMPANY_NUMBER:
        bits.append("registered in England and Wales under company number %s" % COMPANY_NUMBER)
    if REGISTERED_OFFICE:
        bits.append("registered office %s" % REGISTERED_OFFICE)
    if bits:
        return "%s (%s)" % (BRAND, ", ".join(bits))
    return BRAND


def build_legal():
    P = lambda t: "<p>%s</p>" % t
    UL = lambda items: "<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in items)

    legal_page(
        "privacy", "Privacy Policy",
        "How Digital Autonomous collects, uses and protects personal data, and the rights "
        "you have over your information.",
        [
            ("Who we are", [
                P("For any question about this policy or about your personal data, contact "
                  "<a href=\"mailto:%s\">%s</a>." % (EMAIL, EMAIL)),
                P("For the purposes of data protection law we act as a <strong>controller</strong> "
                  "for data you send us directly, and as a <strong>processor</strong> for personal "
                  "data we handle inside a client's systems on that client's instructions. Where we "
                  "act as a processor, our client's own privacy notice governs that data and a "
                  "written data processing agreement sets out the terms."),
            ]),
            ("What this website collects", [
                UL([
                    "<strong>Contact and audit forms.</strong> These collect your name, "
                    "telephone number, email address, company type and whatever you tell us "
                    "about your business. They reach us by email through a form-relay service "
                    "that processes the submission on our behalf and uses it for nothing else. "
                    "We use the details to answer your enquiry and arrange your audit.",
                    "<strong>Email you send us.</strong> If you email us, we receive your address, "
                    "your message and anything you attach.",
                ]),
            ]),
            ("Why we use it, and our lawful basis", [
                UL([
                    "<strong>To reply to your enquiry</strong> — legitimate interests, and steps "
                    "taken at your request prior to entering a contract.",
                    "<strong>To provide services to clients</strong> — performance of a contract.",
                    "<strong>To arrange the audit you asked for</strong> — consent, which you give "
                    "by submitting the form and can withdraw at any time.",
                    "<strong>To keep the site secure and available</strong> — legitimate interests.",
                ]),
            ]),
            ("How long we keep it", [
                P("Enquiry correspondence is kept for as long as needed to deal with the enquiry "
                  "and for a reasonable period afterwards, then deleted. Audit request details are "
                  "kept only for as long as needed to arrange and follow up that audit. A "
                  "specific retention schedule will be published here once confirmed."),
            ]),
            ("Who we share it with", [
                P("We do not sell personal data and we do not share it for advertising."),
            ]),
        ])

    legal_page(
        "cookies", "Cookie Policy",
        "Digital Autonomous does not set cookies on this website. This policy explains what "
        "that means and what would change if that ever does.",
        [
            ("The short version", [
                P("<strong>This website sets no cookies.</strong> There is no analytics script, no "
                  "advertising pixel, no social media tracker and no consent banner, because there "
                  "is nothing to consent to."),
            ]),
            ("What we do instead", [
                P("The site includes a small piece of tracking code that records interactions — a "
                  "click on a call-to-action, for example — in the browser's memory only, so that "
                  "an analytics tool could be connected in future. As shipped it sends nothing "
                  "anywhere and stores nothing on your device."),
            ]),
            ("Things that are not cookies but are worth knowing", [
                UL([
                    "<strong>Google Fonts.</strong> Typefaces load from Google's servers, so your "
                    "browser contacts Google and Google sees your IP address. No cookie is set by "
                    "the font request.",
                    "<strong>Hosting logs.</strong> GitHub, our host, keeps standard server logs.",
                ]),
            ]),
            ("If this changes", [
                P("If we add analytics, a booking widget, a live chat tool or anything else that "
                  "stores data on your device, we will update this page and — where the law "
                  "requires it — ask for your consent before it loads. Our preference is "
                  "cookieless, privacy-conscious tooling wherever a usable option exists."),
            ]),
            ("Controlling cookies", [
                P("Every major browser lets you block or delete cookies through its settings. "
                  "Since this site sets none, doing so will not affect how it works."),
            ]),
        ])

    legal_page(
        "terms", "Terms & Conditions",
        "The terms governing use of the Digital Autonomous website, and the basis on which "
        "automation services are provided.",
        [
            ("Who these terms are with", [
                P("This website is operated by %s. By using the site you accept these terms."
                  % company_line()),
            ]),
            ("Illustrative material", [
                P("Automation examples shown on this site — including the example automation on "
                  "the homepage and the demonstration under \"See Automation in Action\" — are "
                  "labelled as illustrative. They show how a system of that type works. They are "
                  "not recordings of client activity and are not a promise of any particular "
                  "result for your business."),
            ]),
            ("Intellectual property", [
                P("The Digital Autonomous name, logo, site design and written content belong to "
                  "us. Third-party names and marks shown on the integrations section belong to "
                  "their respective owners and are used only to identify platforms we can connect "
                  "to. Their appearance does not imply partnership, endorsement or affiliation."),
            ]),
            ("Services and how we charge", [
                P("Automation services are provided under a separate written agreement. Our "
                  "standard commercial model is a <strong>setup fee</strong> for designing and "
                  "building the automation, plus a <strong>monthly management fee</strong> for "
                  "monitoring, support, maintenance and ongoing optimisation."),
                P("Clients retain ownership of their own business accounts, systems and data. We "
                  "manage and maintain the automation infrastructure as a service. The specific "
                  "scope, licensing position and what happens at the end of an engagement are set "
                  "out in the engagement agreement rather than here."),
            ]),
            ("Contact", [
                P("Questions about these terms: <a href=\"mailto:%s\">%s</a>." % (EMAIL, EMAIL)),
            ]),
        ])


# ==========================================================================
# 404
# ==========================================================================
def build_404():
    body = """<section class="block" style="padding-top:clamp(3rem,8vw,6rem)">
  <div class="wrap">
    <div class="empty-state reveal">
      <div class="eico">%(eico)s</div>
      <h1>That page does not exist.</h1>
      <p>The link may be out of date, or the address may have a typo in it.
        Here is the way back.</p>
      <div class="btn-row center">%(a)s%(b)s</div>
    </div>
    <div class="rel-grid reveal" style="margin-top:2.5rem">
      <a class="rel" href="/#solutions"><div class="k">Automation solutions</div><div class="d">The eight systems we build</div></a>
      <a class="rel" href="/industries/"><div class="k">Industries</div><div class="d">Sectors we know well</div></a>
      <a class="rel" href="/contact/"><div class="k">Contact</div><div class="d">Book a free automation audit</div></a>
    </div>
  </div>
</section>
""" % dict(eico=icon("search"),
           a=btn("/", "Back to the homepage", arrow=True),
           b=btn("/contact/", "Contact us", kind="ghost"))

    html = ("""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | Digital Autonomous</title>
<meta name="description" content="That page could not be found on the Digital Autonomous website. Use the links here to find automation solutions, industries or contact us.">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#05101f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Lato:wght@400;700&display=swap">
<script>document.documentElement.className+=" js"</script>
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""" + header() + '<main id="main">' + body + '</main>' + footer())

    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


# ==========================================================================
# Writing, sitemap, robots, icons
# ==========================================================================
def write(path, html, title, priority, changefreq):
    if path == "/":
        target = os.path.join(ROOT, "index.html")
    else:
        d = os.path.join(ROOT, path.strip("/").replace("/", os.sep))
        os.makedirs(d, exist_ok=True)
        target = os.path.join(d, "index.html")
    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    PAGES.append((path, title, priority, changefreq))


def build_sitemap():
    urls = []
    for path, _title, pri, freq in PAGES:
        urls.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>2026-08-28</lastmod>\n"
                    "    <changefreq>%s</changefreq>\n    <priority>%.1f</priority>\n  </url>"
                    % (SITE, path, freq, pri))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)


def build_robots():
    txt = ("User-agent: *\n"
           "Allow: /\n\n"
           "# Generator source is not content.\n"
           "Disallow: /_src/\n\n"
           "Sitemap: %s/sitemap.xml\n" % SITE)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)


def build_icons():
    """Render the logo mark to apple-touch-icon.png (180) and favicon.ico."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  ! Pillow not available — icons left as-is")
        return

    def draw_mark(size):
        S = 4  # supersample
        n = size * S
        img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        r = int(n * 0.225)
        d.rounded_rectangle([0, 0, n - 1, n - 1], radius=r, fill=(10, 26, 58, 255))

        def pt(x, y):
            return (x / 40 * n, y / 40 * n)

        w = max(1, int(n * 0.065))
        d.line([pt(6, 30), pt(15, 23.5), pt(21.5, 27), pt(31.5, 11.5)],
               fill=(0, 166, 251, 255), width=w, joint="curve")
        d.line([pt(31.5, 11.5), pt(25.5, 12)], fill=(102, 210, 249, 255), width=w)
        d.line([pt(31.5, 11.5), pt(30.7, 17.5)], fill=(102, 210, 249, 255), width=w)

        for (x, y, rad, col) in [(6, 30, 2.6, (102, 210, 249, 255)),
                                 (15, 23.5, 2.6, (255, 255, 255, 255)),
                                 (21.5, 27, 2.6, (102, 210, 249, 255)),
                                 (31.5, 11.5, 3.0, (0, 166, 251, 255))]:
            cx, cy = pt(x, y)
            rr = rad / 40 * n
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)

        return img.resize((size, size), Image.LANCZOS)

    draw_mark(180).save(os.path.join(ROOT, "apple-touch-icon.png"))
    ico = draw_mark(64)
    ico.save(os.path.join(ROOT, "favicon.ico"),
             sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("  + apple-touch-icon.png, favicon.ico")


def clean_generated():
    """Remove pages this generator owns, so a rename does not leave an orphan.

    Deletes files first and only then tries the directories: OneDrive keeps
    handles on synced folders, so an rmdir can fail with WinError 5 even when
    the folder is empty. An undeleted empty directory is harmless — an
    undeleted stale index.html is not — so only the file removal is fatal.
    """
    owned = ([s["slug"] for s in SERVICES]
             + ["industries", "about", "case-studies", "insights", "contact",
                "privacy", "cookies", "terms"])
    for name in owned:
        base = os.path.join(ROOT, name)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirnames, filenames in os.walk(base):
            for fn in filenames:
                if fn.endswith(".html"):
                    os.remove(os.path.join(dirpath, fn))
        for dirpath, dirnames, filenames in os.walk(base, topdown=False):
            if not dirnames and not filenames:
                try:
                    os.rmdir(dirpath)
                except OSError:
                    pass  # OneDrive still holding it; rebuilt in place anyway


# ==========================================================================
def main():
    clean_generated()

    build_home()
    for s in SERVICES:
        build_service(s)
    build_industries_hub()
    for i in INDUSTRIES:
        build_industry(i)
    build_about()
    build_case_studies()
    build_contact()
    build_legal()
    build_404()

    build_sitemap()
    build_robots()
    build_icons()

    print("Built %d pages:" % len(PAGES))
    for path, title, _p, _f in PAGES:
        print("  %-42s %s" % (path, title))


if __name__ == "__main__":
    main()
