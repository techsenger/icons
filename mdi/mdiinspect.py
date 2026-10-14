# to run the script:
#   sudo apt-get install fontforge
#   fontforge -script mdiinspect.py

import fontforge

font = fontforge.open("materialdesignicons-webfont.ttf")

print("=== Font Metrics ===")
print("EM               :", font.em)
print("Ascent          :", font.ascent)
print("Descent         :", font.descent)
print("OS/2 Typo Ascent:", font.os2_typoascent)
print("OS/2 Typo Descent:", font.os2_typodescent)
print("HHEA Ascent     :", font.hhea_ascent)
print("HHEA Descent    :", font.hhea_descent)
print()

print("=== First 20 Glyphs ===")

count = 0

for glyph in font.glyphs():
    if glyph.unicode >= 0:
        print(f"U+{glyph.unicode:04X}")
        print("  name :", glyph.glyphname)
        print("  width:", glyph.width)
        print("  bbox :", glyph.boundingBox())
        print()
        count += 1
        if count == 20:
            break