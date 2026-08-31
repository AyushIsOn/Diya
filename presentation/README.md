# Internship report — presentation

**Present from the website.** `site/index.html` — open it in any browser, full screen, and
scroll. No install, no server, no build step.

| What | Where |
|---|---|
| **The site** (primary) | `site/index.html` |
| Source, to edit or rebuild | `site-src/` — see its README |
| Slide deck (older, still valid) | `Diya-Internship-Report.pdf` / `.pptx` |
| Raw screenshots, diagrams, wireframes | `assets/` |

Everything is inlined into that one HTML file, so it works off a USB stick or with no
network. The `shots/` and `wf/` folders next to it must travel with it.

Placeholders to fill are in the hero only: `[Your Name]`, `[Institution]`,
`[Month Year – Month Year]`, `[Mentor Name]` — edit `site-src/src/App.jsx` and rebuild,
or edit the text directly in `site/index.html` if you only need the names.

## Running order

13 sections, scroll-driven. Roughly 12–15 minutes.

1. **Hero** — one sentence on what Diya is
2. **The brief** — four constraints that ruled things out
3. **Scope** — what you owned vs the hardware team
4. **The problem** — identify someone with no scanner
5. **Three attempts** — you iterated
6. **The inversion** — *give this the most time*
7. **Four stages** — architecture + the API / not-API boundary
8. **Wireframes** — design process, with two flaws marked honestly
9. **Every screen** — real captures, kiosk and web
10. **Architecture** — stack reference
11. **Testing** — building without hardware
12. **Shipping** — packaging, lockdown, deployment
13. **Handover** — what's queued next

Section 6 is the strongest thing in the project: no scanner hardware → three attempts →
invert the QR so the phone reads the kiosk. A constraint produced a simpler design.

The dots on the right jump between sections — useful if a question sends you backwards.

## Presenting notes

- **Full screen** (F11) hides the browser chrome. The Aurora hero needs WebGL; any modern
  browser is fine.
- The wireframes section marks two defects as *known flaws* rather than hiding them. That
  reads as judgement, not weakness — don't apologise through it.
- A live demo of the phone-scanning-the-kiosk flow beats any section here. If the hardware
  isn't available, `testkit/` runs the whole flow on any Linux desktop.

## Honesty notes

Worth knowing before someone asks:

- Screenshots are genuine frames from the running app and the live web pages.
- **The report PDF shown is representative.** The real one comes from the hardware team's
  `meditation-app`, which isn't in this repo. The rendering is real; the numbers are not.
- The backend was a local stub during capture, returning the same JSON shapes.
- The visitor is fictional and the avatar is generated. No real person's data appears.

Full provenance is in `assets/README.md`.

## Credits

Animated components from [React Bits](https://reactbits.dev) — Aurora, SplitText, CountUp,
SpotlightCard, TiltedCard, ScrollReveal, GradientText. Fonts: Inter, JetBrains Mono.
