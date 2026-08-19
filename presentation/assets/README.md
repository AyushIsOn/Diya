# Presentation assets

## Diagrams

| File | Use |
|---|---|
| `diagram-timeline-slide.png` | **For the slide.** 7 grouped events across 4 lanes, left-to-right. Type is large enough to project. |
| `diagram-timeline.png` | **For the handout / appendix.** All 19 steps with exact endpoints. Too fine to project — print it or share the PDF. |

Both show the same thing: the kiosk and the backend talk over one REST API, while the
hardware team's `meditation-app` is reached *without* one — a local process plus a PDF on
disk. That distinction is the point of the legend, and it's the strongest architectural
claim in the project.

Source: `.build/timeline.html` and `.build/timeline-slide.html` (outside the repo). They
render as SVG in a browser and are captured with Playwright at 2× device scale.

## Kiosk screenshots

| File | State |
|---|---|
| `app-01-idle-qr.png` | Idle — session created, QR rendered, waiting for a phone |
| `app-02-authenticated.png` | Claimed — visitor name, email, age and roster photo |
| `app-03-session-running.png` | Pipeline running — live status line from the script's stdout |
| `app-04-report.png` | Report overlay — PDF pages rendered in-app, personalised thank-you |

**These are genuine frames from the real application**, not mockups. `HomeView` was rendered
through Avalonia's headless platform with the Skia backend and captured with
`CaptureRenderedFrame()` — the same layout, fonts, and QR encoder that run on the kiosk.
The QR is real output from QRCoder; the report really is decoded by PDFium.

Two things were stood in for, and it's worth being straight about them if asked:

- **The backend** was a local stub returning the same JSON shapes as the real API, so the
  screenshots didn't depend on the hosted service being awake.
- **The report PDF** is representative. The real one is produced by the hardware team's
  `meditation-app`, which isn't in this repo, so a stand-in with the same structure
  (score, calmness/focus/heart-rate, trend, message) was generated for the capture.
  The *rendering* is real; the *numbers* are illustrative.

The visitor is fictional and the avatar is a generated silhouette — no real person's
name, photo, or ID appears anywhere in these assets.
