from reportlab.platypus.paragraph import ParagraphStyle
from reportlab.lib.units import mm


paragraphs = {
    'left-aligned'  : ParagraphStyle('left-aligned', alignment=0, spaceAfter=8),
    'centered'      : ParagraphStyle('centered', alignment=1),
    'right-aligned' : ParagraphStyle('right-aligned', alignment=2),
    'justified'     : ParagraphStyle('justified', alignment=4, firstLineIndent=10*mm, spaceAfter=8),
    'heading1'      : ParagraphStyle('heading1', fontName='Helvetica-Bold', alignment=0, fontSize=16, spaceBefore=16, spaceAfter=12),
    'heading2'      : ParagraphStyle('heading2', fontName='Helvetica-Bold', alignment=0, fontSize=12, spaceBefore=12, spaceAfter=8)
}
