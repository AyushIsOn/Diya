"""Build the internship report as PDF and DOCX.

    python build.py            # writes ../Diya-Internship-Report.pdf and .docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from content import build                      # noqa: E402
from model import ROOT                          # noqa: E402
import render_docx                              # noqa: E402
import render_pdf                               # noqa: E402

if __name__ == "__main__":
    report = build()
    pdf = os.path.join(ROOT, "Diya-Internship-Report.pdf")
    docx = os.path.join(ROOT, "Diya-Internship-Report.docx")
    entries = render_pdf.render(report, pdf)
    render_docx.render(report, docx, entries)
