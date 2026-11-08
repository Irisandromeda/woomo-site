# WooMo site (GitHub Pages)

Home, Privacy Policy, Terms of Use and Support in English (root), Ukrainian (`uk/`) and Russian (`ru/`).

Sources: `src/<lang>/<page>.html` (first lines are `title:` metadata, then `---`, then the page body), shared `assets/`.
Build: `python3 tools/build.py src docs irisandromeda.dev@gmail.com` → static site in `docs/`, published by GitHub Pages from `main` / `docs`.
