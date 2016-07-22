#!/system/bin/sh
pm list packages -3 | cut -f 2 -d ':' | while read a; do am force-stop $a; done
