"""Renderiza telas animadas da marca Mentor em MP4 (H.264 + AAC, 30fps).

Cada tela é um HTML que usa marca/base.css e os atributos data-in/data-count
de ferramentas/anim.js (o script é injetado automaticamente).

Uso:
  # uma tela -> um MP4 (ex.: item de carrossel do Instagram)
  python3 ferramentas/video.py tela tela.html saida.mp4 --w 1080 --h 1350 --seg 6 --semente 7

  # várias telas em sequência -> um MP4 (Facebook/LinkedIn/Reels)
  python3 ferramentas/video.py sequencia saida.mp4 tela1.html tela2.html ... --w 1080 --h 1920 --seg 5 --semente 7

Sempre inclui trilha (ferramentas/trilha.py). Confere a resolução no final.
Antes de gravar, confere a área segura de cada tela (ferramentas/moldura.py):
no 1080x1920 nada de logo/texto/número nas faixas cobertas pela interface do Reels.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
import trilha  # noqa: E402
import moldura  # noqa: E402
from scipy.io import wavfile  # noqa: E402
import numpy as np  # noqa: E402

FPS = 30
ANIM = (RAIZ / "ferramentas" / "anim.js").read_text(encoding="utf-8")


def _preparar(html_path: Path, destino: Path) -> Path:
    html = html_path.read_text(encoding="utf-8")
    if "<base" not in html:
        html = html.replace("<head>", f'<head><base href="file://{RAIZ}/">', 1)
    html = html.replace("</body>", f"<script>{ANIM}</script></body>", 1)
    destino.write_text(html, encoding="utf-8")
    return destino


def _quadros(html_path: Path, pasta: Path, w: int, h: int, seg: float, inicio: int) -> int:
    tmp = _preparar(html_path, pasta / f"_tela_{inicio}.html")
    total = int(round(seg * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(f"file://{tmp}", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        for i in range(total):
            pg.evaluate(f"window.frame({i / FPS})")
            pg.screenshot(path=str(pasta / f"f{inicio + i:06d}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        b.close()
    return total


def _codificar(pasta: Path, n: int, seg_total: float, saida: Path, semente: int) -> None:
    wav = pasta / "trilha.wav"
    s = trilha.gerar(seg_total, semente)
    wavfile.write(str(wav), trilha.SR, np.column_stack([s, s]))
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(pasta / "f%06d.png"),
        "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(saida),
    ]
    subprocess.run(cmd, check=True)


def conferir(arquivo: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,duration",
                        "-of", "json", str(arquivo)], capture_output=True, text=True, check=True)
    info = json.loads(r.stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    tem_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    return {"largura": v["width"], "altura": v["height"], "duracao": float(v.get("duration", 0)),
            "audio": tem_audio, "mb": round(arquivo.stat().st_size / 1e6, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["tela", "sequencia"])
    ap.add_argument("args", nargs="+")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1350)
    ap.add_argument("--seg", type=float, default=6.0)
    ap.add_argument("--semente", type=int, default=0)
    a = ap.parse_args()
    if a.modo == "tela":
        telas, saida = [Path(a.args[0])], Path(a.args[1])
    else:
        saida, telas = Path(a.args[0]), [Path(x) for x in a.args[1:]]
    probs = moldura.conferir(telas, a.w, a.h)
    if probs:
        sys.exit("ERRO: área segura violada (corrija o layout antes de gravar):\n- " + "\n- ".join(probs))
    with tempfile.TemporaryDirectory(dir=RAIZ) as d:
        pasta = Path(d)
        n = 0
        for tela in telas:
            n += _quadros(tela, pasta, a.w, a.h, a.seg, n)
        _codificar(pasta, n, n / FPS, saida, a.semente)
    info = conferir(saida)
    print(json.dumps(info, ensure_ascii=False))
    ok = info["largura"] == a.w and info["altura"] == a.h and info["audio"] and info["mb"] < 100
    if not ok:
        sys.exit("ERRO: vídeo fora do padrão (resolução, áudio ou tamanho).")


if __name__ == "__main__":
    main()
