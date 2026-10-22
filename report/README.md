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

- Fill in the two yellow-highlighted fields: the **subject code** (cover page) and your
  **faculty guide's name** (Acknowledgments).
- Replace the six **PLACE PHOTOGRAPH HERE** boxes in Section 4.2 (Figures 9–14) with photos of the
  apparatus. In Word: click inside the box, select the table, delete it, insert the photo. Keep the
  caption below it.
- If adding photos moves pages, update the page numbers in the Contents, List of Figures and List
  of Tables tables (they are ordinary tables, not Word fields) — or ask for a rebuild.

## Rebuilding

Requires Python (`python-docx`, `Pillow`, `pypdfium2`, `matplotlib`) and LibreOffice:

```bash
python src/diagrams.py                       # regenerate figures/
SOFFICE=soffice python src/render_muj.py     # rebuild DOCX + PDF, page numbers filled automatically
```
