# 07 — MODEL CALL LOG — Registro de chamadas reais a modelos externos

> Regra: não simular chamadas. Toda chamada real é registrada aqui (canal, modelo, propósito, resultado). Limite: máximo 5 chamadas externas por ciclo sem autorização.

| # | Data | Canal | Modelo | Propósito | Resultado |
|---|---|---|---|---|---|
| 1 | 2026-07-10 | OpenAI API (`/v1/chat/completions`, key do `~/.zshrc`) | gpt-5.2 (tentado) | Teste de integração da Sessão 0 | **FALHA** — `invalid_api_key` (sk-proj-…t1QA rejeitada). Estado: AGUARDANDO INTEGRAÇÃO (renovar key). `/v1/models` também retornou vazio. |
| 2 | 2026-07-10 | Codex MCP (auth ChatGPT, sandbox read-only) | "Codex, an OpenAI agent based on GPT-5" (auto-identificação) | Mesmo teste, canal alternativo | **SUCESSO** — confirmou: (1) identidade GPT-5/Codex; (2) mensagem recebida standalone, sem contexto desta conversa; (3) YES para atuar como referee adversarial de claim packages. threadId 019f4e90-cb71-7da0-92b0-e37be28b4e20. |
| 3 | 2026-07-10 | Codex MCP (read-only) | Codex/GPT-5 | **REV-0001** — primeira revisão adversarial real: claim package 7P-PNP-CLM-0010 (lema 3COL→SAT), protocolo oficial completo | **SUCESSO — GAP_FOUND na parte (b):** lógica (a) validada nas duas direções (incl. confirmação da redundância do grupo (2)); contagem 4n+3\|E\| confirmada; alegação de tempo O(n+\|E\|) corretamente contestada — depende de representação (lista de arestas vs matriz Θ(n²)) e modelo (word-RAM vs bits: Θ((n+\|E\|)log n)). Contraexemplo concreto (grafo vazio em matriz de adjacência). Hipóteses ausentes apontadas: representação, codificação, modelo, convenção n=0. Correção mínima proposta e ACEITA. Confiança: alta. threadId 019f4ec6-2429-79d3-b6b1-1ef528365c14. |

## Pacote que teria sido enviado pela API direta (registrado conforme protocolo de falha)

```
Integration test for a mathematical review pipeline. Reply with exactly:
(1) your model identity, (2) confirmation you received this as a standalone
message with no prior conversation context, (3) YES/NO whether you could
analyze a structured mathematical claim package (statement, hypotheses,
proof sketch, complexity claims). Max 60 words.
```

| 4 | 2026-07-10 | Kimi plugin (kimi-review, read-only, agente ad1d5de7ac95ad3ac) | Kimi (Moonshot) | **REV-0002** — revisão adversarial do DIFF COMPLETO do branch (10 commits, 33+ arquivos) antes do merge do PR #6 | **SUCESSO — veredito "concern", 12 findings** (6 importantes + 6 menores). Adjudicação completa no RESEARCH_LOG (Ciclo 6): 10 aceitos e corrigidos; 1 parcialmente aceito (finding 4 alegou inversão do Thm 4.1 de RR — o verbatim mostra que era AMBIGUIDADE, não inversão; redação precisada); 1 aceito com interpretação (finding 6 — registro completo instituído para claims derivados). Gerou 2 regras novas: convenção de Estado com lista fechada + regra de dupla família para dependências. Nota operacional: wrapper exigiu `CLAUDE_PLUGIN_DATA` manual. |

| 5 | 2026-07-10 | Grok wrapper (grok-adversary, read-only, agente a280c8bae549893ff) | Grok 4.5 (xAI) | **REV-0003** — challenge adversarial da proposta de seleção da FASE 5 (C1 + unidade "2 classes NPN-4") | **SUCESSO — veredito DERRUBAR, 11 findings.** Principais: ponderação executabilidade>relevância; INT inflado; dependência de preprint único sem confirmar gap vivo; capacidade computacional irreal (timeout do próprio autor; sem stack cube-and-conquer); auditoria assimétrica (C3/C4 sem profundidade); valor científico modesto. Recomendou C2 ou C4; se C1, reproduzir classe já resolvida com DRAT + critérios de aborto. Adjudicação: 4 aceitos, 2 aceitos em parte → proposta v3 (piloto reprodutivo + auditoria C3/C4 + seleção definitiva depois). Registro em `PNP_AI/09_CANDIDATE_SUBPROBLEMS.md`. |

## Canais adversariais disponíveis (ainda não usados)

GLM-5.2 (Zhipu) — wrapper read-only configurado. Candidato natural para a 2ª revisão do claim 0010 (regra de dupla família).
