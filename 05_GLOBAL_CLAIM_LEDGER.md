# 05 — GLOBAL CLAIM LEDGER — Índice de afirmações de todos os projetos

> Formato de ID: `7P-[PROBLEM]-CLM-[NUMBER]` (ex.: 7P-PNP-CLM-0001, 7P-NS-CLM-0001).
> A concordância de modelos NÃO altera automaticamente o estado de um claim.
> Ledgers detalhados vivem em cada projeto (ex.: `PNP_AI/10_PNP_CLAIM_LEDGER.md`); este arquivo é o índice global.

## Estados permitidos

`SOURCE_VERIFIED` · `FORMULATION_VERIFIED` · `CONJECTURE` · `HEURISTIC` · `COMPUTATIONALLY_TESTED` · `FINITE_SCOPE_VERIFIED` · `DERIVED_CHECKED` · `FORMALLY_VERIFIED` · `GAP_FOUND` · `REFUTED` · `DUPLICATES_KNOWN_RESULT` · `NOVELTY_UNCLEAR` · `HUMAN_REVIEW_REQUIRED` · `BLOCKED`

## Campos obrigatórios de cada claim

Enunciado · problema · área · definições · hipóteses · quantificadores · conclusão · origem · referências · dependências · prova/derivação · complexidade alegada · testes computacionais · custos ocultos possíveis · casos extremos · críticas · revisões externas · formalização · análise de novidade · próximo passo · estado.

## Índice global

| Claim ID | Projeto | Enunciado (resumo) | Estado | Última atualização |
|---|---|---|---|---|
| 7P-NS-CLM-0001 | NS_PROB | Hipótese probabilística de cancelamentos (ver `NS_PROB/00_NS_STATUS.md`) | CONJECTURE (hipótese preservada do NS-PROB; não é frente de execução atual) | 2026-07-10 |
| 7P-PNP-CLM-0001 | PNP_AI | Formulação oficial: "Does P = NP?" | SOURCE_VERIFIED | 2026-07-10 |
| 7P-PNP-CLM-0002 | PNP_AI | Definição de P (TM, tempo polinomial de pior caso) | FORMULATION_VERIFIED | 2026-07-10 |
| 7P-PNP-CLM-0003 | PNP_AI | Definição de NP via checking relations | FORMULATION_VERIFIED | 2026-07-10 |
| 7P-PNP-CLM-0004 | PNP_AI | ≤p (f poly-time) e NP-completude | FORMULATION_VERIFIED | 2026-07-10 |
| 7P-PNP-CLM-0005 | PNP_AI | Proposition 1 (a–c) do doc oficial | SOURCE_VERIFIED | 2026-07-10 |
| 7P-PNP-CLM-0006 | PNP_AI | SAT/3-SAT NP-completos (Cook/Levin/Karp) | SOURCE_VERIFIED (provas originais pendentes) | 2026-07-10 |
| 7P-PNP-CLM-0007 | PNP_AI | Critérios exatos de solução (matemáticos + regras Clay 2018) | SOURCE_VERIFIED | 2026-07-10 |

Detalhes dos claims PNP em `PNP_AI/10_PNP_CLAIM_LEDGER.md`.

## Pacote de revisão externa (formato obrigatório, sem linguagem promocional)

```
Claim ID: / Problema: / Área:
Enunciado exato: / Definições: / Hipóteses: / Conclusão:
Dependências aceitas: / Prova ou algoritmo proposto: / Complexidade alegada:
Pontos de incerteza: / Testes já realizados: / Referências relacionadas:
```

Instrução ao revisor: "Analise o pacote como árbitro matemático adversarial. Não presuma que o enunciado, o algoritmo ou a prova estejam corretos. Identifique a primeira etapa falsa, circular ou insuficientemente justificada. Verifique hipóteses, quantificadores, uniformidade, complexidade assintótica, custos ocultos, casos extremos e dependências. Procure contraexemplos e precedentes. Não valide por plausibilidade ou consenso."

Formato da revisão: Veredito · Primeira etapa problemática · Explicação técnica · Hipótese ausente · Contraexemplo/teste · Resultado conhecido relacionado · Correção mínima · Confiança.
