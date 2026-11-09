"""Confere o PRIMEIRO item de um post antes de agendar: não pode estar escuro nem vazio.

Uso:
  python3 ferramentas/conferir_capa.py <arquivo ou URL .png/.jpg/.mp4>
Para vídeo, analisa o primeiro quadro (é o que o Instagram usa como capa do carrossel).
Saída: JSON com as medidas e "ok". Código de saída 1 se reprovar.

Reprova quando:
  - brilho médio < 30 (quase preto), ou
  - desvio-padrão < 18 (tela lisa, sem texto), ou
  - menos de 4% dos pixels diferem da cor de fundo (só fundo, ou só o logo).
"""
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image, ImageStat
import numpy as np

LIM_BRILHO, LIM_DESVIO, LIM_CONTEUDO = 30, 18, 0.04


def _local(src: str, pasta: Path) -> Path:
    if src.startswith("http"):
        destino = pasta / ("item" + Path(src.split("?")[0]).suffix)
        urllib.request.urlretrieve(src, destino)
        return destino
    return Path(src)


def primeiro_quadro(arq: Path, pasta: Path) -> Path:
    if arq.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        return arq
    png = pasta / "q0.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(arq), "-frames:v", "1", str(png)], check=True)
    return png


def medir(png: Path) -> dict:
    im = Image.open(png).convert("RGB")
    cinza = im.convert("L")
    st = ImageStat.Stat(cinza)
    a = np.asarray(im).astype(int)
    fundo = np.median(a.reshape(-1, 3), axis=0)
    diff = np.abs(a - fundo).sum(axis=2) > 60
    m = {"brilho": round(st.mean[0], 1), "desvio": round(st.stddev[0], 1), "conteudo": round(float(diff.mean()), 3)}
    motivos = []
    if m["brilho"] < LIM_BRILHO:
        motivos.append("primeiro quadro escuro")
    if m["desvio"] < LIM_DESVIO or m["conteudo"] < LIM_CONTEUDO:
        motivos.append("primeiro quadro vazio (sem título/conteúdo visível)")
    m["ok"] = not motivos
    m["motivos"] = motivos
    return m


def conferir(src: str) -> dict:
    with tempfile.TemporaryDirectory() as d:
        pasta = Path(d)
        return medir(primeiro_quadro(_local(src, pasta), pasta))


if __name__ == "__main__":
    r = conferir(sys.argv[1])
    print(json.dumps(r, ensure_ascii=False))
    sys.exit(0 if r["ok"] else 1)
