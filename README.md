# gen-ai-limits

**The Limitations of Generative AI** — a lay-readable, citation-verified
survey in LaTeX.

Author: Nadia Yvette Chambers — [ORCID 0009-0009-7073-1726](https://orcid.org/0009-0009-7073-1726)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22294860.svg)](https://doi.org/10.5281/zenodo.22294860)

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
*observed*, what is *explained*, and what is merely *narrated*. Three claims
that failed verification — an arXiv ID that resolved to an unrelated paper,
a widely-repeated 2015 report that NSA wiretaps reached ICC prosecutors
whose primary source could not be re-derived despite repeated search
strategies, and one URL guessed from memory that resolved to an unrelated
paper — are documented as dropped, not cited. One *related but distinct*
claim — Israeli intelligence surveillance of ICC staff, documented by +972
Magazine, Local Call, and the Guardian in 2024 — *was* verified and appears
in §5.2; the dropped NSA-2015 item should not be confused with it.

## Layout

```text
main.tex                    the document (article class, biblatex/biber)
main.pdf                    committed build (artifact of record, served by Pages)
slides.tex                  companion beamer deck for giving the talk
slides.pdf                  committed build of the deck (served by Pages)
references.bib              verified bibliography (51 entries)
references_verified.json    raw verification results per entry
VERIFICATION.md             verification report and corrections log
notes/                      research notes backing each section
tools/verify_references.py  rerunnable citation checker
pdfs/                       local OA reading copies (gitignored, hashed)
index.html                  landing page for the published PDF
.gitlab-ci.yml              publishes main.pdf via GitLab Pages (framagit)
Makefile                    build via latexmk (pdflatex + biber); `make pages` refreshes the deploy set
LICENSES.md                 licensing policy
.zenodo.json                Zenodo deposit metadata (used by the GitHub integration)
```

## Reading it

The current build is published on framagit's GitLab Pages:

> **https://nadiayvette.frama.io/gen-ai-limits/main.pdf**

(with a landing page at the site root). The built `main.pdf` is committed and
acts as the artifact of record; the `pages` job ships it (plus the landing
page and this verification report) on every push to `main`, so a plain push
deploys. If you edit the document, rebuild with `make pages` before pushing
so the committed PDF matches the source.

For a citable, versioned DOI, the recommended path is
[Zenodo](https://zenodo.org)'s GitHub integration: sign in via ORCID,
enable the GitHub mirror (`NadiaYvette/gen-ai-limits`) in
zenodo.org/account/settings/github, and **release a tag** — Zenodo then
mints a fresh version DOI per release under a concept DOI that always
targets the latest.Deposit metadata (title, creator, license, keywords)
preloads from `.zenodo.json`, so the first deposit needs no manual entry.
Note the asymmetry: **framagit is the canonical git URL** (used in the
document's footnotes and the Pages deploy), but **GitHub releases are what
trigger the DOI minting** — if GitHub were ever unavailable, the fallback is
a manual deposit upload at zenodo.org, which changes nothing else here.

### Versioning policy

Each release tag mints a permanent, frozen version DOI: versions can be
added but never removed or re-pointed, and Zenodo deduplicates unchanged
files, so the real cost of a version is *citation surface*, not storage.
Accordingly:

- **Tag a version only when the state is one you would be comfortable
  having cited and frozen forever.** This is the single filter; everything
  below derives from it.
- **Tag substance, not noise.** A new section, newly verified claims, or a
  correction that changes an argument (minor for additions, major for
  restructurings or claim reversals, patch sparingly for corrections worth
  freezing). Typos, formatting, and infrastructure work are batched into
  the next substantive version.
- **Metadata-only fixes mint nothing.** Title, keyword, and description
  edits happen in place on the deposit without a new DOI; versions are for
  *file* changes.
- **Cite the version DOI** when reproducibility matters; the concept DOI
  suffices for "the document, current". A handful of substantive versions
  a year is a realistic cadence for a living survey; there is no technical
  ceiling on version count, only permanence.
- Because `main.pdf` is committed, every tag's frozen PDF sits in git
  history too, so the DOI'd deposit and the tagged repo state are
  byte-identical by construction.

**Zenodo**: the concept DOI **10.5281/zenodo.22294860** (badge above) always
resolves to the latest frozen version; **10.5281/zenodo.22294861** is the
v1.0.0 version DOI. The concept DOI is the one embedded in the document's
own footnote and on the slide deck's title slide, since it survives future
versions. New release tags mint new version DOIs automatically via the
GitHub integration.

## Building

Requires TeX Live with `latexmk` and `biber`:

```bash
make          # build main.pdf
make view     # build and open a viewer
make clean    # remove auxiliary files
make cleanall # also remove the PDF
```

## Related project

The companion [MOWGLI](https://framagit.org/NadiaYvette/mowgli) project
implements the multi-type multi-agent multimodal logic profile that the
normative-failure family argues governance demands — see the neurosymbolic
section of the document. The projects are separate repositories with separate
histories; they share only licensing conventions.

## Mirrors

| Forge | URL |
|---|---|
| Framagit *(canonical — used in the document and Pages)* | https://framagit.org/NadiaYvette/gen-ai-limits |
| Sourcehut | https://git.sr.ht/~nadiayvette/gen-ai-limits |
| Disroot | https://git.disroot.org/NadiaYvette/gen-ai-limits |
| GitCode | https://gitcode.com/NadiaYvette/gen-ai-limits |
| GitHub *(releases drive the Zenodo DOI)* | https://github.com/NadiaYvette/gen-ai-limits |
| Radicle | `rad:zZxJXEHTX81NfbRWw2jLXCp5vgLi` |

## License

See [`LICENSES.md`](LICENSES.md). In short: document text and research notes
are **CC BY-SA 4.0** (the primary license — this is a documentation work);
bibliographic metadata and verification data are CC BY 4.0; build tooling is
EUPL-1.2. Cited papers remain under their own copyrights.
