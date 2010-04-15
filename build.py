#!/usr/bin/python

import os, sys
import fontforge
import glob
import subprocess
import tempfile

def run_mpost():
    subprocess.call(
            ['mpost',
             '&mfplain',
             '\mode=localfont;',
             'scale_factor:=100.375;',
             'outputtemplate:="%4c.eps";',
             'input %s;' % mpfile,
             'bye']
            )

def import_glyphs(font, instance):
    glyph_files = glob.glob("[0-9][0-9][0-9][0-9].eps")
    glyph_files.sort()

    for file in glyph_files:
        code  = int(os.path.splitext(file)[0])
        if instance == "0":
            glyph = font.createChar(code)
        else:
            glyph = font.createChar(-1, font[code].glyphname+"."+instance)

        print "importing '%s'" % glyph.glyphname

        glyph.importOutlines(file, ("toobigwarn", "correctdir", "removeoverlap", "handle_eraser"))

def do_instances(instances, tempdir, font):
    for instance in range(instances):
        instance     = str(instance)
        os.mkdir     (os.path.join(tempdir, instance))
        os.chdir     (os.path.join(tempdir, instance))
        run_mpost    ()
        import_glyphs(font, instance)

def add_gsub(font):
    font.addLookup(
            "Randomize lookup",
            "gsub_alternate",
            (),
            (
                ('rand',
                    (
                        ('DFLT', ('dflt',)),
                        ('grek', ('dflt',)),
                        ('latn', ('dflt',))
                    )
                ),
            ))
    font.addLookupSubtable("Randomize lookup", "Randomize subtable")

    for glyph in font.glyphs():
        if glyph.unicode != -1:
                n = glyph.glyphname
                glyph.addPosSub("Randomize subtable", (n+".1",n+".2",n+".3",n+".4",n+".5",n+".6",n+".7",n+".8",n+".9"))

def greek_caps(font):
    caps = {
            "Alpha"  : "A",
            "Beta"   : "B",
            "Epsilon": "E",
            "Zeta"   : "Z",
            "Eta"    : "H",
            "Iota"   : "I",
            "Kappa"  : "K",
            "Mu"     : "M",
            "Nu"     : "N",
            "Omicron": "O",
            "Rho"    : "P",
            "Tau"    : "T",
            "Chi"    : "X"
            }
    for c in caps:
        n     = caps[c]
        glyph = font.createChar(-1, c)
        glyph.addReference(n)
        glyph.useRefsMetrics(n)
        glyph.unlinkRef()
        glyph.addPosSub("Randomize subtable", (n+".1",n+".2",n+".3",n+".4",n+".5",n+".6",n+".7",n+".8",n+".9"))

def autowidth(font):
    font.selection.all()
    font.autoWidth(70, 10, 40)

def finalise(font):
    space         = font.createChar(32)
    space.width   = 400

if __name__ == "__main__":
    cwd       = os.getcwd()
    tempdir   = tempfile.mkdtemp()
    mpfile    = os.path.abspath(sys.argv[1])
    instances = 10

    font            = fontforge.font()

    font.fontname   = "PunkNova"
    font.fullname   = "Punk Nova"
    font.familyname = "Punk Nova"
    font.copyright  = ""
    font.version    = "001.000"
    font.encoding   = "Unicode"

    do_instances(instances, tempdir, font)
    add_gsub    (font)
    greek_caps  (font)
    autowidth   (font)
    finalise    (font)
    os.chdir    (cwd)

    print "saving font '%s'" % font.fullname
    font.save()
