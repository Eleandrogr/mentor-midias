"""Renderiza um reel FLUIDO da Mentor: um HTML com cenas (ferramentas/movimento.js) -> MP4.

- 60 quadros/s renderizados e fundidos 2 a 2 (desfoque de movimento) -> 30 fps.
- Trilha com ritmo + efeitos sonoros sincronizados (whoosh nas transições, pop nas palavras,
  tick nos contadores, impacto nos destaques) — ferramentas/sfx.py.
- Confere a área segura de cada cena (1080x1920: topo 250, rodapé 450, direita 150, esquerda 60;
  1080x1350: 88 em volta) e o "teste da pausa": a tela não pode ficar igual por mais de 1,5 s.
- O primeiro quadro já tem conteúdo (a 1ª cena começa visível); confira com conferir_capa.py.

Uso:
  python3 ferramentas/reel.py reel.html reel.mp4 --w 1080 --h 1920 --semente 7
  python3 ferramentas/reel.py reel.html linkedin.mp4 --w 1080 --h 1350 --semente 7
Elementos decorativos que podem sangrar para fora da área segura: classe "livre".
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from scipy.io import wavfile

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
import sfx  # noqa: E402

MOV = (RAIZ / "ferramentas" / "movimento.js").read_text(encoding="utf-8")
FPS_RENDER, FPS = 60, 30
MARGENS = {1920: (250, 150, 450, 60), 1350: (88, 88, 88, 88), 1080: (88, 88, 88, 88)}

JS_MEDIR = """
(t) => {
  window.frame(t);
  const cenas = Array.from(document.querySelectorAll('.cena'));
  const vis = cenas.filter(c => getComputedStyle(c).visibility === 'visible');
  const c = vis[vis.length - 1];
  c.querySelectorAll('.camera').forEach(k => k.style.transform = 'none');  // mede o layout sem o zoom da câmera
  const out = [];
  c.querySelectorAll('img, svg, .display, p, span, div, li').forEach(el => {
    if (el.closest('.livre') || el.classList.contains('camera') || el.classList.contains('fundo')) return;
    const kids = Array.from(el.children).filter(k => !['BR'].includes(k.tagName));
    const temTexto = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    if (!(el.tagName === 'IMG' || el.tagName === 'svg' || temTexto || (kids.length === 0 && getComputedStyle(el).backgroundColor !== 'rgba(0, 0, 0, 0)'))) return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const x1 = r.left + Math.max(r.width, el.scrollWidth || 0);  // texto que vaza da caixa também conta
    out.push({tag: el.tagName, txt: (el.textContent || '').trim().slice(0, 30), x0: r.left, y0: r.top, x1: x1, y1: r.bottom});
  });
  return out;
}
"""


def _preparar(html_path: Path, pasta: Path) -> Path:
    html = html_path.read_text(encoding="utf-8")
    if "<base" not in html:
        html = html.replace("<head>", f'<head><base href="file://{RAIZ}/">', 1)
    html = html.replace("</body>", f"<script>{MOV}</script></body>", 1)
    p = pasta / "_reel.html"
    p.write_text(html, encoding="utf-8")
    return p


def conferir_area(pg, w, h):
    topo, dir_, rod, esq = MARGENS[h]
    tempos = pg.evaluate("""() => { let a=0; return Array.from(document.querySelectorAll('.cena')).map(c => { const d=parseFloat(c.dataset.dur||'2.5'); const r=[a,d]; a+=d; return r; }); }""")
    probs = []
    for i, (ini, dur) in enumerate(tempos):
        t = ini + dur - 0.5  # cena completa, antes da transição
        for e in pg.evaluate(JS_MEDIR, t):
            if e["x0"] < esq - 2 or e["x1"] > w - dir_ + 2 or e["y0"] < topo - 2 or e["y1"] > h - rod + 2:
                probs.append(f"cena {i + 1}: '{e['txt'] or e['tag']}' fora da área segura ({int(e['x0'])},{int(e['y0'])})-({int(e['x1'])},{int(e['y1'])})")
    return probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("saida")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--semente", type=int, default=0)
    ap.add_argument("--sem-conferencia", action="store_true")
    a = ap.parse_args()
    saida = Path(a.saida).resolve()
    with tempfile.TemporaryDirectory(dir=RAIZ) as d:
        pasta = Path(d)
        pagina = _preparar(Path(a.html).resolve(), pasta)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            pg = b.new_page(viewport={"width": a.w, "height": a.h}, device_scale_factor=1)
            pg.goto(f"file://{pagina}", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            dur = pg.evaluate("window.DURACAO")
            eventos = pg.evaluate("window.EVENTOS()")
            if not a.sem_conferencia:
                probs = conferir_area(pg, a.w, a.h)
                if probs:
                    b.close()
                    sys.exit("ERRO: área segura violada:\n- " + "\n- ".join(probs[:15]))
            n = int(round(dur * FPS_RENDER))
            for i in range(n):
                pg.evaluate(f"window.frame({i / FPS_RENDER})")
                pg.screenshot(path=str(pasta / f"f{i:06d}.png"), clip={"x": 0, "y": 0, "width": a.w, "height": a.h})
            b.close()
        # teste da pausa: a tela não pode ficar igual por mais de 1,5 s
        parada, maior = 0, 0
        prev = None
        for i in range(0, n, 6):  # a cada 0,1 s
            im = np.asarray(Image.open(pasta / f"f{i:06d}.png").convert("L").resize((108, 192)), dtype=np.int16)
            if prev is not None and np.abs(im - prev).mean() < 0.35:
                parada += 0.1
                maior = max(maior, parada)
            else:
                parada = 0
            prev = im
        wav = pasta / "audio.wav"
        wavfile.write(str(wav), sfx.SR, sfx.mixar(n / FPS_RENDER, eventos, a.semente))
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS_RENDER), "-i", str(pasta / "f%06d.png"),
               "-i", str(wav), "-vf", "tmix=frames=2:weights='1 1',fps=30", "-c:v", "libx264", "-preset", "veryfast",
               "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
               "-movflags", "+faststart", str(saida)]
        subprocess.run(cmd, check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-show_entries",
                        "format=duration", "-of", "json", str(saida)], capture_output=True, text=True, check=True)
    info = json.loads(r.stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    res = {"largura": v["width"], "altura": v["height"], "duracao": round(float(info["format"]["duration"]), 2),
           "audio": any(s["codec_type"] == "audio" for s in info["streams"]), "mb": round(saida.stat().st_size / 1e6, 2),
           "efeitos_sonoros": len(eventos), "maior_pausa_s": round(maior, 1)}
    print(json.dumps(res, ensure_ascii=False))
    if maior > 1.5:
        sys.exit(f"ERRO: teste da pausa reprovado: tela parada por {maior:.1f} s. Adicione movimento nessa cena.")
    if not res["audio"] or res["mb"] > 100:
        sys.exit("ERRO: vídeo sem áudio ou acima de 100 MB.")


if __name__ == "__main__":
    main()
