# Internship report (Manipal University Jaipur format)

| File | What |
|---|---|
| `Diya-Internship-Report.docx` | The report, built on the college template |
| `Diya-Internship-Report.pdf` | The same document converted to PDF (page for page) |
| `template/MUJ-format.docx` | The college format file the report is built on |
| `figures/`, `images/` | Diagrams, screenshots, wireframes, demo stills, the IITH certificate scan |
| `src/` | `content_muj.py` holds the text; `render_muj.py` builds both files |

The cover page (MUJ logo and layout), styles, page size and margins come straight from
`template/MUJ-format.docx`. The chapters and the Contents table follow the template's structure:
Introduction, Background Material, Methodology, Implementation, Results and Analysis,
Conclusions & Future Scope, References, Annexures.

## Before submitting

Nothing is left to fill in. If you edit pages in Word and they move, update the page numbers in the
Contents, List of Figures and List of Tables tables (they are ordinary tables, as in the template),
or rebuild with the command below.

## Rebuilding

Requires Python (`python-docx`, `Pillow`, `pypdfium2`, `matplotlib`) and LibreOffice:

```bash
python src/diagrams.py                       # regenerate figures/
SOFFICE=soffice python src/render_muj.py     # rebuild DOCX + PDF, page numbers filled automatically
```
