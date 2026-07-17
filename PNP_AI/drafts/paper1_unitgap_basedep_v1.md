# The Unit Gap Is Base-Dependent: A Mechanically Verified Refutation and a Cross-Base Census

<!-- DRAFT v1 (2026-07-17) — INTERNO, NÃO SUBMISSÃO. Incorpora a revisão adversarial de 4 famílias
     (REV-0015..0018) + verificações próprias. Mudanças vs v0 registradas em
     `paper1_v0_review_consolidado.md`. Submissão exige OK de Luiz + 10_PUBLICATION_RULES + janela de
     resposta da issue krinkin/unit-gap#1. Venue provável: arXiv cs.CC (cross-list cs.LO). -->

## Abstract

Krinkin's *The Unit Gap: How Sharing Works in Boolean Circuits* (arXiv:2603.08033) asserts that for
every Boolean function the minimum formula size exceeds the minimum circuit size by at most one gate
— Theorem 2: `gap ∈ {0,1}` in the And-Inverter Graph (AIG) cost model — with a decomposition
corollary bounding a shared-gate term `s ∈ {0,1}` (Corollary 6). We refute both. Under the paper's
own definition of a formula (fan-out one at every gate), the parity of three variables is a
counterexample: `opt(⊕₃) = 6` — UNSAT for every gate count `k = 1..5`, each certified by a DRAT proof
checked with drat-trim — while `tree(⊕₃) = 9`, giving gap 3; the optimal six-gate circuit has two
output-child sub-DAGs whose intersection is a three-gate block, so Krinkin's own term
`s = |D_a ∩ D_b| = 3`. Khrapchenko's classical bound independently forces `tree(⊕₃) ≥ 8`, so
`gap ≥ 2` survives even if every computation above were wrong. The counterexample is formalized in
Lean 4. The error is locatable in the paper itself: the displayed recursion for `tree(f)` in §2 puts
the DAG measure `opt` in the children, while the Bellman operator in §3 puts the recursive tree
measure `v` — two incompatible definitions, of which the first makes Theorem 2 a one-line tautology
and the second makes it false (the fixed point overshoots `opt(⊕₃)` by 3, not by ≤ 1). An exhaustive
census over the 222 NPN classes of `n = 4` shows the failure is structural: 72 of 222 classes (32.4%
of classes) have `gap ≥ 2`, the maximum gap 6 attained by three distinct NPN classes, one of which is
parity-4. Finally, we show the phenomenon is **base-dependent**. In the XOR-AND-graph (XAG) basis the
unit-gap property holds (under a gated exact-synthesis pipeline): `gap_XAG = 0` for all 256 functions
of `n = 3` and `gap_XAG ∈ {0,1}` for all 222 classes of `n = 4`; a directed search over 25,373
distinct essential functions of `n = 5` finds **no function with `gap_XAG ≥ 2`**. The large AIG gaps
are consistent with the cost of simulating linear (parity) structure without a native XOR gate. A
replicated MIG census matching Soeken et al.'s published size distribution bucket by bucket validates
the synthesis pipeline externally.

## 1. Introduction

The relationship between **formula size** (the smallest fan-out-one circuit for a function) and
**circuit size** (the smallest circuit of any fan-out) is one of the oldest quantitative questions in
Boolean complexity. Formula size is a tree measure, circuit size a DAG measure; their difference
measures how much *sharing* — reusing an intermediate result at more than one place — can buy.
Krinkin's *The Unit Gap* (arXiv:2603.08033) makes a strong claim about this difference in the
And-Inverter Graph model: the gap is **at most one gate** for every Boolean function (Theorem 2), with
a decomposition corollary bounding the sharing in an optimal circuit (Corollary 6).

It is not true. This paper does three things.

1. **We refute Theorem 2 and Corollary 6** with a certified counterexample at `n = 3` (parity), where
   the gap is 3 and Krinkin's shared-gate term is 3. The lower bound on circuit size is a DRAT proof
   chain (UNSAT at every `k = 1..5`) checked by an independent tool; the formula size is confirmed by
   two dynamic programs and a Lean 4 formalization; and an analytic bound (Khrapchenko) forces the gap
   to be at least 2 regardless of any computation. We locate the error inside the paper: §2 and §3
   give two incompatible recursions for `tree(f)`.

2. **We show the failure is structural**, computing the complete gap census over all 222 NPN classes
   of `n = 4`: 32.4% of classes violate the unit-gap bound, and the maximum gap is attained by three
   distinct NPN classes, one being parity.

3. **We show the phenomenon is base-dependent.** The unit-gap property, false in AIG, holds
   empirically in the XOR-AND-graph basis for `n ≤ 4` (exhaustive) and over a large directed search at
   `n = 5`. The AIG gaps are consistent with the price of simulating parity without a native XOR gate.

Our method throughout is **exact synthesis via SAT**: for each function and each size `k`, "is there a
`k`-gate circuit for `f`?" is encoded as a CNF and decided by a modern solver. The encoder is a
normalized exact-size encoding (every non-output gate used, no duplicate gates); by a minimality
lemma, `opt(f) = k` implies the `k`-encoding is satisfiable, so ascending search is exact **only after
every smaller `k` has been excluded** — which is why our circuit lower bounds certify UNSAT at *all*
`k` below the optimum, not just the last. Load-bearing lower bounds carry DRAT certificates. The
package was reviewed adversarially by four independent language-model families before external
communication; the mathematical claims rest on the certificates, not on that review. We claim novelty
only for the refutation and for the gap-by-basis census; the individual optimal-size tables in XAG and
MIG are classical or previously published, and we say so.

## 2. Preliminaries

We quote the paper's own definitions to fix the target precisely.

> **[Krinkin §2]** *A circuit is an AIG where gates may have fan-out greater than one. A formula (or
> tree circuit) has fan-out exactly one at every gate. We write `tree(f)` for the minimum formula
> size. Since every formula is a circuit, `tree(f) ≥ opt(f)`. The gap is `gap(f) = tree(f) − opt(f)`.*

An **AIG** over `x₁,…,xₙ` and the constant 1 is a DAG of two-input AND gates with free edge
complementation; `opt(f)` is the minimum number of AND gates. (The output gate has fan-out zero; "fan-
out one at every gate" is Krinkin's phrasing for the non-output gates of a tree.) An **XAG** adds a
native XOR gate; an **MIG** uses 3-input majority gates. All exhaustive results are for `n ≤ 4`.

**Exact synthesis.** For fixed `(n, k)` we one-hot–select each gate's operation and operands among
earlier nodes and constrain the output to compute `f` up to polarity. The encoding is *normalized*:
every non-output gate is required to be used and duplicate gate options are forbidden. These are sound
for minimality (a minimum circuit has no unused or duplicate gate), so: SAT at `k` yields a valid
`k`-gate circuit, and if `opt(f) = k` a minimality lemma guarantees the `k`-encoding is satisfiable.
Consequently `opt(f)` is the least `k` with SAT, and a lower bound `opt(f) ≥ m` requires UNSAT at
`k = 1,…,m−1`. Restricting selection to fan-out one turns the same encoder into a `tree(f)` oracle
(validated in Appendix B).

## 3. The refutation at n = 3

**The paper gives two incompatible recursions for `tree(f)`.** In §2 it displays

> **[Krinkin §2]** `tree(f) = min over f = a∧b (or f̄ = a∧b) of ( 1 + opt(a) + opt(b) )`,

with **`opt`** in the children, and immediately notes that the trivial decomposition `f = 1 ∧ f`
"always achieves `1 + opt(f)`". With `opt` in the children this yields `tree(f) ≤ 1 + opt(f)` for
every `f` — Theorem 2 becomes a one-line consequence, but the quantity minimized is not a tree (the
children may be internally shared DAGs). In §3, however, the paper defines the Bellman operator

> **[Krinkin §3]** `(Tv)(f) = min over f = a∧b of ( 1 + v(a) + v(b) )`, "iterating `T` … computes
> `tree(f)`",

with the **recursive** measure `v` in the children — the correct formula recursion — and claims its
fixed point "overshoots `opt(f)` by exactly `gap(f) ∈ {0,1}`". These cannot both hold: the recursive
`T` computes the true formula size, which for ⊕₃ is 9, overshooting `opt = 6` by 3. Under the standard
(and §3) reading, Theorem 2 is false.

- **`opt(⊕₃) = 6`.** *Upper bound:* an explicit six-gate circuit (a dual-polarity XOR block feeding a
  combiner), verified by simulation. *Lower bound:* UNSAT at **every `k = 1,2,3,4,5`** (kissat 4.0.4),
  each with a DRAT proof checked by drat-trim (`s VERIFIED`); regeneration reproducible. (The full
  `k = 1..5` chain — not only `k = 5` — is what certifies `opt ≥ 6` under the normalized exact-size
  encoding.)
- **`tree(⊕₃) = 9`.** *Upper bound:* an explicit nine-gate formula, verified by simulation. *Lower
  bound:* the exact fixed point of the tree recursion over all 256 functions, independently confirmed
  by a layer-by-layer enumeration (new functions per cost `1..9`: 24, 64, 30, 80, 32, 0, 16, 0, 2 —
  the two cost-9 functions are exactly parity and its complement).
- **Analytic fail-safe.** Khrapchenko: `L(⊕₃) ≥ |E|²/(|A||B|) = 144/16 = 9` leaves, hence at least 8
  two-input gates, so `gap(⊕₃) ≥ 2` **using only the explicit six-gate circuit and Khrapchenko** —
  independent of the tree DP and of the DRAT chain.

Hence `gap(⊕₃) = 3`, refuting Theorem 2.

**Corollary 6 is refuted with Krinkin's own definition.** Krinkin states

> **[Krinkin Cor. 6]** `opt(f) = 1 + opt(a) + opt(b) − s(a,b)`, where `s(a,b) = |D_a ∩ D_b| ∈ {0,1}`
> counts the shared gates,

and derives `s ≤ 1` *from* the Unit Gap Theorem (`s = 1 + opt(a) + opt(b) − opt(f) ≤ tree(f) − opt(f)
≤ 1`). In the six-gate optimum for ⊕₃, the two children `a, b` of the output gate each have `opt = 4`
and their sub-DAGs share the three-gate block computing `x₁⊕x₂`, so `|D_a ∩ D_b| = 3` and
`s = 1 + 4 + 4 − 6 = 3 ∉ {0,1}` (`opt` of each child = 4 certified by an UNSAT-at-3 DRAT proof). The
corollary's own `s ≤ 1` step is exactly the refuted Theorem 2. Krinkin's Table 3 reports `s = 1`
(100%) for the opt-6 decompositions of parity — a direct conflict with `s = 3`, reflecting the
circular bound rather than the structural count.

**Fate of the other results.** Theorem 7 (a two-mechanism classification assuming `gap = 1`) loses its
proof, which depends on Corollary 6; its conditional statement under the standard definition is not
refuted by ⊕₃ (which has gap 3) and is left unproven. **Theorems 3 and 4 survive.** For Theorem 3
(Threshold: `gap(f)=1 ⇒ opt(f) ≥ n`) the published proof applies Lemma 1 (gate elimination) to the
sub-DAG `S` *below* the shared gate `g` and writes `|S| ≥ k−1`, which fails when `g` is at input level
(the `k` essential variables are covered by `S ∪ {g}`, not `S` alone). A corrected counting argument
by input incidences gives `m ≥ n` for every non-tree optimal single-output circuit; it is stated in
full in Appendix A.

**Diagnostic signature.** In Krinkin's own complete `n = 3` table (Table 1), the two functions listed
with `gap = 1` at `opt = 6` are parity and its complement — precisely what the §2 recursion (with
`opt` in the children: `1 + opt(parity) + opt(1) = 7`) reports, while the true formula size is 9. The
error is visible in the paper's data, not only its proof.

**Verification.** The counterexample is formalized in Lean 4.31.0 without Mathlib (`UnitGap.lean`):
the witnesses and the DP's structural framework are kernel-checked (`decide`, induction), while the
finite fact `par3 ∉ D₈` — and hence `tree(⊕₃) ≥ 9` — is discharged by `native_decide` (compiler-
trusted, not kernel). We report this precisely rather than as blanket "kernel-checked" (see §6).

## 4. The failure is structural: AIG gap census at n = 4

We computed `tree(f)` for all 65,536 functions by a layered dynamic program (independently
re-implemented as a global Bellman fixed point with explicit polarities — all 65,536 cells agree),
joined with the complete exact `opt` catalog. The distribution of `gap` over the 222 NPN classes:

| gap | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| classes | 93 | 57 | 40 | 13 | 14 | 2 | 3 |

**72 of the 222 NPN classes (32.4% of classes) have `gap ≥ 2`.** (This is a fraction of NPN classes,
not of all 65,536 functions, whose orbit sizes differ.) The maximum gap 6 is attained by three
**distinct** NPN classes `{0x1668, 0x16e9, 0x6996}` — with `opt = 9`, `tree = 15` — one of which is
parity-4 (`0x6996`); the other two are not NPN-equivalent to parity (they have Hamming weight 6 and 8
versus parity's 8, and distinct XAG optima 6 and 5 versus parity's 3). For parity-4, Khrapchenko's
bound (`≥ 16` leaves ⟹ `≥ 15` gates) meets `tree = 15` with equality. The embedded `n = 3` functions
reproduce the `n = 3` table 256/256. Parity is thus **a** witness of the maximum gap, not its
exclusive source: the census is consistent with, but does not by itself isolate, "linear structure
without native XOR" as the mechanism for all 72 violating classes.

## 5. Base dependence: XAG, MIG, and a directed search at n = 5

The AIG gaps above coincide with the cost of building parity — a linear function — from AND gates,
suggesting the gap is a basis artifact. We test that directly.

**XAG, `n ≤ 4` (exhaustive).** With a native XOR gate, the pipeline (encoder validated by an
independent exhaustive enumeration at `n = 3` and by a formula-encoder gate on all 222 `n = 4`
classes) gives `opt_XAG` maximum 7 (strictly below AIG in 190/222 classes; `opt_XAG(⊕₄) = 3`) and
`tree_XAG` maximum 7. The gap census: `n = 3` — `gap_XAG = 0` for all 256 functions; `n = 4` —
`gap_XAG ∈ {0,1}`, distributed `{0: 218, 1: 4}`. The unit-gap property, false in AIG, **holds in XAG
for `n ≤ 4`** under this gated exact-synthesis pipeline (the UNSAT side is not DRAT-certified; see §6).

**XAG, `n = 5` (directed search).** Exhaustive census is infeasible at `n = 5` (`2³²` truth tables).
We searched for a *separator* (`gap_XAG ≥ 2`) by generating candidate functions from random XAG
circuits with sharing and XOR bias, keeping those essential in all five variables, and deciding
`opt_XAG` and `tree_XAG` exactly by SAT (ascending search, 20 s cap). We report the search honestly as
a **generator-reachable, solver-decidable sample**, not a probability statement: functions whose `opt`
timed out or exceeded the cap are not written and thus not counted, so the sample is conditional on
easy circuit optimization. The formula encoder was gated before the search (matching the `n = 4` DP on
all 222 classes, including the four with `gap = 1`); an early false positive (parity-5, linear, gap 0)
was fixed by ascending from `opt`.

Over **25,373 distinct** essential functions of five variables (deduplicated across workers):

| verdict | functions | % |
|---|---:|---:|
| gap 0 | 24,875 | 98.04 |
| gap 1 | 294 | 1.16 |
| inconclusive (SAT timeout) | 204 | 0.80 |
| **separator (`gap ≥ 2`)** | **0** | **0** |

**No separator was found** among these functions. Every decided function has `gap_XAG ∈ {0,1}`; the
204 inconclusive cases are formula-search timeouts. As an added check, all 294 gap-1 functions and a
sample of 200 gap-0 functions were re-decoded and simulation-verified (the optimal circuit and the
formula both compute the truth table); 494/494 passed. This is a **directed sample, not a proof**: a
separator of high `opt`, or one outside the generation bias, is not excluded. What the search
establishes is that no separator appears among 25,373 distinct, generator-reachable, solver-decidable
essential functions of `n = 5`.

**MIG (replication as pipeline validation).** Soeken, Amarù, Gaillardon and De Micheli (DATE 2016)
published the optimal MIG size distribution for the 222 classes of `n = 4`. We re-derived the census
with a different solver (kissat vs. Z3) and encoding and matched the published **size distribution**
`{0:2, 1:2, 2:5, 3:18, 4:42, 5:117, 6:35, 7:1}` **bucket by bucket**, including the unique 7-node
class. (Their table publishes bucket counts, not a per-class representative-to-size map; we therefore
claim a distribution match, not a class-by-class one.) This is external validation of the pipeline.

**Cross-base summary (`n = 4`):**

| | AIG | XAG | MIG |
|---|---|---|---|
| max `opt` | 10 | 7 | 7 |
| `opt(⊕₄) / tree(⊕₄)` | 9 / 15 | 3 / 3 | 6 / — |
| gap census | up to 6; 32.4% of classes `≥ 2` | `{0,1}` | deferred |

(`tree_MIG` requires a ternary DP whose naive form is cubic in set sizes; deferred.)

## 6. Verification

| Claim | Level of certification |
|---|---|
| `opt(⊕₃) = 6` (lower bound) | DRAT proofs for UNSAT at **every `k = 1..5`**, drat-trim `s VERIFIED`; reproducible regeneration |
| `opt` of each shared child `= 4` | DRAT proof for UNSAT at `k = 3`, drat-trim `s VERIFIED` |
| `tree(⊕₃) = 9`; witnesses | Lean 4 kernel (`decide`) for witnesses + DP structural framework; the finite exclusion `par3 ∉ D₈` (hence `tree ≥ 9`) by `native_decide` (compiler-trusted); two implementations of the same recurrence agree |
| `gap(⊕₃) ≥ 2` | Analytic (Khrapchenko + six-gate circuit), independent of the tree DP and the DRAT chain |
| AIG gap census `n = 4` | Two implementations of the tree recurrence agree on all 65,536 cells; `opt` side inherits catalog certification |
| XAG census `n ≤ 4` | Gated encoder (independent exhaustive enumeration at `n = 3`; formula encoder matches DP on all 222 `n = 4` classes); SAT models simulation-verified; UNSAT side without DRAT (declared) |
| XAG search `n = 5` | Encoder gated at `n ≤ 4`; 494 instances (all gap1 + a gap0 sample) re-decoded and simulation-verified; sample, not exhaustive (declared) |
| MIG census `n = 4` | Same gating + exact match with an independently published size distribution |

The two `tree` implementations are independent *implementations of the same Bellman recurrence*
(layered vs. fixed-point), which is strong bug detection; the semantic bridge — that the recurrence
computes formula size — is supplied by the Lean completeness lemma. The four-model-family adversarial
review is provenance, not part of the verification chain, and is recorded as such.

## 7. Related work and novelty

- **Krinkin, arXiv:2603.08033** is the refuted paper; **arXiv:2603.09379** (an NPN-4 AIG catalog whose
  two open entries we closed) is a companion note. Both were communicated to the author
  (`krinkin/unit-gap#1`, `krinkin/bounds#1`).
- **MIG:** the optimal `n = 4` sizes were previously published (Soeken et al., DATE 2016; TCAD 2017);
  our census is replication, claimed only as validation.
- **XAG total-gate count** is essentially the classical combinational complexity over the full binary
  basis `B₂`, tabulated for small `n` by Knuth (TAOCP 7.1.2); our maximum of 7 agrees. We claim **no
  novelty for the XAG numbers themselves**.
- **Contributions reported here:** (i) the refutation of Theorem 2 and Corollary 6, with machine-
  checked certificates and a Lean formalization, and the localization of the error to the two
  incompatible recursions in §2 and §3; and (ii) the first *explicitly tabulated* gap-by-basis
  comparison (`tree − opt` per NPN class) in AIG and XAG at `n ≤ 4`, with a directed `n = 5` XAG
  search. The `tree − opt` difference is a subtraction of columns each of which is classical, so (ii)
  is a contribution of *organized data and the base-dependence observation*, not of a new measure; it
  is likely implicit in any catalog publishing both formula and circuit sizes. We searched Knuth's
  B₂ data, the MIG and AIG catalogs above, and standard references, and did not find the gap-by-basis
  comparison stated explicitly, but treat (ii) as "apparently unreported" pending a specialist check.

## 8. Open questions

1. Does `gap_XAG` remain in `{0,1}` for all of `n = 5` (the directed search found no separator among
   25,373 functions) and for larger `n`? Parity no longer separates in XAG; other separators are not
   excluded.
2. Is there a theorem behind the empirical XAG unit gap at small `n` — e.g. a normal-form argument
   bounding sharing once linear structure is factored out?
3. An efficient exact DP for `tree_MIG` (the deferred MIG gap column).
4. A corrected, basis-relative formulation of Krinkin's Theorem 7, with proof.

## References

<!-- a formatar na conversão LaTeX -->
- K. Krinkin. *The Unit Gap: How Sharing Works in Boolean Circuits.* arXiv:2603.08033.
- K. Krinkin. *[NPN-4 AIG catalog].* arXiv:2603.09379.
- V. M. Khrapchenko. *Complexity of the realization of a linear function in the class of Π-circuits.*
  Mathematical Notes 9(1):21–23, 1971.
- M. Soeken, L. Amarù, P.-E. Gaillardon, G. De Micheli. *Optimizing Majority-Inverter Graphs with
  exact synthesis.* DATE 2016; extended IEEE TCAD 2017.
- D. E. Knuth. *The Art of Computer Programming*, Vol. 4A, §7.1.2.
- A. Kojevnikov, A. S. Kulikov, G. Yaroslavtsev. *Finding efficient circuits using SAT-solvers.* SAT
  2009.
- kissat 4.0.4; drat-trim; Lean 4.31.0.

## Appendix A. Corrected proof of Theorem 3 (Threshold)

*Claim.* If `f` has `n` essential variables, is computed by a size-optimal single-output AIG that is
not a tree (so `gap(f) ≥ 1`), then `opt(f) = m ≥ n`.

*Proof.* Count input incidences. Every gate has two inputs, so the total number of input slots is
`2m`. Partition these slots by what they read: `I_var` slots read a primary input (or the constant),
`I_gate` slots read another gate. Then `2m = I_var + I_gate`.

- *Essential variables:* each of the `n` essential variables must feed at least one slot (else `f`
  would not depend on it), so `I_var ≥ n`.
- *Gate usage:* each of the `m − 1` non-output gates must feed at least one later slot (normalized
  circuit: no unused gate), contributing `≥ m − 1` to `I_gate`. Because the circuit is not a tree,
  some gate has fan-out `≥ 2`, contributing at least one further incidence, so `I_gate ≥ m`.

Hence `2m = I_var + I_gate ≥ n + m`, i.e. `m ≥ n`. ∎

(The published proof's `|S| ≥ k − 1` step applies gate elimination to the fan-in cone `S` *excluding*
the shared gate `g`; when `g` is at input level the `k` essential variables of `S ∪ {g}` are not all
covered by `S`, and the count is short by one. The incidence argument avoids the case split.)

## Appendix B. Encoders and gates

The AIG, XAG, and multi-output encoders and their validation gates: G1–G3 (AIG single-output), the
multi-output gate, and G-T1/G-T2/G-T3 for the XAG formula encoder (`n = 3` complete `tree = opt`;
`n = 4` `tree_via_sat` matches the independent DP on all 222 classes, covering the four with
`gap = 1`). The parity-5 false positive in the `n = 5` search and its fix (ascending search from
`opt`) are documented here.

## Appendix C. Reproducibility

kissat 4.0.4; drat-trim; Lean 4.31.0. Encoders, gates, censuses, CNFs, the `k = 1..5` DRAT proofs for
`opt(⊕₃)`, the `n = 5` search CSVs (raw per-worker and globally deduplicated), and the Lean sources
are versioned. The `n = 5` search seeds are deterministic per worker; the bench is a 2-vCPU VPS.

<!-- Provenance note (tom a definir com Luiz; fora do corpo; SEM claim de pioneirismo):
     analysis and code produced by an AI system under the direction of L. A. Busnello; certificates
     checked by standard independent tools (kissat, drat-trim, Lean); claims adversarially reviewed by
     four independent model families before external communication. -->
