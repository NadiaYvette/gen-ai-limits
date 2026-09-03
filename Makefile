# Makefile — build the write-up with latexmk (pdflatex + biber).

MAIN        = main
LATEXMK     = latexmk
LATEXMKFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all view clean cleanall

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib
	$(LATEXMK) $(LATEXMKFLAGS) $(MAIN).tex

view: $(MAIN).pdf
	$(LATEXMK) -pdf -interaction=nonstopmode -pv $(MAIN).tex

clean:
	$(LATEXMK) -c $(MAIN).tex
	rm -f $(MAIN).run.xml

cleanall: clean
	$(LATEXMK) -C $(MAIN).tex
