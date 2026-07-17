# Adversarial Review — `paper1_unitgap_basedep_v0.md`

I tried to rescue Krinkin. I failed. Below are the hardest shots, in severity order, including the attacks that did **not** land.

---

## CRITICAL

### C1 — None found that rescues Theorem 2 or Corollary 6

I could not find a mathematical error that restores `gap ∈ {0,1}` under the paper’s (and the standard) definition of formula. The load-bearing attacks and why they fail:

---

## Attacks on the refutation (Task 1) — all failed

### A1. `opt(⊕₃) = 6` / encoding soundness — FAILS TO RESCUE

**Attack.** The AIG encoder forbids duplicate option-tuples and requires every non-output gate to be used. That makes the CNF incomplete for *some* size-`k` circuits. Could a 5-gate circuit exist that the encoding rejects, so the DRAT “UNSAT@5” is meaningless?

**Why it fails.** Both restrictions are sound for *minimality*, and the ascending search inherits that:

- If a size-5 circuit has a duplicate gate or an unused gate, deleting it yields a correct circuit of size ≤ 4.
- So “∃ circuit of size ≤ 5” ⇒ “∃ duplicate-free, fully-used circuit of size ≤ 5.”
- UNSAT of the restricted encoding at `k = 1..5` therefore implies `opt ≥ 6`.

Upper bound is an explicit 6-gate DAG, simulation-checked in Python (`check_unitgap_claims.py`) and kernel-checked in Lean (`c6`, `circuit_upper`). DRAT for `par3_k5` is on disk (`147189` bytes) with logged `s VERIFIED`. Cost model (2-input AND, free edge/output negations, size = #ANDs) matches the stated AIG model.

Even **without** the DRAT lower bound: Lean + the 6-gate witness already give `tree ≥ 9` and `opt ≤ 6`, hence  
`gap = tree − opt ≥ 9 − opt ≥ 9 − 6 = 3`.  
So Thm 2 dies even if the DRAT chain were discarded.

### A2. `tree(⊕₃) = 9` / possible 8-gate formula — FAILS TO RESCUE

**Attack.** Khrapchenko only forces ≥ 8 gates. Maybe an 8-gate formula exists and both DPs are wrong the same way.

**Why it fails for the refutation (though not for the exact value 9).**

- Tree recursion in `tree_gap_n3.py` is the correct Bellman equation `tree(f) = min 1+tree(a)+tree(b)` over AND-with-polarities; polarities are absorbed by complement-closure (independently re-done with *explicit* 4-polarity enumeration in `tree_gap_n4_v2.py` for n=4; n=3 output matches the claimed layer profile).
- Lean proves *completeness* of the DP inductively (kernel); `par3 ∉ D₈` is only `native_decide`. That is a trust gap for the exact `9`, not for refutation.
- Independent Python fixed-point also gives `tree(0x96)=tree(0x69)=9`, layer counts `24,64,30,80,32,0,16,0,2`.
- **Fail-safe:** Khrapchenko `L ≥ 9` ⇒ `gates ≥ 8`, plus explicit `opt ≤ 6` ⇒ `gap ≥ 2 > 1`, with **no** DP and **no** DRAT.

An 8-gate formula, if it existed, would still refute Thm 2 (`gap ≥ 2`). Only `tree ≤ 7` would save Thm 2; that is incompatible with Khrapchenko.

### A3. Type-confusion / strawman reading of Krinkin — FAILS TO RESCUE

**Attack.** Maybe the displayed identity  
`tree(f) = min (1 + opt(a) + opt(b))`  
is an intentional alternative definition, so Thm 2 is “true as stated” under that measure.

**Why it fails as a rescue.**

1. Under that identity, `f = 1 ∧ f` (constant-1 leaf, free in AIG) gives `tree(f) ≤ 1 + opt(f)` for every `f`. Thm 2 becomes a one-line tautology. A published “theorem” with structural corollaries about sharing is then either vacuous or mislabeled.
2. The paper’s verbal definition is fan-out one (“a tree”). Putting `opt` in the children **silently allows internal DAG sharing inside the children**, which a tree forbids. That is a genuine type error relative to the verbal definition, not a creative redefinition.
3. Diagnostic in Krinkin Table 1: the only `gap=1` at `opt=6` entries decode to parity / complement — exactly where the wrong recursion reports a spurious unit gap while the true formula gap is 3. The bug is visible in his data.

If he meant the hybrid measure, the scientific claim “formula size − circuit size ∈ {0,1}” is still false under every standard meaning of those words. Either reading, Thm 2 as a statement about formulas is false.

### A4. Khrapchenko arithmetic / leaves→gates — FAILS TO RESCUE

**Attack.** Wrong `|E|`, or bound is on leaves not gates, or constants break the conversion.

**Check.**

- 3-cube: every edge flips parity ⇒ `|E| = 3 · 2^{2} = 12` (undirected).
- `|A| = |B| = 4` ⇒ `L ≥ 12²/(4·4) = 144/16 = 9` leaves. Arithmetic correct.
- Binary formula: `#gates = #leaves − 1`, so `L ≥ 9 ⇒ gates ≥ 8`.
- Constant leaves: Khrapchenko counts *variable* occurrences covering sensitive edges; constants do not cover `E`. If some leaves are constants, `#var-leaves ≤ #leaves = gates+1`, so `gates ≥ L_var − 1` still holds.
- Free edge NOTs put the model inside the De Morgan basis Khrapchenko applies to.

Same for n=4 parity: `|E|=32`, `|A|=|B|=8`, `L ≥ 1024/64 = 16` ⇒ `gates ≥ 15`, matching `tree(⊕₄)=15` equality claim.

### A5. Corrected Theorem 3 (`2m ≥ n + m ⇒ m ≥ n`) — essentially holds

**Attack.** Incidence count wrong.

**Reconstruction.** Single-output circuit, all gates used, `n` essential inputs, non-tree:

- `2m = E_i + E_g` (every gate has two inputs).
- Gate-consumer graph is a single-sink DAG; tree case has `E_g = m−1`; any extra fan-out ≥ 2 forces `E_g ≥ m`.
- Essentiality ⇒ `E_i ≥ n`.
- Hence `2m = E_i + E_g ≥ n + m` ⇒ `m ≥ n`.

This is fine as a structural lemma. Minor caveats (not fatal): “optimal” is unnecessary; need “all gates used” and “depends on all `n` inputs.” The paper’s claim that the published `|S| ≥ k−1` fails for input-level gates is plausible and not load-bearing for the refutation.

### A6. Corollary 6 (`s ∈ {0,1}`) — FAILS TO RESCUE

Explicit 6-gate optimum shares the 3-gate `x₁⊕x₂` block between both children of the output (`s = 3` structurally; `1+4+4−6 = 3` arithmetically). Child `opt = 4` has its own UNSAT@3 DRAT. Unless Krinkin defines `s` in some non-standard way that ignores this sharing, Corollary 6 is dead. (I did not have Krinkin’s PDF; this is the one place an exotic definition of `s` could still wriggle — see I2.)

---

## IMPORTANT

### I1. Verification table overclaims n=5 simulation checks  
**Location:** §6 table, row “XAG search n=5”; also Appendix B tone.

**Problem.** The table says “each result simulation-verified.” The actual collector (`search_n5.py`) calls:

- `opt_via_sat(..., verify=False)`
- `solve_k(..., formula=True)` without `return_circuit=True`

So during the 29 643-run harvest, SAT models are **not** decoded or simulation-checked. UNSAT sides are kissat-without-DRAT (declared — fine). The formula encoder was gated on n≤4 (good), but that does not simulation-verify each n=5 row.

**Fix.** Change the cell to:  
“Formula encoder gated on all 222 n=4 classes (incl. 4 with gap=1); n=5 SAT models **not** batch-verified (verify=False); sample, not exhaustive.”  
Optionally re-run a post-pass with `verify=True` on the 296 gap-1 rows and a sample of gap-0.

### I2. Corollary 6 depends on Krinkin’s exact definition of `s` (not inlined)  
**Location:** §3, Corollary 6 paragraph.

**Problem.** The refutation of Cor. 6 uses `s = 1 + opt(a) + opt(b) − opt(f) = 3` and the structural “shared 3-gate sub-DAG.” Without a quoted definition from arXiv:2603.08033, a referee can claim definitional mismatch. Thm 2 does **not** have this vulnerability.

**Fix.** Quote Krinkin’s definition of `s` verbatim (one sentence + equation), then show both the arithmetic and the fan-out-≥2 witness against it.

### I3. Lean package does not certify `opt ≥ 6` (and the paper slightly blurs this)  
**Location:** Abstract; §3 “Verification chain”; §6 Lean paragraph.

**Problem.** `unit_gap_refuted` is:

```text
(∃ 6-gate circuit for par3) ∧ (∀ formulas φ computing par3, gates φ ≥ 9)
```

That yields `gap ≥ 3` because `opt ≤ 6` and `tree ≥ 9` (see A1), **without** a circuit lower bound. The paper’s wording (“counterexample formalized in Lean”) is acceptable for Thm 2, but a reader may think Lean proves `opt = 6`. The exact equality `opt = 6` is DRAT, not Lean. `tree = 9` uses one `native_decide`.

**Fix.** One explicit sentence:  
“Lean proves `opt ≤ 6` and `tree ≥ 9` (hence `gap ≥ 3`); the matching lower bound `opt ≥ 6` is the DRAT certificate, not the kernel.”

### I4. Novelty claim (ii) is soft and possibly overstated  
**Location:** §7, “What is new” (ii).

**Problem.** That formula size can far exceed circuit size over `{∧,∨,¬}` is classical (Khrapchenko, Andreev, random functions, etc.). That the gap collapses once XOR is free is obvious on parity and close to folklore about basis-dependent complexity / boolean chains (Knuth TAOCP 7.1.2 is already cited for sizes). “We have not found the gap-by-base analysis stated anywhere” is an absence claim; absence claims need a search protocol or they read as hope.

The hedge (“correspondingly hedged,” “ongoing”) is present but sits next to a bold abstract claim of base-dependence as a main contribution.

**Fix.** Narrow (ii) to what is actually computed and new-as-data:  
“exhaustive **gap** censuses (tree−opt per NPN class) in AIG and XAG at n≤4, plus a directed n=5 XAG sample.”  
Drop or further weaken “we have not found this stated anywhere”; cite Spira, Neciporuk, and basis-dependence surveys as related.

### I5. n=5 sampling bias is described, but one sentence still invites over-reading  
**Location:** Abstract; §5 last paragraph of n=5 block; §8 Q1.

**Problem.** Body and findings note are careful (“directed sample, not a proof,” “subjective probability of a *low-opt* separator”). Abstract is mostly careful. Residual risk:

- Generation is random XAG of size 4–8 with sharing/XOR bias ⇒ **strongly biased to low `opt`**. High-`opt` separators are invisible by construction (and `opt` timeouts are `continue`’d, not even counted).
- Samples are **functions**, not NPN classes; near-duplicates under NPN may inflate the 29 643.
- 204 inconclusives are open tail, not evidence for gap∈{0,1}.

None of this is hidden, but the phrase “extending the n≤4 observation to n=5 empirically” can be cited as if n=5 were settled.

**Fix.** In abstract and §5 closing sentence, force the qualifier every time:  
“no **low-opt** separator in a sharing-biased sample of 29 643 essential functions; high-opt regime untouched.”  
Report unique NPN-class count if available.

### I6. XAG UNSAT side without DRAT is declared but load-bearing for the “unit gap holds in XAG” slogan  
**Location:** §5 XAG n≤4; §6.

**Problem.** The positive claim “unit-gap property holds in XAG for n≤4” rests on many UNSAT leaves without DRAT. Encoder is gated (n=3 exhaustive both directions; n=4 tree SAT matches DP including all gap=1 classes) — that is real validation, but weaker than the AIG refutation chain. A single encoder bug that *over-constrains* formulas could hide separators (false gap 0).

**Mitigating evidence already in the repo:** G-T3 matches independent DP on all 222 classes and **detects** the 4 gap-1 classes, so systematic over-constraint of formulas is unlikely at n=4. Still: the slogan “holds” should stay “holds in the gated encoder / DP, UNSAT uncertified.”

**Fix.** Prefer “holds under our gated exact-synthesis pipeline (UNSAT without DRAT)” over bare “holds.”

---

## MINOR

### M1. Internal number consistency — all checked sums OK  
**Location:** §§3–5 tables.

| Claim | Check |
|---|---|
| AIG gaps `93+57+40+13+14+2+3` | = 222; `gap≥2` = 72; 72/222 ≈ 32.4% |
| XAG n=4 `{0:218,1:4}` | = 222 |
| MIG `{0:2,…,7:1}` | = 222 |
| n=5 `29143+296+204` | = 29643; CSV line counts `14698+14945=29643` (headers excluded) |
| Cross-base parity-4 | `npn4_bases.csv`: `0x6996 → 9/15, 3/3, mig 6`; max opt AIG 10, XAG 7, MIG 7 — matches table |
| Extremal gap-6 triple | `0x1668, 0x16e9, 0x6996` all `opt_aig=9, tree_aig=15` in CSV |

No internal arithmetic contradiction found.

### M2. `search_n5.py` module docstring is stale  
**Location:** artifacts, not the paper body.

Docstring still describes the pre-fix “test `opt+1` only” protocol; body correctly does ascending search from `opt`. Paper §5 describes the fixed protocol.  
**Fix.** Rewrite the docstring so artifact review cannot invent a methodology contradiction.

### M3. Theorem 3 write-up slightly over-claims scope  
**Location:** §3.

Needs hypotheses “single-output, every gate used, n essential inputs,” not merely “non-tree optimal.”  
**Fix.** Add those hypotheses in one clause.

### M4. “Four model families sustained the package” is not a certificate  
**Location:** Abstract/§3/provenance.

Social consensus among LLMs is not evidence. The paper mostly does not lean on it for math, but listing it under “Verification chain” invites mockery.  
**Fix.** Move to provenance footnote; keep DRAT/Lean/DP as the verification chain.

### M5. Khrapchenko fail-safe wording is easy to misread  
**Location:** §3 bullet “Analytic fail-safe.”

Correct content (as intended): `tree ≥ 8` (Khrapchenko) and `opt ≤ 6` (witness) ⇒ `gap ≥ 2`, independent of tree-DP and of DRAT. A hostile reader may think you claimed independence from the 6-gate upper bound too.  
**Fix.** Write explicitly: “independent of the tree DP and of the UNSAT lower bound on `opt`; uses only Khrapchenko + the explicit 6-gate circuit.”

### M6. Abstract “the unit-gap property *holds*” (XAG) vs open n≥5  
**Location:** Abstract.

Italic *holds* is immediately qualified by the n=5 sample sentence — acceptable. Prefer “*holds for all n≤4 (exhaustive)*.”

---

## Hardest shots that did not produce a hole

| Shot | Outcome |
|---|---|
| Dedup/used-gate ⇒ incomplete CNF ⇒ false UNSAT@5 | Sound for ascending opt; also Lean gives gap≥3 without DRAT |
| Tree DP misses same-child or polarity cases | `a==b` allowed; complement-closure / explicit 4-polarity v2; Lean completeness |
| Khrapchenko leaves≠gates or constants | `gates = L−1`; constants only strengthen the ≤ direction for the lower bound |
| Krinkin “meant” the displayed identity | Makes Thm 2 vacuous; contradicts verbal “tree”; table diagnostic |
| `gap ≥ 2` fail-safe depends on opt lower bound | No: needs only `opt ≤ 6` (upper) + `tree ≥ 8` |
| n=5 sample “proves” unit gap in XAG | Paper does not claim that; residual wording tightened in I5 |
| Encoder forbids `a=a` inputs | Irrelevant for minimal AIGs |
| Lean `native_decide` wrong ⇒ tree=8 possible | Still gap≥2 by Khrapchenko; exact 9 has two independent DPs |

---

## ONE-LINE VERDICT

**The refutation SURVIVES:** under the standard (and Krinkin’s verbal) definition of formula, `gap(⊕₃) ≥ 3` (analytically `≥ 2`) and `s = 3`, so Theorem 2 and Corollary 6 are false; remaining issues are certification hygiene, novelty hedging, and n=5 wording — not a mathematical hole.
