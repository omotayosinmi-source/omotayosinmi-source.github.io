# Deploying digitalautonomous.co.uk

Static multi-page site, 21 pages. GitHub Pages serves exactly what is committed —
there is no build step at deploy time. The HTML is *generated* before committing;
see **Editing the site** below.

## Status

- [x] Domain **digitalautonomous.co.uk** registered at **Porkbun**
      (nameservers: `curitiba` / `fortaleza` / `maceio` / `salvador.ns.porkbun.com`)
- [x] GitHub repo created and pushed
- [x] Pages enabled (GitHub auto-enabled it on first push and auto-bound the
      custom domain from the committed `CNAME`)
- [x] DNS pointed at GitHub — apex and `www` both resolve to GitHub's
      addresses, confirmed live
- [x] HTTPS enforced

Note: `digitalautonomous.com` is owned by a third party (registered 2020, parked
on Afternic for resale). Nothing in this site references it.

## 1. Create the GitHub repo and push

Name the repo `omotayosinmi-source.github.io` — it must exactly match the
account name. That matters: this site uses
root-absolute asset paths (`/favicon.svg`, `/og-image.png`), which resolve
correctly at a domain root but break under a project path like
`username.github.io/reponame/`.

```bash
git remote add origin https://github.com/omotayosinmi-source/omotayosinmi-source.github.io.git
git push -u origin main
```

## 2. Enable Pages

Repo → **Settings** → **Pages**:

- Source: **Deploy from a branch**
- Branch: `main`, folder `/ (root)`

`CNAME` is already committed, so the custom domain populates itself.

## 3. Point Porkbun's DNS at GitHub

Porkbun → **Domain Management** → `digitalautonomous.co.uk` → **DNS**.

**First delete the default parking records** Porkbun created — the `ALIAS`/`A`
record on the root (`@`) and the `CNAME` on `www` that point at Porkbun's
`pixie` / parking hosts. Leaving them in place will fight the new records.

Then add:

| Type | Host | Answer |
|------|------|--------|
| A    | *(blank = root)* | 185.199.108.153 |
| A    | *(blank)* | 185.199.109.153 |
| A    | *(blank)* | 185.199.110.153 |
| A    | *(blank)* | 185.199.111.153 |
| AAAA | *(blank)* | 2606:50c0:8000::153 |
| AAAA | *(blank)* | 2606:50c0:8001::153 |
| AAAA | *(blank)* | 2606:50c0:8002::153 |
| AAAA | *(blank)* | 2606:50c0:8003::153 |
| CNAME | `www` | `omotayosinmi-source.github.io` |

Porkbun's "Host" field is the subdomain only — leave it **empty** for the apex,
do not type `@` or the full domain.

All four IPv4 addresses verified live and returning `Server: GitHub.com` on
2026-08-26.

Leave any MX / TXT records alone if you later set up mail.

## 4. Force HTTPS

Once DNS resolves to GitHub, tick **Enforce HTTPS** in Settings → Pages. GitHub
issues a Let's Encrypt certificate automatically; it can take up to ~24h to
become available after the DNS change.

**Done.** The certificate is issued (Let's Encrypt, covers both the apex and
`www`), Enforce HTTPS is on, and HTTP now 301-redirects to HTTPS.

## Verifying

```bash
# Has DNS moved off Porkbun's parking IPs onto 185.199.x.x?
nslookup digitalautonomous.co.uk 8.8.8.8

# Site serving over TLS?
curl -sI https://digitalautonomous.co.uk | head -1

# Custom domain bound correctly?
curl -s https://digitalautonomous.co.uk/CNAME
```

## Still to fill in

Everything below is deliberately absent rather than faked. The templates omit any
field left blank, so nothing renders as a visible placeholder until it is real.

| What | Where to set it | Why it is blank |
|---|---|---|
| Mailbox for `hello@digitalautonomous.co.uk` | Porkbun free forwarding is enough to start | Registering the domain does not create the mailbox, and the address is the site's only contact route |
| Phone number | `PHONE` in `_src/content.py` | No real business line yet. Set it and the footer, contact page and `tel:` tracking all light up |
| LinkedIn (company) | `LINKEDIN` in `_src/content.py` | Footer icon and contact card appear once set |
| LinkedIn + photo + bio (founder) | `LINKEDIN_FOUNDER` in `_src/content.py`, plus the About founder card | Nothing about the founder is invented; the card shows an explicit "reserved" note until supplied |
| Registered company details | `COMPANY_NAME`, `COMPANY_NUMBER`, `REGISTERED_OFFICE` | Printed in the footer and woven into the legal pages once confirmed |
| Legal review | `/privacy/`, `/cookies/`, `/terms/` | Written to be accurate about how the site actually behaves, but each carries a visible "pending legal review" callout |
| First case study | `build_case_studies()` in `_src/build.py` | There are no clients yet. The page publishes the *format* instead of inventing results |
| Real form delivery | `data-endpoint` on `#auditForm` and `#contactForm` | Static hosting has no server, so both forms validate then hand off to the visitor's mail client. Set an endpoint and they POST JSON instead |
| Leads spreadsheet | `SHEET_ENDPOINT` in `_src/content.py` | Deploy `_src/sheet-logger.gs` as a Google Apps Script web app and paste its `/exec` URL here. See **The leads spreadsheet** below |
| Analytics | subscribe to the `da:track` event in `assets/js/site.js` | No third-party script and no cookies ship by default |

### The leads spreadsheet

Every submission is sent to two places at once: the email relay, and a Google
Sheet that logs it as a row. A submission counts as delivered if **either** gets
through, so a spreadsheet outage never costs an enquiry.

`_src/sheet-logger.gs` is the Apps Script. Setup, once:

1. `sheets.new`, name it *Digital Autonomous — Leads*.
2. **Extensions → Apps Script**, paste the file in, save.
3. **Run → setup**, and authorise it. This builds the *Leads* and *Dashboard*
   tabs, the status dropdown and the conditional formatting.
4. **Deploy → New deployment → Web app**, execute as *Me*, access *Anyone*.
5. Copy the `/exec` URL into `SHEET_ENDPOINT`, rebuild, push.

The *Leads* tab has a column per field plus **Status**, **Follow up on** and
**Notes** for working the pipeline. The *Dashboard* tab is formula-driven, so it
stays live as those columns are edited: totals, last 7 and 30 days, a breakdown
by status, company type and source, and a list of leads still marked New.

Editing the script later needs **Deploy → Manage deployments → New version**, or
the old code keeps running.

The sheet also gets a **Digital Autonomous** menu: *Clear test rows* (removes
anything written while setting up and leaves genuine leads alone), *Delete ALL
leads*, and *Rebuild dashboard*. Both deletions confirm first and are driven
from inside the sheet by a signed-in person — there is deliberately no delete
path on the web endpoint, so knowing the URL can never remove data.

A menu change needs the file re-pasted and saved, then the spreadsheet
reloaded; running a menu item uses the saved code, so no redeploy is needed for
that.

Two notes on limits. Apps Script web apps do not answer CORS preflights, so the
browser posts `text/plain` and the script parses the body itself — do not
"fix" that to `application/json`. And the sheet is a log, not a database: if it
ever grows past a few thousand rows, move the Dashboard queries to a pivot table.

### The claims rule

`_src/check.py` fails the build on fake testimonials, invented client counts,
unheld certifications, placeholder text, stray percentage/hours-saved claims that
are not marked illustrative, and **named delivery vendors**. Do not weaken it to
get a number onto the page — add the number when there is a client behind it.

The vendor rule exists because which platforms we build on is our implementation
detail, not the client's concern: naming them invites the reader to price up doing
it themselves, and ties our positioning to someone else's brand.

## Editing the site

The HTML is generated. **Never hand-edit a generated `index.html`** — the next
build overwrites it.

```
_src/content.py       all copy, services, industries, FAQ, business details
_src/build.py         templates and page assembly
_src/check.py         link / anchor / SEO / accessibility / claims checks
_src/serve.mjs        local preview server (mirrors Pages routing)
_src/og-template.html source for og-image.png
assets/css/site.css   hand-written stylesheet
assets/js/site.js     hand-written behaviour
```

Everything else in the repo root is output.

```bash
python _src/build.py     # regenerate all 21 pages + sitemap.xml + robots.txt + icons
python _src/check.py     # must print "All checks passed" before committing
node _src/serve.mjs      # preview on http://localhost:3000
```

`build.py` also regenerates `favicon.ico` and `apple-touch-icon.png` from the logo
mark (needs Pillow). `og-image.png` is rendered separately from
`_src/og-template.html` at 1200x630 — only regenerate it if the headline changes.

## Updating the site later

```bash
python _src/build.py && python _src/check.py
git add -A
git commit -m "Describe the change"
git push
```

Pages redeploys in roughly a minute.

## Adding a page

Add it to the relevant list in `_src/content.py` (`SERVICES` or `INDUSTRIES`) and
it appears automatically in the nav, the footer, the sitemap and the internal
linking. Anything else needs a `build_*()` function in `_src/build.py` ending in a
`write(path, html, title, priority, changefreq)` call — that call is what registers
the page with the sitemap, and `check.py` fails if a page and the sitemap disagree.
