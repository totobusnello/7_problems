# exp_verify_rerun — rerun do `verify_all.py` do catálogo Krinkin com os 2 valores fechados

- **Data:** 2026-07-11 · **Motivação:** REV-0007 (Codex) finding 4 — os números 987→995 citados na
  nota técnica e na issue precisavam de artefato arquivado, não só menção textual.
- **Procedimento:** download do repo `krinkin/bounds` @ HEAD (`1443063`); patch binário de 2 linhas
  no CSV (`improved_ub` → `exact` nas classes 0x1669/0x166b, line endings preservados); execução do
  `scripts/verify_all.py` DO PRÓPRIO AUTOR (sem modificação) sobre o CSV patchado + o
  `mutation_graph.json` original.
- **Comandos:** `python3 scripts/verify_all.py` (Python 3.14.3, stdlib only — conforme README do autor).
- **Artefatos neste diretório:**
  - `csv_update.diff` — o patch de 2 linhas.
  - `verify_all_updated.out` — saída integral do rerun: **222 exact / 0 ub; 995 exact-exact edges;
    max |diff_opt| = 4; distribuição |0|=301 |1|=421 |2|=221 |3|=45 |4|=7; 7 tight edges; PASS.**
  - `verify_all.py.snapshot` — snapshot do script do autor usado no rerun.
  - `HASHES.txt` — SHA-256 de: CSV original (`5328e44f…` — idêntico ao usado nos experimentos),
    CSV patchado, script, mutation_graph.json.
- **Baseline (CSV original, mesmo script):** 220 exact / 2 ub; 987 edges; max 4; distribuição
  |0|=300 |1|=414 |2|=221 |3|=45 |4|=7; PASS — reproduz exatamente o "Expected output" do README do autor.
- **Conclusão permitida:** COM os dois valores exatos, o conjunto de arestas exact-exact do grafo de
  mutação DO AUTOR cresce 987→995 (+8) e o bound |Δopt| ≤ 4 vale em todas; a distribuição muda em
  |0| (+1) e |1| (+7). A definição/canonicalização das arestas é a do script do autor — não
  redefinimos nada.
- **Conclusão NÃO permitida:** nada sobre exaustividade além do que o script do autor computa.
