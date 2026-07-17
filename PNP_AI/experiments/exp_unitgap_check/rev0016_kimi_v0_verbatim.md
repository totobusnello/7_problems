(node:61109) ExperimentalWarning: SQLite is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
**Adversarial Referee Report — "The Unit Gap Is Base-Dependent"**

I read the draft, the supporting technote, the n=5 findings note, the Lean source, the SAT encoders, the DP scripts, and the CSV artifacts. I could not read Krinkin's PDF directly because this session is read-only and the file is binary, so my assessment of the "type confusion" claim relies on the draft's own quotation of his recursion.

---

## CRITICAL

**C1. The gap-6 extremal classes are *not* "parity-4 and its two NPN relatives."**
- **Location:** Abstract ("maximum gap 6 attained exactly by parity-4 and its two NPN relatives"); §4 ("{0x1668, 0x16e9, 0x6996} — parity-4 and its NPN relatives").
- **Problem:** 0x1668 has truth-table weight 6 (bits 3,5,6,9,10,12 set). Parity-4 (0x6996) has weight 8. NPN equivalence preserves Hamming weight up to output complement, so 0x1668 cannot be NPN-equivalent to parity-4. The CSV `npn4_bases.csv` confirms they are not even in the same equivalence class under XAG: their `opt_xag / tree_xag` are (6,7), (5,5), and (3,3) respectively — measures that *are* NPN-invariant. The three classes happen to share the same AIG gap of 6, but they are three *distinct* NPN classes.
- **Impact:** The "structural extremum" narrative — that AIG gaps are "precisely the cost of simulating linear (parity) structure" — is overstated. Parity is *an* extremum, not the unique source of the maximum gap.
- **Fix:** Replace "parity-4 and its two NPN relatives" with "three distinct NPN classes attaining the maximum gap 6, including parity-4 (0x6996)". Revise the base-dependence prose to say parity is a witness, not the exclusive cause.

---

## IMPORTANT

**I1. The n=5 XAG search is *not* "each result simulation-verified."**
- **Location:** §6 verification table ("XAG search n=5 … each result simulation-verified").
- **Problem:** `search_n5.py` calls `opt_via_sat(..., verify=False)` and `solve_k(..., formula=True)` with default `return_circuit=False`. The SAT models are never decoded and checked against the truth tables. Only the *encoder* was gated (G-T1/G-T2/G-T3); the ~29.6k individual n=5 results were not simulation-verified.
- **Fix:** Change the table entry to "encoder validated on all 222 n=4 classes; individual n=5 SAT results not simulation-verified" — or add and run a post-hoc verifier and update the CSVs.

**I2. MIG replication is "bucket by bucket," not "class by class."**
- **Location:** Abstract ("matching Soeken et al.'s published table class by class"); §5 ("matched the published distribution exactly, bucket by bucket" in the technote).
- **Problem:** The paper claims a class-by-class match, but the only evidence is the size distribution `{0:2, 1:2, 2:5, 3:18, 4:42, 5:117, 6:35, 7:1}` (which I verified sums to 222). That is a distribution match, not a per-class correspondence.
- **Fix:** Say "matched the published size distribution bucket by bucket" unless you actually compared `opt_mig` for each of the 222 representatives against Soeken's table.

**I3. The corrected proof of Theorem 3 is a sketch, not a proof.**
- **Location:** §3 ("counting input incidences instead gives 2m ≥ n + m, i.e., m ≥ n").
- **Problem:** A hostile reader cannot verify the incidence count without the definitions of `S`, `m`, and the gate-level structure from Krinkin's paper. The algebra `2m ≥ n + m ⇒ m ≥ n` is trivial, but the premise is asserted, not derived.
- **Fix:** Include the full corrected proof in an appendix, defining every counted object and showing why the published `|S| ≥ k−1` fails at the input level.

---

## MINOR

**M1. XAG parity-4 values are representative-dependent.**
- **Location:** §5 cross-base table (`opt(⊕₄)/tree(⊕₄) = 3/3` in XAG).
- **Problem:** The table silently uses 0x6996. Other AIG gap-6 "relatives" (which are actually distinct classes) have XAG values 5/5 and 6/7. A reader may think all NPN equivalents of parity-4 have `opt_XAG = 3`.
- **Fix:** Add a footnote: "values shown for representative 0x6996; distinct NPN classes have different XAG complexities."

**M2. "Diagnostic signature" about Krinkin's n=3 table cannot be checked from the supplied artifacts.**
- **Location:** §3.
- **Problem:** The claim that Krinkin's own table lists parity and its complement as the two `gap=1` cases at `opt=6` is plausible but unverifiable here because I cannot read the source PDF. It is not a mathematical error, only an un-audited rhetorical point.

**M3. The n=5 search declares a "SEPARATOR" if no SAT is found from `opt` through `opt+5`.**
- **Location:** `search_n5.py`, lines 107–121.
- **Problem:** This is logically correct (`tree ≥ opt+6 ⇒ gap ≥ 6`), but the code labels it `gap=6`, which is only a lower bound. Since the reported count of separators is zero, this does not affect the published numbers, but it is a minor imprecision.

---

## Attacks I tried and why they failed

- **`opt(⊕₃) = 6` unsound?** Failed. The AIG encoder is a standard exact-synthesis CNF with ordered gates, free edge/output negations, and a symmetry-breaking "no duplicate gates" clause. The duplicate-gate break is sound for determining the minimum: any minimum circuit is duplicate-free, and for `k=5 < opt` it cannot remove a genuine solution. The UNSAT is DRAT-certified.
- **8-gate formula for parity3 possible?** Failed. The n=3 Bellman DP and the Lean `lvls` DP both enforce `tree` on both sides of the recursion and include all AND polarities via complement closure. Khrapchenko allows 8 gates, but the DPs close at 9, and the Lean proof kernel-checks that ⊕₃ is not in `D₈`.
- **Type confusion a strawman?** Failed. Krinkin's displayed recursion uses `opt(a)+opt(b)` inside a recursion for `tree(f)`. Under his own verbal definition of a formula (fan-out one), the children must be trees, not optimally-shared DAGs. With `opt` on the right, the trivial decomposition `f = 1 ∧ f` gives `tree(f) ≤ 1 + opt(f)` for every `f`, making the theorem either trivial or false.
- **Khrapchenko arithmetic wrong?** Failed. For ⊕₃: `|A|=|B|=4`, `|E|=12`, `L ≥ 144/16 = 9` leaves, hence `≥ 8` internal gates, so `gap ≥ 2` independently of the computations. The bound is on formula leaves, and leaves − 1 = gates for binary trees.
- **Theorem 3 algebra wrong?** Failed. `2m ≥ n + m ⇒ m ≥ n` is correct. The only gap is the unproven incidence premise (I3 above).

---

## Internal-consistency check

I verified the CSVs with `Grep` (files are CRLF, so I anchored with `\r?$`):

| Claim | Verified |
|---|---|
| AIG gap distribution `{0:93, 1:57, 2:40, 3:13, 4:14, 5:2, 6:3}` | **Yes**, sums to 222; 72 classes have gap ≥ 2. |
| XAG n=4 gap `{0:218, 1:4}` | **Yes**, sums to 222. |
| n=5 counts 29,143 + 296 + 204 = 29,643 | **Yes** (w00: 14,449+148+101 = 14,698; w01: 14,694+148+103 = 14,945; total 29,643). Zero separators. |
| MIG distribution `{0:2,1:2,2:5,3:18,4:42,5:117,6:35,7:1}` | **Yes**, sums to 222. |
| Cross-base parity4 values | **Partially**: AIG 9/15 is correct for all three listed reps; XAG 3/3 is only for 0x6996, not for the other two. |

---

## ONE-LINE VERDICT

**The refutation of Krinkin's Theorem 2 survives** (parity-3 is a certified counterexample with gap 3), **but the paper has a real hole in §4: the three gap-6 AIG classes are not NPN-relatives of parity-4, so the "parity-as-extremum" narrative is mathematically wrong and must be rewritten.**
