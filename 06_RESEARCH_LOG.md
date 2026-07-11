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
