# PNP-AI — 12 — EXPERIMENTS

> Todo experimento registra: código, versão, parâmetros, hardware (quando relevante), entradas, saídas, seeds, tempo, memória, limite do experimento, conclusão permitida e conclusão NÃO permitida.

---

## EXP-PED-0001 — Redução 3-COLORING → SAT (pedagógico)

- **Data:** 2026-07-10 · **Fase:** 2 (pedagógica) · **Código:** `experiments/exp_ped_0001_3col_to_sat.py`
- **Ambiente:** Python 3.14.3, python-sat (Glucose4), macOS darwin 25.6.0. Determinístico (sem seeds).
- **Codificação:** x[v,c] = "vértice v tem cor c"; cláusulas: ≥1 cor por vértice, ≤1 cor por vértice, vizinhos com cores distintas. Tamanho exato: 4n+3|E| cláusulas e 9n+6|E| literais (grupo 1: n×3; grupo 2: 3n×2; grupo 3: 3|E|×2) [contagem de literais explicitada após REV-0002]; construção O(n+|E|) em word-RAM com lista de arestas, O((n+|E|)·log n) em bits — em qualquer caso polinomial (complexidade corrigida pela REV-0001; ver claim 7P-PNP-CLM-0010).
- **Hardening pós-REV-0002 (Kimi):** verificação independente agora exige EXATAMENTE UMA cor por vértice (rejeita 0 ou ≥2, sem confiar no solver) + validação de arestas na entrada (range e laços). Re-executado: mesmos resultados (C5/Petersen SAT, K4 UNSAT); testes negativos da validação passam.
- **Entradas e saídas (execução real):**

| Instância | \|V\| | \|E\| | Cláusulas | Resultado |
|---|---|---|---|---|
| C5 (ciclo de 5) | 5 | 5 | 35 | SAT — certificado {0:2, 1:1, 2:0, 3:1, 4:0}, conferido independentemente |
| Petersen | 10 | 15 | 85 | SAT — certificado conferido independentemente |
| K4 (completo) | 4 | 6 | 34 | UNSAT (K4 não é 3-colorável) |

- **Limite do experimento:** 3 instâncias minúsculas; propósito exclusivamente didático.
- **Conclusão permitida:** a redução implementada preserva SIM/NÃO nas instâncias testadas; ilustra concretamente redução polinomial, certificado e a assimetria encontrar/conferir.
- **Conclusão NÃO permitida:** qualquer afirmação sobre P vs NP, sobre desempenho assintótico de solvers, ou sobre correção da redução para todos os grafos (a prova geral da correção da codificação é exercício da FASE 3 — candidata a primeiro lema formalizável).

---

## EXP-GATE-0001 — Gate de qualificação da FASE 5 (pré-registrado na proposta v5) — **PASSOU**

- **Data:** 2026-07-11 · **Código:** `experiments/exp_gate_0001/` (`aig_exact.py` encoder, `enumerate_aig.py` enumerador independente, `run_gate.py` orquestração) · **Dados:** `npn4_opt_aig.csv` (SRC-0027, catálogo Krinkin).
- **Ambiente:** Python 3.14.3 + pysat/Glucose4 (G1/G3), kissat 4.x via brew (G2), drat-trim compilado do fonte (checker independente). Determinístico. Budget pré-registrado: 4h/instância.
- **Resultados (execução real):**

| Critério | Resultado | Tempo |
|---|---|---|
| **G3** validação semântica | n=2: 16/16 funções encoder==enumeração (max opt 3) · n=3: 126 funções opt≤3 conferidas + 130 inalcançáveis confirmadas UNSAT k=1..3 (duas direções) | 0,2s |
| **G1** SAT em k=opt | Classe 0x0016 (opt catálogo 7): circuito de 7 portas encontrado e **verificado por simulação** contra a truth table completa | 0,1s |
| **G2** UNSAT em k=opt−1 | k=6: kissat UNSAT; prova DRAT de 3,6MB **verificada por drat-trim ("s VERIFIED")** | 0,9s + 0,7s check |

- **BUG REAL PEGO PELA VALIDAÇÃO SEMÂNTICA (1ª execução):** o encoder colidia constantes 0/1 com literais DIMACS ±1 (variável 1) — o circuito decodificado não batia com a truth table e o assert de simulação REPROVOU. Corrigido com tipos separados ('const'/'lit') e re-executado. **Confirmação empírica do finding central da REV-0004:** DRAT não teria pego isso; a verificação semântica pegou.
- **Conclusão permitida:** o pipeline exact-synthesis (encoder→solver→certificado→checker independente→validação semântica) funciona de ponta a ponta no hardware local; opt_AIG(0x0016)=7 foi reproduzido independentemente com certificados nas duas direções; FER real de C1 = 5 confirmado NESTA escala (k≤7).
- **Conclusão NÃO permitida:** nada sobre as 2 classes pendentes (k=9 é outra escala de dificuldade — o catálogo registra timeout do autor); nada assintótico; nada sobre n=5.
- **Artefatos grandes (CNF/DRAT) não versionados** — regeneráveis por `run_gate.py` (determinístico).

---

## EXP-PROBE-0001 — Sonda k=9 nas classes pendentes 0x1669 / 0x166b (EM ANDAMENTO)

- **Data:** 2026-07-11 · **Código:** `experiments/exp_probe_0001/` · **Budget aprovado:** 12h/classe.
- **Encoder:** o do EXP-GATE-0001 + quebra de simetria v2 (portas duplicadas proibidas — sound para opt ∈ {9,10}: circuito mínimo não tem duplicatas; gate re-validado integralmente após a mudança). CNF k=9: 1.273 vars, 133.909 cláusulas.
- **Tentativa v1 (ABORTADA — lição de engenharia):** rodada COM proof logging; DRATs ultrapassaram 4,2GB+3,8GB em ~25min (projeção >100GB/12h); processos mortos por pressão de sistema. Lição: **veredito primeiro (sem prova), certificado em execução separada e dimensionada**.
- **v2, resultados:**

| Classe | Veredito k=9 | Tempo | Estado |
|---|---|---|---|
| **0x166b** (tt=5739) | **UNSAT — não existe circuito AIG de 9 portas** ⟹ com ub=10: **opt_AIG = 10** | **1.269s (21min)** — vs timeout do autor do catálogo | COMPUTATIONALLY_TESTED; certificação DRAT + busca do circuito de 10 portas EM EXECUÇÃO |
| 0x1669 (tt=5737) | em execução | — | — |

- **Conclusão permitida (0x166b):** sob o encoder validado no gate, não existe AIG de 9 portas para 0x166b; combinado com o ub do catálogo, opt=10 — pendente de certificado DRAT (rodada em curso) e de auto-verificação do ub (busca k=10 em curso).
- **Conclusão NÃO permitida:** nada sobre 0x1669 ainda; nada além destas classes/base/modelo.

---
