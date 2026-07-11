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
(G1) consistência: cada célula tem exatamente um símbolo; um estado e uma posição de cabeça por passo — "exatamente um" = "pelo menos um" (uma cláusula com as opções) ∧ "no máximo um" (cláusulas binárias ¬a∨¬b por par), como no grupo (2) do lema 3COL;
(G2) configuração inicial: linha 0 codifica w, estado inicial, cabeça na célula 1;
(G3) transição: para cada janela local (célula i e vizinhas, passo t → t+1), a mudança respeita ALGUMA transição de N — a disjunção sobre as opções não determinísticas é onde o "∃ ramo" vira "∃ atribuição". Como cada janela envolve O(1) variáveis (alfabeto e estados são constantes de N), a condição da janela é uma função booleana de aridade constante, convertível a CNF com blow-up CONSTANTE — o tamanho total segue O(Q(n)²) [detalhe explicitado após REV-0002];
(G4) inércia: células longe da cabeça não mudam;
(G5) aceitação: alguma linha contém estado aceitante.
Total: O(Q(n)²) janelas × O(1) cláusulas cada = fórmula de tamanho polinomial, construível em tempo polinomial por um algoritmo uniforme (varredura das janelas). Correção: atribuição satisfatória ⟺ tableau válido ⟺ ramo aceitante de N sobre w. Logo toda L ∈ NP tem L ≤p SAT; SAT ∈ NP (certificado = atribuição); portanto SAT é NP-completo. ∎

*Fidelidade: a estrutura segue a prova de Cook (variáveis para símbolo/estado/posição, construção CNF, cota polinomial), modernizada para ≤p. Estado: esboço completo; formalização item da FASE 6; revisão externa pendente.*

## 5. Decisão vs busca: auto-redutibilidade de SAT

**Proposição [RECONSTRUÇÃO; claim 7P-PNP-CLM-0012].** Com um oráculo para SAT-decisão, encontra-se uma atribuição satisfatória em tempo polinomial (portanto P = NP ⟹ a versão de BUSCA também é polinomial).

*Prova.* Dada F satisfatível com variáveis v₁..vₙ: pergunte se F[v₁:=⊤] é satisfatível; se sim fixe v₁ = ⊤, senão fixe v₁ = ⊥ (F satisfatível garante que um dos dois é). Repita para v₂..vₙ. São n consultas, cada uma sobre fórmula de tamanho ≤ |F|; a atribuição final satisfaz F por invariante ("a fórmula restrita permanece satisfatível"). ∎

Morais: (i) para SAT, resolver a decisão já entrega a solução construtiva; (ii) é um exemplo de redução de **Turing** (múltiplas consultas adaptativas) — o tipo original de Cook — mostrando por que as duas noções de redução coexistem.

## 6. Hierarquias de tempo: onde a diagonalização FUNCIONA

**Origem [FONTE: SRC-0009, Hartmanis–Stearns 1965]:** o paper que batizou "computational complexity" já prova (Corollary 1.2) que existem cadeias infinitas de classes de complexidade distintas, sobre TM multifita.

**Forma moderna [FONTE: SRC-0010, Theorem 3.1, verbatim]:** se f, g são time-constructible e f(n)·log f(n) = o(g(n)), então DTIME(f(n)) ⊊ DTIME(g(n)).
*Ideia da prova:* diagonalização com simulação universal — a máquina D, com entrada x, simula M_x sobre x por um orçamento de passos e responde o OPOSTO; D vive em DTIME(g) mas não pode coincidir com nenhuma máquina de DTIME(f). O fator log é o custo da simulação universal.

**Análogo não determinístico [FONTE: SRC-0010, Theorem 3.3, verbatim]:** f(n+1) = o(g(n)) ⟹ NTIME(f(n)) ⊊ NTIME(g(n)) (com "lazy diagonalization" — flip adiado, pois negar uma NTM diretamente custaria exponencial).

**Corolário [RECONSTRUÇÃO; claim 7P-PNP-CLM-0013].** P ⊊ EXP. *Prova:* P ⊆ DTIME(2ⁿ), pois todo n^k é eventualmente < 2ⁿ. Pelo Theorem 3.1 com f(n) = 2ⁿ e g(n) = 2³ⁿ (2ⁿ·log 2ⁿ = o(2³ⁿ)), existe UMA linguagem L ∈ DTIME(2³ⁿ) ⊆ EXP com L ∉ DTIME(2ⁿ) ⊇ P — logo L ∉ P. ∎ [Quantificadores explicitados após REV-0002/Kimi: a separação exige exibir uma única L fora de TODOS os DTIME(n^k), o que a inclusão P ⊆ DTIME(2ⁿ) entrega de uma vez.] — uma das POUCAS separações incondicionais que temos.

**Moral estrutural:** diagonalização separa classes do MESMO tipo com mais recurso (det vs det; não-det vs não-det). P vs NP compara TIPOS diferentes — e a relativization (§ barreiras) explica por que a técnica pura não cruza essa fronteira.

## 7. Ladner: o mundo intermediário

**Teorema [FONTE: SRC-0010, Theorem 3.4, verbatim]:** se P ≠ NP, existe L ∈ NP \ P que NÃO é NP-completo.

*Ideia da prova (padding):* SAT_H = {ψ·0·1^(n^H(n)) : ψ ∈ SAT, n = |ψ|}, com H de crescimento auto-regulado (definida por diagonalização preguiçosa): se H fica constante, SAT_H é SAT com padding polinomial (NP-completo); se H → ∞, o padding mata a NP-completude; a construção equilibra H exatamente para SAT_H escapar de ambos, assumindo P ≠ NP. [Primária: Ladner, JACM 22(1):155–171, 1975 — SRC-0011, A OBTER: ACM bloqueou download automatizado.]

**Consequência:** P ≠ NP implica uma ZONA INTERMEDIÁRIA não vazia. Candidatos naturais que vivem lá (sem prova): graph isomorphism — o mesmo que Cook flagou em 1971 (claim 0008) — e factoring (§3). Essa zona é território experimental privilegiado para o programa: problemas onde nem a completude nem a pertinência a P são conhecidas.

## 8. Hierarquia polinomial e Karp–Lipton

**Σᵖ₂ [FONTE: SRC-0010, Definition 5.1, verbatim]:** L ∈ Σᵖ₂ ⟺ ∃ TM polinomial M e polinômio q com x ∈ L ⟺ ∃u∈{0,1}^q(|x|) ∀v∈{0,1}^q(|x|): M(x,u,v)=1.

**PH geral [FONTE: SRC-0010, Definition 5.4, verbatim]:** Σᵖᵢ = i quantificadores alternados começando por ∃; Πᵖᵢ = começando por ∀; PH = ∪ᵢ Σᵖᵢ. Casos base: Σᵖ₁ = NP, Πᵖ₁ = coNP. [Nota de auditoria: o Remark 5.5 do draft contém o typo "Πᵖ₂ = coNP" — o correto, consistente com a própria Def. 5.4, é Πᵖ₁ = coNP. Erro do draft registrado; não propagado.] [Primária da PH: Stockmeyer, TCS 3(1):1–22, 1976 — SRC-0012, A OBTER (paywall).]

**Colapso [RECONSTRUÇÃO; claim 7P-PNP-CLM-0016]:** P = NP ⟹ PH = P. *Ideia:* com P = NP, cada quantificador pode ser absorvido de dentro pra fora — o predicado polinomial com um ∃ na frente é NP = P, vira novo predicado polinomial; indução em i. ∎ A conjectura padrão da área é que a PH NÃO colapsa (generaliza P ≠ NP e NP ≠ coNP) — usada como "moeda de plausibilidade" em resultados condicionais.

**Karp–Lipton [FONTE: SRC-0010, Theorem 6.13, verbatim]:** NP ⊆ P/poly ⟹ PH = Σᵖ₂ (com melhorias de Sipser).
*Ideia da prova:* mostrar Πᵖ₂ ⊆ Σᵖ₂ via a linguagem Π₂SAT (∀u∃v φ(u,v)). Se NP ⊆ P/poly, existe família de circuitos polinomiais decidindo satisfatibilidade. **Passo intermediário (não imediato — LACUNA apontada por REV-0002/Kimi e agora explicitada):** o §5 dá um ALGORITMO adaptativo com oráculo de decisão; para obter um CIRCUITO que produz a testemunha é preciso implementar essa auto-redução em hardware — compor n cópias do circuito decisor, uma por variável fixada, o que preserva tamanho polinomial (é o Theorem 2.19 de SRC-0010, search-to-decision, aplicado de forma não uniforme). Com o circuito produtor C em mãos, "∀u∃v φ(u,v)" vira "∃C ∀u: φ(u, C(u))" — um ∃∀, ou seja, Σᵖ₂. ∎ (esboço; a composição de circuitos é o detalhe a formalizar)
**Variante de Meyer [FONTE: SRC-0010, Theorem 6.14]:** EXP ⊆ P/poly ⟹ EXP = Σᵖ₂; combinada com a hierarquia de tempo: P = NP ⟹ EXP ⊄ P/poly.

**Interpretação para o programa:** (i) o atalho não uniforme para NP custaria o colapso da PH — evidência estrutural de NP ⊄ P/poly; (ii) upper bounds podem gerar lower bounds (Meyer) — inversão que reaparece nas fronteiras modernas (FASE 4); (iii) P/poly = TMs com advice polinomial por tamanho de entrada = exatamente o modelo das "tabelas escondidas" das confusões proibidas do charter. [Primária: Karp–Lipton 1982, L'Enseignement Math. 28:191–209 — SRC-0013, A OBTER; secundária identificada: notas Waterloo CS860.]

## 9. Dependências e pendências desta reconstrução

| Item | Depende de | Estado |
|---|---|---|
| Equivalência A⟺B (§2) | Defs. de SRC-0003 + SRC-0005 | Reconstruída; revisão externa pendente |
| Cook–Levin moderno (§4) | §1, §2 | Esboço completo; revisão externa pendente; formalização FASE 6 |
| Auto-redutibilidade (§5) | Def. de SAT | Reconstruída; revisão externa pendente; USADA no esboço de Karp–Lipton (§8) |
| Hierarquia de tempo + P ⊊ EXP (§6) | SRC-0009/0010 | Enunciados verificados; corolário reconstruído |
| Ladner (§7) | SRC-0010 (Thm 3.4) | Enunciado verificado; primária SRC-0011 A OBTER |
| PH + colapso (§8) | SRC-0010 (Defs 5.1/5.4) | Verificado; colapso reconstruído; primária SRC-0012 A OBTER |
| Karp–Lipton (§8) | SRC-0010 (Thm 6.13/6.14) + §5 | Enunciado verificado; esboço reconstruído; primária SRC-0013 A OBTER |
| Espaço (PSPACE, Savitch), Mahaney, hierarquia relativizada | próximas iterações | — |
