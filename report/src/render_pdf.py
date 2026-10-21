"""PDF renderer (ReportLab). Multi-pass so the contents pages carry real page numbers."""
import os
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import PageBreakIfNotEmpty
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

from model import ROOT, nice_title, runs

FONT_DIR = os.path.join(ROOT, "fonts")
pdfmetrics.registerFont(TTFont("Serif", os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Bold", os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Italic", os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", os.path.join(FONT_DIR, "LiberationSerif-BoldItalic.ttf")))
pdfmetrics.registerFont(TTFont("Mono", os.path.join(FONT_DIR, "LiberationMono-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Mono-Bold", os.path.join(FONT_DIR, "LiberationMono-Bold.ttf")))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-Italic",
                              boldItalic="Serif-BoldItalic")

PAGE_W, PAGE_H = A4
M_LEFT, M_RIGHT, M_TOP, M_BOTTOM = 1.25 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch
TEXT_W = PAGE_W - M_LEFT - M_RIGHT
GREY = colors.HexColor("#6B7280")
LIGHT = colors.HexColor("#F3F4F6")
FILL_BG = "#FFF3B0"

S = {
    "body": ParagraphStyle("body", fontName="Serif", fontSize=12, leading=18, alignment=TA_JUSTIFY,
                           spaceAfter=8),
    "left": ParagraphStyle("left", fontName="Serif", fontSize=12, leading=18, alignment=TA_LEFT, spaceAfter=8),
    "bullet": ParagraphStyle("bullet", fontName="Serif", fontSize=12, leading=18, alignment=TA_JUSTIFY,
                             leftIndent=0.35 * inch, bulletIndent=0.1 * inch, spaceAfter=4),
    "chap_label": ParagraphStyle("cl", fontName="Serif-Bold", fontSize=16, leading=20, alignment=TA_CENTER,
                                 spaceAfter=6),
    "chap_title": ParagraphStyle("ct", fontName="Serif-Bold", fontSize=18, leading=24, alignment=TA_CENTER,
                                 spaceAfter=26),
    "section": ParagraphStyle("sec", fontName="Serif-Bold", fontSize=14, leading=18, spaceBefore=12,
                              spaceAfter=8, keepWithNext=1),
    "sub": ParagraphStyle("sub", fontName="Serif-Bold", fontSize=12, leading=16, spaceBefore=8, spaceAfter=6,
                          keepWithNext=1),
    "caption": ParagraphStyle("cap", fontName="Serif", fontSize=11, leading=14, alignment=TA_CENTER,
                              spaceBefore=4, spaceAfter=14),
    "tcaption": ParagraphStyle("tcap", fontName="Serif", fontSize=11, leading=14, alignment=TA_CENTER,
                               spaceBefore=6, spaceAfter=6, keepWithNext=1),
    "cell": ParagraphStyle("cell", fontName="Serif", fontSize=10.5, leading=13, alignment=TA_LEFT),
    "cellh": ParagraphStyle("cellh", fontName="Serif-Bold", fontSize=10.5, leading=13, alignment=TA_LEFT),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=9, leading=12),
    "toc_head": ParagraphStyle("th", fontName="Serif-Bold", fontSize=18, leading=24, alignment=TA_CENTER,
                               spaceAfter=20),
    "ref": ParagraphStyle("ref", fontName="Serif", fontSize=11.5, leading=16, alignment=TA_LEFT,
                          leftIndent=0.4 * inch, firstLineIndent=-0.4 * inch, spaceAfter=6),
    "sublabel": ParagraphStyle("sl", fontName="Serif", fontSize=10, leading=12, alignment=TA_CENTER),
}


def md(text):
    """Inline markup -> ReportLab paragraph XML."""
    out = []
    for seg, style in runs(text):
        s = escape(seg)
        if style == "bold":
            out.append(f"<b>{s}</b>")
        elif style == "italic":
            out.append(f"<i>{s}</i>")
        elif style == "code":
            out.append(f'<font name="Mono" size="10">{s}</font>')
        elif style == "fill":
            out.append(f'<font backColor="{FILL_BG}">{s}</font>')
        else:
            out.append(s)
    return "".join(out)


def roman(n):
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


# ------------------------------------------------------------------ flowables
class Mark(Flowable):
    """Zero-size flowable that records an entry (TOC / LoF / LoT / outline) where it lands."""

    def __init__(self, kind, text, level=0, main_start=False):
        super().__init__()
        self.kind, self.text, self.level, self.main_start = kind, text, level, main_start
        self.width = self.height = 0

    def draw(self):
        pass


class Placeholder(Flowable):
    def __init__(self, height, title, hint):
        super().__init__()
        self.w, self.h, self.title, self.hint = TEXT_W * 0.92, height * inch, title, hint

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(colors.HexColor("#FAFAFA"))
        c.setStrokeColor(colors.HexColor("#9CA3AF"))
        c.setDash(5, 4)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, self.w, self.h, 8, stroke=1, fill=1)
        c.setDash()
        c.setFillColor(colors.HexColor("#4B5563"))
        c.setFont("Serif-Bold", 13)
        c.drawCentredString(self.w / 2, self.h / 2 + 14, self.title)
        c.setFont("Serif-Italic", 10.5)
        lines = simpleSplit(self.hint, "Serif-Italic", 10.5, self.w - 60)
        y = self.h / 2 - 6
        for ln in lines:
            c.drawCentredString(self.w / 2, y, ln)
            y -= 14
        c.restoreState()


class TocRow(Flowable):
    """One contents line with dot leaders and an internal link."""

    def __init__(self, text, page, key, indent=0, bold=False, size=12):
        super().__init__()
        self.text, self.page, self.key, self.indent, self.bold, self.size = text, page, key, indent, bold, size
        self.font = "Serif-Bold" if bold else "Serif"

    def wrap(self, aw, ah):
        self.aw = aw
        self.lines = simpleSplit(self.text, self.font, self.size, aw - self.indent - 50)
        self.lh = self.size * 1.45
        self.h = self.lh * len(self.lines) + 3
        return aw, self.h

    def draw(self):
        c = self.canv
        c.setFont(self.font, self.size)
        y = self.h - self.size
        for i, ln in enumerate(self.lines):
            c.drawString(self.indent, y, ln)
            if i == len(self.lines) - 1:
                end = self.indent + c.stringWidth(ln, self.font, self.size) + 4
                pw = c.stringWidth(self.page, self.font, self.size)
                c.setFont("Serif", self.size)
                dot_w = c.stringWidth(". ", "Serif", self.size)
                x = end
                while x + dot_w < self.aw - pw - 6:
                    c.drawString(x, y, ". ")
                    x += dot_w
                c.setFont(self.font, self.size)
                c.drawRightString(self.aw, y, self.page)
            y -= self.lh
        if self.key:
            c.linkRect("", self.key, (0, 0, self.aw, self.h), relative=1, thickness=0)


class Doc(BaseDocTemplate):
    def __init__(self, path, entries_prev, **kw):
        super().__init__(path, pagesize=A4, leftMargin=M_LEFT, rightMargin=M_RIGHT, topMargin=M_TOP,
                         bottomMargin=M_BOTTOM, title="Diya: Design and Development of an Unattended "
                         "Meditation Kiosk", author="Ayush Gupta", **kw)
        frame = Frame(M_LEFT, M_BOTTOM, TEXT_W, PAGE_H - M_TOP - M_BOTTOM, id="f", leftPadding=0,
                      rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate("title", [frame], onPageEnd=lambda c, d: None),
            PageTemplate("front", [frame], onPageEnd=self._front_footer),
            PageTemplate("main", [frame], onPageEnd=self._main_footer),
        ])
        self.offset = None
        self.entries = []
        self.key_n = 0

    def label(self, page):
        if self.offset is None or page <= self.offset:
            return roman(page)
        return str(page - self.offset)

    def _front_footer(self, c, d):
        c.saveState()
        c.setFont("Serif", 11)
        c.drawCentredString(PAGE_W / 2, 0.6 * inch, roman(d.page))
        c.restoreState()

    def _main_footer(self, c, d):
        c.saveState()
        c.setStrokeColor(colors.HexColor("#9CA3AF"))
        c.setLineWidth(0.5)
        c.line(M_LEFT, PAGE_H - 0.72 * inch, PAGE_W - M_RIGHT, PAGE_H - 0.72 * inch)
        c.setFont("Serif-Italic", 9.5)
        c.setFillColor(GREY)
        c.drawRightString(PAGE_W - M_RIGHT, PAGE_H - 0.66 * inch, "Diya: Unattended Meditation Kiosk")
        c.drawString(M_LEFT, PAGE_H - 0.66 * inch, "Summer Internship Report, IIT Hyderabad")
        c.setFillColor(colors.black)
        c.setFont("Serif", 11)
        c.drawCentredString(PAGE_W / 2, 0.6 * inch, self.label(d.page))
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Mark):
            if f.main_start:
                self.offset = self.page - 1
            self.key_n += 1
            key = f"k{self.key_n}"
            self.canv.bookmarkPage(key)
            if f.kind == "toc":
                self.canv.addOutlineEntry(f.text, key, level=f.level, closed=f.level > 0)
            self.entries.append((f.kind, f.text, f.level, self.label(self.page), key))


# ------------------------------------------------------------------ builder
def img_size(path, width_in=None, height_in=None):
    with PILImage.open(path) as im:
        w, h = im.size
    if width_in:
        wpt = min(width_in * inch, TEXT_W)
        return wpt, wpt * h / w
    hpt = height_in * inch
    return hpt * w / h, hpt


def caption(num, text, table=False):
    st = S["tcaption"] if table else S["caption"]
    label = "Table" if table else "Figure"
    if num:
        return Paragraph(f"<b>{label} {num}:</b> {md(text)}", st)
    return Paragraph(md(text), st)


def title_page(meta):
    st = lambda size, bold=False, sp=6, color=colors.black, lead=None: ParagraphStyle(
        "t", fontName="Serif-Bold" if bold else "Serif", fontSize=size, leading=lead or size * 1.3,
        alignment=TA_CENTER, spaceAfter=sp, textColor=color)
    f = []
    f.append(Paragraph("A REPORT ON", st(13, True, 2)))
    f.append(Paragraph("SUMMER INTERNSHIP", st(13, True, 28)))
    f.append(Paragraph(meta["title"], st(19, True, 8, lead=25)))
    f.append(Paragraph(f"<i>{meta['subtitle']}</i>", st(12, False, 32)))
    f.append(Paragraph("Submitted in partial fulfilment of the requirements for the award of the degree of",
                       st(11.5, False, 4)))
    f.append(Paragraph(f"<b>{meta['programme']}</b>", st(12.5, False, 26)))
    f.append(Paragraph("Submitted by", st(11.5, False, 2)))
    f.append(Paragraph(f"<b>{meta['student'].upper()}</b>", st(14, False, 2)))
    f.append(Paragraph(f"Registration No.: {md(meta['regno'])}", st(12, False, 24)))
    f.append(Paragraph("Internship carried out at", st(11.5, False, 2)))
    f.append(Paragraph(f"<b>{meta['lab']}</b>", st(12.5, False, 2)))
    f.append(Paragraph(f"<b>{meta['org']}</b>", st(12.5, False, 2)))
    f.append(Paragraph(f"{meta['period']}", st(11.5, False, 22)))
    data = [[Paragraph("<b>Under the supervision of</b>", st(11, False, 2)),
             Paragraph("<b>Faculty guide</b>", st(11, False, 2))],
            [Paragraph(f"{meta['supervisor']}<br/>{meta['supervisor_desig']}<br/>{meta['org']}",
                       st(11, False, 0, lead=15)),
             Paragraph(f"{md(meta['faculty_guide'])}<br/>{md(meta['faculty_desig'])}<br/>{meta['department']}",
                       st(11, False, 0, lead=15))]]
    t = Table(data, colWidths=[TEXT_W / 2, TEXT_W / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    f.append(t)
    f.append(Spacer(1, 20))
    logo = Placeholder(1.05, "University logo", "Insert the university logo here")
    logo.w = 1.9 * inch
    lt = Table([[logo]], colWidths=[TEXT_W])
    lt.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    f.append(lt)
    f.append(Spacer(1, 16))
    f.append(Paragraph(f"<b>{meta['department'].upper()}</b>", st(12, False, 2)))
    f.append(Paragraph(f"<b>{meta['university'].upper()}</b>", st(12, False, 2)))
    f.append(Paragraph(md(meta["campus"]), st(11.5, False, 2)))
    f.append(Paragraph(meta["month"], st(11.5, False, 0)))
    return f


def build_story(report, prev_entries):
    story = [NextPageTemplate("front")]
    figs = [e for e in prev_entries if e[0] == "lof"]
    tabs = [e for e in prev_entries if e[0] == "lot"]
    tocs = [e for e in prev_entries if e[0] == "toc"]

    def list_page(title, items, bold_lvl0=False, kind=None):
        out = [PageBreakIfNotEmpty(), Mark("toc", nice_title(title)) if kind else Spacer(0, 0),
               Paragraph(title, S["toc_head"])]
        if not items:
            out.append(Paragraph("(generated)", S["body"]))
        for e in items:
            _, text, level, page, key = e
            out.append(TocRow(text, page, key, indent=level * 0.3 * inch,
                              bold=bold_lvl0 and level == 0, size=12 if kind is None else 11.5))
        return out

    blocks = report.blocks
    for bi, b in enumerate(blocks):
        k = b["kind"]
        nxt = blocks[bi + 1]["kind"] if bi + 1 < len(blocks) else None
        if k == "title_page":
            story += title_page(b["meta"])
        elif k == "front":
            story.append(PageBreakIfNotEmpty())
            story.append(Mark("toc", b["orig"]))
            story.append(Paragraph(b["title"], S["toc_head"]))
        elif k == "toc":
            story += list_page("TABLE OF CONTENTS", tocs, bold_lvl0=True)
        elif k == "lof":
            story += list_page("LIST OF FIGURES", figs, kind="lof")
        elif k == "lot":
            story += list_page("LIST OF TABLES", tabs, kind="lot")
        elif k == "chapter":
            if b["first"]:
                story.append(NextPageTemplate("main"))
            story.append(PageBreakIfNotEmpty())
            toc_text = b["orig"]
            if b["label"] and b["label"].startswith("CHAPTER"):
                toc_text = f"{b['num']}   {b['orig']}"
            elif b["label"]:
                toc_text = f"Appendix {b['num']}   {b['orig']}"
            story.append(Mark("toc", toc_text, 0, main_start=b["first"]))
            if b["label"]:
                story.append(Paragraph(b["label"], S["chap_label"]))
            story.append(Paragraph(escape(b["title"]), S["chap_title"]))
        elif k == "section":
            before_table = nxt == "table"
            story.append(CondPageBreak((2.4 if before_table else 1.3) * inch))
            story.append(Mark("toc", f"{b['num']}   {b['title']}", 1))
            st = ParagraphStyle("secT", parent=S["section"], keepWithNext=0) if before_table else S["section"]
            story.append(Paragraph(f"{b['num']}&nbsp;&nbsp;&nbsp;{md(b['title'])}", st))
        elif k == "sub":
            story.append(Mark("toc", f"{b['num']}   {b['title']}", 2))
            story.append(Paragraph(f"{b['num']}&nbsp;&nbsp;{md(b['title'])}", S["sub"]))
        elif k == "para":
            story.append(Paragraph(md(b["text"]), S["left"] if b["align"] == "left" else S["body"]))
        elif k == "bullets":
            for it in b["items"]:
                story.append(Paragraph(md(it), S["bullet"], bulletText="•"))
            story.append(Spacer(1, 4))
        elif k == "numbered":
            for i, it in enumerate(b["items"], 1):
                story.append(Paragraph(md(it), S["bullet"], bulletText=f"{i}."))
            story.append(Spacer(1, 4))
        elif k == "code":
            lines = escape(b["text"]).replace(" ", "&nbsp;").split("\n")
            p = Paragraph("<br/>".join(lines), S["code"])
            t = Table([[p]], colWidths=[TEXT_W])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                                   ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            story += [t, Spacer(1, 10)]
        elif k == "figure":
            w, h = img_size(b["path"], width_in=b["width"])
            max_h = 7.6 * inch
            if h > max_h:
                w, h = w * max_h / h, max_h
            img = Image(b["path"], width=w, height=h)
            story.append(KeepTogether([Spacer(1, 4), img, Mark("lof", f"{b['num']}   {b['caption']}"),
                                       caption(b["num"], b["caption"])]))
        elif k == "figrow":
            cells, labs = [], []
            for path, lab in b["items"]:
                w, h = img_size(path, height_in=b["height"])
                cells.append(Image(path, width=w, height=h))
                labs.append(Paragraph(md(lab), S["sublabel"]))
            n = len(cells)
            t = Table([cells, labs], colWidths=[TEXT_W / n] * n)
            t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
            story.append(KeepTogether([Spacer(1, 4), t, Mark("lof", f"{b['num']}   {b['caption']}"),
                                       caption(b["num"], b["caption"])]))
        elif k == "placeholder":
            ph = Placeholder(b["height"], "PLACE PHOTOGRAPH HERE" if b["num"] else "PLACE SCANNED CERTIFICATE HERE",
                             b["hint"])
            t = Table([[ph]], colWidths=[TEXT_W])
            t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
            items = [Spacer(1, 4), t]
            if b["num"]:
                items += [Mark("lof", f"{b['num']}   {b['caption']}"), caption(b["num"], b["caption"])]
            story.append(KeepTogether(items))
        elif k == "table":
            widths = [w * inch for w in b["widths"]] if b["widths"] else None
            if widths:
                scale = TEXT_W / sum(widths)
                widths = [w * scale for w in widths]
            ncol = len(b["header"])
            data = []
            if b["num"]:
                data.append([caption(b["num"], b["caption"], True)] + [""] * (ncol - 1))
            data.append([Paragraph(md(h), S["cellh"]) for h in b["header"]])
            for row in b["rows"]:
                data.append([Paragraph(md(c), S["cell"]) for c in row])
            h0 = 1 if b["num"] else 0
            t = Table(data, colWidths=widths, repeatRows=h0 + 1)
            style = [
                ("GRID", (0, h0), (-1, -1), 0.5, colors.HexColor("#6B7280")),
                ("BACKGROUND", (0, h0), (-1, h0), colors.HexColor("#E5E7EB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, h0), (-1, -1), 4), ("BOTTOMPADDING", (0, h0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
            if b["num"]:
                style += [("SPAN", (0, 0), (-1, 0)), ("TOPPADDING", (0, 0), (-1, 0), 0),
                          ("BOTTOMPADDING", (0, 0), (-1, 0), 5)]
            t.setStyle(TableStyle(style))
            if b["num"]:
                story.append(Mark("lot", f"{b['num']}   {b['caption']}"))
            story += [t, Spacer(1, 12)]
        elif k == "signature":
            st = ParagraphStyle("sig", parent=S["left"], alignment=TA_RIGHT, spaceAfter=2)
            story.append(Paragraph("(Signature)", st))
            for ln in b["lines"]:
                story.append(Paragraph(md(ln), st))
        elif k == "refs":
            for i, it in enumerate(b["items"], 1):
                story.append(Paragraph(f"[{i}]&nbsp;&nbsp;{md(it)}", S["ref"]))
        elif k == "pagebreak":
            story.append(PageBreak())
        elif k == "spacer":
            story.append(Spacer(1, b["h"] * inch))
    return story


def render(report, out_path):
    entries = []
    for attempt in range(5):
        doc = Doc(out_path, entries)
        doc.build(build_story(report, entries))
        new = [(k, t, l, p) for k, t, l, p, _ in doc.entries]
        old = [(k, t, l, p) for k, t, l, p, _ in entries]
        entries = doc.entries
        if new == old:
            break
    print(f"PDF: {out_path}  ({doc.page} pages, {attempt + 1} passes)")
    return entries
