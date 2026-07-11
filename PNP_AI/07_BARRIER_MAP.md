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

## Barreira 1 — Relativization (Baker–Gill–Solovay 1975)

**Resultado [FONTE: SRC-0017 (survey de Fortnow), conferido no texto; primária SIAM = SRC-0014 A OBTER]:** o paper original de BGS constrói um mundo relativizado onde P = NP **e outro onde P ≠ NP**, e observa que essencialmente todas as técnicas de complexidade da época relativizam — concluindo que as técnicas correntes não resolveriam a questão. (Confirma e completa o que SRC-0003 citava só pela metade do oráculo A.)

**Mecânica:** uma técnica *relativiza* se a prova continua válida quando todas as máquinas ganham acesso ao mesmo oráculo arbitrário. Diagonalização e simulação — as armas da hierarquia de tempo (nossos §6 de `05_COMPLEXITY_FOUNDATIONS.md`) — relativizam. Como existem oráculos A (P^A = NP^A) e B (P^B ≠ NP^B), qualquer prova relativizante de qualquer um dos lados geraria contradição num dos dois mundos.

**O que bloqueia:** diagonalização pura, simulação, argumentos "caixa-preta" sobre máquinas.
**O que escapou:** os resultados de provas interativas dos anos 1990 (IP = PSPACE e afins) não relativizam [FONTE: SRC-0017, que os aponta como A exceção histórica] — via **aritmetização** (converter fórmulas booleanas em polinômios). Foi exatamente essa rota que motivou a Barreira 3.

## Barreira 2 — Natural Proofs (Razborov–Rudich, JCSS 1997)

**A tríade [FONTE: SRC-0015, verbatim]:** uma propriedade combinatória Cₙ de funções booleanas é *natural* se satisfaz:
- **Constructivity:** decidir "fₙ ∈ Cₙ?" está em P no tamanho da truth table de fₙ;
- **Largeness:** |Cₙ| ≥ 2^(−O(n))·|Fₙ| — a propriedade vale para fração não desprezível de TODAS as funções;
e é *useful* contra P/poly se toda sequência fₙ ∈ Cₙ exige circuitos superpolinomiais.

**Teorema central [FONTE: SRC-0015, Theorem 4.1, verbatim]:** não existe prova de lower bound P/poly-natural contra P/poly, a menos que TODO gerador pseudoaleatório em P/poly tenha dureza **no máximo** 2^(k^o(1)) — isto é, a menos que todos os PRGs sejam fracos. Contrapositiva operacional (o "In particular" do paper): **se existem** funções 2^(n^ε)-difíceis (PRGs fortes), **então não existe** prova P/poly-natural contra P/poly. [Redação precisada após REV-0002/Kimi flagar ambiguidade — o "no máximo" estava implícito e podia inverter a leitura.]

**Mecânica (autodestruição):** uma propriedade natural útil contra P/poly seria um DISTINGUIDOR eficiente entre funções aleatórias (que têm a propriedade, por largeness) e funções pseudoaleatórias (que não têm, por usefulness — PRGs vivem em P/poly). Ou seja: a prova de que "circuitos são fracos" forneceria um algoritmo que quebra os geradores construídos a partir dessa mesma dureza. Exemplo concreto do paper: não há prova natural de que o logaritmo discreto exige circuitos exponenciais [FONTE: SRC-0015].

**O que bloqueia:** os métodos de circuit lower bounds dos anos 1980 (o paper mostra que todos se encaixam no molde natural).
**O que escapa:** provas que violem constructivity (propriedades difíceis de decidir) ou largeness (propriedades "raras", sob medida para UMA função) — e argumentos de contagem/diagonalização, que o próprio paper discute como presumivelmente não naturais.

## Barreira 3 — Algebrization (Aaronson–Wigderson, STOC 2008 / TOCT 2009)

**Ideia [FONTE: SRC-0016, abstract verbatim]:** ao relativizar uma inclusão de classes, dar à máquina simuladora acesso não só ao oráculo A, mas a uma **extensão de baixo grau Ã de A sobre corpo/anel finito**. Uma separação C ⊄ D *algebriza* se C^Ã ⊄ D^A para todos A, Ã — com a assimetria (um lado booleano, outro algébrico) essencial à definição.

**Resultados [FONTE: SRC-0016]:** (i) os resultados não-relativizantes conhecidos baseados em aritmetização (a rota IP = PSPACE) **algebrizam**; (ii) resolver P vs NP — em qualquer direção — exige técnicas **não-algebrizantes**. Ou seja: a porta de saída da Barreira 1 foi mapeada e também tem um muro.

**Nuance importante [FONTE: SRC-0016, abstract]:** já existem circuit lower bounds que superam relativization E natural proofs **simultaneamente** (ex.: PP sem circuitos lineares) — as barreiras são específicas por técnica, não um bloqueio universal. O jogo é saber exatamente qual propriedade da computação "do mundo real" cada abordagem explora.

## Síntese operacional

| Barreira | Mata | Porta de escape conhecida |
|---|---|---|
| Relativization | diagonalização/simulação caixa-preta | aritmetização (mas ver Barreira 3); propriedades específicas do mundo não relativizado |
| Natural proofs | lower bounds via propriedades amplas+construtivas | propriedades raras ou não construtivas; contagem; abordagens via meta-complexidade |
| Algebrization | aritmetização estendida | técnicas que exploram estrutura além de extensões de baixo grau (fronteira ativa: GCT, hardness magnification, meta-complexidade — mapear em `08_RESEARCH_FRONTIERS.md`, **ainda stub, entregável pendente**) |

## Leitura estratégica

As barreiras NÃO dizem que P vs NP é insolúvel — dizem que famílias específicas de técnicas são demonstravelmente insuficientes, e cada uma foi descoberta ANALISANDO por que uma geração de ataques falhou. São o filtro de qualidade mais barato do programa: matar uma ideia bloqueada em 1 hora de triagem vale mais que 3 meses desenvolvendo-a. O protocolo de 6 perguntas acima é a aplicação prática deste mapa.
