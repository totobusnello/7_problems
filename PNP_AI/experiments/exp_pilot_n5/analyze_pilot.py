"""
EXP-PILOT-N5 — análise dos resultados (roda a qualquer momento; usa o que houver).

Uso: python3 analyze_pilot.py <dir_out_pod> [<dir_out_mac>]
Saída: resumo em stdout (markdown-friendly).

Estatística (Emenda 1 + REV-0008/F5): amostra uniforme sobre FUNÇÕES; estimativas
sobre CLASSES usam pesos Horvitz-Thompson w=1/orbit (aproximação sob o desenho
"sorteia até N distintas" — ok para distribuições/proporções, que é o que usamos;
totais absolutos exigiriam normalização pela probabilidade de inclusão realizada).
"""
import json
import glob
import sys
from collections import Counter, defaultdict


def load(dirs):
    recs = []
    for d in dirs:
        for f in glob.glob(f"{d}/out_*.jsonl"):
            for line in open(f):
                try:
                    recs.append(json.loads(line))
                except Exception:
                    pass
    return recs


def main():
    dirs = sys.argv[1:] or ["out"]
    recs = load(dirs)
    rand = [r for r in recs if r["stratum"].startswith("random")]
    sym = [r for r in recs if r["stratum"] == "symmetric"]
    print(f"# Piloto n=5 — análise parcial ({len(recs)} classes: {len(rand)} random, {len(sym)} symmetric)\n")

    for name, grp in (("RANDOM (uniforme sobre funções)", rand), ("SYMMETRIC", sym)):
        if not grp:
            continue
        done = [r for r in grp if r.get("opt") is not None]
        cens = [r for r in grp if r.get("censored_k")]
        errs = [r for r in grp if r.get("error")]
        print(f"## {name}: {len(done)} decididas · {len(cens)} censuradas (2h) · {len(errs)} erros")
        if errs:
            for r in errs[:5]:
                print(f"  ERRO: {r['canon_hex']}: {r['error']}")
        if done:
            c = Counter(r["opt"] for r in done)
            wsum = defaultdict(float)
            for r in done:
                wsum[r["opt"]] += 1.0 / r["orbit"]
            tot_w = sum(wsum.values())
            print("| opt | n cru | % cru | % HT (classes) |")
            print("|---|---|---|---|")
            for k in sorted(c):
                print(f"| {k} | {c[k]} | {100*c[k]/len(done):.1f}% | {100*wsum[k]/tot_w:.1f}% |")
        if cens:
            cc = Counter(r["censored_k"] for r in cens)
            print(f"censuras por k: {dict(sorted(cc.items()))}")
        # custo
        if done:
            tot_solve = sum(sum(r["times"].values()) for r in done)
            tot_enc = sum(sum(r.get("enc_times", {}).values()) for r in done)
            times_sorted = sorted(sum(r["times"].values()) + sum(r.get("enc_times", {}).values()) for r in done)
            med = times_sorted[len(times_sorted) // 2]
            p90 = times_sorted[int(len(times_sorted) * 0.9)]
            print(f"custo/classe decidida: mediana {med:.0f}s · p90 {p90:.0f}s · máx {times_sorted[-1]:.0f}s "
                  f"(solve total {tot_solve:.0f}s + encode {tot_enc:.0f}s)")
        print()

    # extrapolação (só com dados suficientes; censuras tratadas como piso)
    done_r = [r for r in rand if r.get("opt") is not None]
    cens_r = [r for r in rand if r.get("censored_k")]
    if len(done_r) + len(cens_r) >= 30:
        n_r = len(done_r) + len(cens_r)
        mean_decided = sum(sum(r["times"].values()) + sum(r.get("enc_times", {}).values()) for r in done_r) / max(1, len(done_r))
        frac_cens = len(cens_r) / n_r
        # custo esperado POR FUNÇÃO amostrada (função-uniforme ≈ custo esperado por classe
        # ponderado pelo tamanho da órbita; para campanha POR CLASSE, reponderar por HT)
        wc = sum(1.0 / r["orbit"] for r in done_r + cens_r)
        mean_ht = sum((sum(r["times"].values()) + sum(r.get("enc_times", {}).values()) if r.get("opt") is not None else 7200.0) * (1.0 / r["orbit"]) for r in done_r + cens_r) / wc
        print("## Extrapolação preliminar (campanha por classe, 616.126 classes)")
        print(f"- fração censurada (cru): {100*frac_cens:.1f}% (cada censura = ≥2h; custo real da cauda DESCONHECIDO)")
        print(f"- custo médio/classe decidida (cru): {mean_decided:.0f}s · custo médio HT/classe (censura=piso 7200s): {mean_ht:.0f}s")
        total_core_h = 616126 * mean_ht / 3600
        print(f"- **recorte A (tudo): ≥ {total_core_h:,.0f} h-core** (piso; censuras subestimadas) "
              f"= {total_core_h/16/24:.0f} dias no pod 16c = {total_core_h/64/24:.0f} dias em 64c")
        print("- recortes B/C: aplicar a mesma média ao subconjunto alvo.")


if __name__ == "__main__":
    main()
