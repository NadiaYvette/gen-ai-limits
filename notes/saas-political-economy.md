# Political economy: service architecture and the research commons

Companion note for §\ref{sec:saas} of `main.tex`. Evidence status is
annotated per item; the intent claim is deliberately left underdetermined.
All references verified 2026-09-03.

## The claim, decomposed

Original intuition: architectural decisions in the recent commercial AI
push preserved Software-as-a-Service structure to the detriment of AI
research and technological development; suspicion that others have
commented; expectation of high falsification potential.

Decomposition:

1. **Serving architecture was selected partly for defensibility.**
   Supported by one internal admission (the leaked Google "no moat" memo)
   and consistent industry behavior (weights withheld, capabilities
   API-only). Cannot be established as a general *motive* from public
   evidence: safety, legal, and moat motives predict the same behavior.
2. **The effect on research is documented and instrumented.**
   Transparency (FMTI: top score 54/100, mean 37%, worst on upstream
   data/compute; declining in 2025), reproducibility (Pozzobon et al.:
   undocumented updates and deprecations invalidate published findings),
   access concentration (Ahmed & Wahed: the compute divide predates and
   structures the SaaS era).
3. **Attribution limits.** The compute divide would gate participation
   even under maximal openness; opacity, compute concentration, and
   benchmark contamination compound. The SaaS choice is one load-bearing
   beam in the research-commons problem, not the whole building.

## Evidence inventory

| Evidence | Status | Source |
|---|---|---|
| Internal moat-reasoning at Google | Leaked memo, one firm, unauthenticable | SemiAnalysis 2023-05-04 |
| Transparency gap, declining trend | Measured, repeated | FMTI 2023; HAI 2025 |
| Reproducibility damage from black-box APIs | Peer-reviewed | Pozzobon et al. EMNLP 2023 |
| Access/compute concentration | Peer-reviewed, pre-ChatGPT | Ahmed & Wahed 2020 |
| Broader ML reproducibility crisis | Peer-reviewed | Kapoor & Narayanan 2023 |

Commentary exists in volume: the memo discourse (Economist leader, May
2023), the de-democratization literature, transparency-index authors, and
reproducibility researchers have all made adjacent arguments. The claim is
not novel; it is now documentable.

## Falsification directions

| Observation | Effect on the claim |
|---|---|
| Frontier releases track safety milestones, not competitive events | Strengthens safety story, weakens moat story |
| Unrestricted frontier open-weights releases persist | Directly undermines moat preservation |
| Antitrust discovery surfaces decision records | Could confirm or kill the intent component |
| Access/reproducibility metrics recover while SaaS persists | Weakens effect attribution |

## Precise formulation for the write-up

> Commercial serving architecture was selected under incentives where
> moat preservation dominated; the selection measurably reduced
> transparency, reproducibility, and independent access, to the
> documented detriment of research. Internal admissions confirm
> moat-reasoning operated at least once. Competing motives (safety,
> legality) partially overlap in observable behavior, so intent is left
> deliberately underdetermined; the measurable detriments are not.

## MOWGLI relevance

MOWGLI's own stack (OmniRoute in front, self-hostable, open weights at
the GPU stage) is a small-scale existence proof of the alternative:
local, inspectable, API-compatible without being API-dependent. The
write-up can note this without overclaiming: the point is feasibility of
the structure, not maturity.

License: documentation → CC BY-SA 4.0 (see `LICENSES.md`).

## Digitale Souveränität addendum (2026-09-04)

Second-order effect added to §5.2 after the first draft: the service model's
consequences were never confined to research. The same architecture sits at
center of the European *digitale Souveränität / souveraineté numérique*
policy turn, whose proximate causes are documented US surveillance incidents:

| Incident | Year | Verified source | Status |
|---|---|---|---|
| NSA monitoring of Merkel's mobile from the Berlin embassy | 2013 | Der Spiegel, 2013-10-27 (Snowden documents) | hand-verified |
| Crypto AG secretly owned by CIA with BND ("Operation Rubicon") | 2020 | Washington Post, 2020-02-11 | hand-verified |
| NSA via Danish cables on European politicians (Operation Dunhammer) | 2021 | BBC / DR-led coalition, 2021-05-31 | hand-verified |
| ECHELON interim report → EP recommends encryption | 2001 | EP resolution TA-5-2001-0264, 2001-09-05 | hand-verified |
| Privacy Shield invalidation on US surveillance law | 2020 | CJEU C-311/18, ECLI:EU:C:2020:559 | hand-verified |

**Dropped for verification failure (recorded as such):** the recurring claim
that the NSA wiretapped ICC prosecutors (Bensouda-era, 2015, Snowden
documents). Multiple targeted searches could not recover the primary story
(recalled as Foreign Policy, 2015), and per this document's verification
discipline an unfindable citation does not ship. If the primary source
resurfaces, it would be the single strongest incident in the table.

**Scholarship and policy:** Couture & Toupin 2019 (concept genealogy,
DOI 10.1177/1461444819865984); Pohle & Thiel 2020 (European framing, DOI
10.14763/2020.4.1532, OA); Schleswig-Holstein migration (EU OSOR 2026);
Denmark digital agency (The Record 2025); EU Data Act, Regulation (EU)
2023/2854 (switching/portability obligations). All verified 2026-09-04.

**The join to AI (text added to §5.2):** generative AI is consumed almost
entirely as a hosted service from a small number of US firms, arriving into
the exact weather these incidents created; research costs and political costs
are two faces of one architecture. The everyday counterpart — services die
with their providers where products do not — is the same risk at commercial
scale, and is precisely what the Data Act's switching provisions legislate
against. Self-hosting + open weights exists as a design-space alternative
(Mowgli cited as a modest existence proof, not a maturity claim).
