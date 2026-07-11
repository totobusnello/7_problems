"""
EXP-PILOT-N5 — Amostrador de classes NPN de n=5 (FASE 6, piloto de medição).

Desenho (emenda datada 2026-07-11 ao 13_FASE6_PLAN, ANTES de qualquer execução):
- Amostragem UNIFORME SOBRE FUNÇÕES (truth tables de 32 bits, seed registrada),
  canonicalizada para NPN. Classes ficam amostradas com probabilidade
  proporcional ao tamanho da órbita -> estimativas SOBRE CLASSES usam pesos
  de Horvitz-Thompson w = 1/orbit_size (registrado por classe).
  Racional: uniforme-sobre-classes exigiria enumerar as 616.126 classes.
- Estrato adicional: as 64 funções simétricas de n=5 (valor depende só do
  popcount, 2^6 mapas), canonicalizadas e deduplicadas.
- Canonical form: mínimo tt sobre a órbita (120 perms x 32 máscaras de
  negação de entrada x 2 negações de saída = 7680 transformações).
"""
import json
import random
from itertools import permutations

N = 5
ROWS = 1 << N          # 32
MASK = (1 << ROWS) - 1
SEED = 20260711
TARGET_RANDOM = 300

# pré-computa rowmaps: para cada (perm, negmask), rowmap[t] = linha fonte
ROWMAPS = []
for perm in permutations(range(N)):
    for neg in range(1 << N):
        rm = []
        for t in range(ROWS):
            u = 0
            for j in range(N):
                bit = (t >> j) & 1
                if (neg >> j) & 1:
                    bit ^= 1
                u |= bit << perm[j]
            rm.append(u)
        ROWMAPS.append(tuple(rm))
assert len(ROWMAPS) == 3840  # x2 de saída = 7680 transformações


def orbit(tt):
    """Conjunto de todas as tts NPN-equivalentes a tt."""
    out = set()
    for rm in ROWMAPS:
        g = 0
        for t in range(ROWS):
            if (tt >> rm[t]) & 1:
                g |= 1 << t
        out.add(g)
        out.add(g ^ MASK)
    return out


def canon(tt):
    orb = orbit(tt)
    return min(orb), len(orb)


def main():
    rng = random.Random(SEED)
    classes = {}  # canon_tt -> {orbit, stratum, draws}

    # estrato 1: aleatórias uniformes sobre funções
    draws = 0
    while len([c for c in classes.values() if c["stratum"] == "random"]) < TARGET_RANDOM:
        tt = rng.getrandbits(ROWS)
        draws += 1
        c, osize = canon(tt)
        if c in classes:
            classes[c]["draws"] += 1
        else:
            classes[c] = {"orbit": osize, "stratum": "random", "draws": 1}
    print(f"aleatórias: {draws} sorteios -> {TARGET_RANDOM} classes distintas")

    # estrato 2: simétricas (64 = 2^6 mapas de popcount)
    from math import comb
    sym_new, sym_dup = 0, 0
    for m in range(64):
        tt = 0
        for t in range(ROWS):
            if (m >> bin(t).count("1")) & 1:
                tt |= 1 << t
        c, osize = canon(tt)
        if c in classes:
            if classes[c]["stratum"] == "random":
                classes[c]["stratum"] = "random+symmetric"
            sym_dup += 1
        else:
            classes[c] = {"orbit": osize, "stratum": "symmetric", "draws": 0}
            sym_new += 1
    print(f"simétricas: 64 funções -> {sym_new} classes novas (+{sym_dup} já na amostra/duplicadas entre si)")

    with open("pilot_sample.jsonl", "w") as f:
        for c in sorted(classes):
            rec = {"canon_hex": f"0x{c:08x}", "canon_dec": c, **classes[c]}
            f.write(json.dumps(rec) + "\n")
    print(f"total: {len(classes)} classes em pilot_sample.jsonl (seed={SEED})")


if __name__ == "__main__":
    main()
