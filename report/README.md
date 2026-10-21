# Internship report

| File | What |
|---|---|
| `Diya-Internship-Report.pdf` | The report, ready to print (A4, 52 pages) |
| `Diya-Internship-Report.docx` | The same report in Word, for editing |
| `figures/` | Diagrams generated for the report |
| `images/` | Screenshots, wireframes and demo stills used in the report |
| `src/` | Source: `content.py` holds all the text; `build.py` produces both files |

## Before submitting

Fill in everything shown with a **yellow highlight** (`[...]`): registration number, faculty
guide, campus, date and place.

Replace these placeholders:
- **Certificate page:** the scanned IIT Hyderabad certificate.
- **Title page:** the university logo.
- **Figures 4.2–4.7:** photographs of the apparatus. In Word, click the dashed box, delete it,
  and insert the photo. The captions stay as they are.

When Word asks to update fields on opening, choose **Yes**, so the contents, figures and tables
lists pick up the final page numbers. If it doesn't ask, right-click the contents list and choose
**Update Field → Update entire table**.

## Rebuilding

```bash
pip install python-docx reportlab matplotlib Pillow
python src/diagrams.py    # regenerate figures/
python src/build.py       # regenerate the PDF and DOCX
```

Fonts: the PDF uses Liberation Serif and Liberation Mono (in `fonts/`, SIL Open Font License),
which have the same metrics as Times New Roman. The DOCX uses Times New Roman.
