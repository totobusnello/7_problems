# PNP-AI — 07 — BARRIER MAP

> Barreiras conhecidas a provas de lower bounds: relativization (Baker–Gill–Solovay), natural proofs (Razborov–Rudich), algebrization (Aaronson–Wigderson).
> Conteúdo técnico completo: FASE 4 (fontes primárias a processar). O protocolo de triagem abaixo já está EM VIGOR desde 2026-07-10.

## PROTOCOLO DE TRIAGEM ANTI-BARREIRA (oficial desde 2026-07-10)

> Origem: formulado por Luiz na Sessão Pedagógica 2 (Q10). Toda proposta de abordagem, lema ou linha de ataque gerada pelo programa DEVE responder, por escrito, ANTES de ser tratada como promissora:

1. **O argumento relativiza?** (Sobrevive à adição de um oráculo arbitrário? Então não separa P de NP.)
2. **Ele se encaixa no formato de natural proof?** (Propriedade ampla + construtiva + útil contra circuitos gerais? Então colide com PRGs.)
3. **Ele algebriza?** (Continua válido em mundos aritmetizados/com extensões de oráculo? Então não basta.)
4. **Qual parte concreta rompe a barreira?** (Apontar o passo específico não-relativizante / não-natural / não-algebrizante.)
5. **Essa ruptura já é conhecida?** (Buscar precedentes — técnicas não-relativizantes existem e são catalogadas.)
6. **O argumento apenas redescreve uma técnica bloqueada com linguagem nova?** (Teste de honestidade contra rebranding.)

Proposta sem respostas a 1–6 → estado máximo permitido: `HEURISTIC`. O REVISOR ADVERSARIAL usa este checklist como roteiro.

## As três barreiras (resumo preliminar — detalhamento na FASE 4)

| Barreira | Resultado central | O que bloqueia | Status de fonte |
|---|---|---|---|
| **Relativization** (Baker–Gill–Solovay) | ∃ oráculo A com P^A = NP^A (✅ citado em SRC-0003); ∃ oráculo B com P^B ≠ NP^B (⚠️ literatura padrão, fonte a processar) — logo técnicas que relativizam dão a mesma conclusão em mundos com respostas opostas | Diagonalização e simulação puras | Parcial (SRC-0003); paper original: FASE 4 |
| **Natural proofs** (Razborov–Rudich) | Propriedades "naturais" (⚠️ amplas + construtivas + úteis — tríade da literatura, fonte a processar) contra circuitos gerais quebrariam PRGs fortes; o doc oficial nota: dariam algoritmo de fatoração melhor que os conhecidos (✅ SRC-0003) | A família inteira dos métodos conhecidos de circuit lower bounds | Parcial (SRC-0003); paper original: FASE 4 |
| **Algebrization** (Aaronson–Wigderson 2008) | Técnicas algébricas/aritmetização que estendem oráculos algebricamente também não separam P de NP | A geração pós-relativization (provas interativas etc.) | ⚠️ Fora de SRC-0003; fonte própria: FASE 4 |

## O que se sabe escapar (a mapear na FASE 4)

Resultados não-relativizantes existem (o doc oficial menciona a existência; catálogo com fontes na FASE 4) — candidatos conhecidos da literatura: aritmetização em provas interativas, lower bounds por diagonalização indireta, GCT, hardness magnification, meta-complexidade. Cada um entrará aqui com fonte primária e análise de qual barreira evita e qual não.

## Leitura estratégica

As barreiras NÃO dizem que P vs NP é insolúvel — dizem que famílias específicas de técnicas são demonstravelmente insuficientes. São o filtro de qualidade mais barato do programa: matar uma ideia bloqueada em 1 hora de triagem vale mais que 3 meses desenvolvendo-a.
