# Reference verification report

All 37 bibliography entries were verified on **2026-09-03** by
`tools/verify_references.py` against DBLP, the arXiv API, and Crossref
(raw results in `references_verified.json`).

| Status | Count | Meaning |
|---|---:|---|
| dblp-matched | 15 | Title match >= 0.82 on DBLP; metadata from DBLP |
| arxiv-matched | 11 | Verified against the arXiv API (title + authors) |
| verified | 3 | DBLP and arXiv agree |
| crossref-matched | 5 | Verified against a known DOI on Crossref |
| manual | 3 | Books / newsletter item (no index); checked by hand |

Rerun anytime with:

```bash
python3 tools/verify_references.py --download
```

Results are cached in `cache/`, so reruns only hit the network for entries
whose status is not yet final or whose PDF is missing.

## Errors the verification caught (and fixed)

The seed bibliography was written from memory; the verifier found real
errors, exactly as intended:

1. **Wrong arXiv ID (Valmeekam et al., planning).** `2210.05575` is an
   intracranial-aneurysm mechanics paper. The correct NeurIPS 2023 paper's
   arXiv ID is `2302.06706`. The wrongly downloaded PDF was deleted and
   re-fetched from the NeurIPS hash URL.
2. **Wrong arXiv ID (Dziri et al., Faith and Fate).** `2210.05618` resolves
   to an unrelated stochastic-gradient paper; the PDF was re-fetched from
   the correct NeurIPS hash URL. No arXiv ID is now asserted in the bib.
3. **Wrong author list (van Hasselt et al., deadly triad).** The actual
   authors are van Hasselt, Doron, Strub, Hessel, **Sonnerat, Modayil** —
   not "Mitra".
4. **Wrong year and title (AlphaProof).** The paper is *"Olympiad-level
   formal mathematical reasoning **with reinforcement learning**"*, Nature
   **651**(8106):607–613, **2025** — not "with AlphaProof", 2026.
5. **Wrong page span (Barth et al. 2006).** 184–198, not 184–193.
6. **Wrong pages (AlphaGeometry).** 625(7995):476–482, not 468–474.
7. **Wrong issue (Kapoor & Narayanan).** Patterns 4(9), e100804, not 4(7).
8. **Wrong first-author key fields (Mercury).** Author is Khanna et al.
   (Inception Labs team), not a corporate author; arXiv:2506.172**98**,
   not 17269.
9. **Bender & Koller DOI.** 10.18653/v1/2020.acl-main.463 (a guessed
   earlier number resolved to an unrelated paper — caught by probing).
10. **Ji et al. pages.** ACM Computing Surveys article number 248:1–248:38,
    not 1–38.
11. **Title casing corrections** from DBLP canonical metadata throughout.

## Known non-verifiable entries

| Entry | Note |
|---|---|
| `nissenbaum2009privacy` | Book (Stanford University Press); checked by hand |
| `arkin2009governing` | Book (Chapman & Hall/CRC); checked by hand |
| `patel2023nomoat` | Leaked memo published by SemiAnalysis; cited as `@misc` with URL |

## Open-access PDFs

25 PDFs were downloaded into `pdfs/` (gitignored; see
`pdfs/manifest.json` for source URL + sha256 of each). Sources: arXiv,
NeurIPS proceedings, PMLR, ACL Anthology, Nature (OA articles), and
Unpaywall-reported locations. Vendor-403/404 fallbacks were handled by
hardcoding known OA locations (e.g., PMLR v162 for Nikishin et al.).

Redistribution note: these copies are for personal reading. Licenses vary
(CC BY, CC BY-NC, publisher terms); `pdfs/` is deliberately not in git.

## Caveats

- DBLP rate-limits aggressively; the tool backs off, caches, and resumes.
- Title matching uses normalized similarity >= 0.82 plus a reject-list for
  known confusable titles (e.g., the two "Lost in the Middle..." papers).
  Two near-miss incidents during development are recorded here as evidence
  the guard is necessary.
- The `liu2024lost` DOI (10.1162/tacl_a_00638) is taken from the MIT Press
  TACL page listing; the anthology URL is 2024.tacl-1.9.
