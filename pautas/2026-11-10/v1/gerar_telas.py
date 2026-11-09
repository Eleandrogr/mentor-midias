"""Gera as telas HTML da pauta 2026-11-10 v1 (tema: conta pessoal pagando despesas da empresa, Sebrae 2025)."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTE = "Fonte: Sebrae, Hábitos Financeiros dos Pequenos Negócios (2025)"

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


def barras(fundo, titulo, subtitulo, series, dec=0, col=300):
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


def gancho_blue():
    css = """
  .rotulo { font-size: 26px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; opacity: .9; }
  .titulo { font-size: 124px; margin-top: 24px; max-width: 904px; }
  .apoio { margin-top: 48px; max-width: 820px; font-size: 36px; }"""
    corpo = f"""{logo('blue')}
  <div class="rotulo topo" data-in="0.3">Gestão financeira</div>
  <div class="display titulo" data-in="0.6">Sua conta paga a empresa?</div>
  <p class="apoio" data-in="1.4"><span class="marcador"></span>Pix do fornecedor, boleto do aluguel, compra de insumo: tudo sai da conta pessoal.</p>"""
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
  <div class="display numero topo" data-in="0.3" data-count="61" data-decimals="0" data-suffix="%">61%</div>
  <div class="display titulo" data-in="1.0">Fazem isso hoje</div>
  <p class="apoio" data-in="1.5">dos pequenos negócios pagam despesas da empresa com a conta pessoal.</p>
  <div class="grafico" data-in="1.8">
    <div class="trilho"><div class="barra" style="width:61%" data-growx="1.9"></div></div>
    <div class="legenda"><span class="d">Conta pessoal: 61%</span><span>100% dos negócios</span></div>
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
  <div class="rotulo topo" data-in="0.3">Como separar</div>
  <div class="display titulo" data-in="0.6">Três passos para separar<span class="ponto">.</span></div>
  <div class="lista">
    <div class="item" data-in="1.2"><span class="n">01</span><p>Abra uma conta só da empresa<span>toda venda entra nela; toda despesa do negócio sai dela</span></p></div>
    <div class="item" data-in="1.6"><span class="n">02</span><p>Defina um pró-labore fixo<span>o seu salário sai da empresa uma vez por mês, no mesmo valor</span></p></div>
    <div class="item" data-in="2.0"><span class="n">03</span><p>Registre toda retirada extra<span>com data, valor e motivo, para o caixa fechar no fim do mês</span></p></div>
  </div>"""
    return pagina("cloud", corpo, css)


CTA = "Ver o Mentor com os meus dados"

TELAS = {
    "p1": [
        dado_night("61%", 61, 0, "Conta pessoal paga a empresa",
                   "dos pequenos negócios pagam despesas da empresa com a conta pessoal do dono.", suf="%"),
        barras("night", "Construção e indústria lideram",
               "Pagam despesas da empresa com a conta pessoal, % por setor, 2025",
               [("Construção/indústria", 64, True), ("Serviços", 62, False), ("Comércio", 57, False)], col=330),
        barras("cloud", "Hábito quase não mudou",
               "Pagam despesas da empresa com a conta pessoal, % dos negócios",
               [("2023", 60, False), ("2025", 61, True)], col=200),
        assinatura_blue("Caixa da empresa separado, com cada entrada e saída registrada.", CTA),
    ],
    "p2": [
        dado_cloud("20%", 20, 0, "", "%", "Controlam com sistema",
                   "dos pequenos negócios usam aplicativo ou sistema digital no controle financeiro."),
        barras("cloud", "Planilha e caderno na frente",
               "Como os pequenos negócios fazem o controle financeiro, % das respostas, 2025",
               [("Planilha", 30, False), ("Caderno", 25, False), ("App ou sistema", 20, True), ("Contador", 13, False),
                ("Sem controle", 10, False), ("Não sabe", 3, False)], col=280),
        dado_night("10%", 10, 0, "Não fazem controle financeiro",
                   "dos pequenos negócios disseram não ter nenhum controle das finanças.", suf="%"),
        assinatura_blue("Contas a pagar, a receber e caixa no mesmo sistema, em nuvem.", CTA),
    ],
    "p3": [
        gancho_blue(),
        progresso_night(),
        checklist_cloud(),
        assinatura_blue("Conta da empresa conciliada, com pró-labore e retiradas à vista.", CTA),
    ],
}

if __name__ == "__main__":
    for peca, telas in TELAS.items():
        d = AQUI / peca
        d.mkdir(parents=True, exist_ok=True)
        for i, html in enumerate(telas, 1):
            (d / f"tela{i}.html").write_text(html, encoding="utf-8")
    print("ok")
