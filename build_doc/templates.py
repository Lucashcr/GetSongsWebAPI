from reportlab.lib.units import mm
from reportlab.platypus import *

from .styles import paragraphs, headings


class CustomBaseTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self.__body = []

    def insert_paragraph(self, text, style='left-aligned'):
        self.__body.append(Paragraph(text, paragraphs[style]))

    def insert_paragraph_link(self, text, href, style='left-aligned'):
        self.__body.append(Paragraph(f'<a href="{href}">{text}</a>', paragraphs[style]))
    
    def insert_heading_link(self, text, href, style='heading1'):
        self.__body.append(Paragraph(f'<a href="{href}">{text}</a>', headings[style]))

    def insert_heading(self, text, style='heading1'):
        self.__body.append(Paragraph(text, headings[style]))

    def build(self):
        super().build(self.__body)


class SingleColumnTemplate(CustomBaseTemplate):

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        
        page = Frame(
            self.leftMargin, self.bottomMargin, 
            self.width, self.height, id='page'
        )
        self.addPageTemplates(PageTemplate('single_column', [page]))


class TwoColumnsTemplate(CustomBaseTemplate):
    
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)

        col1 = Frame(
            self.leftMargin, self.bottomMargin, 
            self.width/2 - 5*mm, self.height, id='col1'
        )
        col2 = Frame(
            self.width/2 + self.leftMargin + 5*mm, self.bottomMargin, 
            self.width/2 - 5*mm, self.height, id='col2'
        )
        self.addPageTemplates(PageTemplate('two_columns', [col1, col2]))


__all__ = ['SingleColumnTemplate', 'TwoColumnTemplate']