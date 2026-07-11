# PNP-AI — 09 — CANDIDATE SUBPROBLEMS (FASE 5)

> Iniciado: 2026-07-10 (Ciclo 7, PR fase5). **Estado deste scorecard: HEURISTIC — proposta inicial do coordenador, PENDENTE de (a) auditoria bibliográfica real por candidato, (b) revisão adversarial multi-modelo, (c) decisão de Luiz.** Os scores abaixo vêm de conhecimento geral do coordenador e serão confirmados ou revisados com buscas reais antes da seleção final. Nenhuma classificação muda silenciosamente.

## Critérios (do brief, escala 1–5; ↑ = melhor)

REL relevância p/ P vs NP · CLA clareza do enunciado · FAL falsificabilidade · FOR formalizabilidade · FER ferramentas disponíveis HOJE · INT probabilidade de resultado intermediário · DUP baixo risco de duplicação (5 = risco baixo) · ESP baixa dependência de especialistas (5 = baixa)

## Candidatos

### C1 — Complexidade exata de funções booleanas pequenas via SAT (exact synthesis)
Determinar valores EXATOS de complexidade (tamanho mínimo de circuito/fórmula) de funções específicas pequenas, usando SAT solvers com proof logging. Linha existente na literatura (a auditar: Knuth; Kojevnikov–Kulikov–Yaroslavtsev; trabalhos recentes de SAT-based synthesis). Resultado intermediário típico: novos valores exatos ou reproduções verificadas com certificados DRAT.

### C2 — Proof complexity experimental: famílias concretas com certificados
Gerar famílias clássicas (Pigeonhole, Tseitin, random k-CNF na transição de fase), medir crescimento de provas de resolution em solvers CDCL com DRAT, reproduzir computacionalmente o comportamento previsto pelos lower bounds conhecidos (Haken etc.) e explorar variantes. Conexão direta com a regra de proof logging do programa.

### C3 — Meta-complexidade experimental: MCSP em pequena escala
Minimum Circuit Size Problem em truth tables pequenas: experimentos exatos, fronteira quente da área (ligações com natural proofs — o próprio Razborov–Rudich). Alto potencial, mas exigência conceitual maior.

### C4 — Formalização Lean 4 da fundação (infraestrutura)
Formalizar em Lean/Mathlib os claims já reconstruídos: definições (P, NP, ≤p), lema 0010 (3COL→SAT), equivalência 0009, rumo a Cook–Levin (0011). Resultado quase garantido, valor composto (destrava FORMALLY_VERIFIED para tudo que vier depois).

### C5 — Hardness magnification / fronteiras teóricas (leitura estruturada)
Mapa profundo de uma fronteira teórica moderna. Sem experimento direto; alto risco de ficar em resumo de literatura.

## Scorecard (proposta HEURISTIC — v1)

| Candidato | REL | CLA | FAL | FOR | FER | INT | DUP | ESP | Total /40 |
|---|---|---|---|---|---|---|---|---|---|
| C1 exact synthesis | 3 | 5 | 5 | 4 | 5 | 4 | 3 | 4 | **33** |
| C2 proof complexity exp. | 4 | 4 | 5 | 3 | 5 | 4 | 3 | 3 | **31** |
| C4 formalização Lean | 3 | 5 | 3 | 5 | 4 | 5 | 4 | 3 | **32** |
| C3 MCSP | 5 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | **28** |
| C5 magnification | 5 | 3 | 2 | 2 | 3 | 2 | 4 | 1 | **22** |

## Leitura da proposta (v1, a validar)

- **C1** lidera por executabilidade: enunciados exatos e falsificáveis ("a função f exige ≥ k portas"), verificáveis por UNSAT+DRAT, com as ferramentas já instaladas. Risco principal: área minerada — a auditoria bibliográfica decide.
- **C4** é o complemento natural de infraestrutura (pode correr como trilha paralela leve, sem violar a regra de um-gargalo-por-vez, se limitada às definições já estabilizadas).
- **C3/C5** são as pontes para relevância profunda, mas pedem maturidade que o laboratório ainda não tem.
- Protocolo anti-barreira: nenhum candidato é uma "estratégia de prova de lower bound geral" — a triagem de 6 perguntas aplica-se aos CLAIMS que os experimentos gerarem.

## Próximos passos da FASE 5 (nesta ordem)

1. Auditoria bibliográfica real de C1 e C2 (estado da arte, últimos resultados, o que está em aberto, onde há espaço) → atualizar scores com fontes.
2. Revisão adversarial do scorecard (≥1 família distinta).
3. Proposta final de UM subproblema → decisão de Luiz.
