# Paper 1 (Cume 1 / P vs NP) — ESQUELETO

> **Status:** esqueleto interno (2026-07-15). NÃO é submissão. Redação e submissão exigem OK
> explícito de Luiz + `10_PUBLICATION_RULES`. Base: `notes/technote_unitgap_basedep.md` (já ~90% do
> conteúdo) + `notes/xag_n5_search_findings.md` (n=5). Este esqueleto define **forma e escopo** antes
> da redação.

---

## Decisão de framing (fixada com Luiz)

- **Paper técnico, result-anchored.** O resultado (refutação + base-dependência) ancora; o método
  (exact synthesis via SAT + certificação + revisão multi-família) entra como **metodologia sóbria**,
  não como narrativa de expedição. A narrativa lúdica "Seven Summits" fica para depois, com mais cumes.
- **Sem claim grandioso de pioneirismo** no corpo. A contribuição fala por si (certificados + Lean).
- **Meta:** preprint arXiv (cs.CC). Venue e timing = decisão de Luiz (ver "Decisões abertas").

## Título (candidatos — escolher 1)

1. *The Unit Gap Is Base-Dependent: A Mechanically Verified Refutation and a Three-Base Census*
   (= título atual da technote; direto, result-first)
2. *Formula-vs-Circuit Gaps Depend on the Basis: Refuting the Unit Gap and a Certified Census at n ≤ 4*
3. *A Type Confusion in "The Unit Gap": Certified Counterexamples and a Cross-Base Census*

## Abstract (stub — condensar o da technote, +1 frase de n=5)

- Krinkin (arXiv:2603.08033) afirma gap ∈ {0,1} (Thm 2) + s ∈ {0,1} (Cor 6). Refutamos ambos.
- ⊕₃: opt=6 (DRAT) vs tree=9 (Lean) ⟹ gap 3; Khrapchenko força gap ≥ 2 independente de código.
- Erro = confusão de tipo na recursão de tree(f) (usa opt nos filhos).
- Censo n=4: 72/222 classes (32,4%) têm gap ≥ 2; max 6 = parity-4 (bate Khrapchenko).
- **Base-dependência:** em XAG a propriedade unit-gap *vale* (gap_XAG ∈ {0,1}) para n ≤ 4 exaustivo
  **e para ~29,6k funções amostradas em n=5, zero separadores** ← integra o n=5.
- MIG replica tabela publicada (Soeken et al. 2016) exatamente → validação recíproca do pipeline.

## Estrutura de seções

**1. Introduction**
- O claim do unit-gap e por que importa (formula-size vs circuit-size é questão central em complexidade).
- O que fazemos: refutar (certificado), mapear (censo n≤4), mostrar base-dependência (n≤4 + n=5 amostral).
- Uma frase de método (exact synthesis + certificação + 4 famílias de modelo adversariais) — sóbria.

**2. Definitions and scope** — reusa technote §1 (AIG/XAG/MIG, opt/tree/gap, NPN, n≤4 exaustivo).

**3. The refutation (n=3)** — reusa technote §2 integralmente.
- Erro de tipo na recursão displayed (opt nos filhos).
- ⊕₃: opt=6 (UNSAT k=5, DRAT drat-trim `s VERIFIED`); tree=9 (DP + Lean); enumeração por camadas.
- Khrapchenko fail-safe (gap ≥ 2 analítico).
- Cor 6 refutada (s=3 no ótimo de 6 gates); Thm 7 perde prova; **Thm 3/4 sobrevivem** (Thm 3 com
  prova corrigida — contagem de incidências de input).

**4. Structural failure: AIG gap census n=4** — reusa technote §3 (tabela gap 0..6; 72/222 ≥ 2).

**5. Base dependence: XAG, MIG, and n=5** — technote §4 **+ n=5 novo**.
- XAG n≤4 exaustivo: gap_XAG ∈ {0,1}.
- **XAG n=5 (novo, `xag_n5_search_findings`):** 29.643 funções amostradas (viés pró-separador),
  0 separadores; gap0 29.143 / gap1 296 / inconclusive 204. **Amostral, não exaustivo** — hedge explícito.
- MIG: replicação exata de Soeken et al. (validação de pipeline).
- Cross-base table.

**6. Verification levels** — reusa technote §5 (tabela por-claim: DRAT / Lean / analítico / gates).

**7. Related work and novelty (hedged)** — reusa technote §6.
- Krinkin (2603.08033 refutado; 2603.09379 catálogo, 2 entradas fechadas — nota separada).
- MIG: Soeken et al. (replicação). XAG totals: Knuth TAOCP (sem novidade nos números XAG).
- Novo: (i) refutação certificada + Lean; (ii) censos gap-por-base n≤4 + n=5 amostral.

**8. Open questions** — reusa technote §7 (n=5 agora com evidência amostral; teorema por trás do
unit-gap XAG; tree_MIG; Thm 7 base-relativo corrigido).

**Appendices**
- A. Certificados: DRAT (opt ⊕₃ e filhos), Lean `UnitGap.lean` (axiom footprint auditado).
- B. Encoders e gates: AIG/XAG/multi-output; gates G1-G3, G-M, G-T; parity-5 false-positive & fix.
- C. Reprodutibilidade: solver/seeds/bancada; artefatos (CNFs, CSVs, npy).
- D. *(interno, NÃO público)* call log + verbatim das revisões adversariais (REV-0009..0014) + ledger de claims.

## O que sai da versão pública (governança)

- Blocos de status interno, IDs de claim (7P-PNP-CLM-*), REV-* ids, referências a `10_PUBLICATION_RULES`.
- Menções a "AI system under direction of L.A. Busnello" ficam na nota de provenance (decidir tom — ver abaixo).

## Decisões abertas (para Luiz)

1. **Timing vs Krinkin.** A issue krinkin/unit-gap#1 foi enviada 2026-07-11, sem resposta (~4 dias).
   Norma acadêmica: dar ao autor uma janela para responder antes de um preprint de refutação. Um paper
   público que refuta é escalada além da issue → **exige novo OK seu** (regra "réplicas ao Krinkin").
   Opções: (a) esperar N dias/semanas a issue; (b) preprint já, citando a issue aberta; (c) contatar
   o autor antes (você decide — nenhum contato sem seu OK).
2. **Venue/formato.** arXiv cs.CC (provável) vs math.CO. Markdown→LaTeX quando redigir.
3. **Autoria/atribuição.** Como creditar o método (AI sob sua direção) sem virar claim de pioneirismo.
   Decidido: fora do corpo; fica na nota de provenance — mas o *tom* é seu.
4. **Escopo:** paper único (refutação + base-dependência, este esqueleto) vs dividir (refutação
   curta + census separado). Recomendação: **único** — a base-dependência é o que dá densidade e
   novidade ao resultado; a refutação sozinha é um erratum.

## Próximo passo

Aprovado o esqueleto → redijo a v0 completa em `drafts/` (markdown, ainda interno), com os apêndices
apontando para os artefatos versionados. Submissão só depois, com seu OK e a decisão de timing.
