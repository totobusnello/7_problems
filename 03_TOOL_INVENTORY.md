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
| sympy | **INDISPONÍVEL** (instalável) | `pip3 install sympy` — aprovar na Sessão 1 |
| scipy / networkx | **INDISPONÍVEL** (instalável) | `pip3 install scipy networkx` |
| SAT solvers (pysat, minisat, cryptominisat, kissat) | **INDISPONÍVEL** (instalável) | `pip3 install python-sat` + `brew install cryptominisat kissat` |
| SMT solver Z3 | **INDISPONÍVEL** (instalável) | `pip3 install z3-solver` |
| SMT solver cvc5 | **INDISPONÍVEL** (instalável) | `brew install cvc5` |
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
| OpenAI API direta | **PRECISA DE CONFIGURAÇÃO HUMANA** | `OPENAI_API_KEY` do `~/.zshrc` retornou `invalid_api_key` em 2026-07-10. Renovar key. Registrado em `07_MODEL_CALL_LOG.md` |
| OpenAI via Codex MCP | **DISPONÍVEL E TESTADA** | Chamada real 2026-07-10: identifica-se como "Codex, an OpenAI agent based on GPT-5"; contexto isolado confirmado; apto a referee adversarial |
| Kimi (Moonshot) | **DISPONÍVEL, AINDA NÃO TESTADA** | `/kimi:{review,challenge,ask}` — OAuth ativo |
| GLM-5.2 (Zhipu) | **DISPONÍVEL, AINDA NÃO TESTADA** | wrapper `~/Claude/scripts/glm`, read-only |
| Grok 4.5 (xAI) | **DISPONÍVEL, AINDA NÃO TESTADA** | wrapper `~/Claude/scripts/grok`, pay-as-you-go |

4 famílias de treino independentes de Claude (OpenAI, Moonshot, Zhipu, xAI) → revisão adversarial multi-modelo é viável hoje.

## Gaps prioritários para a Sessão 1

1. Renovar `OPENAI_API_KEY` (ação de Luiz) — ou padronizar Codex MCP como canal OpenAI.
2. Instalar camada matemática Python: `sympy scipy networkx z3-solver python-sat` (leve, sem custo).
3. Decidir sobre Lean 4 + Mathlib (formalização progressiva de PNP-AI).
4. Testar pipeline de papers (arXiv → parse → source ledger) com o artigo math/0306075.
