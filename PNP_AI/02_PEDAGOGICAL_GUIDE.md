# PNP-AI — 02 — GUIA PEDAGÓGICO DE P VERSUS NP

> Trilha pedagógica (FASE 2), escrita para Luiz. Regras: linguagem clara; **analogias sempre marcadas como analogias**; fórmulas acompanhadas de interpretação; perguntas de compreensão ao final de cada bloco. Este guia NÃO substitui a trilha técnica (`01_OFFICIAL_PROBLEM_SPEC.md`, `05_COMPLEXITY_FOUNDATIONS.md`).
> Fontes: SRC-0003 (Cook, doc oficial Clay), SRC-0005 (Cook 1971), SRC-0006 (Karp 1972), SRC-0007/0008 (Levin via Trakhtenbrot 1984). Escrito 2026-07-10.

---

## Bloco 1 — O que é um algoritmo e o que é "eficiente"

Um **algoritmo** é uma receita mecânica e finita: uma sequência de passos que qualquer executor (humano ou máquina) consegue seguir sem criatividade, e que sempre termina com uma resposta. O modelo matemático padrão de "executor" é a **máquina de Turing** (1936) — não porque seja realista, mas porque é simples o bastante para provar teoremas e forte o bastante para simular qualquer computador real com perda de eficiência no máximo polinomial (fato registrado no doc oficial de Cook).

O custo de um algoritmo é medido em **número de passos em função do tamanho da entrada** (n). O que importa não é o valor exato, e sim o **crescimento assintótico** — como o custo escala quando n cresce:

| Crescimento | n=10 | n=100 | n=1.000 | Veredicto |
|---|---|---|---|---|
| n | 10 | 100 | 1.000 | escala |
| n² | 100 | 10.000 | 10⁶ | escala |
| n³ | 1.000 | 10⁶ | 10⁹ | escala (com dor) |
| 2ⁿ | 1.024 | ~10³⁰ | ~10³⁰¹ | **explode** — o universo acaba antes |

**Tempo polinomial** = existe um k fixo tal que o algoritmo roda em no máximo ~n^k passos. É a definição técnica de "eficiente/viável" (a *feasibility thesis* discutida a partir de Cobham e Edmonds nos anos 1960).

> **ANALOGIA (é analogia, não definição):** polinomial é como custo que cresce de forma administrável com o tamanho do negócio; exponencial é como um passivo que dobra a cada cliente novo. Nenhum orçamento sobrevive ao segundo.

**Nuance honesta:** n¹⁰⁰ é "polinomial" mas inviável na prática. A classe polinomial é usada porque é matematicamente robusta (fechada sob composição, indiferente ao modelo de máquina), não porque todo polinômio seja rápido. Na prática, os algoritmos polinomiais que importam quase sempre têm expoente baixo.

**Perguntas de compreensão:**
1. Por que medir o crescimento em função de n, e não o tempo em segundos de um caso concreto?
2. Um algoritmo que roda em 2ⁿ passos é utilizável para n = 50? (Estime: 2⁵⁰ ≈ 10¹⁵.)

---

## Bloco 2 — Problemas de decisão e a classe P

Para comparar problemas de naturezas diferentes, tudo é padronizado como **problema de decisão**: uma pergunta de resposta SIM/NÃO sobre uma entrada codificada como string. O conjunto das entradas cuja resposta é SIM é uma **linguagem** L.

**Definição (interpretada):**
```
P = linguagens decidíveis por alguma máquina de Turing em tempo polinomial
```
*Interpretação:* P é o clube dos problemas de decisão que possuem um algoritmo eficiente que **resolve** o problema — dá a resposta certa para TODA entrada, dentro do prazo polinomial, no **pior caso**.

Exemplos em P (do doc oficial de Cook): decidir se um número é um quadrado perfeito; decidir se um número é composto (resultado que só entrou em P em 2002 — antes disso só se sabia *verificar* rapidamente).

**Pergunta de compreensão:** por que a definição exige pior caso? O que quebraria se aceitássemos "rápido na maioria das entradas"? (Dica: quem escolhe as entradas num cenário adversarial?)

---

## Bloco 3 — A classe NP: verificar ≠ resolver

Aqui mora o coração do problema. NP **não** significa "não polinomial". Significa *nondeterministic polynomial*, mas a formulação moderna (a do doc oficial) é mais intuitiva:

**Definição via verificador (interpretada):**
```
L ∈ NP  ⟺  existe verificador polinomial R e constante k tais que:
            w é SIM  ⟺  existe certificado y, com |y| ≤ |w|^k, tal que R aceita (w, y)
```
*Interpretação:* um problema está em NP se toda resposta SIM possui um **certificado curto** (tamanho polinomial) que pode ser **conferido rapidamente** (em tempo polinomial). Encontrar o certificado pode ser dificílimo; conferir é fácil.

Exemplos:
- **SAT:** dada uma fórmula booleana, existe atribuição que a torna verdadeira? Certificado = a atribuição. Conferir = avaliar a fórmula.
- **3-COLORING:** o grafo aceita pintura com 3 cores sem vizinhos iguais? Certificado = a pintura. Conferir = olhar cada aresta. (Demonstração executável real: `experiments/exp_ped_0001_3col_to_sat.py` — o solver ENCONTRA a pintura do grafo de Petersen e nosso código CONFERE o certificado em tempo linear. A assimetria encontrar/conferir, viva.)
- **Hamiltonian Path** (exemplo da página oficial do Clay): rota que visita cada cidade uma vez. Certificado = a rota.

P ⊆ NP trivialmente: quem resolve sozinho não precisa de certificado.

> **ANALOGIA (marcada):** NP é a classe dos quebra-cabeças com gabarito conferível — montar pode levar semanas; verificar que a montagem bate com a foto da caixa leva um minuto. **A pergunta P vs NP:** todo quebra-cabeça cujo gabarito se confere em um minuto também se monta em tempo razoável? A intuição quase universal diz NÃO — mas intuição não é prova, e o programa trata essa intuição como AFIRMAÇÃO NÃO ESTABELECIDA.

**A formulação oficial inteira é:** **"Does P = NP?"** (Cook, doc oficial do Clay). Só isso — e ninguém sabe a resposta.

**Perguntas de compreensão:**
1. Qual é o certificado natural para "este número N é composto"? Por que isso mostra que o problema está em NP mesmo sem saber fatorar rápido?
2. "NP = problemas exponenciais" — aponte os dois erros dessa frase.

---

## Bloco 4 — Reduções: a moeda de troca entre problemas

Uma **redução polinomial** (`L₁ ≤p L₂`) é uma tradução eficiente: uma função f computável em tempo polinomial que converte qualquer instância de L₁ numa instância de L₂ **preservando a resposta** (x é SIM em L₁ ⟺ f(x) é SIM em L₂).

*Interpretação:* se eu sei resolver L₂ rápido e sei traduzir L₁ para L₂ rápido, então sei resolver L₁ rápido. Reduções transferem facilidade para baixo e dificuldade para cima:
- L₁ ≤p L₂ e L₂ ∈ P ⟹ L₁ ∈ P (Proposition 1a do doc oficial).
- L₁ ≤p L₂ e L₁ é "difícil" ⟹ L₂ é pelo menos tão difícil.

**Exemplo executado de verdade neste projeto:** `exp_ped_0001` traduz 3-COLORING para SAT com O(|V|+|E|) cláusulas — três famílias de regras ("todo vértice tem cor", "só uma cor por vértice", "vizinhos diferem"). O solver de SAT então responde sobre coloração de grafos sem saber o que é um grafo. Isso é uma redução.

**Pergunta de compreensão:** na redução do experimento, por que a resposta UNSAT para K4 com 3 cores é uma *prova* de que K4 não é 3-colorável (e não apenas "o solver não achou")?

---

## Bloco 5 — NP-completude e o teorema de Cook–Levin

**Definição (Definition 4 do doc oficial):** L é **NP-completo** se (i) L ∈ NP e (ii) TODA linguagem de NP se reduz a L. É o problema "universal" da classe: um algoritmo polinomial para ele resolveria toda a classe de uma vez (Proposition 1c: L NP-completo ∈ P ⟹ P = NP).

**Teorema de Cook (1971) / Levin (independente):** SAT é NP-completo.
Ideia da prova (Cook 1971, SRC-0005 — reconstrução completa na FASE 3): a computação de qualquer verificador polinomial pode ser descrita, passo a passo, por uma fórmula booleana de tamanho polinomial — "a máquina aceita (w,y) em tempo t" vira "esta fórmula é satisfatível". A fórmula simula a máquina.

**Karp (1972, SRC-0006):** mostrou que a dificuldade de SAT se espalha — 21 problemas naturais (CLIQUE, KNAPSACK, CHROMATIC NUMBER, PARTITION, MAX CUT...) são todos NP-completos, via cadeias de reduções. Consequência estrutural: **milhares de problemas práticos de logística, alocação, design e otimização são, no fundo, o MESMO problema** — resolver um rápido resolve todos.

**Levin, lado soviético (SRC-0007/0008 — verificado no survey de Trakhtenbrot):** trabalhando na URSS, Levin obteve resultados análogos em 1971 (publicados em 1973), com o nome "universal search problems" (*universal'nye perebornye zadachi*) e 6 problemas universais. A escola soviética estudava *perebor* (busca exaustiva) desde os anos 1950; na conferência de Tsakhkadzor (março/1973, 70 anos de Kolmogorov), a audiência ainda não conhecia os trabalhos de Cook e Karp.

**Perguntas de compreensão:**
1. Por que basta UM problema NP-completo em P para colapsar P = NP?
2. Se alguém provar que CLIQUE exige tempo exponencial, o que segue para P vs NP? E se provar que CLIQUE ∈ P?

---

## Bloco 6 — Circuitos, uniformidade e o pior caso

**Circuitos booleanos:** um circuito com portas AND/OR/NOT computa uma função de exatamente n bits. Uma **família de circuitos** {Cₙ} tem um circuito por tamanho de entrada — computação **não uniforme**: não há um único algoritmo, e sim infinitos "projetos de hardware", possivelmente sem padrão entre eles.

Por que importa (doc oficial, §3): provar que um problema NP-completo exige circuitos de tamanho superpolinomial provaria P ≠ NP. E o estado da arte é humilhante: o melhor lower bound conhecido para um problema de NP em circuitos gerais é **~4n — linear** (registrado no doc oficial). A distância entre "4n" e "superpolinomial" é a medida honesta da dificuldade.

**Uniformidade — armadilha de auditoria nº 1 deste projeto:** a definição de P exige UMA máquina para todos os tamanhos. Um "algoritmo" diferente para cada n, uma tabela pré-computada gigante ou pesos de rede neural treinados com custo exponencial podem ser não uniformes ou esconder custo — e não provam nada sobre P. Ver `00_PNP_CHARTER.md`, confusões proibidas.

**Pior caso vs caso médio — armadilha nº 2:** P vs NP é sobre PIOR caso. SAT solvers modernos (como o Glucose que instalamos) resolvem instâncias industriais enormes rotineiramente — e isso não move o problema um milímetro, porque a afirmação exigida é sobre TODAS as instâncias. "Funciona quase sempre" e "funciona sempre" são mundos matemáticos diferentes.

**Perguntas de compreensão:**
1. Por que uma rede neural que acerta 99,9% das instâncias de SAT não diz nada sobre P vs NP?
2. O que uma família de circuitos pode "saber" que um algoritmo uniforme não pode?

---

## Bloco 7 — Por que é tão difícil (prévia das barreiras — FASE 4)

Três gerações de técnicas bateram em muros **provados**:
1. **Relativization** (Baker–Gill–Solovay; citada no doc oficial): diagonalização e redução continuam valendo com oráculos, mas existe oráculo A com P^A = NP^A — logo essas técnicas sozinhas não separam P de NP.
2. **Natural proofs** (Razborov–Rudich; citada no doc oficial): os métodos conhecidos de circuit lower bounds são "naturais", e provas naturais de lower bounds gerais destruiriam geradores pseudoaleatórios que se acredita existirem — o doc oficial nota que dariam até um algoritmo de fatoração melhor que os conhecidos.
3. **Algebrization** (Aaronson–Wigderson, 2008 — fora do doc de Cook; fonte própria será registrada na FASE 4): fecha a rota de técnicas algébricas que escapavam das duas primeiras.

Não é que faltaram boas ideias em 50+ anos — é que as boas ideias foram *provadas insuficientes*, o que é conhecimento real. O mapa dessas barreiras (FASE 4) é o filtro pelo qual qualquer proposta deste projeto terá de passar.

---

## Síntese em uma frase (simplificação, não enunciado técnico)

P vs NP pergunta se a criatividade de ENCONTRAR soluções pode sempre ser mecanizada tão eficientemente quanto a rotina de CONFERI-las — e a resposta, seja qual for, tem de valer para todas as entradas, todos os tamanhos, com um único algoritmo, superando as barreiras conhecidas.

## Onde conferir as respostas

As perguntas de compreensão devem ser discutidas em sessão (formato do programa) e conferidas contra a trilha técnica: Blocos 1–3 → `01_OFFICIAL_PROBLEM_SPEC.md` §2; Blocos 4–5 → §3 e SRC-0005/0006; Bloco 6 → §5 e charter; Bloco 7 → `07_BARRIER_MAP.md` (FASE 4).
