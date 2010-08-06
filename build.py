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
             'outputtemplate:="%c.eps";',
             'input %s;' % file,
             'bye'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=tempdir,
            )

def import_glyphs(font, instance, tempdir):
    print "Importing glyph variants set '%s'" % instance

    glyph_files = glob.glob(os.path.join(tempdir, "*.eps"))

    for file in glyph_files:
        code  = int(os.path.splitext(os.path.basename(file))[0])
        char  = unichr(code)

        if char.isupper() and int(instance) > 15:
            continue

        if not char.isupper() and not char.islower() and int(instance) > 7:
            continue

        if instance == "0":
            glyph = font.createChar(code)
        else:
            glyph = font.createChar(-1, font[code].glyphname+"."+instance)

        glyph.importOutlines(file, ("toobigwarn", "correctdir", "handle_eraser"))

def do_instances(font, instances, mpfile, tempdir):
    for instance in range(instances):
        instance     = str(instance)
        instance_dir = os.path.join(tempdir, instance)
        os.mkdir     (instance_dir)
        run_mpost    (mpfile, instance_dir)
        import_glyphs(font, instance, instance_dir)

def get_alt(code, name):
    instances = 8
    alt       = ()
    char      = unichr(code)

    if char.islower():
        instances = 32
    elif char.isupper():
        instances = 16

    for i in range(1,instances):
        alt = alt + ("%s.%d" %(name, i),)

    return alt

def add_gsub(font, instances):
    print "Adding glyph substitution rules..."

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
                glyph.addPosSub("Randomize subtable",
                        get_alt(glyph.unicode, glyph.glyphname))

def greek_caps(font, instances):
    print "Adding missing Greek capitals..."

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
        glyph.addPosSub("Randomize subtable",
                get_alt(font.createMappedChar(name).unicode, name))

def autowidth(font):
    print "Auto setting side bearings..."

    font.selection.all()
    font.autoWidth(70, 10, 40)
    font.round() # this one is needed to make simplify more reliable
    font.simplify()
    font.removeOverlap()
    font.round()
    font.autoHint()

def autokern(font, instances):
    print "Auto kerning..."

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
        alt = get_alt(font.createMappedChar(a).unicode, a)
        for b in alt:
            list2.append(b)

    list1 = list2

    font.autoKern("Kern subtable", 150, list1, list2, onlyCloser=True)

def finalise(font):
    space         = font.createChar(32)
    space.width   = 400

def usage():
    print "Usage: %s FONTFILE.mp [STYLE]" % sys.argv[1]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit()

    if len(sys.argv) >= 3:
        style = sys.argv[2].title()
    else:
        style = "Regular"

    tempdir   = tempfile.mkdtemp()
    mpfile    = os.path.abspath(sys.argv[1])
    instances = 32

    font      = fontforge.font()

    if style != "Regular":
        font.fontname = "PunkNova-%s"  % style
        font.fullname = "Punk Nova %s" % style
    else:
        font.fontname = "PunkNova"
        font.fullname = "Punk Nova"

    font.familyname = "Punk Nova"
    font.weight     = style
    font.version    = "001.000"
    font.encoding   = "Unicode"
    font.copyright  = "Unlimited copying and redistribution of this file are\
 permitted as long as this file is not modified. Modifications\
 are permitted, but only if the resulting file is not named\
 punknova.otf and the (internal) fontname differs from 'Punk Nova'."

    do_instances(font, instances, mpfile, tempdir)
    add_gsub    (font, instances)
    greek_caps  (font, instances)
    autowidth   (font)
    autokern    (font, instances)
    finalise    (font)

    sh.rmtree   (tempdir)

    filename = "%s-%s.otf" %(font.familyname.replace(" ", "").lower(),
                             style.lower())

    print "Saving file '%s'..." % filename
#   font.save()
    font.generate(filename)
