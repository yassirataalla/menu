#!/bin/bash
S=/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad
cd $S
for d in ep9 ep9L; do ls -t $S/out/$d/*.png 2>/dev/null | head -3 | xargs -r rm -f; done
$S/bvenv/bin/python render_range.py toys13.py "$S/out/ep9/f_" 1 840 >> $S/e9.log 2>&1
[ $(ls $S/out/ep9 | wc -l) -ge 840 ] && $S/bvenv/bin/python $S/ep9/finish_ep9.py v $S/out/ep9/ /home/user/menu/boulon_tiktok_09.mp4 >> $S/e9.log 2>&1
LAND_SH=30 LAND_PCT=100 $S/bvenv/bin/python render_range.py toys13L.py "$S/out/ep9L/f_" 1 840 >> $S/e9.log 2>&1
[ $(ls $S/out/ep9L | wc -l) -ge 840 ] && $S/bvenv/bin/python $S/ep9/finish_ep9.py l $S/out/ep9L/ /home/user/menu/boulon_youtube_09.mp4 >> $S/e9.log 2>&1
echo ALLDONE >> $S/e9.log
