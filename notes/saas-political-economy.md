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
