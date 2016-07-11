# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')


import ConfigParser
# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')
deviceId = config.get("dev","dev.adb.id")

import os
import subprocess
from db.Apps import Apps

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



def doAll(method):
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

