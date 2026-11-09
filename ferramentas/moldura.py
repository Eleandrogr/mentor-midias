"""Confere a ÁREA SEGURA das telas da Mentor e gera prévia com a moldura do Instagram.

Reels / vídeo vertical 1080x1920: a interface cobre
  topo 250px (relógio + menu "Reels"), rodapé 450px (perfil, legenda, comentário),
  direita 150px (curtir, comentar, compartilhar, salvar), esquerda 60px.
  Área útil: x 60–930, y 250–1470 (870x1220). O fundo pode ir até a borda.
Feed / carrossel 1080x1350 (4:5): o grid do perfil mostra só o miolo 3:4
  (corta ~34px de cada lado). Logo, títulos e textos ficam dentro da margem de 88px.

A conferência abre cada tela no estado final da animação e mede a caixa de todo
elemento visível (logo, textos, números, barras). Qualquer coisa fora da área útil
reprova. Também reprova se o conteúdo ocupar menos da metade da altura útil
ou deixar a metade de baixo vazia (layout desequilibrado).

Uso:
  python3 ferramentas/moldura.py --w 1080 --h 1920 tela1.html tela2.html ... [--previa previa.png]
  python3 ferramentas/moldura.py --w 1080 --h 1920 --video reel.mp4 --previa previa.png   # vídeo pronto
Sai com erro (código 1) se alguma tela reprovar. O video.py chama conferir() antes de gravar.
"""
import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
ANIM = (RAIZ / "ferramentas" / "anim.js").read_text(encoding="utf-8")

# margens livres (topo, direita, rodapé, esquerda)
MARGENS = {
    (1080, 1920): {"topo": 250, "direita": 150, "rodape": 450, "esquerda": 60},
    (1080, 1350): {"topo": 88, "direita": 88, "rodape": 88, "esquerda": 88},
    (1080, 1080): {"topo": 88, "direita": 88, "rodape": 88, "esquerda": 88},
}
TOL = 2  # px de tolerância (antisserrilhado)

JS_MEDIR = """
() => {
  window.frame(60);
  const out = [];
  const peca = document.querySelector('.peca');
  const visivel = (el) => {
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.01;
  };
  const nome = (el) => (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/).join('.') : el.tagName.toLowerCase());
  // elementos "de conteúdo": imagens, svg, barras e qualquer elemento com texto próprio
  peca.querySelectorAll('*').forEach((el) => {
    if (!visivel(el) || el.classList.contains('spacer')) return;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    const temTexto = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    const grafico = ['IMG', 'svg', 'SVG'].includes(el.tagName) || el.hasAttribute('data-growx') || el.hasAttribute('data-grow')
      || el.classList.contains('trilho') || el.classList.contains('marcador');
    if (!temTexto && !grafico) return;
    let caixa = {x0: r.left, y0: r.top, x1: r.right, y1: r.bottom};
    if (temTexto) {  // mede o texto de verdade (linhas), não a largura do bloco
      const rg = document.createRange(); rg.selectNodeContents(el);
      const rs = [...rg.getClientRects()].filter((q) => q.width > 0 && q.height > 0);
      if (rs.length) caixa = {x0: Math.min(...rs.map(q => q.left)), y0: Math.min(...rs.map(q => q.top)),
                              x1: Math.max(...rs.map(q => q.right)), y1: Math.max(...rs.map(q => q.bottom))};
    }
    const txt = (el.innerText || el.getAttribute('alt') || '').trim().replace(/\\s+/g, ' ').slice(0, 40);
    out.push({el: nome(el), txt, ...caixa});
  });
  return out;
}
"""


def _preparar(html_path: Path) -> Path:
    html = html_path.read_text(encoding="utf-8")
    if "<base" not in html:
        html = html.replace("<head>", f'<head><base href="file://{RAIZ}/">', 1)
    html = html.replace("</body>", f"<script>{ANIM}</script></body>", 1)
    tmp = html_path.with_name(f".moldura-{html_path.stem}.html")
    tmp.write_text(html, encoding="utf-8")
    return tmp


def area_util(w: int, h: int) -> dict:
    m = MARGENS.get((w, h), {"topo": 88, "direita": 88, "rodape": 88, "esquerda": 88})
    return {"x0": m["esquerda"], "y0": m["topo"], "x1": w - m["direita"], "y1": h - m["rodape"]}


def conferir(telas, w: int, h: int, png_dir: Path | None = None) -> list:
    """Devolve uma lista de problemas (vazia = tudo certo). Se png_dir, grava o quadro final de cada tela."""
    a = area_util(w, h)
    problemas = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        for i, tela in enumerate(telas):
            tela = Path(tela).resolve()
            tmp = _preparar(tela)
            try:
                pg.goto(f"file://{tmp}", wait_until="networkidle")
                pg.evaluate("document.fonts.ready")
                caixas = pg.evaluate(JS_MEDIR)
                if png_dir:
                    pg.screenshot(path=str(Path(png_dir) / f"{i:02d}.png"))
            finally:
                tmp.unlink(missing_ok=True)
            for c in caixas:
                fora = []
                if c["y0"] < a["y0"] - TOL: fora.append(f"topo ({c['y0']:.0f}px < {a['y0']})")
                if c["y1"] > a["y1"] + TOL: fora.append(f"rodapé ({c['y1']:.0f}px > {a['y1']})")
                if c["x1"] > a["x1"] + TOL: fora.append(f"direita ({c['x1']:.0f}px > {a['x1']})")
                if c["x0"] < a["x0"] - TOL: fora.append(f"esquerda ({c['x0']:.0f}px < {a['x0']})")
                if fora:
                    problemas.append(f"{tela.name}: {c['el']} \"{c['txt']}\" invade a margem: {', '.join(fora)}")
            # equilíbrio (só no vertical): conteúdo abaixo do logo precisa usar a altura útil
            if h >= 1700 and caixas:
                corpo = [c for c in caixas if c["el"] != ".logo"]
                if corpo:
                    y0 = min(c["y0"] for c in corpo); y1 = max(c["y1"] for c in corpo)
                    meio = (a["y0"] + a["y1"]) / 2
                    if y1 < meio + 60:
                        problemas.append(f"{tela.name}: metade de baixo da área útil vazia (conteúdo termina em {y1:.0f}px)")
                    if y0 > meio - 60:
                        problemas.append(f"{tela.name}: metade de cima da área útil vazia (conteúdo começa em {y0:.0f}px)")
        b.close()
    return problemas


# ── prévia com a moldura do Instagram ───────────────────────────────────────────
def _overlay_svg(w: int, h: int) -> str:
    if h >= 1700:
        a = area_util(w, h)
        icones = "".join(
            f'<circle cx="{w-75}" cy="{y}" r="34" fill="none" stroke="#fff" stroke-width="5"/>'
            f'<text x="{w-75}" y="{y+70}" fill="#fff" font-size="24" text-anchor="middle" font-family="sans-serif">{t}</text>'
            for y, t in [(1080, "curtir"), (1230, "coment."), (1380, "enviar"), (1530, "salvar")])
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
  <rect x="0" y="0" width="{w}" height="{a['y0']}" fill="#000" fill-opacity=".55"/>
  <rect x="0" y="{a['y1']}" width="{w}" height="{h-a['y1']}" fill="#000" fill-opacity=".55"/>
  <rect x="{a['x1']}" y="{a['y0']}" width="{w-a['x1']}" height="{a['y1']-a['y0']}" fill="#000" fill-opacity=".55"/>
  <rect x="0" y="{a['y0']}" width="{a['x0']}" height="{a['y1']-a['y0']}" fill="#000" fill-opacity=".55"/>
  <rect x="{a['x0']}" y="{a['y0']}" width="{a['x1']-a['x0']}" height="{a['y1']-a['y0']}" fill="none" stroke="#00E676" stroke-width="4" stroke-dasharray="18 10"/>
  <text x="48" y="78" fill="#fff" font-size="40" font-weight="700" font-family="sans-serif">9:41</text>
  <text x="48" y="190" fill="#fff" font-size="52" font-weight="700" font-family="sans-serif">Reels</text>
  {icones}
  <circle cx="90" cy="{h-330}" r="34" fill="#fff" fill-opacity=".85"/>
  <text x="140" y="{h-318}" fill="#fff" font-size="34" font-weight="700" font-family="sans-serif">sistemamentor · Seguir</text>
  <rect x="56" y="{h-260}" width="700" height="22" rx="11" fill="#fff" fill-opacity=".8"/>
  <rect x="56" y="{h-222}" width="520" height="22" rx="11" fill="#fff" fill-opacity=".6"/>
  <rect x="40" y="{h-140}" width="{w-80}" height="84" rx="42" fill="none" stroke="#fff" stroke-width="4"/>
  <text x="80" y="{h-86}" fill="#fff" font-size="32" font-family="sans-serif">Adicione um comentário…</text>
</svg>"""
    # feed 4:5: miniatura do grid é o miolo 3:4
    corte = round((w - h * 3 / 4) / 2)
    a = area_util(w, h)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
  <rect x="0" y="0" width="{corte}" height="{h}" fill="#E0245E" fill-opacity=".45"/>
  <rect x="{w-corte}" y="0" width="{corte}" height="{h}" fill="#E0245E" fill-opacity=".45"/>
  <rect x="{a['x0']}" y="{a['y0']}" width="{a['x1']-a['x0']}" height="{a['y1']-a['y0']}" fill="none" stroke="#00E676" stroke-width="4" stroke-dasharray="18 10"/>
  <text x="{w/2}" y="40" fill="#E0245E" font-size="26" text-anchor="middle" font-family="sans-serif">faixas vermelhas: cortadas na miniatura do grid do perfil</text>
</svg>"""


def previa(telas, w: int, h: int, saida: Path) -> list:
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory(dir=RAIZ) as d:
        d = Path(d)
        problemas = conferir(telas, w, h, png_dir=d)
        svg = d / "moldura.svg"; svg.write_text(_overlay_svg(w, h), encoding="utf-8")
        ov = d / "moldura.png"
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(f"file://{svg}"); pg.screenshot(path=str(ov), omit_background=True)
            b.close()
        n = len(telas)
        ins = []
        for i in range(n):
            ins += ["-i", str(d / f"{i:02d}.png")]
        ins += ["-i", str(ov)]
        f = "".join(f"[{i}][{n}]overlay[o{i}];" for i in range(n))
        f += "".join(f"[o{i}]" for i in range(n)) + (f"hstack={n}" if n > 1 else "null") + f",scale={min(n*w, 2400)//1}:-2[s]"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", f, "-map", "[s]",
                        "-frames:v", "1", str(saida)], check=True)
    return problemas


def previa_video(video: Path, w: int, h: int, saida: Path, n: int = 4, seg: float = 0) -> None:
    """Prévia do VÍDEO pronto: n quadros (fim de cada trecho) com a moldura do Instagram por cima."""
    import subprocess
    import tempfile
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(video)], capture_output=True, text=True, check=True).stdout)
    with tempfile.TemporaryDirectory(dir=RAIZ) as d:
        d = Path(d)
        svg = d / "moldura.svg"; svg.write_text(_overlay_svg(w, h), encoding="utf-8")
        ov = d / "moldura.png"
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(f"file://{svg}"); pg.screenshot(path=str(ov), omit_background=True)
            b.close()
        # troca de tela = corte de cena; pega o quadro 0,25 s antes de cada troca e o fim do vídeo
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "select='gt(scene,0.25)',showinfo",
                            "-f", "null", "-"], capture_output=True, text=True)
        import re
        trocas = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
        trocas = [t for t in trocas if t > 0.5]
        tempos = [t - 0.25 for t in trocas] + [dur - 0.1]
        if seg:  # duração por tela conhecida: cada tela termina em dur - k*seg (o corte do início só afeta a 1ª)
            tempos = [dur - (n - 1 - i) * seg - 0.15 for i in range(n)]
        elif len(tempos) != n:  # sem cortes claros: divide por igual
            tempos = [dur * (i + 1) / n - 0.4 for i in range(n)]
        ins = []
        for i, t in enumerate(tempos[:n]):
            q = d / f"q{i}.png"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", str(q)], check=True)
            ins += ["-i", str(q)]
        ins += ["-i", str(ov)]
        f = "".join(f"[{i}][{n}]overlay[o{i}];" for i in range(n))
        f += "".join(f"[o{i}]" for i in range(n)) + (f"hstack={n}" if n > 1 else "null") + f",scale={min(n*w, 2400)}:-2[s]"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", f, "-map", "[s]",
                        "-frames:v", "1", str(saida)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("telas", nargs="*")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--previa", help="grava PNG com as telas (estado final) e a moldura sobreposta")
    ap.add_argument("--video", help="em vez de telas HTML: MP4 pronto; grava em --previa n quadros com a moldura")
    ap.add_argument("--quadros", type=int, default=4)
    ap.add_argument("--seg", type=float, default=0, help="segundos por tela (deixa a prévia do vídeo exata)")
    a = ap.parse_args()
    if a.video:
        previa_video(Path(a.video), a.w, a.h, Path(a.previa or "previa-moldura.png"), a.quadros, a.seg)
        print(a.previa or "previa-moldura.png")
        return
    if a.previa:
        probs = previa(a.telas, a.w, a.h, Path(a.previa))
    else:
        probs = conferir(a.telas, a.w, a.h)
    print(json.dumps({"ok": not probs, "problemas": probs}, ensure_ascii=False, indent=1))
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
