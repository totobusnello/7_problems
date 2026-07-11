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

## Auditoria bibliográfica (executada 2026-07-10 — Ciclo 7; fontes SRC-0018..0023)

**C1 — o que a literatura mostra:**
- Área ATIVA (papers de 2020 a 2026, incl. linha criptográfica). Fronteira prática: exact synthesis instantâneo até tamanho ~7; tamanho 13 leva semanas (SRC-0018). Método padrão: SAT-based synthesis (SRC-0020) + cube-and-conquer (SRC-0021).
- **GAP CONCRETO IDENTIFICADO (SRC-0019, preprint mar/2026):** o catálogo de tamanhos exatos AIG das 222 classes NPN de n=4 tem **2 classes sem valor exato** — upper bound 10 confirmado, decisão em k=9 deu timeout. Fechar cada classe = ou circuito de 9 portas (SAT) ou prova de impossibilidade (UNSAT + DRAT). Dados públicos no GitHub do autor.
- Outras aberturas documentadas: catálogo n=5 (largamente inexistente), outras bases, questões abertas explícitas do SRC-0019 (gap constante sob perturbação de 1 bit; famílias Ω(n)).
- **Impacto no score:** DUP 3→2 (área minerada — reproduzir o genérico duplica); INT 4→5 (alvo aberto específico e alcançável, com resultado publicável como nota/contribuição de dados).

**C2 — o que a literatura mostra:**
- Nicho ativo e competitivo: shortest DRAT proofs de PHP (SRC-0022), hardness de parity reordenada (2024), separação CDCL/DPLL (2026). Random k-SAT: teoria madura (threshold provado p/ k grande) e experimentação de transição de fase muito trilhada — pouco espaço para nós agora. Scores mantidos.

## Scorecard v2 (pós-auditoria)

| Candidato | REL | CLA | FAL | FOR | FER | INT | DUP | ESP | Total /40 | Δ |
|---|---|---|---|---|---|---|---|---|---|---|
| **C1 exact synthesis** | 3 | 5 | 5 | 4 | 5 | **5** | **2** | 4 | **33** | = (composição melhor) |
| C4 formalização Lean | 3 | 5 | 3 | 5 | 4 | 5 | 4 | 3 | 32 | = |
| C2 proof complexity exp. | 4 | 4 | 5 | 3 | 5 | 4 | 3 | 3 | 31 | = |
| C3 MCSP | 5 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | 28 | = |
| C5 magnification | 5 | 3 | 2 | 2 | 3 | 2 | 4 | 1 | 22 | = |

## PROPOSTA DE SELEÇÃO (v2 — aguardando revisão adversarial + decisão de Luiz)

**Subproblema selecionado (proposta): C1 — complexidade exata de funções booleanas pequenas via SAT.**

**Primeira unidade de trabalho (Nível 4) proposta:** *determinar o valor exato de opt_AIG das 2 classes NPN-4 pendentes do catálogo de SRC-0019* — decidir k=9 (SAT → circuito explícito verificável; UNSAT → prova DRAT verificada por checker independente, estabelecendo opt=10).
Due diligence prévia (parte da unidade): (a) obter e verificar o repo de dados do SRC-0019 (quais classes, qual encoding); (b) reproduzir o encoding localmente; (c) checar se o gap ainda está aberto (preprint é de março/2026 — pode ter sido fechado).
Por que é a unidade certa: falsificável com resposta binária; verificável mecanicamente (DRAT — cumprindo a regra pós-REV-0002); tamanho compatível com a fronteira prática (k=9~10 está no limite viável com cube-and-conquer); completa um catálogo público (resultado intermediário real, ainda que modesto); e treina exatamente o pipeline que escala para n=5 e outras bases.

**Triagem anti-barreira (protocolo das 6 perguntas):** N/A no sentido estrito — a unidade não é uma estratégia de prova de lower bound geral; é computação exata em instância finita. Os claims resultantes serão FINITE_SCOPE_VERIFIED/COMPUTATIONALLY_TESTED por construção, sem pretensão assintótica.

## REV-0003 — Revisão adversarial da proposta (Grok/xAI, 2026-07-10): VEREDITO **DERRUBAR**

Findings principais e adjudicação do coordenador:

| Finding (Grok) | Adjudicação |
|---|---|
| Ponderação invertida: scorecard maximiza executabilidade (FER) contra relevância (REL=3 de C1), em tensão com o objetivo máximo do charter | **ACEITO EM PARTE** — os 8 critérios vêm do brief sem pesos; mas a crítica é justa: pesos agora explícitos (v3, REL×2). Ressalva: a Prioridade 1 do brief é "construir o laboratório", o que legitima executabilidade ALTA para a primeira unidade — desde que rotulada como PILOTO, não como identidade de pesquisa |
| INT inflado / valor científico mínimo (fechar 2 classes n=4 = footnote) | **ACEITO EM PARTE** — contribuição real porém modesta; reclassificada como validação de pipeline, não "resultado intermediário" no sentido do charter |
| Dependência de preprint único não revisado; gap pode já estar fechado | **ACEITO** — confirmação do gap passa a ser PRÉ-REQUISITO de qualquer seleção envolvendo esse alvo, não due diligence posterior |
| Capacidade computacional irreal (autor sofreu timeout; nós temos um Mac sem stack cube-and-conquer) | **ACEITO** — qualquer ataque a k=9 exige sonda de viabilidade com critério de aborto e budget pré-aprovado por Luiz |
| Auditoria assimétrica (C3/C4/C5 sem auditoria profunda) | **ACEITO** — C3 e C4 serão auditados com a mesma profundidade antes da seleção definitiva |
| Recomendação: C2 ou C4; se C1, começar reproduzindo classe JÁ RESOLVIDA com DRAT | **ACEITO** como base da proposta v3 |

## Scorecard v3 (pesos explícitos: REL×2 — resposta ao finding 1; total /45)

| Candidato | Total ponderado | Observação |
|---|---|---|
| C1 exact synthesis | **36** | Mantém liderança estreita MESMO com REL dobrado — mas a unidade de trabalho original está vetada na forma proposta |
| C2 proof complexity exp. | 35 | Sobe em competitividade; recomendação principal do Grok |
| C4 formalização Lean | 35 | Recomendação de infraestrutura do Grok |
| C3 MCSP | 33 | Auditoria profunda pendente — pode subir |
| C5 magnification | 27 | — |

## PROPOSTA v3 (pós-adjudicação — aguardando decisão de Luiz)

Separar **piloto de pipeline** de **seleção de pesquisa**:

**(A) PILOTO imediato (sem seleção definitiva, risco ~zero, serve a qualquer candidato):** reproduzir com verificação DRAT completa 1–2 valores exatos JÁ RESOLVIDOS do catálogo NPN-4 (encoding próprio, solver local, checker independente). Valida o pipeline exact-synthesis+DRAT de ponta a ponta sem depender do gap de terceiros. Critério de sucesso binário; custo estimado horas, não semanas.

**(B) Antes da seleção definitiva:** auditoria profunda de C3 e C4 (mesmo padrão de C1/C2) + verificação de o gap das 2 classes seguir aberto + resultado do piloto (A) informando o FER real.

**(C) Seleção definitiva** entre C1-restrito (com sonda k=9 SÓ com budget/aborto aprovados), C2 e C4 — com scorecard v4 alimentado por (A) e (B).
