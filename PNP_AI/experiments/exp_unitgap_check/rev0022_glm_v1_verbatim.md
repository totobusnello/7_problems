I have all the evidence. Let me compile the hostile review.

---

# Adversarial Review — Round 2 (v1)

I read the full v1, the v0 consolidado, the technote, and verified every numeric/cert claim against the artifacts (Lean source, `search_n5_dedup.csv`, `npn4_gap.csv`, `npn4_bases.csv`, the DRAT certs, the verify log) AND against Krinkin's actual PDF (`_sources/krinkin_2026_unit_gap.pdf`, extracted via `pdftotext`).

## PART 1 — Did the Round-1 corrections actually close the findings?

| Round-1 finding | v1 claim | Verified against | Status |
|---|---|---|---|
| A1: n=5 = 25,373 (not 29,643) | "25,373 distinct essential functions" | `search_n5_dedup.csv`: 25,373 rows, 25,373 distinct `tt`, verdict counts gap0=24,875 / gap1=294 / inconclusive=204 / sep=0 — **byte-exact match**; reference `essential_all5` returns True for 25,373/25,373 | **CLOSED** |
| A2: 3 max-gap classes distinct NPN | "three distinct NPN classes {0x1668, 0x16e9, 0x6996}, one being parity-4" | `npn4_gap.csv`: exactly these 3 at gap=6, all opt=9/tree=15; `npn4_bases.csv`: opt_XAG = **6/5/3 (distinct → 3 NPN classes)** | **CLOSED** |
| A3: DRAT chain k=1..5 | "UNSAT for every k=1..5, each DRAT, drat-trim s VERIFIED" | `certs/par3_k1..k5.drat` all present (65/101/7447/26504/147189 bytes); `verify_par3_lowk.log` shows 5× "s VERIFIED" with SHA256 hashes for CNF+DRAT | **CLOSED** (I could not re-run drat-trim — not installed — but the hashes + log are consistent and the files are valid DRAT-format) |
| B2: tree≥9 via native_decide | "par3 ∉ D₈ by native_decide (compiler-trusted, not kernel)" | `UnitGap.lean:271-272`: `par3_not_in_D8 ... by native_decide`; `tree_lower` (line 276) derives from it; `#print axioms tree_lower` is in the audit block | **CLOSED** |
| B3: XAG hedge "under gated pipeline, UNSAT uncertified" | Stated in abstract, §5, §6 | Verbatim present in all three places | **CLOSED** |
| B4: MIG "bucket by bucket" | "matched the published size distribution {0:2,1:2,2:5,3:18,4:42,5:117,6:35,7:1} bucket by bucket" | `npn4_bases.csv` MIG column: **exact match** {0:2,1:2,2:5,3:18,4:42,5:117,6:35,7:1}; v1 also explicitly disclaims per-class match | **CLOSED** |
| C1: Krinkin verbatim | Four block-quotes (§2 formula def, §2 recursion, §3 Bellman, Cor 6) | Checked against `pdftotext` extraction of Krinkin's PDF: **all four quotes are faithful, in-context, no truncation that changes meaning** | **CLOSED** |
| C6: Thm 3 corrected proof in appendix | Incidence argument in Appendix A | See below — proof is valid (and strictly stronger than Krinkin's original statement) | **CLOSED** |

**Theorem 3 proof audit (Appendix A).** I checked the proof line by line. `2m = I_var + I_gate` (every AND has 2 fan-in slots) ✓. `I_var ≥ n` (each essential variable must be read somewhere) ✓. `I_gate ≥ m`: baseline `(m−1)·1` from each non-output gate feeding ≥1 later slot (normalized: no unused gate), plus ≥1 extra from a fan-out-≥2 gate in a non-tree circuit → `I_gate ≥ (m−1) + 1 = m` ✓. Conclusion `2m ≥ n+m ⟹ m ≥ n` ✓. The argument works and proves `m ≥ n` for the **weaker** hypothesis "non-tree optimal circuit", which subsumes Krinkin's "gap=1" case.

## PART 2 — New problems introduced by the v1 edits

### CRITICAL
None. I could not find any load-bearing hole. The refutation, the census, the certificates, and the hedges all hold.

### IMPORTANT

**I1. §3 / abstract: sign error in the description of the shared block.** The v1 says the three-gate shared block is "computing `x₁⊕x₂`". The Lean witness `c6` (`UnitGap.lean:339-344`) defines the shared block as nodes 3, 4, 5 where `node5 = ¬node3 ∧ ¬node4 = ¬(x₁⊕x₂)`. So the shared block computes **`¬(x₁⊕x₂)`**, not `x₁⊕x₂`. This does not affect the arithmetic (`s = 1+4+4−6 = 3` either way) nor the structural count (3 gates either way), but a referee who opens `UnitGap.lean` will catch the mismatch on the first read, and Krinkin himself will catch it too. **Fix:** §3 paragraph on Cor 6 and the abstract: change "computing `x₁⊕x₂`" to "computing `¬(x₁⊕x₂)` (equivalently, the parity-2 block up to output polarity)".

### MINOR

**M1. §4: Hamming weight is a red herring for NPN distinctness.** The v1 argues the three classes are distinct NPN by citing "Hamming weight 6 and 8 versus parity's 8, and distinct XAG optima 6 and 5 versus parity's 3". Hamming weight is **not NPN-invariant** (input negation changes it), so it proves nothing about NPN distinctness. The XAG optima (6/5/3) alone are an NPN-invariant discriminator and suffice. **Fix:** drop the Hamming weight clause or relabel it as descriptive ("they also differ in Hamming weight"), keeping XAG opt as the sole proof of distinctness.

**M2. §3: the "internal inconsistency" framing is fair but slightly conflates a Theorem-2-dependent assertion with a definition.** The v1 writes "§3 … claims its fixed point 'overshoots `opt(f)` by exactly `gap(f) ∈ {0,1}`'." Verified against Krinkin's PDF: he does write this — but as a **consequence** of Theorem 2, not as a second definition of `tree(f)`. So strictly it is §2's displayed identity (`opt` in children) that is *incompatible with §3's Bellman fixed point (`v` in children)* as definitions of `tree(f)`. The "overshoot ∈ {0,1}" claim collapses *with* Theorem 2; it does not, by itself, contradict §2. The v1's argument still lands (the dilemma "§2 is a tautology OR §3 refutes Thm 2" is genuine), but a careful referee (or Krinkin) can ask for cleaner separation. **Fix:** one sentence clarifying that the third quoted clause is Krinkin's *derived* claim (conditional on Thm 2), not a third definition.

**M3. Appendix A: the parenthetical "(so `gap(f) ≥ 1`)" is imprecise.** "Computed by a size-optimal non-tree AIG" does not strictly imply `gap ≥ 1` if a same-size tree-optimal circuit also exists (in which case `gap = 0`). The incidence argument applies to the specific non-tree optimal circuit taken as the witness, so the main claim `m ≥ n` survives — but the parenthetical is logically loose. **Fix:** drop "(so `gap(f) ≥ 1`)" or replace with "(a circuit in which some non-output gate has fan-out ≥ 2)".

**M4. Appendix B: promised documentation of the parity-5 false positive is not delivered.** Appendix B says "The parity-5 false positive in the `n = 5` search and its fix (ascending search from `opt`) are documented here" — but Appendix B then only lists encoder gates, no actual documentation of the bug or the fix. A referee will read this as a broken promise. **Fix:** either add 3–4 sentences actually documenting the false positive (what the encoder reported, why, what the ascending-from-`opt` change was) or drop the sentence.

**M5. Abstract: "the unit-gap property holds (under a gated exact-synthesis pipeline)" could be misread as "for all n".** The lead clause doesn't qualify `n ≤ 4`. The immediately-following enumeration (n=3 exhaustive, n=4 exhaustive, n=5 directed search) does disambiguate, and §8 Open Question 1 explicitly leaves larger `n` open — but the abstract's own lead clause is unqualified. **Fix:** "the unit-gap property **for `n ≤ 4`** holds …; a directed search at `n = 5` finds no separator".

### Direct answers to the host's targeted questions

- **Is the "internal inconsistency" (§2 vs §3) reading fair, or an overreach?** Fair. Verified against the PDF: §2 displays `tree(f) = min 1+opt(a)+opt(b)` and labels it "the minimum formula size satisfies"; §3 defines `(Tv)(f) = min 1+v(a)+v(b)` and says "iterating T … computes `tree(f)`". At the fixed point the second gives `tree(f) = min 1+tree(a)+tree(b)`, which is a different mathematical object from the first. They cannot both equal `tree(f)` unless `opt = tree`. The v1's framing as a dilemma (§2 makes Thm 2 a tautology; §3 refutes it) is the *stronger* critique, not a strawman.
- **Verbatim quotes — any misquote / truncation / out-of-context?** None found. All four quotes (§2 formula definition, §2 recursion, §3 Bellman + "iterating T … computes tree(f)", Cor 6) match the PDF character-for-character modulo markdown styling. The ellipsis in "iterating `T` … computes `tree(f)`" omits "from the base case `v₀(xᵢ)=v₀(1)=0" — immaterial (monotone operator on a finite lattice has a unique fixed point).
- **Are the new hedges too weak or still overstated?** "Holds under gated pipeline (UNSAT uncertified)" — accurate. "Bucket by bucket" — accurately explained. "Directed sample, not a proof" — appropriate. Only the abstract's unqualified "holds" (M5) is still mildly overstated.
- **New numeric inconsistency across tables?** None. I checked abstract ↔ §4 table ↔ §5 table ↔ §6 table ↔ `npn4_gap.csv` ↔ `npn4_bases.csv` ↔ `search_n5_dedup.csv`. The AIG gap distribution (93/57/40/13/14/2/3 = 222), the XAG gap distribution (218/4), the MIG distribution ({0:2,1:2,2:5,3:18,4:42,5:117,6:35,7:1}), the cross-base maxima (AIG 10 / XAG 7 / MIG 7), opt(⊕₄)/tree(⊕₄) per base (9/15, 3/3, 6/—), and the n=5 distribution (24,875/294/204/0) are all internally consistent and match the data files.
- **Is there any reading of `D_a, D_b` under which `|D_a∩D_b| ≠ 3` for the 6-gate optimum?** No. Krinkin's Cor 6 explicitly says "`s(a,b) = |D_a∩D_b|`", and `D_a, D_b` are "the sub-DAGs computing `a` and `b`" inside the optimal circuit `C`. In `c6`, the output gate `g8` has children `a=¬g6, b=¬g7`; their sub-DAGs are `{node3,node4,node5,node6}` and `{node3,node4,node5,node7}`, intersection `{node3,node4,node5}`, size 3. The only escape (GLM's "s = #gates with fan-out ≥ 2 = 1") is a misreading that the verbatim Cor 6 text directly excludes. For internal gates (e.g., `node5`) the count is 0 or 1, but Krinkin's Cor 6 says "**any** gate", so the output gate is a valid choice.

## VERDICT (one line)

**v1 is mathematically sound, all Round-1 findings are genuinely closed against the artifacts, and the new edits introduced no critical or load-bearing defects — ready for LaTeX conversion after fixing I1 (the `¬(x₁⊕x₂)` sign error, which is visibility-only but will be the first thing a referee cross-checks) and the five MINOR items; ready for submission after the author-response window on `krinkin/unit-gap#1`.**
