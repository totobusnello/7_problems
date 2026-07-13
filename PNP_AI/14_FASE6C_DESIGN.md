# 14 — FASE 6C — Desenho do recorte C-restrito (n=5, dataset de meta-complexidade)

> **Status: PROPOSTA PRÉ-REGISTRADA (2026-07-13) — NADA EXECUTA sem aprovação de Luiz.**
> Sucede o piloto (EXP-PILOT-N5) e a decisão "recorte A morto". Zero gasto até o go.

## 1. Objetivo

Dataset estratificado de classes NPN-5 com opt exato (ou censura rotulada) + metadados ricos —
a ponte C1→C3 da seleção definitiva (experimentos MCSP-adjacentes: a distribuição de complexidade
de funções aleatórias é exatamente o objeto da meta-complexidade). NÃO é catálogo (A morreu no
piloto); é amostra com pesos, publicável como metodologia.

## 2. Filtro de upper bound — VALIDADO (2026-07-13, custo zero)

**UB_Shannon** (`experiments/exp_fase6c_design/shannon_ub.py`): para f de 5 variáveis,
min sobre variável de split e casos degenerados de `opt4(f|x=0) + opt4(f|x=1) + custo_mux`,
com `opt4` = lookup NPN no NOSSO catálogo n=4 exato certificado. Sem código externo.

**Calibração nas 470 classes do piloto** (`ub_calibration.csv`):
- Consistência: UB ≥ opt em todas (assert estrutural — UB < opt abortaria).
- Folga UB−opt nas 24 decididas: {0: 4, 1: 6, 2: 7, 3: 3, 4: 4} — mediana 2, máx 4.
- Custo: ~2ms/classe (1s pelas 470) ⟹ rotular 100k amostras ≈ minutos de Mac.
- Distribuição do UB no estrato aleatório: pico em 15–16 (consistente com opt típico ≥ 11 do piloto).

Refinamentos opcionais (não bloqueiam o go): split em 2 variáveis (4 cofatores n=3 + árvore de
mux); ABC (berkeley-abc) como 2º filtro — **exige aprovação nominal de Luiz para instalar**
(classificador bloqueou build de código externo não nomeado, corretamente).

## 3. Desenho amostral (pré-registrado)

- **Frame:** funções de n=5 uniformes (seed novo, declarado no go) → canonização NPN (7680
  transformações) → peso HT 1/|órbita| (metodologia do piloto, já validada).
- **Estratos por UB:** E1: UB ≤ 12 · E2: 13–15 · E3: 16–18 · E4: ≥ 19.
- **Alocação:** oversampling de E1 (onde opt exato é alcançável dentro do budget/classe) +
  amostra menor nos demais estratos para a cauda (censura é DADO, com rótulo "opt > k em T").
  Alocação exata definida no go em função do tamanho escolhido.
- **Budget/classe por estrato** (do piloto: decidida ≤ 10 custa mediana ~55min):
  E1: 2h · E2: 1h · E3/E4: sonda curta (k até UB−5, 30min) — números fecham no go.
- **Registro por classe:** canon_hex, |órbita|, UB_Shannon (+ split usado), opt ou censored_k,
  tempo e tamanho de CNF por k, circuito-testemunha (verificado por simulação), flags de erro.
- **Critérios de aborto:** por classe (budget acima); global (wall-clock contratado); qualquer
  UB < opt observado (invalida o filtro ⟹ para tudo, investiga).

## 4. Opções de tamanho (decisão de Luiz no go)

| Opção | Classes | Compute estimado* | Infra | Custo aprox. |
|---|---|---|---|---|
| C-mini | 2.000 | ~1.800 h-core | Mac + 1 pod 16c (~5 dias) | ~US$ 80 |
| C-médio | 10.000 | ~9.000 h-core | burst 64c (~6 dias) | ~US$ 400–600 |
| C-cheio | 30.000 | ~27.000 h-core | burst 128c (~9 dias) | ~US$ 1.2–1.8k |

*Estimativa com o mix de estratos acima e custo médio HT do piloto ajustado pelo filtro
(E1 domina o gasto exato; E3/E4 são sondas curtas). Refinar no go com a alocação final.

## 5. O que este desenho NÃO decide

1. Tamanho e data de execução — Luiz.
2. Infra (pods preemptíveis + monitor de sync 15min já validado vs VPS dedicada) — Luiz.
3. Publicação de qualquer coisa — 10_PUBLICATION_RULES, como sempre.

## 6. Pré-requisitos técnicos antes do go (baratos, sem aprovação extra)

- [ ] Encoder n=5 revalidado G3-style (n=4 completo pelas 222 é o gate natural — horas de Mac).
- [ ] UB2 (split duplo) implementado e recalibrado nas 470 (aperta E1 sem custo).
- [ ] Job queue com resume + sync (herdada do piloto, já battle-tested em 2 preempções).
