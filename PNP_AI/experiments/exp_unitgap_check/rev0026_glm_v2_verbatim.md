I have completed a full audit. Here is my adversarial review.

---

# Adversarial Review — Round 3 (final confirmation, v2)

I read v2 in full, cross-checked every numeric claim against the CSVs, verified all 8 DRAT hashes against `verify_lowk.log`, extracted Krinkin's PDF via `pdftotext` to check the quotes, and verified the Lean source line-by-line. Concordance with rounds 1–2 was **not** taken as proof; every load-bearing claim was re-derived.

## PART 1 — Did v2 close the Round-2 findings?

| Round-2 finding (family) | v2 fix location | Artifact check | Closed? |
|---|---|---|---|
| **Sign error** ¬(x₁⊕x₂) vs x₁⊕x₂ (GLM I1) | §3 lines 144–146 | `UnitGap.lean:337–344`: `c6` node 5 = `¬n3 ∧ ¬n4`; n3=x₁∧¬x₂, n4=¬x₁∧x₂ ⟹ node 5 = (x₁∧x₂)∨(¬x₁∧¬x₂) = **¬(x₁⊕x₂)**. v2 says "computing `¬(x₁⊕x₂)` in the Lean witness `c6`" | **YES** |
| **opt_XAG as NPN discriminator**, not Hamming weight (GLM M1) | §4 lines 178–181 | `npn4_xag.csv`: `0x1668`→6, `0x16e9`→5, `0x6996`→3. opt_XAG is NPN-invariant (NPN ops preserve size in any fixed basis), distinct values ⟹ distinct classes. No Hamming-weight clause remains | **YES** |
| **Thm 3 bridge** gap=1⇒non-tree before incidence count (Codex I1, Grok I6, GLM M3) | App. A lines 305–319 | "Since `gap(f)=1`… `C` is **not a tree**: if it were, `tree(f) ≤ |C| = opt(f)`, forcing `gap(f)=0`, contrary to hypothesis." THEN the incidence count. Logically valid: gap=1 ⟹ tree>opt ⟹ optimal circuit not a tree (else tree≤opt). | **YES** |
| **Bellman base case** in quote (Codex I3, Grok I2) | §3 lines 109–110 | v2: "iterating `T` from the base case `v₀(xᵢ) = v₀(1) = 0` computes `tree(f)`". PDF p.3: "Iterating T from the base case v0(xi) = v0(1) = 0 computes tree(f)." — character-faithful. | **YES** |
| **Cor 6 premises** in quote (Codex I3) | §3 lines 136–138 | v2: "Let `C` be an optimal AIG, and let `g` be any gate computing `f = a ∧ b`. Let `D_a, D_b` be the sub-DAGs computing `a` and `b`." PDF p.5: "Let C be an optimal AIG, and let g be any gate computing f = a ∧ b. Let Da, Db be the sub-DAGs computing a and b." — faithful. | **YES** |
| **"Incompatible characterizations"** not "two definitions" (Codex I4, Grok I1, Kimi I2) | Abstract lines 23–25; §3 lines 103–104 | "incompatible characterizations of formula size, the first making Theorem 2 a one-line tautology and the second making it false". No "two definitions" anywhere. | **YES** |
| **Overshoot ∈{0,1} as consequence** of Thm 2 (Grok M2) | §3 lines 115–117 | "Krinkin further states (as a *consequence of Theorem 2*, not a definition) that `T`'s fixed point 'overshoots `opt(f)` by exactly `gap(f) ∈ {0,1}`' — which collapses together with Theorem 2." | **YES** |
| **s≤1 inequality reversed** (Codex I5) | §3 lines 140–143 | §2 identity gives `tree(f) ≤ 1+opt(a)+opt(b)` ⟹ `s ≥ tree(f)−opt(f)`, opposite to Krinkin's needed `s ≤ tree(f)−opt(f)`. I verified the direction algebraically: the minimizer of §2 is over ALL decompositions, so for the specific gate-g decomposition the inequality is indeed reversed in general. | **YES** |
| **25,169 decided vs 25,373 tested** (Codex I6, Grok I5) | Abstract lines 32–33; §5 lines 217–218 | CSV: 24,875+294+204=25,373 rows, 25,373 distinct TTs; decided = 24,875+294 = **25,169**; unresolved = 204. v2: "all 25,169 gap-decided functions have `gap_XAG ≤ 1`; 204 remain unresolved". | **YES** |
| **Abstract XAG hedge** (Codex I8, Grok I4) + **"for n≤4"** (GLM M5) | Abstract lines 29–31 | "the unit-gap property holds for `n ≤ 4` (under a separately gated exact-synthesis pipeline whose UNSAT side is not proof-certified)" — both qualifiers present. | **YES** |
| **Appendix B parity-5** (GLM M4) | App. B lines 333–340 | Documents the bug (testing exactly opt+1 in isolation is unsound for normalized encoder), the surface (parity-5 `0x69969669`), and the fix (ascending from `opt`). | **YES** |
| **verify_lowk.log archived** (Codex I7, Grok C1, Kimi CRITICAL) | App. C line 346; `certs/verify_lowk.log` | Log has 8 proofs, all "s VERIFIED". I recomputed all 16 SHA-256 hashes (8 CNF + 8 DRAT) — **every hash matches byte-for-byte**. | **YES** |
| **Child opt=4 DRAT chain** k=1,2,3 (Codex I2, Grok C2) | §3 line 146; §6 line 247; `h_child_k1..k3` | All 3 child DRAT files present (65/149/11546 bytes), all "s VERIFIED" with matching hashes. Lower bound ⟹ opt≥4; 4-gate witness is nodes {3,4,5,6} of `c6`. | **YES** |
| **494/494 recheck archived** (Kimi I1) | §5 lines 219–221; `verify_n5_recheck.log` | Log: "alvos: 294 gap1 + 200 gap0 = 494"; "VERIFICADAS POR SIMULACAO: 494/494". | **YES** |

**All 14 distinct Round-2 findings are genuinely closed.** I verified each against the artifact, not the prose.

## PART 2 — Hunt for residual / newly introduced issues

### CRITICAL

**None.** I could not find any load-bearing hole. The refutation (opt=6 via 8 DRAT proofs, tree=9 via Lean + DP, gap=3, s=3, Khrapchenko fail-safe gap≥2), the census (222 classes, 72 at gap≥2, 32.4%, three max-gap classes distinct by opt_XAG), the n=5 search (25,373/25,169/204/0), the base-dependence framing, and all hedges hold against the artifacts.

### IMPORTANT

**None must-fix.** Two items worth noting but not blocking:

**I1 (observation, not a defect) — the reversed-inequality claim is correct but subtle.** For parity *specifically*, `s = tree − opt = 3` (equality), so Krinkin's first inequality `s ≤ tree − opt` happens to hold; the chain breaks at the *second* step (`tree − opt ≤ 1`). The v2's critique is that the derivation is *generally* unsound (§2 yields `s ≥ tree − opt`, the opposite direction). I verified this is algebraically correct: since §2's min is over all decompositions and the trivial decomposition `f=1∧f` gives `tree(f) ≤ 1+opt(f) < 1+opt(a)+opt(b)` whenever `opt(a)+opt(b) > opt(f)`, the gate-g decomposition is generically *not* the minimizer, so `s > tree − opt` in general. The v2's framing is accurate; a referee might benefit from one extra clause noting that for parity the first inequality is equality (so the bound fails at Theorem 2 itself), but this is polish, not a defect.

### MINOR

**M1 — §5 line 201 "solver-decidable sample" could echo the old conflated phrasing.** The term is used correctly here (describing the sample's conditional nature: "functions whose opt timed out… are not written"), and the immediately following sentence clarifies it. But a referee scanning for the old "25,373 solver-decidable" language might double-take. *Optional fix:* rename to "generator-reachable, solver-decided sample" (past tense) to match the abstract's "25,169 gap-decided".

**M2 — XAG gap-1 distribution `{0:218, 1:4}` at n=4 is not independently verifiable from the archived CSVs.** `npn4_xag.csv` has `opt_xag` but no `tree_xag`/`gap_xag` column; the four gap-1 classes come from the `tree_via_sat` encoder (Appendix B gating). The claim is internally consistent and was not flagged in rounds 1–2, but a referee could ask for the per-class XAG gap table to be archived alongside the AIG one. *Fix (pre-submission):* write `npn4_xag_gap.csv` (rep, opt_xag, tree_xag, gap_xag) to `certs/` or `exp_xag_n4/`.

**M3 — ⊕₃ used in abstract (line 17) without explicit definition.** Standard notation for the target audience (cs.CC), but a one-clause "(parity of three variables)" on first use in the abstract would match §3's "the parity of three variables". The abstract already says "the parity of three variables is a counterexample: `opt(⊕₃) = 6`" — so ⊕₃ is contextually defined. *No fix needed; noting for completeness.*

**M4 — Provenance note (lines 350–353) is a LaTeX-comment placeholder** ("tom a definir com Luiz"). Fine for the internal Markdown draft; must be finalized (or removed) during LaTeX conversion. Not a v2-mathematics issue.

### What I deliberately checked and could not break

- **DRAT hashes (all 16):** recomputed `shasum -a 256` for every `.cnf` and `.drat` — **byte-exact match** with `verify_lowk.log`. The 8 "s VERIFIED" lines cover the full parity chain (k=1..5) and the full child chain (k=1..3).
- **Gap census:** `93+57+40+13+14+2+3 = 222`; `72/222 = 32.4%`; three gap-6 classes `{0x1668, 0x16e9, 0x6996}` all `opt=9, tree=15`; `opt_XAG = 6/5/3` (verified against `npn4_xag.csv`).
- **n=5 CSV:** 25,373 data rows, 25,373 distinct TTs, verdicts `24,875/294/204/0`, decided = 25,169.
- **MIG distribution:** `{0:2,1:2,2:5,3:18,4:42,5:117,6:35,7:1} = 222`; max opt = 7.
- **Cross-base maxima:** AIG 10 / XAG 7 / MIG 7; `opt(⊕₄)` = 9/3/6 per basis.
- **"190/222 classes" (§5 line 193):** verified — XAG strictly below AIG in exactly 190/222 classes; equal in 32; never above.
- **Khrapchenko:** `|E|=12, |A|=|B|=4 ⟹ 144/16 = 9` leaves ⟹ ≥ 8 gates ⟹ gap ≥ 2. Correct.
- **Cor 6 arithmetic:** `s = 1+4+4−6 = 3 ∉ {0,1}`; `|D_a∩D_b| = |{3,4,5}| = 3` in `c6`.
- **Krinkin quotes (PDF cross-check via pdftotext):** §2 decomposition identity, §3 Bellman with base case, Cor 6 with full premises — all faithful, no truncation that changes meaning. The `∈{0,1}` in Cor 6 is Krinkin's own statement (PDF p.5), not an editorial insertion.
- **Appendix A proof:** `gap=1 ⟹ non-tree` (bridged) ⟹ fan-out≥2 gate exists ⟹ `I_gate ≥ m` (m−1 baseline + 1 extra) ⟹ `2m ≥ n+m ⟹ m ≥ n`. Valid; strictly stronger than Krinkin's (holds for all gap≥1).
- **Lean trust claims:** `complete` by induction (kernel); `par3_not_in_D8` by `native_decide` (compiler); witnesses by `decide`/`rfl`. v2 reports each at the right level.

### Numeric consistency sweep (abstract ↔ §3 ↔ §4 ↔ §5 ↔ §6 ↔ data files)

No discrepancy found. Every number I could check ties out: gap census (222 total, 72 violating), three max-gap classes (opt/tree/gap = 9/15/6, opt_XAG = 6/5/3), n=5 (25,373/25,169/204/0), MIG buckets (sum 222), cross-base maxima (10/7/7), Khrapchenko (9 leaves ⟹ 8 gates), DRAT chain (k=1..5 + child k=1..3, 8 proofs, all hashes match), 494 = 294+200.

---

## ONE-LINE VERDICT

**v2 is ready for LaTeX conversion and (pending the author-response window on `krinkin/unit-gap#1`) submission — all 14 Round-2 findings are genuinely closed against the artifacts, no CRITICAL or IMPORTANT must-fix remains, and the only actionable items are two optional pre-submission polish steps (archive `npn4_xag_gap.csv` for M2; rename "solver-decidable" to "solver-decided" for M1).**
