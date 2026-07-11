# PNP-AI — 01 — OFFICIAL PROBLEM SPEC

> **PRIMEIRA TAREFA EXECUTÁVEL — EXECUTADA em 2026-07-10** (autorizada por Luiz).
> Fonte primária: Stephen Cook, *"The P versus NP Problem"* — descrição oficial do Clay Mathematics Institute, 12 pp.
> PDF: https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf (baixado e parseado localmente; trechos conferidos verbatim via pypdf — registrado como SRC-0003).
> Método: toda definição abaixo foi conferida contra o texto extraído do PDF, não contra memória de modelo.

---

## 1. Formulação oficial — FATO VERIFICADO

O documento oficial enuncia (Seção 1, "Problem Statement"):

> "Does P = NP?"

Observações do próprio documento, conferidas no texto:
- A resposta independe do tamanho do alfabeto Σ (assume-se |Σ| ≥ 2), pois strings sobre qualquer alfabeto fixo são codificáveis eficientemente em binário.
- Caso unário (|Σ| = 1): o documento registra que o problema permanece aberto nesse caso, e que é possível P = NP valer no caso unário sem valer no geral.
- P ⊆ NP é trivial (todo L ∈ P admite checking relation que ignora o certificado).
- Estrutura do documento: §1 Statement of the Problem · §2 History and Importance · §3 The Conjecture and Attempts to Prove It · Appendix (definição de máquina de Turing).

**Claim:** `7P-PNP-CLM-0001` (SOURCE_VERIFIED).

---

## 2. Definições mínimas (conforme o documento oficial) — FORMULATION_VERIFIED

Modelo de computação: **máquina de Turing** (Turing 1936), definida formalmente no apêndice do documento. O documento observa que P é robusta: modelos razoáveis (multi-fita, RAM) simulam-se mutuamente com overhead polinomial (quadrático/cúbico).

**Linguagem.** Σ alfabeto finito com |Σ| ≥ 2; Σ* o conjunto de strings finitas sobre Σ; uma linguagem é L ⊆ Σ*. Problemas de decisão são codificados como linguagens (conjunto das strings que codificam instâncias YES).

**Tempo polinomial.** Para uma TM M que para em toda entrada, T_M(n) = pior caso do número de passos sobre entradas de comprimento n. M roda em tempo polinomial se existe k tal que T_M(n) ≤ n^k + k para todo n.

**Classe P.**
```
P = { L : L = L(M) para alguma TM M que roda em tempo polinomial }
```

**Checking relation e classe NP.** Uma checking relation é uma relação binária R ⊆ Σ* × Σ₁* (alfabetos finitos Σ, Σ₁). Associa-se a R a linguagem
```
L_R = { w#y : R(w, y) }        (# ∉ Σ)
```
R é polynomial-time sse L_R ∈ P. Então:
```
L ∈ NP  ⟺  existem k ∈ ℕ e checking relation R polynomial-time tais que,
            para todo w ∈ Σ*:   w ∈ L ⟺ ∃y ( |y| ≤ |w|^k  e  R(w, y) )
```
Terminologia: y é o **certificado** (witness); o algoritmo de L_R é o **verificador**.

**Redução polinomial (Definition 3 do documento, conferida verbatim).**
```
L₁ ≤p L₂  ⟺  existe f : Σ₁* → Σ₂* computável em TEMPO POLINOMIAL
              tal que  x ∈ L₁ ⟺ f(x) ∈ L₂ , para todo x ∈ Σ₁*
```
(Análogo polinomial da many-one reducibility ≤m da computabilidade — Definition 1 do documento, onde f é apenas computável. O qualificador *polynomial-time computable* em ≤p foi conferido no texto exato; uma extração automática anterior o havia omitido — ver RESEARCH_LOG.)

**NP-completude (Definition 4, conferida verbatim).**
```
L é NP-completo  ⟺  L ∈ NP  e  L' ≤p L para toda L' ∈ NP
```

**Proposition 1 do documento (conferida):**
(a) L₁ ≤p L₂ e L₂ ∈ P ⟹ L₁ ∈ P.
(b) L₁ NP-completo, L₂ ∈ NP, L₁ ≤p L₂ ⟹ L₂ NP-completo.
(c) **L NP-completo e L ∈ P ⟹ P = NP.**

**Uniformidade.** A definição de P exige UMA máquina M que funcione para todas as entradas de todos os tamanhos. Famílias de circuitos (um circuito por tamanho de entrada) definem classes não uniformes (ex.: P/poly) — distinção central para auditar algoritmos candidatos (ver `00_PNP_CHARTER.md`, confusões proibidas).

**Claims:** `7P-PNP-CLM-0002..0005`.

---

## 3. Equivalências fundamentais — RESULTADO CONHECIDO

1. **NP via verificadores ≡ NP via máquinas não determinísticas.** O documento define NP por checking relations e registra que essa é a formulação hoje usual, equivalente à original por NTMs ("NP" = nondeterministic polynomial time). Reconstrução técnica da equivalência: FASE 3.
2. **SAT é NP-completo (Cook 1971; Levin 1973 independentemente).** Conferido no documento: Satisfiability (dado F proposicional, decidir se F é satisfatível) está em NP (certificado = atribuição verdadeira) e foi provado NP-completo na ref. [9] do documento (Cook, 1971 — via análogo polinomial de Turing reducibility). Karp (1972, ref. [21]) provou 20 problemas naturais NP-completos, introduziu a notação P/NP e a definição de NP-completude via ≤p que se tornou padrão. Levin (ref. [23]) definiu independentemente "universal search problems" com seis exemplos, incluindo Satisfiability. 3-SAT também é NP-completo (documento, com definição própria).
3. **Consequência operacional (Prop. 1c):** para provar P = NP basta um algoritmo polinomial correto para UM problema NP-completo qualquer.

**Claim:** `7P-PNP-CLM-0006`.

## 4. Formulações adequadas a pesquisa assistida por IA — DERIVAÇÃO DO PROJETO

- **Via SAT/3-SAT:** conecta diretamente com SAT solvers (z3, pysat instalados) — geração de instâncias, testes exatos de algoritmos candidatos, contraexemplos automáticos.
- **Via circuitos booleanos:** P ≠ NP seguiria de lower bound superpolinomial no tamanho de circuitos para um problema NP-completo (caminho apontado pelo próprio documento; NP ⊄ P/poly ⟹ P ≠ NP). Objetos finitos e enumeráveis — compatível com busca automatizada em pequena escala.
- **Via verificadores:** a definição por checking relations é a mais direta para formalização (Lean/Mathlib) por evitar não determinismo primitivo.

## 5. Critérios exatos que uma solução teria de satisfazer

### Matemáticos (do documento oficial — FATO VERIFICADO)
**Para P = NP:** exibir algoritmo de tempo polinomial para um problema NP-completo (ex.: 3-SAT), com: correção para TODAS as entradas; UMA máquina uniforme; bound polinomial demonstrado no pior caso. Auditoria obrigatória: constantes dependentes de n, pré-computação escondida, não uniformidade, tabelas exponenciais (charter, confusões proibidas).
**Para P ≠ NP:** limitação universal — nenhuma TM polinomial decide o problema. O documento registra as barreiras verificadas no texto:
- *Relativization:* lower bounds por diagonalização+redução relativizam; existe oráculo A com P^A = NP^A (ref. [3] do documento = Baker–Gill–Solovay), logo essas técnicas não separam P de NP.
- *Natural proofs* (Razborov–Rudich, ref. [27]): os métodos conhecidos de circuit lower bounds são "naturais" e, assumindo geradores pseudoaleatórios fortes, não podem provar lower bounds gerais; o documento nota que uma natural proof de lower bound geral daria um algoritmo de fatoração melhor que os conhecidos.
- Melhor lower bound de circuitos para problema em NP registrado no documento: ~4n (linear) — a distância até superpolinomial é o tamanho do desafio.
Uma prova séria deve enfrentar ou contornar explicitamente essas barreiras (+ algebrization, Aaronson–Wigderson 2008 — a mapear na FASE 4 com fonte própria; não está no documento de Cook, que é anterior).

### Institucionais (regras do Clay, adotadas 2018-09-26 — FATO VERIFICADO em claymath.org/millennium-problems/rules/, 2026-07-10)
1. Publicação em **Qualifying Outlet**.
2. **≥ 2 anos** decorridos desde a publicação.
3. **Aceitação geral** na comunidade matemática global.
4. CMI **não aceita submissões diretas** de soluções propostas.

**Claim:** `7P-PNP-CLM-0007` (critérios consolidados).

## 6. Lacunas e próximos passos desta spec

- LACUNA: equivalência verificador/NTM citada, não reconstruída (FASE 3).
- LACUNA: provas de Cook–Levin e dos resultados de Karp não verificadas nas fontes primárias (SRC-0005/0006/0007 marcadas A OBTER; FASE 3).
- LACUNA: barreira de algebrization fora do documento oficial — exige fonte primária própria (FASE 4).
- Próximo: trilha pedagógica (FASE 2) sobre este material + reconstrução técnica (FASE 3).
