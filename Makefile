NAME=punknova
SRCNAME=punkfont
VERSION=001.003

SRC=source
TOOLS=tools
DOC=documentation
DOCSRC=$(DOC)/$(DOC)-sources
DIST=$(NAME)-$(VERSION)

FF=$(TOOLS)/build.py

FONTS=regular bold slanted boldslanted
DOCS=sample

MP=$(FONTS:%=$(SRC)/$(SRCNAME)-%.mp)
OTF=$(FONTS:%=$(NAME)-%.otf)
TEX=$(DOCS:%=$(DOCSRC)/%.tex)
PDF=$(DOCS:%=$(DOC)/%.pdf)

all: otf

otf: $(OTF)
doc: $(PDF)

$(NAME)-%.otf: $(SRC)/$(SRCNAME)-%.mp
	@echo "Building $@"
	@$(FF) $< $@ $(VERSION)

$(DOC)/%.pdf: $(DOCSRC)/%.tex
	@echo "Building $@"
	@context --nonstopmode --result=$@ $< 1>/dev/null

dist: $(OTF) $(PDF)
	@echo "Making dist tarball"
	@mkdir -p $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(TOOLS)
	@mkdir -p $(DIST)/$(DOC)
	@mkdir -p $(DIST)/$(DOCSRC)
	@cp $(MP) $(DIST)/$(SRC)
	@cp $(OTF) $(DIST)
	@cp $(FF) $(DIST)/$(TOOLS)
	@cp -r $(PDF) $(DIST)/$(DOC)
	@cp -r $(TEX) $(DIST)/$(DOCSRC)
	@cp -r Makefile NEWS $(DIST)
	@cp README.md $(DIST)/README
	@zip -r $(DIST).zip $(DIST)

clean:
	@rm -rf $(OTF) $(DIST) $(DIST).zip
