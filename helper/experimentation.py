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
from terminaltables import AsciiTable

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
actions=["start", "document", "missing"]
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
    missingDocs.insert(0, ["test case", "test steps", "#"])
    table = AsciiTable(missingDocs)
    table.inner_row_border=True
    print table.table
    raw_input("TO CONTINUE PRESS ENTER...")

def select_recorded_experiment(package):
    title = "choose recording"
    recorded = Experiments.getExperimentLogForPackag(package)
    recorded.append("quit")
    record, index = pick(recorded, title)
    if record == "quit":
        return
    else:
        return recorded[index], index

def doc_recorded_test_cases(package):
    record, index = select_recorded_experiment(package)
    if record:
        exp = Experiments()
        exp.id = record[0]
        document_test_steps(record[3], exp)

def choose_test_case(package):
    recorded = Experiments.getExperimentLogForPackag(package)
    recorded.append("quit")
    record, expid = pick(recorded, "choose recording")
    return record



def document_test_steps(test_case, exp):
    print exp
    while True:
        title="select test step"
        steps = TestSteps.getStepsForCase(test_case)
        steps.append("quit")
        step, index = pick(steps,title)
        if step == "quit":
            break
        ts = TestSteps.getByName(step)
        print ts.short_desc
        ed = ExperimentsDetails()
        ed.comment = multiline_input("Comment")
        print ts.rating
        ed.rating = multiline_input("Rating")
        ed.experiment = exp.id
        ed.test_step = step
        ed.upsert()


def select_test_case():
    title = "choose test case"
    cases = TestCases.getCases()
    case, index = pick(cases, title)

    return case

def start_screen_cast(app_recordingpath):
    # start screen recording
    print("recording started - select window for screen cast")
    castfile="{}/screencast.ogv".format(app_recordingpath)
    cmd = "gnome-terminal -e \"recordmydesktop --windowid `xwininfo -display :0 | grep 'id: 0x' | grep -Eo '0x[a-z0-9]+'` -o {}\" --geometry 1x1+0+0".format(castfile)
    os.system(cmd)

def stop_screen_cast():
    # stop screen recording
    logger.debug("stopping recording")
    cmd = "kill -2 `pgrep -a recordmydesktop | awk '{print $1}'`"
    os.system(cmd)


def start_capture_network(app_recordingpath, type="p2w"):
    # start packet capturing PHONE <=> WEB
    fhandle = open("{}/mitm.out".format(app_recordingpath),'w')
    fhandle.close()
    if type == "p2w": # capture phone to web communication
        mitmconfig= "-T --host"
    elif type == "wo": # capture web browser usage
        mitmconfig= ""
    else:
        mitmconfig=""

    cmd = "export 'SSLKEYLOGFILE={}' && gnome-terminal -e 'mitmproxy {} -w "\
            "{}/mitm.out' --geometry 80x65+0+0".format(keylogfile, mitmconfig, app_recordingpath)
    os.system(cmd)

    # tShark start and send to background
    cmd = "tshark -i wlan0 -w '{}/tshark.pncap' -o ssl.keylog_file:{}  2> /dev/null &".format(app_recordingpath, keylogfile) #
    os.system(cmd)

def stop_capture_network():
    # stop mitmproxy
    logger.debug("stopping mitmproxy")
    cmd = "kill -2 `pgrep -a mitm | awk '{print $1}'`"
    os.system(cmd)

    # stop recording with tshark
    logger.debug("stopping packet capture")
    cmd = "kill -2 `pgrep -a tshark | awk '{print $1}'`"
    os.system(cmd)


def start_capture_phone(package):
    # startup app on phone but with some delay
    cmd = "adb shell 'sleep 2 && monkey -p %s -c android.intent.category.LAUNCHER 1' &" % package
    os.system(cmd)

    # start packet capturing SENSOR <=> PHONE
    # make sure HCI log is enabled on phone
    # restarting bluetooth will create a fresh log file
    cmd = "adb shell \"su -c service call bluetooth_manager 8\"" # off
    os.system(cmd)
    cmd = "adb shell \"rm  /sdcard/btsnoop_hci.log\""
    os.system(cmd)
    cmd = "adb shell \"su -c service call bluetooth_manager 6\""
    os.system(cmd)

    # reset logcat
    cmd = "adb logcat -c" # off
    os.system(cmd)

def stop_capture_phone(app_recordingpath, package):
    # copy bluetooth hci log file from phone
    logger.debug("copying hci bluetooth log")
    cmd = "adb pull /sdcard/btsnoop_hci.log {}/hci.log".format(app_recordingpath)
    os.system(cmd)

    # retrieve logcat log
    logger.debug("retrieving logcat logs")
    cmd = "adb logcat -d -f /sdcard/logcat.log"
    os.system(cmd)
    cmd = "adb pull /sdcard/logcat.log {}/logcat.log 1> /dev/null 2> /dev/null".format(app_recordingpath)
    os.system(cmd)
    cmd = "adb shell \"rm -rf /sdcard/logcat.log\""
    os.system(cmd)

    # copy app content incl. database from phone
     # this command uses ToyBox which comes with Android 6.0
     # other possibilities would have been BusyBox (cp implementation not as good)
    logger.debug("pulling full appliation backup")
    cmd = "adb shell \"su -c toybox cp -r /data/data/{} /sdcard/app_backups/{}\"".format(package, package)
    os.system(cmd)
    cmd = "adb pull /sdcard/app_backups/{} {}/app_content 1> /dev/null 2> /dev/null".format(package, app_recordingpath)
    os.system(cmd)
    cmd = "adb shell \"rm -rf /sdcard/app_backups/{}\"".format(package)
    os.system(cmd)

    if raw_input("Clear app data?") == "y":
        logger.debug("clearing app data")
        cmd = "adb shell pm clear {}".format(package)
        os.system(cmd)

    #     adb shell am force-stop $APP
    logger.debug("stopping app")
    cmd = "adb shell am force-stop {}".format(package)
    os.system(cmd)


def start_recording(context, package, testcase):
    #TODO organise different tools in functions and map functions to test cases --> recodring depends on test cases
    experiment = Experiments()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

    if testcase != "sol_arch":
        app_recordingpath = '/'.join([config.get("experiments","experiment.rec.path"), package, testcase, st])
        if not os.path.exists(app_recordingpath):
            os.makedirs(app_recordingpath)
        experiment.log_folder = app_recordingpath

    timestamp = st.replace('_',' ')


    experiment.package = package
    experiment.test_case = testcase
    experiment.time = timestamp
    experiment.upsert()

    if testcase != "sol_arch":
        start_screen_cast(app_recordingpath)

        if testcase == "av6_web_application":
            start_capture_network(app_recordingpath,"wo")
        else:
            start_capture_network(app_recordingpath)

            start_capture_phone(package)

        document_test_steps(testcase, experiment)

        stop_capture_network()

        stop_screen_cast()

        if testcase != "av6_web_application":
            stop_capture_phone(app_recordingpath, package)

    experiment.comment = raw_input("Comment?")
    experiment.upsert()

def choosePackage():
    title = 'choose package: '
    packages = Apps.getPackages()
    packages.append("quit")
    package, index = pick(packages, title)
    return package


def show_traces(context):
    if not context.package:
        package = choosePackage()
    else:
        package = context.package
    if package != "quit":
        record = choose_test_case(package)
        if record != "quit":
            cmd = "gnome-terminal -e 'mitmproxy -r {}/mitm.out'".format(record[4])
            os.system(cmd)


def open_log_folder(context):
    if not context.package:
        package = choosePackage()
    else:
        package = context.package
    if package != "quit":
        record = choose_test_case(package)
        if record != "quit":
            cmd = "xdg-open {}".format(record[4])
            os.system(cmd)


def do(action, context=None):
    if not context.package:
        package = choosePackage()
    else:
        package = context.package
    if package != "quit":
        if action == actions[0]:
            case = select_test_case()
            start_recording(context, package, case)
        elif action == actions[1]:
            doc_recorded_test_cases(package)
        elif action == actions[2]:
            show_missing_documentation(package)
