# PNP-AI — 10 — CLAIM LEDGER

> IDs: `7P-PNP-CLM-NNNN`. Estados e campos obrigatórios definidos em `../05_GLOBAL_CLAIM_LEDGER.md`. Append-only: claims refutados permanecem registrados.
> Origem comum dos claims 0001–0007: SRC-0003 (Cook, "The P versus NP Problem", doc oficial Clay), trechos conferidos verbatim via parse local do PDF em 2026-07-10. Detalhes em `01_OFFICIAL_PROBLEM_SPEC.md`.

| Claim ID | Enunciado (resumo) | Estado | Origem | Última atualização |
|---|---|---|---|---|
| 7P-PNP-CLM-0001 | Formulação oficial do problema: "Does P = NP?"; resposta independe de \|Σ\|≥2; caso unário aberto; P ⊆ NP trivial | SOURCE_VERIFIED | SRC-0003 §1 | 2026-07-10 |
| 7P-PNP-CLM-0002 | Definição de P: linguagens decididas por TM em tempo polinomial de pior caso; classe robusta a modelos razoáveis | FORMULATION_VERIFIED | SRC-0003 §1 | 2026-07-10 |
| 7P-PNP-CLM-0003 | Definição de NP via checking relations: L ∈ NP ⟺ ∃k, R poly-time com w ∈ L ⟺ ∃y(\|y\| ≤ \|w\|^k ∧ R(w,y)); R poly-time ⟺ L_R ∈ P | FORMULATION_VERIFIED | SRC-0003 §1 (verbatim) | 2026-07-10 |
| 7P-PNP-CLM-0004 | ≤p exige f computável em tempo polinomial (Def. 3); NP-completude: L ∈ NP e L' ≤p L ∀L' ∈ NP (Def. 4) | FORMULATION_VERIFIED | SRC-0003 §2 (verbatim; qualificador poly-time conferido após falha de extração automática) | 2026-07-10 |
| 7P-PNP-CLM-0005 | Proposition 1: (a) ≤p preserva P para baixo; (b) método de propagação de NP-completude; (c) L NP-completo ∈ P ⟹ P = NP | SOURCE_VERIFIED | SRC-0003 §2 | 2026-07-10 |
| 7P-PNP-CLM-0006 | SAT é NP-completo (Cook 1971 [9]; Levin 1973 [23] indep.; Karp 1972 [21]: +20 problemas, notação padrão e ≤p); 3-SAT NP-completo | SOURCE_VERIFIED (fontes primárias OBTIDAS 2026-07-10: SRC-0005/0006/0007 no source ledger; enunciados conferidos; **reconstrução das provas pendente** — FASE 3) | SRC-0003 §2 + SRC-0005/6/7 | 2026-07-10 |
| 7P-PNP-CLM-0007 | Critérios de solução: P=NP ⟸ algoritmo polinomial uniforme correto p/ um NP-completo; P≠NP exige limitação universal enfrentando relativization (oráculo A com P^A=NP^A) e natural proofs (Razborov–Rudich); melhor circuit lower bound p/ NP registrado no doc: ~4n. Regras Clay: Qualifying Outlet + 2 anos + aceitação geral; sem submissão direta | SOURCE_VERIFIED | SRC-0003 §3 + SRC-0004 | 2026-07-10 |

## Observações

- Nenhum claim acima é derivação do projeto — são reconstruções da fonte oficial (fundação para as fases 2–4).
- A barreira de **algebrization** (Aaronson–Wigderson 2008) NÃO está no documento de Cook; será registrada com fonte própria na FASE 4.
