#!/bin/sh

PBKEY="/media/exthdd/experiments/com.withings.wiscale2/device-16/wspubkey.pem"


MACS[0]="00:00:00:00:00:00"
MACS[1]="00:00:00:00:00:00"

CHALLENGE=("AAAAAAAA" "AAAAAAAA")


for i in `seq 0 1`;
do
    DATA="action=get&mac_address=${MACS[i]}&service=wbs04-ws.withings.net&challenge=${CHALLENGE[i]}&method=sha&keyonly=1"
    MSG="`curl  http://wbs04-ws.withings.net/cgi-bin/v2/certificate -d $DATA`"

    DIGEST="`echo $MSG | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["body"]["digest"]'`"
    TS="`echo $MSG | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["body"]["date"]'`"

    d="${MACS[i]}:${CHALLENGE[i]}:$TS"
    echo $d > data
    echo "$DIGEST" > signature

    echo $d
    echo $DIGEST

    openssl dgst -sha256 -verify $PBKEY -signature signature data
done



