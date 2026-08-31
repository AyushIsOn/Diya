# Presentation site — source

React + Vite. The built output lives in `../site/` and is what you actually present.

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # writes dist/ — copy it to ../site/
```

## Structure

- `src/App.jsx` — every section, in order. Edit text here.
- `src/index.css` — the whole design system (colours, type scale, cards, layout).
- `src/reactbits/` — components pulled from [React Bits](https://reactbits.dev),
  unmodified. Aurora, SplitText, CountUp, SpotlightCard, TiltedCard, ScrollReveal,
  GradientText.

## Two things to know if you change the build

`vite.config.js` sets `base: './'` and uses `vite-plugin-singlefile`, which inlines all
JS and CSS into one `index.html`. Both are deliberate: ES modules loaded over `file://`
are blocked by CORS, so without inlining the page renders blank when opened off disk.
Keep them unless you're only ever serving over HTTP.

Image paths are **relative** (`shots/…`, not `/shots/…`) for the same reason. A leading
slash resolves to the filesystem root under `file://` and the images vanish.

## Fill in

Placeholders are in the hero block of `src/App.jsx`: `[Your Name]`, `[Institution]`,
`[Month Year – Month Year]`, `[Mentor Name]`.
