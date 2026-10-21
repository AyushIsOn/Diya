"""Tiny document model shared by the DOCX and PDF renderers.

Blocks are plain dicts. Figures and tables are numbered per chapter here, so both
renderers print identical numbers. Inline markup inside text:
    **bold**   *italic*   `code`   [[placeholder to fill in]]
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Report:
    def __init__(self):
        self.blocks = []
        self.chapter_no = 0
        self.section_no = 0
        self.sub_no = 0
        self.fig_no = 0
        self.tab_no = 0
        self.appendix = False

    # -- structure ----------------------------------------------------------
    def add(self, kind, **kw):
        kw["kind"] = kind
        self.blocks.append(kw)
        return kw

    def front(self, title, toc=True):
        """Unnumbered front-matter heading on a new page."""
        self.add("front", title=title, orig=nice_title(title), toc=toc)

    def chapter(self, title):
        self.chapter_no += 1
        self.section_no = self.sub_no = self.fig_no = self.tab_no = 0
        label = f"CHAPTER {self.chapter_no}"
        self.add("chapter", label=label, title=title.upper(), orig=title, num=str(self.chapter_no),
                 first=self.chapter_no == 1)

    def appendix_chapter(self, letter, title):
        self.appendix = True
        self.chapter_no = letter
        self.section_no = self.sub_no = self.fig_no = self.tab_no = 0
        self.add("chapter", label=f"APPENDIX {letter}", title=title.upper(), orig=title, num=letter, first=False)

    def unnumbered_chapter(self, title):
        self.add("chapter", label=None, title=title.upper(), orig=title, num=None, first=False)

    def section(self, title):
        self.section_no += 1
        self.sub_no = 0
        self.add("section", num=f"{self.chapter_no}.{self.section_no}", title=title)

    def sub(self, title):
        self.sub_no += 1
        self.add("sub", num=f"{self.chapter_no}.{self.section_no}.{self.sub_no}", title=title)

    # -- content ------------------------------------------------------------
    def p(self, text, align="justify"):
        self.add("para", text=" ".join(text.split()), align=align)

    def bullets(self, items):
        self.add("bullets", items=[" ".join(i.split()) for i in items])

    def numbered(self, items):
        self.add("numbered", items=[" ".join(i.split()) for i in items])

    def code(self, text):
        self.add("code", text=text.strip("\n"))

    def fig(self, path, caption, width=6.0):
        self.fig_no += 1
        full = path if os.path.isabs(path) else os.path.join(ROOT, path)
        if not os.path.exists(full):
            raise FileNotFoundError(full)
        self.add("figure", path=full, caption=caption, width=width,
                 num=f"{self.chapter_no}.{self.fig_no}")

    def figs_side(self, items, caption, height=3.2):
        """Several images side by side under one caption. items = [(path, sublabel)]."""
        self.fig_no += 1
        paths = []
        for path, lab in items:
            full = os.path.join(ROOT, path)
            if not os.path.exists(full):
                raise FileNotFoundError(full)
            paths.append((full, lab))
        self.add("figrow", items=paths, caption=caption, height=height,
                 num=f"{self.chapter_no}.{self.fig_no}")

    def _num(self, counter):
        return None if self.chapter_no == 0 else f"{self.chapter_no}.{counter}"

    def placeholder(self, caption, hint, height=3.0):
        if self.chapter_no != 0:
            self.fig_no += 1
        self.add("placeholder", caption=caption, hint=hint, height=height,
                 num=self._num(self.fig_no))

    def table(self, caption, header, rows, widths=None):
        if self.chapter_no != 0:
            self.tab_no += 1
        self.add("table", caption=caption, header=header, rows=rows, widths=widths,
                 num=self._num(self.tab_no))

    def pagebreak(self):
        self.add("pagebreak")

    def spacer(self, h=0.2):
        self.add("spacer", h=h)


# -- inline markup ------------------------------------------------------------
TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[\[.+?\]\])")


def runs(text):
    """Split text into [(segment, style)] where style in normal/bold/italic/code/fill."""
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], "bold"))
        elif part.startswith("[[") and part.endswith("]]"):
            out.append(("[" + part[2:-2] + "]", "fill"))
        elif part.startswith("`") and part.endswith("`"):
            out.append((part[1:-1], "code"))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append((part[1:-1], "italic"))
        else:
            out.append((part, "normal"))
    return out


SMALL = {"of", "the", "and", "from", "to", "in", "on", "for", "a", "an"}


def nice_title(s):
    words = s.lower().split()
    return " ".join(w if (i and w in SMALL) else w.capitalize() for i, w in enumerate(words))
