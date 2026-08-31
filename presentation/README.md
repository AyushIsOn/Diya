# Internship report deck

**14 slides, 16:9.** Two formats — both identical:

- `Diya-Internship-Report.pdf` — use this to present. Nothing to install, fonts can't shift.
- `Diya-Internship-Report.pptx` — same slides, plus **speaker notes on all 14** (*View → Notes*).

Fill in slide 1: `[Your Name]`, `[Institution]`, `[Month Year – Month Year]`, `[Mentor Name]`.

## How it's built

The slides are designed in HTML/CSS (`assets/deck-source.html`), rendered at 1920×1080 with
Playwright, and placed full-bleed into the `.pptx`. That's why they look designed rather than
like default PowerPoint — but it also means **the text isn't editable in PowerPoint.**

To change wording: edit `assets/deck-source.html`, re-render, re-assemble. To change only
slide 1's placeholders, editing the HTML is still the fastest route.

If you'd rather have editable text and accept a plainer look, say so — it's a different build.

## The arc

| # | Slide | Job |
|---|---|---|
| 1 | Diya | Cover |
| 2 | A visitor walks up | The brief, as four constraints |
| 3 | Two teams, one thin seam | Scope — what you owned |
| 4 | How do you identify someone? | The central question |
| 5 | Three attempts | You iterated |
| 6 | **The phone is the scanner** | **The hero slide** |
| 7 | Four stages, one API | Architecture + the API / not-API boundary |
| 8 | The whole flow, on screen | Real screenshots |
| 9 | Three parts I built | Stack reference |
| 10 | Three that cost me days | Debugging depth |
| 11 | Building it without the hardware | Testability |
| 12 | One command each | Packaging, deployment, docs |
| 13 | Where I handed it over | Future work |
| 14 | Someone can walk up… | Close |

## Timing

Roughly 12–14 minutes at a comfortable pace. **Give slide 6 the most time** — it's the
strongest thing in the project, because the design got simpler under a constraint.

For a 10-minute slot, cut 9 and 12.

Slide 13 reads as confidence, not weakness. Don't rush or apologise through it.

## Worth having ready

A live demo of the phone-scanning-the-kiosk flow beats any slide. If the hardware isn't
available, `testkit/` runs the whole flow on any Linux desktop — see `testkit/README.md`.

## Assets

`assets/` holds the screenshots, diagrams, rendered slide PNGs and the HTML source.
Provenance — including the two things that were stood in for — is in `assets/README.md`.
