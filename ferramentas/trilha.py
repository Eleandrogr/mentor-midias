"""Gera trilha instrumental original (livre de direitos) para os vídeos Mentor.

Pad ambiente suave + pulso leve, em tom sóbrio. A semente muda a progressão,
então cada dia pode ter uma trilha diferente.

Uso: python3 ferramentas/trilha.py saida.wav segundos [semente]
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
PROGRESSOES = [
    [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)],   # Am F C G
    [(50, 53, 57), (55, 58, 62), (48, 52, 55), (53, 57, 60)],   # Dm Gm C F
    [(52, 55, 59), (48, 52, 55), (55, 59, 62), (50, 54, 57)],   # Em C G D
    [(48, 52, 55), (57, 60, 64), (53, 57, 60), (55, 59, 62)],   # C Am F G
]


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lowpass(x, cut):
    b, a = butter(2, cut / (SR / 2))
    return lfilter(b, a, x)


def gerar(seg: float, semente: int = 0) -> np.ndarray:
    rng = np.random.default_rng(semente)
    prog = PROGRESSOES[semente % len(PROGRESSOES)]
    n = int(SR * seg)
    t = np.arange(n) / SR
    out = np.zeros(n)
    acorde_dur = 2.4
    for i in range(int(np.ceil(seg / acorde_dur)) + 1):
        notas = prog[i % len(prog)]
        ini = int(i * acorde_dur * SR)
        fim = min(n, int((i + 1) * acorde_dur * SR) + int(0.8 * SR))
        if ini >= n:
            break
        tt = t[ini:fim] - t[ini]
        env = np.minimum(tt / 0.6, 1) * np.exp(-np.maximum(tt - acorde_dur, 0) / 0.4)
        for nota in notas:
            f = hz(nota)
            det = 1 + rng.uniform(-0.002, 0.002)
            voz = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2 * det * tt) + 0.15 * np.sin(2 * np.pi * f * 0.5 * tt)
            out[ini:fim] += voz * env * 0.12
        # baixo suave
        fb = hz(notas[0] - 12)
        out[ini:fim] += np.sin(2 * np.pi * fb * tt) * env * 0.10
    # pulso leve (batida macia a 96 bpm)
    bpm = 96
    passo = 60 / bpm
    k = 0
    while k * passo < seg:
        ini = int(k * passo * SR)
        dur = int(0.12 * SR)
        tt = np.arange(min(dur, n - ini)) / SR
        out[ini:ini + len(tt)] += np.sin(2 * np.pi * 60 * tt) * np.exp(-tt / 0.05) * (0.18 if k % 2 == 0 else 0.10)
        k += 1
    out = lowpass(out, 3500)
    # fade in/out
    fade = int(0.6 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    out /= max(1e-9, np.max(np.abs(out)))
    return (out * 0.5 * 32767).astype(np.int16)


if __name__ == "__main__":
    a = sys.argv
    sinal = gerar(float(a[2]), int(a[3]) if len(a) > 3 else 0)
    wavfile.write(a[1], SR, np.column_stack([sinal, sinal]))
