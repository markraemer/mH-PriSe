#!/usr/bin/python
# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import os
import ConfigParser
import subprocess
import datetime
import time
import json

from pick import pick

from db.Apps import Apps
from db.Experiments import Experiments
from db.TestCases import TestCases
from db.TestSteps import TestSteps
from db.ExperimentsDetails import ExperimentsDetails
from db.CodeAnalysis import CodeAnalysis
from db.Drozer import Drozer


# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

deviceId = config.get("dev","dev.adb.id")
keylogfile = config.get("experiments","mitmproxy.keylog.file")

######################
actions=["start recording", "display recording", "document", "missing documentation", "quit"]
## output formatting
FN='\e[0m' # normal
FB='\e[1m' # bold
FU='\e[4m' # underlined
FBL='\e[5m' # blink
FRED='\e[91m' # red
FGRE='\e[92m' # green
FYEL='\e[93m' # yellow
FBLU='\e[94m' # blue
######################

def multiline_input(title):
    data = []
    sentinel = ''
    print(title)
    for line in iter(raw_input, sentinel):
        data.append(line)
    return '\n'.join(data)

def show_missing_documentation(package):
    missingDocs = Experiments.getMissingDocumentation(package)
    for doc in missingDocs:
        print "{0:20s}{1}".format(doc[0],doc[1])
    raw_input("TO CONTINUE PRESS ENTER...")

def doc_recorded_test_cases(package):

    title = "choose recording"
    recorded = Experiments.getExperimentLogForPackag(package)
    recorded.append("quit")
    record, index = pick(recorded, title)
    if record == "quit":
        return
    document_test_steps(recorded[index][3], recorded[index][0])


def review_experiments(package):
    recorded = Experiments.getExperimentLogForPackag(package)
    recorded.append("quit")
    while True:
        record, expid = pick(recorded, "choose recording")
        if record == "quit":
            return
        actions = ["network traces","open folder"]
        action, index = pick(actions,"choose action")
        if action == actions[1]:
            cmd = "xdg-open {}".format(record[4])
            os.system(cmd)
        elif action == actions[0]:
            cmd = "gnome-terminal -e 'mitmproxy -r {}/mitm.out'".format(record[4])
            os.system(cmd)

def document_test_steps(test_case, experiment):

   while True:
        title="select test step"
        steps = TestSteps.getStepsForCase(test_case)
        steps.append("quit")
        step, index = pick(steps,title)
        if step == "quit":
            break

        ed = ExperimentsDetails()
        ed.comment = multiline_input("Comment")
        ed.rating = multiline_input("Rating")
        ed.experiment = experiment.id
        ed.test_step = step
        ed.upsert()


def select_test_case():
    title = "choose test case"
    cases = TestCases.getCases()
    case, index = pick(cases, title)

    return case


def start_recording(package, testcase):

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

    app_recordingpath = '/'.join([config.get("experiments","experiment.rec.path"), package, testcase, st])
    print app_recordingpath

    if not os.path.exists(app_recordingpath):
        os.makedirs(app_recordingpath)

    timestamp = st.replace('_',' ')

    experiment = Experiments()
    experiment.package = package
    experiment.test_case = testcase
    experiment.log_folder = app_recordingpath
    experiment.time = timestamp
    experiment.upsert()

    # start screen recording
    print("recording started - select window for screen cast")
    castfile="{}/screencast.ogv".format(app_recordingpath)
    cmd = "gnome-terminal -e \"recordmydesktop --windowid `xwininfo -display :0 | grep 'id: 0x' | grep -Eo '0x[a-z0-9]+'` -o {}\" --geometry 1x1+0+0".format(castfile)
    os.system(cmd)


    # start packet capturing PHONE <=> WEB
    fhandle = open("{}/mitm.out".format(app_recordingpath),'w')
    fhandle.close()
    cmd = "export 'SSLKEYLOGFILE={}' && gnome-terminal -e 'mitmproxy -T --host -w "\
            "{}/mitm.out' --geometry 80x65+0+0".format(keylogfile,app_recordingpath)
    os.system(cmd)


    # tShark start and send to background
    cmd = "tshark -i wlan0 -w '{}/tshark.pncap' -o ssl.keylog_file:{} 2> /dev/null  &".format(app_recordingpath, keylogfile) #
    os.system(cmd)

    # startup app on phone but with some delay
    cmd = "adb shell 'sleep 2 && monkey -p %s -c android.intent.category.LAUNCHER 1' &" % package
    os.system(cmd)

    # start packet capturing SENSOR <=> PHONE
    # make sure HCI log is enabled on phone
    # restarting bluetooth will create a fresh log file
    cmd = "adb shell \"su -c service call bluetooth_manager 8\"" # off
    os.system(cmd)
    cmd = "adb shell \"rm  /storage/self/primary/btsnoop_hci.log\""
    os.system(cmd)
    cmd = "adb shell \"su -c service call bluetooth_manager 6\""
    os.system(cmd)

    time.sleep(3)

    document_test_steps(testcase, experiment)

    # stop mitmproxy
    cmd = "kill -2 `pgrep -a mitm | awk '{print $1}'`"
    os.system(cmd)

    # stop screen recording
    cmd = "kill -2 `pgrep -a recordmydesktop | awk '{print $1}'`"
    os.system(cmd)

     # copy log file from phone
    cmd = "adb pull /storage/self/primary/btsnoop_hci.log {}/hci.log".format(app_recordingpath)
    os.system(cmd)
     # copy app content incl. database from phone
     # this command uses ToyBox which comes with Android 6.0
     # other possibilities would have been BusyBox (cp implementation not as good)

    cmd = "adb shell \"su -c toybox cp -r /data/data/{} /sdcard/app_backups/{}\"".format(package, package)
    os.system(cmd)
    cmd = "adb pull /sdcard/app_backups/{} {}/app_content 1> /dev/null 2> /dev/null".format(package, app_recordingpath)
    os.system(cmd)
    cmd = "adb shell \"rm -rf /sdcard/app_backups/{}\"".format(package)
    os.system(cmd)

    if raw_input("Clear app data?") == "y":
        cmd = "adb shell pm clear {}".format(package)
        os.system(cmd)

    #     adb shell am force-stop $APP
    cmd = "adb shell am force-stop {}".format(package)
    os.system(cmd)

    # stop recording with tshark
    cmd = "kill -2 `pgrep -a tshark | awk '{print $1}'`"
    os.system(cmd)

    experiment.comment = raw_input("Comment?")
    experiment.upsert()

def start():

    while True:
        title = 'choose package: '
        packages = Apps.getPackages()
        packages.append("quit")
        package, index = pick(packages, title)
        if package == "quit":
            break
        print "package >>> {}".format(package)

        title = 'choose action: '
        action, index = pick(actions, title)

        if action == actions[0]:
            print "starting recording"
            case = select_test_case()
            start_recording(package,case)
        elif action == actions[1]:
            print "showing experiments"
            review_experiments(package)
        elif action == actions[2]:
            print "document test cases"
            doc_recorded_test_cases(package)
        elif action == actions[3]:
            print "show missing documentation"
            show_missing_documentation(package)
        elif action == actions[4]:
            break