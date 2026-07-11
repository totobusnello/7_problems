# 7_problems — notas operacionais

## ⚠️ HARD RULE — Lançamento de revisores externos (2026-07-11, após 4 falhas recorrentes)

- **TODO revisor externo (kimi/codex/glm/grok) é lançado via `tools/rev.sh <canal> ...`** — nunca comando manual re-derivado (env vars e model ids corretos moram NO script, não em notas).
- **Antes do primeiro lançamento da sessão: `tools/rev.sh doctor`** (valida os 4 canais sem gastar tokens).
- **Chamadas longas (kimi review/challenge, codex exec) rodam da SESSÃO PRINCIPAL com `run_in_background: true`** — NUNCA via Bash de subagente (teto ~10min mata a chamada no meio; aconteceu 2026-07-11).
- Falhas que motivaram a regra: `CLAUDE_PLUGIN_DATA` faltando 2× (REV-0002 e 2026-07-11), `gpt-5.6` vs `gpt-5.6-sol`, timeout de subagente matando o Kimi aos 12min.

## Canal OpenAI (Codex)

- A OpenAI API key do `~/.zshrc` está **INVÁLIDA** — usar o **Codex MCP/CLI** (auth ChatGPT) como canal OpenAI.
- **GPT-5.6 no Codex: o model id é `gpt-5.6-sol`** (já é o default do `~/.codex/config.toml`, reasoning high). Os ids `gpt-5.6` e `gpt-5.6-codex` são **rejeitados** (400) no plano ChatGPT — não concluir "indisponível" por causa deles (verificado 2026-07-11, call log #7).
- Na prática: **omitir o model id** nas chamadas ao Codex já usa o modelo certo.

## Regras do projeto (lembretes)

- Toda chamada real a modelo externo é registrada em `07_MODEL_CALL_LOG.md` — nunca simular chamadas.
- Governança de claims: correções são aditivas e datadas; não reescrever registros históricos.
