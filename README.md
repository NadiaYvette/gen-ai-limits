# gen-ai-limits

**The Limitations of Generative AI** — a lay-readable, citation-verified
survey in LaTeX.

## Audience and purpose

Written for a less-technical reader whose exposure to AI is primarily through
generative systems of the past decade. The document catalogues what
generative systems systematically cannot do, and sorts every limitation into
one of three families with different remedies:

| Family | Signature | Matching remedy |
|---|---|---|
| Statistical | errors average out over samples | better data, better measurement |
| Dynamical | errors circulate through feedback | architectural separation of learning from acting |
| Normative | the violated rule cannot even be represented | inspectable, typed structure outside the trained weights |

Most announced fixes fail, on this accounting, by offering a statistical
remedy for a dynamical or normative problem.

## Verification discipline

Every bibliography entry was checked against public indexes (DBLP, the arXiv
API, Crossref) by `tools/verify_references.py` — the raw machine-readable
results ship in `references_verified.json`, and the full report including the
errors that verification caught is in
[`VERIFICATION.md`](VERIFICATION.md). Open-access copies of 29 cited papers
are archived (gitignored) in `pdfs/` with sha256 hashes and source URLs
pinned in `pdfs/manifest.json`. Claims in the text are separated into what is
*observed*, what is *explained*, and what is merely *narrated*. Two claims
that failed verification — an arXiv ID that resolved to an unrelated paper,
and a widely-repeated surveillance report (ICC prosecutors) whose primary
source could not be re-derived — are documented as dropped, not cited.

## Layout

```text
main.tex                    the document (article class, biblatex/biber)
references.bib              verified bibliography (50 entries)
references_verified.json    raw verification results per entry
VERIFICATION.md             verification report and corrections log
notes/                      research notes backing each section
tools/verify_references.py  rerunnable citation checker
pdfs/                       local OA reading copies (gitignored, hashed)
index.html                  landing page for the published PDF
.gitlab-ci.yml              publishes main.pdf via GitLab Pages (framagit)
Makefile                    build via latexmk (pdflatex + biber)
LICENSES.md                 licensing policy
```

## Reading it

The current build is published on framagit's GitLab Pages:

> **https://nadiayvette.framagit.io/gen-ai-limits/main.pdf**

(with a landing page at the site root). Pages deploys from the `main`
branch on push; the PDF in git is the artifact of record. For a citable,
versioned DOI, the recommended path is [Zenodo](https://zenodo.org):
sign in via ORCID, create a **new versioned upload** pointing at the GitHub
mirror (`NadiaYvette/gen-ai-limits`), and reserve a DOI — Zenodo mints a
fresh version DOI on each GitHub release and keeps a concept DOI that always
targets the latest. This is done once from the web UI (no API key needed in
this repo) and needs no changes to the document itself.

## Building

Requires TeX Live with `latexmk` and `biber`:

```bash
make          # build main.pdf
make view     # build and open a viewer
make clean    # remove auxiliary files
make cleanall # also remove the PDF
```

## Related project

The companion [MOWGLI](https://git.sr.ht/~nadiayvette/mowgli) project
implements the multi-type multi-agent multimodal logic profile that the
normative-failure family argues governance demands — see the neurosymbolic
section of the document. The projects are separate repositories with separate
histories; they share only licensing conventions.

## Mirrors

| Forge | URL |
|---|---|
| Sourcehut | https://git.sr.ht/~nadiayvette/gen-ai-limits |
| Framagit | https://framagit.org/NadiaYvette/gen-ai-limits |
| Disroot | https://git.disroot.org/NadiaYvette/gen-ai-limits |
| GitCode | https://gitcode.com/NadiaYvette/gen-ai-limits |
| GitHub | https://github.com/NadiaYvette/gen-ai-limits |
| Radicle | `rad:zZxJXEHTX81NfbRWw2jLXCp5vgLi` |

## License

See [`LICENSES.md`](LICENSES.md). In short: document text and research notes
are **CC BY-SA 4.0** (the primary license — this is a documentation work);
bibliographic metadata and verification data are CC BY 4.0; build tooling is
EUPL-1.2. Cited papers remain under their own copyrights.
