NAME=punknova
SRCNAME=punkfont
VERSION=1.103

SRC=source
DIST=$(NAME)-$(VERSION)

FF=./tools/build.py

FONTS=regular bold slanted boldslanted

MP=$(FONTS:%=$(SRC)/$(SRCNAME)-%.mp)
OTF=$(FONTS:%=$(NAME)-%.otf)

all: otf

otf: $(OTF)

$(NAME)-%.otf: $(SRC)/$(SRCNAME)-%.mp
	@echo "Building $@"
	@$(FF) $< $@

dist: $(OTF) $(PDF) FONTLOG.txt
	@echo "Making dist tarball"
	@mkdir -p $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(DOC)
	@mkdir -p $(DIST)/$(DOCSRC)
	@cp $(SFD) $(DIST)/$(SRC)
	@cp $(SRC)/$(FEA) $(DIST)/$(SRC)
	@cp $(OTF) $(DIST)
	@cp -r $(PDF) $(DIST)/$(DOC)
	@cp -r $(TEX) $(DIST)/$(DOCSRC)
	@cp -r Makefile OFL-FAQ.txt OFL.txt FONTLOG.txt tex $(DIST)
	@cp README.md $(DIST)/README.txt
	@zip -r $(DIST).zip $(DIST)

clean:
	@rm -rf $(OTF) $(DIST) $(DIST).zip
