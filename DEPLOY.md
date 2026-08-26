# Deploying digitalautonomous.co.uk

Static one-page site. No build step — what is in this repo is what ships.

## Status

- [x] Domain **digitalautonomous.co.uk** registered at **Porkbun**
      (nameservers: `curitiba` / `fortaleza` / `maceio` / `salvador.ns.porkbun.com`)
- [ ] GitHub repo created and pushed
- [ ] Pages enabled
- [ ] DNS pointed at GitHub — apex currently serves Porkbun's parked page
      (`207.207.210.107` / `207.207.210.229`), `www` does not resolve
- [ ] HTTPS enforced

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
become available after the DNS change. Until then the site serves over HTTP.

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

- Footer social links (LinkedIn, X) and the "Careers" link are `href="#"`.
- Set up mail for `hello@digitalautonomous.co.uk`; it is referenced 3x in the
  page, but registering the domain does not create the mailbox. Porkbun offers
  forwarding free, which is enough to start.
- No phone number is listed. Add one back to the footer "Get in touch" column
  when you have a real business line.

## Updating the site later

```bash
git add -A
git commit -m "Describe the change"
git push
```

Pages redeploys in roughly a minute.
