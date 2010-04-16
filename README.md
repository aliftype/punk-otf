The Punk Nova font
==================

This is an OpenType implementation of Donald Knuth's
[Punk font](http://tug.org/TUGboat/Articles/tb09-2/tb21knut.pdf).

Glyph outlines are coded in Metapost, which is then used to generate
the glyphs, 10 variants each, and then FontForge is used to build a font
mapping the glyphs through OpenType Randomize ("rand") feature to be
selected randomly by OpenType engines that support "rand" feature.

The MetaPost source has the following notice:

    This file is a merge of the original punk files by Donald Knuth, who
    added this comment:
    
      Font inspired by Gerard and Marjan Unger's lectures,
      Feb 1985

    The regular punk files are part of TeXLive and in metafont format. All
    errors introduced are ours. We also changed the encoding to unicode. In
    due time we might add a few more more characters. We still need to
    improve some of the metrics which involves a bit of trial and error. The
    font just covers basic latin shapes but in ConTeXt MkIV we add virtual
    composed shapes. There is a module m-punk.tex that implements this. This
    derivate is also used in mk.tex (mk.pdf) which is one of our tests for
    LuaTeX. We published an article on it in the MAPS (NTG magazine).
    
    2008, Taco Hoekwater & Hans Hagen

Khaled Hosny

16 Apr. 2010
