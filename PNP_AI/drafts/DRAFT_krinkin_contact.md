# DRAFT — Contato com K. Krinkin (repo `krinkin/bounds`) — AGUARDANDO APROVAÇÃO DE LUIZ

> **Status: DRAFT. NADA FOI ENVIADO.** Regra 10_PUBLICATION_RULES: qualquer contato externo exige
> autorização explícita de Luiz + aprovação do texto final. Este arquivo é o texto proposto.
>
> **Sequência proposta (recomendação da REV-0005/GLM):** abrir primeiro a ISSUE (pergunta antes de
> afirmar); se o autor confirmar interesse, abrir o PR (fork → branch → PR) com o diff da Parte B.
> Conta a usar: `totobusnello` (decisão de Luiz).
>
> **Decisões pendentes de Luiz:** (1) autorizar envio; (2) como nos apresentamos — o texto abaixo
> usa "AI-assisted research program" com atribuição honesta de papéis; ajustar se quiser;
> (3) hospedagem das provas de 4,5GB/3,6GB se o autor pedir (Zenodo grátis vs link direto).

---

## PARTE A — GitHub Issue (abrir primeiro) — inglês

**Título:** `Exact values for the two improved_ub classes: opt_AIG(0x1669) = opt_AIG(0x166b) = 10 (DRAT-certified)`

**Corpo:**

Hi Kirill,

Your paper (arXiv:2603.09379) and this dataset leave exactly two NPN-4 classes without exact
values — `0x1669` and `0x166b`, both listed as `improved_ub` with upper bound 10. We believe we
have closed both, and before anything else we wanted to ask: **Is this gap still open on your
side** (no unpublished exact values or follow-up in progress)? If it is, we'd be glad to
contribute the results back via a PR.

**Result.** Under the same cost model as your catalog (2-input AND gates, free inversions on
edges and output, size = number of AND gates):

```
opt_AIG(0x1669) = 10
opt_AIG(0x166b) = 10
```

i.e. your upper bounds are tight.

**Lower bound (opt ≥ 10).** SAT-based exact synthesis (one-hot operand-selection encoding,
1273 vars / 133,909 clauses at k=9). `kissat 4.0.4` returns UNSAT for k=9 for both classes,
with DRAT proofs checked by `drat-trim` (commit 2e3b2dc) — each proof generated and verified
independently on two machines (macOS/arm64 and Ubuntu/EPYC):

| class | DRAT size | drat-trim | proof SHA-256 |
|---|---|---|---|
| 0x1669 | 4.8 GB | `s VERIFIED` (12,162,375 of 20,591,176 lemmas in core) | `49e125a3bb6ee732508374450f1393f58892ffe44584c5c925e2b3905f8d7762` |
| 0x166b | 3.9 GB | `s VERIFIED` (10,679,089 of 17,445,110 lemmas in core) | `10ebb75c41bf25660f6057a35cdb9c6e51a9f8556c00b9cca18a308ac0e6dd51` |

CNF SHA-256: `ae822d22…df87d1a` (0x1669), `3e669606…78ca64f` (0x166b) — 1.7 MB each, attached
on request; proofs are deterministic to regenerate (~20–25 min each on one core) or we can host
them (Zenodo). We additionally ran the same encoder for k = 1..8 (all UNSAT, ≤48 s each), so the
value does not rest on any implicit monotonicity argument.

**Upper bound (opt ≤ 10).** Explicit 10-gate circuits, checked by exhaustive simulation over all
16 input rows. Gate i has inputs (a, pa, b, pb): node a with polarity pa AND node b with polarity
pb; nodes 1–4 are the inputs x1..x4, node 4+i is gate i; the output is the last gate,
non-inverted. You can re-check each in seconds with the snippet below.

```
0x1669 (tt=5737): [(3,0,4,0),(3,1,4,1),(1,1,2,1),(2,0,5,1),(1,0,8,0),
                   (7,1,9,1),(5,1,6,1),(10,0,11,1),(10,1,11,0),(12,1,13,1)]
0x166b (tt=5739): [(2,0,3,0),(2,1,3,1),(1,0,6,1),(5,1,6,1),(4,1,8,0),
                   (4,0,8,1),(9,1,10,1),(1,1,11,1),(7,0,9,1),(12,1,13,1)]
```

```python
def simulate(circ, n=4):
    tt = 0
    for t in range(1 << n):
        v = {j + 1: (t >> j) & 1 for j in range(n)}
        for i, (a, pa, b, pb) in enumerate(circ):
            v[n + 1 + i] = (v[a] ^ pa) & (v[b] ^ pb)
        tt |= v[n + len(circ)] << t
    return tt   # expect 5737 / 5739
```

**Encoder validation.** Before touching the open classes, the encoder was validated against an
independent exhaustive enumerator (all 2-input functions; all 3-input functions bidirectionally
up to k=3) and reproduced a solved catalog entry (opt_AIG(0x0016)=7) with a DRAT-checked UNSAT
at k=6.

**Effect on your verification.** With the two classes marked `exact`, `scripts/verify_all.py`
extends from 987 to **995 exact-exact mutation edges, and the Lipschitz bound holds on all of
them** — max |diff_opt| stays 4 = n (distribution: |0|=301, |1|=421, |2|=221, |3|=45, |4|=7;
still 7 tight edges, unchanged). So the exhaustive n=4 verification in the paper becomes
gap-free.

**Provenance note.** This came out of an AI-assisted research program led by L.A. Busnello: the
encoding, scripts, runs and cross-checks were produced by an AI system (Claude) under human
direction, with all certificates checked by standard independent tools (kissat/drat-trim) on two
machines. We're stating this explicitly for transparency; happy to share every artifact.

If the gap is still open, we'll send a PR updating `data/npn4_opt_aig.csv` (2 lines), the README
expected output, and — if you want — the two witness circuits as a small data file. And of course,
if you already have these values or spot an error in the chain above, we'd genuinely like to know.

Best regards,
Luiz Antonio (Toto) Busnello

---

## PARTE B — PR (abrir só depois do OK do autor na issue)

**Título:** `Close the two improved_ub classes: 0x1669 and 0x166b are exactly 10 (DRAT-certified)`

**Mudanças:**

1. `data/npn4_opt_aig.csv` — 2 linhas:
```diff
-0x1669,5737,10,improved_ub
+0x1669,5737,10,exact
-0x166b,5739,10,improved_ub
+0x166b,5739,10,exact
```

2. `README.md` — bloco "Expected output" (números verificados rodando o `verify_all.py` do
   próprio repo com o CSV atualizado, 2026-07-11):
```diff
-- 220 exact classes, 2 upper bounds
-- 987 exact-exact mutation edges
+- 222 exact classes, 0 upper bounds
+- 995 exact-exact mutation edges
 - Max |diff_opt| = 4 = n
-- Distribution: |0|=300, |1|=414, |2|=221, |3|=45, |4|=7
+- Distribution: |0|=301, |1|=421, |2|=221, |3|=45, |4|=7
 - 0 violations
 - 7 edges achieving |diff| = n
```
   E na seção "Files": `220 exact, 2 upper bounds` → `222 exact (2 contributed, see PR #N)`.

3. (Opcional, se o autor quiser) `data/witness_circuits_0x1669_0x166b.json` — os 2 circuitos de
   10 portas no formato acima.

**Corpo do PR:** versão condensada da issue (resultado, cadeia de certificação com hashes,
validação do encoder, saída nova do verify_all.py) + link para a issue.

---

## Apêndice — fatos conferidos que sustentam o draft (não vão no texto)

- Re-simulação independente dos 2 circuitos nesta sessão: tt = 5737/5739 ✓ (2026-07-11).
- `verify_all.py` do autor rodado com CSV original (987 edges, PASS) e atualizado (995, PASS) ✓.
- SHA-256 completos dos CNFs: `ae822d229081d3c888de86275c6373060bdd4f43c8f9cfaa8c0a507d0df87d1a`
  (0x1669), `3e66960696edf4cbdf2b5e83d6bff388a8ca297b160bb803570b912b478ca64f` (0x166b).
- Estatísticas drat-trim verbatim em `experiments/exp_probe_0001/dt_*.out` (tempos 1.389s/1.462s
  no pod; "s VERIFIED" nas 4 execuções Mac+pod).
- Novidade re-checada em 2026-07-11 (REV-0005/GLM, SUSTENTADA): arXiv v1 único, repo sem
  atividade desde 03-10, zero citações no Semantic Scholar.
