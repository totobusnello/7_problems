# The Unit Gap Is Base-Dependent: A Mechanically Verified Refutation and a Cross-Base Census

<!-- DRAFT v0 (2026-07-15) — INTERNO, NÃO SUBMISSÃO. Redação em curso; submissão exige OK de Luiz
     + 10_PUBLICATION_RULES + janela de resposta da issue krinkin/unit-gap#1. Título alternativo:
     "Formula-vs-Circuit Gaps Depend on the Basis". Venue provável: arXiv cs.CC. -->

## Abstract

Krinkin's *The Unit Gap* (arXiv:2603.08033) asserts that for every Boolean function the minimum
formula size exceeds the minimum circuit size by at most one gate — Theorem 2: `gap ∈ {0,1}` in the
And-Inverter Graph (AIG) cost model — with a structural corollary bounding a "sharing term"
`s ∈ {0,1}` (Corollary 6). We refute both. Under the paper's own verbal definition of a formula
(every gate has fan-out one), the parity of three variables is a counterexample: `opt(⊕₃) = 6` —
UNSAT at five gates, certified by a DRAT proof checked with drat-trim — while `tree(⊕₃) = 9`, giving
gap 3; the optimal six-gate circuit shares a three-gate sub-DAG between the two children of its
output gate, giving `s = 3`. Khrapchenko's classical bound independently forces `tree(⊕₃) ≥ 8`, so
`gap ≥ 2` survives even if every computation above were wrong. The counterexample is formalized in
Lean 4. The error in the published proof is a type confusion in the recursion for `tree(f)`: the
displayed identity minimizes `1 + opt(a) + opt(b)` over decompositions, silently allowing
internally-shared children inside an object that the definition requires to be a tree. An exhaustive
census over the 222 NPN classes of `n = 4` shows the failure is structural, not incidental: 72/222
classes (32.4%) have `gap ≥ 2`, the maximum gap 6 attained exactly by parity-4 and its two NPN
relatives, where the formula lower bound `tree(⊕₄) = 15` meets Khrapchenko's bound with equality.
Finally, we show the phenomenon is **base-dependent**. Repeating the census in the XOR-AND-graph
(XAG) basis, the unit-gap property *holds*: `gap_XAG = 0` for all 256 functions of `n = 3` and
`gap_XAG ∈ {0,1}` for all 222 classes of `n = 4`; a directed sample of 29,643 functions of `n = 5`
(biased toward likely separators) yields **no function with `gap_XAG ≥ 2`**. The large AIG gaps are
precisely the cost of simulating linear (parity) structure in a basis without XOR. A replicated MIG
census matching Soeken et al.'s published table class by class validates the synthesis pipeline
externally.

## 1. Introduction

The relationship between **formula size** (the smallest fan-out-one circuit computing a function)
and **circuit size** (the smallest circuit of any fan-out) is one of the oldest quantitative
questions in Boolean complexity. Formula size is a tree measure; circuit size is a DAG measure;
their difference measures how much *sharing* — reusing an intermediate result at more than one place
— can buy. A recent preprint, Krinkin's *The Unit Gap* (arXiv:2603.08033), makes a strong claim
about this difference: in the And-Inverter Graph model, the gap is **at most one gate** for every
Boolean function (Theorem 2), with a companion structural bound on the amount of sharing in an
optimal circuit (Corollary 6). If true, this would be a surprisingly tight universal statement.

It is not true. This paper does three things.

1. **We refute Theorem 2 and Corollary 6** with a certified counterexample at `n = 3` (parity), where
   the gap is 3 and the sharing term is 3. The lower bound on circuit size is a DRAT proof checked by
   an independent tool; the formula size is confirmed both by dynamic programming and by a Lean 4
   formalization; and an entirely analytic bound (Khrapchenko) forces the gap to be at least 2
   regardless of any computation. We also locate the exact error in the published proof: a type
   confusion that puts the DAG measure `opt` inside a recursion whose defining object is a tree.

2. **We show the failure is structural, not a lucky counterexample**, by computing the complete gap
   census over all 222 NPN-equivalence classes of `n = 4`: nearly a third of all functions violate
   the unit-gap bound, and the extremal case is exactly parity, where the formula lower bound meets
   Khrapchenko's bound with equality.

3. **We show the phenomenon is base-dependent.** The unit-gap property, false in AIG, *holds*
   empirically in the XOR-AND-graph basis for `n ≤ 4` (exhaustive) and for a large directed sample at
   `n = 5`. The AIG gaps are the price of simulating parity without a native XOR gate; once XOR is in
   the basis, sharing buys at most one gate at these sizes. Krinkin's structural intuition survives
   in a richer basis at small `n`; his theorem, in his own basis, does not.

Our method throughout is **exact synthesis via SAT**: for each function and each candidate size `k`
we encode "is there a `k`-gate circuit for `f`?" as a CNF and decide it with a modern solver, taking
the smallest satisfiable `k` as the exact optimum. Optimality claims are lower bounds and therefore
rest on UNSAT; the load-bearing ones are backed by DRAT certificates. Formula sizes use the same
encoder restricted to fan-out one. The refutation package was reviewed adversarially by four
independent language-model families before external communication; the mathematical claims stand on
the certificates, not on that review. We claim novelty only for the refutation and for the
gap-by-basis census; the individual optimal-size tables in XAG and MIG are classical or previously
published, and we say so.

## 2. Preliminaries

An **AIG** over `x₁,…,xₙ` is a circuit of 2-input AND gates with free negations on edges and on the
output; its **size** is the number of gates. A **formula** (tree) is a circuit in which every gate
has fan-out one. We write `tree(f)` and `opt(f)` for the minimum formula and minimum circuit size,
and `gap(f) = tree(f) − opt(f)`. Both measures are invariant under negating inputs, permuting
inputs, and negating the output (NPN-invariance), so censuses range over NPN classes. An **XAG**
adds a native 2-input XOR gate (negations on XOR inputs normalize away, since `¬a ⊕ b = ¬(a ⊕ b)`);
an **MIG** uses 3-input majority gates with edge negations and constant inputs. All exhaustive
results below are for `n ≤ 4` and make no claim for general `n`.

**Exact synthesis.** For fixed `(n, k)` we introduce a Boolean variable for the truth value of each
gate on each of the `2ⁿ` input rows and one-hot selection variables choosing each gate's operation
and its two operands among earlier nodes; clauses enforce the gate semantics, that every non-output
gate is used, and that the output computes `f` up to polarity. `f` has a `k`-gate circuit iff the
CNF is satisfiable. Ascending `k = 0,1,2,…`, the first satisfiable `k` is `opt(f)`; the preceding
UNSAT certifies the lower bound. Restricting selection so that every internal gate has exactly one
consumer (fan-out one, no deduplication of identical sub-results) turns the same encoder into an
exact `tree(f)` oracle. The encoders are validated by gates described in Appendix B.

## 3. The refutation at n = 3

**Theorem 2 of arXiv:2603.08033 is false under the paper's definition of a formula.** The paper
defines a formula verbally as fan-out-one ("a tree") and then displays the recursion

> `tree(f) = min over f = a ∧ b (or f̄ = a ∧ b) of ( 1 + opt(a) + opt(b) )`,

with **`opt`**, not **`tree`**, on the right-hand side. With `opt` in the children, the trivial
decomposition `f = 1 ∧ f` already yields `tree(f) ≤ 1 + opt(f)` for every `f` — so the "theorem" is
an artifact of the displayed identity, which measures the cost of a *single* top-level decomposition
with optimally-shared children, not formula size. Under the verbal definition the recursion must be
`tree(f) = min ( 1 + tree(a) + tree(b) )`, with the tree measure on both sides. For parity of three
variables these two readings diverge sharply.

- **`opt(⊕₃) = 6`.** *Upper bound:* an explicit six-gate circuit (two chained XOR blocks sharing the
  middle node), verified by simulation. *Lower bound:* UNSAT at `k = 5` (kissat 4.0.4), with a DRAT
  proof (147 KB) checked by drat-trim (`s VERIFIED`); regeneration is byte-identical.
- **`tree(⊕₃) = 9`.** *Upper bound:* an explicit nine-gate formula (duplicate the `x₁ ⊕ x₂`
  subtree), verified by simulation. *Lower bound:* the exact fixed point of the tree recursion over
  all 256 functions, independently confirmed by a layer-by-layer enumeration (new functions per cost
  `1..9`: 24, 64, 30, 80, 32, 0, 16, 0, 2 — the two cost-9 functions are exactly `0x96` and `0x69`,
  parity and its complement).
- **Analytic fail-safe.** Khrapchenko's bound gives `L(⊕₃) ≥ |E|² / (|A||B|) = 144/16 = 9` leaves,
  hence at least 8 two-input gates, so `gap(⊕₃) ≥ 2` **independently of both computations above.**

Hence `gap(⊕₃) = 3`, refuting Theorem 2.

**Corollary 6 (`s ∈ {0,1}`) is refuted directly.** In the six-gate optimum both children of the
output gate contain the same three-gate sub-DAG computing `x₁ ⊕ x₂`, so the sharing term is `s = 3`
— structurally, and arithmetically `1 + 4 + 4 − 6 = 3`, with each child's `opt = 4` certified by an
UNSAT-at-3 DRAT proof.

**Fate of the other results.** Theorem 7 (a classification of shared gates assuming `gap = 1`) loses
its proof, which depends on Corollary 6, and its universal reading is false; its conditional
statement under the standard definition is not refuted by `⊕₃` (which has gap 3) and is left
unproven. **Theorems 3 and 4 survive.** For Theorem 3 we supply a corrected proof: the published
`|S| ≥ k − 1` count fails when the relevant gate is at input level; counting input incidences
instead gives `2m ≥ n + m`, i.e. `m ≥ n`, for every non-tree optimal circuit.

**Diagnostic signature.** In the paper's own complete `n = 3` table, the two functions listed with
`gap = 1` at `opt = 6` decode exactly to parity and its complement — precisely the functions for
which the displayed recursion (with `opt` in the children) reports a spurious gap of 1. The error is
thus visible in the paper's data, not only in its proof.

## 4. The failure is structural: AIG gap census at n = 4

We computed `tree(f)` for all 65,536 functions by a layered dynamic program (2.4 s, numpy;
independently re-implemented as a global Bellman fixed point with explicit polarities — all 65,536
cells agree), joined with the complete exact `opt` catalog (status `exact` enforced). The
distribution of `gap` over the 222 NPN classes:

| gap | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| classes | 93 | 57 | 40 | 13 | 14 | 2 | 3 |

**72 of 222 classes (32.4%) violate `gap ∈ {0,1}`.** The maximum gap 6 is attained exactly by
`{0x1668, 0x16e9, 0x6996}` — parity-4 and its NPN relatives — with `opt = 9` and `tree = 15`, where
Khrapchenko's bound (`≥ 16` leaves, hence `≥ 15` gates) is met with equality. The embedded `n = 3`
functions reproduce the `n = 3` table 256/256. The unit-gap bound is not narrowly false; it fails on
a constant fraction of all functions, with parity as the structural extremum.

## 5. Base dependence: XAG, MIG, and a sampled search at n = 5

The AIG gaps above are dominated by the cost of building parity — a linear function — out of AND
gates. This suggests the gap is an artifact of the basis. We test that directly.

**XAG, `n ≤ 4` (exhaustive).** With a native XOR gate, the exact-synthesis pipeline (encoder
validated by an independent exhaustive enumeration at `n = 3`, agreeing with the SAT route in both
directions) gives, over all 222 classes: `opt_XAG` maximum 7, strictly below AIG in 190/222 classes,
with `opt_XAG(⊕₄) = 3`; and by the same layered DP, `tree_XAG` maximum 7 with `tree_XAG(⊕₄) = 3`.
The gap census:

- `n = 3`: **`gap_XAG = 0` for all 256 functions.**
- `n = 4`: **`gap_XAG ∈ {0,1}`**, distributed `{0: 218, 1: 4}` over the 222 classes.

That is: **the unit-gap property, false in AIG, holds in XAG for `n ≤ 4`.** The large AIG gaps are
the cost of duplicating linear structure; once XOR is native, sharing buys at most one gate at these
sizes.

**XAG, `n = 5` (directed sample).** Exhaustive census is infeasible at `n = 5` (`2³²` truth tables).
We instead searched for a *separator* — a function with `gap_XAG ≥ 2` — by generating candidate
functions from random XAG circuits biased toward sharing and toward XOR structure (that is, biased
toward low `opt` and rich non-linear structure, where a non-linear separator is most likely), keeping
only functions essential in all five variables, and deciding `opt_XAG` and `tree_XAG` exactly by SAT
(ascending search, 20 s cap per call). The formula encoder was validated before the search by a gate
matching the `n = 4` DP on all 222 classes, including the four with `gap = 1` (Appendix B); an early
false positive (parity-5, which is linear and has gap 0) was traced to testing `opt + 1` in isolation
and fixed by ascending from `opt`.

Over **29,643 essential functions of five variables**, the outcome was:

| verdict | functions | % |
|---|---:|---:|
| gap 0 | 29,143 | 98.31 |
| gap 1 | 296 | 1.00 |
| inconclusive (SAT timeout) | 204 | 0.69 |
| **separator (`gap ≥ 2`)** | **0** | **0** |

**No separator was found.** Every decided function has `gap_XAG ∈ {0,1}`; the 204 inconclusive cases
are timeouts, neither confirmed nor separators. This is a **directed sample, not a proof**: a
separator of high `opt`, or one outside the generation bias, is not excluded. What the search does is
drive the subjective probability of a *low-opt* separator — the most likely kind — to near zero over
~29.6k attempts, extending the `n ≤ 4` observation to `n = 5` empirically.

**MIG (replication as pipeline validation).** The optimal MIG sizes for all 222 classes of `n = 4`
were published by Soeken, Amarù, Gaillardon and De Micheli (DATE 2016, Table I). We re-derived the
full census with a different solver (kissat vs. Z3), a different encoding, and ten years apart, and
matched the published distribution **exactly, bucket by bucket** (`{0:2, 1:2, 2:5, 3:18, 4:42,
5:117, 6:35, 7:1}`), including the unique 7-node class. This is reciprocal external validation: of
their table, and of the exact-synthesis pipeline used throughout.

**Cross-base summary (`n = 4`):**

| | AIG | XAG | MIG |
|---|---|---|---|
| max `opt` | 10 | 7 | 7 |
| `opt(⊕₄) / tree(⊕₄)` | 9 / 15 | 3 / 3 | 6 / — |
| gap census | up to 6; 32% `≥ 2` | `{0,1}` | deferred |

(`tree_MIG` requires a ternary DP whose naive form is cubic in set sizes; deferred.)

## 6. Verification

| Claim | Level of certification |
|---|---|
| `opt(⊕₃) = 6`, `opt` of shared child `= 4` (lower bounds) | DRAT proof, drat-trim `s VERIFIED`, byte-identical regeneration |
| `tree(⊕₃) = 9`; witnesses | Lean 4 kernel (`decide`) for witnesses + structural minimality lemma; DP sweep via `native_decide`; two independent implementations |
| `gap(⊕₃) ≥ 2` | Analytic (Khrapchenko), independent of all computation |
| AIG gap census `n = 4` | Two independent `tree` implementations; `opt` side inherits catalog certification |
| XAG census `n ≤ 4` | Gated encoder (independent exhaustive enumeration at `n = 3`, both directions); SAT models simulation-verified; UNSAT side without DRAT (declared) |
| XAG search `n = 5` | Formula encoder validated on all 222 `n = 4` classes; each result simulation-verified; sample, not exhaustive (declared) |
| MIG census `n = 4` | Same gating + exact match with an independently published table |

The Lean development (`UnitGap.lean`, Lean 4.31.0, no Mathlib) kernel-checks the witnesses and the
structural minimality lemma; the finite DP sweep uses one `native_decide`; the axiom footprint is
audited (`propext, Classical.choice, Quot.sound`).

## 7. Related work and novelty

- **Krinkin, arXiv:2603.08033** is the refuted paper; **arXiv:2603.09379** (an NPN-4 AIG catalog,
  whose two open entries we closed) is treated in a companion note. Both were communicated to the
  author (issues `krinkin/unit-gap#1`, `krinkin/bounds#1`).
- **MIG:** the optimal `n = 4` sizes were previously published (Soeken et al., DATE 2016; extended
  TCAD 2017). Our census is a replication, claimed only as validation.
- **XAG total-gate count** is essentially the classical combinational complexity over the full binary
  basis `B₂` — every 2-input operation depending on both inputs is one AND-with-polarities or one XOR
  — tabulated for small `n` by Knuth (TAOCP 7.1.2). Our maximum of 7 agrees with the classical value;
  we claim **no novelty for the XAG numbers themselves**. Multiplicative complexity (counting only
  ANDs) is a different measure and not what we tabulate.
- **What is new:** (i) the refutation of the Unit Gap theorem and its corollary, with machine-checked
  certificates and a Lean formalization, and the identification of the type confusion in the proof;
  and (ii) the complete gap censuses (`tree − opt` per class) in AIG and XAG at `n ≤ 4`, the sampled
  extension at `n = 5`, and the resulting base-dependence observation. Formula-size tables at small
  `n` exist in the classical literature; we have not found the gap-by-basis analysis stated anywhere,
  and this novelty claim for (ii) is correspondingly hedged.

## 8. Open questions

1. Does `gap_XAG` remain in `{0,1}` for all of `n = 5` (the sample found no separator), and for
   larger `n`? Parity no longer separates in XAG, but nothing here rules out other separators.
2. Is there a clean theorem behind the empirical XAG unit gap at small `n` — e.g. a normal-form
   argument bounding sharing once linear structure is factored out?
3. An efficient exact DP for `tree_MIG` (the deferred MIG gap column).
4. A corrected, basis-relative formulation of Krinkin's Theorem 7, with proof.

## References

<!-- a formatar na conversão LaTeX -->

- M. Krinkin. *The Unit Gap.* arXiv:2603.08033.
- M. Krinkin. *[NPN-4 AIG catalog].* arXiv:2603.09379.
- V. M. Khrapchenko. *A method of determining lower bounds for the complexity of Π-schemes.* (1971).
- M. Soeken, L. Amarù, P.-E. Gaillardon, G. De Micheli. *Optimizing Majority-Inverter Graphs with
  exact synthesis.* DATE 2016; extended in IEEE TCAD 2017.
- D. E. Knuth. *The Art of Computer Programming*, Vol. 4A, §7.1.2 (Boolean evaluation / chains).
- A. Biere et al. *kissat* SAT solver 4.0.4; *drat-trim* proof checker.
- *Lean 4* theorem prover, v4.31.0.

## Appendix A. Certificates

DRAT proofs for the load-bearing lower bounds (`opt(⊕₃) ≥ 6` and each shared child's `opt ≥ 4`),
checked by drat-trim to `s VERIFIED`, with byte-identical regeneration. Lean sources for the `n = 3`
witnesses and the structural minimality lemma, with the audited axiom footprint.

## Appendix B. Encoders and gates

The AIG, XAG, and multi-output encoders, and the validation gates: G1–G3 (AIG single-output), the
multi-output gate, and G-T1/G-T2/G-T3 for the XAG formula encoder (`n = 3` complete `tree = opt`;
`n = 4` `tree_via_sat` matches the independent DP on all 222 classes, covering the four with
`gap = 1`). The parity-5 false positive in the `n = 5` search and its fix (ascending search from
`opt` rather than an isolated `opt + 1` test) are documented here.

## Appendix C. Reproducibility

Solver kissat 4.0.4; drat-trim; Lean 4.31.0. Encoders, gates, censuses, CNFs, DRAT proofs, the
`n = 5` search CSVs, and Lean sources are versioned in the program repository. Seeds for the `n = 5`
search are deterministic per worker (`Random(90210 + wid)`); the bench is a 2-vCPU always-on VPS.

<!-- Provenance note (tom a definir com Luiz; fora do corpo; SEM claim de pioneirismo):
     analysis and code produced by an AI system under the direction of L. A. Busnello; certificates
     checked by standard independent tools; claims adversarially cross-reviewed by four independent
     model families before external communication. -->
