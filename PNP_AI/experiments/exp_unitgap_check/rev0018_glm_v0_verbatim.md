I have now read the paper, technote, findings note, and verified all key claims against the artifacts. Here is my adversarial review.

---

# ADVERSARIAL REVIEW — `paper1_unitgap_basedep_v0.md`

## Summary of attacks tried

I attacked every load-bearing claim. The refutation **SURVIVES**. Below I rank findings by severity and show exactly what I tried and where it held vs. cracked.

---

## CRITICAL — None

No mathematical error rescues Theorem 2 or Corollary 6. The counterexample is real and certified.

---

## IMPORTANT findings

### I-1. The entire refutation rests on an unverifiable reading of Krinkin's verbal definition (the "type confusion" is a strawman risk)

**Location:** §3 (paper), first paragraph; the sentence *"The paper defines a formula verbally as fan-out-one ('a tree') and then displays…"*

**The attack:** If Krinkin's `tree(f) = min(1 + opt(a) + opt(b))` is a **deliberate definition** (not a typo), then Theorem 2 is *trivially true and vacuous* under that definition — because the decomposition `f = 1 ∧ f` gives `tree(f) ≤ 1 + opt(f)` for every `f`, so `gap ∈ {0,1}` is a 2-line consequence, not a theorem. Under this reading, the paper is not "refuting" anything — it is complaining that Krinkin's definition is non-standard, which is a much weaker claim.

**Why it fails (mostly):** The *diagnostic signature* in §3 is devastating corroboration: Krinkin's **own n=3 table** reportedly lists parity-3 with `gap = 1` at `opt = 6`, which is exactly what the `opt`-on-RHS recursion produces (`tree = 1 + opt(parity) + opt(1) = 7`, `gap = 1`). Under the standard definition his table should show `gap = 3`. So the type confusion is visible in his data, not just his proof.

**The real problem:** The paper **paraphrases** Krinkin's verbal definition rather than quoting it verbatim. A hostile referee can simply say "quote the source or withdraw." The diagnostic signature also depends on decoding Krinkin's table, which is asserted, not shown.

**Concrete fix:** Add a block-quoted, verbatim passage from arXiv:2603.08033 containing (a) the verbal definition of "formula" and (b) the displayed recursion, side by side. Do the same for Corollary 6's definition of `s`. Without these quotes the refutation is rhetorically vulnerable even though it is mathematically correct.

### I-2. Lean certification for `tree(⊕₃) ≥ 9` is OVERCLAIMED — it rests on `native_decide`, not kernel `decide`

**Location:** §6 verification table, row *"tree(⊕₃) = 9; witnesses | Lean 4 kernel (decide) for witnesses + structural minimality lemma; DP sweep via native_decide."* Same claim in technote §5.

**The problem:** I read `formal/UnitGap.lean`. The lower bound is `tree_lower`, which depends on:

```
theorem par3_not_in_D8 : par3 ∉ dpAt 8 8 ∧ cmpl par3 ∉ dpAt 8 8 := by native_decide
```

So the specific finite fact "no ≤ 8-gate AIG formula computes parity-3" is `native_decide`, i.e. **compiler-trusted, not kernel-trusted**. The verification table places the "structural minimality lemma" on the kernel-`(decide)` side, which is inaccurate if that lemma is `tree_lower`. The structural *framework* (`complete`, `step_mem`, `dpAt_mono`, `dpAt_top`) is kernel-checked by induction — but the application to parity-3 is not. Also, `#print axioms tree_lower` will show `Lean.ofReduceBool` (or `Lean.ofReduceNat`) in addition to `propext, Classical.choice, Quot.sound`; the paper's axiom audit lists only the standard three.

**Severity upgrade rationale:** This is the single load-bearing lower bound of the entire paper. If it is misreported, every downstream claim (`gap = 3`, "refuted") inherits the mislabeling.

**Concrete fix:** Reword the table to: *"Structural framework (`complete`, membership lemmas): kernel `decide`/induction. The finite lower-bound check `par3 ∉ dpAt[8]` and hence `tree_lower`: `native_decide` (compiler-trusted). Two independent Python DPs agree. Axiom audit of `tree_lower` includes `Lean.ofReduceBool`."* Then re-run `#print axioms` on each theorem and paste the actual output.

---

## IMPORTANT — overclaim / hedging

### I-3. "Novelty (ii): gap-by-basis census" is very likely known-classical, and the hedge is thin

**Location:** §7, bullet *"What is new: …(ii) the complete gap censuses (tree − opt per class)…we have not found the gap-by-basis analysis stated anywhere."*

**The attack:** Formula-size tables over B₂ (= XAG here, as the paper admits) and circuit-size tables over AIG and MIG are all published (Knuth TAOCP 7.1.2; Soeken et al. DATE 2016; Krinkin arXiv:2603.09379). The *difference* `tree − opt` per NPN class is a subtraction of two known columns, not a new measurement. A referee whose field is classical formula complexity will likely read "we have not found this stated anywhere" as "we did not look hard enough," because the gap is implicit in any table that publishes both `L(f)` and `C(f)`.

**Why the hedge is honest but insufficient:** The paper does say "correspondingly hedged" and defers cross-validation against Knuth. But the abstract still headlines the census as contribution (ii), and §7 presents it as a novelty item. The hedge belongs in the **abstract**, not only in §7.

**Concrete fix:** Either (a) demote the claim to "we present the first *explicitly tabulated* gap-by-basis comparison at n ≤ 4, a straightforward subtraction of classical catalogs" (conceding the likely prior art), or (b) actually cross-check against Knuth's B₂ column before claiming novelty at all. As written it is a vulnerability.

### I-4. Corrected Theorem 3 proof is asserted, not shown

**Location:** §3 (paper), last paragraph before the diagnostic signature; also technote §2.

**The problem:** The paper writes: *"counting input incidences instead gives `2m ≥ n + m`, i.e. `m ≥ n`, for every non-tree optimal circuit."* This is presented as a one-line proof replacement. I cannot reconstruct it: with `n` = #variables and `m` = #gates, the incidence count gives `2m = (slots to inputs) + (slots to earlier gates)`. The slots-to-earlier-gates term is `≥ m − 1` in any connected single-output circuit, so `2m ≥ I_in + m − 1`, i.e. `m ≥ I_in − 1`. To conclude `m ≥ n` one needs `I_in ≥ n + 1`, which is not justified by "counting input incidences" alone (essential variables only force `I_in ≥ n`).

**Why it is not fatal:** Theorem 3 *survives* in the paper's own framing; the corrected proof is a side contribution, not load-bearing for the refutation. But a referee can demand the proof and reject the "we supply a corrected proof" claim.

**Concrete fix:** Either show the full incidence argument (define `S`, define `m`, `n`, show the inequality chain), or downgrade to "Theorem 3 survives but its published proof has a gap when `g` is input-level; a corrected counting argument appears to give `m ≥ n`; full proof deferred to Appendix X." Do not claim a proof you do not show.

### I-5. XAG census lower bounds are UNSAT-without-DRAT — fine, but the abstract inherits the risk silently

**Location:** §6 table, row *"XAG census | UNSAT side without DRAT (declared)."*

**The problem:** The abstract claims `gap_XAG ∈ {0,1}` for all 222 classes of `n = 4` as the central "base dependence" finding. Every `opt_XAG` value in `npn4_xag.csv` ultimately rests on kissat UNSAT without DRAT. The encoder is gated (X1/X2 in `gate_xag.py`, G-T1/G-T2/G-T3 in `gate_xag_tree.py`) and the MIG replication cross-validates the *pipeline*, but neither certifies any individual XAG UNSAT. The abstract's confident "the unit-gap property *holds*" is therefore one kissat UNSAT regression away from being wrong on a single class — which would sink the base-dependence story.

**Concrete fix:** Tighten the abstract: "the unit-gap property *holds under uncross-checked SAT UNSAT* in XAG for `n ≤ 4`; the encoder is gated but lower bounds are not DRAT-certified." The §6 declaration is honest; the abstract is not.

---

## MINOR

### M-1. Corollary 6 refutation depends on the definition of `s`, which is not quoted

**Location:** §3, *"the sharing term is `s = 3` — structurally, and arithmetically `1 + 4 + 4 − 6 = 3`."*

The arithmetic is correct (verified: `opt(child) = 4` via DRAT `h_child_k3.drat`, drat-trim `VERIFIED`, 11 546 bytes). But if Krinkin's `s` is the *count of gates with fan-out ≥ 2* (which is `1` in the witness — only `g₃` has fan-out 2), then `s = 1 ∈ {0,1}` and the corollary survives. The paper's reading (`s = 1 + opt(a) + opt(b) − opt(f)`) is one specific definition. Quote Corollary 6's definition of `s` verbatim.

### M-2. Khrapchenko is not tight for parity-3 — paper's framing is correct but invites the question

**Location:** §3, *"L(⊕₃) ≥ … = 9 leaves ⟹ ≥ 8 gates."*

I verified the arithmetic independently (`|A|=4, |B|=4, |E|=12, 144/16 = 9.0`). I also verified the DP gives `tree(⊕₃) = 9` gates = 10 leaves, so Khrapchenko is **not tight** for n=3 (it is tight for n=2 and n=4, both powers of 2 — a known phenomenon). The paper uses Khrapchenko only as a fail-safe (`gap ≥ 2`), which is legitimate. But a referee may ask "why is the bound off by one?" — a footnote noting that Khrapchenko is tight for parity-`n` iff `n` is a power of 2 would preempt this.

### M-3. "Diagnostic signature" depends on decoding Krinkin's table

**Location:** §3, *"the two functions listed with gap = 1 at opt = 6 decode exactly to parity and its complement."*

Cannot verify without Krinkin's source table. The GLM re-derivation ("18 functions with opt = 6 at n = 3, sixteen have true formula cost 7 and exactly two have 9") is consistent with my own DP re-run on `tree_gap_n3_output.txt` (`{0:214, 1:40, 3:2}`, max gap 3 on `0x96`/`0x69`). But the *diagnostic claim about Krinkin's table* is asserted, not shown.

### M-4. "Optimal six-gate circuit shares a three-gate sub-DAG" — witness has `s = 3` structurally only under one decomposition

The witness `c6` in `UnitGap.lean` has gate `n₅` (the `¬(x₁⊕x₂)` node) with fan-out 2, used by both `n₆` and `n₇`. The "3-gate sub-DAG" is `{n₃, n₄, n₅}` (the XOR block). This is structurally correct. But the paper says "both children of the output gate contain the same three-gate sub-DAG" — more precisely, both children *reference* the same 3 gates by fan-out; the sub-DAG is not duplicated in the circuit (that's the whole point of sharing). Reword for precision.

---

## Internal consistency — all verified ✓

| Claim | Source | Check |
|---|---|---|
| `{0:93,1:57,2:40,3:13,4:14,5:2,6:3}` sums to 222 | `npn4_gap.csv` | ✓ sums to 222; 72 with gap ≥ 2 |
| `gap_XAG n=4 = {0:218, 1:4}`; n=3 all 0 | `tree_xag_n4.npy` × `npn4_xag.csv`; `gate_xag_tree.py` | ✓ verified by direct Python cross-check |
| n=5: 29 643 = 29 143 + 296 + 204; 0 separators | `search_n5_w00.csv` + `w01.csv` | ✓ combined `FNR>1` rows = 29 643; `grep SEPARATOR` = 0 |
| MIG `{0:2,1:2,2:5,3:18,4:42,5:117,6:35,7:1}` sums to 222 | `npn4_mig.csv` | ✓ sums to 222 |
| Cross-base: `opt(⊕₄)/tree(⊕₄)` = 9/15 (AIG), 3/3 (XAG), 6/— (MIG); max opt AIG=10, XAG=7, MIG=7 | `npn4_bases.csv` | ✓ all four cells match |
| `opt(⊕₃)=6`: DRAT 147 189 bytes, drat-trim `VERIFIED` | `certs/par3_k5.drat`, `check_claims_output.txt` | ✓ byte count and status confirmed |
| `opt(child)=4`: DRAT, drat-trim `VERIFIED` | `certs/h_child_k3.drat` (11 546 bytes) | ✓ |
| Khrapchenko parity-3: `144/16 = 9` leaves → ≥ 8 gates | brute-force `|A|=4,|B|=4,|E|=12` | ✓ independently re-computed |
| Khrapchenko parity-4: `1024/64 = 16` leaves → ≥ 15 gates | brute-force `|A|=8,|B|=8,|E|=32` | ✓ independently re-computed |
| 4 classes with `gap_XAG=1`: `{0x01e9, 0x0661, 0x1668, 0x167e}` all `opt=6, tree=7` | `tree_xag_n4.npy` × `npn4_xag.csv` | ✓ directly verified |
| `190/222` classes have `opt_XAG < opt_AIG` | same cross-check | ✓ |

---

## Specific hard shots that failed (and why)

1. **Could an 8-gate AIG formula for ⊕₃ exist (tree = 8, gap = 2)?** Tried: the DP is the only thing standing between 8 and 9, and the DP could be wrong. Failed because: (a) `tree_gap_n3.py` (v2 Bellman) and the layer-BFS v1 agree; (b) `tree_gap_n4_v2.py` re-implements the same Bellman with explicit polarity handling and `v2 == v1` on all 65 536 cells; (c) I derived 9 gates by hand two independent ways (both XOR-decomposition shapes). No 8-gate formula exists.

2. **Could `opt(⊕₃) < 6`?** Tried: encoding soundness (one-hot, used-gate, dedup, topological order). All are necessary for minimality, none over-constrain. The DRAT proof is drat-trim `VERIFIED` on a 147 KB file. The 6-gate witness is simulation-verified (`tt6 == 0x96 == PAR3`). Failed.

3. **Could the type-confusion be a legitimate alternative definition under which Thm 2 is true-as-stated?** This is the strongest attack. It *could be* — but only if Krinkin's verbal definition matches his displayed recursion, which contradicts the paper's claim that he says "fan-out one." The diagnostic signature (Krinkin's own table reportedly showing `gap=1` for parity at `opt=6`) makes the type-confusion reading far more likely than the deliberate-definition reading. Attack fails *contingent on the verbatim quote being accurate* — which I could not verify without Krinkin's source.

4. **Could the Khrapchenko arithmetic be wrong (rescuing the fail-safe)?** Tried: recomputed `|E|` by brute enumeration of Hamming-1 edges across the parity cut. Got `12` for n=3 and `32` for n=4, confirming `144/16 = 9` and `1024/64 = 16`. Khrapchenko bounds leaves of a formula (not a circuit) — confirmed. Leaves → gates via `L − 1` for binary trees — confirmed. `gap ≥ 8 − 6 = 2`. Attack fails.

5. **Could the XAG formula encoder be unsound (making `gap_XAG ∈ {0,1}` unreliable)?** Tried: the formula flag adds exactly-one-consumer + drops dedup. I checked the consumer-collection logic (`users = [o[5] for j … if o[1]==n+i or o[3]==n+i]`) — it correctly enumerates all options that reference `n+i`. The at-most-one is over selection variables, redundant with each gate's one-hot but correct. Gate `G-T3` cross-checks `tree_via_sat` against the independent DP on all 222 classes including the 4 gap-1 classes. Attack fails.

6. **Could the n=5 search have false negatives hiding real separators?** Tried: a separator with low `opt` and `tree = opt+2` would be caught by the ascending search (first SAT at `opt+2`, gap 2). The 204 timeouts are honestly declared as inconclusive. The selection bias (random XAG circuits, `k ∈ [4,8]`, opt-low) *does* miss high-opt separators — but the paper says so. Attack fails on the headline claim (zero separators among 29 439 decided) and succeeds only on the open frontier (which the paper already concedes).

---

## ONE-LINE VERDICT

**The refutation SURVIVES.** The counterexample `gap(⊕₃) = 3` is mathematically airtight (DRAT + two independent DPs + Khrapchenko fail-safe + Lean witnesses), the census numbers all reconcile, and every hard shot I took at the lower bound, the upper bound, the fail-safe, and the encoder soundness failed. The two real problems are (I-1) the paper's failure to quote Krinkin's definition verbatim, which leaves the "type confusion" reading legally vulnerable, and (I-2) the overclaim that `tree ≥ 9` is kernel-checked when `par3_not_in_D8` is `native_decide` — fix both before submission.
