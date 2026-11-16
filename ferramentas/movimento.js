// Motor de movimento dos reels Mentor (determinístico, quadro a quadro).
// Um HTML = o vídeo inteiro, dividido em cenas. O renderizador (ferramentas/reel.py)
// chama window.frame(t) para cada quadro e lê window.EVENTOS() para os efeitos sonoros.
//
// CENAS
//   <section class="cena" data-dur="2.4" data-trans="empurra">...</section>
//   data-dur     duração da cena em segundos (a transição de 0,45 s acontece no fim dela)
//   data-trans   como ESTA cena entra: empurra | sobe | zoom | mascara | corte (padrão: empurra)
//   data-camera  movimento contínuo da cena: aproxima | afasta | desliza | nenhum (padrão: aproxima)
//   A primeira cena já está na tela no quadro 0 (nada de abrir com tela vazia).
//
// ELEMENTOS (tempos relativos ao início da cena)
//   data-in="0.3"          entra com mola (sobe 40px, escala 0.92→1, desfoque 10→0)
//   data-from="left|right|down|zoom"   direção da entrada
//   data-palavras          tipografia cinética: as palavras entram uma a uma (ritmo de leitura)
//   data-ritmo="0.11"      segundos entre palavras (padrão 0.11)
//   data-count="22" data-decimals="1" data-prefix="R$ " data-suffix="%"  contador (pt-BR)
//   data-growx / data-grow="0.8"   barra cresce na horizontal / vertical (com leve passada e volta)
//   data-draw="0.8"        <path>/<polyline> SVG se desenha
//   data-dur="1.2"         duração de grow/draw/count
//   data-pulsa="1.6"       pulso de destaque (escala 1→1.08→1) nesse segundo
//   data-flutua            deriva lenta contínua (elementos decorativos / prints)
//   data-esvazia="0.8" data-ate="0.2"  barra que esvazia até a fração indicada (estoque/caixa acabando)
//   data-desce="0.5"       valor que despenca: translada para baixo e some (ex.: caixa zerando)
//   data-som="pop|tick|whoosh|impacto"  força um efeito sonoro na entrada do elemento
(function () {
  const TRANS = 0.45;
  const clamp = (x) => Math.min(Math.max(x, 0), 1);
  const easeOut = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const easeInOut = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  // mola amortecida: passa um pouco do alvo e volta (0→1)
  const mola = (x) => { if (x <= 0) return 0; if (x >= 1.6) return 1; return 1 - Math.exp(-6 * x) * Math.cos(9 * x); };
  const fmt = (v, d) => v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });

  const cenas = Array.from(document.querySelectorAll(".cena"));
  let acc = 0;
  const tempos = cenas.map((c) => { const ini = acc; const dur = parseFloat(c.dataset.dur || "2.5"); acc += dur; return { ini, dur }; });
  window.DURACAO = acc;

  // quebra textos com data-palavras em spans
  document.querySelectorAll("[data-palavras]").forEach((el) => {
    if (el.dataset.quebrado) return;
    const partes = el.innerHTML.split(/(\s+|<br\s*\/?>)/);
    el.innerHTML = partes.map((p) => (/^\s+$/.test(p) || /^<br/i.test(p) || !p ? p : `<span class="pal" style="display:inline-block">${p}</span>`)).join("");
    el.dataset.quebrado = "1";
  });

  function cenaDe(el) { const c = el.closest(".cena"); const i = cenas.indexOf(c); return i < 0 ? { ini: 0, dur: acc } : tempos[i]; }

  function entrada(el, p, de) {
    const m = mola(p * 1.25);
    const o = easeOut(p * 2.2);
    const blur = (1 - easeOut(p * 1.8)) * 10;
    let tf = "";
    const d = 1 - m;
    if (de === "left") tf = `translateX(${-90 * d}px)`;
    else if (de === "right") tf = `translateX(${90 * d}px)`;
    else if (de === "zoom") tf = `scale(${0.6 + 0.4 * m})`;
    else if (de === "down") tf = `translateY(${-50 * d}px)`;
    else tf = `translateY(${40 * d}px) scale(${0.92 + 0.08 * m})`;
    el.style.opacity = o;
    el.style.filter = blur > 0.2 ? `blur(${blur.toFixed(2)}px)` : "none";
    return tf;
  }

  window.frame = function (t) {
    // cenas: visibilidade, transição e câmera
    cenas.forEach((c, i) => {
      const { ini, dur } = tempos[i];
      const fim = ini + dur;
      const proxima = cenas[i + 1];
      const entraIni = i === 0 ? -1 : ini - TRANS;
      const visivel = t >= entraIni && t < fim + (proxima ? 0 : 1);
      c.style.visibility = visivel ? "visible" : "hidden";
      if (!visivel) return;
      let tf = "", op = 1, clip = "none";
      // entrada desta cena
      if (i > 0 && t < ini) {
        const q = easeInOut((t - entraIni) / TRANS);
        const modo = c.dataset.trans || "empurra";
        if (modo === "empurra") tf = `translateX(${(1 - q) * 100}%)`;
        else if (modo === "sobe") tf = `translateY(${(1 - q) * 100}%)`;
        else if (modo === "zoom") { tf = `scale(${0.82 + 0.18 * q})`; op = q; }
        else if (modo === "mascara") clip = `circle(${q * 150}% at 50% 55%)`;
        else if (modo === "corte") op = q > 0.5 ? 1 : 0;
      }
      // saída desta cena (quando a próxima entra)
      if (proxima && t >= fim - TRANS) {
        const q = easeInOut((t - (fim - TRANS)) / TRANS);
        const modo = proxima.dataset.trans || "empurra";
        if (modo === "empurra") tf = `translateX(${-q * 35}%)`;
        else if (modo === "sobe") tf = `translateY(${-q * 30}%)`;
        else if (modo === "zoom") { tf = `scale(${1 + 0.35 * q})`; op = 1 - q; }
        else if (modo === "mascara") tf = `scale(${1 + 0.05 * q})`;
        else if (modo === "corte") op = q > 0.5 ? 0 : 1;
      }
      c.style.transform = tf; c.style.opacity = op; c.style.clipPath = clip;
      c.style.zIndex = String(10 + i);
      // câmera contínua no conteúdo da cena
      const cam = c.querySelector(":scope > .camera");
      if (cam) {
        const u = clamp((t - entraIni) / (dur + TRANS));
        const modo = c.dataset.camera || "aproxima";
        let ct = "";
        if (modo === "aproxima") ct = `scale(${1 + 0.05 * u})`;
        else if (modo === "afasta") ct = `scale(${1.06 - 0.06 * u})`;
        else if (modo === "desliza") ct = `translateX(${-24 * u}px) scale(1.03)`;
        cam.style.transformOrigin = "50% 45%";
        cam.style.transform = ct;
      }
    });

    document.querySelectorAll("[data-in]").forEach((el) => {
      const { ini } = cenaDe(el);
      const t0 = ini + parseFloat(el.dataset.in);
      const p = (t - t0) / 0.55;
      if (el.hasAttribute("data-palavras")) {
        el.style.opacity = 1;
        const ritmo = parseFloat(el.dataset.ritmo || "0.11");
        el.querySelectorAll(".pal").forEach((s, k) => {
          const pk = (t - t0 - k * ritmo) / 0.45;
          const tf = entrada(s, pk, el.dataset.from);
          s.style.transform = tf;
        });
        return;
      }
      let tf = entrada(el, p, el.dataset.from);
      if (el.dataset.pulsa) {
        const tp = ini + parseFloat(el.dataset.pulsa);
        const x = (t - tp) / 0.5;
        if (x > 0 && x < 1) tf += ` scale(${1 + 0.08 * Math.sin(Math.PI * x)})`;
      }
      if (el.dataset.desce) {
        const td = ini + parseFloat(el.dataset.desce);
        const x = easeInOut((t - td) / 0.8);
        if (x > 0) { tf += ` translateY(${x * 220}px)`; el.style.opacity = String(Math.max(0, 1 - x)); }
      }
      el.style.transform = tf;
      if (el.dataset.count) {
        const alvo = parseFloat(el.dataset.count);
        const dec = parseInt(el.dataset.decimals || "0", 10);
        const q = easeOut((t - t0) / parseFloat(el.dataset.dur || "0.9"));
        el.textContent = (el.dataset.prefix || "") + fmt(alvo * q, dec) + (el.dataset.suffix || "");
      }
    });

    document.querySelectorAll("[data-grow],[data-growx]").forEach((el) => {
      const { ini } = cenaDe(el);
      const vert = el.hasAttribute("data-grow");
      const t0 = ini + parseFloat(vert ? el.dataset.grow : el.dataset.growx);
      const x = (t - t0) / parseFloat(el.dataset.dur || "0.9");
      const q = x <= 0 ? 0 : Math.min(mola(x * 1.2), 1.04);
      el.style.transformOrigin = vert ? "50% 100%" : "0% 50%";
      el.style.transform = vert ? `scaleY(${q})` : `scaleX(${q})`;
    });

    document.querySelectorAll("[data-esvazia]").forEach((el) => {
      const { ini } = cenaDe(el);
      const q = easeInOut((t - ini - parseFloat(el.dataset.esvazia)) / parseFloat(el.dataset.dur || "1.4"));
      const alvo = parseFloat(el.dataset.ate || "0");
      el.style.transformOrigin = "0% 50%";
      el.style.transform = `scaleX(${1 - (1 - alvo) * q})`;
    });

    document.querySelectorAll("[data-draw]").forEach((el) => {
      const { ini } = cenaDe(el);
      const len = el.getTotalLength ? el.getTotalLength() : 1000;
      const q = easeInOut((t - ini - parseFloat(el.dataset.draw)) / parseFloat(el.dataset.dur || "1.2"));
      el.style.strokeDasharray = `${len}`;
      el.style.strokeDashoffset = `${len * (1 - q)}`;
    });

    document.querySelectorAll("[data-flutua]").forEach((el, k) => {
      const a = t * 0.9 + k * 1.7;
      const base = el.dataset.flutuaBase || (el.dataset.flutuaBase = el.style.transform || "");
      el.style.transform = `${base} translate(${Math.sin(a) * 10}px, ${Math.cos(a * 0.8) * 14}px) rotate(${Math.sin(a * 0.6) * 1.5}deg)`;
    });
  };

  // efeitos sonoros: whoosh nas transições, pop nas entradas, tick nos contadores
  window.EVENTOS = function () {
    const ev = [];
    cenas.forEach((c, i) => {
      if (i > 0) ev.push({ t: Math.max(0, tempos[i].ini - TRANS), tipo: (c.dataset.trans || "empurra") === "mascara" ? "impacto" : "whoosh" });
    });
    document.querySelectorAll("[data-in]").forEach((el) => {
      const { ini } = cenaDe(el);
      const t0 = ini + parseFloat(el.dataset.in);
      if (t0 < 0) return;
      const tipo = el.dataset.som || (el.dataset.count ? "tick" : el.classList.contains("display") || el.hasAttribute("data-palavras") ? "pop" : "");
      if (tipo) ev.push({ t: t0, tipo });
    });
    document.querySelectorAll("[data-growx],[data-grow]").forEach((el) => {
      const { ini } = cenaDe(el);
      ev.push({ t: ini + parseFloat(el.dataset.growx || el.dataset.grow), tipo: "sobe" });
    });
    document.querySelectorAll("[data-pulsa]").forEach((el) => { const { ini } = cenaDe(el); ev.push({ t: ini + parseFloat(el.dataset.pulsa), tipo: "impacto" }); });
    document.querySelectorAll("[data-esvazia]").forEach((el) => { const { ini } = cenaDe(el); ev.push({ t: ini + parseFloat(el.dataset.esvazia), tipo: "cai" }); });
    document.querySelectorAll("[data-desce]").forEach((el) => { const { ini } = cenaDe(el); ev.push({ t: ini + parseFloat(el.dataset.desce), tipo: "cai" }); });
    return ev.sort((a, b) => a.t - b.t);
  };

  window.frame(0);
})();
