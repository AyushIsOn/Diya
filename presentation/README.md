# Internship report — presentation

**Present from the website.** `site/index.html` — open it in any browser, go full screen, and
use the arrow keys. Seven slides. No install, no server, no build step.

| What | Where |
|---|---|
| **The deck** (primary) | `site/index.html` — 7 slides, white and black over a blue Grainient background |
| **The deck as a PDF** | `Diya-Presentation.pdf` — 7 pages, 16:9, for handing out or presenting without a browser |
| **Real report screenshot** | drop one in at `site/shots/real-report.png` and slide 4 uses it automatically |
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

All the JavaScript and CSS is inlined into that one HTML file, so it works off a USB stick or
with no network. The `shots/`, `wf/`, `clips/` and `video/` folders next to it must travel
with it.

### Swapping in the real report

Slide 4 shows `site/shots/real-report.png` if that file exists, and falls back to the
representative `site/shots/app-04-report.png` if it does not. So to show a genuine report —
the posture and gaze analysis that the hardware team's `meditation-app` produces — just save
the screenshot to that path. No code change and no rebuild:

```bash
cp your-report-screenshot.png presentation/site/shots/real-report.png
```

Then regenerate the PDF if you hand that out too (see `site-src/README.md`).

## Running order

Seven slides. Roughly 8–10 minutes.

1. **Title** — Diya, presented by Ayush Gupta, under the guidance of Eshwar Teja
2. **What I worked on** — the kiosk app, phone identification, hardware integration, packaging
3. **The QR code system** — the inversion, with the scan footage playing large
4. **The whole flow** — identify → claim → session → report
5. **Two real problems** — no scanner, and integrating another team's `.deb` by watching for
   the report file instead of calling an API
6. **The full walkthrough** — the complete recorded run
7. **Thank you** — the learning, and thanks to Eshwar Teja and Kalyan Sir

Slide 3 is the strongest point in the project: there was no scanner, so the kiosk shows the
QR and the visitor's phone reads it. A constraint produced a simpler design.

## Presenting notes

- **Full screen** first (**⌃⌘F** on macOS, **F11** elsewhere).
- **Arrow keys**, **Space** or **Page Up/Down** move between slides; the dots on the right
  jump directly to one.
- The blue background is a WebGL shader, so it needs a current browser. If WebGL is
  unavailable the slides still read fine — they just lose the wash.
- The two clips on slide 3 autoplay muted on loop. The walkthrough on slide 6 has controls,
  so click it when you are ready.
- Printing (**⌘P**) produces the same seven 16:9 pages, without the background.
- A live demo of the phone-scanning-the-kiosk flow beats any slide here. If the hardware
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

Background from [React Bits](https://reactbits.dev) — Grainient. Earlier vendored components
from the same library are still in `site-src/src/reactbits/`. Fonts: Inter, JetBrains Mono.
Colours are taken from the kiosk app itself.
