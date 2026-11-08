#!/usr/bin/env python3
"""Builds the static WooMo site from src/<lang>/*.html into out/. Usage: build.py <src> <out> <email>"""
import sys, os, shutil, html
src, out, email = sys.argv[1], sys.argv[2], sys.argv[3]
LANGS = {"en": ("English", ""), "uk": ("Українська", "uk/"), "ru": ("Русский", "ru/")}
NAV = {
 "en": ("Home", "Privacy", "Terms", "Support", "Language"),
 "uk": ("Головна", "Конфіденційність", "Умови", "Підтримка", "Мова"),
 "ru": ("Главная", "Конфиденциальность", "Условия", "Поддержка", "Язык"),
}
FOOT = {"en": "WooMo is developed by Olha Dyka, Ukraine.", "uk": "WooMo розробляє Ольга Дика, Україна.", "ru": "WooMo разрабатывает Ольга Дикая, Украина."}
PAGES = ["index", "privacy", "terms", "support"]
TPL = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{root}assets/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/style.css">
{alts}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{root}{lp}index.html">WooMo</a>
  <nav>{nav}</nav>
</div></header>
<main class="wrap{cls}">
{body}
</main>
<footer class="wrap foot">
  <p>{langs}</p>
  <p>© 2026 WooMo · {foot} · <a href="mailto:{email}">{email}</a></p>
</footer>
</body>
</html>
"""
if os.path.exists(out): shutil.rmtree(out)
shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"), os.path.join(out, "assets"))
for lang, (lname, lp) in LANGS.items():
    root = "../" if lp else ""
    for page in PAGES:
        raw = open(os.path.join(src, lang, page + ".html"), encoding="utf-8").read()
        head, body = raw.split("\n---\n", 1)
        meta = dict(l.split(": ", 1) for l in head.splitlines())
        n = NAV[lang]
        links = [("index", n[0]), ("privacy", n[1]), ("terms", n[2]), ("support", n[3])]
        nav = " ".join(f'<a href="{root}{lp}{p}.html"{" aria-current=\"page\"" if p == page else ""}>{t}</a>' for p, t in links)
        langs = n[4] + ": " + " · ".join(
            (f"<strong>{nm}</strong>" if l == lang else f'<a href="{root}{p2}{page}.html" hreflang="{l}">{nm}</a>')
            for l, (nm, p2) in LANGS.items())
        alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{root}{p2}{page}.html">' for l, (nm, p2) in LANGS.items())
        title = meta["title"] if page == "index" else f'{meta["title"]} · WooMo'
        doc = TPL.format(lang=lang, title=html.escape(title), desc=html.escape(meta["title"]), root=root, lp=lp, nav=nav,
                         alts=alts, body=body.replace("__ROOT__", root), cls=" home" if "home" in meta else " doc",
                         langs=langs, foot=FOOT[lang], email=email)
        doc = doc.replace("__EMAIL__", email)
        d = os.path.join(out, lp); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, page + ".html"), "w", encoding="utf-8").write(doc)
open(os.path.join(out, ".nojekyll"), "w").close()
print("built", out)
