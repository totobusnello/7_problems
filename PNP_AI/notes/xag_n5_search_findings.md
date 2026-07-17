# Busca n=5 por um separador do unit-gap em XAG — findings

> **Status interno:** entrega fechada (2026-07-15). Ataca a **Open Question #1** da
> `technote_unitgap_basedep.md` §7 ("gap_XAG permanece em {0,1} em n=5, ou aparece um separador
> não-linear?"). Resultado: **amostral, não exaustivo** — zero separadores em ~29,6 mil funções de
> 5 variáveis. Evidência a favor da conjectura, não prova. Este bloco e as referências internas saem
> de qualquer versão pública. Publicação/preprint SOMENTE com autorização de Luiz (10_PUBLICATION_RULES).
>
> **Correção 2026-07-17 (pós REV-0015..0018):** `29.643`/`29,6 mil` abaixo é contagem de LINHAS; após
> dedup cross-worker são **25.373 tt distintas** (4.270 duplicatas; dist gap0 24.875 / gap1 294 /
> inconclusive 204 / **separadores 0** — `search_n5_dedup.csv`). O veredito (0 separadores) é mantido.
> A frase "cada resultado verificado por simulação" era imprecisa (a busca rodou verify=False):
> 494/494 (294 gap1 + 200 gap0) re-decodificadas e simuladas depois (`verify_n5_recheck.py`, 0
> divergências). Wording de probabilidade ("viés pró-separador", "near zero") rebaixado. Números
> corretos e wording final na **v1 do paper** (`../drafts/paper1_unitgap_basedep_v1.md`).

## Pergunta

Em n ≤ 4, `gap_XAG(f) = tree_XAG(f) − opt_XAG(f) ∈ {0,1}` (censo exaustivo, technote §4). Em XAG
**não** vale a decomposição trivial `f = 1∧f` que força `gap ≤ 1` no AIG, então `gap ≥ 2` é possível
a priori em n=5. Um **separador** (função com `gap_XAG ≥ 2`) refinaria a base-dependência; a
**ausência** numa amostra grande é evidência a favor de a propriedade unit-gap se estender ao XAG.

Exaustar n=5 é inviável (2³² ≈ 4,3 bilhões de tabelas-verdade; centenas de milhões de classes NPN)
— ao contrário de n ≤ 4, onde o censo é completo. Logo a busca é **amostragem dirigida**, não prova.

## Método

Por candidato (circuito XAG aleatório → tabela-verdade `tt` de 5 variáveis):

1. filtro de essencialidade — `f` depende das 5 variáveis (senão reduz a n < 5, já coberto);
2. `opt_XAG(f)` por SAT (busca ascendente k=1,2,…, kissat 4.0.4, cap 20 s), modelo SAT
   verificado por simulação;
3. `tree_XAG(f)` por SAT em **modo formula** (fan-out 1 em toda porta interna, sem dedup — computa
   formula-size, não DAG), busca **ascendente a partir de opt** (cap 20 s);
4. `gap = tree − opt`. `gap ≥ 2` ⟹ **separador** (candidato, sempre re-verificado). Timeout em
   qualquer etapa ⟹ **inconclusive** (não decidido, não separador).

**Geração dos candidatos:** circuitos XAG aleatórios com viés de sharing/reconvergência (reuso de
gates) e viés XOR (estrutura não-linear), `opt` baixo (SAT viável). Isso concentra a amostra
justamente onde um separador não-linear seria mais provável — funções de opt baixo com estrutura
não-linear rica — mas **não cobre o espaço todo**. Seeds determinísticos por worker
(`Random(90210 + wid)`), dedup por `tt`, 2 workers em paralelo.

**Encoder de formula validado antes da busca** pelo gate `gate_xag_tree.py` (G-T1/G-T2/G-T3):
- G-T1: `opt_via_sat` bate com o censo XAG em 222/222 classes de n=4 (o flag `formula` não quebrou o DAG);
- G-T2: n=3 completo, `tree_via_sat == opt` para as 256 funções (gap_XAG n=3 = 0);
- G-T3: n=4, `tree_via_sat == tree_xag_n4.npy` (DP independente) em 222/222 classes, cobrindo as
  **4 classes com gap=1** (não só gap=0) — o encoder DETECTA formula > opt. **PASSOU.**

**Falso positivo corrigido antes desta coleta:** a 1ª versão testava `solve_k(formula, opt+1)`
isolado e reportava parity-5 (`0x69969669` etc — linear, gap 0) como separador; UNSAT em opt+1 só
diz "não há formula de exatamente opt+1 gates", não `tree ≥ opt+2`. Corrigido para busca ascendente
a partir de opt (o primeiro k SAT é `tree`); parity-5 reconfirmado gap 0.

## Resultado

**29.643 funções de 5 variáveis** (essenciais em todas as 5, opt baixo), 2 workers, ~20 h de wall-clock:

| Veredicto | Funções | % |
|---|---:|---:|
| gap 0 | 29.143 | 98,31 |
| gap 1 | 296 | 1,00 |
| inconclusive (timeout SAT) | 204 | 0,69 |
| **separador (gap ≥ 2)** | **0** | **0** |

**Zero separadores.** Toda função *decidida* caiu em `gap ∈ {0,1}`. Os 204 inconclusive são
timeouts (opt exige k alto, ou a formula não fechou em ≤ 20 s) — cauda aberta, não separadores.

## Leitura (com o hedge correto)

- **Evidência amostral a favor** de `gap_XAG ∈ {0,1}` também em n=5: nas ~29,6 mil funções testadas
  — escolhidas com viés *pró-separador* (opt baixo, estrutura não-linear) — o sharing compra no
  máximo 1 gate. Reforça (não prova) a base-dependência da technote: o "unit gap" que é **falso** no
  AIG **resiste empiricamente** no XAG, agora até n=5.
- **Não fecha a Open Question #1.** Exaustão de n=5 é inviável; um separador pode existir fora da
  amostra (opt alto, ou fora do viés de geração). O que a coleta faz é **rebaixar a probabilidade
  subjetiva** de um separador de opt baixo — o alvo mais provável — a ~0 nas ~29,6 mil tentativas.
- Coerente com a §4 da technote ("parity não separa mais em XAG, mas nada aqui exclui outros
  separadores"): não achamos outro separador na faixa de opt baixo.

## Reprodutibilidade

- Código: `../experiments/exp_xag_n4/search_n5.py` (busca), `xag_exact.py` (encoder, flag
  `formula=True`), `gate_xag_tree.py` (gate G-T do encoder de formula).
- Artefatos: `search_n5_w00.csv`, `search_n5_w01.csv` (uma linha por função:
  `tt, opt, tree, gap, verdict, t_sec`).
- Solver: kissat 4.0.4. Bancada: VPS Hostinger 2 vCPU (always-on). Seeds: `Random(90210 + wid)`,
  determinístico por worker.

## Aberto / próximo

- **Não é exaustão.** Um separador de opt alto (fora do alcance do cap SAT de 20 s) ou fora do viés
  de geração continua possível. Estender exigiria cap SAT maior + mais cores, com retorno decrescente.
- Alimenta a Open Question #1 da technote (agora com evidência amostral n=5) e a §4 (base-dependência).
- Open Question #2 (technote §7) — um teorema por trás do unit gap empírico em XAG (normal form
  limitando sharing quando a estrutura linear é fatorada) — segue como o caminho *dedutivo*; a busca
  n=5 é o lado *empírico*.
