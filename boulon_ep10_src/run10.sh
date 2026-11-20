#!/bin/bash
S=/tmp/claude-0/-home-user-menu/0da142f0-cc7e-5e88-b2dc-1c103cc03c6a/scratchpad
cd $S; mkdir -p $S/out/ep10 $S/out/ep10L
for d in ep10 ep10L; do ls -t $S/out/$d/*.png 2>/dev/null | head -3 | xargs -r rm -f; done
$S/bvenv/bin/python render_range.py toys17.py "$S/out/ep10/f_" 1 840 >> $S/e10.log 2>&1
[ $(ls $S/out/ep10 | wc -l) -ge 840 ] && [ ! -f /home/user/menu/boulon_tiktok_10.mp4 ] && $S/bvenv/bin/python $S/ep10/finish_ep10.py v $S/out/ep10/ /home/user/menu/boulon_tiktok_10.mp4 >> $S/e10.log 2>&1
LAND_SH=30 LAND_PCT=100 $S/bvenv/bin/python render_range.py toys17L.py "$S/out/ep10L/f_" 1 840 >> $S/e10.log 2>&1
[ $(ls $S/out/ep10L | wc -l) -ge 840 ] && [ ! -f /home/user/menu/boulon_youtube_10.mp4 ] && $S/bvenv/bin/python $S/ep10/finish_ep10.py l $S/out/ep10L/ /home/user/menu/boulon_youtube_10.mp4 >> $S/e10.log 2>&1
echo ALLDONE >> $S/e10.log
