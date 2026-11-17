"""Gera a CAPA estática (slide 1) de um carrossel da Mentor — regras de nov/2026.

- Fundo segue a alternância do grid: blue -> cloud -> night (nunca só azul).
- Abre com uma SITUAÇÃO ou PERGUNTA em 1ª pessoa (Saira, maiúsculas, título ≥ 90px).
- Traz uma PRÉVIA do que vem: mini gráfico (sem eixos, rótulo no dado) ou print do Mentor.
- Número gigante sozinho na capa é proibido (não existe campo "numero").
- Título no miolo da peça (o grid corta para 3:4), nunca colado no topo. Logo ≥ 48px.

Uso:
  python3 ferramentas/capa.py capa.json saida.png [--w 1080 --h 1350]

capa.json:
  {"fundo": "cloud",
   "titulo": "Fechei o mês sem saber quanto tinha no estoque",   # até 12 palavras
   "apoio": "O que eu faria na primeira semana.",                  # opcional, até 12 palavras
   "previa": {"tipo": "barras", "series": [{"rotulo": "Planilha", "valor": 38}, {"rotulo": "Sistema", "valor": 62, "destaque": true}], "sufixo": "%"},
   #   ou {"tipo": "tela", "img": "marca/telas-site/gestao_de_estoque.png", "legenda": "Estoque no Mentor"}
   #   ou {"tipo": "linha", "pontos": [100, 92, 80, 61, 40, 12], "rotulo_fim": "caixa"}   (forma ilustrativa: sem números)
   "chamada": "Arraste para ver a conta"}
"""
import argparse
import html
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
from render import render  # noqa: E402

LOGOS = {"blue": "mentor-logo-sobre-azul.svg", "cloud": "mentor-logo-claro.svg", "night": "mentor-logo-escuro.svg"}
CORES = {  # texto, apoio, destaque, barra comum, trilho
    "blue": ("#FFFFFF", "rgba(255,255,255,.88)", "#1E272E", "rgba(255,255,255,.45)", "rgba(30,39,46,.18)"),
    "cloud": ("#1E272E", "#5B6670", "#0984E3", "#C5CBD3", "rgba(30,39,46,.08)"),
    "night": ("#F5F6FA", "#A3AFB8", "#00CEC9", "#46535E", "rgba(245,246,250,.08)"),
}


def _fmt(v, suf):
    s = f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if s.endswith(",0"):
        s = s[:-2]
    return s + (suf or "")


def previa_html(p: dict, fundo: str) -> str:
    txt, apoio, dest, comum, trilho = CORES[fundo]
    if not p:
        return ""
    if p["tipo"] == "barras":
        mx = max(s["valor"] for s in p["series"]) or 1
        linhas = []
        for s in p["series"][:4]:
            cor = dest if s.get("destaque") else comum
            linhas.append(f'''<div class="pb"><div class="pr">{html.escape(s["rotulo"])}</div>
              <div class="pt"><div class="pf" style="width:calc((100% - 200px) * {s["valor"] / mx:.3f});background:{cor}"></div>
              <span class="pv mono" style="color:{dest if s.get("destaque") else txt}">{_fmt(s["valor"], p.get("sufixo"))}</span></div></div>''')
        return f'<div class="previa barras" style="background:{trilho}">{"".join(linhas)}</div>'
    if p["tipo"] == "linha":
        pts = p["pontos"]
        mx = max(pts) or 1
        w, h = 560, 240
        xy = [(i * w / (len(pts) - 1), h - v / mx * (h - 20)) for i, v in enumerate(pts)]
        d = " ".join(f"{x:.0f},{y:.0f}" for x, y in xy)
        x2, y2 = xy[-1]
        rot = html.escape(p.get("rotulo_fim", ""))
        return f'''<div class="previa" style="background:{trilho}"><svg width="{w + 260}" height="{h + 30}" viewBox="-10 -10 {w + 260} {h + 30}">
          <polyline points="{d}" fill="none" stroke="{dest}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="{x2:.0f}" cy="{y2:.0f}" r="16" fill="{dest}"/>
          <text x="{x2 + 28:.0f}" y="{y2 + 10:.0f}" font-family="Geist" font-weight="600" font-size="34" fill="{txt}">{rot}</text></svg></div>'''
    if p["tipo"] == "tela":
        img = RAIZ / p["img"]
        if not img.exists():
            sys.exit(f"ERRO: print do Mentor não encontrado: {p['img']}")
        leg = f'<div class="leg">{html.escape(p.get("legenda", ""))}</div>' if p.get("legenda") else ""
        return f'<div class="previa tela"><div class="moldura"><img src="{p["img"]}"></div>{leg}</div>'
    sys.exit("ERRO: previa.tipo deve ser barras, linha ou tela.")


def montar(c: dict, w: int, h: int) -> str:
    if "numero" in c:
        sys.exit("ERRO: número gigante na capa é proibido. Use uma situação/pergunta e uma prévia.")
    fundo = c.get("fundo", "cloud")
    if fundo not in LOGOS:
        sys.exit("ERRO: fundo deve ser blue, cloud ou night.")
    tit = c.get("titulo") or ""
    n = len(tit.split())
    if not 3 <= n <= 12:
        sys.exit("ERRO: título da capa com 3 a 12 palavras (situação ou pergunta em 1ª pessoa).")
    txt, apoio, dest, _, _ = CORES[fundo]
    tam = 112 if n <= 6 else 100 if n <= 9 else 92
    e = lambda k: html.escape(c.get(k, "") or "")
    ap = f'<p class="apoio">{e("apoio")}</p>' if c.get("apoio") else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="marca/base.css">
<style>
  .peca {{ background: var(--{fundo}); color: {txt}; justify-content: space-between; }}
  .logo {{ height: 60px; }}
  .miolo {{ display: flex; flex-direction: column; gap: 44px; }}
  .titulo {{ font-size: {tam}px; line-height: .98; color: {txt}; max-width: 904px; }}
  .titulo .ponto {{ color: {dest}; }}
  .apoio {{ font-size: 40px; color: {apoio}; max-width: 880px; margin-top: -12px; }}
  .previa {{ border-radius: 22px; padding: 34px 36px; }}
  .barras {{ display: flex; flex-direction: column; gap: 22px; }}
  .pb {{ display: grid; grid-template-columns: 230px 1fr; align-items: center; gap: 20px; }}
  .pr {{ font-size: 34px; font-weight: 600; }}
  .pt {{ position: relative; height: 64px; display: flex; align-items: center; }}
  .pf {{ height: 100%; border-radius: 8px; flex-shrink: 0; }}
  .pv {{ font-size: 38px; font-weight: 500; margin-left: 16px; white-space: nowrap; }}
  .tela {{ padding: 0; }}
  .moldura {{ border-radius: 22px; overflow: hidden; border: 3px solid {dest}; max-height: 420px; }}
  .moldura img {{ width: 100%; display: block; }}
  .leg {{ font-size: 28px; color: {apoio}; margin-top: 14px; }}
  .chamada {{ font-size: 34px; font-weight: 600; display: flex; align-items: center; }}
  .marcador {{ display: inline-block; width: 26px; height: 26px; border-radius: 5px; background: {dest}; margin-right: 18px; }}
</style></head>
<body><div class="peca">
  <img class="logo" src="marca/logos/{LOGOS[fundo]}" alt="Mentor">
  <div class="miolo">
    <div class="display titulo">{html.escape(tit)}<span class="ponto">{"" if tit.rstrip().endswith("?") else "."}</span></div>
    {ap}
    {previa_html(c.get("previa"), fundo)}
  </div>
  <div class="chamada"><span class="marcador"></span>{e("chamada") or "Arraste para ver"} &rarr;</div>
</div></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("saida")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1350)
    a = ap.parse_args()
    c = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    saida = Path(a.saida)
    html_path = saida.with_suffix(".html")
    html_path.write_text(montar(c, a.w, a.h), encoding="utf-8")
    render(str(html_path), str(saida), a.w, a.h)
    print(saida)


if __name__ == "__main__":
    main()
