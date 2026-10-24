# Guwahati Flowers+ — Landing Page Demo

Build a one-page demo website for **Guwahati Flowers+**, a premium florist in Christianbasti, Guwahati. The Figma exports in this folder are the source of truth for layout. Match them closely, and make the page responsive and lightly animated.

> Put this file in the root of the `Guwahati Flowers/` folder (next to `logo.PNG` and `assets/`) and run Claude Code from that folder. All paths below are relative to it.

---

## 1. Read the designs first

Before you write any code, open these images and study them:

| Purpose | Path |
|---|---|
| Full home page (all sections, top to bottom) | `home-page-figma-design-image.png` (6912×17972 — downscale it to view) |
| Hero | `assets/1. hero-section/Hero-Section-figma-design-image.png` |
| Featured Bouquets | `assets/2. Featured-bouquet-section/BOUQUETS-section-figma-design-image.png` |
| Fresh Flowers | `assets/4. Testimonials-Section/FRESH-FLOWERS-section-figma-design-image.png` ⚠️ the file is in the wrong folder, but it is the Fresh Flowers design |
| Testimonials | `assets/4. Testimonials-Section/TESTIMONIALS-section-figma-design-image.png` |
| CTA | `assets/5. Cta-section/CTA-section-figma-design-image.png` |
| Footer | `assets/6. Footer-section/FOOTER-section-figma-design-image.png` |

The `*-figma-design-image.png` files are **reference only**. Never ship them on the page.

---

## 2. Project setup

- Use static **HTML + CSS + vanilla JS** with no framework and no build step, so it deploys straight to Netlify or Vercel.
- Structure:

```
site/
  index.html
  css/styles.css
  js/main.js
  img/            ← optimised copies of the assets (see §3)
```

- Copy the assets into `site/img/` with **clean, kebab-case names**, because the source folders have spaces and numbers in their names. Convert every PNG to **WebP** at roughly 2× its displayed size (quality 82) and keep a PNG fallback only for the logo. Skip `.DS_Store`.

---

## 3. Asset map

| Source | Rename to | Used in |
|---|---|---|
| `logo.PNG` (16-bit, 759px — resize to 256px) | `img/logo.webp` + `img/logo.png` | Nav (40px circle), footer (150px circle), favicon |
| `assets/1. hero-section/bouquet-1.png` | `img/hero-bouquet-white.webp` | Hero, left/front bouquet (white wrap, pink ribbon) |
| `assets/1. hero-section/bouquet-2.png` | `img/hero-bouquet-kraft.webp` | Hero, right/back bouquet (kraft wrap) |
| `assets/1. hero-section/flower-bg-svg.svg` | `img/lily-sprig.svg` | Decorative lily silhouettes scattered in the hero. Inline it or use it as a mask so its fill can be set to `--sage` at ~60–80% opacity |
| `assets/2. Featured-bouquet-section/bouquet-1.png` | (same file as hero bouquet-1, so reuse it) | Card: Blush Lily |
| `assets/2. Featured-bouquet-section/bouquet-2.png` | (same file as hero bouquet-2, so reuse it) | Card: Kraft Romance |
| `assets/2. Featured-bouquet-section/bouquet-3.png` | `img/bouquet-garden-pastel.webp` | Card: Garden Pastel |
| `assets/2. Featured-bouquet-section/bouquet-4.png` | `img/bouquet-cloud-white.webp` | Card: Cloud White |
| `assets/3. Fresh-Flowers-Section/lily.png` | `img/stem-lily.webp` | Card: Oriental Lily |
| `assets/3. Fresh-Flowers-Section/rose.png` | `img/stem-rose.webp` | Card: White Rose |
| `assets/3. Fresh-Flowers-Section/sunflower.png` | `img/stem-sunflower.webp` | Card: Sunflower |
| `assets/3. Fresh-Flowers-Section/tulip.png` | `img/stem-tulip.webp` | Card: Pink Tulip |
| `assets/5. Cta-section/tulips.png` | `img/cta-tulips.webp` | CTA, bottom-left (mirror it with `scaleX(-1)` for bottom-right) |
| `assets/5. Cta-section/butterflies.png` | `img/cta-butterflies.webp` | CTA, floating above the tulips |

All product PNGs have transparent backgrounds. Place them directly on the sage card with no box or shadow.

---

## 4. Design tokens

```css
:root {
  /* Colour */
  --cream:      #ECE6DA;  /* brand cream — pill buttons on sage, text on sage */
  --paper:      #F1EDE6;  /* page background (sampled from the Figma export) */
  --sage:       #7C8A6A;  /* brand sage — cards, hero oval, footer, CTA pills */
  --sage-deep:  #5E6B4F;  /* hover/pressed state for sage; also for small text that must pass contrast */
  --ink:        #1F2A22;  /* headings and body text on paper */

  /* Type */
  --font-display: "Gloock", Georgia, serif;
  --font-body: "Schibsted Grotesk", system-ui, sans-serif;

  /* Motion */
  --ease: cubic-bezier(0.22, 1, 0.36, 1);       /* smooth ease-out, used everywhere */
  --ease-inout: cubic-bezier(0.65, 0, 0.35, 1); /* for looping float/sway only */
  --dur-fast: 240ms;
  --dur: 600ms;
  --dur-slow: 900ms;

  /* Shape */
  --radius-card: 32px;
  --radius-pill: 999px;
}
```

**Fonts** (Google Fonts):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Schibsted+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
```

- **Gloock** (400 only) is for all headings, card names and testimonial names. Section headings are UPPERCASE with tight tracking (`letter-spacing: -0.02em`), as in the designs.
- **Schibsted Grotesk** is for body text, nav, buttons and prices.
- The **two-tone hero heading** is in the design: alternate words are `--ink` and `--sage`. Wrap the sage words in `<span class="accent">`.

**Contrast note:** cream on sage measures about 3:1, which is fine for large text but too faint for small text. Keep card descriptions at 13px or larger, at weight 500. For solid sage buttons with cream labels, use `--sage-deep` on hover and focus.

**Type scale (desktop → mobile):** Hero H1 72→42px · Section H2 48→30px · Card name 22→18px · Body 18→16px · Button 16px · Small 13px.

---

## 5. Layout grid

| Breakpoint | Columns | Margin | Gutter | Section padding (top/bottom) |
|---|---|---|---|---|
| ≥1280 | 12 | 80px | 24px | 96px |
| 768–1279 | 8 | 32px | 20px | 72px |
| <768 | 4 | 16px | 12px | 56px |

The content container has `max-width: 1280px` and is centred. Use an 8px spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 40 / 64 / 80 / 120.

---

## 6. Sections and copy

Use this copy exactly. Anything in `[BRACKETS]` is a placeholder the client still needs to confirm, so leave it visible.

WhatsApp link: `https://wa.me/919101780136` · Phone: `tel:+919101780136`

### 6.1 Nav (sticky, paper background, gains a 1px sage hairline after 8px of scroll)
- Left: logo in a 40px circle
- Centre links: Home · Fresh Cut Flowers · Bouquets (anchor-scroll to the sections)
- Right: sage pill button **Order on WhatsApp**, plus a small cart count badge (see 6.3)
- Mobile: logo + hamburger. The menu slides down as a full-width paper panel.

### 6.2 Hero
- Left column (spans columns 1–5):
  - H1: **FRESH** <span class="accent">**BLOOMS,**</span> **RIGHT TO YOUR** <span class="accent">**DOOR.**</span> (match the two-tone split in the hero design)
  - Body: Premium bouquets for every moment, at your door by evening.
  - Button: **Shop Now** (sage pill, cream text) → scrolls to Featured Bouquets
- Right column (spans columns 7–12): a tall sage **oval/stadium shape** (`border-radius: 999px`, about 3:4 ratio) with the two hero bouquets overlapping it. The kraft bouquet sits behind and to the right, and the white bouquet sits in front and to the left. Both bouquets overflow the oval's top and side edges, as in the design.
- Decorative lily sprigs (`lily-sprig.svg`) are absolutely positioned around the hero at varied sizes and rotations, matching the design. They are `aria-hidden="true"`.
- Mobile: the image block stacks above the text.

### 6.3 Featured Bouquets (`id="bouquets"`)
- H2: **FEATURED BOUQUETS** (the Figma design misspells it as "FEAUTRED", so fix the spelling)
- 4 cards in a row (2 per row on tablet, 2 per row on mobile with smaller cards). Each card has a `--sage` background, `--radius-card` corners, the product image centred at the top, and the following beneath it:
  - Name (Gloock, cream) on the left and price on the right
  - A one-line description (small, cream)
  - Two cream pills: **Add to Cart** · **Buy Now** (sage text)

| Name | Description | Price | Image |
|---|---|---|---|
| Blush Lily | Pink lilies, roses & baby's breath | ₹ [PRICE] | hero-bouquet-white |
| Kraft Romance | Lilies wrapped in kraft paper | ₹ [PRICE] | hero-bouquet-kraft |
| Garden Pastel | Mixed seasonal blooms | ₹ [PRICE] | bouquet-garden-pastel |
| Cloud White | Whites in a soft blue wrap | ₹ [PRICE] | bouquet-cloud-white |

- **Buy Now** opens WhatsApp with a prefilled message: `Hi! I'd like to order the {Name} bouquet.` (URL-encode it and use `?text=`).
- **Add to Cart** is a demo only. It increments the nav cart badge with a small pop animation and shows a toast reading "Added {Name}". It has no real checkout.
- Below the grid: sage pill **View All Bouquets**

### 6.4 Fresh Flowers (`id="fresh"`)
- H2: **FRESH FLOWERS**
- The cards are identical in structure to 6.3.

| Name | Description | Price | Image |
|---|---|---|---|
| Oriental Lily | Sold by the stem | ₹ [PRICE] | stem-lily |
| White Rose | Sold by the stem | ₹ [PRICE] | stem-rose |
| Sunflower | Sold by the stem | ₹ [PRICE] | stem-sunflower |
| Pink Tulip | Sold by the stem | ₹ [PRICE] | stem-tulip |

- Below the grid: **View All Flowers**

### 6.5 Testimonials
- H2: **WORDS FROM OUR LOVED CUSTOMERS**
- A **coverflow carousel** with 5 visible cards. The centre card is the largest, the next two are slightly smaller, and the outer two are the smallest. Each card has a sage background and is centre-aligned, holding a circular avatar placeholder, a name (Gloock), a 2–4 line quote and ★★★★★, as in the design.
- Behaviour: autoplay every 5s, pause on hover or focus, prev/next buttons (with `aria-label`), swipe on touch, and keyboard arrows. Transitions scale and opacity with `--ease` over `--dur`.
- Mobile: one card at full width with the next card peeking, and scroll-snap.
- **Content:** do NOT invent reviews. Use clearly marked placeholders such as `[CUSTOMER NAME]` / `[Real review from Google or Instagram]`. The client will supply real ones.

### 6.6 CTA
- Centred:
  - H2: **SAY IT WITH FLOWERS TODAY.**
  - Body: Order on WhatsApp — we'll handle the rest.
  - Button: **Order on WhatsApp** (sage pill) → WhatsApp link
- `cta-tulips` sits bottom-left and a mirrored copy sits bottom-right, both anchored to the section's bottom edge. `cta-butterflies` floats above each cluster. On mobile, shrink both to about 40% and keep them behind the text with lower opacity.

### 6.7 Footer
- A sage panel with a large top radius (about 40px), as in the design.
- Columns:
  1. Logo in a 150px circle, with the tagline beneath: *Premium flowers, door-step delivery.*
  2. Links: Home · Fresh Cut Flowers · Bouquets
  3. Social: Instagram (`https://instagram.com/guwahati_flowers`) · WhatsApp · Facebook (`[FACEBOOK URL]`)
  4. The **white card** from the design becomes a "Visit the studio" card:
     - **Visit the studio** (Gloock)
     - Christianbasti, near Zudio Mall, Guwahati
     - 91017 80136 (tel link)
     - Open [HOURS]
     - Text link: Get directions → (Google Maps search URL for "Guwahati Flowers+ Christianbasti")
- Bottom line: © 2026 Guwahati Flowers+. All rights reserved.
- Mobile: the columns stack and the white card goes full width.

---

## 7. Animation — subtle, smooth, never bouncy

Every transition uses `--ease` (`cubic-bezier(0.22, 1, 0.36, 1)`). Nothing should overshoot or spring.

1. **Page load (hero only, staggered):**
   - The heading lines rise 24px and fade in, 80ms apart
   - Then the body and button follow
   - The sage oval scales from 0.92 to 1 and fades in
   - The two bouquets rise 40px with a 120ms offset between them
   - Total time is under 1.2s.
2. **Scroll reveal:** an `IntersectionObserver` (threshold 0.15) adds `.is-visible`, which moves elements from `opacity 0; translateY(24px)` to their resting state over `--dur`. Cards in a grid stagger 70ms apart. Each element reveals once, then gets unobserved.
3. **Idle float:** the hero bouquets float ±6px vertically on a 6s `--ease-inout` infinite alternate loop, and the two bouquets are out of phase with each other. The lily sprigs sway ±3° around their base (`transform-origin: bottom center`) on a 7–9s loop. The CTA butterflies drift ±8px.
4. **Hover (pointer devices only, `@media (hover: hover)`):**
   - Cards lift 6px and their product image scales to 1.04 over `--dur-fast`.
   - Pill buttons switch to `--sage-deep` (or to white on cream pills) with a 2px lift.
   - Nav links get an underline that grows from the left.
5. **Cart badge:** scales 1 → 1.25 → 1 over 300ms when an item is added.
6. **Parallax (optional, light):** the hero oval moves at 0.9× scroll speed. Use `transform` only and throttle with `requestAnimationFrame`.
7. **Reduced motion:** under `@media (prefers-reduced-motion: reduce)`, turn off the float, sway, parallax and autoplay, and make reveals instant.

Animate only `transform` and `opacity`, never layout properties.

---

## 8. Quality bar

- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section aria-labelledby>`, `<footer>`. Use real `<button>` and `<a>` elements.
- Alt text on every product image (e.g. "Blush Lily bouquet — pink lilies and roses in white wrap"). Decorative images get `alt=""`.
- Visible focus rings: a 2px `--ink` outline with a 3px offset.
- Touch targets of at least 44px.
- Every image except the hero gets `loading="lazy"`. Hero images get `fetchpriority="high"`. Set `width`/`height` on all images to avoid layout shift.
- Meta: a title ("Guwahati Flowers+ | Premium Bouquets, Door-Step Delivery in Guwahati"), a description, OG tags, and the logo as favicon.
- Check the layout at 1440, 1280, 768 and 390 widths. There must be no horizontal scroll at any width.
- When you finish, list every `[PLACEHOLDER]` still on the page so the team knows what to collect from the client.
