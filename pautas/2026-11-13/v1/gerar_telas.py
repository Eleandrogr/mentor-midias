"""Gera as telas HTML da pauta 2026-11-13 v1 (tema: taxa de margem de comercialização, markup x margem; IBGE, PAC 2024)."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTE = "Fonte: IBGE, Pesquisa Anual de Comércio 2024 (2026)"
CALC = "Cálculo Mentor sobre IBGE, Pesquisa Anual de Comércio 2024 (2026)"

CSS_COMUM = """
  .fonte-n { color: var(--muted-dark); border-top: 1px solid rgba(245,246,250,.18); padding-top: 22px; }
  .fonte-c { color: var(--muted-light); border-top: 1px solid rgba(30,39,46,.14); padding-top: 22px; }
  .fonte-b { color: #FFFFFF; opacity: .9; border-top: 1px solid rgba(255,255,255,.28); padding-top: 22px; }
  .fonte-n, .fonte-c, .fonte-b { font-size: 24px; }
  .ponto { color: var(--blue); }
  .marcador { display: inline-block; width: 22px; height: 22px; border-radius: 4px; background: var(--night); margin-right: 16px; vertical-align: -2px; }
  .topo { margin-top: 130px; }
  @media (min-height: 1700px) { .grafico { margin-top: 96px !important; } }  /* área segura do Reels: marca/base.css */
"""


def pagina(fundo, corpo, css=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="marca/base.css">
<style>{CSS_COMUM}{css}</style></head>
<body><div class="peca {fundo}">
{corpo}
</div></body></html>
"""


LOGO = {"night": "mentor-logo-escuro.svg", "cloud": "mentor-logo-claro.svg", "blue": "mentor-logo-sobre-azul.svg"}


def logo(f):
    return f'  <img class="logo" src="marca/logos/{LOGO[f]}" alt="Mentor" data-in="0">'


def dado_night(numero, count, dec, titulo, apoio, suf=""):
    css = """
  .numero { font-size: 380px; color: var(--cyan); line-height: 0.82; }
  .titulo { font-size: 84px; margin-top: 52px; max-width: 904px; }
  .apoio { color: var(--muted-dark); margin-top: 36px; max-width: 860px; }"""
    corpo = f"""{logo('night')}
  <div class="display numero topo" data-in="0.3" data-count="{count}" data-decimals="{dec}" data-suffix="{suf}">{numero}</div>
  <div class="display titulo" data-in="1.3">{titulo}</div>
  <p class="apoio" data-in="1.9">{apoio}</p>
  <div class="spacer"></div>
  <p class="fonte-n" data-in="2.5">{FONTE}</p>"""
    return pagina("night", corpo, css)


def dado_cloud(numero, count, dec, pre, suf, titulo, apoio, tam=300, fonte=None):
    fonte = fonte or FONTE
    css = f"""
  .numero {{ font-size: {tam}px; color: var(--night); line-height: 0.86; white-space: nowrap; }}
  .titulo {{ font-size: 84px; margin-top: 52px; max-width: 904px; }}
  .apoio {{ color: var(--muted-light); margin-top: 36px; max-width: 860px; }}"""
    corpo = f"""{logo('cloud')}
  <div class="display numero topo" data-in="0.3" data-count="{count}" data-decimals="{dec}" data-prefix="{pre}" data-suffix="{suf}">{numero}</div>
  <div class="display titulo" data-in="1.3">{titulo}<span class="ponto">.</span></div>
  <p class="apoio" data-in="1.9">{apoio}</p>
  <div class="spacer"></div>
  <p class="fonte-c" data-in="2.5">{fonte}</p>"""
    return pagina("cloud", corpo, css)


def barras(fundo, titulo, subtitulo, series, dec=0, col=300, alto=False, fonte=None):
    fonte = fonte or FONTE
    maior = max(v for _, v, _ in series)
    if fundo == "night":
        cinza, dest, cval, cdest, cap, crot, cf = "#46535E", "var(--cyan)", "var(--muted-dark)", "var(--cyan)", "var(--muted-dark)", "var(--cloud)", "fonte-n"
        ponto = ""
    else:
        cinza, dest, cval, cdest, cap, crot, cf = "#C5CBD3", "var(--blue)", "var(--muted-light)", "var(--night)", "var(--muted-light)", "var(--night)", "fonte-c"
        ponto = '<span class="ponto" style="color:var(--night)">.</span>'
    css = f"""
  .titulo {{ font-size: 76px; margin-top: 64px; max-width: 904px; }}
  .apoio {{ color: {cap}; margin-top: 20px; max-width: 860px; font-size: 30px; }}
  .grafico {{ margin-top: 56px; display: flex; flex-direction: column; gap: 26px; }}
  .linha {{ display: grid; grid-template-columns: {col}px 1fr 110px; align-items: center; gap: 20px; }}
  .rotulo {{ font-size: 28px; color: {crot}; }}
  .trilho {{ height: 44px; position: relative; }}
  .barra {{ position: absolute; inset: 0 auto 0 0; border-radius: 4px; background: {cinza}; min-width: 4px; }}
  .barra.destaque {{ background: {dest}; }}
  .valor {{ font: 500 32px "Geist Mono", monospace; color: {cval}; text-align: right; font-variant-numeric: tabular-nums; }}
  .valor.destaque {{ color: {cdest}; }}"""
    if alto:  # 2 séries: barras grossas e valores grandes (gráfico ocupa a tela e o 1º quadro tem conteúdo)
        css += f"""
  .grafico {{ margin-top: 88px; gap: 56px; }}
  .linha {{ grid-template-columns: 1fr; gap: 16px; }}
  .linha .cab {{ display: flex; justify-content: space-between; align-items: baseline; }}
  .rotulo {{ font-size: 36px; }}
  .trilho {{ height: 120px; }}
  .valor {{ font-size: 72px; text-align: right; }}"""
    if alto == "medio":  # 3 séries: barras médias, cabem em 1080x1350 sem deixar a metade de baixo vazia
        css += """
  .grafico { margin-top: 64px; gap: 36px; }
  .trilho { height: 76px; }
  .valor { font-size: 52px; }
  .rotulo { font-size: 32px; }"""
    linhas = []
    t = 1.0
    for rot, v, d in series:
        cls = " destaque" if d else ""
        w = round(v / maior * 100, 1)
        txt = (f"{v:.{dec}f}".replace(".", ",")) + "%"
        barra = f'<div class="trilho"><div class="barra{cls}" style="width:{w}%" data-growx="{t + 0.1:.1f}"></div></div>'
        valor = f'<span class="valor{cls}" data-in="{t + 0.1:.1f}" data-count="{v}" data-decimals="{dec}" data-suffix="%">{txt}</span>'
        if alto:
            linhas.append(f'    <div class="linha" data-in="{t:.1f}"><div class="cab"><span class="rotulo">{rot}</span>{valor}</div>{barra}</div>')
        else:
            linhas.append(f'    <div class="linha" data-in="{t:.1f}"><span class="rotulo">{rot}</span>{barra}{valor}</div>')
        t += 0.2
    corpo = f"""{logo(fundo)}
  <div class="display titulo" data-in="0.3">{titulo}</div>
  <p class="apoio" data-in="0.7">{subtitulo}</p>
  <div class="grafico">
{chr(10).join(linhas)}
  </div>
  <div class="spacer"></div>
  <p class="{cf}" data-in="{t + 0.4:.1f}">{fonte}</p>"""
    return pagina(fundo, corpo, css)


def assinatura_blue(apoio, cta):
    css = """
  .titulo { font-size: 150px; line-height: 0.94; }
  .apoio { margin-top: 48px; max-width: 800px; font-size: 36px; }
  .cta { margin-top: 40px; font: 600 32px "Geist", sans-serif; }"""
    corpo = f"""{logo('blue')}
  <div class="display titulo topo" data-in="0.3">Clareza<br>para<br>decidir.</div>
  <p class="apoio" data-in="1.1"><span class="marcador"></span>{apoio}</p>
  <p class="cta" data-in="1.7">{cta}</p>
  <div class="spacer"></div>
  <div class="fonte-b" data-in="1.7" style="display:flex;justify-content:space-between"><span>ERP em nuvem</span><span>by EGR Systems</span></div>"""
    return pagina("blue", corpo, css)


def gancho_blue(rotulo, titulo, apoio, fonte=None):
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; opacity: .9; }
  .titulo { font-size: 124px; margin-top: 24px; max-width: 904px; }
  .apoio { margin-top: 48px; max-width: 820px; font-size: 36px; }"""
    corpo = f"""{logo('blue')}
  <div class="rotulo topo" data-in="0.3">{rotulo}</div>
  <div class="display titulo" data-in="0.6">{titulo}</div>
  <p class="apoio" data-in="1.4"><span class="marcador"></span>{apoio}</p>"""
    if fonte:
        corpo += f'''
  <div class="spacer"></div>
  <p class="fonte-b" data-in="1.8">{fonte}</p>'''
    return pagina("blue", corpo, css)


def progresso_night(v, titulo, apoio, leg, total="100% das empresas", dec=0, fonte=None):
    fonte = fonte or FONTE
    vt = f"{v:.{dec}f}".replace(".", ",")
    css = """
  .numero { font-size: 380px; color: var(--cyan); line-height: 0.82; }
  .titulo { font-size: 84px; margin-top: 52px; max-width: 904px; }
  .apoio { color: var(--muted-dark); margin-top: 32px; max-width: 860px; }
  .grafico { margin-top: 56px; }
  .trilho { height: 44px; position: relative; background: #46535E; border-radius: 4px; overflow: hidden; }
  .barra { position: absolute; inset: 0 auto 0 0; background: var(--cyan); border-radius: 4px; }
  .legenda { display: flex; justify-content: space-between; margin-top: 16px; font: 500 28px "Geist Mono", monospace; color: var(--muted-dark); }
  .legenda .d { color: var(--cyan); }"""
    corpo = f"""{logo('night')}
  <div class="display numero topo" data-in="0.3" data-count="{v}" data-decimals="{dec}" data-suffix="%">{vt}%</div>
  <div class="display titulo" data-in="1.0">{titulo}</div>
  <p class="apoio" data-in="1.5">{apoio}</p>
  <div class="grafico" data-in="1.8">
    <div class="trilho"><div class="barra" style="width:{v}%" data-growx="1.9"></div></div>
    <div class="legenda"><span class="d">{leg}: {vt}%</span><span>{total}</span></div>
  </div>
  <div class="spacer"></div>
  <p class="fonte-n" data-in="2.5">{fonte}</p>"""
    return pagina("night", corpo, css)


def checklist_cloud(rotulo, titulo, itens, fonte=None):
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--muted-light); }
  .titulo { font-size: 96px; margin-top: 20px; max-width: 904px; }
  .lista { margin-top: 56px; display: flex; flex-direction: column; gap: 28px; }
  .item { display: grid; grid-template-columns: 76px 1fr; gap: 12px; align-items: baseline; border-top: 1px solid rgba(30,39,46,.14); padding-top: 26px; }
  .item .n { font: 500 40px "Geist Mono", monospace; color: var(--muted-light); }
  .item p { font-size: 34px; line-height: 1.35; }
  .item p span { display: block; font-size: 28px; color: var(--muted-light); margin-top: 6px; }"""
    corpo = f"""{logo('cloud')}
  <div class="rotulo topo" data-in="0.3">{rotulo}</div>
  <div class="display titulo" data-in="0.6">{titulo}<span class="ponto">.</span></div>
  <div class="lista">
{itens_html(itens)}
  </div>"""
    if fonte:
        corpo += f'''
  <div class="spacer"></div>
  <p class="fonte-c" data-in="2.6">{fonte}</p>'''
    return pagina("cloud", corpo, css)




def itens_html(itens):
    out = []
    for k, (a, b) in enumerate(itens):
        out.append(f'    <div class="item" data-in="{1.2 + 0.4 * k:.1f}"><span class="n">0{k + 1}</span><p>{a}<span>{b}</span></p></div>')
    return "\n".join(out)


def frase_night(titulo, apoio):
    css = """
  .titulo { font-size: 110px; max-width: 904px; line-height: .96; }
  .apoio { color: var(--muted-dark); margin-top: 48px; max-width: 860px; font-size: 36px; }
  .ponto-c { color: var(--cyan); }"""
    corpo = f"""{logo('night')}
  <div class="display titulo topo" data-in="0.3">{titulo}<span class="ponto-c">.</span></div>
  <p class="apoio" data-in="1.2">{apoio}</p>
  <div class="spacer"></div>
  <div class="fonte-n" data-in="1.8" style="display:flex;justify-content:space-between"><span>ERP em nuvem</span><span>by EGR Systems</span></div>"""
    return pagina("night", corpo, css)


CTA = "Ver o Mentor com os meus dados"

TELAS = {
    "p1": [
        barras("night", "Varejo põe mais sobre o custo", "Taxa de margem de comercialização, % sobre o custo da mercadoria, 2024",
               [("Comércio varejista", 38.6, True), ("Veículos, peças e motos", 23.2, False), ("Comércio por atacado", 22.0, False)],
               dec=1, col=400, alto="medio"),
        barras("cloud", "Do vestuário ao combustível", "Taxa de margem por atividade, % sobre o custo da mercadoria, 2024",
               [("Varejo de vestuário", 86.1, True), ("Varejo de tecidos e armarinho", 77.9, False),
                ("Varejo cultural e esportivo", 72.1, False), ("Comércio de veículos", 14.2, False),
                ("Atacado de matérias&#8209;primas agrícolas", 12.9, False), ("Atacado de combustíveis", 6.3, False)],
               dec=1, col=420),
        assinatura_blue("O custo de cada mercadoria e a margem de cada venda, no mesmo relatório.", CTA),
    ],
    "p2": [
        dado_cloud("R$ 138,60", 138.6, 2, "R$ ", "", "Preço com 38,6% sobre custo",
                   "Uma mercadoria que custou R$ 100, vendida com a taxa de margem média do varejo em 2024.", tam=165, fonte=CALC),
        barras("night", "Margem real é menor", "Mesma venda de R$ 138,60, medida de dois jeitos, %",
               [("Sobre o custo (markup)", 38.6, False), ("Sobre a venda (margem)", 27.8, True)], dec=1, alto=True, fonte=CALC),
        checklist_cloud("Indicadores e KPIs", "Duas contas, dois nomes", [
            ("Markup = (venda − custo) ÷ custo", "R$ 38,60 ÷ R$ 100 = 38,6%"),
            ("Margem = (venda − custo) ÷ venda", "R$ 38,60 ÷ R$ 138,60 = 27,8%"),
            ("Despesas e impostos saem da margem", "aluguel, folha e tributos são pagos com os 27,8%, não com os 38,6%"),
        ], fonte=CALC),
        assinatura_blue("Preço, custo e margem de cada produto calculados do mesmo jeito.", CTA),
    ],
    "p3": [
        gancho_blue("Comércio · IBGE 2024", "86,1% sobre o custo",
                    "é a taxa de margem do varejo de vestuário, a maior do comércio. No atacado de combustíveis, 6,3%.", fonte=FONTE),
        barras("night", "Mesmo comércio, margens opostas", "Taxa de margem de comercialização, % sobre o custo da mercadoria, 2024",
               [("Varejo de vestuário", 86.1, True), ("Atacado de combustíveis", 6.3, False)], dec=1, alto=True),
        checklist_cloud("Indicadores e KPIs", "Três contas antes do preço", [
            ("Quanto custou a mercadoria?", "preço do fornecedor, frete e impostos da compra"),
            ("Quanto sobra da venda?", "margem = (venda − custo) ÷ venda, e não ÷ custo"),
            ("A margem paga a operação?", "aluguel, folha e tributos precisam caber nela"),
        ]),
        assinatura_blue("A margem de cada produto, calculada sobre a venda.", CTA),
    ],
}

if __name__ == "__main__":
    for peca, telas in TELAS.items():
        d = AQUI / peca
        d.mkdir(parents=True, exist_ok=True)
        for i, html in enumerate(telas, 1):
            (d / f"tela{i}.html").write_text(html, encoding="utf-8")
    print("ok")
