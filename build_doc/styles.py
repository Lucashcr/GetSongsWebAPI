from reportlab.platypus.paragraph import ParagraphStyle
from reportlab.lib.units import mm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(
    TTFont("Ubuntu-Medium", "./staticfiles/fonts/Ubuntu-Medium.ttf")
)
pdfmetrics.registerFont(TTFont("Ubuntu-Light", "./staticfiles/fonts/Ubuntu-Light.ttf"))
pdfmetrics.registerFont(
    TTFont("Ubuntu-Regular", "./staticfiles/fonts/Ubuntu-Regular.ttf")
)

CENTERED_HEADING = ParagraphStyle(
    "centered_heading",
    fontName="Ubuntu-Medium",
    fontSize=18,
    alignment=1,
    spaceBefore=16,
    spaceAfter=12,
)

HEADING_1 = ParagraphStyle(
    "heading1",
    fontName="Ubuntu-Medium",
    fontSize=14,
    alignment=0,
    spaceBefore=16,
    spaceAfter=12,
)

HEADING_2 = ParagraphStyle(
    "heading2",
    fontName="Ubuntu-Regular",
    fontSize=12,
    alignment=0,
    spaceBefore=12,
    spaceAfter=8,
)

LEFT_ALIGNED = ParagraphStyle(
    "left-aligned", fontName="Ubuntu-Light", alignment=0, spaceAfter=8
)
CENTERED = ParagraphStyle(
    "centered", fontName="Ubuntu-Light", alignment=1, spaceAfter=8
)
RIGHT_ALIGNED = ParagraphStyle(
    "right_aligned", fontName="Ubuntu-Light", alignment=2, spaceAfter=8
)

JUSTIFIED = ParagraphStyle(
    "justified",
    fontName="Ubuntu-Light",
    alignment=4,
    firstLineIndent=10 * mm,
    spaceAfter=8,
)

__all__ = [
    "CENTERED_HEADING",
    "HEADING_1",
    "HEADING_2",
    "LEFT_ALIGNED",
    "CENTERED",
    "RIGHT_ALIGNED",
    "JUSTIFIED",
]
