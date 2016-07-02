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
from db.Apps import Apps

# install apk file to device
def installapk(app):
    command = ["adb"]
    if deviceId  <> "":
        command.extend(["-s", deviceId])
    command.extend(["install", "-r", "-d", app.path_to_apk])
    result = os.system(" ".join(command))

def do():
    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getApks()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]
        installapk(app)

