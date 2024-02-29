from reportlab.lib.units import mm
from reportlab.platypus import *

from .styles import *


def page_setup(canvas, doc):
    canvas.saveState()
    canvas.drawImage(
        "build_doc/images/background.png", x=0, y=0, width=210 * mm, height=297 * mm
    )
    canvas.restoreState()


class CustomBaseTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self.__body = []

    def insert_paragraph(self, text, style=LEFT_ALIGNED):
        self.__body.append(Paragraph(text, style))

    def insert_paragraph_link(self, text, href, style=LEFT_ALIGNED):
        self.__body.append(Paragraph(f'<a href="{href}">{text}</a>', style))

    def insert_heading_link(self, text, href, style=HEADING_1):
        self.__body.append(Paragraph(f'<a href="{href}">{text}</a>', style))

    def insert_heading(self, text, style=HEADING_1):
        self.__body.append(Paragraph(text, style))

    def add_new_page(self):
        self.__body.append(PageBreak())

    def build(self):
        super().build(self.__body)


class SingleColumnTemplate(CustomBaseTemplate):

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)

        page = Frame(
            self.leftMargin, self.bottomMargin, self.width, self.height, id="page"
        )
        self.addPageTemplates(PageTemplate("single_column", [page], onPage=page_setup))


class TwoColumnsTemplate(CustomBaseTemplate):

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)

        col1 = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width / 2 - 5 * mm,
            self.height,
            id="col1",
        )
        col2 = Frame(
            self.width / 2 + self.leftMargin + 5 * mm,
            self.bottomMargin,
            self.width / 2 - 5 * mm,
            self.height,
            id="col2",
        )
        self.addPageTemplates(
            PageTemplate("two_columns", [col1, col2], onPage=page_setup)
        )


__all__ = ["SingleColumnTemplate", "TwoColumnTemplate"]
