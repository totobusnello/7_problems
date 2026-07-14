# Alvo C — Auditoria da database AIG do Simplifier (findings)

> **Status:** entrega parcial fechada (2026-07-14). Alvo C do AUDIT SWEEP 001, aprovado por Luiz
> como quick-win paralelo. Auditoria construtiva (não-ataque): verificamos otimalidade das
> entradas da database pública de subcircuitos "ótimos" do Simplifier e emitimos circuitos
> menores certificados onde encontramos melhoria. **Nenhum contato com os autores** — divulgação
> depende de OK explícito de Luiz (10_PUBLICATION_RULES).

## O que é o alvo

`arXiv:2503.19103` — *Simplifier: A New Tool for Boolean Circuit Simplification* (grupo SPbSAT).
A ferramenta simplifica circuitos usando uma database pré-computada de subcircuitos de 3 entradas
supostamente **ótimos** (mínimo de portas AND). Repo: `github.com/SPbSAT/simplifier`,
`databases/database_aig.txt` (base AIG: AND-2 + NOT livre; custo = nº de ANDs). Nós temos o
ground-truth n=3 completo por exact synthesis via SAT (encoder single validado por gates G1-G3 +
222/222 no n=4; extensão multi-output validada por `gate_multi.py`: 256/256 + G-M2a/b/c).

## Método

Por entrada `(n=3, m saídas, circuito deles)`:
1. simulação valida que o circuito declarado computa os `tts` (convenção x0=MSB, refs forward);
2. `k_deles` = nº de ANDs no circuito deles;
3. exact synthesis SAT (encoder multi-output, ANDs compartilhados entre saídas):
   - UNSAT em `k_deles − 1` ⟹ **OPTIMAL** (o circuito deles é mínimo — certificado);
   - SAT ⟹ **SUBOPTIMAL**: desce até fechar o `k_opt` real e emite o circuito menor;
4. cap de 30 s por chamada SAT (`TIMEOUT_S`) contra a cauda k-alto (UNSAT-hard). Estouro no 1º
   teste ⟹ **INCONCLUSIVE** (não auditada); toda melhoria emitida segue **verificada por
   simulação** — o cap só enfraquece a certificação de otimalidade da cauda, nunca o rigor das
   melhorias.

Toda melhoria foi **re-verificada por simulação independente** (fora da VPS) antes desta nota:
3.370/3.370 (3-out) computam os `tts` e usam estritamente menos ANDs.

## Resultados

| Camada | Auditado | Ótimas (confirmadas) | Subótimas (melhoria certificada) | Não-decididas |
|---|---:|---:|---:|---:|
| single-output (m=1) | 77 | 77 | 0 | 0 |
| 2-output (m=2) | 7.177 | 7.127 | **50** | 0 |
| 3-output (m=3, parcial 16,9%) | 102.655 | 99.067 | **3.370** | 218 |
| **Total** | **109.909** | **106.271** | **3.420** | **218** |

**Distribuição de ganho (ANDs economizados):**
- 3-out: 3.183 × −1 AND, 115 × −2, 72 × −3.
- 2-out: 42 × (5→4), 7 × (6→5), 1 × (7→6).

## Leitura

- A database do Simplifier é **muito boa**: >99% das entradas auditadas são de fato ótimas
  (certificado por UNSAT). Isso é validação externa forte da ferramenta deles.
- As **3.420 melhorias** são um **presente construtivo**: circuitos estritamente menores, cada um
  com certificado de otimalidade (opt exato fechado) e verificado por simulação. Numa base AIG onde
  o custo é medido em ANDs, cada AND a menos é ganho real para quem consome a database.
- Cobertura 3-out parcial (16,9%): a cauda de circuitos com `k` alto é UNSAT-hard e tem retorno
  decrescente (as melhorias concentram-se em `k` baixo/médio). Parada de engenharia deliberada — a
  cauda k-alto fica como trabalho aberto, não como afirmação de exaustividade.

## Reprodutibilidade

- Database: `database_aig.txt`, sha256 `ac253e596bed0cdb05ee138cf6191e79b6e15ff0bf1d6d6708615f2249dca1aa`
  (fonte: `raw.githubusercontent.com/SPbSAT/simplifier/5b088f2f.../databases/database_aig.txt`).
- Encoder: `multi_aig_exact.py` (gate: `gate_multi.py`). Auditoria: `audit_multi.py` (`TIMEOUT_S=30`).
- Artefatos: `improved_{1,2,3}out_w*.jsonl` (circuitos melhorados, um por linha, com `certified_opt`).
- Solver: kissat 4.0.4. Bancada: VPS Hostinger 2 vCPU (always-on).

## Aberto / próximo

- Fechar o restante do lote 3-out (83%) exigiria mais cores + cap menor; ROI baixo — parqueado.
- **Divulgação aos autores do Simplifier = decisão de Luiz.** O material está pronto (circuitos +
  certificados), mas nenhum contato externo foi feito.
- Motor multi-output reutilizável para **Alvo A** (arXiv:2601.08368, implementações (AND,XOR) de
  funções quadráticas — mesma pergunta de minimalidade, base XAG).
