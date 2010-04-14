#!/usr/bin/python

import fontforge
import glob
import os
import subprocess

subprocess.call(["mpost",
	"""&mfplain \mode=localfont; scale_factor:=100.375; outputtemplate:="%4c.eps"; input punkfont.mp; bye"""])


font = fontforge.font()

font.fontname = "PunkNova"
font.fullname = "Punk Nova"
font.encoding = "Unicode"

svg_glyphs    = glob.glob("[0-9][0-9][0-9][0-9].eps")
svg_glyphs.sort()

for i in svg_glyphs:
	number = int(os.path.splitext(i)[0])
	glyph  = font.createChar(number)
	print "importing '%s'" % glyph.glyphname
	glyph.importOutlines(i, ("toobigwarn", "correctdir", "removeoverlap", "handle_eraser"))

print "saving font '%s'" % font.fullname
font.save()
