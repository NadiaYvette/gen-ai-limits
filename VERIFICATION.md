# Reference verification report

## Addendum 2026-09-04: digitale Souveränität expansion (10 entries)

Ten entries were added to §5.2 (service architecture → sovereignty) and
verified on 2026-09-04, bringing the total to 47. Two scholarly entries were
confirmed by Crossref DOI lookup (`references_verified.json`):
`pohle2020sovereignty` (10.14763/2020.4.1532, Internet Policy Review 9(4),
OA landing page) and `couture2019sovereignty` (10.1177/1461444819865984,
New Media & Society 21(10):2305–2322; DBLP returned HTTP 500 during the
session, Crossref is the verification source of record).

Eight are incident/legal/policy items outside the indexes' coverage, verified
by direct inspection of the source during this session:

| Key | What was checked |
|---|---|
| `spiegel2013merkel` | Der Spiegel English edition, 2013-10-27, Berlin embassy story |
| `cryptoag2020rubicon` | Washington Post "The Intelligence Coup of the Century", 2020-02-11 |
| `dunhammer2021spying` | BBC, 2021-05-31, Danish-cables revelation (DR-led coalition) |
| `echelon2001resolution` | European Parliament resolution TA-5-2001-0264, 2001-09-05 |
| `schrems2020judgment` | CJEU C-311/18, Grand Chamber, 2020-07-16, ECLI:EU:C:2020:559 |
| `eu2023dataact` | Regulation (EU) 2023/2854, EUR-Lex ELI page |
| `osor2026schleswig` | EU Interoperable Europe / OSOR progress report |
| `denmark2025open` | The Record, 2025-06-13, Danish digital agency |

**One claim was dropped for verification failure.** The recurring report that
the NSA wiretapped International Criminal Court prosecutors (Bensouda era,
Snowden documents, recalled as Foreign Policy 2015) could not be re-derived
from any reachable source despite repeated targeted searches. It is not
cited. Press bylines were also written conservatively: outlet as author for
items whose bylines were not inspected directly.

The tool's ENTRIES list carried a stale internal key from the original
verification round (`hubert2026alphaproof`); a rerun would have desynchronized
the JSON report from the corrected bib. Fixed in this session; orphan record
removed from the JSON.

## Addendum 2026-09-04 (second): misrepresentation frame (3 entries)

Three arXiv-verified entries added for the new §5.4 (misrepresentation and
the incentive structure), bringing the total to 50. Canonical author lists
harvested from the arXiv API and written to the bib from the verifier output,
not from memory:

| Key | arXiv ID | Status | PDF |
|---|---|---|---|
| `singh2025leaderboard` | 2504.20879 | dblp+arXiv agree (`verified`), NeurIPS 2025 D&B | yes |
| `zhang2024gsm1k` | 2405.00332 | arxiv-matched (DBLP returned 500/503 throughout the session) | yes |
| `sharma2023sycophancy` | 2310.13548 | arxiv-matched (same DBLP outage) | yes |

Quantitative claims in §5.4 (up to 27 private variants; 205/243 silently
deprecated; up to 112% ArenaHard; up to 8% GSM1k drop with the frontier
exception) were extracted from the archived copies via pdftotext, not from
abstracts recalled from memory. The ICC-surveillance claim was re-attempted
(five query strategies + Wayback CDX; the Archive was returning outage pages)
and remains dropped; see `notes/saas-political-economy.md`.

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
