   “The AIG gaps coincide with the cost of building parity” sounds like a mechanism for all 72 violating classes, which §4 correctly declines to establish. Use “The large parity AIG gaps…” or “The parity example suggests…”.

5. **The Krinkin blocks are faithful but normalized, not letter-for-letter quotations.**

   Locations: [§2](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:75), [§3](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:109).

   I found no meaning-changing misquotation: the §2 decomposition is equivalent to the PDF’s polarity notation; the Bellman base case is included; and Corollary 6 includes `C` optimal, `g` any gate, and the child sub-DAG premises. For publication hygiene, either reproduce the displays literally or label the blocks “notation-normalized quotations.”

6. **Checker provenance could be stronger.**

   [verify_lowk.log](/Users/lab/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/certs/verify_lowk.log:1) has all eight `s VERIFIED` results and hashes, but not the exact `drat-trim` commit, command lines, or exit codes requested in Round 2. Add those if easily recoverable. This is reproducibility polish, not a mathematical defect.

## Confirmed closures

- The shared Lean block is correctly `¬(x₁⊕x₂)`: node 5 in [UnitGap.lean](/Users/lab/Projetos/7_problems/PNP_AI/formal/UnitGap.lean:339). Its three gates are exactly the intersection of the output-child cones.
- The maximum-gap classes are exactly `0x1668`, `0x16e9`, `0x6996`, each `opt_AIG=9`, `tree_AIG=15`; their `opt_XAG` values are 6/5/3. The NPN-invariance argument is valid.
- Appendix A now correctly derives non-tree structure from `gap=1` before counting incidences. The proof `2m=I_var+I_gate≥n+m` is complete.
- Krinkin’s §2 identity, §3 Bellman operator and base case, and Corollary 6 premises agree substantively with the PDF.
- The “incompatible characterizations” framing and classification of the overshoot claim as a consequence of Theorem 2 are fair.
- Krinkin’s Corollary 6 proof indeed uses the inequality in the wrong direction.
- `search_n5_dedup.csv` contains 25,373 distinct rows and 25,373 distinct truth tables; all 25,373 pass the five-essential-variable test. Counts are exactly 24,875 gap-0, 294 gap-1, 204 inconclusive, zero separators: 25,169 gap-decided.
- The abstract’s `n≤4` and uncertified-XAG-UNSAT hedges are adequate.
- Appendix B adequately explains the parity-5 false positive and correction.
- All 16 CNF/DRAT files are present. Every recomputed SHA-256 matches `verify_lowk.log` for all eight proof pairs. I could not independently replay them because `drat-trim` is not installed in this environment.
- Numeric reconciliation succeeded: AIG gaps `93/57/40/13/14/2/3`; XAG gaps `218/4`; maxima AIG/XAG/MIG `10/7/7`; `opt_XAG<opt_AIG` in 190/222 classes; MIG buckets `2/2/5/18/42/117/35/1`; parity-4 rows `9/15`, `3/3`, `6/—`; and the 494/494 replay log is present.

**VERDICT: v2 has no remaining mathematical hole, but is not yet ready for LaTeX conversion/submission until the four IMPORTANT wording/artifact inconsistencies above are fixed; after those small fixes, it is ready pending the author-response window.**
tokens used
130.058
No critical mathematical hole remains. The parity counterexample, Corollary 6 refutation, Theorem 3 repair, and principal census numbers survive. However, I found four important precision/reproducibility issues that should be fixed before conversion/submission.

## CRITICAL

None.

## IMPORTANT

1. **The `n=5` correction is not propagated throughout the paper.**

   Locations: [paper v2, Introduction](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:60), [§5](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:200).

   The Introduction says the property “holds … over a large directed search at `n=5`,” and §5 calls all 25,373 functions a “solver-decidable sample.” But 204 formula searches timed out; only 25,169 are gap-decided.

   Concrete fix:

   > The property holds exhaustively for `n≤4`; at `n=5`, no separator was found among 25,169 gap-decided functions in a directed sample, with 204 cases unresolved.

   In §5, replace “solver-decidable sample” with “sample conditional on solver-decidable `opt`; 25,169 cases were also gap-decided.”

2. **The Khrapchenko independence claim remains literally false in the abstract and Introduction.**

   Locations: [Abstract](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:20), [Introduction](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:49).

   Khrapchenko alone proves `tree≥8`, not `gap≥2`. The latter additionally requires the explicit six-gate circuit, giving `opt≤6`. Thus `gap≥2` does not survive if “every computation above” includes verification of that circuit. §3 already states the dependency correctly.

   Concrete fix:

   > Together with the explicit six-gate circuit, Khrapchenko forces `gap≥2`, independently of the SAT lower-bound chain and tree-DP computation.

3. **The child-optimum certification wording claims two DRAT chains, but the archive contains one child chain.**

   Locations: [§3](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:144), [§6](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:247).

   The eight archived proofs are five for parity and three for a single target `h_child`; there are not three separate proofs for each of two children. This is sufficient because the second child is NPN-equivalent to the first, but v2 does not say that.

   Concrete fix:

   > One child has a DRAT-certified `k=1..3` lower-bound chain and an explicit four-gate realization; the other child is NPN-equivalent, so its optimum is also 4.

   Change the §6 row accordingly.

4. **The released `n=5` search script still documents the obsolete, unsound algorithm.**

   Location: [search_n5.py](/Users/lab/Projetos/7_problems/PNP_AI/experiments/exp_xag_n4/search_n5.py:1).

   Its top-level docstring still says it tests only `opt+1` and declares UNSAT a separator—the parity-5 false-positive procedure. The implementation below is fixed and searches upward from `opt`, and Appendix B explains the correction, but the source’s primary documentation contradicts both.

   Concrete fix: rewrite the docstring to describe ascending formula search from `opt`, including timeout and search-cap outcomes.

## MINOR

1. **Write the reversed inequality explicitly.**

   Location: [§3](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:140).

   From §2,
   \[
   tree(f)\le 1+opt(a)+opt(b),
   \]
   so the actual implication is
   \[
   tree(f)-opt(f)\le s(a,b),
   \]
   i.e. `s ≥ gap`, whereas Krinkin needs `s ≤ gap`. The present prose reaches the right conclusion but phrases it indirectly.

2. **“The two agree only if `opt=tree`” is too absolute.**

   Location: [§3](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:112).

   The two operators differ; their minima may nevertheless coincide for particular functions. Fix to:

   > They coincide term-by-term only on children for which `opt=tree`; as global characterizations they are different.

3. **Use `opt_XAG` in the NPN-invariance sentence.**

   Location: [§4](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:179).

   The argument is correct: NPN transformations preserve total XAG gate count with free complementation, so different values 6/5/3 force different classes. But “`opt` is NPN-invariant” is ambiguous because the paper normally uses bare `opt` for AIG. Write “`opt_XAG` is NPN-invariant.”

4. **The opening of §5 re-inflates the parity explanation.**

   Location: [§5](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:189).

   “The AIG gaps coincide with the cost of building parity” sounds like a mechanism for all 72 violating classes, which §4 correctly declines to establish. Use “The large parity AIG gaps…” or “The parity example suggests…”.

5. **The Krinkin blocks are faithful but normalized, not letter-for-letter quotations.**

   Locations: [§2](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:75), [§3](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v2.md:109).

   I found no meaning-changing misquotation: the §2 decomposition is equivalent to the PDF’s polarity notation; the Bellman base case is included; and Corollary 6 includes `C` optimal, `g` any gate, and the child sub-DAG premises. For publication hygiene, either reproduce the displays literally or label the blocks “notation-normalized quotations.”

6. **Checker provenance could be stronger.**

   [verify_lowk.log](/Users/lab/Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/certs/verify_lowk.log:1) has all eight `s VERIFIED` results and hashes, but not the exact `drat-trim` commit, command lines, or exit codes requested in Round 2. Add those if easily recoverable. This is reproducibility polish, not a mathematical defect.

## Confirmed closures

- The shared Lean block is correctly `¬(x₁⊕x₂)`: node 5 in [UnitGap.lean](/Users/lab/Projetos/7_problems/PNP_AI/formal/UnitGap.lean:339). Its three gates are exactly the intersection of the output-child cones.
- The maximum-gap classes are exactly `0x1668`, `0x16e9`, `0x6996`, each `opt_AIG=9`, `tree_AIG=15`; their `opt_XAG` values are 6/5/3. The NPN-invariance argument is valid.
- Appendix A now correctly derives non-tree structure from `gap=1` before counting incidences. The proof `2m=I_var+I_gate≥n+m` is complete.
- Krinkin’s §2 identity, §3 Bellman operator and base case, and Corollary 6 premises agree substantively with the PDF.
- The “incompatible characterizations” framing and classification of the overshoot claim as a consequence of Theorem 2 are fair.
- Krinkin’s Corollary 6 proof indeed uses the inequality in the wrong direction.
- `search_n5_dedup.csv` contains 25,373 distinct rows and 25,373 distinct truth tables; all 25,373 pass the five-essential-variable test. Counts are exactly 24,875 gap-0, 294 gap-1, 204 inconclusive, zero separators: 25,169 gap-decided.
- The abstract’s `n≤4` and uncertified-XAG-UNSAT hedges are adequate.
- Appendix B adequately explains the parity-5 false positive and correction.
- All 16 CNF/DRAT files are present. Every recomputed SHA-256 matches `verify_lowk.log` for all eight proof pairs. I could not independently replay them because `drat-trim` is not installed in this environment.
- Numeric reconciliation succeeded: AIG gaps `93/57/40/13/14/2/3`; XAG gaps `218/4`; maxima AIG/XAG/MIG `10/7/7`; `opt_XAG<opt_AIG` in 190/222 classes; MIG buckets `2/2/5/18/42/117/35/1`; parity-4 rows `9/15`, `3/3`, `6/—`; and the 494/494 replay log is present.

**VERDICT: v2 has no remaining mathematical hole, but is not yet ready for LaTeX conversion/submission until the four IMPORTANT wording/artifact inconsistencies above are fixed; after those small fixes, it is ready pending the author-response window.**
