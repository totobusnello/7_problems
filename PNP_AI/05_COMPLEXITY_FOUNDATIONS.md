# PNP-AI — 05 — COMPLEXITY FOUNDATIONS (reconstrução técnica)

> FASE 3, iniciada 2026-07-10. Trilha TÉCNICA: definições formais, teoremas com prova ou esboço rigoroso, dependências explícitas.
> Convenção de rótulos: **[FONTE]** = conferido em fonte primária do ledger · **[RECONSTRUÇÃO]** = derivação do projeto reproduzindo resultado conhecido (não é claim de novidade) · **[⚠️]** = resultado conhecido com fonte primária ainda não processada.

---

## 1. Modelos de computação

**TM determinística [FONTE: SRC-0003, Appendix].** Máquina de Turing com fita e tabela de transição finita; T_M(n) = pior caso de passos sobre entradas de comprimento n; M é polinomial se ∃k: T_M(n) ≤ n^k + k.

**TM não determinística (NTM).** Igual, mas a relação de transição permite múltiplos sucessores por configuração; M aceita w sse EXISTE ao menos uma computação que termina em estado de aceitação. Tempo = comprimento do menor ramo aceitante (para w aceito). O não determinismo não é um mecanismo físico — é um quantificador existencial disfarçado de máquina.

**Robustez [FONTE: SRC-0003 §1].** Modelos razoáveis (multi-fita, RAM) simulam-se com overhead polinomial (quadrático/cúbico) — P e NP não dependem da escolha.

## 2. NP: as duas caracterizações e sua equivalência

**Def. A (verificador) [FONTE: SRC-0003, verbatim]:** L ∈ NP ⟺ ∃k e checking relation R polynomial-time tais que w ∈ L ⟺ ∃y(|y| ≤ |w|^k ∧ R(w,y)).

**Def. B (NTM) [FONTE: SRC-0005, Summary]:** L ∈ NP ⟺ L é aceita por alguma NTM em tempo polinomial. (A forma original de Cook: "any recognition problem solved by a polynomial time-bounded nondeterministic Turing machine".)

**Teorema (equivalência A ⟺ B). [RECONSTRUÇÃO — resultado padrão; claim 7P-PNP-CLM-0009]**

*Prova.*
(A ⟹ B): dada R e k, construa a NTM N que, com entrada w, escreve não deterministicamente um y com |y| ≤ |w|^k na fita (cada símbolo é uma escolha) e então roda o decisor polinomial de L_R sobre w#y, aceitando sse R(w,y). Cada ramo tem custo polinomial; existe ramo aceitante ⟺ existe certificado y válido ⟺ w ∈ L.
(B ⟹ A): dada NTM N com tempo Q(n) polinomial e grau de ramificação ≤ c (constante, pois a tabela de transição é finita), defina o certificado y como a sequência das escolhas não determinísticas de um ramo aceitante, |y| ≤ Q(|w|)·⌈log c⌉ = polinomial. Defina R(w,y) = "a simulação determinística de N sobre w, seguindo as escolhas ditadas por y, aceita em ≤ Q(|w|) passos". R é decidível em tempo polinomial (simulação passo a passo) e w ∈ L ⟺ ∃y: R(w,y). ∎

*Estado: reconstrução completa; revisão adversarial externa pendente.*

## 3. co-NP e a zona NP ∩ co-NP

**Def.** co-NP = {L : complemento de L ∈ NP}. Certificados curtos para respostas **NÃO**.

- A definição de NP é assimétrica (só o SIM tem certificado) — por isso co-NP ≠ NP é plausível mas TAMBÉM aberto; NP ≠ co-NP implicaria P ≠ NP (P é fechada por complemento). [RECONSTRUÇÃO trivial: se P = NP, então NP = P = co-P = co-NP.]
- **TAUTOLOGY** (a forma que Cook usou em 1971!) é o exemplo canônico de co-NP: "F é tautologia" ⟺ "¬F é insatisfatível" — o certificado curto natural é do NÃO (uma atribuição que falsifica F). [FONTE: SRC-0005 usa {DNF tautologies} como alvo.]
- **NP ∩ co-NP** é a zona suspeita de conter problemas de P "ainda não descobertos": PRIMES tinha certificados dos dois lados (composto: fator; primo: certificado de Pratt [⚠️ Pratt 1975, fonte a processar]) décadas antes do AKS provar PRIMES ∈ P [FONTE: SRC-0003 cita composites ∈ P, ref. [1]]. FACTORING (versão decisão) vive aí hoje — base da esperança de que fatorar não seja NP-completo.

## 4. Cook–Levin: original e forma moderna

**Forma original [FONTE: SRC-0005, verbatim]:**
> "Theorem 1. If a set S of strings is accepted by some nondeterministic Turing machine within polynomial time, then S is P-reducible to {DNF tautologies}."

Notas de fidelidade histórica (conferidas no paper):
- A redução original de Cook é a **P-reducibility**: máquina de consulta (query machine) com oráculo, tempo polinomial — análogo polinomial da redução de **Turing**, não a many-one. A versão many-one (≤p) que virou padrão foi introduzida por Karp [FONTE: SRC-0003 §2].
- O alvo original é {DNF tautologies} (co-NP-completo na linguagem moderna); a ponte é: A(w) em CNF é satisfatível ⟺ ¬A(w) em DNF não é tautologia [FONTE: SRC-0005, abertura da prova].
- **Theorem 2 de Cook [FONTE: SRC-0005, verbatim]:** {tautologies}, {DNF tautologies}, D3 (cláusulas com 3 literais) e {subgraph pairs} têm o mesmo grau polinomial. Com o Remark histórico notável: Cook já em 1971 aponta que **{primes}** e **{isomorphic graph pairs}** resistiam à classificação — os dois problemas que meio século depois continuam especiais (PRIMES caiu em P; graph isomorphism segue intermediário, cf. SRC-0003).

**Forma moderna [RECONSTRUÇÃO do enunciado padrão]:** SAT é NP-completo sob ≤p.

**Esboço rigoroso da prova (argumento do tableau). [RECONSTRUÇÃO; claim 7P-PNP-CLM-0011]**
Seja L ∈ NP via NTM N com tempo Q(n). Fixe w, n = |w|. Uma computação aceitante de N é uma matriz (tableau) de (Q(n)+1) × (Q(n)+1) células: linha t = configuração no passo t. Defina variáveis booleanas:
- x[t, i, σ]: "no passo t, a célula i contém o símbolo σ";
- y[t, q]: "no passo t, o estado é q";
- z[t, i]: "no passo t, a cabeça está na célula i".

Cláusulas em cinco grupos, todas de tamanho O(1) ou O(Q(n)):
(G1) consistência: cada célula tem exatamente um símbolo; um estado e uma posição de cabeça por passo;
(G2) configuração inicial: linha 0 codifica w, estado inicial, cabeça na célula 1;
(G3) transição: para cada janela local (célula i e vizinhas, passo t → t+1), a mudança respeita ALGUMA transição de N — a disjunção sobre as opções não determinísticas é onde o "∃ ramo" vira "∃ atribuição";
(G4) inércia: células longe da cabeça não mudam;
(G5) aceitação: alguma linha contém estado aceitante.
Total: O(Q(n)²) janelas × O(1) cláusulas cada = fórmula de tamanho polinomial, construível em tempo polinomial por um algoritmo uniforme (varredura das janelas). Correção: atribuição satisfatória ⟺ tableau válido ⟺ ramo aceitante de N sobre w. Logo toda L ∈ NP tem L ≤p SAT; SAT ∈ NP (certificado = atribuição); portanto SAT é NP-completo. ∎

*Fidelidade: a estrutura segue a prova de Cook (variáveis para símbolo/estado/posição, construção CNF, cota polinomial), modernizada para ≤p. Estado: esboço completo; formalização item da FASE 6; revisão externa pendente.*

## 5. Decisão vs busca: auto-redutibilidade de SAT

**Proposição [RECONSTRUÇÃO; claim 7P-PNP-CLM-0012].** Com um oráculo para SAT-decisão, encontra-se uma atribuição satisfatória em tempo polinomial (portanto P = NP ⟹ a versão de BUSCA também é polinomial).

*Prova.* Dada F satisfatível com variáveis v₁..vₙ: pergunte se F[v₁:=⊤] é satisfatível; se sim fixe v₁ = ⊤, senão fixe v₁ = ⊥ (F satisfatível garante que um dos dois é). Repita para v₂..vₙ. São n consultas, cada uma sobre fórmula de tamanho ≤ |F|; a atribuição final satisfaz F por invariante ("a fórmula restrita permanece satisfatível"). ∎

Morais: (i) para SAT, resolver a decisão já entrega a solução construtiva; (ii) é um exemplo de redução de **Turing** (múltiplas consultas adaptativas) — o tipo original de Cook — mostrando por que as duas noções de redução coexistem.

## 6. Não uniformidade: enunciados-ponte [⚠️ fontes a processar na FASE 4]

- **NP ⊄ P/poly ⟹ P ≠ NP** (P ⊆ P/poly; separar do lado não uniforme é mais forte). É a rota dos circuit lower bounds apontada em SRC-0003 §3.
- **Karp–Lipton:** NP ⊆ P/poly ⟹ colapso da hierarquia polinomial (PH = Σ₂ᵖ). Interpretação: nem o atalho não uniforme sai de graça — teria consequências estruturais dramáticas. [⚠️ enunciado da literatura padrão; fonte primária pendente; a própria definição formal de PH entra aqui na próxima iteração.]

## 7. Dependências e pendências desta reconstrução

| Item | Depende de | Estado |
|---|---|---|
| Equivalência A⟺B (§2) | Defs. de SRC-0003 + SRC-0005 | Reconstruída; revisão externa pendente |
| Cook–Levin moderno (§4) | §1, §2 | Esboço completo; revisão externa pendente; formalização FASE 6 |
| Auto-redutibilidade (§5) | Def. de SAT | Reconstruída; revisão externa pendente |
| Hierarquia de tempo, Ladner (problemas intermediários), PH formal, Karp–Lipton c/ prova | fontes a obter | Próxima iteração da FASE 3 |
