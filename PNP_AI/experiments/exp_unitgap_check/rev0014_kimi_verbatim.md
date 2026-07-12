(node:28470) ExperimentalWarning: SQLite is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
approve

The hardening branch is sound. The new Bellman fixed-point implementation (`tree_gap_n4_v2.py`) is algorithmically independent from the layered-BFS v1, covers all polarity combinations explicitly, and converges to the true tree-formula optimum. The CSV upgrade of `0x1669`/`0x166b` from `improved_ub` to `exact` is legitimate given the DRAT-certified claims 0022/0023, and the new `status == "exact"` assert in `tree_gap_n4.py` is the right safeguard. The only material issue was the stale metadata that this diff already fixes.

## Finding 1 — CSV metadata staleness fixed; assert is the right guard
`Projetos/7_problems/PNP_AI/experiments/exp_gate_0001/npn4_opt_aig.csv:184` and `:186`
`Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py:86-87`

The catalog left `0x1669` and `0x166b` as `improved_ub` even though claims 0022/0023 proved `opt=10` with DRAT `s VERIFIED` and explicit 10-gate witnesses. The diff corrects both rows to `status=exact` and adds:

```python
nonexact = [r["npn_rep_hex"] for r in rows if r["status"] != "exact"]
assert not nonexact, f"catalogo com linhas nao-exatas: {nonexact}"
```

This is appropriate: the gap distribution is only as strong as the opt catalog, and silently consuming `improved_ub` rows would have weakened the claim. Other consumers such as `run_gate.py:61` already filter on `status == "exact"`, so the new assert is consistent with existing usage.

## Finding 2 — v2 Bellman relaxation is sound and complete
`Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_v2.py:40-53`

The recurrence is exact for the AIG tree model:

- Lines 45-46 iterate `aa in (a, a ^ MASK)` and `bvec in (known, known ^ MASK)`, covering the four edge-polarity combinations `a&b`, `~a&b`, `a&~b`, `~a&~b`.
- Line 49 also relaxes `f ^ MASK`, absorbing free output negation.
- `newc = 1 + ca + kc` charges one gate plus the full cost of each child formula, enforcing fan-out 1 (no sharing).
- `np.minimum.at` with duplicate indices is correct here: it applies `cost[i] = min(cost[i], val)` for each duplicate, which is equivalent to taking the per-index minimum.

Because initial costs are finite only for constants/literals, every relaxation corresponds to a valid formula, and iteration from `INF` with monotone decreasing updates converges to the least fixed point of the Bellman equation, which equals the true minimum. The cheap-first ordering at line 38 only affects convergence speed, not the fixed point.

## Finding 3 — v1/v2 agreement is meaningful independence, not a shared-bug artifact
`Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4.py:42-72`
`Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_v2.py:24-57`

The two implementations differ structurally:

- v1 builds exact frontier layers `D_k` and relies on complement-closed layers to absorb polarities.
- v2 does a global fixed-point sweep and handles polarities explicitly, with no layer invariant.

Both seed the same 10 cost-0 functions (`0`, `1`, four literals, four negated literals), and both use the same standard truth-table convention (bit `t` is output on input row `t`). The agreement on all 65,536 cells is therefore unlikely to come from a shared modeling bug. This is further corroborated by the external REV-0013 run, which independently re-implemented the DP and obtained identical cost-level counts `{10, 48, 256, 940, 2048, 5248, 8672, 11768, 10592, 11536, 5472, 6304, 960, 1472, 96, 114}`.

## Finding 4 — adversarial checks on the tree DP pass
`Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_v2.py:92-96`

The v2 script recomputes v1 inline and fails on any divergence. In addition, the following adversarial invariants hold in both scripts:

- Complement invariance is maintained: v1 asserts `cost[f] == cost[f ^ MASK]` for all 65,536 functions; v2 enforces it symmetrically by always relaxing `f` and `f ^ MASK` together.
- No undercounting: every function assigned cost `k` is built from subformulas of costs `i` and `j` with `i + j + 1 = k`.
- No overcounting / sharing: the recurrence `1 + cost(a) + cost(b)` pays for two independent copies of the child formulas; there is no memoization or DAG sharing across the tree.
- Worst-case sanity: `tree(0x6996) = 15`, matching the Khrapchenko lower bound of `32² / (8·8) = 16` leaves ⇒ ≥ 15 gates for parity-4.

## Finding 5 — minor: v2 uses scalar inner loop over chunked outer loop
`Projetos/7_problems/PNP_AI/experiments/exp_unitgap_check/tree_gap_n4_v2.py:40-43`

The outer loop chunks over `known` but then iterates `for a, ca in zip(A.tolist(), cA.tolist())` scalar-by-scalar. This is correct but leaves performance on the table; it is not a bug given the 6-sweep convergence, but a fully vectorized inner loop would be a straightforward later optimization. No action required for correctness.

## Suggestion
Consider adding the same `status == "exact"` guard to any other scripts that join `npn4_opt_aig.csv`, or centralize the catalog load behind a helper that rejects non-exact rows by default. The current fix is sufficient for the claim-0026 pipeline.
