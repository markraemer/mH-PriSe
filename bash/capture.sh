#!/bin/bash
## files and folders
SSLKEYLOGFILE="/media/exthdd/recording/sslkeylogfile.txt"
RECORDINGPATH="/media/exthdd/experiments/"
APPLIST_FILE="../apps_companion.prop"

###
## SETUP LOCAL PATH for mysql
## mysql_config_editor set --login-path=local --host=localhost --user=root --password
###


## output formatting
FN='\e[0m' # normal
FB='\e[1m' # bold
FU='\e[4m' # underlined
FBL='\e[5m' # blink
FRED='\e[91m' # red
FGRE='\e[92m' # green
FYEL='\e[93m' # yellow
FBLU='\e[94m' # blue

## function declarations ##

function exec_query {
    QUERY_RES="`echo $1 | mysql --login-path=local -i mhealth_apps | tail -n1`"
    echo $QUERY_RES
}

function echoc {
    echo -e "\n$FBLU $1 $FN"
}
# prepare recording
if [ $# != 1 ]
  then
    echo "Usage: capture.sh <test_case>"
    exit 0
fi

# ask to select another app
while true;
do

# load test steps and ask for input
TEST_STEPS="`exec_query "select group_concat(name SEPARATOR '\n') as names from experiment_test_steps where test_case='${1}' order by experiment_test_steps.order ASC;"`"

# ask for which pacakge to execute tests for
cat -n $APPLIST_FILE
echoc "choose package by providing number; ctrl+c to abort"
read id
{
    APP="`sed "${id}q;d" $APPLIST_FILE`"
} &&
  # do if valid input
  {
    TIMESTAMP="`date +%Y-%m-%d_%H:%M:%S`"
    APP_RECORDINGPATH="$RECORDINGPATH$APP/$1/$TIMESTAMP"
    mkdir -p ${APP_RECORDINGPATH}

    #reformat timestamp to insert into db
    TIMESTAMP="`echo $TIMESTAMP | sed 's/_/ /g'`"

    exec_query "insert into experiments (package, time, test_case, log_folder) values ('$APP','${TIMESTAMP}','$1', '$APP_RECORDINGPATH');"

    # startup app on phone but with some delay
    adb shell "sleep 2 && monkey -p $APP -c android.intent.category.LAUNCHER 1" &

    # tShark start and send to background
    tshark -i wlan0 -w "$APP_RECORDINGPATH/tshark.pncap" -o ssl.keylog_file:$SSLKEYLOGFILE 2> /dev/null &
    TSHARK_PID=$!

    # MITM proxy start up
    export "SSLKEYLOGFILE=$SSLKEYLOGFILE"
    touch "$APP_RECORDINGPATH/mitm.out"



    # start screen recording
    echoc "RECORDING -- don't forget to click Android window to activate the recording"
    PHONESCREENCAST="$APP_RECORDINGPATH/screencast.ogv"
    gnome-terminal -e "recordmydesktop --windowid `xwininfo -display :0 | grep 'id: 0x' | grep -Eo '0x[a-z0-9]+'` -o $PHONESCREENCAST" --geometry 1x1+0+0

    # start packet capturing
    gnome-terminal -e "`echo -e mitmproxy -T --host -w $APP_RECORDINGPATH/mitm.out`" --geometry 80x65+0+0



    sleep 3
    # allow to iterate through test cases
    while true;
    do

    echo -e $TEST_STEPS "q quit"  | cat -n
    echoc "select test step or type q to exit"
    read id

    if [ $id == 'q' ]
      then
        break
    fi

    TS="`echo -e $TEST_STEPS | sed "${id}q;d"`"

    exec_query "select short_desc, long_desc from experiment_test_steps where name='${TS}';"
    echoc "provide comment"
    read COMMENT
    echoc "provide rating"
    read RATING


    exec_query "insert into experiments_details set comment='$COMMENT', experiment=(select id from experiments where package='$APP' and time='$TIMESTAMP' and test_case='$1' limit 1), test_step='$TS', rating='$RATING';"

    done

    # stop mitmproxy
    MITM="`pgrep -a mitm | awk '{print $1}'`"
    kill -1 $MITM

    # stop screen recording
    RECORDER="`pgrep -a recordmydesktop | awk '{print $1}'`"
    kill -2 $RECORDER

    echoc 'Clear all data for app?'
    read CLEARP
    if [ $CLEARP == 'y' ]
       then
        # stop app on phone again and clear data
        adb shell pm clear $APP
    fi
    # stop the app anyway
    adb shell am force-stop $APP


    # stop recording with tshark
    kill -2 $TSHARK_PID

    # read commint from input
    echoc "Comment on test result:"
    read COMMENT
    # insert comment into database
    exec_query "update experiments set comment='$COMMENT' where package='$APP' and test_case='$1' and time='${TIMESTAMP}';"
  }

done
