# 08 — NOVELTY PROTOCOL — Avaliação de novidade

> Princípio: ausência de resultados numa busca bibliográfica NÃO prova novidade. Somente especialistas humanos + revisão bibliográfica extensa sustentam uma alegação de novidade.

## Classificações

`JÁ CONHECIDO` · `PRECEDENTE PRÓXIMO ENCONTRADO` · `POSSIVELMENTE NOVO, BUSCA INCOMPLETA` · `NOVIDADE PLAUSÍVEL, REVISÃO PENDENTE` · `FALSO` · `INCONCLUSIVO`

## Procedimento (por claim estabilizado)

1. **Decompor** o claim em componentes pesquisáveis (definições, técnica, enunciado, corolários).
2. **Buscar em camadas:** arXiv (cs.CC, math.*) → surveys reconhecidos → Complexity Zoo / literatura padrão da área → busca semântica de papers (citation graph) → busca web geral.
3. **Registrar cada busca:** query exata, base consultada, data, resultados relevantes, resultado negativo também conta.
4. **Comparar com precedentes:** se técnica ou enunciado próximo existir, registrar a diferença exata (hipóteses, quantificadores, regime de parâmetros).
5. **Classificar** com uma das seis categorias — nunca acima de `NOVIDADE PLAUSÍVEL, REVISÃO PENDENTE` sem revisão humana especializada.
6. **Revisão externa:** enviar claim package a ≥1 modelo de família distinta com papel REVISOR BIBLIOGRÁFICO antes de subir a classificação.
7. **Gate humano:** classificação final de novidade só com parecer de especialista humano (protocolo em `09_HUMAN_REVIEW_PROTOCOL.md`).

## Registro

Cada avaliação vive no claim ledger do projeto, campo "análise de novidade", com histórico de buscas anexado.
