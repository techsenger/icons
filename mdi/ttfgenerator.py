# to run the script:
#   pip install "fonttools[lxml]"
#   python3 ttfgenerator.py

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import SVGPath

FONT_EM = 512
FONT_ASCENT = 448
FONT_DESCENT = 64
SOURCE_VIEWBOX = 24
SCALE = FONT_EM / SOURCE_VIEWBOX

icons = {
    0xE000: ("file-archive", "file-archive.svg"),
    0xE001: ("file-audio", "file-audio.svg"),
    0xE002: ("file-document", "file-document.svg"),
    0xE003: ("file-font", "file-font.svg"),
    0xE004: ("file-application", "file-application.svg"),
    0xE005: ("base-disk", "base-disk.svg"),
    0xE006: ("network-disk", "network-disk.svg"),
    0xE007: ("folder-link", "folder-link.svg"),
    0xE008: ("file-link", "file-link.svg"),
    0xE009: ("folder-video", "folder-video.svg"),
    0xE00A: ("desktop", "desktop.svg"),
    0xE00B: ("folder-desktop", "folder-desktop.svg"),
    0xE00C: ("file-alert", "file-alert.svg"),
    0xE00D: ("folder-alert", "folder-alert.svg"),
    0xE00E: ("other-link", "other-link.svg"),
}

glyph_order = [".notdef"] + [name for _, (name, _) in icons.items()]
cmap = {cp: name for cp, (name, _) in icons.items()}

glyphs = {}
metrics = {}

notdef_pen = TTGlyphPen(None)
glyphs[".notdef"] = notdef_pen.glyph()
metrics[".notdef"] = (FONT_EM, 0)

for codepoint, (name, svg_path) in icons.items():
    # First pass: compute the real bounding box of the transformed outline,
    # so we can derive the correct left side bearing instead of assuming 0.
    bounds_pen = BoundsPen(None)
    bounds_transform_pen = TransformPen(bounds_pen, (SCALE, 0, 0, -SCALE, 0, FONT_ASCENT))
    SVGPath(svg_path).draw(bounds_transform_pen)
    xmin, ymin, xmax, ymax = bounds_pen.bounds

    # Second pass: draw the actual glyph outline for the glyf table.
    tt_pen = TTGlyphPen(None)
    quad_pen = Cu2QuPen(tt_pen, max_err=1.0, reverse_direction=False)
    transform_pen = TransformPen(quad_pen, (SCALE, 0, 0, -SCALE, 0, FONT_ASCENT))
    SVGPath(svg_path).draw(transform_pen)

    glyphs[name] = tt_pen.glyph()
    # Left side bearing must match the outline's real xMin, not 0,
    # otherwise hmtx and glyf disagree and some renderers shift the glyph.
    metrics[name] = (FONT_EM, round(xmin))

fb = FontBuilder(unitsPerEm=FONT_EM, isTTF=True)
fb.setupGlyphOrder(glyph_order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=FONT_ASCENT, descent=-FONT_DESCENT, lineGap=0)
fb.setupOS2(
    sTypoAscender=FONT_ASCENT,
    sTypoDescender=-FONT_DESCENT,
    sTypoLineGap=0,
    usWinAscent=FONT_ASCENT,
    usWinDescent=FONT_DESCENT,
    fsSelection=0x0040 | 0x0080,
    sxHeight=0,
    sCapHeight=0,
)
fb.setupNameTable({
    "familyName": "Techsenger Icons MDI",
    "styleName": "Regular",
    "uniqueFontIdentifier": "Techsenger Icons MDI: Regular: 2026",
    "fullName": "Techsenger Icons MDI Regular",
    "psName": "TechsengerIconsMDI-Regular",
    "version": "Version 1.0",
    "manufacturer": "Techsenger",
})
fb.setupPost()

fb.save("techsenger-icons-mdi.ttf")
print("Done: techsenger-icons-mdi.ttf")