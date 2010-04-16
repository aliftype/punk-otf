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

def do_instances(font, instances, tempdir):
    for instance in range(instances):
        instance     = str(instance)
        os.mkdir     (os.path.join(tempdir, instance))
        os.chdir     (os.path.join(tempdir, instance))
        run_mpost    ()
        import_glyphs(font, instance)

def get_alt(name, instances):
    alt = ()
    for i in range(1,instances):
        alt = alt + ("%s.%d" %(name, i),)
    return alt

def add_gsub(font, instances):
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
                glyph.addPosSub("Randomize subtable", get_alt(glyph.glyphname, instances))

def greek_caps(font, instances):
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
        name  = caps[c]
        glyph = font.createChar(-1, c)
        glyph.addReference(name)
        glyph.useRefsMetrics(name)
        glyph.unlinkRef()
        glyph.addPosSub("Randomize subtable", get_alt(name, instances))

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

    do_instances(font, instances, tempdir)
    add_gsub    (font, instances)
    greek_caps  (font, instances)
    autowidth   (font)
    finalise    (font)
    os.chdir    (cwd)

    print "saving font '%s'" % font.fullname
    font.save()
