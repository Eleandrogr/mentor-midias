#!/bin/bash
# Produção dos vídeos da pauta 2026-11-08 v1 (3 jobs em paralelo)
cd "$(dirname "$0")/../../.."
V=pautas/2026-11-08/v1
{
for p in p1 p2; do
  s=$([ $p = p1 ] && echo 3121 || echo 3122)
  for i in 1 2 3 4; do echo "tela $V/$p/tela$i.html $V/$p/ig_tela$i.mp4 --w 1080 --h 1350 --seg 6 --semente $s"; done
  echo "sequencia $V/$p/facebook.mp4 $V/$p/tela1.html $V/$p/tela2.html $V/$p/tela3.html $V/$p/tela4.html --w 1080 --h 1920 --seg 5 --semente $s"
done
echo "sequencia $V/p2/linkedin.mp4 $V/p2/tela1.html $V/p2/tela2.html $V/p2/tela3.html $V/p2/tela4.html --w 1080 --h 1350 --seg 5 --semente 3122"
echo "sequencia $V/p3/reel.mp4 $V/p3/tela1.html $V/p3/tela2.html $V/p3/tela3.html $V/p3/tela4.html --w 1080 --h 1920 --seg 4.5 --semente 3123"
echo "sequencia $V/p3/facebook.mp4 $V/p3/tela1.html $V/p3/tela2.html $V/p3/tela3.html $V/p3/tela4.html --w 1080 --h 1920 --seg 4.5 --semente 3123"
} | xargs -P 3 -L 1 sh -c 'python3 ferramentas/video.py "$@" 2>&1 | tail -1 | sed "s|^|$1 $2 $3: |"' _
echo FIM
