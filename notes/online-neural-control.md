# Learning in the loop: why "neural network + online optimal control" fails

Companion research note for §\ref{sec:learning-in-the-loop} of `main.tex`.

## The scheme under examination

A neural network acts as the controller, value function, or dynamics model,
and its weights are updated online from data gathered while it controls the
plant. The question: does the natural joint adaptation scheme work?

**Answer: no, and the failures are proven, named, and mechanistically
understood.** The failure is not one category but an *intersection* of
several; the one genuinely recent addition is *plasticity loss*. The
classical umbrella that predicts all of it is dual control.

## Mechanism 1 — Divergent updates (the deadly triad)

Bootstrapping + function approximation + off-policy data diverges *provably*:

- Baird (1995): divergence with **linear** function approximation and exact
  dynamic-programming updates — the minimal counterexample.
- Tsitsiklis & Van Roy (1997): convergence of TD(0) with linear approximation
  holds **only on-policy** (updates along trajectories of the Markov chain).
  Off-policy, the projected Bellman operator is no longer a contraction with
  respect to the projected norm, and the fixed point can vanish or repel.
- van Hasselt et al. (2018): systematic empirical anatomy in deep RL.

Mechanism: bootstrapping makes the regression target a function of the
current parameters (moving target). Off-policy data breaks the stationary-
distribution assumption that makes the self-reference contract. Estimation
error amplifies through self-reference — positive feedback rather than
averaging.

## Mechanism 2 — The controller poisons its own data distribution

The data distribution is a function of the current policy; learning changes
the policy, which changes the distribution, which changes learning. The
coupled system has bad attractors:

- Primacy bias (Nikishin et al., ICML 2022): agents overfit their earliest
  experiences; later evidence barely moves them; periodic resets outperform.
  Early gradient dynamics select the loss-landscape basins occupied forever
  after.
- Catastrophic forgetting (French, 1999): overlapping representations +
  shifting input distributions = overwrite. A control loop shifts the
  distribution *continuously* as behavior improves, so interference is
  chronic, not episodic.
- **Loss of plasticity** (Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood,
  Sutton; Nature 632:768–774, 2024): networks trained through continual task
  changes stop learning *entirely* — no better than a shallow network — even
  without forgetting. Remedied only by continual reinjection (Shrink &
  Perturb). This is degradation of the **capacity to learn**, a third
  failure distinct from divergence and forgetting.

## Mechanism 3 — Model exploitation (learned dynamics models)

Janner et al. (NeurIPS 2019, "When to Trust Your Model"): a policy optimized
against a learned model seeks out exactly the states where the model's
extrapolations are most flattering; long synthetic rollouts visit regions the
real system never exhibits. Working remedy: very short rollouts branched from
*real* states. This is Goodharting one's own model — objective misspecification
under optimization pressure.

## Mechanism 4 — Dual control is intractable

Feldbaum (1960s) named the coupling: actions affect both the plant state and
the information state (what is learned). The optimal solution must trade
probing cost against information gain. Wittenmark (1995) surveys the field:
even linear-Gaussian systems with unknown parameters yield a nonlinear,
effectively infinite-dimensional belief-state problem; only approximations
are practical (certainty equivalence, cautious control, explicit probing).
"Let the network learn while it controls optimally" requests the intractable
optimum in its least tractable form (nonlinear function approximation).

## What the theory says can work

- **Two-timescale stochastic approximation** (Borkar, 1997): if the learner's
  stepsize is asymptotically smaller than the controller's, the fast loop
  sees the slow loop as quasi-static and the ODE method gives convergence.
  Formalizes: *adapt slowly, control fast*; separate estimation from action.
- **Persistent excitation** (classical adaptive control): parameters converge
  only with sufficient probing; probing costs performance. The dual tradeoff
  cannot be abolished, only managed.
- Engineering mitigations, each patching one mechanism: target networks +
  replay (lag the target — a crude two-timescale), resets (Nikishin),
  shrink-and-perturb (Dohare), short model rollouts (Janner), robust/cautious
  MPC.
- The MOWGLI `control_filter` design (exact Bayesian filter, threshold-
  triggered discrete actions, **no** continuously-updated in-loop weights)
  sidesteps the trap entirely. The literature's verdict: that separation is
  the right call.

## Categorization for the write-up

| Component | Status |
|---|---|
| Self-referential-target divergence | Established (1995–1997) |
| Behavior-induced non-stationarity | Established |
| Plasticity loss | Recently named and measured (2023–2024) |
| Objective misspecification (model exploitation) | Established (Goodhart) |
| Umbrella theory | Classical: dual control + two-timescale SA |

Distinguishing feature of the category: **dynamical** failure (errors
circulate through feedback) vs. the **statistical** failures that dominate
the rest of the write-up (errors average out over samples). Filed in
`main.tex` as its own subsection for exactly this reason.

## References (verified 2026-09-03)

- Baird, L. C. III (1995). Residual algorithms: Reinforcement learning with
  function approximation. *ICML 1995*, 30–37.
  https://link.springer.com/chapter/10.1007/3-540-59102-3_39
- Tsitsiklis, J. N., & Van Roy, B. (1997). An analysis of temporal-difference
  learning with function approximation. *IEEE Transactions on Automatic
  Control*, 42(5), 674–690.
  https://web.mit.edu/dimitrib/www/TD_Policy_Eval_04.pdf (related lecture)
- van Hasselt, H., Doron, Y., Strub, F., Hessel, M., Mitra, N., & Bellemare,
  M. G. (2018). Deep reinforcement learning and the deadly triad.
  https://arxiv.org/abs/1812.02648
- Nikishin, E., Schwarzer, M., D'Oro, M., Courville, A., & Bacon, P.-L.
  (2022). The primacy bias in deep reinforcement learning. *ICML 2022*.
  https://arxiv.org/abs/2205.07802
- French, R. M. (1999). Catastrophic forgetting in connectionist networks.
  *Trends in Cognitive Sciences*, 3(4), 128–135.
  https://doi.org/10.1016/S1364-6613(99)01294-2
- Dohare, S., Hernandez-Garcia, J. F., Lan, Q., Rahman, P., Mahmood, A. R., &
  Sutton, R. S. (2024). Loss of plasticity in deep continual learning.
  *Nature*, 632(8026), 768–774.
  https://www.nature.com/articles/s41586-024-07711-7
- Janner, M., Fu, J., Zhang, M., & Levine, S. (2019). When to trust your
  model: Model-based policy optimization. *NeurIPS 32*.
  https://proceedings.neurips.cc/paper/2019/hash/5faf461eff3099671ad63c6f3f094f7f-Abstract.html
- Wittenmark, B. (1995). Adaptive dual control methods: An overview. *IFAC
  Symposium on Adaptive Systems in Control and Signal Processing*.
  https://www.researchgate.net/publication/3352290_Survey_of_adaptive_dualcontrol_methods
- Borkar, V. S. (1997). Stochastic approximation with two time scales.
  *Systems & Control Letters*, 33, 9–13 (as commonly cited).
  https://www.sciencedirect.com/science/article/pii/S0167691197900153

License: documentation → CC BY-SA 4.0 (see `LICENSES.md`).
