# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')


# initialize configuration parser
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.prop')
# get configuration parameter
path = config.get('apps','apps.fs.dir')
jdgui= config.get('tools', 'jdgui.jar')
zipalign = config.get('tools', 'zipalign.path')

import subprocess
import re
from db.Certificates import Certificates
from db.Apps import Apps
from onDevice import deviceHelper

#////////////////////////////



# extracts smali code

def apkToSmali(context):
    app = Apps.getApp(context.package)
    logger.info("%s starting dissambly to smali", app.package)

    cmd = ["apktool", "d", app.path_to_apk, "-o", path + app.package + "/smali/"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if err:
        logger.error(err)
        return
    else:
        logger.debug(out)


def allApksToSmali():

    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]

        allApksToSmali()

def assemble_and_install(context):
    app = Apps.getApp(context.package)
    logger.info("%s starting reassembling to apk", app.package)

    newapk = path + app.package + "/" + app.package + "-new.apk"
    newalignedapk = path + app.package + "/" + app.package + "-aligned.apk"

    logger.info("%s reassembling to apk", context.package)
    cmd = ["apktool", "b", path + app.package + "/smali/", "-o", newapk]
    logger.debug(" ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        logger.error(err)
        return
    else:
        logger.debug(out)

    logger.info("%s signing apk", context.package)
    cmd = ["jarsigner", "-verbose", "-sigalg", "SHA1withRSA", "-digestalg", "SHA1", "-keystore", "my-release-key.keystore", "--store-pass", "123456", "-keypass", "123456", newapk, "alias_name"]
    logger.debug(" ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        logger.error(err)
        return
    else:
        logger.debug(out)

    logger.info("%s aligning apk", context.package)
    cmd = [zipalign, "-f", "-v", "4", newapk, newalignedapk]
    logger.debug(" ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        logger.error(err)
        return
    else:
        logger.debug(out)

    app = Apps()
    app.package = context.package
    app.path_to_apk = newalignedapk
    deviceHelper.uninstallapk(app)
    deviceHelper.installapk(app)



# unpacks to jar file

def apkTorJar(context):
    app = Apps.getApp(context.package)
    logger.info("%s starting dex to jar", app.package)
    cmd = ["d2j-dex2jar", "-o", path + app.package + "/" + app.package + "-dex2jar.jar", app.path_to_apk, ]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        logger.error(err)
        return
    else:
        logger.debug(out)

def allApksToJar():

    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]

        apkTorJar(app)


# open jd gui
def openJarInJdGui(context):
    logger.info("%s opening jar in JD Gui", context.package)
    app = Apps.getApp(context.package)
    cmd = [jdgui, path + app.package + "/" + app.package + "-dex2jar.jar"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if err:
        logger.error(err)
        return
    else:
        logger.debug(out)