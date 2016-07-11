# MK Jul 2016

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import subprocess
import re
from db.Certificates import Certificates
from db.Apps import Apps
from db.Malware import Malware

# initialize configuration parser
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.prop')
# get configuration parameter
eviscript = config.get('evicheck', 'evi.script.file')
evipolicy = config.get('evicheck', 'evi.script.file')
path = config.get('apps', 'apps.fs.dir')


# ////////////////////////////

def do():
    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    p_result = re.compile(".*Policy valid!.*")

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]
        certFile = path + app.package + "/EviCheck.cert"
        logFile = path + app.package + "/EviCheck.log"
        logger.info("%s running EviCheck", app.package)

        malware = Malware()
        malware.package = app.package
        malware.logfile = logFile
        malware.tool = "EviCheck"

        cmd = ["python", eviscript, "-f", app.path_to_apk, "-g", "-p", evipolicy, "-t", certFile,
               "-m"]  # there are RSA and DSA certificates; cater for both

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        if err:
            logger.error(err)
            continue
        else:
            lines = out.splitlines()
            log = open(logFile, 'w')
            log.writelines(lines)
            log.close()

            global a # init variable
            for line in lines:
                a = p_result.match(line)
                if a:
                    malware.result = "valid"
                    logger.info("%s is valid", app.package)
                    break
            if not a:
                malware.result = "invalid"
                logger.info("%s is not valid", app.package)
            malware.insert()
