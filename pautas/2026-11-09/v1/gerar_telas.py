"""Gera as telas HTML da pauta 2026-11-09 v1 (tema: peso dos custos no lucro da PME, Sebrae RS jul/2026)."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTE = "Fonte: Sebrae RS, Monitoramento dos Pequenos Negócios (jul/2026)"

CSS_COMUM = """
  .fonte-n { color: var(--muted-dark); border-top: 1px solid rgba(245,246,250,.18); padding-top: 22px; }
  .fonte-c { color: var(--muted-light); border-top: 1px solid rgba(30,39,46,.14); padding-top: 22px; }
  .fonte-b { color: #FFFFFF; opacity: .9; border-top: 1px solid rgba(255,255,255,.28); padding-top: 22px; }
  .fonte-n, .fonte-c, .fonte-b { font-size: 24px; }
  .ponto { color: var(--blue); }
  .marcador { display: inline-block; width: 22px; height: 22px; border-radius: 4px; background: var(--night); margin-right: 16px; vertical-align: -2px; }
  .topo { margin-top: 130px; }
  @media (min-height: 1700px) { .topo { margin-top: 330px; } .grafico { margin-top: 96px !important; } }
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


def dado_cloud(numero, count, dec, pre, suf, titulo, apoio, tam=300):
    css = f"""
  .numero {{ font-size: {tam}px; color: var(--night); line-height: 0.86; white-space: nowrap; }}
  .titulo {{ font-size: 84px; margin-top: 52px; max-width: 904px; }}
  .apoio {{ color: var(--muted-light); margin-top: 36px; max-width: 860px; }}"""
    corpo = f"""{logo('cloud')}
  <div class="display numero topo" data-in="0.3" data-count="{count}" data-decimals="{dec}" data-prefix="{pre}" data-suffix="{suf}">{numero}</div>
  <div class="display titulo" data-in="1.3">{titulo}<span class="ponto">.</span></div>
  <p class="apoio" data-in="1.9">{apoio}</p>
  <div class="spacer"></div>
  <p class="fonte-c" data-in="2.5">{FONTE}</p>"""
    return pagina("cloud", corpo, css)


def barras(fundo, titulo, subtitulo, series, dec=0):
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
  .linha {{ display: grid; grid-template-columns: 300px 1fr 110px; align-items: center; gap: 20px; }}
  .rotulo {{ font-size: 28px; color: {crot}; }}
  .trilho {{ height: 44px; position: relative; }}
  .barra {{ position: absolute; inset: 0 auto 0 0; border-radius: 4px; background: {cinza}; min-width: 4px; }}
  .barra.destaque {{ background: {dest}; }}
  .valor {{ font: 500 32px "Geist Mono", monospace; color: {cval}; text-align: right; font-variant-numeric: tabular-nums; }}
  .valor.destaque {{ color: {cdest}; }}"""
    linhas = []
    t = 1.0
    for rot, v, d in series:
        cls = " destaque" if d else ""
        w = round(v / maior * 100, 1)
        txt = (f"{v:.{dec}f}".replace(".", ",")) + "%"
        linhas.append(
            f'    <div class="linha" data-in="{t:.1f}"><span class="rotulo">{rot}</span><div class="trilho">'
            f'<div class="barra{cls}" style="width:{w}%" data-growx="{t + 0.1:.1f}"></div></div>'
            f'<span class="valor{cls}" data-in="{t + 0.1:.1f}" data-count="{v}" data-decimals="{dec}" data-suffix="%">{txt}</span></div>')
        t += 0.2
    corpo = f"""{logo(fundo)}
  <div class="display titulo" data-in="0.3">{titulo}</div>
  <p class="apoio" data-in="0.7">{subtitulo}</p>
  <div class="grafico">
{chr(10).join(linhas)}
  </div>
  <div class="spacer"></div>
  <p class="{cf}" data-in="{t + 0.4:.1f}">{FONTE}</p>"""
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


def educativo_formula():
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; opacity: .9; }
  .titulo { font-size: 104px; margin-top: 20px; }
  .formula { margin-top: 56px; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.28); border-radius: 12px; padding: 30px 34px; font-size: 34px; line-height: 1.6; }
  .formula b { font-weight: 500; }
  .apoio { margin-top: 44px; max-width: 820px; }"""
    corpo = f"""{logo('blue')}
  <div class="rotulo topo" data-in="0.3">Indicador da semana</div>
  <div class="display titulo" data-in="0.6">Peso do<br>custo operacional</div>
  <div class="formula mono" data-in="1.2">Custos operacionais do mês<br>÷ faturamento do mês<br>× 100<br><b>= peso do custo (%)</b></div>
  <p class="apoio" data-in="1.8"><span class="marcador"></span>Mostra quanto de cada R$ 100 vendidos fica com a operação.</p>"""
    return pagina("blue", corpo, css)


def progresso_night():
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
  <div class="display numero topo" data-in="0.3" data-count="43" data-decimals="0" data-suffix="%">43%</div>
  <div class="display titulo" data-in="1.0">Têm só uma noção geral</div>
  <p class="apoio" data-in="1.5">de como os custos afetam o lucro e não acompanham em detalhe.</p>
  <div class="grafico" data-in="1.8">
    <div class="trilho"><div class="barra" style="width:43%" data-growx="1.9"></div></div>
    <div class="legenda"><span class="d">Noção geral: 43%</span><span>100% das respostas</span></div>
  </div>
  <div class="spacer"></div>
  <p class="fonte-n" data-in="2.5">{FONTE}</p>"""
    return pagina("night", corpo, css)


def checklist_cloud():
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--muted-light); }
  .titulo { font-size: 96px; margin-top: 20px; max-width: 904px; }
  .lista { margin-top: 56px; display: flex; flex-direction: column; gap: 28px; }
  .item { display: grid; grid-template-columns: 76px 1fr; gap: 12px; align-items: baseline; border-top: 1px solid rgba(30,39,46,.14); padding-top: 26px; }
  .item .n { font: 500 40px "Geist Mono", monospace; color: var(--muted-light); }
  .item p { font-size: 34px; line-height: 1.35; }
  .item p span { display: block; font-size: 28px; color: var(--muted-light); margin-top: 6px; }"""
    corpo = f"""{logo('cloud')}
  <div class="rotulo topo" data-in="0.3">Como acompanhar</div>
  <div class="display titulo" data-in="0.6">Três passos por mês<span class="ponto">.</span></div>
  <div class="lista">
    <div class="item" data-in="1.2"><span class="n">01</span><p>Separe custos fixos e variáveis<span>aluguel e folha de um lado; insumos e comissões do outro</span></p></div>
    <div class="item" data-in="1.6"><span class="n">02</span><p>Divida pelo faturamento do mês<span>o resultado é o peso do custo em %</span></p></div>
    <div class="item" data-in="2.0"><span class="n">03</span><p>Compare com os meses anteriores<span>a tendência diz mais que um mês isolado</span></p></div>
  </div>"""
    return pagina("cloud", corpo, css)


def pergunta_night():
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--muted-dark); }
  .titulo { font-size: 104px; margin-top: 20px; max-width: 904px; }
  .titulo .q { color: var(--cyan); }
  .lista { margin-top: 56px; display: flex; flex-direction: column; gap: 0; }
  .op { display: grid; grid-template-columns: 76px 1fr; align-items: baseline; border-top: 1px solid rgba(245,246,250,.18); padding: 24px 0; }
  .op .n { font: 500 36px "Geist Mono", monospace; color: var(--muted-dark); }
  .op span.t { font: 500 40px "Geist Mono", monospace; color: var(--cloud); }
  .apoio { color: var(--muted-dark); margin-top: 36px; max-width: 860px; }"""
    ops = ["Menos de 30%", "Entre 30% e 50%", "Entre 51% e 70%", "Acima de 70%"]
    itens = "\n".join(f'    <div class="op" data-in="{1.0 + 0.3 * i:.1f}"><span class="n">{chr(65 + i)}</span><span class="t">{o}</span></div>' for i, o in enumerate(ops))
    corpo = f"""{logo('night')}
  <div class="rotulo topo" data-in="0.3">Custo operacional ÷ faturamento</div>
  <div class="display titulo" data-in="0.6">Em qual faixa você está<span class="q">?</span></div>
  <div class="lista">
{itens}
  </div>
  <p class="apoio" data-in="2.3">Responda nos comentários com a letra.</p>"""
    return pagina("night", corpo, css)


TELAS = {
    "p1": [
        dado_night("41%", 41, 0, "Sabem o peso de cada custo",
                   "dos pequenos negócios pesquisados dizem saber como cada custo afeta o lucro.", suf="%"),
        barras("night", "A maioria acompanha por alto",
               "Acompanhamento do impacto dos custos no lucro, % das respostas, jul/2026",
               [("Sabe em detalhe", 41, False), ("Noção geral", 43, True), ("Sem controle", 10, False), ("Não acompanha", 6, False)]),
        dado_cloud("38%", 38, 0, "", "%", "Controle financeiro é desafio",
                   "dos empresários citam o controle financeiro do negócio entre os principais desafios do momento."),
        assinatura_blue("Custo de cada produto e de cada área ao lado do faturamento.", "Ver o Mentor com os meus dados"),
    ],
    "p2": [
        dado_cloud("39%", 39, 0, "", "%", "Gastam de 30% a 50%",
                   "do faturamento mensal com custos operacionais: é a faixa mais citada pelos pequenos negócios pesquisados."),
        barras("cloud", "Onde está o seu custo",
               "Custos operacionais em % do faturamento mensal, % das empresas, jul/2026",
               [("Menos de 30%", 22, False), ("30% a 50%", 39, True), ("51% a 70%", 25, False), ("Acima de 70%", 8, False), ("Não sabe", 6, False)]),
        dado_night("6%", 6, 0, "Não sabem o próprio percentual",
                   "não souberam informar quanto os custos operacionais levam do faturamento mensal.", suf="%"),
        assinatura_blue("O peso de cada custo no faturamento, atualizado todo mês.", "Ver o Mentor com os meus dados"),
    ],
    "p3": [
        educativo_formula(),
        progresso_night(),
        checklist_cloud(),
        pergunta_night(),
        assinatura_blue("Custos e faturamento no mesmo lugar, com o percentual calculado.", "Ver o Mentor com os meus dados"),
    ],
}

if __name__ == "__main__":
    for peca, telas in TELAS.items():
        d = AQUI / peca
        d.mkdir(parents=True, exist_ok=True)
        for i, html in enumerate(telas, 1):
            (d / f"tela{i}.html").write_text(html, encoding="utf-8")
    print("ok")
