# PNP-AI — 14_OPEN_QUESTIONS

> Propósito: Perguntas abertas do projeto (não do campo) — o que ainda não sabemos responder.
> Fase de preenchimento: contínuo · Estado: PREENCHIDO (primeira leva 2026-07-15)

## Técnicas (linha Unit Gap / base-dependência)

**OQ-1 — `gap_XAG` permanece em {0,1} além de n=4?**
Status: em n ≤ 4, SIM (censo exaustivo, claim 0028). Em **n=5**, busca amostral de 29.643 funções
(viés pró-separador) achou **0 separadores** (claim 0030) — evidência a favor, **não prova**
(exaustão de n=5 é inviável: 2³² tabelas-verdade). Continua aberto: (a) exaustão de n=5 (exigiria
enumeração NPN + muito mais cores); (b) um separador de **opt alto** (fora do cap SAT de 20 s da
busca); (c) n ≥ 6. Parity deixou de separar em XAG, mas nada exclui outro separador.

**OQ-2 — Há um teorema por trás do Unit Gap empírico em XAG?**
Um argumento de normal form que limite o sharing quando a estrutura linear é fatorada (a intuição:
em AIG o gap é o custo de duplicar paridade; XAG absorve isso na porta XOR). Este é o caminho
**dedutivo**; a busca n=5 é o lado **empírico**. Aberto.

**OQ-3 — `tree_MIG`: um DP exato eficiente (a coluna gap do MIG).**
O DP ternário ingênuo é O(N³) em tamanhos de conjunto — deferido no censo MIG (claim 0029). Fechar
daria a base-dependência nas 3 bases, não só AIG/XAG. Aberto.

**OQ-4 — Formulação base-relativa corrigida do Teorema 7 do Krinkin, com prova.**
O Thm 7 dele perde a prova (depende do Cor. 6 refutado) e sua leitura universal é falsa (⊕₃); o
enunciado condicional sob a definição padrão fica SEM PROVA, não refutado (claim 0025). Um enunciado
correto e base-relativo, com prova, é trabalho aberto.

## Operacionais / de governança

**OQ-5 — Resposta do Krinkin à issue `krinkin/unit-gap#1`.**
Enviada 2026-07-11; **sem resposta e sem reação** até 2026-07-15 (~4 dias). Governa o **timing** da
publicação: decisão de Luiz é esperar a janela de resposta antes de submeter o preprint, redigindo em
paralelo. Réplica ou novo contato exige novo OK. "Não vamos ter 2 chances."

**OQ-6 — Cauda do lote 3-out do Alvo C (Simplifier), 83% não auditada.**
Parqueada por ROI decrescente (cauda k-alto UNSAT-hard). Fecho de engenharia declarado (nota do Alvo
C), não exaustão. Reabrir exigiria mais cores + cap menor.

## Estratégicas (Seven Summits)

**OQ-7 — Qual o Cume 2 (próximo Problema do Milênio com rota auditável)?**
Após o paper 1 (P=NP / Unit Gap). Candidatos com auditabilidade alta no charter da AUDIT TRACK:
Navier-Stokes (alvo-rico em "provas" erradas + conexão Barbara Busnello) e RH. Requer OK de Luiz
para iniciar — nada executa sem aprovação.
