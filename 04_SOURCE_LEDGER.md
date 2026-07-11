# 04 — SOURCE LEDGER — Bibliografia verificada

> Prioridade de fontes: Clay (formulação oficial) → artigo original → peer-reviewed → versão do autor → arXiv → livro/survey reconhecido → docs de software → secundária identificada.
> Cada entrada registra: autores, título, ano, publicação, DOI/ID, teorema/seção/página usada, hipóteses, conclusão, data de consulta.
> **Proibido inventar:** artigos, autores, links, citações, números de teorema, páginas, resultados, consenso.

## Entradas

### SRC-0001 — Clay Mathematics Institute: Millennium Problems (página oficial)
- **URL:** https://www.claymath.org/millennium-problems/
- **Uso:** estado oficial dos sete problemas.
- **Conteúdo verificado:** 6 problemas unsolved; Poincaré solved (Perelman).
- **Data de consulta:** 2026-07-10 (HTTP 200, scrape direto).
- **Estado:** SOURCE_VERIFIED.

### SRC-0002 — Busnello, Flandoli, Romito (2003/2005)
- **Título:** "A probabilistic representation for the vorticity of a three-dimensional viscous fluid and for general systems of parabolic equations"
- **Autores:** Barbara Busnello; Franco Flandoli; Marco Romito.
- **arXiv:** math/0306075 — https://arxiv.org/abs/math/0306075
- **Publicação peer-reviewed:** Proceedings of the Edinburgh Mathematical Society, 48 (2005) 295–336 — **PENDENTE DE VERIFICAÇÃO DIRETA** (metadado a confirmar quando o PDF for processado).
- **Uso:** artigo-base da frente NS-PROB; representação probabilística da vorticidade 3D.
- **Data de consulta:** referenciado no briefing 2026-07-10; **PDF ainda não baixado/parseado nesta sessão**.
- **Estado:** SOURCE_VERIFIED (existência no arXiv) / conteúdo AGUARDANDO PROCESSAMENTO.

### SRC-0003 — Cook, "The P versus NP Problem" (descrição oficial do Clay)
- **Autor:** Stephen Cook. **Título:** The P versus NP Problem. **Publicação:** Clay Mathematics Institute, official problem description (12 pp.).
- **URL:** https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf (página do problema: https://www.claymath.org/millennium/p-vs-np/)
- **Uso:** formulação oficial, definições de P/NP/≤p/NP-completude (Defs. 1–4, Prop. 1), barreiras (relativization, natural proofs). Base de `PNP_AI/01_OFFICIAL_PROBLEM_SPEC.md` e claims 7P-PNP-CLM-0001..0007.
- **Método de verificação:** PDF baixado (176 KB, HTTP 200) e parseado localmente com pypdf; trechos-chave conferidos verbatim (não confiado a extração por LLM — uma extração automática errou um heading e omitiu o qualificador poly-time da Def. 3; corrigido contra o texto).
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED.

### SRC-0004 — Clay: Rules for the Millennium Prize Problems
- **URL:** https://www.claymath.org/millennium-problems/rules/ (regras adotadas pelo Board do CMI em 2018-09-26).
- **Uso:** critérios institucionais de solução: publicação em Qualifying Outlet + ≥2 anos + aceitação geral da comunidade; CMI não aceita submissões diretas.
- **Data de consulta:** 2026-07-10. **Estado:** SOURCE_VERIFIED.

### SRC-0005 — Cook (1971), "The complexity of theorem-proving procedures" (ref. [9] de SRC-0003)
- **Uso futuro:** prova original da NP-completude de SAT/3-SAT (via análogo polinomial de Turing reducibility).
- **Estado:** A OBTER (FASE 3) — por ora referenciado apenas via SRC-0003.

### SRC-0006 — Karp (1972), "Reducibility among combinatorial problems" (ref. [21] de SRC-0003)
- **Uso futuro:** 20+ problemas NP-completos; notação P/NP; NP-completude via ≤p.
- **Estado:** A OBTER (FASE 3) — por ora referenciado apenas via SRC-0003.

### SRC-0007 — Levin (1973), universal search problems (ref. [23] de SRC-0003)
- **Uso futuro:** definição independente de universal search problems, 6 exemplos incl. Satisfiability.
- **Estado:** A OBTER (FASE 3) — por ora referenciado apenas via SRC-0003.

## Template de entrada

```
### SRC-NNNN — [autores curtos, ano]
- Título / Autores / Ano / Publicação / DOI ou ID
- Teorema, seção ou página usada
- Hipóteses / Conclusão
- Data de consulta / Estado
```
