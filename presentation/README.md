# Internship report — presentation

**Present from the website.** `site/index.html` — open it in any browser, full screen, and
scroll. No install, no server, no build step.

| What | Where |
|---|---|
| **The site** (primary) | `site/index.html` |
| **The site as a PDF** | `Diya-Presentation.pdf` — 22 pages, 16:9, for handing out or presenting without a browser |
| **Your demo video** | drop it at `site/video/demo.mp4` — see `site/video/README.md` |
| Source, to edit or rebuild | `site-src/` — see its README |
| Slide deck (older, still valid) | `Diya-Internship-Report.pdf` / `.pptx` |
| Raw screenshots, diagrams, wireframes | `assets/` |

## The footage

Cut from a real recorded run, and committed — the files are small enough:

| File | What | Size |
|---|---|---|
| `site/clips/scan-phone.mp4` | The scan itself, rotated upright. Autoplays muted on loop. | 1.4 MB |
| `site/clips/kiosk-authed.mp4` | The kiosk responding. Autoplays muted on loop. | 0.4 MB |
| `site/video/demo.mp4` | Full walkthrough, with controls. | 4.9 MB |
| `assets/video-stills/` | Four stills at the key beats. | — |

The source clip mixed orientations — the phone close-ups were portrait-in-landscape while
the laptop shots were already upright — so the phone segment is rotated 90° and the kiosk
segment is not. That is why they are two clips rather than one.

`site/video/.gitignore` still blocks anything else dropped in there, so an unprocessed
recording can't be committed by accident. `site/video/README.md` has the ffmpeg commands if
you want to recut.

### Three things to check before you present

1. **Real personal data is on screen.** The footage shows a real name, a legible Gmail
   address, and a face photo. Fine if that person consents; worth a moment's thought if the
   recording will be shared beyond the room.
2. **The video shows an older build.** It says *Start Calibration* and *Registered! Welcome*,
   whereas the current code has a *Start* button and says *Authenticated! Welcome*. The
   screenshots elsewhere are from the current build, so the copy differs slightly between
   them. Nobody is likely to notice, but you should know before someone asks.
3. **It was demoed on Windows.** A taskbar was visible in the original, so the kiosk clip is
   cropped to the app area. The project targets Ubuntu — if asked, Avalonia is cross-platform
   and this was just the convenient dev machine.

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
