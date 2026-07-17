# Adversarial Review — Round 3 (v2, final confirmation)

I read `paper1_unitgap_basedep_v2.md` end-to-end, re-checked it against `UnitGap.lean`, Krinkin arXiv:2603.08033v2 (PDF pages 1–8), `certs/` + `verify_lowk.log`, `search_n5_dedup.csv` / `verify_n5_recheck.log`, `npn4_gap.csv` / `npn4_xag.csv`, and the four round-2 verbatims. Concordance with prior rounds is not treated as evidence.

---

## 1) Did v2 close the Round-2 findings?

| Round-2 item | v2 text / artifact | Status |
|---|---|---|
| Shared block sign (`¬(x₁⊕x₂)` vs XOR) | §3 cites Lean `c6` node 5 = `¬n3 ∧ ¬n4 = ¬(x₁⊕x₂)`; Lean lines 337–344 match | **CLOSED** |
| Max-gap classes by `opt_XAG`, not Hamming | §4: `{0x1668,0x16e9,0x6996}` with `opt_XAG = 6,5,3`; Hamming gone. CSV: 6/5/3. NPN-invariant: yes (`opt` preserved under free NPN) | **CLOSED** (argument correct) |
| Thm 3: non-tree **from** `gap=1` before incidence | Appendix A opens with the bridge, then counts; false parenthetical removed | **CLOSED** (proof valid) |
| Krinkin quotes: §2 identity, §3 Bellman **with base case**, Cor 6 **with premises** | All three present; PDF matches substance (Bellman base `v₀(xᵢ)=v₀(1)=0`; Cor 6 has `C` optimal, `g` any gate, `D_a/D_b` child sub-DAGs) | **CLOSED** |
| “Incompatible **characterizations**”; overshoot as *consequence* of Thm 2 | §3 / abstract wording matches the requested separation | **CLOSED** (fair) |
| Cor 6 `s≤1` inequality direction | §3 flags reverse direction vs §2’s `tree ≤ 1+opt(a)+opt(b)` | **CLOSED** (correct) |
| 25,169 gap-decided vs 25,373 / 204 timeouts | CSV verdicts: `gap0=24875`, `gap1=294`, `inconclusive=204` → 25,169 / 25,373; abstract + §5 + §8 agree | **CLOSED** |
| Abstract XAG hedge + `n ≤ 4` | “holds for `n ≤ 4` (… separately gated … UNSAT side is not proof-certified)” | **CLOSED** (adequate) |
| Appendix B parity-5 false positive | Full bug (exact `opt+1` only) + fix (ascend from `opt`) | **CLOSED** |
| `verify_lowk.log` for all 8 proofs | Present: 5×`par3` + 3×`h_child`, each `s VERIFIED` + CNF/DRAT SHA-256; file sizes consistent; historical `check_claims_output.txt` matches `par3_k5` / `h_child_k3` hash prefixes | **CLOSED** (archive present & consistent) |

**Thm 3 proof re-audit.**  
`gap=1` ⇒ optimal `C` is not a tree (else `tree ≤ opt` ⇒ gap 0) ⇒ some non-output gate has fan-out ≥ 2.  
`2m = I_var + I_gate`; essential vars ⇒ `I_var ≥ n`; normalization (no unused gate, free from optimality) ⇒ ≥ `m−1` gate incidences, plus ≥1 extra from the multi-fanout gate ⇒ `I_gate ≥ m`; hence `m ≥ n`. Valid; stronger parenthetical (“any non-tree optimal single-output circuit”) is correctly labeled.

**NPN discriminator.** Distinct `opt_XAG ∈ {6,5,3}` forces three NPN classes because XAG size is NPN-invariant under free inversions. No Hamming appeal remains.

---

## 2) Residual hunt (new / unclosed)

### CRITICAL
**None.** I could not find a load-bearing inconsistency that rescues Krinkin’s Thm 2 / Cor 6, breaks the certified `gap(⊕₃)=3` package, or falsifies the census numbers against the data files.

### IMPORTANT
**None that block LaTeX conversion.** Two near-misses, both polish rather than holes:

1. **§3 / Appendix C — “each child” DRAT chain is one representative + NPN.**  
   Location: §3 (“Each child's `opt = 4` is certified by a DRAT chain”); `certs/` has only `h_child_k{1,2,3}` for `h=(x₁⊕x₂)∧¬x₃`.  
   The other output-child `¬(x₁⊕x₂)∧x₃` is NPN-equivalent (input/output polarities), so `opt=4` transfers — but the text does not say that. Structural `|D_a∩D_b|=3` does not need the arithmetic.  
   **Fix (one sentence):** “DRAT chain for a representative child; the other is NPN-equivalent, hence same `opt`.”

2. **Certification trail is archived, not re-executed in this review environment.**  
   `verify_lowk.log` + eight proof pairs are present and size-consistent; partial hash cross-check vs `check_claims_output.txt` matches. Independent `drat-trim` re-run / full re-hash of all eight was not completed in this session (tooling limits). That is a review limitation, not a manuscript defect — but before submission, one local re-run of the eight checks is still good hygiene.

### MINOR
1. **Appendix A — `I_var` wording.** “slots read a primary input (or the constant)” then “`I_var ≥ n`” from essential variables: the constant does not help the lower bound. Drop “or the constant” from the lower-bound sentence (keep it only in the partition definition).

2. **§3 opposite-direction sentence.** The content is right (`§2` yields `s ≥ tree−opt`, so Krinkin’s `s ≤ tree−opt` is reversed); the “i.e.” packaging is slightly tangled. Prefer: “§2 yields `tree ≤ 1+opt(a)+opt(b)`, i.e. `s ≥ tree−opt` — the reverse of the comparison the proof needs.”

3. **§3 tree-layer histogram** `24,64,30,80,32,0,16,0,2` is still not printed by the current `tree_gap_n3.py` artifact (only gap distribution is). Harmless if regenerated at LaTeX time or dropped.

4. **Quotes remain English renderings** of PDF displays (fine in markdown; pin exact displays in LaTeX).

5. **Table 3 “complete opt-6 bucket (which includes the parity decompositions)”** — already softened correctly; keep that wording.

### Numeric consistency re-check (abstract ↔ §4 ↔ §5 ↔ §6 ↔ files)
| Claim | Source | Match |
|---|---|---|
| AIG gap classes 93/57/40/13/14/2/3 = 222 | `tree_gap_n4_out.txt`, §4 | ✓ |
| 72/222 = 32.4% | arithmetic | ✓ |
| Max-gap `{0x1668,0x16e9,0x6996}`, opt 9 / tree 15 | `npn4_gap.csv` | ✓ |
| `opt_XAG` 6/5/3 for those three | `npn4_xag.csv` | ✓ |
| n=5: 24,875 / 294 / 204 / 0; 25,373 total; 25,169 decided | `search_n5_dedup.csv` (`cut` counts) | ✓ |
| 494/494 recheck | `verify_n5_recheck.log` | ✓ |
| Cross-base ⊕₄ 9/15, 3/3, 6/— | csv + stated MIG | ✓ |
| MIG bucket `{0:2,…,7:1}` | stated; prior rounds matched bases csv | ✓ (not re-derived here) |

No new arithmetic drift from the v2 edits.

### What I deliberately could not break
- `opt(⊕₃)=6` upper (Lean `c6` / simulation) + lower (DRAT chain k=1..5, log `s VERIFIED`).
- `tree(⊕₃)=9` (DP + Lean completeness + `native_decide` honesty).
- Khrapchenko fail-safe: cube edges 12 → `12²/(4·4)=9` leaves → ≥8 gates → `gap≥2` from the six-gate circuit alone.
- Cor 6 under written `|D_a∩D_b|`: cones of the two output children in `c6` intersect in `{n3,n4,n5}`, size 3; no rescue by redefining “shared.”
- §2 (`opt` in children) vs §3 (recursive `v`) are incompatible as characterizations of formula size; overshoot∈{0,1} is correctly treated as a Thm-2 consequence.
- XAG hedges and n=5 “sample, not proof” are not overstated in v2.

---

## ONE-LINE VERDICT

**v2 closes the Round-2 findings against the artifacts; no CRITICAL/IMPORTANT must-fix remains — ready for LaTeX conversion, and for submission after the author-response window on `krinkin/unit-gap#1` (optional one-line NPN note on the child DRAT + a local re-run of the eight `drat-trim` checks for hygiene).**
