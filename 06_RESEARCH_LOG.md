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

---
