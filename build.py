#!/usr/bin/python

import os, sys
import fontforge
import glob
import subprocess
import tempfile
import shutil as sh

def run_mpost(file, tempdir):
    subprocess.call(
            ['mpost',
             '&mfplain',
             '\mode=localfont;',
             'scale_factor:=100.375;',
             'outputtemplate:="%4c.eps";',
             'input %s;' % file,
             'bye'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=tempdir,
            )

def import_glyphs(font, instance, tempdir):
    print "Importing instance '%s'" % instance

    glyph_files = glob.glob(os.path.join(tempdir, "[0-9][0-9][0-9][0-9].eps"))

    for file in glyph_files:
        code  = int(os.path.splitext(os.path.basename(file))[0])
        if instance == "0":
            glyph = font.createChar(code)
        else:
            glyph = font.createChar(-1, font[code].glyphname+"."+instance)

        glyph.importOutlines(file, ("toobigwarn", "correctdir", "removeoverlap", "handle_eraser"))
        glyph.round()

def do_instances(font, instances, mpfile, tempdir):
    for instance in range(instances):
        instance     = str(instance)
        instance_dir = os.path.join(tempdir, instance)
        os.mkdir     (instance_dir)
        run_mpost    (mpfile, instance_dir)
        import_glyphs(font, instance, instance_dir)

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

def autokern(font, instances):
    font.addLookup(
            "Kern lookup",
            "gpos_pair",
            (),
            (
                ('kern',
                    (
                        ('DFLT', ('dflt',)),
                        ('grek', ('dflt',)),
                        ('latn', ('dflt',))
                    )
                ),
            ))
    font.addLookupSubtable("Kern lookup", "Kern subtable")

    list1 = ["A", "V", "a", "v", "W", "w", "o", "O", "T", "L", "Y", "l", "y"]
    list2 = [ ]

    for a in list1:
        list2.append(a)
        alt = get_alt(a, instances)
        for b in alt:
            list2.append(b)

    list1 = list2

    print "Auto kerning\t'%s'" % font.fullname
    font.autoKern("Kern subtable", 150, list1, list2, onlyCloser=True)

def finalise(font):
    space         = font.createChar(32)
    space.width   = 400

if __name__ == "__main__":
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

    do_instances(font, instances, mpfile, tempdir)
    add_gsub    (font, instances)
    greek_caps  (font, instances)
    autowidth   (font)
    autokern    (font, instances)
    finalise    (font)

    sh.rmtree   (tempdir)

    print "Saving font\t'%s'" % font.fullname
    font.save()
    font.generate(font.fontname+".otf")
