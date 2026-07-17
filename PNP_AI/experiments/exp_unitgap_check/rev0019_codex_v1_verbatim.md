## CRITICAL

None. I found no interpretation or artifact discrepancy that rescues Krinkin’s Unit Gap Theorem or defeats the parity-3 counterexample.

## IMPORTANT

1. **Appendix A: the corrected Theorem 3 proof contains a false implication and omits the bridge from the theorem’s premise.**

   Location: [Appendix A, lines 300–313](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:300).

   The incidence count itself is valid:

   \[
   I_{\rm var}\ge n,\qquad I_{\rm gate}\ge(m-1)+1=m,\qquad 2m\ge n+m.
   \]

   But “a size-optimal AIG that is not a tree (so `gap(f) ≥ 1`)" is false. A function may have both a non-tree optimal circuit and an equally small optimal formula, giving gap zero. The appendix also never explicitly derives non-tree structure from the actual hypothesis `gap(f)=1`.

   Concrete fix: begin:

   > Assume `gap(f)=1` and choose a size-optimal single-output AIG \(C\). Then \(C\) cannot be a tree, since otherwise `tree(f) ≤ |C| = opt(f)`, forcing gap zero.

   Then run the incidence count. Remove the false parenthetical.

2. **Corollary 6: `opt(child)=4` is not certified by UNSAT at \(k=3\) alone.**

   Location: [§3, lines 133–137](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:133) and [§6, line 241](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:241).

   The manuscript itself correctly emphasizes that its encoder is normalized and exact-size. Therefore, an UNSAT certificate at \(k=3\) does not exclude optima at \(k=1,2\). The sentence “`opt = 4` certified by an UNSAT-at-3 DRAT proof” contradicts the paper’s own certification standard.

   The missing argument is available: restricting
   \[
   h=(x_1\oplus x_2)\land\neg x_3
   \]
   at \(x_3=0\) gives two-variable XOR, which requires three AIG gates. Thus `opt(h) ≥ 3`; UNSAT at 3 upgrades this to `opt(h) ≥ 4`; the explicit four-gate cone supplies the upper bound. The other child is NPN-equivalent.

   Concrete fix: state that restriction argument, the four-gate witness, and the NPN equivalence. Alternatively, archive DRAT certificates for \(k=1,2,3\).

3. **The Krinkin blocks are substantively faithful, but they are not verbatim quotations as presented.**

   Location: [§2–§3, lines 74–110](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:74) and [Corollary 6, lines 128–136](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:128). Primary source checked: [Krinkin v2 PDF](/Users/lab/Projetos/7_problems/_sources/krinkin_2026_unit_gap.pdf).

   Problems:

   - The §2 equation is an English rendering of the display, not a verbatim quotation.
   - The Bellman quote splices an equation and a later phrase with an ellipsis, omitting the stated base case.
   - The Corollary 6 quote omits its relevant premise: \(C\) is an optimal AIG, \(g\) is a gate, and \(D_a,D_b\) are the child sub-DAGs inside that circuit.
   - The citation should pin `arXiv:2603.08033v2`, since exact wording is load-bearing.

   Concrete fix: reproduce the complete source wording and equations, including the Bellman base case and the full Corollary 6 hypotheses.

4. **The internal-inconsistency diagnosis is fair, but v1 overstates it technically.**

   Location: [Abstract, lines 20–23](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:20) and [§3, lines 96–111](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:96).

   The central charge is correct: Krinkin verbally defines genuine formula size; §2 asserts an `opt`-in-children identity; §3 claims a recursive-in-children Bellman construction computes `tree`. Those characterizations are incompatible, and parity exposes the contradiction.

   But:

   - §2’s one-shot minimum is not itself a recursion.
   - These are incompatible characterizations, not “two definitions”; the verbal definition is unambiguous.
   - Krinkin’s printed \(T\) only ranges over \(f=a\land b\), whereas §2 includes \(f\) or \(\bar f\). The printed operator also leaves complement closure/base clamping underspecified. Calling the literal display “the correct formula recursion” grants it more coherence than it has.

   Concrete fix:

   > Section 2 and Section 3 give incompatible characterizations of formula size. Under the natural polarity-completed reading, §3’s recursive-in-child construction is the standard formula recurrence.

5. **The manuscript repeats an independently invalid inequality in Krinkin’s Corollary 6 proof without flagging it.**

   Location: [§3, lines 133–139](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:133).

   Krinkin writes
   \[
   1+\operatorname{opt}(a)+\operatorname{opt}(b)-\operatorname{opt}(f)
   \le \operatorname{tree}(f)-\operatorname{opt}(f).
   \]
   But for an arbitrary gate decomposition, the asserted §2 minimum gives the opposite relevant direction:
   \[
   \operatorname{tree}(f)\le 1+\operatorname{opt}(a)+\operatorname{opt}(b).
   \]
   Thus the `s≤1` proof does not follow merely from Unit Gap; it also contains an unjustified—or reversed—comparison.

   Concrete fix: say Krinkin *purports* to derive the bound using this displayed inequality, identify the inequality failure separately, and then give the structural parity refutation. “The step is exactly the refuted Theorem 2” is too coarse.

6. **The \(n=5\) prose still treats 204 unresolved functions as solver-decidable.**

   Location: [Introduction, lines 57–59](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:57) and [§5, lines 192–217](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:192).

   The [deduplicated CSV](/Users/lab/Projetos/7_problems/PNP_AI/experiments/exp_xag_n4/search_n5_dedup.csv:1) matches the table exactly:

   - 25,373 distinct truth tables;
   - 24,875 gap zero;
   - 294 gap one;
   - 204 inconclusive;
   - zero certified separators.

   But only 25,169 functions are gap-decided. The 204 timeouts could still be separators. Therefore “holds empirically … over” the search and “25,373 … solver-decidable” are inaccurate.

   Concrete fix throughout:

   > No separator was certified. All 25,169 gap-decided cases have gap at most one; 204 cases remain unresolved because formula synthesis timed out.

7. **The new DRAT chain exists, but the supplied artifacts do not preserve the claimed checker results for \(k=1,\ldots,4\).**

   Location: [Abstract, lines 15–16](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:15), [§3, lines 113–117](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:113), and [§6, line 240](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:240).

   All ten `par3_k1..k5.{cnf,drat}` files are present and nonempty. That closes the round-1 missing-certificate defect. However, `check_claims_output.txt` preserves `s VERIFIED` only for `par3_k5` and the child certificate. The ledger asserts VPS verification of \(k=1,\ldots,4\), but that is not an independent checker transcript.

   Concrete fix: archive a machine-readable verification log containing the exact `drat-trim` version/commit, commands, CNF and DRAT hashes, exit codes, and `s VERIFIED` output for every \(k=1,\ldots,5\). Do the same for the claimed 494/494 \(n=5\) replay, whose script exists but whose run output is not versioned.

8. **The round-1 XAG hedge is only partially implemented in the abstract.**

   Location: [Abstract, lines 26–29](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:26).

   The body correctly discloses that XAG UNSAT results lack DRAT certification. The abstract merely says “under a gated exact-synthesis pipeline,” which is vague and does not implement the requested prominent disclosure.

   Concrete fix:

   > The exhaustive XAG result is solver-reported under a separately gated encoder; its UNSAT instances are not proof-certified.

## MINOR

1. **Table 3 is not parity-specific.**

   Location: [§3, lines 137–139](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:137).

   Krinkin’s Table 3 aggregates 299 `opt=6` decompositions and reports all as `s=1`. The complete bucket necessarily includes parity, but the table does not isolate a parity row.

   Fix: say that the complete `opt=6` bucket includes the parity decompositions. Replace “reflecting the circular bound” with “consistent with having imposed the bound”; the causal claim is unproved.

2. **MIG agreement is an aggregate cross-check, not external validation of the whole pipeline.**

   Location: [Abstract, lines 30–32](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:30) and [§5, lines 219–224](/Users/lab/Projetos/7_problems/PNP_AI/drafts/paper1_unitgap_basedep_v1.md:219).

   “Bucket by bucket” is now correct. But equal aggregate distributions do not validate per-class assignments, the XAG formula encoder, or the complete synthesis stack.

   Fix: call it “an aggregate external cross-check of the shared exact-synthesis machinery.”

## Round-1 closure summary

- **\(n=5\) deduplication:** closed; CSV exactly matches 25,373 / 24,875 / 294 / 204 / 0.
- **Three maximum-gap AIG classes:** closed; `0x1668`, `0x16e9`, `0x6996` have `opt=9`, `tree=15`, gap 6. Weights are 6/8/8 and exact XAG optima 6/5/3; `0x6996` is parity-4.
- **Parity DRAT files:** all \(k=1,\ldots,5\) present; checker-status archival remains incomplete.
- **Lean trust statement:** closed. [UnitGap.lean](/Users/lab/Projetos/7_problems/PNP_AI/formal/UnitGap.lean:271) uses `native_decide` for `par3_not_in_D8`; v1 correctly calls this compiler-trusted.
- **MIG bucket wording:** closed.
- **XAG hedge:** correct in §5/§6, incomplete in the abstract.
- **Krinkin source use:** mathematically faithful in substance, not yet verbatim/context-complete.
- **Theorem 3:** incidence argument valid, but the stated theorem proof still needs the premise-to-topology bridge.
- **Numeric consistency:** no new arithmetic discrepancy across the abstract, §§4–6, or the cross-base table.

Krinkin’s \(D_a,D_b\) admit no credible rescue: the source fixes them as the two child cones inside the same optimal circuit, whose intersection in the displayed six-gate parity circuit is exactly the three XOR-block gates. Treating them as independently renamed stand-alone circuits would make the intersection arbitrary and destroy Krinkin’s own inclusion–exclusion argument.

**VERDICT: v1 is not ready for LaTeX conversion or submission; the Theorem 3 bridge, child-optimality proof, source quotations, \(n=5\) wording, and certification trail are must-fix first.**
