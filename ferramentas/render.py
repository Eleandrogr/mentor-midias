"""Renderiza peças da marca Mentor (HTML -> PNG) com Chrome headless.

Uso:
  python3 ferramentas/render.py entrada.html saida.png [largura] [altura]

O HTML deve usar os caminhos relativos ../marca/fonts e ../marca/logos
ou caminhos absolutos file://. Este script injeta <base> apontando para a raiz do repo.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent


def render(html_path: str, out_path: str, w: int = 1080, h: int = 1080) -> None:
    html = Path(html_path).read_text(encoding="utf-8")
    if "<base" not in html:
        html = html.replace("<head>", f'<head><base href="file://{RAIZ}/">', 1)
    tmp = RAIZ / ".render-tmp.html"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(f"file://{tmp}", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(200)
        pg.screenshot(path=out_path, clip={"x": 0, "y": 0, "width": w, "height": h})
        b.close()
    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    a = sys.argv
    render(a[1], a[2], int(a[3]) if len(a) > 3 else 1080, int(a[4]) if len(a) > 4 else 1080)
