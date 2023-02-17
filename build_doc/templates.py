from reportlab.lib.units import mm
from reportlab.platypus import *


class SingleColumnTemplate(BaseDocTemplate):

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        
        page = Frame(
            self.leftMargin, self.bottomMargin, 
            self.width - self.leftMargin*2, self.height, id='page'
        )
        self.addPageTemplates(PageTemplate('single_column', [page]))


class TwoColumnsTemplate(BaseDocTemplate):
    
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)

        frame1 = Frame(
            self.leftMargin, self.bottomMargin, 
            self.width/2 - 5*mm, self.height, id='col1'
        )
        frame2 = Frame(
            self.width/2+self.leftMargin + 5*mm, self.bottomMargin, 
            self.width/2 - 5*mm, self.height, id='col2'
        )
        self.addPageTemplates(PageTemplate('two_columns', [frame1, frame2]))