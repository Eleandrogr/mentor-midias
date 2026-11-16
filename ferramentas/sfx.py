"""Efeitos sonoros e trilha com ritmo para os reels Mentor (tudo sintetizado, livre de direitos).

Efeitos: whoosh (transição), pop (palavra/título entrando), tick (contador), sobe (barra crescendo),
impacto (destaque/máscara), cai (valor despencando).

Uso como módulo: mixar(segundos, eventos, semente) -> np.int16 estéreo (n, 2)
"""
import numpy as np
from scipy.signal import butter, lfilter

import trilha

SR = trilha.SR


def _bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], btype="band")
    return lfilter(b, a, x)


def _env(n, ataque, queda):
    t = np.arange(n) / SR
    return np.minimum(t / max(ataque, 1e-4), 1) * np.exp(-np.maximum(t - ataque, 0) / queda)


def whoosh(rng):
    n = int(0.42 * SR)
    ruido = rng.standard_normal(n)
    t = np.arange(n) / SR
    # varredura do filtro: grave -> agudo -> grave
    out = np.zeros(n)
    blocos = 12
    for k in range(blocos):
        a, b = k * n // blocos, (k + 1) * n // blocos
        f = 400 + 3200 * np.sin(np.pi * (k + 0.5) / blocos)
        out[a:b] = _bp(ruido[max(0, a - 400):b], f * 0.6, min(f * 1.6, SR / 2 - 100))[-(b - a):]
    env = np.sin(np.pi * np.clip(t / 0.42, 0, 1)) ** 2
    return out * env * 0.55


def pop(rng):
    n = int(0.07 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 380
    fase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(fase) * _env(n, 0.002, 0.025) * 0.28


def tick(rng):
    n = int(0.02 * SR)
    return _bp(rng.standard_normal(n), 2500, 6000) * _env(n, 0.001, 0.005) * 0.35


def sobe(rng):
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    f = 220 + 440 * (t / 0.5) ** 1.5
    fase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(fase) * np.sin(np.pi * t / 0.5) * 0.10


def impacto(rng):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    corpo = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 25)) * t) * _env(n, 0.003, 0.12)
    estalo = _bp(rng.standard_normal(n), 800, 5000) * _env(n, 0.001, 0.02)
    return (corpo * 0.6 + estalo * 0.25)


def cai(rng):
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    f = 700 * np.exp(-t * 3.2) + 90
    fase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(fase) * _env(n, 0.01, 0.35) * 0.16


EFEITOS = {"whoosh": whoosh, "pop": pop, "tick": tick, "sobe": sobe, "impacto": impacto, "cai": cai}


def ritmo(seg: float, semente: int, bpm: int = 108) -> np.ndarray:
    """Trilha base (pad do trilha.py) + bumbo e chimbal em colcheias, para dar pulso ao reel."""
    base = trilha.gerar(seg, semente).astype(np.float64) / 32767
    n = len(base)
    rng = np.random.default_rng(semente + 99)
    passo = 60 / bpm / 2
    k = 0
    while k * passo < seg:
        ini = int(k * passo * SR)
        if k % 4 == 0:  # bumbo nos tempos 1 e 3
            m = min(int(0.18 * SR), n - ini)
            t = np.arange(m) / SR
            base[ini:ini + m] += np.sin(2 * np.pi * (50 + 80 * np.exp(-t * 35)) * t) * np.exp(-t / 0.09) * 0.35
        m = min(int(0.04 * SR), n - ini)
        hat = _bp(rng.standard_normal(m + 10), 6000, 12000)[:m] * np.exp(-np.arange(m) / SR / 0.012)
        base[ini:ini + m] += hat * (0.10 if k % 2 else 0.06)
        k += 1
    return base


def mixar(seg: float, eventos: list, semente: int = 0) -> np.ndarray:
    n = int(SR * seg)
    mus = ritmo(seg, semente)[:n] * 0.6
    fx = np.zeros(n)
    rng = np.random.default_rng(semente)
    ultimo = {}
    for e in eventos:
        tipo = e["tipo"]
        if tipo not in EFEITOS:
            continue
        # evita metralhadora: no máximo um pop/tick a cada 0,09 s
        if tipo in ("pop", "tick") and e["t"] - ultimo.get(tipo, -9) < 0.09:
            continue
        ultimo[tipo] = e["t"]
        s = EFEITOS[tipo](rng)
        ini = int(e["t"] * SR)
        if ini >= n:
            continue
        m = min(len(s), n - ini)
        fx[ini:ini + m] += s[:m]
    out = mus + fx
    fade = int(0.4 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))  # som desde 0,0 s sem estalo
    out /= max(1e-9, np.max(np.abs(out)) / 0.89)
    s16 = (out * 32767).astype(np.int16)
    return np.column_stack([s16, s16])
