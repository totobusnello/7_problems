# 7_problems — notas operacionais

## Canal OpenAI (Codex)

- A OpenAI API key do `~/.zshrc` está **INVÁLIDA** — usar o **Codex MCP/CLI** (auth ChatGPT) como canal OpenAI.
- **GPT-5.6 no Codex: o model id é `gpt-5.6-sol`** (já é o default do `~/.codex/config.toml`, reasoning high). Os ids `gpt-5.6` e `gpt-5.6-codex` são **rejeitados** (400) no plano ChatGPT — não concluir "indisponível" por causa deles (verificado 2026-07-11, call log #7).
- Na prática: **omitir o model id** nas chamadas ao Codex já usa o modelo certo.

## Regras do projeto (lembretes)

- Toda chamada real a modelo externo é registrada em `07_MODEL_CALL_LOG.md` — nunca simular chamadas.
- Governança de claims: correções são aditivas e datadas; não reescrever registros históricos.
