# The Unit Gap Is Base-Dependent: A Mechanically Verified Refutation and a Cross-Base Census

<!-- DRAFT v3 (2026-07-17) — INTERNO, versão CONVERGIDA pré-LaTeX. Incorpora a 3ª rodada adversarial
     (REV-0023..0026): 4/4 famílias, 0 CRITICAL, ready for LaTeX. Ajustes vs v2: desigualdade s≥gap
     explícita (+ nuance parity); child = representative + NPN; opt_XAG NPN-invariant; §5 opening;
     "solver-decided"; quotes rotulados notation-normalized; artefatos npn4_xag_gap.csv + log
     provenance. Krinkin quotes são notation-normalized de arXiv:2603.08033v2 (fiéis por pdftotext,
     REV-0026). Submissão exige OK de Luiz + 10_PUBLICATION_RULES + janela de krinkin/unit-gap#1.
     Venue: arXiv cs.CC (cross-list cs.LO). -->

## Abstract

Krinkin's *The Unit Gap: How Sharing Works in Boolean Circuits* (arXiv:2603.08033v2) asserts that for
every Boolean function the minimum formula size exceeds the minimum circuit size by at most one gate
— Theorem 2: `gap ∈ {0,1}` in the And-Inverter Graph (AIG) cost model — with a decomposition
corollary bounding a shared-gate term `s ∈ {0,1}` (Corollary 6). We refute both. Under the paper's
own definition of a formula (fan-out one at every gate), the parity of three variables (⊕₃) is a
counterexample: `opt(⊕₃) = 6` — UNSAT for every gate count `k = 1..5`, each certified by a DRAT proof
checked with drat-trim — while `tree(⊕₃) = 9`, giving gap 3; in the optimal six-gate circuit the two
output-child sub-DAGs intersect in a three-gate parity-2 block, so Krinkin's own term
`s = |D_a ∩ D_b| = 3`. Khrapchenko's classical bound forces `tree(⊕₃) ≥ 8`; together with the explicit
six-gate circuit (`opt ≤ 6`) this gives `gap ≥ 2` independently of the SAT lower-bound chain and the
tree dynamic program. The counterexample is formalized in Lean 4. The error is locatable in the paper:
§2 displays `tree(f) = min(1 + opt(a) + opt(b))` (the DAG measure `opt` in the children), while §3's
Bellman operator is `(Tv)(f) = min(1 + v(a) + v(b))` (the recursive measure); these are incompatible
characterizations of formula size, the first making Theorem 2 a one-line tautology and the second
making it false (its fixed point overshoots `opt(⊕₃)` by 3). An exhaustive census over the 222 NPN
classes of `n = 4` shows the failure is structural: 72 of 222 classes (32.4% of classes) have
`gap ≥ 2`, the maximum gap 6 attained by three distinct NPN classes (distinguished by their XAG
optima 6/5/3), one of which is parity-4. Finally, the phenomenon is **base-dependent**. In the
XOR-AND-graph (XAG) basis the unit-gap property holds for `n ≤ 4` (under a separately gated
exact-synthesis pipeline whose UNSAT side is not proof-certified): `gap_XAG = 0` for all 256 functions
of `n = 3` and `gap_XAG ∈ {0,1}` for all 222 classes of `n = 4`; a directed search over 25,373
distinct essential functions of `n = 5` certifies **no separator** (all 25,169 gap-decided functions
have `gap_XAG ≤ 1`; 204 remain unresolved). The large AIG gaps are consistent with the cost of
simulating linear (parity) structure without a native XOR gate. A replicated MIG census matching
Soeken et al.'s published size distribution bucket by bucket gives an aggregate external cross-check.

## 1. Introduction

The relationship between **formula size** (the smallest fan-out-one circuit for a function) and
**circuit size** (the smallest circuit of any fan-out) is one of the oldest quantitative questions in
Boolean complexity. Their difference measures how much *sharing* — reusing an intermediate result at
more than one place — can buy. Krinkin's *The Unit Gap* claims that in the And-Inverter Graph model
this difference is **at most one gate** for every Boolean function (Theorem 2), with a decomposition
corollary bounding the sharing (Corollary 6).

It is not true. This paper does three things.

1. **We refute Theorem 2 and Corollary 6** with a certified counterexample at `n = 3` (parity), where
   the gap is 3 and Krinkin's shared-gate term is 3. The circuit lower bound is a DRAT proof chain
   (UNSAT at every `k = 1..5`) checked by an independent tool; the formula size is confirmed by two
   dynamic programs and a Lean 4 formalization; and Khrapchenko's bound, together with the explicit
   six-gate circuit, forces the gap ≥ 2 regardless of the SAT and DP computations. We locate the error
   inside the paper: §2 and §3 give incompatible characterizations of `tree(f)`.

2. **We show the failure is structural**, computing the complete gap census over all 222 NPN classes
   of `n = 4`: 32.4% of classes violate the unit-gap bound, the maximum gap attained by three distinct
   NPN classes, one being parity.

3. **We show the phenomenon is base-dependent.** The property, false in AIG, holds in the XAG basis
   for `n ≤ 4` (exhaustive) and over a large directed search at `n = 5`. The large parity AIG gaps are
   consistent with the price of simulating parity without a native XOR gate.

Our method is **exact synthesis via SAT**: "is there a `k`-gate circuit for `f`?" is a CNF decided by
a modern solver. The encoder is a normalized exact-size encoding (every non-output gate used, no
duplicate gates); by a minimality lemma, `opt(f) = k` implies the `k`-encoding is satisfiable, so a
lower bound `opt(f) ≥ m` requires UNSAT at *every* `k = 1..m−1` — which is why our circuit lower
bounds certify the whole chain, not just the last step. The package was reviewed adversarially by four
independent language-model families before external communication; the mathematics rests on the
certificates, not that review. We claim novelty only for the refutation and for the gap-by-basis
census; the individual optimal-size tables in XAG and MIG are classical or previously published.

## 2. Preliminaries

We quote the paper's definitions to fix the target precisely (arXiv:2603.08033v2, §2;
notation-normalized).

> *A circuit is an AIG where gates may have fan-out greater than one. A formula (or tree circuit) has
> fan-out exactly one at every gate. We write `tree(f)` for the minimum formula size. Since every
> formula is a circuit, `tree(f) ≥ opt(f)`. The gap is `gap(f) = tree(f) − opt(f)`.*

And, for the decomposition (§2):

> *Every AIG gate computes `f = a ∧ b` (with possible edge complementation). The minimum formula size
> satisfies `tree(f) = min over a,b: f = a∧b or f = ¬(a∧b) of (1 + opt(a) + opt(b))`. The trivial
> decomposition `f = 1 ∧ f` always achieves `1 + opt(f)`.*

An **AIG** over `x₁,…,xₙ` and the constant 1 is a DAG of two-input AND gates with free edge
complementation; `opt(f)` is the minimum number of AND gates. (The output gate has fan-out zero; the
"fan-out one" condition is Krinkin's, for the non-output gates of a tree.) An **XAG** adds a native
XOR gate; an **MIG** uses 3-input majority gates. All exhaustive results are for `n ≤ 4`.

**Exact synthesis.** For fixed `(n, k)` we one-hot–select each gate's operation and operands among
earlier nodes and constrain the output to compute `f` up to polarity. The encoding is *normalized*:
every non-output gate must be used and duplicate gate options are forbidden. These are sound for
minimality: SAT at `k` yields a valid `k`-gate circuit, and if `opt(f) = k` a minimality lemma
guarantees the `k`-encoding is satisfiable. Hence `opt(f)` is the least `k` with SAT, and a lower
bound `opt(f) ≥ m` requires UNSAT at *every* `k = 1,…,m−1`. Restricting selection to fan-out one turns
the same encoder into a `tree(f)` oracle (validated in Appendix B).

## 3. The refutation at n = 3

**The paper gives incompatible characterizations of `tree(f)`.** The §2 identity puts the DAG measure
`opt` in the children; with `opt` there, the trivial decomposition `f = 1 ∧ f` yields
`tree(f) ≤ 1 + opt(f)` for every `f`, so Theorem 2 is a one-line consequence — but the minimized
object is not a tree (the children may be internally shared DAGs). In §3, however, the paper defines
the Bellman operator (notation-normalized):

> *`(Tv)(f) = min over a,b: f = a∧b of (1 + v(a) + v(b))`; iterating `T` from the base case
> `v₀(xᵢ) = v₀(1) = 0` computes `tree(f)`.*

with the **recursive** measure `v` in the children. At its fixed point this reads
`tree(f) = min(1 + tree(a) + tree(b))`, a different object from the §2 identity: as global
characterizations of formula size the two coincide term-by-term only on children for which
`opt = tree`. Krinkin further states — as a *consequence of Theorem 2*, not a definition — that `T`'s
fixed point "overshoots `opt(f)` by exactly `gap(f) ∈ {0,1}`", which collapses together with Theorem
2. For ⊕₃ the recursive `T` computes 9, overshooting `opt = 6` by 3; under the §3 reading, Theorem 2
is false.

- **`opt(⊕₃) = 6`.** *Upper bound:* an explicit six-gate circuit (a dual-polarity parity-2 block
  feeding a combiner), verified by simulation. *Lower bound:* UNSAT at **every `k = 1,2,3,4,5`**
  (kissat 4.0.4), each with a DRAT proof checked by drat-trim (`s VERIFIED`; transcript and hashes in
  Appendix C). The full `k = 1..5` chain — not only `k = 5` — certifies `opt ≥ 6` under the normalized
  exact-size encoding.
- **`tree(⊕₃) = 9`.** *Upper bound:* an explicit nine-gate formula, verified by simulation. *Lower
  bound:* the exact fixed point of the tree recursion over all 256 functions, independently confirmed
  by a layer-by-layer enumeration (new functions per cost `1..9`: 24, 64, 30, 80, 32, 0, 16, 0, 2 —
  the two cost-9 functions are parity and its complement).¹
- **Analytic fail-safe.** Khrapchenko: `L(⊕₃) ≥ |E|²/(|A||B|) = 144/16 = 9` leaves, hence ≥ 8
  two-input gates. Together with the explicit six-gate circuit (`opt ≤ 6`), `gap(⊕₃) ≥ 2` follows
  **using only Khrapchenko and that circuit** — independent of the tree DP and the DRAT chain.

Hence `gap(⊕₃) = 3`, refuting Theorem 2.

**Corollary 6 is refuted with Krinkin's own definition.** He states (§5; notation-normalized):

> *Let `C` be an optimal AIG, and let `g` be any gate computing `f = a ∧ b`. Let `D_a, D_b` be the
> sub-DAGs computing `a` and `b`. Then `opt(f) = 1 + opt(a) + opt(b) − s(a,b)`, where
> `s(a,b) = |D_a ∩ D_b| ∈ {0,1}` counts the shared gates.*

Structurally, take `g` to be the output gate of the six-gate optimum for ⊕₃: its children `a, b` share
the three-gate parity-2 block (computing `¬(x₁⊕x₂)` in the Lean witness `c6`; `x₁⊕x₂` up to free
output polarity), so `|D_a ∩ D_b| = 3` and, since each child has `opt = 4`, `s = 1 + 4 + 4 − 6 = 3 ∉
{0,1}`. One child, `(x₁⊕x₂) ∧ ¬x₃`, has its `opt = 4` certified by a DRAT chain (UNSAT at
`k = 1,2,3`; Appendix C); the other child is NPN-equivalent (input/output polarity), hence also
`opt = 4`. Krinkin's own `s ≤ 1` derivation is separately unsound: he needs `s ≤ tree(f) − opt(f)`,
but the §2 identity gives `tree(f) ≤ 1 + opt(a) + opt(b)`, i.e. `s ≥ tree(f) − opt(f)` — the reverse
of the comparison the proof requires. (For parity itself `s = tree − opt = 3`, an equality, so
Krinkin's first inequality happens to hold there; his chain then breaks at the *second* step,
`tree − opt ≤ 1`, which is Theorem 2.) Krinkin's Table 3 reports `s = 1` for the complete opt-6 `n=3`
bucket, which includes the parity decompositions — consistent with his having imposed the bound, and
in conflict with the structural count `s = 3`.

**Fate of the other results.** Theorem 7 (a classification assuming `gap = 1`) loses its proof, which
depends on Corollary 6; its conditional statement under the standard definition is not refuted by ⊕₃
(gap 3) and is left unproven. **Theorems 3 and 4 survive.** Theorem 3's published proof applies Lemma
1 (gate elimination) to the sub-DAG `S` below the shared gate `g` and writes `|S| ≥ k−1`, which fails
when `g` is at input level; a corrected incidence-count proof is in Appendix A.

**Diagnostic signature.** In Krinkin's complete `n = 3` table (Table 1), the two functions with
`gap = 1` at `opt = 6` are parity and its complement — precisely what the §2 identity (with `opt` in
the children: `1 + opt(parity) + opt(1) = 7`) reports, while the true formula size is 9. The error is
visible in the paper's data.

**Verification.** The counterexample is formalized in Lean 4.31.0 without Mathlib (`UnitGap.lean`):
the witnesses and the DP's structural framework are kernel-checked (`decide`, induction); the finite
fact `par3 ∉ D₈` — hence `tree(⊕₃) ≥ 9` — is discharged by `native_decide` (compiler-trusted, not
kernel). We report this precisely rather than as blanket "kernel-checked" (see §6).

¹ The gap distribution at `n = 3` (`{gap 0: 214, 1: 40, 3: 2}`) is reproduced by `tree_gap_n3.py`; the
per-cost histogram above was independently re-derived during adversarial review (REV-0010).

## 4. The failure is structural: AIG gap census at n = 4

We computed `tree(f)` for all 65,536 functions by a layered dynamic program (independently
re-implemented as a global Bellman fixed point with explicit polarities — all 65,536 cells agree),
joined with the complete exact `opt` catalog. The distribution of `gap` over the 222 NPN classes:

| gap | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| classes | 93 | 57 | 40 | 13 | 14 | 2 | 3 |

**72 of the 222 NPN classes (32.4% of classes) have `gap ≥ 2`** (a fraction of classes, not of all
65,536 functions, whose orbit sizes differ). The maximum gap 6 is attained by three **distinct** NPN
classes `{0x1668, 0x16e9, 0x6996}` — all with `opt = 9`, `tree = 15` — distinguished by their XAG
optima (`opt_XAG = 6, 5, 3` respectively; `opt_XAG` is NPN-invariant, so distinct values force
distinct classes). One of the three is parity-4 (`0x6996`, `opt_XAG = 3`). For parity-4, Khrapchenko's
bound (`≥ 16` leaves ⟹ `≥ 15` gates) meets `tree = 15` with equality. The embedded `n = 3` functions
reproduce the `n = 3` table 256/256. Parity is thus **a** witness of the maximum gap, not its
exclusive source: the census is consistent with, but does not by itself isolate, "linear structure
without native XOR" as the mechanism for all 72 violating classes.

## 5. Base dependence: XAG, MIG, and a directed search at n = 5

The large parity AIG gaps coincide with the cost of building parity from AND gates, suggesting a basis
artifact.

**XAG, `n ≤ 4` (exhaustive).** With a native XOR gate, the pipeline (encoder validated by an
independent exhaustive enumeration at `n = 3` and by a formula-encoder gate on all 222 `n = 4`
classes) gives `opt_XAG` maximum 7 (strictly below AIG in 190/222 classes; `opt_XAG(⊕₄) = 3`) and
`tree_XAG` maximum 7. The gap census (`certs`: `npn4_xag_gap.csv`): `n = 3` — `gap_XAG = 0` for all
256 functions; `n = 4` — `gap_XAG ∈ {0,1}`, distributed `{0: 218, 1: 4}`. The unit-gap property, false
in AIG, **holds in XAG for `n ≤ 4`** under this separately gated encoder whose UNSAT instances are not
proof-certified (§6).

**XAG, `n = 5` (directed search).** Exhaustive census is infeasible (`2³²` truth tables). We searched
for a *separator* (`gap_XAG ≥ 2`) by generating candidate functions from random XAG circuits with
sharing and XOR bias, keeping those essential in all five variables, and deciding `opt_XAG` and
`tree_XAG` exactly by SAT (ascending search, 20 s cap). This is a **generator-reachable, solver-decided
sample**, not a probability statement: functions whose `opt` timed out or exceeded the cap are not
written and thus not counted, so the sample is conditional on easy circuit optimization. The formula
encoder was gated before the search (matching the `n = 4` DP on all 222 classes, including the four
with `gap = 1`); an early false positive (parity-5) was fixed by ascending from `opt` (Appendix B).

Over **25,373 distinct** essential functions of five variables (deduplicated across workers):

| verdict | functions | % |
|---|---:|---:|
| gap 0 | 24,875 | 98.04 |
| gap 1 | 294 | 1.16 |
| inconclusive (SAT timeout) | 204 | 0.80 |
| **separator (`gap ≥ 2`)** | **0** | **0** |

**No separator was certified.** All **25,169 gap-decided** functions have `gap_XAG ∈ {0,1}`; the 204
inconclusive cases are formula-search timeouts and could in principle be separators. As an added
check, all 294 gap-1 functions and a sample of 200 gap-0 functions were re-decoded and
simulation-verified (optimal circuit and formula both compute the truth table); 494/494 passed
(Appendix C). This is a **directed sample, not a proof**: a separator of high `opt`, or outside the
generation bias, is not excluded. What the search establishes is that no separator appears among
25,169 gap-decided, generator-reachable essential functions of `n = 5`.

**MIG (aggregate cross-check).** Soeken, Amarù, Gaillardon and De Micheli (DATE 2016) published the
optimal MIG size distribution for the 222 classes of `n = 4`. We re-derived the census with a
different solver (kissat vs. Z3) and encoding and matched the published **size distribution**
`{0:2, 1:2, 2:5, 3:18, 4:42, 5:117, 6:35, 7:1}` **bucket by bucket**, including the unique 7-node
class. (Their table publishes bucket counts, not a per-class map; equal aggregate distributions
cross-check the shared exact-synthesis machinery, not the per-class assignments.)

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
| `opt(⊕₃) = 6` (lower bound) | DRAT proofs for UNSAT at **every `k = 1..5`**, drat-trim `s VERIFIED`; transcript + hashes archived (Appendix C) |
| `opt` of the shared child `= 4`; other child NPN-equivalent | DRAT proofs for UNSAT at `k = 1,2,3` on the representative child, drat-trim `s VERIFIED`; the second child is NPN-equivalent |
| `tree(⊕₃) = 9`; witnesses | Lean 4 kernel (`decide`) for witnesses + DP structural framework; the finite exclusion `par3 ∉ D₈` (hence `tree ≥ 9`) by `native_decide` (compiler-trusted); two implementations of the same recurrence agree |
| `gap(⊕₃) ≥ 2` | Analytic (Khrapchenko + six-gate circuit), independent of the tree DP and the DRAT chain |
| AIG gap census `n = 4` | Two implementations of the tree recurrence agree on all 65,536 cells; `opt` side inherits catalog certification |
| XAG census `n ≤ 4` | Gated encoder (independent exhaustive enumeration at `n = 3`; formula encoder matches DP on all 222 `n = 4` classes); SAT models simulation-verified; UNSAT side not proof-certified (declared) |
| XAG search `n = 5` | Encoder gated at `n ≤ 4`; 494 instances (all gap1 + a gap0 sample) re-decoded and simulation-verified; sample, not exhaustive (declared) |
| MIG census `n = 4` | Same gating + exact match with an independently published size distribution (aggregate) |

The two `tree` implementations are independent *implementations of the same Bellman recurrence*
(layered vs. fixed-point) — strong bug detection; the semantic bridge (that the recurrence computes
formula size) is the Lean completeness lemma. The four-model-family adversarial review is provenance,
not part of the verification chain.

## 7. Related work and novelty

- **Krinkin, arXiv:2603.08033** is the refuted paper; **arXiv:2603.09379** (an NPN-4 AIG catalog whose
  two open entries we closed) is a companion note. Both were communicated to the author
  (`krinkin/unit-gap#1`, `krinkin/bounds#1`).
- **MIG:** the optimal `n = 4` sizes were previously published (Soeken et al., DATE 2016; TCAD 2017);
  our census is replication, claimed only as an aggregate cross-check.
- **XAG total-gate count** is essentially the classical combinational complexity over `B₂`, tabulated
  for small `n` by Knuth (TAOCP 7.1.2); our maximum of 7 agrees. We claim **no novelty for the XAG
  numbers themselves**.
- **Contributions reported here:** (i) the refutation of Theorem 2 and Corollary 6, with machine-
  checked certificates and a Lean formalization, and the localization of the error to the two
  incompatible characterizations in §2 and §3; and (ii) the first *explicitly tabulated* gap-by-basis
  comparison (`tree − opt` per NPN class) in AIG and XAG at `n ≤ 4`, with a directed `n = 5` XAG
  search. The `tree − opt` difference is a subtraction of columns each of which is classical, so (ii)
  is a contribution of organized data and the base-dependence observation, not of a new measure; it is
  likely implicit in any catalog publishing both sizes. We searched Knuth's B₂ data, the MIG/AIG
  catalogs, and standard references without finding the gap-by-basis comparison stated explicitly, but
  treat (ii) as "apparently unreported" pending a specialist check.

## 8. Open questions

1. Does `gap_XAG` remain in `{0,1}` for all of `n = 5` (the directed search certified no separator
   among 25,169 gap-decided functions) and for larger `n`? Parity no longer separates in XAG; other
   separators are not excluded.
2. Is there a theorem behind the empirical XAG unit gap at small `n` — e.g. a normal-form argument
   bounding sharing once linear structure is factored out?
3. An efficient exact DP for `tree_MIG` (the deferred MIG gap column).
4. A corrected, basis-relative formulation of Krinkin's Theorem 7, with proof.

## References

<!-- a formatar na conversão LaTeX -->
- K. Krinkin. *The Unit Gap: How Sharing Works in Boolean Circuits.* arXiv:2603.08033v2.
- K. Krinkin. *[NPN-4 AIG catalog].* arXiv:2603.09379.
- V. M. Khrapchenko. *Complexity of the realization of a linear function in the class of Π-circuits.*
  Mathematical Notes 9(1):21–23, 1971.
- M. Soeken, L. Amarù, P.-E. Gaillardon, G. De Micheli. *Optimizing Majority-Inverter Graphs with
  exact synthesis.* DATE 2016; extended IEEE TCAD 2017.
- D. E. Knuth. *The Art of Computer Programming*, Vol. 4A, §7.1.2.
- A. Kojevnikov, A. S. Kulikov, G. Yaroslavtsev. *Finding efficient circuits using SAT-solvers.* SAT 2009.
- kissat 4.0.4; drat-trim; Lean 4.31.0.

## Appendix A. Corrected proof of Theorem 3 (Threshold)

*Claim.* If `f` has `n` essential variables and `gap(f) = 1`, then `opt(f) = m ≥ n`.

*Proof.* Since `gap(f) = 1`, take a size-optimal single-output AIG `C` for `f`. `C` is **not a tree**:
if it were, `tree(f) ≤ |C| = opt(f)`, forcing `gap(f) = 0`, contrary to hypothesis. So some non-output
gate of `C` has fan-out ≥ 2. Now count input incidences. Every gate has two inputs, so the total
number of input slots is `2m`; partition them into `I_var` slots reading a primary input or the
constant, and `I_gate` slots reading another gate, so `2m = I_var + I_gate`.

- *Essential variables:* each of the `n` essential variables must feed at least one slot (else `f`
  would not depend on it), so `I_var ≥ n`.
- *Gate usage:* each of the `m − 1` non-output gates feeds at least one later slot (normalized
  circuit: no unused gate), contributing `≥ m − 1`; the fan-out-≥2 gate contributes at least one
  further incidence, so `I_gate ≥ m`.

Hence `2m = I_var + I_gate ≥ n + m`, i.e. `m ≥ n`. ∎

(The bound holds for any non-tree optimal single-output circuit, subsuming the `gap = 1` case. The
published proof's `|S| ≥ k−1` step applies gate elimination to the cone `S` *excluding* the shared
gate `g`; when `g` is at input level the `k` essential variables of `S ∪ {g}` are not all covered by
`S`, and the count is short by one. The incidence argument avoids the case split.)

## Appendix B. Encoders, gates, and the parity-5 false positive

The AIG, XAG, and multi-output encoders and their validation gates: G1–G3 (AIG single-output), the
multi-output gate, and G-T1/G-T2/G-T3 for the XAG formula encoder (`n = 3` complete `tree = opt`;
`n = 4` `tree_via_sat` matches the independent DP on all 222 classes, covering the four with
`gap = 1`).

**The parity-5 false positive.** The first `n = 5` search implementation tested formula-satisfiability
at exactly `opt + 1` gates in isolation and declared a separator when that single instance was UNSAT.
This is unsound for a normalized exact-size encoder: UNSAT at exactly `opt + 1` means "no formula of
*exactly* `opt + 1` gates", not `tree ≥ opt + 2` (a formula of a different size may exist). The bug
surfaced on parity-5 (`0x69969669`), a linear function with `gap_XAG = 0`, which the isolated test
misreported as a separator. The fix searches **ascending from `opt`** (`tree` is the first `k ≥ opt`
with a satisfiable formula encoding); parity-5 then correctly returns `gap 0`. All results in §5 use
the fixed procedure.

## Appendix C. Reproducibility

kissat 4.0.4; drat-trim (marijnheule @ commit 2e3b2dc); Lean 4.31.0. Versioned artifacts: encoders,
gates, censuses (AIG `npn4_gap.csv`, XAG `npn4_xag_gap.csv` with per-class `opt_xag/tree_xag/gap_xag`,
MIG); CNFs and the `k = 1..5` DRAT proofs for `opt(⊕₃)` and `k = 1..3` for the representative child;
the drat-trim transcript `certs/verify_lowk.log` (`s VERIFIED`, exit code, and CNF/DRAT SHA-256 for
all eight proofs); the `n = 5` search CSVs (raw per-worker and globally deduplicated) and the 494/494
re-verification log; and the Lean sources. The `n = 5` search seeds are deterministic per worker; the
bench is a 2-vCPU VPS.

<!-- Provenance note (tom a definir com Luiz; fora do corpo; SEM claim de pioneirismo):
     analysis and code produced by an AI system under the direction of L. A. Busnello; certificates
     checked by standard independent tools (kissat, drat-trim, Lean); claims adversarially reviewed by
     four independent model families before external communication. -->
