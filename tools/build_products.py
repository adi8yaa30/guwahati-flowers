#!/usr/bin/env python3
"""Generate the static product pages in site/products/.

The header, CTA band and footer are copied from site/index.html so the home
page stays the single source of truth for them. Edit PRODUCTS below, then run:

    python3 tools/build_products.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "products"

BOUQUET, STEM = "bouquet", "stem"

PRODUCTS = [
    {
        "slug": "blush-lily", "name": "Blush Lily", "kind": BOUQUET, "price": "[PRICE]",
        "short": "Pink lilies, roses & baby's breath",
        "lead": "Soft pink lilies and garden roses, clouded with baby's breath and finished in a white wrap with a satin bow. A sweet choice for birthdays and thank-yous.",
        "includes": ["Pink oriental lilies", "Pink roses", "Baby's breath", "White wrap with pink satin ribbon"],
        "img": "hero-bouquet-white.webp", "w": 376, "h": 483,
        "alt": "Blush Lily bouquet — pink lilies and roses in white wrap with a pink ribbon",
    },
    {
        "slug": "kraft-romance", "name": "Kraft Romance", "kind": BOUQUET, "price": "[PRICE]",
        "short": "Lilies wrapped in kraft paper",
        "lead": "Pink lilies and blush blooms gathered in natural kraft paper and tied with raffia. Relaxed, romantic and made for anniversaries.",
        "includes": ["Pink lilies", "Blush seasonal blooms", "Fresh greens", "Kraft wrap tied with raffia"],
        "img": "hero-bouquet-kraft.webp", "w": 254, "h": 366,
        "alt": "Kraft Romance bouquet — pink lilies wrapped in kraft paper",
    },
    {
        "slug": "garden-pastel", "name": "Garden Pastel", "kind": BOUQUET, "price": "[PRICE]",
        "short": "Mixed seasonal blooms",
        "lead": "A loose, just-picked mix of the season's prettiest pastels, wrapped in dusty pink. Every bouquet is a little different, depending on what's freshest that morning.",
        "includes": ["Pastel roses", "Seasonal mixed blooms", "Fresh greens", "Dusty pink wrap with ribbon"],
        "img": "bouquet-garden-pastel.webp", "w": 466, "h": 467,
        "alt": "Garden Pastel bouquet — mixed seasonal blooms in pastel wrap",
    },
    {
        "slug": "cloud-white", "name": "Cloud White", "kind": BOUQUET, "price": "[PRICE]",
        "short": "Whites in a soft blue wrap",
        "lead": "Creamy white roses and delicate fillers in a soft blue wrap. Calm and elegant, for weddings, new beginnings and quiet sympathies.",
        "includes": ["White roses", "Baby's breath", "Fresh greens", "Soft blue wrap with ribbon"],
        "img": "bouquet-cloud-white.webp", "w": 413, "h": 550,
        "alt": "Cloud White bouquet — white roses in a soft blue wrap",
    },
    {
        "slug": "oriental-lily", "name": "Oriental Lily", "kind": STEM, "price": "[PRICE]",
        "short": "Sold by the stem",
        "lead": "Large, fragrant pink lilies with buds that keep opening for days. Pick as many stems as you like for a vase or your own arrangement.",
        "includes": ["Long-stemmed pink oriental lily", "Several buds per stem", "Wrapped for delivery"],
        "img": "stem-lily.webp", "w": 346, "h": 499,
        "alt": "Oriental Lily — a single pink lily stem",
    },
    {
        "slug": "white-rose", "name": "White Rose", "kind": STEM, "price": "[PRICE]",
        "short": "Sold by the stem",
        "lead": "Classic white roses with full, velvety heads. Timeless on their own and beautiful in a cluster.",
        "includes": ["Long-stemmed white rose", "Leaves left on", "Wrapped for delivery"],
        "img": "stem-rose.webp", "w": 302, "h": 527,
        "alt": "White Rose — a single white rose stem",
    },
    {
        "slug": "sunflower", "name": "Sunflower", "kind": STEM, "price": "[PRICE]",
        "short": "Sold by the stem",
        "lead": "Bright, cheerful sunflowers that turn any room sunny. A favourite for get-well-soon wishes and congratulations.",
        "includes": ["Sunflower stem", "Large open blooms", "Wrapped for delivery"],
        "img": "stem-sunflower.webp", "w": 423, "h": 547,
        "alt": "Sunflower — a single sunflower stem",
    },
    {
        "slug": "pink-tulip", "name": "Pink Tulip", "kind": STEM, "price": "[PRICE]",
        "short": "Sold by the stem",
        "lead": "Graceful pink tulips with smooth, cupped petals. Lovely as a single stem or gathered in a bunch.",
        "includes": ["Single pink tulip stem", "Fresh leaves", "Wrapped for delivery"],
        "img": "stem-tulip.webp", "w": 310, "h": 551,
        "alt": "Pink Tulip — a single pink tulip stem",
    },
]

e = html.escape


def extract(src, start, end):
    i = src.index(start)
    return src[i:src.index(end, i) + len(end)]


def relink(fragment):
    """Point a fragment copied from index.html at the right places from /products/."""
    fragment = re.sub(r'href="#(?=[a-z])', 'href="../index.html#', fragment)
    fragment = fragment.replace('href="../index.html#top"', 'href="../index.html"')
    fragment = re.sub(r'(src|srcset)="img/', r'\1="../img/', fragment)
    fragment = fragment.replace('href="products/', 'href="')
    return fragment


def card(p):
    return f'''          <li class="card reveal" data-name="{e(p["name"])}"{' data-kind="stem"' if p["kind"] == STEM else ''}>
            <a class="card__media" href="{p["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="../img/{p["img"]}" alt="" width="{p["w"]}" height="{p["h"]}" loading="lazy"></a>
            <div class="card__head"><h3 class="card__name"><a href="{p["slug"]}.html">{e(p["name"])}</a></h3><span class="card__price">₹ {p["price"]}</span></div>
            <p class="card__desc">{e(p["short"])}</p>
            <div class="card__actions"><button class="btn btn--cream" type="button" data-add>Add to Cart</button><a class="btn btn--cream" data-buy target="_blank" rel="noopener" href="#">Buy Now</a></div>
          </li>'''


def page(p, header, cta, footer, sprig):
    is_stem = p["kind"] == STEM
    category, anchor = ("Fresh Flowers", "fresh") if is_stem else ("Bouquets", "bouquets")
    unit = "stems" if is_stem else "bouquets"
    others = [o for o in PRODUCTS if o["kind"] == p["kind"] and o is not p]
    others.append(next(o for o in PRODUCTS if o["kind"] != p["kind"]))
    includes = "\n".join(f"              <li>{e(i)}</li>" for i in p["includes"])
    related = "\n".join(card(o) for o in others)
    title = f'{p["name"]} {"Stem" if is_stem else "Bouquet"} | Guwahati Flowers+'
    desc = f'{p["name"]} — {p["short"].lower()}. {p["lead"].split(". ")[0]}. Same-day delivery in Guwahati from Guwahati Flowers+.'

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta property="og:type" content="product">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(p["lead"])}">
  <meta property="og:image" content="../img/{p["img"]}">
  <meta name="theme-color" content="#7C8A6A">
  <link rel="icon" type="image/png" href="../img/logo.png">
  <link rel="apple-touch-icon" href="../img/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Gloock&family=Schibsted+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">
  <script>document.documentElement.classList.add('js');</script>
</head>
<body>
  <!-- Generated by tools/build_products.py — edit that script, not this file. -->
  <a class="skip-link" href="#main">Skip to content</a>

{header}

  <main id="main">
    <section class="product" aria-labelledby="product-title" data-name="{e(p["name"])}"{' data-kind="stem"' if is_stem else ''}>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="../index.html">Home</a></li>
            <li><a href="../index.html#{anchor}">{category}</a></li>
            <li aria-current="page">{e(p["name"])}</li>
          </ol>
        </nav>
        <div class="product__grid">
          <div class="product__media">
            <svg width="0" height="0" style="position:absolute" aria-hidden="true">{sprig}</svg>
            <svg class="product__sprig product__sprig--a" viewBox="0 0 119 188" aria-hidden="true"><use href="#lily-sprig"/></svg>
            <svg class="product__sprig product__sprig--b" viewBox="0 0 119 188" aria-hidden="true"><use href="#lily-sprig"/></svg>
            <div class="product__panel"></div>
            <img class="product__img" src="../img/{p["img"]}" alt="{e(p["alt"])}" width="{p["w"]}" height="{p["h"]}" fetchpriority="high">
          </div>
          <div class="product__info">
            <p class="product__eyebrow load-in" style="--i:0">{"Sold by the stem" if is_stem else "Signature bouquet"}</p>
            <h1 class="product__title load-in" style="--i:1" id="product-title">{e(p["name"])}</h1>
            <p class="product__price load-in" style="--i:2">₹ {p["price"]}{' <span>per stem</span>' if is_stem else ''}</p>
            <p class="product__lead load-in" style="--i:3">{e(p["lead"])}</p>
            <div class="product__includes load-in" style="--i:4">
              <h2>What's inside</h2>
              <ul>
{includes}
              </ul>
            </div>
            <div class="product__buy load-in" style="--i:5">
              <div class="qty" role="group" aria-label="Quantity">
                <button class="qty__btn" type="button" data-qty="-1" aria-label="Decrease quantity">−</button>
                <input class="qty__input" type="number" inputmode="numeric" min="1" max="99" value="1" aria-label="Number of {unit}">
                <button class="qty__btn" type="button" data-qty="1" aria-label="Increase quantity">+</button>
              </div>
              <button class="btn btn--sage btn--lg" type="button" data-add>Add to Cart</button>
              <a class="btn btn--outline btn--lg" data-buy target="_blank" rel="noopener" href="#">Buy Now</a>
            </div>
            <ul class="product__notes load-in" style="--i:6">
              <li>At your door by evening, across Guwahati</li>
              <li>Add a card message when you order on WhatsApp</li>
              <li>Questions? Call <a href="tel:+919101780136">91017 80136</a></li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section related" aria-labelledby="related-title">
      <div class="container">
        <h2 class="section__title reveal" id="related-title">You may also like</h2>
        <ul class="cards" role="list">
{related}
        </ul>
      </div>
    </section>

{cta}
  </main>

{footer}

  <div class="toast" role="status" aria-live="polite"></div>
  <script src="../js/main.js" defer></script>
</body>
</html>
'''


def main():
    index = (SITE / "index.html").read_text()
    header = relink(extract(index, '  <header class="site-header"', "</header>"))
    cta = relink(extract(index, '    <section class="cta"', "</section>"))
    footer = relink(extract(index, '  <footer class="footer">', "</footer>"))
    sprig = re.search(r'<symbol id="lily-sprig".*?</symbol>', index, re.S).group(0)

    OUT.mkdir(exist_ok=True)
    for p in PRODUCTS:
        (OUT / f'{p["slug"]}.html').write_text(page(p, header, cta, footer, sprig))
        print(f'products/{p["slug"]}.html')


if __name__ == "__main__":
    main()
