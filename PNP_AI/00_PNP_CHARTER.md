# PNP-AI — 00 — CHARTER

> Primeiro laboratório AI-first do 7_PROBLEMS. Criado: 2026-07-10 (Sessão 0).

## Por que P versus NP primeiro (hipótese metodológica auditada na Sessão 0)

1. **Objetos discretos** — fórmulas, grafos, circuitos, algoritmos e provas têm representação finita.
2. **Execução direta** — algoritmos candidatos são implementáveis e executáveis.
3. **Contraexemplos automáticos** — instâncias adversariais podem ser geradas e pesquisadas.
4. **Verificação exata** — subresultados testáveis sem aproximação numérica.
5. **Solvers especializados** — SAT/SMT, theorem provers, CAS participam do processo.
6. **Formalização** — definições, reduções e provas progressivamente formalizáveis (Lean 4 / Mathlib como candidato principal).
7. **Critérios objetivos** — algoritmo candidato auditável em correção, completude, pior caso, memória, uniformidade, complexidade assintótica.
8. **Revisão adversarial adequada** — outros modelos procuram entradas que quebram o algoritmo, passos não uniformes, custos exponenciais ocultos, circularidade, pré-computação escondida.

**Isso NÃO significa que P vs NP seja mais fácil.** P≠NP exige limitação universal; P=NP exige algoritmo polinomial correto para todas as entradas.

## Confusões proibidas (recitar antes de todo ciclo)

- Resolver muitas instâncias rápido ≠ P=NP.
- Heurística boa no caso médio ≠ algoritmo polinomial de pior caso.
- Rede neural certa "na maioria dos casos" ≠ resolver problema NP-completo exatamente.
- Pré-computação gigante / conhecimento nos pesos = custo escondido.
- Um algoritmo por tamanho de entrada = não uniformidade.
- Experimento finito nunca demonstra comportamento para todo n.
- P≠NP exige limitação universal, não o fracasso dos algoritmos conhecidos.
- Prova séria enfrenta ou contorna explicitamente as barreiras (relativization, natural proofs, algebrization).
- SAT resolvido por busca exponencial ≠ P=NP.
- "Aparência polinomial" pode esconder: constante dependente de n, preparação exponencial, número exponencial de parâmetros, oráculo, tabela exponencial, hipótese não computável.
- Custo de treinamento de IA conta quando relevante para a alegação algorítmica.

## Perguntas da fase inicial (antes de qualquer tentativa de prova)

1. Qual é a formulação oficial exata (Clay / Cook)?
2. Quais definições mínimas: linguagem, algoritmo, máquina de Turing, tempo polinomial, P, NP, verificador, certificado, redução polinomial, NP-completude, circuitos, uniformidade?
3. Quais formulações equivalentes são mais adequadas para pesquisa assistida por IA?
4. Quais famílias de abordagens já bateram em barreiras conhecidas?
5. Quais subproblemas restritos permitem experimentos exatos, busca automatizada, formalização e resultados incrementais?
6. Onde a IA contribui de forma diferente da busca humana tradicional?
7. Quais resultados intermediários seriam relevantes mesmo sem resolver P vs NP?
8. Qual subproblema será o primeiro laboratório? (FASE 5 — scorecard)

## Linhas de pesquisa candidatas (Nível 3 — a mapear na FASE 4, sem escolha antecipada)

circuit lower bounds (restritos e gerais) · monotone circuits · algebraic circuit complexity · formula size · branching programs · communication complexity · proof complexity · pseudorandom generators · hardness vs randomness · meta-complexity · natural proofs · relativization · algebrization · geometric complexity theory · hardness magnification · fine-grained complexity · average-case complexity · parameterized complexity · automated lower-bound search · circuit minimization · problemas Kolmogorov-related (MCSP etc.)

Para cada área registrar: definição, objetivo, melhores resultados, barreira atual, compatibilidade com IA, dados/software, formalizabilidade, chance de resultado intermediário, risco de duplicação, especialistas, ferramentas. **Verificar a lista na literatura — não assumir completa.**
