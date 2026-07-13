# AUDIT SWEEP 001 — Shortlist scoreada de alvos (Problema 1: P=NP-adjacente)

> **Status:** entregue para decisão de Luiz (2026-07-13). Varredura autorizada por ele; NENHUM alvo
> aprovado ainda. Protocolo: busca semântica em papers (2024+) em 3 framings (exact synthesis
> small-n / MCSP concreto / databases de implementações ótimas) + tentativa de expansão por grafo
> de citações a partir dos papers do Krinkin (vazia — papers novos demais, 1 citação).
> Score pelos 5 eixos do 11_AUDIT_TRACK_CHARTER §3. 0 chamadas de modelo; 0 contato externo.

## Shortlist (ordenada por recomendação)

### A. arXiv:2601.08368 — "A New Tool to Find Lightweight (And, Xor) Implementations of Quadratic Vectorial Boolean Functions up to Dimension 9" ⭐ RECOMENDADO como Alvo 2

| Checabilidade | Peso | Tratabilidade | Reparabilidade | Risco |
|---|---|---|---|---|
| 5 | 4 | 4 | 5 | baixo |

(AND, XOR) = exatamente a nossa base XAG, com encoder validado por gate. O paper publica
implementações de funções vetoriais quadráticas até dimensão 9 encontradas por ferramenta
heurística — ou seja, **upper bounds sem certificado de otimalidade**. Auditoria: verificar
minimalidade das implementações publicadas via exact synthesis (extensão multi-output do nosso
encoder, trabalho moderado); qualquer melhoria que acharmos é **vitória construtiva** (circuito
menor certificado = presente, não ataque) para uma comunidade APLICADA (lightweight crypto:
custo de S-box/masking é medido em portas AND). Perfil ideal de primeiro alvo pós-Krinkin.

### B. arXiv:2511.16903 — "Simple Circuit Extensions for XOR in PTIME" (Alvo 3 natural)

| Checabilidade | Peso | Tratabilidade | Reparabilidade | Risco |
|---|---|---|---|---|
| 4 | 5 | 3 | 3 | médio-baixo |

Linha Ilango/MCSP* (ETH-hardness de MCSP total — o CORAÇÃO da nossa linha teórica). Usa
caracterizações de circuitos ótimos para extensões de XOR. Auditoria: stress-test mecanizado das
caracterizações em n pequeno com nosso ground truth. Peso teórico máximo; checabilidade parcial
(parte estrutural é prosa). Encaixa como alvo seguinte, quando o motor multi-output existir.

### C. arXiv:2503.19103 — "Simplifier: A New Tool for Boolean Circuit Simplification" (quick win paralelo)

| Checabilidade | Peso | Tratabilidade | Reparabilidade | Risco |
|---|---|---|---|---|
| 5 | 3 | 5 | 5 | baixo |

Tool open-source com database de subcircuitos 3-input "ótimos". Nós TEMOS o ground truth n=3
completo em 3 bases (AIG/XAG/MIG, com gates). Validação estilo MIG-match em dias. Menor manchete,
mas barato e rende nota curta + relacionamento com os autores (grupo de SAT).

### D. arXiv:2601.04446 — "Optimal Depth-Three Circuits for Inner Product"

| Checabilidade | Peso | Tratabilidade | Reparabilidade | Risco |
|---|---|---|---|---|
| 3 | 4 | 3 | 3 | baixo |

Claims de otimalidade com matching bound (Göös et al.). Verificável em n pequeno, mas modelo
depth-3 exige encoder novo. Fila de espera.

### E. bioRxiv 2025.11.28.691216 — database de implementações ótimas p/ biologia sintética

| Checabilidade | Peso | Tratabilidade | Reparabilidade | Risco |
|---|---|---|---|---|
| 5 | 3 | 5 | 5 | baixo |

Circuitos genéticos: cada porta a mais tem custo biológico real. Validar/melhorar a database deles
com certificados = história cross-disciplinar boa ("auditoria que ajuda outra área"). Fila de espera.

## Descartados no gate (anti-padrões)

Papers de lower bound assintótico puro (2503.24061 magnificação, 2411.02936, 2604.04760, etc.):
peso alto mas **checabilidade < 4** (prosa assintótica, sem componente mecanizável no nosso
alcance). Ferramentas de SAT-solving (CASCAD etc.): fora do escopo de claims matemáticos.

## Recomendação

**Alvo 2 = A** (motor: estender encoder XAG para multi-output — reutilizável para B e E depois)
com **C como quick-win paralelo** (dias, ground truth já pronto). Decisão de Luiz.
