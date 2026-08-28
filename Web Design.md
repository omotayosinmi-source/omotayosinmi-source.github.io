# CLAUDE.md — Frontend Website Rules

Rules for working on **digitalautonomous.co.uk**. `DEPLOY.md` covers hosting, DNS
and the outstanding content gaps; this file covers how to build.

## Always Do First

- **Invoke the `frontend-design` skill** before writing any frontend code, every
  session, no exceptions.
- **Read `_src/content.py` before writing copy.** All site copy lives there. Editing
  a generated `index.html` is always wrong — the next build overwrites it.

## The site is generated

21 static pages, produced by a Python generator and committed as plain HTML.
GitHub Pages serves the output as-is; there is no build step at deploy time.

| Source | What it is |
|---|---|
| `_src/content.py` | Copy, services, industries, FAQ, business details |
| `_src/build.py` | Templates, page assembly, sitemap, robots, icon generation |
| `_src/check.py` | Link / anchor / SEO / accessibility / claims checks |
| `_src/serve.mjs` | Local preview server (mirrors Pages routing, including 404) |
| `_src/og-template.html` | Source for `og-image.png` |
| `assets/css/site.css` | Hand-written stylesheet — the design system |
| `assets/js/site.js` | Hand-written behaviour — no dependencies |

Everything else in the repo root is output. Never hand-edit it.

```bash
python _src/build.py     # regenerate everything
python _src/check.py     # must pass before committing
node _src/serve.mjs      # preview on http://localhost:3000
```

## The claims rule

This site sells trust. Nothing may assert a client result, a metric, a
certification, a named customer or a founder detail that is not verified.

- There are no clients yet, so there are **no case studies and no numbers**.
- Illustrative material is labelled illustrative, in the markup, where the visitor
  sees it — not in a footnote.
- Optional business details (`PHONE`, `LINKEDIN`, `COMPANY_NUMBER`, …) are blank in
  `content.py` and the templates **omit** them rather than printing a placeholder.
- `check.py` fails the build on fake testimonials, invented client counts, unheld
  certifications, placeholder text and unmarked percentage/hours-saved claims.

Do not weaken the checker to get a number onto the page. Add the number when there
is a client behind it.

## Local Server

- **Always serve on localhost** — never screenshot a `file:///` URL. Root-absolute
  asset paths (`/assets/…`, `/favicon.svg`) do not resolve under `file:///`, and
  directory URLs like `/about/` need the server's index resolution.
- `node _src/serve.mjs [port]` — defaults to port 3000, serves the repo root.
- If the server is already running, do not start a second instance.

## Screenshot Workflow

Chrome is cached at `C:/Users/omota/.cache/puppeteer/chrome/`. Install
`puppeteer-core` in the scratchpad (not in this repo — it must stay dependency-free)
and point `executablePath` at that binary.

Two things that will waste your time if you do not know them:

- **`html{scroll-behavior:smooth}` makes `scrollIntoView` animate.** Measuring or
  hit-testing straight after it reads a mid-scroll position. Pass
  `{behavior:'instant'}`.
- **`.reveal` sections start at `opacity:0`.** Scroll the whole page before
  capturing a full-page screenshot or everything below the fold shoots blank.

When comparing, be specific: "heading is 32px but reference shows ~24px", "card gap
is 16px but should be 24px". Check spacing/padding, font size/weight/line-height,
colours (exact hex), alignment, border-radius, shadows, image sizing.

## Verify before claiming done

`check.py` covers the static side. For anything visual or interactive, drive a real
browser — do not assume:

- Every page at 1440px **and** 390px: no horizontal overflow, no clipped text.
- Card overlay links (`h3 a::after`) actually hit-test across the whole card.
- Mobile menu opens, locks scroll, closes on Escape.
- Forms: empty submit blocks, invalid email is caught, valid submit clears errors.
- `prefers-reduced-motion`: all content visible, animations resolved to end state.
- WCAG contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text, computed against the
  actual painted background.

## Brand Assets

`Brand Assets/logo-and-themes/` is the visual source of truth.

- Navy `#0A1A3A` · Vibrant blue `#00A6FB` · Secondary `#66D2F9` · Gray `#6C757D` ·
  Light gray `#E1E4E8`
- Montserrat (headings, 500–800) / Lato (body, 400/700)
- Tagline: Intelligence · Automation · Acceleration

Do not invent brand colours. The tokens in `site.css` `:root` are the palette; use
them rather than raw hex.

## Anti-Generic Guardrails

- **Colours:** never the default Tailwind palette. Derive from the brand tokens.
- **Shadows:** no flat `shadow-md`. Layered, colour-tinted, low opacity —
  `--shadow-1/2/3` exist for this.
- **Typography:** Montserrat display against Lato body. Tight tracking
  (`-.022em`) on large headings, generous line-height (1.7) on body.
- **Animations:** only `transform` and `opacity`. Never `transition-all`.
- **Interactive states:** every clickable element needs hover, focus-visible and
  active. No exceptions.
- **Spacing:** use the `--s1`…`--s8` and `--section` tokens, not arbitrary values.
- **Depth:** base → elevated → floating. Surfaces should not all sit on one plane.
- **Icons:** always via `icon()` in `build.py`, which emits explicit `width`/`height`.
  A bare `viewBox` SVG falls back to 300×150 and silently blows out its flex row.

## Hard Rules

- Do not hand-edit generated HTML
- Do not fabricate results, metrics, testimonials or founder details
- Do not add a dependency to this repo — it ships as static files
- Do not use `transition-all`
- Do not stop after one screenshot pass
