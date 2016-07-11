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

import subprocess
import re
from db.Certificates import Certificates
from db.Apps import Apps

#////////////////////////////

# extracts smali code
def allApksToSmali():

    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]

        logger.info("%s starting dissambly to smali", app.package)

        cmd = ["apktool", "d",  app.path_to_apk, "-o", path + app.package + "/smali/"]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        if err:
            logger.error(err)
            continue
        else:
            logger.debug(out)

# unpacks to jar file
def allApksToJar():

    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]

        logger.info("%s starting dex to jar", app.package)

        cmd = ["d2j-dex2jar", "-o", path + app.package + "/" + app.package + "-dex2jar.jar", app.path_to_apk,]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        if err:
            logger.error(err)
            continue
        else:
            logger.debug(out)