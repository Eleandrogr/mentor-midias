# Mentor — Manual operacional de conteúdo (config/marca) — v2, nov/2026 (volume v3: 3 peças/dia desde 16/11)

Vale como regra para todas as skills de conteúdo. Substitui a v1 (molde azul com número gigante).
Assinatura: **Clareza para decidir.** Mentor é o ERP em nuvem da EGR Systems. Instagram: @sistemamentor.

## 0. Diagnóstico que motivou a v2 (perfil em 15/11/2026)
- 420 posts, 385 seguidores. Posts automáticos recentes: 8 a 110 visualizações.
- Vídeos com gente real rendem até 7x mais (melhor post: 768 views, usuário de capacete no almoxarifado usando o sistema).
- O que funciona: **gente real e o produto em uso**. Estatística genérica em tela azul não funciona.
- Erros visuais a não repetir: tudo no mesmo molde azul, número gigante na capa, metade de baixo vazia, texto pequeno, logo minúsculo, sem gráfico, primeiro quadro vazio, cor avulsa.

## 1. Público, objetivo e voz
- **Público:** dono ou gestor de pequena e média empresa (indústria, comércio, clínica, serviços) que controla estoque, vendas, financeiro, pessoas e contratos em planilha, caderno ou sistemas soltos.
- **Um objetivo por post:** alcance, salvamento ou lead (pedido de demonstração).
- **Voz:** a do Eleandro, em 1ª pessoa, consultor que já sentou com muito empresário ("já vi empresa...", "o que eu faria"). Direto, prático, sem jargão de TI.
- **Nunca inventar** história, cliente, resultado ou número na voz dele. Toda frase de experiência ("já vi", "um cliente meu", "paguei...") vai para a lista `CONFIRME:` da pauta, para ele validar antes de aprovar.
- Continua proibido: superlativo, promessa vaga ("revolucione", "potencialize"), ponto de exclamação.

## 2. Temas: os 5 módulos do Mentor
- Rodízio por **Estoque, Vendas, Financeiro, Pessoas, Contratos** (os mesmos dos destaques). Nunca o mesmo módulo em dois dias seguidos.
- Cada post mostra **o Mentor resolvendo o problema** (tela, relatório, alerta). Prints oficiais em `marca/telas-site/` (do site mentor.egrsystems.com.br) e gravações enviadas pelo Eleandro em `marca/telas/`. Sem print disponível, a pauta avisa e pede.
- **Brief de 5 campos** obrigatório por post: ângulo (dor, bastidor, prova ou educativo), tema, cliente ideal (quem é o dono e em que situação está), objetivo, CTA.
- **Teste do envio:** "para quem o dono mandaria isto e por quê?" (sócio, contador, gerente). Sem resposta concreta, troca o post.

## 3. Texto
- **Gancho** = situação, tensão ou pergunta do dia a dia do dono, em 1ª pessoa. **Número não abre o post nem a capa**: o dado entra no slide 2 ou até 3 s no vídeo, com fonte.
- **Dado nunca vem sozinho**: todo dado leva uma linha "Na prática" com uma ação para esta semana. Todo post termina com passo a passo, conta pronta ou checklist.
- Frases de até 10 palavras; no máximo 25 palavras por slide/cena. Alterne frases soltas com parágrafos de 2–3 linhas.
- **CTA de palavra-chave que entrega algo ligado ao problema**: "Comente ESTOQUE que te mando a planilha de inventário", "Mande DEMO na DM". Nunca "siga o perfil" ou "conheça o Mentor". O material prometido fica pronto em `materiais/` antes de o post ir ao ar.
- Legenda: 1ª linha = o gancho (até 125 caracteres); corpo curto com o dado, a fonte com link e a ação; CTA de palavra-chave. Hashtags: Instagram até 5, LinkedIn 3, Facebook 0–3.

## 4. Todo número tem fonte
- Conferido na fonte original (Sebrae, IBGE, Banco Central, Cetic.br, FGV, Receita). Registrar valor, rótulo, fonte, ano, link e trecho que confirma. Nunca de memória. Sem fonte, troca o dado.
- Na arte: "Fonte: <instituição>, <estudo> (<ano>)" (mín. 24px). Na legenda: fonte com link.
- Valores de exemplo sempre marcados como exemplo.

## 5. Cores e grid
| Token | Hex | Uso |
|---|---|---|
| Electric Blue | #0984E3 | cor da marca; fundo azul; destaque sobre claro |
| Night Black | #1E272E | fundo escuro; texto sobre claro; destaque sobre azul |
| Cloud White | #F5F6FA | fundo claro; texto sobre escuro |
| Cyan Neon | #00CEC9 | **só** como destaque sobre fundo escuro (nunca fundo, nunca sobre claro) |
| Apoio sobre Night / Cloud | #A3AFB8 / #5B6670 | texto secundário e fonte |
- **Um destaque de cor por peça**: Cyan no escuro, Blue no claro, Night no azul. Nada de cor avulsa. Verde/vermelho só para variação com sinal.
- **Grid**: o fundo da capa/1º quadro alterna em sequência entre posts: azul → branco → escuro → azul… (nunca dois seguidos iguais; capa nunca "sempre azul").
- **Formato também varia**: todo dia tem story, carrossel e reel (item 12); dentro de cada formato, varie o tipo (gente real, tela do sistema, gráfico, frase). As 3 peças do dia não repetem o mesmo fundo no 1º quadro.

## 6. Tipografia e legibilidade (1080px de largura)
- Saira ExtraBold (títulos, maiúsculas), Geist (texto), Geist Mono (valores). Arquivos em `marca/fonts/`.
- **Mínimos:** título 90px, apoio 36px, linha de fonte 24px.
- **Logo** oficial (`marca/logos/mentor-logo-*`) em toda peça: no mínimo 48px de altura no cabeçalho e maior no slide final. Claro → `-claro`; escuro → `-escuro`; azul → `-sobre-azul`.
- O conteúdo ocupa a peça inteira. Proibido deixar metade do quadro vazia.

## 7. Capa (carrossel)
- `ferramentas/capa.py`: situação ou pergunta em 1ª pessoa + **prévia** do gráfico ou da tela do sistema. Fundo pela alternância do grid.
- **Número gigante sozinho na capa é proibido** (o capa.py recusa).
- O grid corta para 3:4: título no miolo, nunca colado no topo nem nas laterais.

## 8. Gráficos
- Todo post de dado tem gráfico: barras, comparação lado a lado, linha do caixa caindo, antes × depois.
- Sem eixos nem grade: rótulo no próprio dado. Barras do zero, proporcionais. Destaque só na série que conta a história.

## 9. Carrossel
1. A capa para o scroll (imagem estática).
2. O slide 2 prova que valeu arrastar: dado mais forte + fonte (vídeo curto animado).
3. Uma ideia por slide; cada slide faz sentido sozinho.
4. Pelo menos um slide que vale salvar (checklist, conta pronta, modelo).
5. Último slide = CTA de palavra-chave.
Slides animados com `ferramentas/reel.py --h 1350` (uma cena por arquivo); slides estáticos com `ferramentas/render.py`.

## 10. Vídeo e reels (nada fica parado)
- Motor: `ferramentas/movimento.js` + `ferramentas/reel.py` (um HTML com cenas → MP4). Modelo: `pautas/2026-11-17/v2/p1/reel.html`.
- **Ação e som desde o quadro 0**: a 1ª cena já começa visível, com palavras entrando. Proibido fade a partir de tela vazia.
- **Transições com movimento** entre cenas (empurra, sobe, zoom, máscara) e **câmera sempre em movimento** (aproxima, afasta, desliza).
- Mudança visual a cada 1–1,5 s; **tipografia cinética** (`data-palavras`): palavras entram uma a uma, no ritmo da leitura.
- O gráfico age: barra cresce com mola, caixa esvazia (`data-esvazia`), valor despenca (`data-desce`), destaque pulsa (`data-pulsa`).
- **Desfoque de movimento** (renderiza a 60 fps e funde em 30 fps) para ficar fluido.
- **Teste da pausa**: o reel.py reprova se a tela ficar igual por mais de 1,5 s.
- **Áudio**: trilha com ritmo + efeitos sonoros sincronizados (whoosh nas transições, pop nas palavras, tick nos contadores, impacto nos destaques), tudo sintetizado e livre de direitos (`ferramentas/sfx.py`).
- **Área segura 9:16**: conteúdo entre 250px do topo e 450px da base (a legenda do Reels cobre essa faixa), 150px à direita, 60px à esquerda (usamos 88). O reel.py confere cada cena.
- Facebook: o mesmo HTML em 1080x1920. LinkedIn: o mesmo HTML em 1080x1350 quando couber.

## 11. Gente real (prioridade)
- Toda segunda-feira, pedir ao Eleandro 2 vídeos de celular (15–40 s): situação de cliente, dúvida que ouviu ou ele mostrando uma tela. Junto, o roteiro de 3 linhas de cada um.
- Edição: cortar silêncios, legenda grande palavra por palavra, zoom nos momentos-chave, gancho nos primeiros 2 s.
- Vídeos de clientes usando o sistema só com autorização do cliente.

## 11A. Story
- 1080x1920, imagem PNG (`render.py`) ou vídeo de 5 a 15 s (`reel.py`). O story não mostra legenda: **todo o texto vai desenhado na arte**.
- Área segura: 250px no topo (barra de progresso e nome do perfil), 340px no rodapé (campo de resposta), 88px nas laterais.
- Papel do story: conversa rápida com o dono. Ângulos: pergunta do dia ("Você já sabe quanto pode retirar este mês?"), bastidor, mini-dica de 1 passo, chamada para o post do dia, prova com tela do Mentor.
- Até 3 blocos de texto, título ≥ 90px. Mesmo destaque único de cor e logo ≥ 48px. Fundo também segue a alternância do grid.
- CTA: "Responda este story com ESTOQUE", "Mande DEMO na DM". Link sticker só quando houver URL (campo `link`).
- Número em story também leva a linha de fonte na arte (≥ 24px).
- Facebook recebe a mesma arte como story. LinkedIn não recebe story.

## 12. Volume (v3, 16/11/2026)
- **3 peças por dia, sempre 1 story, 1 carrossel e 1 reel** (pedido do Eleandro). Horários padrão: story 08:40, carrossel 12:15, reel 18:30 no Instagram; Facebook 5 a 15 min depois (story como story, carrossel e reel como vídeo vertical); LinkedIn 1 por dia às 12:45 (versão 1080x1350 do carrossel, ou do reel se fizer mais sentido).
- As 3 peças do dia têm temas diferentes e podem ser de módulos diferentes; o carrossel e o reel do dia nunca repetem o módulo do carrossel e do reel do dia anterior.
- Os 2 vídeos de gente real da semana entram no lugar do reel do dia em que chegarem.
- **Limite do Buffer (10 posts agendados por canal):** agendar só até o dia seguinte. Fila máxima: Instagram 6, Facebook 6, LinkedIn 2. Antes de criar, contar os agendados do canal; se passar de 10, parar e avisar.
- Qualidade continua acima de volume: se uma peça não passar no item 13, ela não vai ao ar e as outras seguem.

## 13. Checagens antes de publicar (se falhar, não publica)
- [ ] Primeiro quadro de todo vídeo preenchido (`conferir_capa.py`), sem quadro branco ou preto.
- [ ] Capa legível no recorte 3:4 do grid.
- [ ] Logo visível (≥ 48px).
- [ ] Todo número com fonte na arte e link na legenda.
- [ ] Áudio no arquivo.
- [ ] Fundo seguindo a alternância do grid.
- [ ] CTA de palavra-chave presente e material pronto em `materiais/`.
- [ ] Lista `CONFIRME:` aprovada pelo Eleandro.
- [ ] Nada vai ao ar sem o ok do Eleandro. A pauta traz tema, teste do dia, dados com links e a lista `CONFIRME:`.
