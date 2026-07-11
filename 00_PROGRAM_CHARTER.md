# 00 — PROGRAM CHARTER — 7_PROBLEMS

> AI-Assisted Research Program for the Millennium Prize Problems
> Responsável humano: Luiz Antonio Busnello · Coordenador inicial: Claude Fable 5
> Criado: 2026-07-10 (Sessão 0) · Fonte: 7_PROBLEMS Project Brief (docx)

## Missão

Construir um sistema rigoroso de pesquisa matemática assistida por IA para estudar os sete Problemas do Milênio, identificar quais subproblemas são mais compatíveis com as ferramentas atuais e tentar produzir resultados matemáticos novos, verificáveis e úteis.

- **Objetivo máximo:** contribuir para a solução de um dos Problemas do Milênio.
- **Objetivo operacional:** avanços intermediários reais — lemas, lower bounds, algoritmos, formulações, contraexemplos, classificações de barreiras, formalizações, resultados parciais publicáveis, infraestrutura reutilizável.

## Escopo e prioridades

| Prioridade | Frente | Papel |
|---|---|---|
| 1 | **PNP-AI** (P versus NP) | Primeiro laboratório AI-first |
| 2 | **NS-PROB** (Navier–Stokes) | Segunda frente estratégica; origem pessoal do projeto (artigo Busnello–Flandoli–Romito, arXiv math/0306075) |
| 3 | **COMPARATIVE MAP** | Mapear os demais problemas e reavaliar compatibilidade AI-first periodicamente |

Não iniciar pesquisa profunda simultânea nos demais problemas durante a primeira fase.

## Hipóteses estratégicas

1. **Diferentes problemas exigem diferentes arquiteturas de IA** — não existe metodologia única para os sete.
2. **P versus NP é o melhor primeiro laboratório AI-first** — objetos discretos, representação finita, testes exatos, SAT/SMT, proof assistants. Hipótese de adequação metodológica, NÃO de menor dificuldade matemática.
3. **Navier–Stokes é a vantagem particular de Luiz** — origem pessoal, artigo-base delimitado, linha probabilística concreta, possibilidade futura de revisão por especialistas próximos.

## Estrutura em 4 níveis

- **Nível 1 — 7_PROBLEMS CORE:** governança, bibliografia, integração de modelos, claim ledger, verificação, formalização, versionamento, revisão humana.
- **Nível 2 — Projetos por problema:** PNP_AI, NS_PROB, RH_AI, BSD_AI, HODGE_AI, YM_AI, POINCARE_CASE.
- **Nível 3 — Linhas de pesquisa** dentro de cada problema.
- **Nível 4 — Unidades de trabalho:** cada ciclo investiga UMA definição/conjectura/lema/estimativa/algoritmo/barreira/contraexemplo/dependência formal por vez.

## Regras de governança científica (invioláveis)

1. Correção matemática vem antes de novidade.
2. Concordância entre LLMs não é prova; resposta convincente não é evidência de validade.
3. Simulações e verificação finita não demonstram enunciados universais.
4. Ausência de resultados em busca bibliográfica não prova novidade.
5. Nenhum modelo inventa referências, teoremas, citações, páginas ou resultados.
6. Toda afirmação relevante recebe Claim ID (`7P-[PROBLEM]-CLM-[NUMBER]`) com enunciado exato, hipóteses, conclusão, dependências, origem, estado de verificação, críticas e testes.
7. O projeto tenta refutar as próprias ideias antes de promovê-las.
8. Resultado produzido por IA nasce como CONJECTURA ou demonstração candidata.
9. Histórico de erros, refutações e resultados negativos é preservado — nada é apagado ou reformulado silenciosamente.
10. Um problema principal por vez; dentro dele, um gargalo intermediário por vez.
11. Nenhuma alegação de solução é publicada sem: prova completa + revisão humana especializada + verificação de dependências + comparação com a literatura + auditoria de ferramentas + regras do Clay Mathematics Institute.

## Papéis (processos/chamadas realmente independentes)

COORDENADOR · PROPONENTE · REVISOR ADVERSARIAL · REVISOR BIBLIOGRÁFICO · REVISOR FORMAL · REVISOR COMPUTACIONAL.
O mesmo modelo não finge executar várias revisões independentes numa única resposta.
Revisores externos disponíveis: Codex/GPT-5 (MCP, testado), Kimi, GLM-5.2, Grok 4.5 (wrappers read-only).

## Limites de autonomia — parar e pedir autorização de Luiz antes de:

Contatar Barbara Busnello ou qualquer pesquisador · enviar e-mail · divulgar/publicar/submeter · anunciar avanço · declarar problema resolvido · executar gastos ou adicionar serviços pagos · alterar o problema principal · iniciar pesquisa profunda em outro problema · apagar/sobrescrever registros · >5 chamadas externas de modelos por ciclo · iniciar formalização de grande escala.

**Nunca enviar mensagens ou materiais externamente sem autorização explícita de Luiz.**

## Critérios de sucesso (métricas válidas além da solução final)

Formulações oficiais reconstruídas · fontes verificadas · definições formalizadas · provas conhecidas reproduzidas · erros de IA detectados · conjecturas refutadas · contraexemplos encontrados · algoritmos testados · lemas formalizados · resultados intermediários revisados · mapas de barreiras úteis · experimentos reproduzíveis · manuscritos sólidos · revisão positiva de especialistas · melhoria documentada da metodologia.

## Idiomas

Operacional: português do Brasil. Científico: inglês para artigos, teoremas, código, bibliografia e formalização.

## Trilhas por projeto

- **Trilha pedagógica:** Luiz compreende origem, definições, estado da arte, barreiras e o significado de cada resultado. Linguagem clara, analogias identificadas, glossário progressivo.
- **Trilha técnica:** trabalho matemático auditável — definições formais, hipóteses explícitas, provas detalhadas, testes, formalização, revisão especializada.
- A trilha pedagógica **não** substitui nem flexibiliza a técnica.
