# portfolio-website-astro

Astro rebuild of walkswithgiants.com. Two-tier portfolio: thin landing page
(digital business card) + per-role pages (unlisted).

## Status

🚧 **Landing page in progress.** Circuit background content locked; animation
effects pending. Role pages pending.

Landing page has a three-card deck (Identity / Timeline / Certifications) with
a circuit board background and a hero cutout. Mobile hides the hero and centers
card. Background uses decoded PCB trace data from the reference video.

## Stack

- **Astro 7** — static site generation, content collections
- **Tailwind v4** — via `@tailwindcss/vite`
- **No JS framework** — vanilla `<script>` for the card-deck nav
- **Schema-validated content** — Zod schemas in `src/content.config.ts`

## Structure

```
portfolio-website-astro/
├── astro.config.mjs         # Tailwind v4 plugin
├── tsconfig.json
├── package.json
├── scripts/
│   ├── generate_bg.py       # circuit pattern generator + blob removal
│   └── vision.py            # gemma4 vision verification helper
├── public/
│   ├── favicon.svg
│   └── images/
│       ├── bg-circuit.png   # circuit bg (black traces on gray, blob-free)
│       └── raul-best-3.png  # hero cutout (BiRefNet, head-to-waist)
└── src/
    ├── content.config.ts    # Zod schemas (landing + roles collections)
    ├── content/
    │   └── landing.json     # landing page content
    ├── layouts/
    │   └── BaseLayout.astro # head, meta, OG, robots, bg-circuit (CSS inline)
    ├── components/
    │   ├── Contact.astro
    │   └── icons/           # Email, GitHub, Phone SVGs
    └── pages/
        └── index.astro      # landing page (3-card deck + hero + navbar)
```

## Develop

```sh
npm install      # first time
npm run dev      # dev server at http://localhost:4321/
npm run build    # static output to dist/
```

## Background

The circuit pattern is decoded from 1-bit-per-pixel packed bitmaps extracted
from the reference illumination video. The OVERALL scene provides the full-frame
traces; the FIRST scene adds genuinely-new detail to the left side (filtered to
remove offset ghosting). Solid blobs are removed via a local density filter
(15×15 window, 50% threshold). Right side is extended via mirroring. The final
image is anti-aliased at 4× upscale with balanced blur + sharpen.

## Pending

- Breathing/glow illumination animation on locked circuit content
- Seed 17 role JSON files from cached Postgres data
- Build `[role].astro` dynamic route + role page template
- Write design doc to `docs/specs/`
- `netlify.toml` for deploy
