# Revisão adversarial da v0 (4 famílias) — consolidado + plano de correção

> **Data:** 2026-07-15/17. **Alvo:** `paper1_unitgap_basedep_v0.md`. **Revisores:** REV-0015 (Grok/xAI),
> REV-0016 (Kimi/Moonshot), REV-0017 (Codex/OpenAI `gpt-5.6-sol`), REV-0018 (GLM/Zhipu). Verbatims em
> `../experiments/exp_unitgap_check/rev001{5,6,7,8}_v0_verbatim.md`. Chamadas #18–21 no `07_MODEL_CALL_LOG`.
> Correções são **aditivas e datadas** (governança); nada reescreve registro histórico.

## Veredito

**4/4 famílias: a refutação do Teorema 2 (Unit Gap) SOBREVIVE.** Nenhuma achou erro matemático que
resgate o Thm 2 ou o Cor 6. Todos os ataques ao núcleo (opt=6, tree=9, type-confusion, Khrapchenko,
Thm 3, soundness do encoder) falharam. Os problemas são **higiene de certificação e precisão de
redação** — não um furo matemático. O núcleo está intacto e, após a leitura verbatim do paper do
Krinkin, **mais forte** (ver §Reforços).

## Resolvido contra a fonte (scrape de arXiv:2603.08033v2)

- **Definição de `s` (Cor 6), verbatim:** `s(a,b)=|D_a∩D_b|` ("counts the shared gates"). No ótimo de
  6 gates de ⊕₃, os dois filhos da saída compartilham o bloco XOR de 3 gates ⟹ `s=3=1+4+4−6`. **Cor 6
  refutado, confirmado.** A dúvida do GLM (s como "#gates com fan-out≥2" ⟹ s=1) foi um erro de leitura.

## Reforços do verbatim (a INCORPORAR — fortalecem a refutação)

- **D1. Inconsistência interna do paper.** §2 mostra `tree(f)=min(1+opt(a)+opt(b))` (opt nos filhos ⟹
  Thm 2 trivial), mas §3 define o Bellman `(Tv)(f)=min(1+v(a)+v(b))` (v **recursivo** ⟹ tree real) e
  afirma que ele "computes tree(f)" **e** "overshoots opt by gap∈{0,1}" — impossível ao mesmo tempo
  (para ⊕₃ o T recursivo dá 9, overshoot 3). As duas definições do próprio paper se contradizem.
- **D2. Table 3 do Krinkin** reporta `s=1` (100%) para as decomposições opt=6 (parity) — conflito
  direto com `s=3`. Segundo diagnostic signature (a tabela reflete o bound circular `s≤tree−opt≤1`).
- **D3. Table 1 do Krinkin** lista opt=6/gap=1 nas 2 paridades (tree real=9, gap=3) — diagnostic
  signature já citado, agora confirmado verbatim.

## Erros materiais (dados) — VERIFICADOS com scripts próprios (não os dos LLMs)

| # | Erro | Verificação | Correção |
|---|---|---|---|
| **A1** | n=5 = **row-count**, não funções distintas | 29.643 linhas → **25.373 tt distintas** (4.270 dups cross-worker, 0 conflitos de veredito); pós-dedup **gap0 24.875 / gap1 294 / inconclusive 204 / sep 0** | trocar 29.643→25.373 em v0(§5+abstract), technote, `xag_n5_search_findings`, claim 0030, RESEARCH_LOG C34, ledger, PR #9; regenerar CSV dedup OU declarar "worker-results com 4.270 dups" |
| **A2** | 3 classes gap-6 ≠ "parity-4 e relativas NPN" | 0x1668 peso 6, 0x16e9 peso 8, 0x6996 peso 8; **opt_XAG = 6/5/3** (distintos ⟹ 3 classes NPN distintas) | "três classes NPN distintas atingem gap 6, incl. parity-4 (0x6996)"; parity é *um* extremo, não a fonte única — v0 abstract+§4, technote §3, claim 0026 |
| **A3** | opt(⊕₃)=6: só k=5 tem DRAT | `certs/` tem só `par3_k5.drat` + `h_child_k3.drat`; **nenhum DRAT p/ k=1..4** | **gerar DRAT k=1..4** (barato, fecha de vez) OU reformular p/ "UNSAT@5 certifica opt≠5; opt≥6 via minimalidade + restrição do filho". Decisão do Luiz. NÃO derruba a refutação (Khrapchenko blinda) |

## Overclaims de certificação/verificação (múltiplas famílias)

- **B1** [3/4] n=5 "each result simulation-verified" é **falso** (`verify=False`). → tabela §6:
  "encoder validado por gate em n≤4; instâncias n=5 não decodificadas/simuladas". Opção forte:
  re-rodar `verify=True` nas 294 gap1 + amostra das gap0.
- **B2** [3/4] Lean `tree(⊕₃)≥9` é `native_decide` (compiler-trusted), **não** kernel `decide`. →
  tabela §6 + §3; re-rodar `#print axioms tree_lower` e colar (inclui `Lean.ofReduceBool`).
- **B3** [3/4] XAG UNSAT sem DRAT é load-bearing p/ o slogan "holds in XAG". → hedge no **abstract**:
  "holds under our gated exact-synthesis pipeline (UNSAT uncertified)".
- **B4** [2/4 + verbatim] MIG "class by class" → **"bucket by bucket"** (Krinkin publica só a
  distribuição, não mapping por-classe). → abstract.
- **B5** as "two independent tree implementations" são a **mesma recorrência** (layered vs fixed-point).
  → "independent implementations of the same recurrence".

## Redação / hedge / precisão

- **C1** [GLM/Kimi] **citar Krinkin verbatim** (definição de formula §2 + recursão §2 + Bellman §3 +
  Cor 6/`s`). Verbatim já em mãos (scrape). → block-quotes.
- **C2** [3/4] novidade (ii): hedge no **abstract** (não só §7); trocar "we have not found stated
  anywhere" por "first *explicitly tabulated* gap-by-basis comparison; likely implicit in classical
  catalogs (Knuth B₂, Soeken MIG, Krinkin AIG)".
- **C3** [2/4] n=5 wording: remover "biased toward likely separators", "drives probability near zero",
  "pro-separator". → "among 25.373 distinct, generator-reachable, solver-decidable essential
  functions, no separator was found".
- **C4** [Codex] "nearly a third of all functions" → **"32.4% das 222 classes NPN"** (órbitas diferem).
- **C5** [Codex] "large AIG gaps are *precisely* the cost of linear structure" → "parity demonstrates
  that the absence of native XOR can produce large AIG gaps; the census is consistent with, but does
  not isolate, this mechanism".
- **C6** [4/4] **Thm 3 corrected proof**: escrever por extenso em apêndice (o GLM tropeçou na versão de
  1 linha — sinal de que é insuficiente). Prova correta: `2m = I_in + I_g`, `I_in≥n` (essential),
  `I_g≥m` (non-tree: m−1 baseline + 1 do sharing) ⟹ `2m≥n+m` ⟹ `m≥n`, com hipóteses "single-output,
  todas as portas usadas, n inputs essenciais".
- **C7** [Codex] "fan-out one at every gate" (a saída tem fan-out 0) → "every non-output gate fan-out
  ≤ 1". (Nota: o Krinkin escreve "fan-out exactly one at every gate" — espelhar com precisão.)
- **C8** [Codex] spec do §2: "SAT@k yields a valid k-gate circuit; ascending search is exact only after
  every smaller k is excluded" (o encoder é normalizado, não "at most k" ingênuo).
- **C9** [Codex] n=5 flow table: logar candidatos gerados → veredito (incl. timeouts de opt e
  opt>kmax, hoje `continue`ados sem contar). Requer re-instrumentar `search_n5.py` OU declarar a
  população condicional.

## Prioridade sugerida

1. **A1 + A2** (erros de dado que aparecem em vários docs + no ledger) — mais urgentes.
2. **A3** (decisão: gerar DRAT k=1..4 vs reformular) — precisa do Luiz.
3. **B1–B4** (certificação honesta) — obrigatório antes de submeter.
4. **D1–D3** (reforços do verbatim) — fortalecem, baixo custo.
5. **C1–C9** (redação) — na passada de v1.
6. Depois de v1: **2ª rodada adversarial** só das correções + conversão LaTeX.
