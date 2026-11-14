#!/bin/bash
cd "$(dirname "$0")/../../.."
V=pautas/2026-11-15/v1
{
echo "tela $V/p1/tela2.html $V/p1/ig_tela2.mp4 --w 1080 --h 1350 --seg 6 --semente 3191"
echo "sequencia $V/p1/facebook.mp4 $V/p1/tela1.html $V/p1/tela2.html $V/p1/tela3.html --w 1080 --h 1920 --seg 5 --semente 3191 --abertura 2.9"
echo "tela $V/p2/tela2.html $V/p2/ig_tela2.mp4 --w 1080 --h 1350 --seg 6 --semente 3192"
echo "sequencia $V/p2/facebook.mp4 $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1920 --seg 5 --semente 3192 --abertura 2.9"
echo "sequencia $V/p2/linkedin.mp4 $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1350 --seg 5 --semente 3192"
} | xargs -P 3 -L 1 sh -c 'python3 ferramentas/video.py "$@" 2>&1 | tail -3 | sed "s|^|$1 $2 $3: |"' _
for f in $V/p1/facebook.mp4 $V/p2/facebook.mp4; do
  python3 ferramentas/cortar_inicio.py $f ${f%.mp4}_c.mp4 --max 2.4 && mv ${f%.mp4}_c.mp4 $f
done
python3 ferramentas/cortar_inicio.py $V/p2/linkedin.mp4 $V/p2/linkedin_c.mp4 && mv $V/p2/linkedin_c.mp4 $V/p2/linkedin.mp4
echo FIM
