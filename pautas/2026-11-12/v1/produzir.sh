#!/bin/bash
# Produção dos vídeos da pauta 2026-11-12 v1 (3 jobs em paralelo)
cd "$(dirname "$0")/../../.."
V=pautas/2026-11-12/v1
{
for i in 1 2 3; do echo "tela $V/p1/tela$i.html $V/p1/ig_tela$i.mp4 --w 1080 --h 1350 --seg 6 --semente 3161"; done
echo "sequencia $V/p1/facebook.mp4 $V/p1/tela1.html $V/p1/tela2.html $V/p1/tela3.html --w 1080 --h 1920 --seg 5 --semente 3161 --abertura 2.9"
for i in 1 2 3 4; do echo "tela $V/p2/tela$i.html $V/p2/ig_tela$i.mp4 --w 1080 --h 1350 --seg 6 --semente 3162"; done
echo "sequencia $V/p2/facebook.mp4 $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1920 --seg 5 --semente 3162 --abertura 2.9"
echo "sequencia $V/p2/linkedin.mp4 $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1350 --seg 5 --semente 3162"
echo "sequencia $V/p3/reel.mp4 $V/p3/tela1.html $V/p3/tela2.html $V/p3/tela3.html $V/p3/tela4.html --w 1080 --h 1920 --seg 5 --semente 3163 --abertura 2.9"
} | xargs -P 3 -L 1 sh -c 'python3 ferramentas/video.py "$@" 2>&1 | tail -3 | sed "s|^|$1 $2 $3: |"' _
# Abertura curta: corte do começo vazio nos vídeos que vão como primeiro item
for f in $V/p1/facebook.mp4 $V/p2/facebook.mp4 $V/p3/reel.mp4; do
  python3 ferramentas/cortar_inicio.py $f ${f%.mp4}_c.mp4 --max 2.4 && mv ${f%.mp4}_c.mp4 $f
done
python3 ferramentas/cortar_inicio.py $V/p2/linkedin.mp4 $V/p2/linkedin_c.mp4 && mv $V/p2/linkedin_c.mp4 $V/p2/linkedin.mp4
cp $V/p3/reel.mp4 $V/p3/facebook.mp4
echo FIM
