#!/bin/bash
# Produção dos vídeos da pauta 2026-11-17 v1 (3 jobs em paralelo)
cd "$(dirname "$0")/../../.."
V=pautas/2026-11-17/v1
{
for i in 1 2 3 4; do echo "tela $V/p1/tela$i.html $V/p1/ig_tela$i.mp4 --w 1080 --h 1350 --seg 6 --semente 3211"; done
echo "sequencia $V/p1/facebook.mp4 $V/p1/tela1.html $V/p1/tela2.html $V/p1/tela3.html $V/p1/tela4.html --w 1080 --h 1920 --seg 5 --semente 3211 --abertura 2.9"
for i in 1 2 3 4; do echo "tela $V/p2/tela$i.html $V/p2/ig_tela$i.mp4 --w 1080 --h 1350 --seg 6 --semente 3212"; done
echo "sequencia $V/p2/facebook.mp4 $V/p2/abertura.html $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1920 --seg 5 --semente 3212 --abertura 2.9"
echo "sequencia $V/p2/linkedin.mp4 $V/p2/abertura.html $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1350 --seg 5 --semente 3212"
echo "sequencia $V/p3/reel.mp4 $V/p3/tela1.html $V/p3/tela2.html $V/p3/tela3.html $V/p3/tela4.html --w 1080 --h 1920 --seg 5 --semente 3213 --abertura 2.9"
} | xargs -P 3 -L 1 sh -c 'python3 ferramentas/video.py "$@" 2>&1 | tail -3 | sed "s|^|$1 $2 $3: |"' _
# Abertura curta: corte do começo vazio nos vídeos que vão como primeiro item
for f in $V/p1/facebook.mp4 $V/p2/facebook.mp4 $V/p3/reel.mp4; do
  python3 ferramentas/cortar_inicio.py $f ${f%.mp4}_c.mp4 --max 2.4 && mv ${f%.mp4}_c.mp4 $f
done
python3 ferramentas/cortar_inicio.py $V/p2/linkedin.mp4 $V/p2/linkedin_c.mp4 && mv $V/p2/linkedin_c.mp4 $V/p2/linkedin.mp4
cp $V/p3/reel.mp4 $V/p3/facebook.mp4
echo FIM
# Ajuste p1/facebook: abertura de 4,2 s e corte em 1,6 s, para o 1º quadro já mostrar os valores finais do gráfico (sem número contando)
# python3 ferramentas/video.py sequencia fb1_raw.mp4 $V/p1/tela1.html $V/p1/tela2.html $V/p1/tela3.html $V/p1/tela4.html --w 1080 --h 1920 --seg 5 --semente 3211 --abertura 4.2
# ffmpeg -ss 1.6 -i fb1_raw.mp4 -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -b:a 128k -af "afade=t=in:d=0.3" -movflags +faststart $V/p1/facebook.mp4
# Ajuste p3/tela1: título 136px e apoio 46px para o 1º quadro do reel passar no conferir_capa (reel refeito com o mesmo comando acima)
