# Neurosymbolic structure as a governance prerequisite

Companion note for the neurosymbolic subsection of `main.tex` §"What the
limitations imply". All references verified 2026-09-03.

## The formal core already exists: contextual integrity

Nissenbaum's contextual integrity (CI) is the dominant positive theory of
privacy: privacy = appropriate information flow relative to contextual
norms. Barth, Datta, Mitchell & Nissenbaum (IEEE S&P 2006) formalized CI in
a deontic logic with temporal operators over attributed transmission norms.

Reading the required logic profile off the formalization:

| CI requirement | Logic component | MOWGLI module |
|---|---|---|
| Norms of permitted transmission | Deontic (KD/serial) | `mm_multi` O-type |
| Recipient knowledge/belief | Epistemic/doxastic, agent-indexed | `mm`, `mmb` |
| Roles, groups, senders/receivers | Multi-agent structure | `social_mm` |
| Retention, expiry, re-transmission | Temporality | `ec` (fluents) |
| Leak-path risk, harm probability | Probabilism | `dtmc`, `plp` |
| "Information about whom," portrayals | Semiotic typing | `semio` layer |

The demand profile **is** multi-type multi-agent multimodal logic +
temporality + probabilism. The 2006 result predates the neurosymbolic
revival; the fields have simply not been joined.

## The coherence criterion

Statistical-only guardrails (PII classifiers, moderation models) can produce
instances of protective behavior. What they cannot maintain is *coherence*:

- norm consistency across agents, contexts, and time;
- auditability (which norm fired, with what provenance);
- reversibility (what was transmitted, on whose authority, revocable);
- resistance to Goodharting (no differentiable surface to optimize against).

Privacy protection is a normative function; a corpus gradient can only
imitate descriptions of norms, not apply them. This is the precise sense in
which neurosymbolic structure is a prerequisite for *coherent* attempts —
not merely helpful.

## The semiotic layer as CI's missing type system

CI is criticized as hard to operationalize: "information type in context" is
left informal. Peircean typing supplies the field with provenance:

- **indexical** link (this face ↔ this person) → doxxing/identification
  vector;
- **iconic** rendering (stereotyped portrayal) → representational harm;
- **symbolic** misuse (slurs, insignia, dogwhistles) → norm violation with
  an explicit norm-object.

Semiotic classification turns "what kind of sign is transmitted, about
whom, in which context" into a typed, checkable field. Neither the CI
literature nor the neurosymbolic surveys make this connection; it appears
to be an original contribution available to this write-up (and to MOWGLI).

## Deployment status (corrected claim)

- Narrow symbolic-in-the-loop structure **is** deployed commercially:
  constrained decoding, rule-engine guardrails over LLMs, retrieval
  grounding, formal verification in chips (non-neural).
- Flagship neurosymbolic systems are research-stage: AlphaGeometry
  (Trinh et al., Nature 2024 — neural LM guides a symbolic deduction
  engine); AlphaProof (Hubert et al., Nature 2026 — IMO silver standard,
  formal math).
- The **governance-demanding profile** — normative, multi-agent,
  multimodal, temporal, probabilistic — is deployed nowhere at scale.

Sharp formulation: *narrow hybrids exist; the profile that governance
demands does not.* The absence is the vacuum MOWGLI occupies.

## Machine-ethics mapping

- Arkin's ethical governor (2009): an architectural component that vets
  proposed actions against codified constraints before execution — the same
  slot as MOWGLI's norm-violation-triggered actuation in `grounding_demo`.
- Two-timescale discipline (see `online-neural-control.md`) becomes a
  *safety* property here: norms live outside the trained weights (slow,
  symbolic, inspectable); neural perception stays fast and graded. Dual-
  control divergence and plasticity loss are governance arguments for this
  separation, not merely performance arguments.
- Norm provenance is itself a requirement (Gebru's participatory point):
  whose norms, specified by whom, revisable how. `social_mm` currently has
  no "whose norm is this?" field — a gap worth closing.

## MOWGLI hardening checklist (from this note)

1. `ec.m`: retention/expiry fluent demo with deontic queries
   (`O(not visible_to(strangers))` after tick T).
2. `dtmc.m`: leak-path reachability scenario (P(leak before t)).
3. `social_mm`: norm-provenance field (source, revision, jurisdiction-ish).
4. `semio`: typed sign-class fields for transmitted items (index/icon/
   symbol + subject link), feeding CI-style transmission checks.
5. Keep all normative state out of any trained component (two-timescale /
   governor architecture) — documented as a safety invariant, not a
   performance choice.

## References (verified 2026-09-03)

- Barth, A., Datta, A., Mitchell, J. C., & Nissenbaum, H. (2006). Privacy
  and contextual integrity: Framework and applications. *IEEE Symposium on
  Security and Privacy*, 184–193.
  https://crypto.stanford.edu/portia/pubs/articles/BDMN811702440.html
- Nissenbaum, H. (2009). *Privacy in Context*. Stanford University Press.
- Garcez, A. d'Avila, & Lamb, L. C. (2023). Neurosymbolic AI: the 3rd wave.
  *Artificial Intelligence Review*, 56(11), 12387–12406.
  https://arxiv.org/abs/2012.05876
- Trinh, T. H., et al. (2024). Solving olympiad geometry without human
  demonstrations. *Nature*, 625, 683–689 (pages: verify).
  https://research.google/pubs/solving-olympiad-geometry-without-human-demonstrations/
- Hubert, T., et al. (2026). Olympiad-level formal mathematical reasoning
  with AlphaProof. *Nature* (volume/pages: verify).
  https://www.nature.com/articles/s41586-025-09833-y
- Arkin, R. C. (2009). *Governing Lethal Behavior in Autonomous Robots*.
  Chapman & Hall/CRC.
  Governor tech report:
  https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1166&context=csetechreports

License: documentation → CC BY-SA 4.0 (see `LICENSES.md`).
