# Mentor — Manual operacional de conteúdo (config/marca)

Resumo do Manual da Marca aplicado às redes sociais. Vale como regra para todas as skills de conteúdo.
Assinatura: **Clareza para decidir.** Mentor é o ERP em nuvem da EGR Systems.

## 1. Conceito e voz
- Transparência e decisão orientada a dados. Tom claro, preciso, seguro e próximo do gestor de PME.
- Nunca frio, burocrático, arrogante ou informal demais.
- **O dado vem antes do adjetivo.** "Receita 18% acima do orçado", não "Ótimo resultado!".
- Frases curtas, verbos de ação. Fale como quem traz o número pronto.
- Proibido: superlativos e promessas vagas ("revolucione", "potencialize", "o melhor"), ponto de exclamação, jargão contábil quando existe palavra simples.
- CTA no tom da marca: "Ver o Mentor com os meus dados", não "Agende já uma demonstração!".

## 2. Todo número tem fonte
- Cada número de cada peça tem fonte verificável com link (pesquisa, órgão, data).
- Na arte: linha "Fonte: <instituição>, <estudo> (<ano>)" no rodapé, em texto de apoio.
- Na legenda: a fonte completa com link.
- Sem fonte, o número não entra. Prefira fontes primárias (Sebrae, IBGE, Banco Central, Receita Federal, FGV).

## 3. Cores (proporção 60% Cloud, 25% Night, 10% Blue, 5% Cyan)
| Token | Hex | Uso |
|---|---|---|
| Electric Blue | #0984E3 | cor da marca; quadrado do símbolo no fundo claro; fundo do modelo educativo |
| Night Black | #1E272E | base escura; texto sobre claro |
| Cyan Neon | #00CEC9 | dado em destaque no fundo escuro (com moderação; nunca texto sobre claro) |
| Cloud White | #F5F6FA | fundo claro; texto sobre escuro |
| Índigo EGR | #272A7C | só peças institucionais e co-branding |
| Apoio sobre Night | #A3AFB8 | texto secundário e fonte |
| Apoio sobre Cloud | #5B6670 | texto secundário e fonte |
- Sem degradê, sem 3D, sem sombra pesada. Linhas finas (1px, 14–18% de opacidade) no lugar de sombras.
- Verde/vermelho só para variação, sempre com sinal (+/−) ou seta.

## 4. Tipografia
- **Saira ExtraBold**: títulos e números-herói. Sempre MAIÚSCULAS, tracking +1%, até 6 palavras.
- **Geist** 400/500/600: texto de apoio. Sem itálico.
- **Geist Mono**: valores, fórmulas e tabelas (algarismos tabulares).
- Arquivos em `marca/fonts/`. CSS base em `marca/base.css`.

## 5. Logo
- Use sempre o arquivo oficial de `marca/logos/`. Nunca redigitar, distorcer, girar, recolorir (exceto a variação abaixo), aplicar sombra ou pôr sobre foto sem faixa sólida.
- Posts: **logo sem endosso** (`mentor-logo-*`) no canto superior esquerdo, altura 52px em 1080px de largura (mínimo 88px de largura total).
- Fundo Cloud → `mentor-logo-claro.svg`. Fundo Night → `mentor-logo-escuro.svg`. Fundo Blue → `mentor-logo-sobre-azul.svg` (versão escura com quadrado em Night, prevista no manual).
- Área de proteção: 1,5× a largura do quadrado de destaque, livre ao redor.
- Peças institucionais/co-branding: assinatura com "by EGR Systems" (`mentor-assinatura-*`).

## 6. Layout dos posts
- Margem externa 88px (em 1080px). Grade de 4px.
- **Um único destaque de cor por peça**: o número-herói, o ponto final ou o quadrado-marcador. O quadrado do logo não conta.
- Título em Saira de 3 a 6 palavras.
- Três modelos-base (1080x1080; para feed vertical, 1080x1350 com o mesmo esquema):
  1. **Dado-herói** (Night): logo → número-herói em Cyan (~360px) → título → apoio (o que o número significa) → rodapé com fonte. Arquivo: `exemplos/dado-heroi.html`.
  2. **Manifesto** (Cloud): logo → frase em Saira grande com ponto final em Blue → apoio → rodapé "ERP em nuvem · by EGR Systems". Arquivo: `exemplos/manifesto.html`.
  3. **Educativo** (Blue): logo sobre azul → rótulo (Geist 600, caixa alta) → título → bloco de fórmula/lista em Geist Mono → apoio com quadrado-marcador Night. Arquivo: `exemplos/educativo.html`.
- Grade de alternância: não repetir o mesmo fundo em dois posts seguidos do mesmo dia.

## 6A. Gráficos animados (prioridade)
Pedido do Eleandro: **abusar de gráficos animados**. O gráfico é o jeito mais claro de mostrar "o dado antes do adjetivo".
- Meta: **pelo menos 1 tela com gráfico animado em cada peça** (carrossel ou reel) sempre que o tema tiver números comparáveis. Sem dado com fonte, sem gráfico.
- Tipos: barras horizontais (comparar categorias; até 6 barras), barras verticais (até 8 períodos), linha (evolução no tempo), número-herói com barra de progresso (parte de um todo). Evite pizza e rosca.
- Animação: barras crescem (`data-growx` / `data-grow`), linhas se desenham (`data-draw`), valores contam (`data-count`). Entradas escalonadas de 0,2 s por barra.
- Destaque único: só a barra/série que conta a história usa a cor de destaque (Cyan sobre Night, Blue sobre Cloud, Night sobre Blue). O resto em cinza (#46535E sobre Night; #C5CBD3 sobre Cloud).
- Escala honesta: barras sempre começam do zero; largura/altura proporcional ao valor; rótulo com o valor exato em Geist Mono; unidade explícita no subtítulo; período no subtítulo.
- Ordem das séries quando houver várias: realizado (azul), projetado (ciano), orçado/meta (laranja #F29F05), período anterior (Night), outros (cinza). Máximo 5 séries.
- Toda tela com gráfico leva a linha "Fonte: ..." no rodapé.
- Modelos: `exemplos/video/tela-grafico-barras.html` (dados reais, Sebrae) e `exemplos/video/tela-grafico-linha.html` (estrutura de referência com dados ILUSTRATIVOS: troque por dados reais antes de usar).

## 7. Formatos e tamanhos
| Rede | Formato | Tamanho |
|---|---|---|
| Instagram feed / carrossel | imagem ou vídeo por tela | 1080x1350 (4:5) ou 1080x1080 |
| Instagram Reels | vídeo vertical | 1080x1920, 9:16 |
| Facebook | vídeo único vertical ou reel | 1080x1920 ou 1080x1350 |
| LinkedIn (página) | vídeo único, imagem ou PDF-carrossel | 1080x1080 ou 1080x1350; PDF até 300 páginas |
- **Carrossel de vídeos (Instagram)**: **slide 1 é sempre uma CAPA ESTÁTICA (PNG 1080x1350)**, fundo Electric Blue, logo sobre azul, rótulo, número-herói (se houver), título em Saira e chamada "Arraste…" com quadrado-marcador Night; gerada com `ferramentas/capa.py`. Os vídeos vêm do slide 2 em diante (2 a 6 vídeos de 4–8s). Motivo: o Instagram usa o primeiro item como capa no perfil e não deixa trocar depois; vídeo começando em fundo liso vira capa preta/vazia. Última tela = assinatura/CTA.
- **Vídeo como primeiro item** (reel, vídeo único no Facebook/LinkedIn): depois do `video.py`, rodar `ferramentas/cortar_inicio.py` para cortar o começo vazio; o primeiro quadro já mostra o conteúdo.
- **Trava de capa**: antes de agendar, `ferramentas/conferir_capa.py` no primeiro item de cada post. Escuro ou vazio → não agenda e avisa o Eleandro.
- **Facebook e LinkedIn** (Buffer aceita 1 vídeo por post): o carrossel vira um vídeo único em que as telas passam em sequência.
- Todo vídeo tem som: trilha instrumental livre de direitos autorais (biblioteca royalty-free ou trilha gerada), volume moderado, sem voz.
- Animações sóbrias: entrada por fade/slide curto (200–400ms), número contando até o valor. Sem efeitos 3D, brilho ou transições chamativas.
- Exportar MP4 H.264 + AAC, 30fps, até 100MB (limite do Instagram no Buffer). Conferir resolução antes de subir.

## 8. Legenda e hashtags
- Primeira linha: o dado ou a ideia central, em até 125 caracteres.
- Corpo: 2 a 4 frases curtas explicando o que fazer com o dado.
- Fonte completa com link.
- CTA no tom da marca.
- Hashtags: Instagram até 5 (limite do Buffer); LinkedIn 3; Facebook 0 a 3. Ex.: #gestaofinanceira #pme #fluxodecaixa #indicadores #erp
- Sem aviso legal fixo (pode ser ativado depois em config/marca).

## 9. Checklist de conferência (toda peça)
- [ ] Primeiro item com conteúdo visível: carrossel abre com capa estática; vídeo único com começo cortado; `conferir_capa.py` aprovado.
- [ ] Título em Saira, maiúsculas, até 6 palavras.
- [ ] Um único destaque de cor.
- [ ] Logo oficial, versão certa para o fundo, canto superior esquerdo, área de proteção livre.
- [ ] Cores só da paleta; sem degradê, 3D ou sombra.
- [ ] Todo número com fonte na arte e link na legenda; número confere com a fonte.
- [ ] Sem superlativo, sem exclamação, dado antes do adjetivo.
- [ ] Tamanho certo para a rede; vídeo com som; arquivo dentro do limite.
- [ ] Texto legível no celular (apoio ≥ 28px em 1080px; contraste ≥ 4,5:1).
- [ ] Pelo menos 1 tela com gráfico animado por peça, quando houver dados comparáveis; escala começando do zero.
- [ ] Revisão ortográfica.
