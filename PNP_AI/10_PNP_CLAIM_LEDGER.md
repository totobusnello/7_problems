# PNP-AI — 10 — CLAIM LEDGER

> IDs: `7P-PNP-CLM-NNNN`. Estados e campos obrigatórios definidos em `../05_GLOBAL_CLAIM_LEDGER.md`. Append-only: claims refutados permanecem registrados.
> Origem comum dos claims 0001–0007: SRC-0003 (Cook, "The P versus NP Problem", doc oficial Clay), trechos conferidos verbatim via parse local do PDF em 2026-07-10. Detalhes em `01_OFFICIAL_PROBLEM_SPEC.md`.

| Claim ID | Enunciado (resumo) | Estado | Origem | Última atualização |
|---|---|---|---|---|
| 7P-PNP-CLM-0001 | Formulação oficial do problema: "Does P = NP?"; resposta independe de \|Σ\|≥2; caso unário aberto; P ⊆ NP trivial | SOURCE_VERIFIED | SRC-0003 §1 | 2026-07-10 |
| 7P-PNP-CLM-0002 | Definição de P: linguagens decididas por TM em tempo polinomial de pior caso; classe robusta a modelos razoáveis | FORMULATION_VERIFIED | SRC-0003 §1 | 2026-07-10 |
| 7P-PNP-CLM-0003 | Definição de NP via checking relations: L ∈ NP ⟺ ∃k, R poly-time com w ∈ L ⟺ ∃y(\|y\| ≤ \|w\|^k ∧ R(w,y)); R poly-time ⟺ L_R ∈ P | FORMULATION_VERIFIED | SRC-0003 §1 (verbatim) | 2026-07-10 |
| 7P-PNP-CLM-0004 | ≤p exige f computável em tempo polinomial (Def. 3); NP-completude: L ∈ NP e L' ≤p L ∀L' ∈ NP (Def. 4) | FORMULATION_VERIFIED | SRC-0003 §2 (verbatim; qualificador poly-time conferido após falha de extração automática) | 2026-07-10 |
| 7P-PNP-CLM-0005 | Proposition 1: (a) ≤p preserva P para baixo; (b) método de propagação de NP-completude; (c) L NP-completo ∈ P ⟹ P = NP | SOURCE_VERIFIED | SRC-0003 §2 | 2026-07-10 |
| 7P-PNP-CLM-0006 | SAT é NP-completo (Cook 1971 [9]; Levin 1973 [23] indep.; Karp 1972 [21]: +20 problemas, notação padrão e ≤p); 3-SAT NP-completo | SOURCE_VERIFIED (fontes primárias OBTIDAS 2026-07-10: SRC-0005/0006/0007 no source ledger; enunciados conferidos; **reconstrução das provas pendente** — FASE 3) | SRC-0003 §2 + SRC-0005/6/7 | 2026-07-10 |
| 7P-PNP-CLM-0007 | Critérios de solução: P=NP ⟸ algoritmo polinomial uniforme correto p/ um NP-completo; P≠NP exige limitação universal enfrentando relativization (oráculo A com P^A=NP^A) e natural proofs (Razborov–Rudich); melhor circuit lower bound p/ NP registrado no doc: ~4n. Regras Clay: Qualifying Outlet + 2 anos + aceitação geral; sem submissão direta | SOURCE_VERIFIED | SRC-0003 §3 + SRC-0004 | 2026-07-10 |

| 7P-PNP-CLM-0008 | Cook 1971 verbatim: Theorem 1 (NTM poly-time ⟹ P-reducible a {DNF tautologies}); P-reducibility é redução de TURING (query machine + oráculo), não many-one; Theorem 2 (tautologies ≡ DNF taut. ≡ D3 ≡ subgraph pairs); Remark: primes e graph isomorphism já apontados como não classificados em 1971 | SOURCE_VERIFIED | SRC-0005 (verbatim, cópia redigitada) | 2026-07-10 |
| 7P-PNP-CLM-0009 | Equivalência das caracterizações de NP: verificador+certificado ⟺ NTM poly-time | Enunciado FORMULATION_VERIFIED; prova [RECONSTRUÇÃO] em `05_COMPLEXITY_FOUNDATIONS.md` §2 — revisão externa pendente | SRC-0003 + SRC-0005 | 2026-07-10 |
| 7P-PNP-CLM-0010 | Lema: φ(G) (codificação one-hot de 3-COLORING) é satisfatível ⟺ G 3-colorável; 4n+3\|E\| cláusulas, Θ(n+\|E\|) literais; construção O(n+\|E\|) em word-RAM com lista de arestas, O((n+\|E\|)log n) em codificação de bits; em qualquer caso polinomial ⟹ 3-COLORING ≤p SAT | **DERIVED_CHECKED** — histórico: proposto → REV-0001 (Codex adversarial): lógica confirmada, **GAP_FOUND** na complexidade original "O(n+\|E\|)" sem modelo/representação (contraexemplo: matriz de adjacência Θ(n²)) → correção mínima do revisor ACEITA e incorporada ao enunciado | Projeto (EXP-PED-0001) + REV-0001 | 2026-07-10 |
| 7P-PNP-CLM-0011 | Cook–Levin forma moderna (SAT NP-completo sob ≤p) com esboço de prova via tableau (grupos G1–G5, tamanho O(Q(n)²)) | [RECONSTRUÇÃO] esboço completo em `05_COMPLEXITY_FOUNDATIONS.md` §4 — revisão externa pendente; formalização = FASE 6 | SRC-0005 (estrutura) + reconstrução | 2026-07-10 |
| 7P-PNP-CLM-0012 | Auto-redutibilidade de SAT: oráculo de decisão ⟹ busca em n consultas (P=NP ⟹ versão construtiva também polinomial) | [RECONSTRUÇÃO] prova em `05_COMPLEXITY_FOUNDATIONS.md` §5 — revisão externa pendente | Reconstrução padrão | 2026-07-10 |

## Observações

- Claims 0001–0009 e 0011–0012 são reconstruções de resultados conhecidos (fundação das fases 2–4) — NENHUM é alegação de novidade.
- **0010 é o primeiro claim a completar o ciclo proposta → revisão adversarial → gap → correção → DERIVED_CHECKED** (REV-0001, registro integral em `../07_MODEL_CALL_LOG.md`).
- A barreira de **algebrization** (Aaronson–Wigderson 2008) NÃO está no documento de Cook; será registrada com fonte própria na FASE 4.
