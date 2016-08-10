#!/usr/bin/env bash

tcpdump -r tshark.pncap -w tshark-filtered.pncap "src 10.0.0.35 or dst 10.0.0.35"
tshark -r tshark-filtered.pncap -Y "tcp.flags==2" -T fields -e ip.dst |  sort |  uniq |  awk '{printf("%s\n",$1)}'
