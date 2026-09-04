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

# Stage a Pages deploy: rebuild the PDF and copy the deploy set into
# pages-staging/ for inspection. (GitLab's `artifacts: export` form lets the
# CI job ship files that are not committed to git; this target simply
# reproduces what the job's script does, locally.)
pages: $(MAIN).pdf
	mkdir -p pages-staging
	cp $(MAIN).pdf pages-staging/
	cp slides.pdf pages-staging/
	cp index.html pages-staging/
	cp VERIFICATION.md pages-staging/VERIFICATION.txt
	@echo "pages-staging/ ready — commit source changes and push; CI ships these files."
