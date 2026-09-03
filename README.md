# gen-ai-limits

A critical write-up on the limitations of generative AI, in LaTeX.

## Audience and purpose

Written for a less-technical reader whose exposure to AI is primarily
through generative systems of the past decade. The scope spills beyond
generative AI where the same limitation categories apply, but generative
systems remain the anchor. Where findings suggest ways to bulletproof the
companion MOWGLI project (`~/src/logic/`), they are recorded in
`notes/`.

## Layout

```text
main.tex         the document (article class, biblatex/biber)
references.bib   bibliography seed — verify entries before circulating
Makefile         build via latexmk (pdflatex + biber)
LICENSES.md      licensing policy
```

## Building

Requires TeX Live with `latexmk` and `biber`:

```bash
make          # build main.pdf
make view     # build and open a viewer
make clean    # remove auxiliary files
make cleanall # also remove the PDF
```

## Conventions

- Passages that still need substantive work are marked with the `\draft{...}`
  macro so they are visible in red and easy to grep: `grep -n 'draft{' main.tex`.
- Bibliography entries were added from memory as a starting point; verify every
  field against DBLP or the publisher page before citing them in anything
  circulated.

## License

See `LICENSES.md`. In short: source code (Makefile) is EUPL-1.2; the document
text and bibliography are CC BY-SA 4.0, consistent with the MOWGLI project
conventions.
