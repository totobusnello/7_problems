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

---

## ETAPA B EXECUTADA (2026-07-10, ordem invertida por decisão de Luiz: B antes de A)

**B1 — Gap das 2 classes NPN-4: CONFIRMADO VIVO** (SRC-0027): README do repo diz "220 exact, 2 upper bounds"; último commit 2026-03-10; nenhum fechamento registrado. Risco residual: preprints não indexados — aceito e documentado.

**B2 — Auditoria profunda de C4 (formalização):** duas descobertas que derrubam C4 como *subproblema de pesquisa*:
- Cook–Levin **já foi mecanizado em Coq** (Gäher–Kunze, SRC-0024) — port a Lean tem novidade parcial.
- **P/NP em Mathlib está sendo formalizado agora por terceiros** (issue #35366, SRC-0025) — duplicação direta; a rota de valor seria contribuir ao esforço deles (interação externa ⟹ autorização de Luiz).
- C4 permanece valioso como INFRAESTRUTURA para formalizar os NOSSOS claims (lema 0010 etc.), mas DUP 4→2 como pesquisa. Base 32→30; ponderado 33.
- **Alerta ambiental registrado:** circulam alegações de "provas verificadas em Lean" de P≠NP e de P=NP (!) em preprints/redes — reforça a regra do charter: "compilou no Lean" só vale com axiomas e definições auditados.

**B3 — Auditoria profunda de C3 (MCSP):** teoria profunda e MUITO ativa (ETH-hardness de MCSP* provada; MCSP total ABERTO com obstáculos identificados; SoS lower bounds; ligação com Graph Isomorphism). Dependência de especialistas alta (ESP 2 confirmado). **Convergência estrutural descoberta: a face experimental de C3 É o C1** — catálogos exatos de complexidade em pequena escala são os dados da meta-complexidade (o próprio SRC-0019 usa o catálogo para uma questão MCSP-adjacente). Isso sustenta upgrade de REL de C1: 3→4 (com fonte, não por conveniência — flag para revisão).

## Scorecard v4 (final da FASE 5; pesos REL×2; total /45)

| Candidato | Base /40 | Ponderado /45 | Mudanças vs v3 |
|---|---|---|---|
| **C1 exact synthesis (restrito)** | 34 | **38** | REL 3→4 (ponte MCSP documentada em B3) |
| C2 proof complexity exp. | 31 | 35 | = |
| C3 MCSP | 28 | 33 | ESP 2 confirmado; face experimental converge p/ C1 |
| C4 formalização | 30 | 33 | DUP 4→2 (Coq feito; Mathlib em andamento por terceiros) |
| C5 magnification | 22 | 27 | = |

## PROPOSTA v4 — SUPERADA POR REV-0004 (mantida para histórico; ver v5 abaixo)

**Selecionar C1-restrito** como primeiro subproblema do PNP-AI, com as salvaguardas do Grok incorporadas:
1. **Unidade 1 (piloto, ex-etapa A):** reproduzir com DRAT + checker independente 1–2 valores exatos JÁ RESOLVIDOS do catálogo NPN-4, com encoding próprio. Sucesso binário; custo horas.
2. **Unidade 2 (condicional):** identificar as 2 classes pendentes no CSV do repo; sonda de viabilidade em k=9 SOMENTE com budget computacional e critério de aborto aprovados por Luiz.
3. **Horizonte:** expandir catálogo (n=5 parcial, outras bases) e conectar às questões abertas de meta-complexidade (a ponte C1→C3 é o caminho de relevância crescente).
4. C4-infra continua permitido em doses mínimas (formalizar claims nossos), sem virar frente.

---

## REV-0004 — Revisão de confirmação (Codex/GPT-5, pedida por Luiz, 2026-07-11): VEREDITO **DERRUBAR**

> Nota de canal: Luiz solicitou GPT-5.6; o canal Codex (OAuth ChatGPT) rejeitou `gpt-5.6` e `gpt-5.6-codex` como não suportados no plano. Revisão executada com o modelo default do canal (auto-id: "Codex, baseado em GPT-5, sem acesso ao checkpoint específico"). Registrado sem simulação.

Findings e adjudicação (11 findings; os centrais):

| Finding (Codex) | Adjudicação |
|---|---|
| CRÍTICO: seleção declarada "final" sem executar o piloto que a própria v3 definia como gate — FER=5 e "custo em horas" seguem conjecturais | **ACEITO** — seleção revertida a PENDENTE; o piloto volta a ser GATE pré-seleção |
| REL 3→4 não demonstrado (relação temática com MCSP ≠ avançar MCSP); dupla adaptação pós-crítica do scorecard; soma ponderada com pseudo-precisão | **ACEITO** — REL de C1 volta a 3; pesos/âncoras serão fixados ANTES de qualquer scorecard futuro; liderança de 1–2 pontos ordinais não decide nada |
| **DRAT não valida o encoding** — UNSAT certifica a CNF, não que a CNF signifique "não existe AIG ≤ k para f" | **ACEITO — vira regra do programa:** todo resultado via encoding próprio exige validação SEMÂNTICA independente (cross-check com enumeração exaustiva em tamanhos pequenos + verificação por simulação de todo circuito encontrado) |
| Unidade 1 só não é teatro se puder REPROVAR C1 (critérios pré-registrados, incl. falha/custo) | **ACEITO** — gate pré-registrado abaixo |
| "Gap confirmado vivo" = overclaim | **ACEITO** — reformulado: "não fechado na fonte e nas buscas realizadas até 2026-07-10" |
| Comparação assimétrica: C2 sem alvo concreto na mesma granularidade; sem busca fora da shortlist | **ACEITO** — pré-requisitos da seleção definitiva |
| n=5 como horizonte = promessa sem evidência de escalabilidade | **ACEITO** — rebaixado a hipótese sujeita a benchmark |

## PROPOSTA v5 (vigente) — seleção PENDENTE + gate de qualificação pré-registrado

**Estado da seleção: PENDENTE.** Nenhum candidato selecionado. C1 tem apenas prioridade de teste.

**GATE DE QUALIFICAÇÃO (pré-registro — executar mediante aprovação de Luiz):**
- **G1 (SAT):** para 1 classe NPN-4 já resolvida do catálogo, encontrar circuito AIG de tamanho ótimo com encoding próprio; verificar o circuito por SIMULAÇÃO contra a truth table (validação semântica, não só solver).
- **G2 (UNSAT):** para a mesma classe, provar impossibilidade em (ótimo − 1) com prova DRAT verificada por checker independente (drat-trim ou equivalente).
- **G3 (validação semântica do encoding):** cross-check do encoding contra enumeração exaustiva independente em escala mínima (todas as funções de n=2 e amostra de n=3): valores ótimos do nosso pipeline == valores por enumeração.
- **Budget e aborto (pré-registrados):** máx. 4h de wall-clock por instância no hardware local; estouro = FALHA do gate (dado real de FER), não "quase sucesso".
- **Critérios de decisão:** G1∧G2∧G3 dentro do budget ⟹ C1 ganha seleção PROVISÓRIA para sonda k=9 limitada (budget próprio a aprovar). Qualquer falha ⟹ re-pontuar FER de C1 com o dado real e formular alvo concreto de C2 na mesma granularidade antes de nova rodada.
- **Antes da seleção DEFINITIVA (independente do resultado do gate):** (i) alvo concreto de C2 formulado e auditado no mesmo nível; (ii) busca documentada por ≥1 candidato fora da shortlist C1–C5; (iii) pesos e âncoras do scorecard fixados ex-ante.
