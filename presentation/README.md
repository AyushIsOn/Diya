# Internship report deck

`Diya-Internship-Report.pptx` — 10 slides, 16:9. Every slide has **speaker notes**
(what to say, and likely questions with answers). Open the notes pane in PowerPoint
with *View → Notes*, or in Google Slides with *View → Show speaker notes*.

## Fill in before presenting

Slide 1 only: `[Your Name]`, `[Institution]`, `[Month Year – Month Year]`, `[Mentor Name]`.

## Visuals to drop in

`assets/` holds diagrams and real kiosk screenshots, with provenance notes in
`assets/README.md`. They are **not yet embedded in the .pptx** — add them where they help:

| Asset | Suggested slide |
|---|---|
| `diagram-timeline-slide.png` | Slide 5 (*How a Visitor Actually Logs In*) — sized for projection |
| `diagram-timeline.png` | Print as a handout; too fine-grained to project |
| `app-01-idle-qr.png` | Slide 4 (*Invert the QR*) — the kiosk showing its own QR |
| `app-02-authenticated.png` | Slide 5 — visitor name and roster photo resolved |
| `app-03-session-running.png` | Slide 7 (*Building It Without the Hardware*) |
| `app-04-report.png` | Slide 9 (*Where I Left It*) — the report rendered in-app |

## If you need it shorter

For a 10-minute slot, cut to 7 slides by deleting **3 (Architecture)** and **8 (Packaging)**,
and merging **10** into **9**. The argument still holds: problem → the QR decision →
how login works → hard bugs → testing → state and takeaways.

## Suggested timing

| Slides | Content | Minutes |
|---|---|---|
| 1–3 | Framing and architecture | 3 |
| 4–5 | The design decision and the flow | 4 |
| 6–7 | Debugging and testing | 4 |
| 8–10 | Shipping, state, takeaways | 3 |

Slide 4 is the strongest one — give it the most time. Slide 9 (known limitations) reads as
confidence, not weakness; don't rush or apologise through it.

## Worth having open in another tab

A live demo of the phone-scans-kiosk flow lands better than any slide. If the hardware
isn't available, the `testkit/` mock runs the whole flow on any Linux desktop — see
`testkit/README.md`.

## Regenerating

Built with [python-pptx](https://python-pptx.readthedocs.io/). Edit directly in PowerPoint;
the generator script isn't committed, since the deck is meant to be hand-tuned from here.
