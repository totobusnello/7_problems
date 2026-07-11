# 03 — TOOL INVENTORY — Inventário real de ferramentas

> Testado em: 2026-07-10 (Sessão 0), macOS (darwin 25.6.0), ambiente Claude Code / Claude Fable 5.
> Classificações: DISPONÍVEL E TESTADA · DISPONÍVEL, AINDA NÃO TESTADA · PRECISA DE CONFIGURAÇÃO HUMANA · INDISPONÍVEL.
> Regra: não simular ferramentas indisponíveis; não simular chamadas a outras LLMs.

## Núcleo de execução

| Ferramenta | Estado | Detalhe |
|---|---|---|
| Python | **DISPONÍVEL E TESTADA** | 3.14.3, pip 26.0 |
| numpy | **DISPONÍVEL E TESTADA** | 2.4.4 |
| matplotlib | **DISPONÍVEL E TESTADA** | 3.10.9 |
| Node.js | **DISPONÍVEL E TESTADA** | v24.13.0 |
| Git | **DISPONÍVEL E TESTADA** | 2.50.1 + gh CLI 2.95.0 |
| Armazenamento persistente | **DISPONÍVEL E TESTADA** | Filesystem local + repo GitHub (totobusnello/Claude) |
| Logs completos / ambientes reproduzíveis | **DISPONÍVEL, AINDA NÃO TESTADA** | Convenções definidas nos artefatos; primeiro experimento validará |

## Matemática simbólica e solvers

| Ferramenta | Estado | Ação |
|---|---|---|
| sympy 1.14.0 | **DISPONÍVEL E TESTADA** (2026-07-10, autorizado por Luiz) | instalada via pip |
| scipy 1.18.0 / networkx 3.6.1 | **DISPONÍVEL E TESTADA** (2026-07-10) | instaladas via pip |
| SAT solver pysat (Glucose4) | **DISPONÍVEL E TESTADA** (2026-07-10) | smoke test real: modelo SAT retornado |
| SMT solver Z3 4.16.0 | **DISPONÍVEL E TESTADA** (2026-07-10) | smoke test real: modelo SAT retornado |
| pypdf | **DISPONÍVEL E TESTADA** (2026-07-10) | usada na verificação verbatim do PDF oficial de P vs NP |
| kissat (nativo, com proof logging DRAT) | **DISPONÍVEL E TESTADA** (2026-07-11, EXP-GATE-0001) | UNSAT k=6 com emissão de prova DRAT |
| drat-trim (checker independente de provas) | **DISPONÍVEL E TESTADA** (2026-07-11) | compilado do fonte (marijnheule/drat-trim); "s VERIFIED" no gate |
| cryptominisat | **INDISPONÍVEL** (instalável) | `brew install cryptominisat` — se precisar de 2º solver |
| **Pod RunPod dedicado (compute)** | **DISPONÍVEL E TESTADA** (2026-07-11, configurado por Luiz) | AMD EPYC 4564P 16 cores / 124GB RAM / 100GB disco / Ubuntu 24.04 · $0,64/h · SSH root@157.157.221.177:24959 · Stack instalado: kissat (source), CaDiCaL 3.0 (rota LRAT), drat-trim + lrat-check, Python 3.12 · tools em /workspace/tools · **desligar quando ocioso** |
| **VPS maior (próxima etapa — decisão de Luiz 2026-07-11)** | PLANEJADA | Após fechar as tarefas atuais, migrar p/ VPS com mais CPUs/RAM. Dimensionamento com dados reais de n=4 (21–26min/classe em k=9, 1 core): p/ n=5 (616.126 classes NPN) o gargalo é CORES × single-thread + RAM p/ verificação de provas. Especificar quando o escopo n=5 for definido (FASE 6) |
| SMT solver cvc5 | **INDISPONÍVEL** (instalável) | `brew install cvc5` — segunda opinião de solver |
| CAS SageMath | **PRECISA DE CONFIGURAÇÃO HUMANA** | Instalação pesada (~1GB+); avaliar necessidade real antes |

## Verificadores formais

| Ferramenta | Estado | Ação |
|---|---|---|
| Lean 4 + Mathlib | **INDISPONÍVEL** (instalável) | `elan` toolchain; Mathlib tem `Mathlib.Computability` (TMs, P, NP parciais) — melhor candidato p/ PNP-AI |
| Coq / Rocq | **INDISPONÍVEL** (instalável) | Alternativa; menor prioridade inicial |
| Isabelle | **INDISPONÍVEL** (instalável) | Alternativa; menor prioridade inicial |

## Pesquisa acadêmica

| Ferramenta | Estado | Detalhe |
|---|---|---|
| Pesquisa web | **DISPONÍVEL E TESTADA** | Firecrawl (search/scrape/crawl) + WebSearch nativo |
| Busca de papers (arXiv+) | **DISPONÍVEL, AINDA NÃO TESTADA** | Firecrawl research tools (search_papers, read_paper, related_papers via citation graph) |
| Leitura de PDFs | **DISPONÍVEL E TESTADA** | Read nativo + firecrawl_parse |
| Crossref / Semantic Scholar | **DISPONÍVEL, AINDA NÃO TESTADA** | APIs públicas via HTTP |
| MathSciNet / zbMATH | **PRECISA DE CONFIGURAÇÃO HUMANA** | Exigem assinatura institucional — Luiz decide se contrata |

## Integração de modelos (revisores independentes reais)

| Canal | Estado | Detalhe |
|---|---|---|
| OpenAI via Codex MCP (OAuth ChatGPT) | **DISPONÍVEL E TESTADA — CANAL OFICIAL** | Decisão de Luiz (2026-07-10): este é o canal OpenAI do programa. Chamada real: identifica-se como "Codex, an OpenAI agent based on GPT-5"; contexto isolado confirmado; apto a referee adversarial |
| OpenAI API direta (key) | **DESCARTADA POR DECISÃO** (2026-07-10) | Key do `~/.zshrc` inválida E desnecessária — OAuth via Codex cobre o caso de uso. Reconsiderar só se surgirem chamadas programáticas em lote fora do MCP |
| Kimi (Moonshot) | **DISPONÍVEL, AINDA NÃO TESTADA** | `/kimi:{review,challenge,ask}` — OAuth ativo |
| GLM-5.2 (Zhipu) | **DISPONÍVEL E TESTADA** (2026-07-11, REV-0005) | wrapper `~/Claude/scripts/glm`, read-only; auditoria do re-check Krinkin |
| Grok 4.5 (xAI) | **DISPONÍVEL, AINDA NÃO TESTADA** | wrapper `~/Claude/scripts/grok`, pay-as-you-go |

4 famílias de treino independentes de Claude (OpenAI, Moonshot, Zhipu, xAI) → revisão adversarial multi-modelo é viável hoje.

## Gaps prioritários (atualizado 2026-07-10, pós-Ciclo 2)

1. ~~OPENAI_API_KEY~~ **RESOLVIDO por decisão:** Codex MCP (OAuth) é o canal OpenAI oficial do programa.
2. ~~Camada matemática Python~~ **FEITO:** sympy, z3, pysat, networkx, scipy, pypdf instalados e testados.
3. Decidir sobre Lean 4 + Mathlib (formalização progressiva de PNP-AI) — proposta na FASE 3.
4. ~~Pipeline de papers~~ **VALIDADO** no Ciclo 2 (busca → download → parse local → conferência verbatim → ledger); falta aplicar ao artigo math/0306075 (NS-PROB).
5. OCR local (tesseract) para conferência verbatim de scans (Karp) — instalar quando a FASE 3 precisar.
