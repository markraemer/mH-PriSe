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
    QUERY_RES=`echo $1 | mysql --login-path=local -i mhealth_apps`
    echo $QUERY_RES
}

# list all recorded experiments for a specific package
function show_experiments {
    echoc $1
    REC_EXP=`exec_query "select id, time, test_case, '\n' from experiments where package='$1' order by time DESC;"`
    echo -e $REC_EXP
    read id

    EXP_FOLDER=`exec_query "select log_folder from experiments where id='$id';" | awk {'print $2'}`

    # select action
    ACTIONS=("network traces" "open folder")
    select ACTION in "${ACTIONS[@]}"
    do
        case $ACTION in
            "network traces")
                mitmproxy -r $EXP_FOLDER/mitm.out
                break
                ;;
            "open folder")
                xdg-open $EXP_FOLDER
                break
                ;;
            *) echo invalid option;;
        esac
    done



}

# show missing documentation
function missing_doc {
    echo "select tc.name as test_case, group_concat(ts.name) as test_steps, count(ts.name) as num from experiment_test_steps ts join experiment_test_cases tc on ts.test_case = tc.name
    where ts.name not in (select test_step from experiments_details ed join experiments e on ed.experiment = e.id where
    e.package='$1')  group by tc.name;" | mysql --login-path=local -i mhealth_apps

}

function echoc {
    echo -e "$FBLU $1 $FN"
}

function doc_test_cases {
    CASES=`exec_query "SELECT id, time, test_case, '\n' FROM experiments where package='$1';"`
    # cut down query where id not in (select distinct experiment from experiments_details) and
    echo -e $CASES

    read id
    TC=`exec_query "select test_case from experiments where id='$id';" | awk {'print $2'}`
    doc_test_steps $TC $id

}

function doc_test_steps {
    # load test steps and ask for input
    TEST_STEPS=`exec_query "select group_concat(name SEPARATOR ' ') as names from experiment_test_steps where test_case='${1}' order by experiment_test_steps.order ASC;"`
    # allow to iterate through test cases
    # select test step
    PS3="select test step or exit"
    STEPS=( ${TEST_STEPS} "quit")
    select STEP in "${STEPS[@]:1}"
    do
        case $STEP in
            "quit")
                break
                ;;
            *)  TS=$STEP
                exec_query "select short_desc, long_desc from experiment_test_steps where name='${TS}';"
                echoc "provide comment"
                rm /tmp/comment
                nano /tmp/comment
                COMMENT=`cat /tmp/comment`
                echoc "provide rating"
                rm /tmp/rating
                nano /tmp/rating
                RATING=`cat /tmp/rating`
                re='^[0-9]+$' # check if time or number provided
                if ! [[ $2 =~ $re ]] ;
                    then
                        id=`exec_query "select id from experiments where package='$APP' and time='$2' and test_case='$1' limit 1;"`
                fi

                exec_query "insert into experiments_details set comment='$COMMENT', experiment='$id', test_step='$TS', rating='$RATING';"
                ;;
        esac
    done
}

function select_test_case {
    # load test steps and ask for input
    TEST_CASES=`exec_query "select group_concat(name SEPARATOR ' ') as names from experiment_test_cases;"`
    # allow to iterate through test cases
    # select test step
    PS3="select test case or exit"
    CASES=( ${TEST_CASES} "quit")
    select CASE in "${CASES[@]:1}"
    do
        case $CASE in
            "quit")
                break
                ;;
            *)  TC=$CASE
                break
                ;;
        esac
    done
}

function start_recording  {


    #show_experiments $APP
    #exit 0
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

    # start packet capturing PHONE <=> WEB
    gnome-terminal -e "`echo -e mitmproxy -T --host -w $APP_RECORDINGPATH/mitm.out`" --geometry 80x65+0+0

    # start packet capturing SENSOR <=> PHONE
    # make sure HCI log is enabled on phone
    # restarting bluetooth will create a fresh log file
    adb shell "su -c service call bluetooth_manager 8" # off
    adb shell "rm  /storage/self/primary/btsnoop_hci.log" # delete log file
    adb shell "su -c service call bluetooth_manager 6" # on


    sleep 3

    # start documentation here
    doc_test_steps $1

    # stop mitmproxy
    MITM="`pgrep -a mitm | awk '{print $1}'`"
    kill -1 $MITM

    # stop screen recording
    RECORDER="`pgrep -a recordmydesktop | awk '{print $1}'`"
    kill -2 $RECORDER

    # copy log file from phone
    adb pull /storage/self/primary/btsnoop_hci.log $APP_RECORDINGPATH/hci.log

    # copy app content incl. database from phone
    # this command uses ToyBox which comes with Android 6.0
    # other possibilities would have been BusyBox (cp implementation not as good)
    adb shell "su -c toybox cp -r /data/data/$APP /sdcard/app_backups/$APP"
    adb pull /sdcard/app_backups/$APP $APP_RECORDINGPATH/app_content 1> /dev/null 2> /dev/null
    adb shell "rm -rf /sdcard/app_backups/$APP"

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


################ main script starts here ############################

# ask to select another app
while true;
do

    # ask for which pacakge to execute tests for
    # load packages from file
    readarray -t PACKAGES < $APPLIST_FILE

    PS3="choose package by providing number; ctrl+c to abort"
    select opt in "${PACKAGES[@]}"
    do
        APP=$opt
        echoc $APP
        break
    done


    # select action
    ACTIONS=("start recording" "display recording" "document" "missing documentation")
    select ACTION in "${ACTIONS[@]}"
    do
        case $ACTION in
            "start recording")
                echoc "starting recording"
                select_test_case
                start_recording $TC
                break
                ;;
            "display recording")
                show_experiments ${APP}
                break
                ;;
            "document")
                doc_test_cases $APP
                break
                ;;
            "missing documentation")
                missing_doc $APP
                break
                ;;
            *) echo invalid option;;
        esac
    done

      # do if valid input

done
