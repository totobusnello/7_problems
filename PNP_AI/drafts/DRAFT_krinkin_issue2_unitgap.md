# Issue #2: repo `krinkin/unit-gap` — ENVIADA

> **Status (2026-07-11): ISSUE ABERTA — https://github.com/krinkin/unit-gap/issues/1** (autorização de Luiz: "então vamos", após checagem de certeza — 4 famílias + fail-safe Khrapchenko). Ajuste no envio: anexos substituídos por LINKS para os artefatos versionados no repo público totobusnello/Claude (verificabilidade máxima, com histórico como carimbo). Texto enviado = corpo abaixo.
>
> **Histórico: DRAFT criado e aprovado 2026-07-11.** Alvo: github.com/krinkin/unit-gap (repo próprio do paper —
> venue correto; a issue #1 do catálogo vive em krinkin/bounds). Tom: pergunta-antes-de-afirmar,
> com oferta construtiva (prova corrigida do Thm 3). Anexos: DRATs pequenos (11KB/147KB) upáveis
> direto na issue (recomendação da REV-0012). Backing: 4 famílias adversariais SUSTENTARAM
> (REV-0009..0012); claims 0024/0025.

---

**Título:** `Question about the tree(f) recursion in §2 — parity of 3 variables appears to give gap = 3 under the paper's definition of formula`

**Corpo:**

Hi Kirill,

Same person from krinkin/bounds#1 — while reading *The Unit Gap* (arXiv:2603.08033v2) we hit
something in §2 that we'd like to check with you before drawing conclusions, because it affects
Theorem 2. It's possible we're misreading the intended definition; if so, please correct us.

**The question.** §2 defines a formula verbally as "a circuit in which every gate has fan-out
one — a tree", and then displays:

> tree(f) = min over f = a∧b (or f̄ = a∧b) of (1 + opt(a) + opt(b)).

Under the verbal definition, the children of the root gate of a formula must themselves be
**formulas**, so the recursion for minimum formula size would be
`tree(f) = min (1 + tree(a) + tree(b))` — with `tree`, not `opt`, on the right-hand side. With
`opt` in the children, the trivial decomposition f = 1∧f indeed gives ≤ 1 + opt(f), but the object
being minimized is no longer a tree (the children may be internally shared DAGs). **Is the
displayed identity the intended definition of tree(f), or is it a typo for the tree-recursive
version?**

**Why it matters — a concrete case.** For parity of three variables (f = x1⊕x2⊕x3, tt `0x96`):

- **opt(f) = 6**: two chained 3-gate XOR blocks sharing the middle node; UNSAT at 5 gates by
  kissat 4.0.4 with a DRAT proof checked by drat-trim (`s VERIFIED`, 147 KB — attached).
- **tree(f) = 9** under the verbal (fan-out-one) definition: an explicit 9-gate tree exists
  (duplicate the x1⊕x2 subformula; snippet below verifies it in seconds), and no 8-gate formula
  exists — by an exact fixed-point computation of the tree recursion over all 256 functions,
  independently confirmed by a layer-by-layer enumeration (new functions per cost 1..9:
  24, 64, 30, 80, 32, 0, 16, 0, 2 — the two cost-9 functions are exactly `0x96` and `0x69`).
  Analytically, Khrapchenko's bound already gives ≥ 9 leaves ⟹ ≥ 8 gates, so gap ≥ 2 regardless
  of our computations.

That yields gap(⊕₃) = 3. We suspect this is consistent with your own data: in Table 1 (n = 3,
complete), the two functions listed as gap = 1 at opt = 6 are — if we decoded them correctly —
exactly parity and its complement, which is what the displayed recursion (with `opt` in the
children) would report for them.

**A second, definition-independent point.** In the 6-gate optimal circuit for ⊕₃, the two
children of the output gate both contain the 3-gate sub-DAG computing x1⊕x2, so the sharing term
of Corollary 6 is s = 3 (structurally, and arithmetically: 1 + 4 + 4 − 6 = 3, with
opt((x1⊕x2)∧¬x3) = 4 certified by an UNSAT-at-3 DRAT proof, 11 KB — attached). This seems to
contradict s ∈ {0,1} independently of how tree(f) is defined. It would also affect the proof of
Theorem 7 (which uses Corollary 6), though not necessarily its statement as a conditional on
gap = 1.

**On the positive side**, Theorems 3 and 4 seem robust to all of this. For Theorem 3 we can offer
a small fix, since the |S| ≥ k−1 count in the published proof has an edge case (g being an
input-level gate): counting input incidences instead — a useful circuit with m gates has 2m
input slots, and n essential inputs plus m−1 non-output gates each need fan-out ≥ 1, plus one
extra incidence if any gate is shared — gives 2m ≥ n + m, i.e. m ≥ n, for every non-tree optimal
circuit (any gap > 0, in fact). Happy to write this up properly if useful.

**Verification snippet for the 9-gate tree** (python, stdlib):

```python
def par3_tree9(x, y, z):
    g1 = x & ~y & 1; g2 = ~x & y & 1; g3 = ~(~g1 & ~g2) & 1   # copy 1 of x^y
    g4 = x & ~y & 1; g5 = ~x & y & 1; g6 = ~(~g4 & ~g5) & 1   # copy 2
    g7 = g3 & ~z & 1; g8 = ~g6 & z & 1
    return ~(~g7 & ~g8) & 1
assert all(par3_tree9(t&1, (t>>1)&1, (t>>2)&1) == (bin(t).count('1') & 1) for t in range(8))
```

**Provenance note** (same as in bounds#1): this comes from an AI-assisted research program led by
L. A. Busnello — analysis and scripts produced by an AI system (Claude, Anthropic) under human
direction, with certificates checked by standard independent tools (kissat/drat-trim), and the
mathematical claims cross-reviewed adversarially by four independent model families before
contacting you. All artifacts (scripts, CNFs, DRAT proofs, outputs) are available.

If the intended definition of tree(f) is the displayed identity (children as optimal circuits),
then Theorem 2 is of course consistent as arithmetic — but then it measures a one-level
decomposition cost rather than formula size, and the comparison with the classical Θ(n²) parity
formula bound in §3 wouldn't apply. Either way we thought you'd want to know before this
propagates. And again — if we've misread something, we'd genuinely like to understand the
intended reading.

Best regards,
Luiz Antonio (Toto) Busnello

**Anexos a subir na issue:** `certs/par3_k5.cnf`, `certs/par3_k5.drat` (147 KB),
`certs/h_child_k3.cnf`, `certs/h_child_k3.drat` (11 KB) — do repo do programa.

---

## Notas internas (não vão no texto)

- Enviar SÓ após aprovação de Luiz. GitHub issues aceitam anexos por upload (arrastar) — se a API
  não suportar anexo direto, subir os 4 arquivos num gist público e linkar (decisão no envio).
- Se o autor responder à issue #1 antes do envio, considerar referenciar a resposta.
- Tudo o que a issue afirma tem lastro: claims 0024/0025 (4 famílias), certs versionados,
  fórmula-testemunha simulada nesta sessão.
