"""Corta o começo "vazio" de um vídeo (fade/entrada a partir do fundo liso) para que o
primeiro quadro já mostre o conteúdo. Use quando o vídeo PRECISA ser o primeiro item
(reel, vídeo único no Facebook/LinkedIn ou carrossel sem capa).

Uso:
  python3 ferramentas/cortar_inicio.py entrada.mp4 saida.mp4 [--max 4]

Procura, nos primeiros --max segundos, o primeiro quadro em que o conteúdo da tela
chegou a 90% do que ela mostra quando está completa, corta ali (vídeo e áudio) e confere
o resultado com conferir_capa.py. Se nada passar, sai com erro.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import conferir_capa as cc  # noqa: E402


def quadro(video: Path, t: float, png: Path) -> dict:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video),
                    "-frames:v", "1", str(png)], check=True)
    return cc.medir(png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--max", type=float, default=4.0)
    a = ap.parse_args()
    v = Path(a.entrada)
    with tempfile.TemporaryDirectory() as d:
        png = Path(d) / "q.png"
        alvo = quadro(v, a.max, png)["conteudo"]
        corte = None
        t = 0.0
        while t <= a.max:
            m = quadro(v, t, png)
            if m["ok"] and m["conteudo"] >= 0.9 * alvo:
                corte = round(t, 2)
                break
            t += 0.1
    if corte is None:
        sys.exit("ERRO: não achei quadro com conteúdo nos primeiros segundos.")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(corte), "-i", str(v),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", a.saida], check=True)
    r = cc.conferir(a.saida)
    print(json.dumps({"corte_s": corte, **r}, ensure_ascii=False))
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
