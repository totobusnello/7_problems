# PNP-AI — 06 — NP-COMPLETENESS MAP

> Mapa de problemas NP-completos e reduções relevantes para experimentação. Iniciado na FASE 3 (2026-07-10); cresce conforme as fases avançam.

## Núcleo histórico verificado

**Cook 1971 [SRC-0005]:** tautologies ≡ DNF tautologies ≡ D3 (3 literais) ≡ subgraph pairs (mesmo grau polinomial — Theorem 2). Já com a observação de que {primes} e {isomorphic graph pairs} não se encaixavam — os dois "casos especiais" que a história confirmou.

**Karp 1972 [SRC-0006, via OCR do scan]:** Main Theorem — os 21 problemas da lista são completos. Capturados: SATISFIABILITY, 0-1 INTEGER PROGRAMMING, CLIQUE, SET PACKING, NODE COVER, SET COVERING, FEEDBACK NODE SET, FEEDBACK ARC SET, [item 9 ilegível no scan — pela literatura, DIRECTED HAMILTON CIRCUIT ⚠️], UNDIRECTED HAMILTON CIRCUIT, SAT WITH AT MOST 3 LITERALS PER CLAUSE, CHROMATIC NUMBER, CLIQUE COVER, EXACT COVER, HITTING SET, STEINER TREE, 3-DIMENSIONAL MATCHING, KNAPSACK, SEQUENCING, PARTITION, MAX CUT.

**Levin 1973 [SRC-0007/0008]:** 6 problemas universais de busca (incl. Satisfiability), com universalidade "somewhat stronger than in the sense of Cook–Karp" (Trakhtenbrot).

## Reduções com implementação executável no projeto

| Redução | Direção | Implementação | Status |
|---|---|---|---|
| 3-COLORING → SAT | CHROMATIC NUMBER (k=3) ≤p SAT | `experiments/exp_ped_0001_3col_to_sat.py` (O(\|V\|+\|E\|) cláusulas) | Executada; lema de correção = claim 7P-PNP-CLM-0010 |

## Uso experimental (FASE 5+)

Critério para adicionar problema ao mapa: ter (i) codificação executável p/ solver, (ii) gerador de instâncias, (iii) fonte da prova de NP-completude no ledger. Candidatos naturais: 3-SAT (gerador de instâncias aleatórias na transição de fase), CLIQUE/NODE COVER (grafos), SUBSET-SUM/PARTITION (aritméticos).
