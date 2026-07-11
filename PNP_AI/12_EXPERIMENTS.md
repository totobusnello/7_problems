# PNP-AI — 12 — EXPERIMENTS

> Todo experimento registra: código, versão, parâmetros, hardware (quando relevante), entradas, saídas, seeds, tempo, memória, limite do experimento, conclusão permitida e conclusão NÃO permitida.

---

## EXP-PED-0001 — Redução 3-COLORING → SAT (pedagógico)

- **Data:** 2026-07-10 · **Fase:** 2 (pedagógica) · **Código:** `experiments/exp_ped_0001_3col_to_sat.py`
- **Ambiente:** Python 3.14.3, python-sat (Glucose4), macOS darwin 25.6.0. Determinístico (sem seeds).
- **Codificação:** x[v,c] = "vértice v tem cor c"; cláusulas: ≥1 cor por vértice, ≤1 cor por vértice, vizinhos com cores distintas. Tamanho O(|V|+|E|) — redução linear.
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
