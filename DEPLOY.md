# Deploying digitalautonomous.co.uk

Static one-page site. No build step — what is in this repo is what ships.

## 1. Register the domain

Register **digitalautonomous.co.uk** with any Nominet-accredited registrar
(Namecheap, Gandi, Porkbun, IONOS, 123-reg). Confirmed available 2026-08-26.

Note: `digitalautonomous.com` is *not* available — it was registered in 2020 and
sits on Afternic's nameservers, i.e. held by a reseller. Buying it means an
aftermarket negotiation, not a £10 registration.

Enable WHOIS privacy and auto-renew while you are in there.

## 2. Create the GitHub repo and push

Name the repo `<your-username>.github.io`. That matters: this site uses
root-absolute asset paths (`/favicon.svg`, `/og-image.png`), which resolve
correctly at a domain root but break under a project path like
`username.github.io/reponame/`.

```bash
git remote add origin https://github.com/<your-username>/<your-username>.github.io.git
git push -u origin main
```

## 3. Enable Pages

Repo → **Settings** → **Pages**:

- Source: **Deploy from a branch**
- Branch: `main`, folder `/ (root)`

`CNAME` is already committed, so the custom domain populates itself.

## 4. Point DNS at GitHub

At your registrar's DNS panel, for the apex record (`@`):

| Type | Name | Value |
|------|------|-------|
| A    | @    | 185.199.108.153 |
| A    | @    | 185.199.109.153 |
| A    | @    | 185.199.110.153 |
| A    | @    | 185.199.111.153 |
| AAAA | @    | 2606:50c0:8000::153 |
| AAAA | @    | 2606:50c0:8001::153 |
| AAAA | @    | 2606:50c0:8002::153 |
| AAAA | @    | 2606:50c0:8003::153 |
| CNAME | www | `<your-username>.github.io.` |

All four IPv4 addresses verified live and returning `Server: GitHub.com` on
2026-08-26.

## 5. Force HTTPS

Once DNS resolves, tick **Enforce HTTPS** in Settings → Pages. GitHub issues a
Let's Encrypt certificate automatically; this can take up to ~24h to become
available after the DNS change.

## Verifying

```bash
# DNS resolving to GitHub?
nslookup digitalautonomous.co.uk

# Site serving over TLS?
curl -sI https://digitalautonomous.co.uk | head -1

# Custom domain bound correctly?
curl -s https://digitalautonomous.co.uk/CNAME
```

## Still to fill in

- `tel:+441234567890` / "+44 (0) 1234 567 890" in `index.html` is a **placeholder**.
  Replace it with the real number or delete the line — a fake number on a live
  site is worse than none.
- Footer social links (LinkedIn, X) and the "Careers" link are `href="#"`.
- Set up mail for `hello@digitalautonomous.co.uk`; it is referenced 3x in the page
  but registering the domain does not create the mailbox.

## Updating the site later

```bash
git add -A
git commit -m "Describe the change"
git push
```

Pages redeploys in roughly a minute.
