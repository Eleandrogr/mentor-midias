"""Gera a CAPA estática (slide 1) de um carrossel da Mentor: PNG 1080x1350, fundo Electric Blue.

O Instagram usa o primeiro item do carrossel como capa no perfil e não deixa trocar depois.
Por isso todo carrossel abre com esta imagem, já com título legível; os vídeos vêm do slide 2 em diante.

Uso:
  python3 ferramentas/capa.py capa.json saida.png [--w 1080 --h 1350]

capa.json:
  {"rotulo": "Inadimplência · ago/2026",          # Geist 600, caixa alta (opcional)
   "numero": "9,3 mi",                            # número-herói (opcional; sem número, o título cresce)
   "titulo": "Recorde de empresas no vermelho",   # Saira, até 6 palavras (obrigatório)
   "apoio": "CNPJs negativados em agosto de 2026.",
   "fonte": "Fonte: Serasa Experian, ... (ago/2026)",  # obrigatório se houver número
   "chamada": "Arraste para ver os dados"}
Também grava o HTML ao lado do PNG (mesmo nome, .html).
"""
import argparse
import html
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
from render import render  # noqa: E402


def montar(c: dict, h: int) -> str:
    e = lambda k: html.escape(c.get(k, "") or "")
    palavras = len((c.get("titulo") or "").split())
    if not c.get("titulo") or palavras > 6:
        sys.exit("ERRO: a capa precisa de título com 1 a 6 palavras.")
    if c.get("numero") and not c.get("fonte"):
        sys.exit("ERRO: capa com número precisa da linha de fonte.")
    tem_num = bool(c.get("numero"))
    tam_tit = 96 if tem_num else 128
    # número-herói cabe na largura útil (904px): Saira ExtraBold ~0,53 em por caractere
    tam_num = min(300, int(904 / (0.55 * max(len(c.get("numero") or "x"), 1))))
    topo = 96 if h <= 1400 else 300
    numero = f'<div class="display numero">{e("numero")}</div>' if tem_num else ""
    rotulo = f'<div class="rotulo">{e("rotulo")}</div>' if c.get("rotulo") else ""
    apoio = f'<p class="apoio">{e("apoio")}</p>' if c.get("apoio") else ""
    fonte = f'<p class="fonte-b">{e("fonte")}</p>' if c.get("fonte") else ""
    chamada = e("chamada") or "Arraste para ver"
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="marca/base.css">
<style>
  .rotulo {{ font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; margin-top: {topo}px; opacity: .9; }}
  .numero {{ font-size: {tam_num}px; line-height: .84; margin-top: 28px; white-space: nowrap; color: #FFFFFF; }}
  .titulo {{ font-size: {tam_tit}px; margin-top: 40px; max-width: 904px; color: #FFFFFF; }}
  .apoio {{ margin-top: 36px; max-width: 860px; color: #FFFFFF; opacity: .92; }}
  .chamada {{ font-size: 30px; font-weight: 600; margin-bottom: 28px; display: flex; align-items: center; }}
  .marcador {{ display: inline-block; width: 22px; height: 22px; border-radius: 4px; background: var(--night); margin-right: 16px; }}
  .fonte-b {{ font-size: 24px; color: #FFFFFF; opacity: .9; border-top: 1px solid rgba(255,255,255,.28); padding-top: 22px; }}
</style></head>
<body><div class="peca blue">
  <img class="logo" src="marca/logos/mentor-logo-sobre-azul.svg" alt="Mentor">
  {rotulo}
  {numero}
  <div class="display titulo">{e("titulo")}</div>
  {apoio}
  <div class="spacer"></div>
  <div class="chamada"><span class="marcador"></span>{chamada} &rarr;</div>
  {fonte}
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
    html_path.write_text(montar(c, a.h), encoding="utf-8")
    render(str(html_path), str(saida), a.w, a.h)
    print(saida)


if __name__ == "__main__":
    main()
