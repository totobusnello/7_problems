# Adversarial Review — Round 2 (`paper1_unitgap_basedep_v1.md`)

I tried to re-open Round-1 holes and to invent new ones from the v1 edits. The core refutation still stands. Several Round-1 items are genuinely closed against artifacts; a few claimed closures are incomplete or overstated; and the v1 “internal inconsistency” reading is fair but one notch sharper than the PDF’s wording.

---

## 1) Did the corrections actually close Round 1?

Checked against `search_n5_dedup.csv`, `npn4_gap.csv`, `npn4_xag.csv`, `certs/`, `UnitGap.lean`, `verify_n5_recheck.py`, and the arXiv PDF `_sources/krinkin_2026_unit_gap.pdf`.

| # | Claimed fix | Artifact check | Closed? |
|---|---|---|---|
| **A1** n=5 distinct | `search_n5_dedup.csv`: 25,373 data rows; verdicts **24,875 / 294 / 204 / 0** | Matches abstract + §5 exactly | **YES** |
| **A2** three max-gap classes | `npn4_gap.csv`: `0x1668,0x16e9,0x6996` all gap 6 (opt 9 / tree 15). Weights 6 / 8 / 8. `npn4_xag.csv`: opt_XAG **6 / 5 / 3** | Distinct NPN; parity is one of three | **YES** |
| **A3** DRAT k=1..5 | `certs/par3_k{1..5}.{cnf,drat}` all present (k1–k4 dated 2026-07-17). `h_child_k3` present | **Artifacts yes; “s VERIFIED” for k=1..4 not evidenced** (see CRITICAL/IMPORTANT) | **PARTIAL** |
| **B2** `native_decide` | `UnitGap.lean:271–272` `par3_not_in_D8` by `native_decide`; `tree_lower` uses it | Paper §3/§6 accurate | **YES** |
| **B3/B4** hedges | Abstract: XAG “under a gated… pipeline”; MIG “bucket by bucket”; §5 spells distribution-not-class | Matches | **YES** |
| **B1** n=5 sim | No longer “each result verified”; §5/§6: 494/494 via `verify_n5_recheck.py` | Script targets all gap1 + 200 gap0 | **YES** (contingent on that run having been executed) |
| **B5** same recurrence | §6: “independent *implementations of the same* Bellman recurrence” | Matches | **YES** |
| **C1** Krinkin quotes | PDF §2 formula def, §2 recursion with `opt`, §3 Bellman with `v` + “computes tree(f)” + overshoot ∈{0,1}, Cor.6 `s=\|Da∩Db\|∈{0,1}` | Faithful enough (see MINOR truncation) | **YES** |
| **C6** Thm 3 proof | Appendix A: `2m=I_var+I_gate`, `I_var≥n`, `I_gate≥m` ⇒ `m≥n` | Valid under stated hypotheses (see MINOR) | **YES** |
| **C3/C5/C2** wording | Probability rhetoric gone; “32.4% of classes”; “consistent with, but does not isolate”; novelty hedge in §7 | Matches | **YES** |
| **C9** flow table | Conditional sample declared; no generator→verdict flow table | **Wording only** | **PARTIAL** |

Gap census 93+57+40+13+14+2+3 = 222; 72/222 = 32.4%. n=5 24875+294+204 = 25373. Cross-section numbers are internally consistent.

---

## CRITICAL

### C1 — Abstract / §3 / §6: “each [k=1..5] … drat-trim `s VERIFIED`” is not backed for k=1..4

**What is true.**  
`certs/par3_k1.drat` … `par3_k5.drat` exist. `gen_drat_par3_lowk.py` builds CNFs via the normalized encoder and asks kissat for proofs. That **closes the Round-1 artifact hole** (missing files).

**What is not evidenced.**  
- `gen_drat_par3_lowk.py` explicitly says: *“Verificacao drat-trim: rodar separadamente.”*  
- Historical `check_claims_output.txt` only logs **k=5** and **h_child_k3** as `s VERIFIED`.  
- `drat-trim` is not even on `PATH` in this environment.  
- No new log, checksum, or CI step for k=1..4 trim.

So the abstract’s load-bearing sentence — UNSAT at every k=1..5, **each** checked with drat-trim — currently overclaims relative to the repo record. Kissat-produced `.drat` files are not the same as independent `s VERIFIED`.

This does **not** rescue Theorem 2: six-gate witness + Khrapchenko still give `gap ≥ 2`, and Lean still gives `tree ≥ 9`. It does weaken the advertised certification level for `opt = 6` and `gap = 3`.

**Concrete fix.**  
Run and archive:

```text
for k in 1 2 3 4 5; do drat-trim certs/par3_k$k.cnf certs/par3_k$k.drat; done
```

Paste `s VERIFIED` + sizes/hashes into Appendix C (and regenerate `check_claims_output`). Until then, write: “DRAT proofs produced by kissat for k=1..5; k=5 (and child k=3) independently trim-verified; k=1..4 trim verification pending” — or just run the tool.

---

### C2 — §3 / §6: child `opt = 4` still has the exact-size certification hole (A3 half-fixed)

Paper: *“`opt` of each child = 4 certified by an UNSAT-at-3 DRAT proof.”*

Only `h_child_k3` exists. Under the **normalized exact-size** encoder (the whole point of A3), UNSAT@3 proves `opt ≠ 3`, not `opt ≥ 4`. Possible residual values include 1 or 2 unless excluded.

Cor 6’s **structural** hit (`|Da ∩ Db| = 3` in the exhibited circuit) does **not** need `opt(a)=4`. The **arithmetic** line `s = 1+4+4−6 = 3` does. §6’s table row for the child is overstated in the same way Round 1 hammered for parity.

**Concrete fix (any one):**  
1. Generate DRAT for child at k=1,2 (and keep k=3); or  
2. Write the restriction lemma: `h|_{x3=0} = x1⊕x2` needs 3 AIG gates, and combining with `x3` forces ≥4, with SAT@4; or  
3. Downgrade text to “child has a 4-gate circuit; UNSAT@3; opt=4 under ascending search / restriction.”

---

## IMPORTANT

### I1 — §3 “two incompatible definitions”: fair diagnosis, slightly over-sharp packaging

**PDF facts (checked):**  
- §2: formula = fan-out one; displays `tree(f) = min (1+opt(a)+opt(b))`; “trivial decomposition f=1∧f always achieves 1+opt(f)”.  
- §3 Thm 2 proof upper bound: literally `tree ≤ 1+opt` via `f=1∧f`.  
- §3 Bellman: `(Tv)(f)=min(1+v(a)+v(b))`, “computes tree(f)”, fixed point “overshoots opt by exactly gap∈{0,1}”.  
- §7: same T, “overshoots by exactly 0 or 1, never more.”

**Fair.** Under the verbal definition, the Thm 2 upper bound is invalid (child is an `opt`-circuit, not a formula). The Bellman with recursive `v` is the real formula recurrence; for ⊕₃ it yields 9, overshoot 3. Table 1 at opt=6 (gap0=16, gap1=2) matches the hybrid one-shot measure, not true formula size. That diagnostic is solid.

**Over-sharp.** Krinkin does not present two *named competing definitions*. §2 is written as an equality that tree “satisfies,” and the Thm 2 proof only needs the one-sided `f=1∧f` abuse. Calling them “two incompatible definitions, of which the first makes Theorem 2 a one-line tautology” is rhetorically right and mathematically usable, but a hostile author (or referee) can say: “§2 is a claimed property under the theorem, not a second definition.”

**Concrete fix.** Prefer:  
> “The upper bound in the Theorem 2 proof treats an optimal circuit child as if it were a formula (via f=1∧f / the §2 display with `opt` in the children). The Bellman operator of §3/§7, which the paper says computes formula size, is the standard recursive measure and already falsifies the unit-gap claim on ⊕₃.”

Keep the incompatibility; attribute it primarily to **proof/type error + inconsistent use of `tree`**, not to two formal definitions.

---

### I2 — Verbatim block-quotes: faithful, with one packaging risk on Cor 6

Checked against PDF p.2, p.3, p.5:

| Quote | Faithful? |
|---|---|
| Formula / fan-out one / gap | Yes (minor reformatting) |
| §2 recursion with `opt` | Yes |
| §3 Bellman + “computes tree” + overshoot | Yes (ellipsis OK) |
| Cor 6 formula + `s=\|Da∩Db\|∈{0,1}` | Yes — PDF really writes `∈{0,1}` in the statement |

**Risk.** Grouping `∈{0,1}` inside the definitional `where` makes it look like a definitional restriction; in the PDF it is already a claimed bound baked into the corollary statement, derived from Thm 2. Not a misquote, but add one sentence: “the ∈{0,1} is not an independent definition of s; it is derived from Theorem 2 in the proof.”

Bellman quote omits that §3’s min is written over `f=a∧b` only (not `f̄=a∧b`); harmless given free output inversion, but a pedant could nitpick. **MINOR** if you add “up to output polarity.”

---

### I3 — Cor 6 / `s=3`: no rescue via re-reading `Da, Db`

PDF Cor 6: *“Let Da, Db be the sub-DAGs computing a and b … s(a,b)=|Da∩Db|.”* Proof uses inclusion-exclusion `|Dg|=1+|Da|+|Db|−|Da∩Db|` and Remark 5 (sub-DAGs of an optimal AIG are optimal for their functions).

In the standard 6-gate dual-polarity XOR construction, the two output-child cones both contain the three-gate `x1⊕x2` block ⇒ intersection size 3.  

Charitable escapes fail:  
- Counting only fan-out≥2 gates as “shared” (s=1) **contradicts the written `|Da∩Db|`**.  
- Taking separately re-synthesized minimal DAGs for a and b (possibly disjoint) **breaks the inclusion-exclusion identity in the parent**.  
- Table 3’s “s=1 (100%) at opt=6” is then a **symptom** of computing s from the circular bound, not of a different D-set definition — exactly as v1 says.

No CRITICAL hole here. Keep structural s=3 as primary; arithmetic as check.

**MINOR imprecision:** Table 3 is all n=3 opt=6 decompositions (299), not “of parity” alone. Say “including the parity decompositions” or “all opt=6 decompositions (parity among them).”

---

### I4 — Hedges: mostly right; two residual overstatements

| Location | Issue | Fix |
|---|---|---|
| Abstract “we **show** … base-dependent” | Exhaustive only for n≤4 XAG; n=5 is a sample | “show for n≤4 (exhaustive) and support with a directed n=5 search” |
| §5 “holds in XAG for n≤4 under this gated pipeline” | Correct with UNSAT-uncertified hedge | Keep |
| §5/§8 n=5 | Good “sample not proof” | Keep; still no full candidate flow (C9) |
| MIG | “bucket by bucket” correct | Keep |

Not too weak. Not still claiming class-by-class MIG or kernel-only Lean.

---

### I5 — Residual n=5 population bias (C9 not closed)

v1 correctly drops probability talk and states the sample is conditional on easy `opt`. It still does **not** log opt-timeouts / `opt>kmax` discards. A separator could hide in the uncounted tail.

**Fix.** Either re-instrument `search_n5.py` for a generated→filtered→decided flow table, or one sentence in §5: “Candidates with opt timeout or opt>kmax are discarded before write and are not in the 25,373.”

---

### I6 — Appendix A (Thm 3): valid, with one polish item

Proof structure is correct for single-output, all-gates-used, non-tree AIGs with n essential inputs:

- `2m = I_var + I_gate`  
- essential vars ⇒ ≥n primary-input incidences ⇒ `I_var ≥ n`  
- m−1 non-outputs used once each, plus ≥1 extra from some fan-out≥2 ⇒ `I_gate ≥ m`  
- ⇒ `m ≥ n`

**Polish (MINOR→IMPORTANT if a referee is pedantic):**  
- State explicitly that optimality ⇒ no unused gate (so normalization is free).  
- “or the constant” in the `I_var` sentence is slightly muddy: constants inflate `I_var` but the lower bound only needs primary-input incidences ≥ n — say that.  
- Note the claim proved is stronger than Krinkin’s (`gap≥1`, not only `gap=1`), which is fine and should be labeled as such.

This closes Round-1 C6.

---

## MINOR

1. **§3 Bellman quote:** add “up to output polarity” / note §3’s min is written over `f=a∧b` only.  
2. **Table 3 “of parity”:** broaden as above.  
3. **Abstract “fan-out one at every gate”:** already parenthetically fixed in §2; fine.  
4. **Lean trust sentence:** good; optional `#print axioms tree_lower` footnote mentioning `Lean.ofReduceBool`.  
5. **Technote / findings notes** still carry stale 29,643 in body text (headers corrected). Not in v1 paper, but clean before any joint release.  
6. **§6 “two implementations … same recurrence”** + Lean completeness: good; don’t re-inflate to “independent semantics.”  
7. **Khrapchenko arithmetic** (144/16=9 leaves ⇒ ≥8 gates): still correct; fail-safe intact.

---

## What I deliberately could **not** break

- True formula size of ⊕₃ is 9 under fan-out-one AIGs (DP + Lean completeness + layer profile).  
- Khrapchenko ⇒ `tree ≥ 8` ⇒ `gap ≥ 2` from the six-gate upper bound alone.  
- Cor 6’s `s∈{0,1}` fails on the exhibited optimal-size circuit under Krinkin’s own `|Da∩Db|`.  
- Gap census and three distinct max-gap NPN classes (weights + opt_XAG).  
- n=5 dedup numbers.  
- MIG “bucket by bucket” and XAG UNSAT-uncertified hedges.  
- `native_decide` honesty for `par3 ∉ D₈`.

Concordance with Round-1’s “refutation survives” is **not** taken as proof; the PDF + certs + CSVs were re-read.

---

## ONE-LINE VERDICT

**Not submission-ready yet:** v1 closes the material Round-1 data/hedge issues and the Thm 3 write-up, but must (i) actually drat-trim–log k=1..4 (or hedge the abstract), and (ii) finish the child-opt lower-bound chain before LaTeX conversion and the author-response window.
