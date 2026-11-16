"""Gera as telas HTML da pauta 2026-11-17 v1 (tema: 13º salário sem aperto no caixa; Sebrae-SP 2024, Lei 4.090/1962, Lei 4.749/1965, Lei 8.036/1990)."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTE = "Fonte: Sebrae-SP e Fundação Seade, Indicadores Sebrae-SP, MPEs e o 13º salário (2024)"

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


def dado_night(numero, count, dec, titulo, apoio, suf="", tam=380, fonte=None, pre=""):
    fonte = fonte or FONTE
    css = f"""
  .numero {{ font-size: {tam}px; color: var(--cyan); line-height: 0.82; white-space: nowrap; }}
  .titulo {{ font-size: 84px; margin-top: 52px; max-width: 904px; }}
  .apoio {{ color: var(--muted-dark); margin-top: 36px; max-width: 860px; }}"""
    corpo = f"""{logo('night')}
  <div class="display numero topo" data-in="0.3" data-count="{count}" data-decimals="{dec}" data-prefix="{pre}" data-suffix="{suf}">{numero}</div>
  <div class="display titulo" data-in="1.3">{titulo}</div>
  <p class="apoio" data-in="1.9">{apoio}</p>
  <div class="spacer"></div>
  <p class="fonte-n" data-in="2.5">{fonte}</p>"""
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


def barras(fundo, titulo, subtitulo, series, dec=0, col=300, alto=False, fonte=None, pre="", suf="%", colv=110, milhar=False):
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
  .linha {{ display: grid; grid-template-columns: {col}px 1fr {colv}px; align-items: center; gap: 20px; }}
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
        txt = pre + (f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".") if milhar else f"{v:.{dec}f}".replace(".", ",")) + suf
        barra = f'<div class="trilho"><div class="barra{cls}" style="width:{w}%" data-growx="{t + 0.1:.1f}"></div></div>'
        valor = f'<span class="valor{cls}" data-in="{t + 0.1:.1f}" data-count="{v}" data-decimals="{dec}" data-prefix="{pre}" data-suffix="{suf}">{txt}</span>'
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
  .item { display: grid; grid-template-columns: var(--coln, 76px) 1fr; gap: 12px; align-items: baseline; border-top: 1px solid rgba(30,39,46,.14); padding-top: 26px; }
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
    for k, it in enumerate(itens):
        a, b = it[0], it[1]
        n = it[2] if len(it) > 2 else f"0{k + 1}"
        out.append(f'    <div class="item" data-in="{1.2 + 0.4 * k:.1f}"><span class="n">{n}</span><p>{a}<span>{b}</span></p></div>')
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




def formula_cloud(rotulo, titulo, formula, linhas, apoio):
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--muted-light); }
  .titulo { font-size: 96px; margin-top: 20px; max-width: 904px; }
  .formula { margin-top: 56px; border-top: 1px solid rgba(30,39,46,.14); border-bottom: 1px solid rgba(30,39,46,.14); padding: 36px 0; font: 500 40px/1.4 "Geist Mono", monospace; color: var(--night); }
  .ex { margin-top: 40px; display: flex; flex-direction: column; gap: 18px; }
  .ex div { display: flex; justify-content: space-between; font: 500 34px "Geist Mono", monospace; color: var(--muted-light); font-variant-numeric: tabular-nums; }
  .ex div.r { color: var(--night); border-top: 1px solid rgba(30,39,46,.14); padding-top: 18px; }
  .apoio { color: var(--muted-light); margin-top: 40px; max-width: 860px; font-size: 30px; }"""
    ex = "\n".join(f'    <div class="{c}" data-in="{1.5 + 0.4 * k:.1f}"><span>{a}</span><span>{b}</span></div>' for k, (a, b, c) in enumerate(linhas))
    corpo = f"""{logo('cloud')}
  <div class="rotulo topo" data-in="0.3">{rotulo}</div>
  <div class="display titulo" data-in="0.6">{titulo}<span class="ponto">.</span></div>
  <div class="formula" data-in="1.1">{formula}</div>
  <div class="ex">
{ex}
  </div>
  <p class="apoio" data-in="2.9">{apoio}</p>"""
    return pagina("cloud", corpo, css)


CTA = "Ver o Mentor com os meus dados"
F_LEI = "Fonte: Lei 4.090/1962, art. 1º; Lei 8.036/1990, art. 15"
F_CAL = "Fonte: Lei 4.749/1965, arts. 1º e 2º; Lei 8.036/1990, art. 15"
F_EX = "Cálculo ilustrativo pela Lei 4.090/1962 (1/12 por mês) e Lei 8.036/1990 (FGTS de 8%)"

TELAS = {
    "p1": [
        barras("night", "Reserva subiu desde 2019", "% das MPEs paulistas que fizeram reservas para pagar o 13º",
               [("2019", 37.4, False), ("2022", 45.1, False), ("2023", 44.7, False), ("2024", 53.4, True)],
               dec=1, col=160, colv=170, alto="medio").replace(
            ".grafico { margin-top: 64px; gap: 36px; }", ".grafico { margin-top: 48px; gap: 24px; }").replace(
            ".trilho { height: 76px; }", ".trilho { height: 56px; }"),
        progresso_night(62.9, "Sem reserva, mais aperto",
                        "dos que acham mais difícil pagar o 13º não fizeram provisões.",
                        "Não reservaram", total="Acham mais difícil", dec=1).replace("font-size: 380px", "font-size: 250px"),
        checklist_cloud("Gestão financeira", "Reserva sem susto", [
            ("Comece cedo", "entre quem reservou, 74,2% começou até julho"),
            ("Reserve 1/12 por mês", "é a parte do 13º que cada mês de trabalho gera"),
            ("Separe o valor", "a reserva não paga despesa do mês"),
        ], fonte=FONTE),
        assinatura_blue("13º e encargos provisionados mês a mês, ao lado do fluxo de caixa.", CTA),
    ],
    "p2": [
        formula_cloud("Como calcular", "Reserva mensal do 13º",
                      "salário ÷ 12 × 1,08",
                      [("Salário (exemplo)", "R$ 3.000,00", ""), ("13º do mês (÷ 12)", "R$ 250,00", ""),
                       ("FGTS de 8% sobre ele", "R$ 20,00", ""), ("Reserva do mês", "R$ 270,00", "r")],
                      "Valores ilustrativos. 8,33% do 13º + FGTS = 9% do salário por mês."),
        barras("night", "R$ 32.400 em dezembro", "Reserva acumulada (13º + FGTS) de uma folha de R$ 30 mil por mês, exemplo, em R$",
               [("Fev", 5400, False), ("Abr", 10800, False), ("Jun", 16200, False), ("Ago", 21600, False),
                ("Out", 27000, False), ("Dez", 32400, True)],
               dec=0, col=110, colv=230, pre="R$ ", suf="", milhar=True, fonte=F_EX).replace(
            "gap: 26px; }", "gap: 34px; }").replace("height: 44px;", "height: 60px;").replace(
            "font: 500 32px", "font: 500 38px").replace(".rotulo { font-size: 28px", ".rotulo { font-size: 34px"),
        checklist_cloud("Calendário 2026", "Duas datas no caixa", [
            ("1ª parcela até 30/11", "metade do salário do mês anterior", "30/11"),
            ("2ª parcela até 20/12", "o saldo; em 2026, o dia 20 cai num domingo", "20/12"),
            ("FGTS sobre o 13º", "8% depositados até o dia 20 do mês seguinte", "8%"),
        ], fonte=F_CAL).replace('<div class="peca cloud">', '<div class="peca cloud" style="--coln:160px">'),
        assinatura_blue("13º e FGTS provisionados todo mês, sem surpresa em novembro.", CTA),
    ],
    "p3": [
        gancho_blue("13º salário · 2026", "1ª parcela até 30/11",
                    "Metade do salário do mês anterior, paga de uma só vez entre fevereiro e novembro.", fonte="Fonte: Lei 4.749/1965, art. 2º").replace(
            ".titulo { font-size: 124px;", ".titulo { font-size: 136px;").replace(
            ".apoio { margin-top: 48px; max-width: 820px; font-size: 36px; }", ".apoio { margin-top: 48px; max-width: 820px; font-size: 46px; line-height: 1.3; }"),
        formula_cloud("Como calcular", "Quanto sai em novembro",
                      "salário de outubro ÷ 2",
                      [("Salário de outubro (exemplo)", "R$ 3.000", ""), ("1ª parcela", "R$ 1.500", "r")],
                      "Valores ilustrativos. O saldo vai até 20/12; em 2026, o dia 20 cai num domingo."),
        progresso_night(62.9, "Sem reserva, mais aperto",
                        "dos que acham mais difícil pagar o 13º não fizeram provisões.",
                        "Não reservaram", total="Acham mais difícil", dec=1).replace("font-size: 380px", "font-size: 250px"),
        assinatura_blue("13º provisionado mês a mês, sem aperto no fim do ano.", CTA),
    ],
}

# Abertura dos vídeos únicos da p2 (Facebook e LinkedIn): o 1º quadro precisa de conteúdo forte
ABERTURAS = {
    "p2": dado_cloud("8,33%", 8.33, 2, "", "%", "Da folha, todo mês",
                     "é 1/12 da remuneração por mês de serviço. Com o FGTS de 8% sobre ele, a reserva vai a 9%.",
                     tam=260, fonte=F_LEI),
}

if __name__ == "__main__":
    for peca, html in ABERTURAS.items():
        (AQUI / peca / "abertura.html").write_text(html, encoding="utf-8")
    for peca, telas in TELAS.items():
        d = AQUI / peca
        d.mkdir(parents=True, exist_ok=True)
        for i, html in enumerate(telas, 1):
            (d / f"tela{i}.html").write_text(html, encoding="utf-8")
    print("ok")
