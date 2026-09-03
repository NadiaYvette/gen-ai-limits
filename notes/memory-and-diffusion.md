# Memory and the generator design space

Companion note for §\ref{sec:memory} and §\ref{sec:alternatives} of
`main.tex`. All references verified 2026-09-03 unless flagged.

## Part 1 — Memory: read side vs. write side

Intuition under test: "models can't remember; context is papered-over
short-term memory; this is all absorbed into the dual-control issue."

The intuition splits cleanly in two:

### Write side (absorbed into dual control, as predicted)

Updating what the system *is* from experience means changing weights while
the system acts — the learning-in-the-loop problem of
`online-neural-control.md`, with all its divergence, non-stationarity, and
plasticity-loss machinery. Serving "memory" by re-reading a context window
is the degenerate zero-learning corner of that same design space: nothing
is consolidated, everything is re-paid per query.

### Read side (a separate category)

Even with weights frozen — no learning, no dual control anywhere in the
picture — the model must *use* what is in its context, and it doesn't, in
two measured ways:

1. **Position pathology** (Liu et al., TACL 12:157–173, 2024): performance
   on retrieval/reasoning over multi-document contexts is U-shaped in
   position. Information at the beginning and end is used; information in
   the middle is substantially missed. More context ≠ more usable context.
2. **Claimed-vs-effective window** (Hsieh et al., RULER, arXiv:2404.06654,
   2024): models advertising 32K+ token contexts frequently fail realistic
   tasks (multi-hop tracing, aggregation) well below the advertised length;
   standard needle-in-a-haystack tests overstate capability because they
   permit shallow matching.

Consequences for the taxonomy:

- Context is **short-term working memory with unmeasured fidelity**, not
  knowledge. The advertised window is a hardware capability; the effective
  window is a behavioral one, and the gap is a genuine limitation category.
- Externalized memory (RAG, memory stores, summarization) does not remove
  the category; it **moves the read-reliability problem into the retrieval
  layer** (recall misses, poisoned entries, stale beliefs, embedding drift)
  and adds write-policy problems (what to keep, what to overwrite).
- Classification: **statistical/architectural**, like hallucination — not
  dynamical. Errors do not circulate; they are present in every forward
  pass.

**MOWGLI implication**: externalize memory into typed, inspectable stores
(event-calculus fluents, annotation records) — already done — and *measure*
read recall against a gold set as a regression test, exactly as the
gold-scene review discipline does for annotations. Never assume the read
path works; test it.

## Part 2 — Diffusion vs. autoregressive generation

Intuition under test: "diffusion models are better in parallelisability,
multimodality, and latency — ultimately better overall."

### Where the claim is right (verified)

| Axis | Evidence |
|---|---|
| Parallelisability | AR: N tokens = N sequential forward passes. Masked diffusion: all positions refined in parallel, steps ≪ N (LLaDA, Mercury) |
| Throughput/latency | Mercury Coder: >1000 tok/s on H100, sub-300 ms TTFT, claimed up to 10× vs speed-optimized AR (arXiv:2506.17298) |
| Multimodality | Diffusion is native to continuous signals (image/audio/video); text is the discrete special case it learned (LLaDA proves masked diffusion scales to 8B on text) |
| Scale viability | LLaDA 8B competitive with LLaMA 3 8B on >2T training tokens — a fraction of LLaMA 3's reported ~15T (verify Meta's figure) — a token-efficiency argument for diffusion |

### Where "better overall" overshoots (as of the verified 2025–26 literature)

1. **Long-context economics.** AR amortizes context through the KV cache:
   after prefill, each emitted token is cheap. Masked diffusion re-attends
   over the full sequence at every refinement step. Mercury's measured wins
   are coding-length outputs; very long contexts and outputs remain
   AR-served territory.
2. **Reasoning-time compute.** o1-style deliberation is long sequential
   chain-of-thought — trivially expressible in AR's left-to-right
   factorization. Diffusion's any-order refinement is structurally suited
   to *self-correction* (revise early tokens without regenerating the
   suffix — AR cannot), but the verified frontier reasoning results are
   still AR-led.
3. **Likelihood machinery.** AR yields exact token-level logprobs; masked
   diffusion yields ELBO bounds. Calibration, routing, distillation, and
   speculative/tooling pipelines built on logprobs remain AR-native.
4. **Frontier gap.** "Competitive with LLaMA 3 8B" is a viability proof at
   the Feb-2024 capability class, not frontier parity.

### Verdict for the write-up

> Better on parallelisability, multimodality, and latency — demonstrated.
> Better overall — a defensible directional thesis whose deciding
> battlegrounds are reasoning-time compute and long-context serving, both
> currently unresolved.

For a non-technical audience: *one kind of model writes left to right like
a typist; the other sculpts the whole answer at once, like developing a
photograph. The sculptor is much faster and handles sound and images
natively; the typist currently reads very long documents more cheaply and
thinks out loud more naturally. Which wins depends on which matters more.*

**MOWGLI implication**: the audio-first, prosody-preserving frontend
(`audio_observation.py`, sidebands kept typed and separate) is well-matched
to diffusion-native multimodal backends; LLaDA is already the designated
GPU-stage dependency. Keep the boundary: diffusion models generate
observations; Mercury reasons over them.

## References (verified 2026-09-03)

- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M.,
  Petroni, F., & Liang, P. (2024). Lost in the middle: How language models
  use long contexts. *TACL*, 12, 157–173.
  https://aclanthology.org/2024.tacl-1.9/ (middle-author order: verify)
- Hsieh, C.-Y., et al. (2024). RULER: What's the real context size of your
  long-context language models? https://arxiv.org/abs/2404.06654
  (full author list: verify against the arXiv page)
- Nie, F., et al. (2025). Large language diffusion models (LLaDA).
  https://arxiv.org/abs/2502.09992 (full author list: verify)
- Inception Labs (2025). Mercury: Ultra-fast language models based on
  diffusion. https://arxiv.org/abs/2506.17298 (author list: verify;
  throughput claims are vendor-reported)

License: documentation → CC BY-SA 4.0 (see `LICENSES.md`).
