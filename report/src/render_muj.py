"""Build the report on top of the college template (report/template/MUJ-format.docx).

The cover page (with the MUJ logo), styles, page size and margins come from the template itself.
The PDF is produced from the finished DOCX with LibreOffice, so both files match page for page.
"""
import copy
import os
import re
import shutil
import subprocess
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, Twips, RGBColor
from docx.text.paragraph import Paragraph
from PIL import Image as PILImage

sys.path.insert(0, os.path.dirname(__file__))
from model import ROOT, runs              # noqa: E402
import content_muj                        # noqa: E402

TEMPLATE = os.path.join(ROOT, "template", "MUJ-format.docx")
OUT_DOCX = os.path.join(ROOT, "Diya-Internship-Report.docx")
OUT_PDF = os.path.join(ROOT, "Diya-Internship-Report.pdf")
SOFFICE = os.environ.get("SOFFICE", "soffice")

FONT = "Times New Roman"
BODY = 14            # template body text size
LEFT, RIGHT, TOP, BOTTOM = 660, 900, 1260, 1000      # twips (template: left 660)
TEXT_W_TW = 11900 - LEFT - RIGHT
TABLE_W_TW = TEXT_W_TW - 240 - 100                    # template tables are indented 240
TEXT_W_IN = TEXT_W_TW / 1440

PPR_AFTER_SHD = ("w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct",
                 "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi", "w:adjustRightInd",
                 "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
                 "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
                 "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")
TCPR_AFTER_BORDERS = ("w:shd", "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign",
                      "w:hideMark")


def insert_ordered(parent, child, successors):
    for tag in successors:
        f = parent.find(qn(tag))
        if f is not None:
            f.addprevious(child)
            return child
    parent.append(child)
    return child


def roman(n):
    out = ""
    for v, s in [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]:
        while n >= v:
            out += s
            n -= v
    return out


# ------------------------------------------------------------------ run helpers
def font(run, size=BODY, bold=None, italic=None, name=FONT, color=None):
    run.font.name = name
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    return run


def add_md(p, text, size=BODY, bold=False, italic=False):
    for seg, st in runs(text):
        if st == "code":
            r = p.add_run(seg)
            font(r, size - 1.5, bold or None, italic or None, name="Courier New")
            continue
        r = p.add_run(seg)
        font(r, size, (st == "bold") or bold or None, (st == "italic") or italic or None)
        if st == "fill":
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return p


def fmt(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=4, left=None, hanging=None, first=None,
        keep=False, line=None):
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if left is not None:
        pf.left_indent = Twips(left)
    if hanging is not None:
        pf.first_line_indent = Twips(-hanging)
    if first is not None:
        pf.first_line_indent = Twips(first)
    if keep:
        pf.keep_with_next = True
    if line is not None:
        pf.line_spacing = line
    return p


def set_runs(p, parts, proto=None):
    """Replace a template paragraph's runs, keeping the formatting of its first run."""
    proto = proto if proto is not None else p.runs[0]._r
    proto_rpr = proto.find(qn("w:rPr"))
    for child in list(p._p):
        if child.tag in (qn("w:r"), qn("w:proofErr"), qn("w:bookmarkStart"), qn("w:bookmarkEnd")):
            p._p.remove(child)
    for text, hl in parts:
        r = OxmlElement("w:r")
        if proto_rpr is not None:
            r.append(copy.deepcopy(proto_rpr))
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = text
        r.append(t)
        p._p.append(r)
        if hl:
            from docx.text.run import Run
            Run(r, p).font.highlight_color = WD_COLOR_INDEX.YELLOW


def split_fill(text):
    return [(s if st != "fill" else s, st == "fill") for s, st in runs(text)]


# ------------------------------------------------------------------ XML helpers
def cell_borders(cell, val="single", sz=4, color="C0C0C0"):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), val)
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:color"), color)
        b.append(e)
    insert_ordered(tcPr, b, TCPR_AFTER_BORDERS)


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), fill)
    insert_ordered(tcPr, s, TCPR_AFTER_BORDERS[1:])


def shade_par(p, fill):
    pPr = p._p.get_or_add_pPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), fill)
    insert_ordered(pPr, s, PPR_AFTER_SHD)


def template_tblpr(tbl, indent=240):
    """Give a table the template's look: thin grey borders, fixed layout, indented 240."""
    tblPr = tbl._tbl.tblPr
    for tag in ("w:tblStyle", "w:tblBorders", "w:tblInd", "w:tblLayout", "w:tblLook", "w:tblW"):
        e = tblPr.find(qn(tag))
        if e is not None:
            tblPr.remove(e)
    xml = (f'<w:tblW xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:w="0" w:type="auto"/>')
    from lxml import etree
    w = etree.fromstring(xml)
    ind = OxmlElement("w:tblInd")
    ind.set(qn("w:w"), str(indent))
    ind.set(qn("w:type"), "dxa")
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "C0C0C0")
        borders.append(e)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    for el in (w, ind, borders, layout):
        tblPr.append(el)


def no_borders(tbl):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "nil")
        b.append(e)
    tblPr.append(b)


def page_field(p):
    for kind, txt in (("begin", None), (None, "PAGE"), ("separate", None), (None, None), ("end", None)):
        r = p.add_run()
        font(r, 12)
        if kind:
            c = OxmlElement("w:fldChar")
            c.set(qn("w:fldCharType"), kind)
            r._r.append(c)
        elif txt:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = txt
            r._r.append(it)
        else:
            r.text = "1"


def pgnum(section, fmt_, start):
    sectPr = section._sectPr
    pg = sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        insert_ordered(sectPr, pg, ("w:cols", "w:formProt", "w:vAlign", "w:noEndnote", "w:titlePg",
                                    "w:textDirection", "w:bidi", "w:rtlGutter", "w:docGrid"))
    pg.set(qn("w:fmt"), fmt_)
    pg.set(qn("w:start"), str(start))


def margins(section):
    section.left_margin, section.right_margin = Twips(LEFT), Twips(RIGHT)
    section.top_margin, section.bottom_margin = Twips(TOP), Twips(BOTTOM)
    section.header_distance, section.footer_distance = Twips(720), Twips(500)


# ------------------------------------------------------------------ builder
class Builder:
    def __init__(self, report, pages=None):
        self.r = report
        self.pages = pages or {}
        self.doc = Document(TEMPLATE)
        self.fig = 0
        self.tab = 0
        self.figs, self.tabs, self.toc = [], [], []   # (key, number, title)
        self.contents_tbl = self.lof_tbl = self.lot_tbl = None

    def page(self, key):
        return self.pages.get(key, "")

    # --- template cover --------------------------------------------------
    def cover(self, meta):
        body = self.doc.element.body
        els = list(body.iterchildren())
        P = lambda i: Paragraph(els[i], self.doc)
        set_runs(P(0), [(meta["report_type"], False)])
        set_runs(P(5), [(meta["title"], False)])
        p7 = P(7)
        r0, r1, r2 = [r._r for r in p7.runs[:3]]
        set_runs(p7, [("carried out as part of the ", False)], proto=r0)
        tmp = copy.deepcopy(p7._p)
        set_runs(Paragraph(tmp, self.doc), [("Industrial Training (", False), ("[Subject Code]", True),
                                            (")", False)], proto=r1)
        for r in tmp.findall(qn("w:r")):
            p7._p.append(r)
        set_runs(Paragraph(tmp, self.doc), [(" Submitted", False)], proto=r2)
        for r in tmp.findall(qn("w:r")):
            p7._p.append(r)
        set_runs(P(11), [(meta["student"], False)])
        set_runs(P(12), [(meta["regno"], False)])
        set_runs(P(30), [(meta["month"], False)])
        # Drop everything after the cover; keep the final section properties.
        sect = body.find(qn("w:sectPr"))
        for el in els[31:]:
            if el is not sect:
                body.remove(el)
        for s in self.doc.sections:
            margins(s)

    def certificate(self, path):
        p = self.doc.add_paragraph()
        p.paragraph_format.page_break_before = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        full = os.path.join(ROOT, path)
        with PILImage.open(full) as im:
            w, h = im.size
        height = 9.6
        p.add_run().add_picture(full, height=Inches(height), width=Inches(height * w / h))
        # new section: front matter, roman page numbers
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        margins(sec)
        sec.footer.is_linked_to_previous = False
        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        page_field(fp)
        pgnum(sec, "lowerRoman", 1)
        self.first_front = True

    # --- headings --------------------------------------------------------
    def heading_par(self, text, style="Heading 1", newpage=True, size=16):
        p = self.doc.add_paragraph(style=style)
        pf = p.paragraph_format
        pf.page_break_before = newpage and not getattr(self, "first_front", False)
        self.first_front = False
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.left_indent = Twips(0)
        pf.right_indent = Twips(0)
        pf.first_line_indent = Twips(0)
        pf.space_before = Pt(4)
        pf.space_after = Pt(14)
        pf.line_spacing = 1.0
        pf.keep_with_next = True
        add_md(p, text, size=size, bold=True)
        return p

    def front(self, b):
        self.heading_par(b["title"])
        self.toc.append(("front", b["key"], b["title"]))

    def chapter(self, b):
        if b["num"] == 1:
            sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
            margins(sec)
            pgnum(sec, "decimal", 1)
            self.first_front = True
        self.heading_par(b["title"])
        self.toc.append(("chapter", f"ch{b['num']}", b["title"], b["num"]))

    def section(self, b):
        self.heading_par(f"{b['num']}) {b['title']}", style="Heading 2", newpage=b["newpage"])
        self.toc.append(("section", f"s{b['num']}", b["toc_title"], b["num"], b["title"]))

    def unnumbered(self, b):
        self.heading_par(b["title"])
        self.toc.append(("end", b["title"].lower(), b["title"].upper()))

    # --- text ------------------------------------------------------------
    def para(self, b):
        add_md(fmt(self.doc.add_paragraph()), b["text"])

    def sub(self, b):
        add_md(fmt(self.doc.add_paragraph(), WD_ALIGN_PARAGRAPH.LEFT, before=8, after=3, keep=True),
               b["text"], bold=True)

    def list_items(self, items, numbered):
        for i, it in enumerate(items, 1):
            p = fmt(self.doc.add_paragraph(), left=720, hanging=360, after=2)
            p.paragraph_format.tab_stops.add_tab_stop(Twips(720))
            r = p.add_run(f"{i}.\t" if numbered else "•\t")
            font(r)
            add_md(p, it)
        self.doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

    def code(self, b):
        p = fmt(self.doc.add_paragraph(), WD_ALIGN_PARAGRAPH.LEFT, after=8, left=240, line=1.0)
        shade_par(p, "F2F2F2")
        lines = b["text"].split("\n")
        for j, ln in enumerate(lines):
            r = p.add_run(ln)
            font(r, 10, name="Courier New")
            if j < len(lines) - 1:
                r.add_break()

    # --- figures and tables ----------------------------------------------
    def caption(self, label, num, text, keep=False):
        p = fmt(self.doc.add_paragraph(), WD_ALIGN_PARAGRAPH.CENTER, before=3, after=10, keep=keep)
        r = p.add_run(f"{label} {num}: ")
        font(r, 12, bold=True)
        add_md(p, text, size=12)
        return p

    def figure(self, b):
        self.fig += 1
        path = os.path.join(ROOT, b["path"])
        with PILImage.open(path) as im:
            w, h = im.size
        width = min(b["width"], TEXT_W_IN - 0.4)
        if width * h / w > 8.0:
            width = 8.0 * w / h
        p = fmt(self.doc.add_paragraph(), WD_ALIGN_PARAGRAPH.CENTER, before=6, after=0, keep=True, line=1.0)
        p.add_run().add_picture(path, width=Inches(width))
        self.caption("Figure", self.fig, b["caption"])
        self.figs.append((f"f{self.fig}", self.fig, b["caption"]))

    def figrow(self, b):
        self.fig += 1
        n = len(b["items"])
        t = self.doc.add_table(rows=2, cols=n)
        no_borders(t)
        col_w = (TEXT_W_IN - 0.4) / n
        for i, (path, lab) in enumerate(b["items"]):
            full = os.path.join(ROOT, path)
            with PILImage.open(full) as im:
                w, h = im.size
            width = min(b["height"] * w / h, col_w - 0.1)
            c = t.cell(0, i)
            c.width = Inches(col_w)
            p = fmt(c.paragraphs[0], WD_ALIGN_PARAGRAPH.CENTER, after=2, keep=True, line=1.0)
            p.add_run().add_picture(full, width=Inches(width))
            lp = fmt(t.cell(1, i).paragraphs[0], WD_ALIGN_PARAGRAPH.CENTER, after=0, keep=True)
            add_md(lp, lab, size=11)
        self.caption("Figure", self.fig, b["caption"])
        self.figs.append((f"f{self.fig}", self.fig, b["caption"]))

    def placeholder(self, b):
        self.fig += 1
        t = self.doc.add_table(rows=1, cols=1)
        template_tblpr(t)
        c = t.cell(0, 0)
        c.width = Twips(TABLE_W_TW)
        t.rows[0].height = Inches(b["height"])
        t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell_borders(c, "dashed", 8, "808080")
        p = fmt(c.paragraphs[0], WD_ALIGN_PARAGRAPH.CENTER, after=4, keep=True)
        font(p.add_run("PLACE PHOTOGRAPH HERE"), 14, bold=True, color="595959")
        p2 = fmt(c.add_paragraph(), WD_ALIGN_PARAGRAPH.CENTER, after=0, keep=True)
        font(p2.add_run(b["hint"]), 12, italic=True, color="595959")
        trPr = t.rows[0]._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        self.caption("Figure", self.fig, b["caption"])
        self.figs.append((f"f{self.fig}", self.fig, b["caption"]))

    def data_table(self, header, rows, widths, size=12):
        t = self.doc.add_table(rows=1, cols=len(header))
        template_tblpr(t)
        scale = TABLE_W_TW / sum(widths)
        tw = [int(w * scale) for w in widths]
        for i, h in enumerate(header):
            p = fmt(t.rows[0].cells[i].paragraphs[0], WD_ALIGN_PARAGRAPH.LEFT, before=2, after=2, left=80)
            add_md(p, h, size=size, bold=True)
        trPr = t.rows[0]._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:tblHeader"))
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                p = fmt(cells[i].paragraphs[0], WD_ALIGN_PARAGRAPH.LEFT, before=2, after=2, left=80)
                add_md(p, v, size=size)
        for r in t.rows:
            for i, c in enumerate(r.cells):
                c.width = Twips(tw[i])
        grid = t._tbl.find(qn("w:tblGrid"))
        for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(tw[i]))
        return t

    def table(self, b):
        if b["caption"]:
            self.tab += 1
            self.caption("Table", self.tab, b["caption"], keep=True)
            self.tabs.append((f"t{self.tab}", self.tab, b["caption"]))
        self.data_table(b["header"], b["rows"], b["widths"])
        fmt(self.doc.add_paragraph(), after=4)

    def refs(self, b):
        for i, it in enumerate(b["items"], 1):
            p = fmt(self.doc.add_paragraph(), WD_ALIGN_PARAGRAPH.LEFT, after=5, left=600, hanging=600)
            p.paragraph_format.tab_stops.add_tab_stop(Twips(600))
            font(p.add_run(f"[{i}]\t"), 13)
            add_md(p, it, size=13)

    # --- lists of figures/tables and contents ----------------------------
    def list_table(self, kind):
        title = "LIST OF FIGURES" if kind == "lof" else "LIST OF TABLES"
        self.heading_par(title)
        self.toc.append(("front", kind, title))
        p = self.doc.add_paragraph()
        holder = p
        if kind == "lof":
            self.lof_tbl = holder
        else:
            self.lot_tbl = holder

    def contents(self):
        self.contents_tbl = self.doc.add_paragraph()

    def fill_list(self, holder, kind):
        items = self.figs if kind == "lof" else self.tabs
        label = "Figure No" if kind == "lof" else "Table No"
        title = "Figure Title" if kind == "lof" else "Table Title"
        rows = [[f"{n})", t, self.page(k)] for k, n, t in items]
        t = self.data_table([label, title, "Page No"], rows, [1281, 7652, 1165], size=12)
        holder._p.addnext(t._tbl)
        holder._p.getparent().remove(holder._p)

    def fill_contents(self, holder):
        """Rebuild the template's Contents table, row prototypes and all, with our entries."""
        tpl = Document(TEMPLATE).tables[1]._tbl
        rows = tpl.findall(qn("w:tr"))
        proto = {"title": rows[0], "pageno": rows[1], "front": rows[2], "chapter": rows[6],
                 "section": rows[7], "end": rows[27]}
        new = copy.deepcopy(tpl)
        for tr in new.findall(qn("w:tr")):
            new.remove(tr)

        def row(kind, texts, bold=None):
            tr = copy.deepcopy(proto[kind])
            tcs = tr.findall(qn("w:tc"))
            for tc, txt in zip(tcs, texts):
                if txt is None:
                    continue
                p = tc.find(qn("w:p"))
                for ch in list(p):
                    if ch.tag != qn("w:pPr"):
                        p.remove(ch)
                if txt == "":
                    continue
                para = Paragraph(p, self.doc)
                add_md(para, txt, size=12, bold=(bold is True) or None)
            new.append(tr)
            return tr

        row("title", [None])
        row("pageno", [None, None])
        names = {"ack": "Acknowledgement", "abstract": "Abstract", "lof": "List Of Figures",
                 "lot": "List Of Tables", "abbr": "List of Abbreviations"}
        for e in self.toc:
            if e[0] == "front":
                row("front", [names[e[1]], "", self.page(e[1])])
            elif e[0] == "chapter":
                label = f"Chapter {e[3]}"
                row("chapter", [label, None, self.page(e[1])])
                tc = new.findall(qn("w:tr"))[-1].findall(qn("w:tc"))[1]
                p = tc.find(qn("w:p"))
                for ch in list(p):
                    if ch.tag != qn("w:pPr"):
                        p.remove(ch)
                add_md(Paragraph(p, self.doc), e[2], size=12, bold=True)
            elif e[0] == "section":
                row("section", ["", e[3], e[2], self.page(e[1])])
            elif e[0] == "end":
                row("end", [e[2], self.page(e[1])], bold=True)
        for tr in new.findall(qn("w:tr"))[1:]:
            tc = tr.findall(qn("w:tc"))[-1]
            Paragraph(tc.find(qn("w:p")), self.doc).alignment = WD_ALIGN_PARAGRAPH.CENTER
        holder._p.addnext(new)

    # --- main ------------------------------------------------------------
    def build(self):
        for b in self.r.blocks:
            k = b["kind"]
            if k == "cover":
                self.cover(b["meta"])
            elif k == "certificate":
                self.certificate(b["path"])
            elif k in ("lof", "lot"):
                self.list_table(k)
            elif k == "contents":
                p = self.doc.add_paragraph()
                p.paragraph_format.page_break_before = True
                self.contents_tbl = p
            elif k == "bullets":
                self.list_items(b["items"], False)
            elif k == "numbered":
                self.list_items(b["items"], True)
            else:
                getattr(self, k)(b)
        self.fill_list(self.lof_tbl, "lof")
        self.fill_list(self.lot_tbl, "lot")
        self.fill_contents(self.contents_tbl)
        # Template paragraphs have page-break markers from Word; keep the doc clean of stale ones.
        self.doc.core_properties.title = "Diya: Design and Development of an Unattended Meditation Kiosk"
        self.doc.core_properties.author = "Ayush Gupta"
        return self


# ------------------------------------------------------------------ page numbers
def to_pdf(docx_path, outdir):
    env = dict(os.environ)
    env.setdefault("SAL_USE_VCLPLUGIN", "svp")
    profile = os.environ.get("LO_PROFILE", "file:///tmp/lo-profile")
    cmd = [SOFFICE, "--headless", "--norestore", f"-env:UserInstallation={profile}", "--convert-to", "pdf",
           "--outdir", outdir, docx_path]
    for _ in range(2):
        res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
        pdf = os.path.join(outdir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
        if os.path.exists(pdf):
            return pdf
    raise RuntimeError(res.stdout + res.stderr)


def find_pages(pdf_path, builder):
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(pdf_path)
    texts = [re.sub(r"\s+", "", pdf[i].get_textpage().get_text_range()) for i in range(len(pdf))]
    norm = lambda s: re.sub(r"\s+", "", re.sub(r"\*", "", s))
    targets = []
    for e in builder.toc:
        if e[0] == "front":
            word = {"ack": "ACKNOWLEDGMENTS", "abstract": "ABSTRACT", "lof": "LISTOFFIGURES",
                    "lot": "LISTOFTABLES", "abbr": "AbbreviationFullForm"}[e[1]]
            targets.append((e[1], word))
        elif e[0] == "chapter":
            targets.append((e[1], norm(e[2])))
        elif e[0] == "section":
            targets.append((e[1], norm(f"{e[3]}) {e[4]}")[:28]))
        elif e[0] == "end":
            targets.append((e[1], norm(e[2].title())))
    pages, pos = {}, 2
    first_ch = None
    for key, needle in targets:
        for i in range(pos, len(texts)):
            if needle in texts[i]:
                pages[key] = i
                pos = i
                break
        if key == "ch1":
            first_ch = pages.get("ch1")
    for kind, items in (("Figure", builder.figs), ("Table", builder.tabs)):
        pos = first_ch or 0
        for key, n, _ in items:
            needle = f"{kind}{n}:"
            for i in range(pos, len(texts)):
                if needle in texts[i]:
                    pages[key] = i
                    pos = i
                    break
    labels = {}
    for k, i in pages.items():
        labels[k] = roman(i - 1) if (first_ch is None or i < first_ch) else str(i - first_ch + 1)
    return labels, len(texts)


def main():
    report = content_muj.build()
    tmpdir = "/tmp/muj-build"
    os.makedirs(tmpdir, exist_ok=True)
    pages = {}
    for attempt in range(4):
        b = Builder(report, pages).build()
        path = os.path.join(tmpdir, "Diya-Internship-Report.docx")
        b.doc.save(path)
        pdf = to_pdf(path, tmpdir)
        new, n = find_pages(pdf, b)
        missing = [e for e in b.toc if e[1] not in new] + [f for f in b.figs + b.tabs if f[0] not in new]
        if missing:
            print("could not locate:", missing)
        if new == pages:
            break
        pages = new
    shutil.copy(path, OUT_DOCX)
    shutil.copy(pdf, OUT_PDF)
    print(f"DOCX: {OUT_DOCX}\nPDF:  {OUT_PDF}  ({n} pages, {attempt + 1} passes)")


if __name__ == "__main__":
    main()
