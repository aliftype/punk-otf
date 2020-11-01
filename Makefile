NAME=punknova
SRCNAME=punkfont
VERSION=1003

SRC=source
TOOLS=tools
DIST=$(NAME)-$(VERSION)

FF=$(TOOLS)/build.py

FONTS=regular bold slanted boldslanted

MP=$(FONTS:%=$(SRC)/$(SRCNAME)-%.mp)
OTF=$(FONTS:%=$(NAME)-%.otf)

all: otf

otf: $(OTF)

$(NAME)-%.otf: $(SRC)/$(SRCNAME)-%.mp $(MP)
	@echo "Building $@"
	@$(FF) $< $@ $(VERSION)

dist: $(OTF)
	@echo "Making dist tarball"
	@mkdir -p $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(TOOLS)
	@cp $(MP) $(DIST)/$(SRC)
	@cp $(OTF) $(DIST)
	@cp $(FF) $(DIST)/$(TOOLS)
	@cp -r Makefile NEWS $(DIST)
	@cp README.md $(DIST)/README
	@zip -r $(DIST).zip $(DIST)

clean:
	@rm -rf $(OTF) $(DIST) $(DIST).zip
