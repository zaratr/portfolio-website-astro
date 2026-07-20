# portfolio-website-astro

Astro rebuild of walkswithgiants.com. Two-tier portfolio: thin landing page
(digital business card) + per-role pages (unlisted).

## Status

🚧 **Landing page complete; role pages pending.**

Landing page is a three-card deck (Identity / Timeline / Certifications) with
a video background and a hero cutout. Mobile hides the hero and centers card.

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
├── public/
│   ├── favicon.svg
│   └── images/
│       ├── bg-illumination.mp4   # background video (loops, autoplay muted)
│       ├── bg-circuit-dark.jpg   # reduced-motion fallback bg
│       └── raul-best-3.png       # hero cutout (BiRefNet, head-to-waist)
└── src/
    ├── content.config.ts     # Zod schemas for landing + roles collections
    ├── content/
    │   └── landing.json      # landing page content
    ├── styles/
    │   └── global.css        # Tailwind import + design tokens + bg video
    ├── layouts/
    │   └── BaseLayout.astro  # head, meta, OG, robots, bg-video
    ├── components/
    │   ├── Contact.astro     # contact icon row
    │   └── icons/            # Email, GitHub, Phone SVGs
    └── pages/
        └── index.astro       # landing page (3-card deck + hero + navbar)
```

## Develop

```sh
npm install      # first time
npm run dev      # dev server at http://localhost:4321/
npm run build    # static output to dist/
npm run preview  # serve the production build locally
```

## Architecture notes

- **Landing page** is the only public/indexed route. Three cards swap via
  prev/next/dots nav; only one card visible at a time.
- **Background video** plays the reference illumination animation directly
  (CSS couldn't reproduce its internal motion). Muted + playsinline + loop
  for autoplay compliance. Hidden + replaced by static image when user has
  `prefers-reduced-motion: reduce`.
- **Hero cutout** is hidden below 900px viewport width — true left/right
  layout doesn't fit on phone screens, so card shows alone centered.
- **Card text** entrance animations fade in over ~1.5s on load. If you're
  debugging with a backgrounded CDP browser, these will appear stuck at
  opacity 0 — focus the tab to see them play.

## Pending (post-checkpoint)

- Seed 17 role JSON files from cached Postgres data
- Build `[role].astro` dynamic route + role page template
- Rich vs stub rendering per role
- Write design doc to `docs/specs/`
- `netlify.toml` for deploy
