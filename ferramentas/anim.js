// Animação determinística quadro a quadro para peças Mentor.
// Marque elementos com:
//   data-in="0.3"        segundo em que o elemento entra (fade + subida curta de 24px, 350ms)
//   data-from="left"     opcional: entra deslizando da esquerda em vez de subir
//   data-count="22"      opcional: número que conta de 0 até o valor (dura 0,9s a partir de data-in)
//   data-decimals="1" data-prefix="R$ " data-suffix="%"   formatação do contador (pt-BR)
//   data-out="5.6"       opcional: segundo em que o elemento sai (fade 300ms)
// Gráficos:
//   data-grow="0.8"      barra vertical cresce de baixo para cima a partir desse segundo (0,9s)
//   data-growx="0.8"     barra horizontal cresce da esquerda para a direita (0,9s)
//   data-draw="0.8"      <path>/<polyline> SVG se desenha a partir desse segundo (1,4s)
//   data-dur="1.2"       opcional: muda a duração de grow/growx/draw
// O renderizador chama window.frame(t) para cada quadro.
(function () {
  const ease = (x) => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
  const fmt = (v, d) => v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });
  window.frame = function (t) {
    document.querySelectorAll("[data-grow],[data-growx]").forEach((el) => {
      const vert = el.hasAttribute("data-grow");
      const t0 = parseFloat(vert ? el.dataset.grow : el.dataset.growx);
      const q = ease((t - t0) / parseFloat(el.dataset.dur || "0.9"));
      el.style.transformOrigin = vert ? "50% 100%" : "0% 50%";
      el.style.transform = vert ? `scaleY(${q})` : `scaleX(${q})`;
    });
    document.querySelectorAll("[data-draw]").forEach((el) => {
      const len = el.getTotalLength ? el.getTotalLength() : 1000;
      const q = ease((t - parseFloat(el.dataset.draw)) / parseFloat(el.dataset.dur || "1.4"));
      el.style.strokeDasharray = `${len}`;
      el.style.strokeDashoffset = `${len * (1 - q)}`;
    });
    document.querySelectorAll("[data-in]").forEach((el) => {
      const t0 = parseFloat(el.dataset.in);
      const p = ease((t - t0) / 0.35);
      let o = p;
      if (el.dataset.out) o *= 1 - ease((t - parseFloat(el.dataset.out)) / 0.3);
      el.style.opacity = o;
      const d = (1 - p) * 24;
      el.style.transform = el.dataset.from === "left" ? `translateX(${-d * 2}px)` : `translateY(${d}px)`;
      if (el.dataset.count) {
        const alvo = parseFloat(el.dataset.count);
        const dec = parseInt(el.dataset.decimals || "0", 10);
        const q = ease((t - t0) / 0.9);
        el.textContent = (el.dataset.prefix || "") + fmt(alvo * q, dec) + (el.dataset.suffix || "");
      }
    });
  };
  window.frame(0);
})();
