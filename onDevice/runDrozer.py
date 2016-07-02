# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import os
import ConfigParser
import subprocess

from db.Apps import Apps
from db.CodeAnalysis import CodeAnalysis
from db.Drozer import Drozer


# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

deviceId = config.get("dev","dev.adb.id")

# check if drozer client application is installed on the phone
def checkInstall():
    command = ["adb"]
    if deviceId <> "":
        command.extend(["-s", deviceId])
    command.extend(["shell", "pm list packages", "|", "grep", "com.mwr.dz"])

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip().endswith("com.mwr.dz")

# forward the drozer port via adb
def forwardPort():
    command = ["adb"]
    if deviceId <> "":
        command.extend(["-s", deviceId])
    command.extend(["forward", "tcp:31415", "tcp:31415"])
    os.system(" ".join(command))

# starts drozer app on phone
# app needs to run drozer server to allow communication
# so trying to start the server by pushing the button (tap)
def startApp():
    command = ["adb"]
    if deviceId <> "":
        command.extend(["-s", deviceId])
    command.extend(["shell", "'am start -n com.mwr.dz/com.mwr.dz.activities.MainActivity && input tap 880 1700'"])
    os.system(" ".join(command))

# run drozer command to run command
def runDrozerCmd(app, cmd):
    command = ["drozer", "console", "connect", "-c", "run " + cmd + " " + app.package]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    logger.debug(out)
    return out, err

def writeToDb(type,out,app):
    dz = Drozer()
    lines = out.splitlines()
    lines.pop(len(lines) - 1)
    while "Package" not in lines.pop(0):
        pass
    dz.package = app.package
    while len(lines) > 0:
        dz.type_name = type
        dz.class_name = lines.pop(0).strip()
        dz.permission = lines.pop(0).strip().replace("Permission: ", "")
        if "Parent Activity" in dz.permission:
            # skip parent activity information
            dz.permission = lines.pop(0).strip().replace("Permission: ", "")
        dz.insert()

def do():
    if checkInstall():
        forwardPort()
        #startApp()

        # get all apks which are linked in the database
        # will come with [0] package [1] path_to_apk
        appsList = Apps().getApks()

        for apk in appsList:
            app = Apps()
            app.path_to_apk = apk[1]
            app.package = apk[0]
            logger.info("%s running drozer", app.package)

            out, err = runDrozerCmd(app, "app.service.info -a")
            if err:
                logger.error(err.strip())
                logger.error("Probably client app is not running or app not installed ...")
            else:
                if "No exported" in out:
                    pass
                else:
                    writeToDb("service", out, app)


            out, err = runDrozerCmd(app, "app.broadcast.info -a")
            if err:
                logger.error(err.strip())
                logger.error("Probably client app is not running or app not installed ...")
            else:
                if "No matching" in out:
                    pass
                else:
                    writeToDb("broadcast", out, app)

            out, err = runDrozerCmd(app, "app.provider.info -a")
            if err:
                logger.error(err.strip())
                logger.error("Probably client app is not running or app not installed ...")
            else:
                if "No matching" in out:
                    pass
                else:
                    writeToDb("provider", out, app)

            out, err = runDrozerCmd(app, "app.activity.info -a")
            if err:
                logger.error(err.strip())
                logger.error("Probably client app is not running or app not installed ...")
            else:
                if "No exported" in out:
                    pass
                else:
                    writeToDb("activity", out, app)

            out, err = runDrozerCmd(app, "app.package.attacksurface")
            if err:
                logger.error(err.strip())
                logger.error("Probably client app is not running or app not installed ...")
            else:
                cal = CodeAnalysis()
                cal.package = app.package
                if "is debuggable" in out:
                    cal.debuggable = 'y'
                else:
                    cal.debuggable = 'n'
                cal.insert()


    else:
        logger.warning("Install Drozer Client application first")

