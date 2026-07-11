# 06 — RESEARCH LOG — Histórico cronológico

> Registro append-only. Nada é apagado ou reformulado silenciosamente.

---

## 2026-07-10 — SESSÃO 0 — Inicialização do 7_PROBLEMS

**Contexto:** recebido o Project Brief (docx) definindo o programa. Nenhuma tentativa de resolver problema nesta sessão (por regra).

**Feito:**
1. Brief lido e incorporado (origem: artigo Busnello–Flandoli–Romito → NS-PROB → ampliação para 7_PROBLEMS).
2. Inventário real de ferramentas executado (ver `03_TOOL_INVENTORY.md`): Python/git/pesquisa web OK; SAT/SMT/CAS/Lean ausentes (instaláveis); OpenAI API key inválida; Codex MCP (GPT-5) testado com sucesso.
3. Status oficial dos 7 problemas verificado direto no claymath.org: 6 unsolved, Poincaré solved (ver `01_OFFICIAL_STATUS.md`).
4. Tabela AI-fit auditada preliminarmente — todas as classificações do briefing CONFIRMADAS sem alteração; auditoria profunda delegada à FASE 1 (ver `02_COMPARATIVE_AI_FIT.md`).
5. Decisão inicial avaliada: hipótese "P vs NP como primeiro laboratório AI-first" **CONFIRMADA** (justificativa em `02_COMPARATIVE_AI_FIT.md` e `PNP_AI/00_PNP_CHARTER.md`).
6. Estrutura de arquivos criada (core + PNP_AI + NS_PROB + stubs RH/BSD/HODGE/YM/POINCARE).
7. NS-PROB: nenhum artefato prévio localizado no filesystem ou na memória de longo prazo (nox-mem) — material anterior marcado AGUARDANDO IMPORTAÇÃO (ver `NS_PROB/00_NS_STATUS.md`).
8. Teste de integração OpenAI: API direta FALHOU (key inválida — registrado em `07_MODEL_CALL_LOG.md`); canal alternativo Codex MCP FUNCIONOU (chamada real, contexto isolado confirmado).
9. Primeira tarefa executável definida: reconstruir a formulação oficial de P vs NP (ver `PNP_AI/01_OFFICIAL_PROBLEM_SPEC.md`).

**Bloqueios:** OPENAI_API_KEY inválida (ação de Luiz); material NS-PROB anterior não está nesta máquina (ação de Luiz: exportar das conversas anteriores).

**Próxima ação:** aguardando aprovação de Luiz para executar a primeira tarefa (FASE 0 → FASE 2/3 parcial sobre a formulação oficial).

---

## 2026-07-10 — CICLO 1 — Primeira tarefa executável (autorizada por Luiz: "Sim autorizo")

**Escopo:** reconstruir a formulação oficial de P vs NP + instalar bibliotecas matemáticas gratuitas.

**Feito:**
1. Instaladas e smoke-testadas: sympy 1.14.0, z3-solver 4.16.0, python-sat (Glucose4), networkx 3.6.1, scipy 1.18.0, pypdf (`03_TOOL_INVENTORY.md` atualizado).
2. PDF oficial de Cook ("The P versus NP Problem", Clay) baixado e parseado localmente — SRC-0003 SOURCE_VERIFIED.
3. Regras do prêmio Clay (2018) verificadas — SRC-0004: Qualifying Outlet + 2 anos + aceitação geral; sem submissão direta.
4. `PNP_AI/01_OFFICIAL_PROBLEM_SPEC.md` preenchido: formulação oficial, definições mínimas (P, NP via checking relations, ≤p, NP-completude, uniformidade), equivalências (verificador/NTM, Cook–Levin, Prop. 1c), critérios exatos de solução (matemáticos + institucionais + barreiras).
5. Claims 7P-PNP-CLM-0001..0007 registrados (SOURCE_VERIFIED / FORMULATION_VERIFIED) nos ledgers local e global.

**ERRO DE IA DETECTADO E CORRIGIDO (métrica do programa):** a extração do PDF via LLM (Firecrawl query mode) (a) inventou um heading inexistente ("Feasibility Thesis" — o real é "History and Importance") e (b) omitiu o qualificador *polynomial-time computable* na Definition 3 (≤p), retornando a Definition 1 (≤m) no lugar. Ambos corrigidos por conferência verbatim com parse local (pypdf). **Lição operacional:** extração por LLM de fonte primária exige conferência verbatim mecânica antes de virar claim — regra incorporada ao método (ver SRC-0003).

**LACUNAS abertas:** equivalência verificador/NTM não reconstruída (FASE 3); provas originais Cook/Karp/Levin não verificadas (SRC-0005/6/7 A OBTER); algebrization fora do doc de Cook (FASE 4, fonte própria).

**Próxima ação proposta:** FASE 2 (fundação pedagógica de P vs NP sobre o material da spec) em paralelo com obtenção das fontes primárias SRC-0005/6/7.

---

## 2026-07-10 — CICLO 2 — FASE 2 (fundação pedagógica) + fontes primárias (autorizado por Luiz: "Sim")

**Feito:**
1. **Fontes primárias obtidas e registradas** (`_sources/` local com SHA-256; PDFs fora do git):
   - SRC-0005 Cook 1971 — 2 cópias (scan do autor + redigitação pesquisável); Summary e Theorem 1 conferidos no texto.
   - SRC-0006 Karp 1972 — 2 cópias (scan + reprint 2010); Main Theorem e 20/21 problemas via OCR; item 9 ilegível (⚠️ não preenchido de memória — regra do Ciclo 1).
   - SRC-0007 Levin 1973 — tradução integral obtida dentro de SRC-0008 (Trakhtenbrot 1984): Problems 1–6, Lemma 1 conferidos.
   - Nugget histórico verificado (SRC-0008): Levin obteve os resultados em **1971**; URSS desconhecia Cook/Karp até ≥1973 (Tsakhkadzor).
2. **FASE 2 entregue:** `PNP_AI/02_PEDAGOGICAL_GUIDE.md` (7 blocos: algoritmos/assintótica, P, NP/verificadores, reduções, NP-completude/Cook–Levin, circuitos/uniformidade/pior caso, prévia de barreiras; analogias marcadas; perguntas de compreensão) + `03_CONCEPT_GLOSSARY.md` (25 entradas com fonte) + `04_HISTORY_AND_TIMELINE.md` (marcação ✅ fonte primária / ⚠️ literatura pendente).
3. **EXP-PED-0001 executado:** redução 3-COLORING → SAT em pysat/Glucose4 (C5 e Petersen SAT com certificados conferidos independentemente; K4 UNSAT). Registrado em `PNP_AI/12_EXPERIMENTS.md` com conclusões permitidas/não permitidas. Candidato natural a primeiro lema formalizável: correção da codificação.

**Método consolidado:** hierarquia de confiança nas fontes — texto conferido mecanicamente > OCR/LLM > memória de modelo; itens não conferíveis ficam marcados ⚠️ e nunca são completados de memória.

**Bloqueios:** inalterados (OPENAI_API_KEY; importação NS-PROB).

**Próxima ação proposta:** FASE 3 (reconstrução técnica: fundamentos, Cook–Levin com prova, equivalência verificador/NTM) — inclui processar as fontes primárias obtidas.

---

## 2026-07-10 — DECISÃO — Canal OpenAI = Codex MCP (OAuth)

Luiz: "Pra que OpenAI API!? Temos integração por OAuth c/ GPT." Decisão registrada: o canal OpenAI oficial do programa é o **Codex MCP (OAuth ChatGPT, GPT-5)**, já testado. A API key direta é DESCARTADA (inválida e desnecessária); reconsiderar apenas se surgirem chamadas programáticas em lote fora do MCP. Bloqueio removido de todos os artefatos. Em seguida: sessão de perguntas sobre o guia pedagógico (FASE 2).

---

## 2026-07-10 — SESSÃO PEDAGÓGICA 1 — Perguntas essenciais do guia (Q1–Q5)

**Resultado: 5/5 corretas.** Luiz respondeu com as próprias palavras: assintótica/pior caso (Q1), resolver vs verificar + P⊆NP + pergunta como recíproca (Q2), os dois erros de "NP = exponencial" (Q3), condições para UNSAT valer como prova — incluindo, espontaneamente, certificado de insatisfatibilidade verificável independentemente (Q4), colapso via redução + composição polinomial (Q5). **Blocos 1–5 do guia consolidados.**

**Refinamentos entregues (lapidação, não correção):** justificativa formal de P⊆NP (verificador ignora certificado); assimetria SIM/NÃO da definição de NP → co-NP (FASE 3); provas DRAT como padrão de proof logging; decisão vs busca e auto-redutibilidade (FASE 3).

**Melhoria de protocolo identificada na sessão (crédito: pergunta Q4 de Luiz):** EXP-PED-0001 não emitiu prova DRAT — experimentos futuros com resultados UNSAT relevantes devem usar proof logging + checker independente. Anotado como requisito para a FASE 6.

**Pendente da sessão:** Q6–Q10 (aprofundamento) a critério de Luiz.

---

## 2026-07-10 — SESSÃO PEDAGÓGICA 2 — Aprofundamento (Q6–Q10)

**Resultado: 5/5 corretas. Placar total do guia: 10/10 — FASE 2 (trilha pedagógica, blocos 1–7) CONSOLIDADA.**

Destaques: Q6 com o detalhe "polinomial no nº de bits"; Q8 com o quantificador universal correto; Q9 reproduzindo o checklist de custos escondidos; Q10 acima do material entregue — citou o resultado completo de BGS (oráculos A e B) e a tríade de natural proofs, que o guia não continha (corretos pela literatura; marcados ⚠️ até a FASE 4 processar fontes).

**2ª contribuição metodológica de Luiz (Q10): PROTOCOLO DE TRIAGEM ANTI-BARREIRA** — checklist de 6 perguntas incorporado a `PNP_AI/07_BARRIER_MAP.md` como protocolo oficial em vigor: proposta sem respostas às 6 perguntas não passa de `HEURISTIC`.

**Refinamentos entregues:** Pratt/PRIMES ∈ NP ∩ co-NP pré-AKS; teste finito vs quantificador universal (paralelo com zeros da zeta/Riemann); ETH e fine-grained como ponte pra FASE 4; Karp–Lipton (NP ⊆ P/poly ⟹ colapso da PH) como material da FASE 3.

**Próxima ação:** FASE 3 — reconstrução técnica.

---

## 2026-07-10 — CICLO 3 — FASE 3 (reconstrução técnica, 1ª iteração) + PRIMEIRA REVISÃO ADVERSARIAL (autorizado: "Aprovo")

**Feito:**
1. **`PNP_AI/05_COMPLEXITY_FOUNDATIONS.md` criado:** TM/NTM; equivalência verificador⟺NTM com prova [RECONSTRUÇÃO]; co-NP e NP∩co-NP (TAUTOLOGY como canônico de co-NP — a forma que Cook usou!); Cook–Levin original verbatim (Theorem 1, P-reducibility = redução de Turing via query machines) + forma moderna com esboço tableau (G1–G5); auto-redutibilidade de SAT com prova; pontes não uniformes (NP⊄P/poly, Karp–Lipton ⚠️).
2. **Achado histórico verificado (SRC-0005, Theorem 2 + Remark):** Cook já em 1971 destacava {primes} e {isomorphic graph pairs} como não classificados — exatamente os dois problemas que a história confirmou como especiais.
3. **`PNP_AI/06_NP_COMPLETENESS_MAP.md` iniciado:** núcleo Cook/Karp/Levin + tabela de reduções executáveis.
4. **REV-0001 — primeiro ciclo completo proposta→revisão→gap→correção:** claim 7P-PNP-CLM-0010 (lema 3COL→SAT) enviado ao Codex/GPT-5 no formato oficial. Veredito: lógica correta (duas direções + redundância do grupo (2) confirmada), MAS **GAP_FOUND** na complexidade — "O(n+|E|)" sem fixar representação/modelo (contraexemplo: matriz de adjacência ⟹ Θ(n²); bits ⟹ Θ((n+|E|)log n)). Correção mínima aceita e incorporada. **Estado final: DERIVED_CHECKED.** O pipeline de revisão adversarial FUNCIONA — pegou um gap real que o proponente não viu.
5. Claims 0008–0012 registrados nos ledgers.

**Lição do ciclo (candidata a regra):** toda alegação de complexidade DEVE declarar modelo de máquina + representação da entrada + unidade de custo (palavras vs bits). Incorporar ao template de claim package.

**Chamadas externas do ciclo:** 1 (dentro do limite de 5).

**Próxima ação proposta:** FASE 3, 2ª iteração — hierarquia de tempo, Ladner, PH formal + Karp–Lipton com fontes; OU sessão pedagógica sobre o material técnico novo, a critério de Luiz.

---

## 2026-07-10 — CICLO 4 — FASE 3, 2ª iteração: hierarquias, Ladner, PH, Karp–Lipton (autorizado: "A")

**Fontes:**
- SRC-0009 Hartmanis–Stearns 1965 — verificado no PDF oficial da AMS (parse remoto; download local truncou 2×, arquivo A OBTER).
- SRC-0010 Arora–Barak draft 2007 (489 pp., livro reconhecido, PDF local + hash) — Thms 3.1/3.3/3.4/6.13/6.14 e Defs 5.1/5.4 conferidos verbatim. **Erratum do draft detectado** (Remark 5.5: "Πᵖ₂ = coNP", typo por Πᵖ₁) — registrado, não propagado.
- SRC-0011 Ladner (JACM 1975), SRC-0012 Stockmeyer (TCS 1976), SRC-0013 Karp–Lipton (1982): primárias A OBTER (ACM bot-block / paywalls); enunciados verificados via SRC-0010; secundária Waterloo arquivada p/ K-L.

**Conteúdo (`05_COMPLEXITY_FOUNDATIONS.md` §§6–9):** hierarquias de tempo (com prova-ideia por diagonalização) + corolário P ⊊ EXP [RECONSTRUÇÃO] — separação incondicional; Ladner com prova por padding — zona NP-intermediária (ligação com graph isomorphism, que Cook flagou em 1971); PH formal + colapso P=NP ⟹ PH=P [RECONSTRUÇÃO]; Karp–Lipton com esboço que USA a auto-redutibilidade do §5 (claims se encadeando) + variante de Meyer.

**Claims 0013–0017 registrados.** Glossário +13 entradas; timeline +4 linhas (1965 ✅, 1975 Ladner, 1976 PH, 1980/82 K-L).

**Erros de fonte detectados no ciclo (métrica):** typo no draft A-B (Remark 5.5); 2 downloads truncados detectados por parse antes de qualquer uso.

**Chamadas externas de modelo:** 0 (buscas/downloads não contam; nenhuma revisão neste ciclo).

**Próxima ação proposta:** com fundamentos prontos, FASE 4 (mapa de barreiras com fontes primárias: BGS 1975, Razborov–Rudich, Aaronson–Wigderson) — último degrau antes da FASE 5 (seleção do subproblema).

---

## 2026-07-10 — CICLO 5 — FASE 4: mapa de barreiras com fontes primárias (autorizado: "Sim")

**Fontes obtidas:**
- SRC-0015 Razborov–Rudich "Natural Proofs" (versão JCSS 1997, mirror MIT 6.875) — tríade constructivity/largeness/usefulness E Theorem 4.1 conferidos verbatim; exemplo do log discreto. (1ª tentativa no site do Razborov: 404 detectado pelo parse.)
- SRC-0016 Aaronson–Wigderson "Algebrization" (cópia do autor, 50 pp.) — abstract, definição assimétrica de algebrizes e conclusão (P vs NP exige técnicas não-algebrizantes) verbatim.
- SRC-0017 Fortnow, survey de relativization — confirma o resultado COMPLETO de BGS (dois oráculos) e a exceção histórica (provas interativas). **Upgrade do ⚠️ da Sessão Pedagógica 2:** a resposta de Luiz sobre P^B ≠ NP^B agora está verificada em fonte.
- SRC-0014 BGS primária (SIAM) segue A OBTER (paywall).

**`07_BARRIER_MAP.md` preenchido:** mecânica das três barreiras (relativization: dois mundos; natural proofs: o distinguidor autodestrutivo que quebraria PRGs; algebrization: extensões de baixo grau fechando a rota da aritmetização), o-que-bloqueia/o-que-escapa por barreira, síntese operacional, e a nuance do A-W de que certos lower bounds já superam as duas primeiras barreiras simultaneamente. Protocolo de triagem de 6 perguntas (de Luiz) mantido como cabeçalho operacional.

**Claims 0018–0020 registrados** (todos SOURCE_VERIFIED; 0018 via survey até obter a primária). Glossário +6; timeline: 3 upgrades ⚠️→✅.

**Estado do pipeline pré-FASE 5:** FASES 0–4 com entregas concluídas (FASE 1 em nível preliminar; iterações adicionais da FASE 3 sob demanda). Pronto para FASE 5 — scorecard e seleção do primeiro subproblema.

**Chamadas externas de modelo:** 0.

---

## 2026-07-10 — CICLO 6 — REV-0002: revisão Kimi do branch inteiro + correções (pedido de Luiz)

**Chamada:** Kimi (Moonshot, 2ª família de modelo usada pelo programa) revisou o diff completo do branch antes do merge. Veredito: **concern**, 12 findings. Adjudicação (revisor também é auditado — cada finding conferido contra as fontes antes de aplicar):

| # | Finding | Adjudicação | Ação |
|---|---|---|---|
| 1 | Verificação do certificado no script não confere "exatamente uma cor" | **ACEITO** | Script endurecido + re-executado (mesmos resultados) + testes negativos |
| 2 | DERIVED_CHECKED do 0010 inflado (1 família, sem humano) | **ACEITO em parte** | Estado mantido (a derivação FOI conferida adversarialmente), mas instituída a **regra de dupla família** para uso como dependência; interpretação de 09 (humano p/ candidatos a resultado) documentada |
| 3 | Estados fora da lista fechada | **ACEITO** | Convenção "ESTADO · ressalva" normalizada nos 2 ledgers |
| 4 | Enunciado de natural proofs "invertido" | **PARCIAL** — verbatim de SRC-0015 mostra que NÃO estava invertido, estava AMBÍGUO (faltava "no máximo" na dureza) | Redação precisada com a contrapositiva operacional explícita |
| 5 | Salto no esboço de Karp–Lipton (circuito decisor → circuito produtor) | **ACEITO** — lacuna técnica real | Passo search-to-decision não uniforme explicitado como lacuna a formalizar |
| 6 | Campos obrigatórios ausentes nos claims | **ACEITO com interpretação** | Registro completo instituído p/ claims DERIVADOS (0010 preenchido como exemplar); reconstruções apontam pros docs de reconstrução |
| 7 | Sem validação de entrada no script | **ACEITO** | Validação de range/laços + testes |
| 8 | Quantificadores imprecisos em P ⊊ EXP | **ACEITO** | Prova reescrita exibindo UMA L fora de P |
| 9 | Literais ≠ cláusulas (9n+6\|E\| vs 4n+3\|E\|) | **ACEITO** | Contagem de literais explicitada |
| 10 | AKS atribuído a COMPOSITES | **ACEITO** | Redação corrigida (PRIMES ∈ P; ambos por complemento) |
| 11 | Referência a 08_RESEARCH_FRONTIERS vazio | **ACEITO** | Marcado explicitamente como stub/pendente |
| 12 | Esboço Cook–Levin omite exactly-one e conversão CNF de G3 | **ACEITO** | Detalhes adicionados (pairwise + blow-up constante por janela de aridade O(1)) |

**Meta-observação:** o programa agora tem evidência empírica do valor de famílias distintas — Codex pegou um gap de complexidade que eu não vi (REV-0001); Kimi pegou 10 problemas que Codex e eu não vimos (REV-0002); e a adjudicação pegou 1 finding do Kimi que estava impreciso. Nenhuma camada sozinha bastaria.

**Chamadas externas de modelo do ciclo:** 1 (Kimi).

**Próxima ação:** merge do PR #6 (decisão de Luiz) e abertura de PR novo para a FASE 5.

---

## 2026-07-10 — CICLO 7 (início) — PR #6 MERGED · FASE 5 aberta (autorizado: "Pode")

- PR #6 mergeado na main (`e102557`) — bootstrap completo (FASES 0–4, 6 ciclos, 2 revisões externas). Branch antigo removido; novo branch `feat/7problems-fase5`.
- **Scorecard v1 criado** (`PNP_AI/09_CANDIDATE_SUBPROBLEMS.md`), estado **HEURISTIC**: 5 candidatos (C1 exact synthesis via SAT · C2 proof complexity experimental · C3 MCSP · C4 formalização Lean · C5 magnification), 8 critérios do brief, scores marcados como proposta do coordenador PENDENTE de auditoria bibliográfica real + revisão adversarial + decisão de Luiz. Liderança provisória: C1 (33/40).
- Próximos passos declarados no próprio arquivo: (1) auditoria bibliográfica de C1/C2, (2) revisão adversarial do scorecard, (3) seleção final por Luiz.

**Continuação (auditoria bibliográfica, autorizada: "Sim quero"):**
- 4 varreduras semânticas de papers + 2 inspeções profundas. Fontes SRC-0018..0023 registradas.
- **C1 confirmado como área ativa** (2009→2026) com fronteira prática calibrada (tamanho ~7 fácil / 13 = semanas) e **gap aberto concreto encontrado**: 2 classes NPN-4 sem valor exato de opt_AIG no catálogo do preprint Krinkin mar/2026 (timeout em k=9; dados públicos). DUP 3→2, INT 4→5.
- **C2:** nicho ativo (shortest DRAT do PHP; parity reordenada; CDCL vs DPLL 2026), porém mais estreito; random k-SAT experimental descartado (teoria madura, campo trilhado).
- **Scorecard v2 + proposta de seleção:** C1, com 1ª unidade de trabalho = decidir k=9 das 2 classes NPN-4 pendentes (SAT→circuito / UNSAT→DRAT), precedida de due diligence do repo de dados e checagem de que o gap segue aberto.
- Pendente: revisão adversarial da proposta (família distinta) + decisão de Luiz.

**Continuação (REV-0003, revisor escolhido por Luiz: Grok):**
- Grok 4.5 (xAI, 4ª família — 1º uso no programa) **DERRUBOU a proposta de seleção** com 11 findings. A condição de Luiz ("se ela não derrubar") ativou: seleção NÃO registrada.
- Adjudicação (em `09_CANDIDATE_SUBPROBLEMS.md`): 4 findings aceitos (confirmação do gap ANTES de selecionar; risco computacional real; auditoria assimétrica de C3/C4; começar por reprodução), 2 aceitos em parte (pesos do scorecard — agora explícitos com REL×2; valor científico — reclassificado como validação de pipeline).
- **Fato notável do scorecard v3:** mesmo com REL dobrado, C1 mantém liderança estreita (36 vs 35 vs 35) — mas a UNIDADE original (atacar o gap alheio) fica vetada na forma proposta.
- **Proposta v3:** (A) piloto imediato de pipeline — reproduzir com DRAT valores já resolvidos do catálogo NPN-4 (risco ~zero, serve a qualquer candidato); (B) auditoria profunda de C3/C4 + confirmação do gap; (C) seleção definitiva com scorecard v4.
- **Meta-observação:** 3 revisões, 3 famílias, 3 contribuições distintas — Codex (gap técnico pontual), Kimi (governança e precisão), Grok (estratégia e realismo de recursos). O custo de derrubar uma proposta na FASE 5 é horas; o custo de descobrir esses problemas na FASE 6 seria semanas.

**Chamadas externas de modelo (ciclo 7 total):** 1 (Grok). Buscas de papers não contam.

**Continuação (Etapa B, escolhida por Luiz — ordem invertida, B antes do piloto):**
- **Gap confirmado vivo** (repo krinkin/bounds: "220 exact, 2 upper bounds", commit 2026-03-10) — SRC-0027.
- **C4 rebaixado como pesquisa:** Cook–Levin já mecanizado em Coq (SRC-0024); P/NP em Mathlib sendo formalizado por terceiros AGORA (issue #35366, SRC-0025). Permanece como infra p/ claims próprios. Alerta ambiental: "provas Lean" de P≠NP E de P=NP circulando — regra do charter sobre auditoria de axiomas confirmada como necessária.
- **C3 auditado:** teoria ativa (MCSP total ainda aberto), ESP baixo confirmado; **convergência estrutural: a face experimental de C3 é C1** (catálogos exatos = dados de meta-complexidade) → REL de C1 3→4 com fonte.
- **Scorecard v4 final:** C1-restrito 38 · C2 35 · C3 33 · C4 33 · C5 27. Proposta final registrada com as salvaguardas do Grok (piloto reprodutivo primeiro; sonda k=9 só com budget+aborto aprovados).
- Aguardando decisão de Luiz (etapa C — seleção definitiva).

**Continuação (REV-0004, pedida por Luiz "pra garantir", 2026-07-11):**
- Solicitado GPT-5.6; canal Codex/OAuth rejeitou o model id (plano ChatGPT) — usado default do canal (GPT-5-based), registrado sem simulação.
- **Correção (2026-07-11, verificada com chamada real — call log #7):** o id correto do GPT-5.6 no canal Codex/ChatGPT é **`gpt-5.6-sol`** (default do `~/.codex/config.toml`). A "indisponibilidade" acima era erro de model id (`gpt-5.6`/`gpt-5.6-codex` não existem no canal), não limitação do plano. A REV-0004 permanece válida como executada.
- **Segundo DERRUBAR da FASE 5.** Codex confirmou e aprofundou a linha do Grok: seleção fechada sem executar o próprio gate; REL 3→4 revertido (relação temática ≠ avanço demonstrado); scorecard pós-hoc; e o finding metodológico mais importante do ciclo — **DRAT valida a CNF, não o encoding** — que virou regra permanente (validação semântica independente: enumeração cruzada + simulação de circuitos encontrados).
- **Proposta v5 vigente:** seleção PENDENTE; gate de qualificação PRÉ-REGISTRADO (G1 SAT + G2 UNSAT + G3 validação semântica; budget 4h/instância; estouro = falha; falha reprova C1 com dado real); pré-requisitos da seleção definitiva: alvo de C2 na mesma granularidade + busca fora da shortlist + pesos ex-ante.
- **Meta-observação:** as duas famílias (xAI e OpenAI) convergiram INDEPENDENTEMENTE na mesma direção — validar o pipeline antes de selecionar — cada uma com findings distintos e complementares. O processo da FASE 5 está funcionando exatamente como o charter desenhou: a proposta melhorou 3 versões sob fogo adversarial sem gastar um minuto de computação em alvo errado.

**Chamadas externas de modelo (acumulado FASE 5):** 2 (Grok, Codex). Dentro do limite de 5 por ciclo.

---

## 2026-07-11 — CICLO 8 — GATE DE QUALIFICAÇÃO EXECUTADO: **PASSOU** (autorizado: "Aprovo")

**Setup:** CSV do catálogo baixado (2 classes pendentes identificadas: **0x1669 e 0x166b**, ambas ub=10); kissat instalado (brew); drat-trim compilado do fonte.

**Execução (EXP-GATE-0001):**
1. **1ª rodada: REPROVADO pela validação semântica** — o assert de simulação pegou bug real no encoder (constantes 0/1 colidindo com literais DIMACS ±1). Corrigido. **O finding central da REV-0004 (DRAT ≠ validação de encoding) se provou empiricamente na primeira execução.**
2. **2ª rodada: G3 ∧ G1 ∧ G2 PASSARAM em 1,9s** (budget 4h/instância): encoder ≡ enumeração independente (n=2 completo, n=3 bidirecional k≤3); classe 0x0016 com circuito de 7 portas verificado por simulação; UNSAT k=6 com DRAT de 3,6MB verificada por drat-trim.
3. Claim **7P-PNP-CLM-0021** (opt_AIG(0x0016)=7, reprodução independente com certificados) — FINITE_SCOPE_VERIFIED.

**Consequência do pré-registro:** C1 ganha **SELEÇÃO PROVISÓRIA**; sonda k=9 nas classes 0x1669/0x166b aguarda budget + critério de aborto de Luiz. Seleção definitiva ainda exige: alvo C2 comparável, busca fora da shortlist, pesos ex-ante.

**Ferramentas novas testadas:** kissat (proof logging DRAT) + drat-trim (checker) — inventário atualizado.

---

## 2026-07-11 — CICLO 9 — EXP-PROBE-0001 CONCLUÍDO: as 2 classes pendentes FECHADAS E CERTIFICADAS

**Resultado científico (o primeiro do programa):**
- **opt_AIG(0x1669) = opt_AIG(0x166b) = 10** — claims 0022/0023 em **FINITE_SCOPE_VERIFIED**.
- Cadeia de evidência por classe: encoder validado semanticamente (G3) · UNSAT k=9 com prova DRAT verificada **2× em máquinas independentes** (Mac + pod EPYC) · circuito de 10 portas explícito conferido por simulação. Nada herdado do catálogo.
- O catálogo público de tamanhos exatos AIG das 222 classes NPN-4 fica completo (220 do autor + 2 nossos).
- A previsão de Luiz ("vai ser bem mais rápido") venceu: vereditos em 21–26 min contra timeout do autor e budget de 12h. Fator provável: quebra de simetria por deduplicação de portas.

**Infra:** pod RunPod (16c EPYC/124GB) configurado por Luiz mid-ciclo após 2 OOM locais; certificação em duplicata Mac+pod. Decisão de Luiz registrada: próxima etapa migra para VPS maior (spec com dados reais quando o escopo n=5 for definido).

**Falhas de engenharia do ciclo (todas registradas em 12_EXPERIMENTS):** 2 kills por OOM (proof logging paralelo + drat-trim em máquina de RAM curta); 1 bug de observabilidade (awk buffering engolindo eventos de monitor). Nenhuma afetou a ciência — afetaram o relógio.

**Chamadas externas de modelo:** 0 neste ciclo.

**Pendências que passam a decisão de Luiz:** (a) destino do resultado — contato com o autor do catálogo e/ou nota pública exigem autorização explícita (10_PUBLICATION_RULES); (b) conclusão formal da FASE 5 — pré-requisitos restantes da seleção definitiva (alvo C2 comparável, busca fora da shortlist, pesos ex-ante); (c) desligar o pod (custo/hora) até a próxima campanha.

---

## 2026-07-11 — CICLO 10 — Re-check de novidade (Krinkin) + fecho do lema k≤8

**Pedido de Luiz:** "faça um re-check para termos certeza (Krinkin) — use grok, glm ou kimi, o que achar melhor — 1 só."

**Escolha do revisor:** GLM-5.2 (Zhipu) — única família ainda não usada no programa (valida o canal de quebra) e formato adequado ao wrapper read-only: Claude coleta a evidência web/GitHub, o modelo externo audita o dossiê adversarialmente.

**Evidência coletada (ferramentas reais, 2026-07-11):**
- arXiv 2603.09379: SOMENTE v1 (2026-03-10), sem revisões.
- Repo krinkin/bounds: 4 commits, todos de 2026-03-10; zero issues; zero PRs.
- CSV público `data/npn4_opt_aig.csv` (HEAD): `0x1669,…,10,improved_ub` e `0x166b,…,10,improved_ub`; 220 `exact` + 2 `improved_ub`; **SHA-256 idêntico à nossa cópia local** (`5328e44f…ba49`) — sem drift de dados.
- Semantic Scholar: lista de citações VAZIA (endpoint de metadata deu 429; o de citations respondeu).
- Buscas web direcionadas (classes/valores): zero resultados além do próprio paper. Autor: Constructor University, Bremen (ResearchGate).

**REV-0005 (GLM-5.2, 1 chamada, registro em 07_MODEL_CALL_LOG):** veredito **SUSTENTADA** — "gap continua aberto; resultado novo o suficiente para contribuir ao repo do autor". Findings adjudicados:
1. Semantic Scholar era a lacuna de maior impacto → **fechada no mesmo ciclo** (0 citações).
2. Literatura clássica de exact synthesis (ABC/mockturtle, Haaswijk/Soeken) não varrida → **ressalva declarada** no ledger; varredura fica para antes de qualquer nota pública (não bloqueia contato com o autor, que pergunta e não afirma).
3. **Finding real de soundness (aceito e fechado):** encoder pergunta "exatamente k"; UNSAT k=9 não decide k≤8 sem o lema de minimalidade — que estava implícito. Resposta: lema explicitado em 12_EXPERIMENTS + **varredura empírica k=1..8: UNSAT em todos, nas duas classes** (k=8 em ≤48s; `lowk_check.py`). opt≥9 agora tem duas vias independentes.
4. Doc stale em 12_EXPERIMENTS (cabeçalho "EM ANDAMENTO", conclusões intermediárias) → **corrigido com supersessão datada**.
5. Guia para o contato com o autor: anexar circuitos + CNFs + hashes + versões + comando de regeneração; perguntar "gap ainda aberto?" antes de reivindicar; framing "fechando o gap declarado no seu abstract" (o abstract diz "220 of 222" — corrobora a leitura de gap real).

**Interpretação de `improved_ub` (risco 3 do dossiê):** corroborada pelo abstract; risco residual é o autor considerar o valor "conjecturado" — indiferente para o ato de contribuir, relevante só para a narrativa.

**Chamadas externas de modelo:** 1 (REV-0005). Limite do ciclo respeitado.

**Estado ao fim do ciclo:** re-check CONCLUÍDO com novidade SUSTENTADA; claims 0022/0023 fortalecidos (adição datada no ledger); canal GLM validado (inventário atualizado). Contato com o autor SEGUE BLOQUEADO aguardando autorização explícita de Luiz (10_PUBLICATION_RULES).

### Adendo do Ciclo 10 (2026-07-11) — CONTATO EXTERNO AUTORIZADO E EXECUTADO

**Autorização de Luiz (verbatim):** "vamos fazer a pergunta pro Krinkin primeiro certo? pode fazer" — após revisar o draft (commit `13c4684` + fix `aa6c11a`).

**Ação:** Issue aberta em `krinkin/bounds` — **https://github.com/krinkin/bounds/issues/1** — pela conta `totobusnello`. Primeiro contato externo do programa. Formato pergunta-antes-de-afirmar (REV-0005): pergunta se o gap segue aberto, oferece PR, entrega cadeia de verificação completa (hashes DRAT/CNF, circuitos + snippet de simulação, efeito no verify_all.py dele: 987→995 arestas com bound PASS) e nota de proveniência AI-assisted explícita.

**Bloqueios remanescentes:** Parte B (PR com o diff do CSV/README) aguarda resposta do autor + novo OK de Luiz. Provas grandes (4,5/3,9GB): hospedagem só se ele pedir (Zenodo vs link direto — decisão de Luiz pendente).

## 2026-07-11 — CICLO 11 — FASE 5 FORMALMENTE ENCERRADA (pré-requisitos da v5 cumpridos; C1 seleção DEFINITIVA)

**Contexto:** Luiz aprovou a fila de 5 itens ("vamos atacar a fila sugerida! qualquer coisa me chama"). Item 1: fechar a dívida de governança da FASE 5 — os 3 pré-requisitos que a REV-0004 impôs à seleção definitiva.

**Executado (registro integral em 09_CANDIDATE_SUBPROBLEMS.md, seção v6):**
- **(i) Alvo concreto de C2** formulado na mesma granularidade da Unidade 1 de C1: shortest DRAT proofs de PHP(n) (SRC-0022) — binário, verificável por drat-trim, custo horas–dias. Fica como reserva ativável.
- **(ii) Busca fora da shortlist** documentada (queries reais registradas): candidato C6 — combinatória extremal/conjecturas via SAT certificado (linha Heule/MathCheck; SRC-0028 e SRC-0029 novos no ledger). Pontuado: 27/40 — não supera a shortlist (REL=1, DUP=1: nicho dominado, provas de ~2PB fora do envelope).
- **(iii) Pesos e âncoras fixados:** REL×2, âncoras 1/3/5 por critério — vinculantes para seleções FUTURAS; limitação retrospectiva declarada explicitamente (não são ex-ante para ESTA seleção; mitigação = análise de sensibilidade).
- **Análise de sensibilidade (honesta):** C1 lidera sob pesos uniformes e REL×2; sob REL×3 há EMPATE técnico C1/C2. O scorecard não decide sozinho — o desempate é dado real vs estimativa: FER/INT de C1 MEDIDOS e ENTREGUES (gate 1,9s; sonda 21–26min; claims 0021–0023 verificados; novidade sustentada), C2 só estimado.

**SELEÇÃO DEFINITIVA: C1-restrito**, com termos consolidados: n=5 segue HIPÓTESE sujeita a benchmark + decisão de Luiz (FASE 6); ponte C1→C3 como critério de desenho; C2/C6 como reservas; pesos vinculantes daqui em diante. Sujeita a veto de Luiz.

**Chamadas externas de modelo:** 0 neste ciclo (buscas web não contam como chamadas de modelo).

## 2026-07-11 — CICLO 12 — REV-0006: claim 0010 VALIDADO pela 2ª família (GLM) — dupla família cumprida

**Item 2 da fila aprovada por Luiz.** GLM-5.2 (Zhipu) revisou adversarialmente o claim 7P-PNP-CLM-0010 (lema 3COL→SAT): **VALIDADO, 0 findings críticos/importantes, 5 MENOR** — com verificação empírica independente da aritmética (35/85/34 cláusulas e 75/180/72 literais conferidos), das duas direções da prova e da redundância do grupo (2).

**Adjudicação (5/5 aceitos, correções aplicadas e re-executadas no mesmo ciclo):** encoding p-razoável explicitado na hipótese word-RAM (F2 — o único que tocava a alegação de polinomialidade); multiarestas rejeitadas na implementação (F1); n=0 na bateria (F3); 3n variáveis explícitas (F4); F5 = estilo.

**Consequência:** claim 0010 com **dupla família CUMPRIDA** (REV-0001 OpenAI + REV-0006 Zhipu) — primeiro claim do programa **LIBERADO como dependência**. As 4 famílias adversariais (OpenAI, Moonshot, xAI, Zhipu) estão agora todas testadas e operacionais.

**Chamadas externas de modelo:** 1 (REV-0006).

## 2026-07-11 — CICLO 13 — Nota técnica escrita, revisada (REV-0007) e corrigida (v2)

**Item 4 da fila.** Nota técnica em inglês (`PNP_AI/notes/technote_npn4_gap_closure.md`): método, resultado, reprodutibilidade e efeito no catálogo — primeiro manuscrito do pipeline de publicação do programa.

**Processo (como planejado — revisão adversarial ANTES de Luiz ver):** v1 → REV-0007 (Codex/gpt-5.6-sol): **NEEDS_REVISION, 14 findings (6 MAJOR)** → todos aceitos → v2. Os MAJOR renderam correções que TRANSBORDARAM da nota para os registros internos:
1. **Lema de minimalidade/normalização completado** (v1 omitia fan-ins iguais e o argumento de redirecionamento de fanouts) — agora enunciado com esboço de prova na §2.1 da nota.
2. **Varredura k=1..8 reclassificada:** não é via independente do lema e não tem DRAT — é sanity check. Correção datada aplicada TAMBÉM no 12_EXPERIMENTS (a formulação "duas vias independentes" do Ciclo 10 era imprecisa).
3. **Rerun do verify_all arquivado como experimento** (`experiments/exp_verify_rerun/`): diff de 2 linhas, snapshot do script do autor, saída integral (987→995 edges, PASS), hashes — baseline reproduz o Expected output do autor.
4. **Unidades corrigidas nos registros:** provas = 4.785.094.117 e 3.871.475.211 bytes (o "4,5GB" era GiB rotulado como GB).
5. **Proveniência honesta:** kissat do Mac é brew (não source); commit do drat-trim do pod não registrado — gap DECLARADO na nota em vez de encoberto.
6. Codex confirmou empiricamente os números centrais (vars/cláusulas, testemunhas, tempos, hashes): "most numerical claims check out".

**Estado:** nota v2 pronta para leitura de Luiz. Preprint/publicação seguem bloqueados (10_PUBLICATION_RULES).

**Chamadas externas de modelo:** 1 (REV-0007).

## 2026-07-11 — CICLO 14 — Plano da FASE 6 (n=5) + spec provisória de infra — PROPOSTA a Luiz

**Item 5 da fila (último).** `PNP_AI/13_FASE6_PLAN.md`: números honestos de escala (616.126 classes; teto ingênuo 29 anos-core, piso 71 dias-core — a distribuição real é DESCONHECIDA), 4 recortes científicos (A catálogo completo / B parcial curado / C dataset ponte C1→C3 / D outras bases em n=4), **piloto de medição pré-registrado** (300 classes uniformes + 16 simétricas, busca ascendente sem proof logging, timeout 2h/classe, budget 72h no pod ≈ US$ 46, aborto pré-registrado), spec de infra provisória com regra de decisão (pod sob demanda vs dedicado mensal, ponto de equilíbrio ~700 h-core) e a lista explícita do que fica com Luiz: aprovar piloto, escolher recorte após os dados, contratar infra, publicar.

**Recomendação do coordenador:** recorte C (dataset meta-complexidade) como espinha dorsal com B como subproduto — é o que serve à seleção definitiva de C1 (ponte C1→C3).

**REV-0004 honrada:** nenhum compromisso com n=5 assumido — tudo condicionado ao piloto.

**Issue Krinkin (#1):** checada neste ciclo — sem resposta ainda.

**Chamadas externas de modelo:** 0 neste ciclo.

**FILA DE LUIZ (aprovada 2026-07-11) — STATUS FINAL: 5/5 CONCLUÍDA.** (1) FASE 5 encerrada, C1 definitivo; (2) claim 0010 dupla família cumprida; (3) PR #7 mergeado, branch fase6 aberto; (4) nota técnica v2 revisada; (5) plano FASE 6 proposto.

## 2026-07-11 — CICLO 15 — PILOTO n=5 LANÇADO (320 classes, 16 workers no pod re-provisionado)

**Autorização:** Luiz respondeu ao checkpoint da FASE 6 fornecendo o SSH do pod re-provisionado (endpoint novo) — interpretado como aprovação do piloto pré-registrado (budget 72h ≈ US$ 46).
**Antes de rodar:** pré-gate n=3 COMPLETO passou (256/256, bidirecional, k≤4) + Emenda 1 ao plano registrada ANTES da execução (amostragem uniforme-sobre-funções com pesos HT; 64 simétricas → 20 classes; correções datadas).
**Execução:** amostra de 320 classes (seed=20260711), 16 shards, 16 workers paralelos, lançados 16:35 UTC. Smoke test local: 0x00000001 → opt=4 (AND de 5 entradas, correto). Stack do pod reinstalado do fonte com commits REGISTRADOS (fecha o gap de proveniência da REV-0007 p/ execuções futuras).
**Chamadas externas de modelo:** 0.

## 2026-07-11 — CICLO 16 — REV-0008 (Kimi): "concern" no runner do piloto — 2 bugs operacionais corrigidos EM VOO

**Contexto:** Luiz pediu paralelização + review do Kimi. 1ª tentativa via subagente morreu no teto de ~10min do Bash de subagente (turn.cancel aos 11min); 2ª tentativa manual falhou por CLAUDE_PLUGIN_DATA ausente (MESMA pegadinha da REV-0002 — anotada mas não operacionalizada). Resposta estrutural: **`tools/rev.sh`** (lançador único dos 4 canais com pre-flight `doctor`) + HARD RULE no CLAUDE.md do projeto + memória persistente. 3ª tentativa (background da sessão principal, env correto): SUCESSO.

**REV-0008 (Kimi, kimi-for-coding, thinking high): veredito "concern", 5 findings.** Ciência confirmada correta (canonicalização NPN 7.680 transformações ✓, encoding ✓, direção dos pesos HT ✓). Adjudicação:
- **F1 (MEDIUM, ACEITO+CORRIGIDO):** budget da classe não recontava o tempo de encode/escrita do CNF antes do kissat — em k alto o kissat estourava o budget, e no pior caso `subprocess.run(timeout<=0)` derrubaria o shard inteiro. Corrigido (recomputa+clampa) — runner v2.
- **F2 (MEDIUM, ACEITO+CORRIGIDO):** `assert` de verificação e parse frágil de modelo abortavam o shard; agora falha vira registro recuperável (`error`) e o loop continua — runner v2.
- **F3 (MEDIUM, ACEITO+EM EXECUÇÃO):** varredura k=1..8 do n=4 sem DRAT quando certificar é barato — `cert_lowk.py` lançado (prova→check→hash→apaga, 16 execuções).
- **F4 (LOW, ACEITO+CORRIGIDO):** tempos por k não incluíam encode — agora `enc_times` separado (extrapolação de custo fica honesta).
- **F5 (LOW, ACEITO, documentado):** pesos HT são aproximação sob o desenho "sorteia até 300 distintas" — ok para distribuições (constante cancela); totais exigem normalização. Vai declarado na análise.

**Redeploy em voo com resume:** pod e Mac migrados pro runner v2 (classes concluídas preservadas). Dois incidentes operacionais no redeploy, ambos diagnosticados e corrigidos: pkill remoto auto-casou com o próprio `bash -c` (matou a sessão antes de relançar — padrão `pilot_[r]un.py` resolve) e pkill local não pegou os PIDs antigos do Mac (kill explícito).

**Alerta de segurança do plugin (para Luiz):** o safety hook do kimi-plugin-cc está com path drift (aponta pra versão antiga do cache) — sem ele, o modo `-p` do kimi-code auto-aprova QUALQUER tool call, incluindo Write/Bash, mesmo em comandos documentados como read-only. Recomendação: rodar `/kimi:setup` para re-pinar. Até lá, chamadas kimi só nos modos read-only e com diff conferido.

**Chamadas externas de modelo:** 1 (REV-0008; as 2 tentativas falhas não geraram chamada faturável — morreram antes/no transporte).

### Adendo do Ciclo 16 — "kimi setup" resolvido: era falso positivo, correção foi no NOSSO lançador

Pedido de Luiz: "resolve o kimi setup pra mim". Diagnóstico com o `setup --check` do próprio plugin, rodado do root CORRETO (cache versionado 1.5.0): **hook instalado, probe passou** ("deny reason captured" — o hook nega Bash em modo review como deve), node pinado existe, review gate no default. O warning de "path drift" da REV-0008 foi **falso positivo do nosso lançamento** (root do marketplace ≠ root pinado no config) — e, pior, aquele run rodou SEM hook ativo. Auditoria do working tree pós-REV-0008: nenhuma escrita inesperada (kimi comportou-se read-only).

**Correções:** `tools/rev.sh` agora resolve o root do plugin dinamicamente pelo cache versionado (à prova de update do plugin) e o `doctor` ganhou o probe do hook como check obrigatório. Config do Luiz: intocada (não precisou de /kimi:setup).

## 2026-07-11 — CICLO 17 — SRC-0032 ("The Unit Gap", Krinkin): Teorema 2, Corolário 6 e Teorema 7 REFUTADOS (claims 0024/0025)

**Origem:** leitura pré-campanha do 2º paper do autor do catálogo (obrigação da Emenda 2). O abstract afirma gap(fórmula, circuito) ∈ {0,1} para TODA função booleana na base AIG — em tensão direta com separações clássicas. Leitura verbatim (pypdf) localizou a causa: a identidade do §2 usa opt (circuitos) nos filhos onde a recursão de fórmula exige tree (árvores).

**Contraexemplo (⊕₃, verificado mecanicamente, artefatos em `experiments/exp_unitgap_check/`):**
- opt(⊕₃)=6: UNSAT@5 com DRAT "s VERIFIED" + testemunha de 6 portas simulada. tree(⊕₃)=9 pelo DP exato de ponto fixo (256 funções); sanduíche independente do DP: Khrapchenko ⟹ ≥8, construção explícita ⟹ ≤9. **gap ∈ {2,3} ∌ {0,1}** — Teorema 2 falso sob a definição que o próprio paper enuncia.
- A Tabela 1 do paper lista "2 funções gap=1 em opt=6" no n=3 completo — são exatamente ⊕₃ e ¬⊕₃, cujo gap real é 3: o experimento dele computou a grandeza errada (tree_oneshot), não formula size.
- **REV-0009 (Grok, via rev.sh): SUSTENTADA** — e derivou refutação ADICIONAL, independente da disputa de definição: s=3 no circuito ótimo de ⊕₃ (filhos da saída compartilham as 3 portas de x1⊕x2; 1+4+4−3=6 conferido com opt(filho)=4, UNSAT@3 DRAT) ⟹ Corolário 6 (s∈{0,1}) e Teorema 7 caem juntos. Teoremas 3 e 4 SOBREVIVEM.

**Claims:** 7P-PNP-CLM-0024 (gap≥2/=3) e 0025 (s=3) — COMPUTATIONALLY_TESTED, 1 família revisou (Grok); **regra de dupla família pendente** antes de qualquer comunicação técnica formal. SRC-0032 marcado GAP_FOUND no source ledger (não usar Thm2/Cor6/Thm7 como dependência).

**Também neste ciclo:** cadeia k=1..9 do resultado 0x1669/0x166b ficou 100% DRAT-certificada (16/16 "s VERIFIED", fecho do F3 da REV-0008).

**Decisão que passa a Luiz:** comunicar (ou não) o achado ao autor — sensível: temos issue amigável aberta no outro repo dele. Recomendação do coordenador: 2ª revisão de família antes (Codex ou Kimi, 1 chamada), e só então decidir o canal/tom.

**Chamadas externas de modelo:** 1 (REV-0009).

## 2026-07-11 — CICLO 18 — REV-0010 (gpt-5.6-sol): refutação SUSTENTADA pela 2ª família — dupla família CUMPRIDA nos claims 0024/0025

**Pedido de Luiz:** "gpt-5.6-sol roda". Codex revisou adversarialmente com re-derivação independente: enumeração própria por camadas confirmou **tree(⊕₃)=9 exato** (⊕₃/¬⊕₃ são as duas únicas funções de custo 9 em n=3); re-executou os UNSATs; auditou o DP e a aplicação de Khrapchenko; confirmou s=3 e o Cor. 6 falso (e de quebra: o Remark 5 do paper — optimal substructure — também falha com portas compartilhadas).

**Refinamentos adjudicados (ambos aceitos, ledger corrigido com data):**
1. **Thm 7:** ⊕₃ (gap 3) não satisfaz a hipótese "gap=1" do enunciado condicional — logo não o refuta sob a definição padrão; o que se estabelece é: prova INVALIDADA (usa Cor. 6), alegação universal FALSA, e contradição direta sob a grandeza que o autor computou. Claim 0025 precisado.
2. **Thm 3:** furo de contagem na prova publicada (|S|≥k−1 falha quando g é porta de entrada); prova corrigida fornecida (contagem de fan-out, 2m≥n+m ⟹ m≥n, para todo gap>0). Material adicional para eventual comunicação.

**Fecho de reprodutibilidade (F5):** CNF+DRAT de ⊕₃@k=5 e do filho@k=3 arquivados permanentemente em `exp_unitgap_check/certs/` — regeneração byte-idêntica (hashes iguais aos da 1ª execução).

**Estado final do pacote Unit Gap:** Thm 2 e Cor. 6 REFUTADOS (dupla família: Grok + Codex, ambas SUSTENTADA); Thm 7 sem prova e com alegação universal falsa; Thms 3–4 sobrevivem (Thm 3 com prova corrigida nossa). Claims 0024/0025 liberados como dependência. **Comunicação ao autor: DESBLOQUEADA pela governança, aguardando decisão de Luiz** (recomendação: draft respeitoso, mesmo tom da issue #1, possivelmente aguardando a resposta dele lá).

**Chamadas externas de modelo:** 1 (REV-0010).
