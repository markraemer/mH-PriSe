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


class helper():

    adb_command = []

    def __init__(self):
        deviceId = config.get("dev", "dev.adb.id")
        self.adb_command = ["adb"]
        if deviceId <> "":
            self.adb_command.extend(["-s", deviceId])


    # starts drozer app on phone
    # app needs to run drozer server to allow communication
    # so trying to start the server by pushing the button (tap)
    def startApp(self,app, activity):
        command = copy(self.adb_command)
        command.extend(["shell", "'am start -n", app.package + "/" + activity, "'"])
        os.system(" ".join(command))

    def tapScreem(self, x,y):
        command = copy(self.adb_command)
        command.extend(["shell", "'input tap", x, y,"'"])
        os.system(" ".join(command))

    # checks if application is installed on phone
    def checkInstall(self, app):
        command = copy(self.adb_command)
        command.extend(["shell", "pm list packages", "|", "grep", app.package])

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out.strip().endswith(app.package)

    # forward the drozer port via adb
    def forwardPort(self, port):
        command = copy(self.adb_command)
        command.extend([ "forward", "tcp:" + port, "tcp:" + port])
        os.system(" ".join(command))

    def copyFile(self, src, dst):
        if not os.path.exists(dst):
            os.mkdir(dst)
        command = copy(self.adb_command)
        command.extend(["pull", src, dst])
        os.system(" ".join(command))

    def deleteFile(self, file):
        command = copy(self.adb_command)
        command.extend(["shell", "rm -rf ",file])
        os.system(" ".join(command))