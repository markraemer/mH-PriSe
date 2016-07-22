# MK Jul 2016
# helper to run apps on device and get some results back

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

# initialize root adb
# initialize configuration parser
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

import os
import subprocess
from copy import copy

from db.Apps import Apps
from db.CodeAnalysis import CodeAnalysis
from db.Drozer import Drozer

adb_command = []


deviceId = config.get("dev", "dev.adb.id")
adb_command = ["adb"]
if deviceId <> "":
    adb_command.extend(["-s", deviceId])


# starts drozer app on phone
# app needs to run drozer server to allow communication
# so trying to start the server by pushing the button (tap)
def startApp(app, activity):
    command = copy(adb_command)
    command.extend(["shell", "'am start -n", app.package + "/" + activity, "'"])
    os.system(" ".join(command))

def tapScreem( x,y):
    command = copy(adb_command)
    command.extend(["shell", "'input tap", x, y,"'"])
    os.system(" ".join(command))

# checks if application is installed on phone
def checkInstall( app):
    command = copy(adb_command)
    command.extend(["shell", "pm list packages", "|", "grep", app.package])

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip().endswith(app.package)

# forward the drozer port via adb
def forwardPort( port):
    command = copy(adb_command)
    command.extend([ "forward", "tcp:" + port, "tcp:" + port])
    os.system(" ".join(command))

def copyFile( src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    command = copy(adb_command)
    command.extend(["pull", src, dst])
    os.system(" ".join(command))

def deleteFile( file):
    command = copy(adb_command)
    command.extend(["shell", "rm -rf ",file])
    os.system(" ".join(command))

def stopAllApps():
    command = copy(adb_command)
    command.extend(["shell \"pm list packages -3\" | cut -f 2 -d ':' | tr -d '\\r' | while read a; do adb shell \"am force-stop $a\"; done"])
    logger.info("stopping all 3rd party apps on the device")
    os.system(" ".join(command))

# get the sdk version
def android_version():
    cmd = ["adb", "shellgetprop", "ro.build.version.sdk"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

# install apk file to device
def installapk(app):
    command = ["adb"]
    if deviceId  <> "":
        command.extend(["-s", deviceId])
    command.extend(["install", "-r", "-d", app.path_to_apk])
    result = os.system(" ".join(command))

# uninstall app from device
def uninstallapk(app):
    command = ["adb"]
    if deviceId  <> "":
        command.extend(["-s", deviceId])
    logger.info("%s uninstalling" % app.package)
    command.extend(["uninstall", app.package])
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        logger.error(err)
    else:
        logger.info(out)


def doAllAppInstall(method):
    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]
        if method is "INSTALL": #install apps
            installapk(app)
        elif method is "UNINSTALL": #uninstall apps
            uninstallapk(app)