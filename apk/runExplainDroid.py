# MK Jul 2016

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import subprocess
import re
from db.Apps import Apps
from db.Malware import Malware
from multiprocessing import Process

# initialize configuration parser
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.prop')
# get configuration parameter
expdroidscript = config.get('tools', 'expdroid.script.file')
path = config.get('apps', 'apps.fs.dir')


def explaindroid(appsList):
    """
    running Explain Droid on a list of apps
    :param appsList:
    :return:
    """
    p_result = re.compile(".*LABEL: BENIGN.*")

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]
        logFile = path + app.package + "/ExplainDroid.log"
        logger.info("%s running ExplainDroid", app.package)

        malware = Malware()
        malware.package = app.package
        malware.logfile = logFile
        malware.tool = "ExplainDroid"


        cmd = [expdroidscript, "-mod", "linux", "-apk", app.path_to_apk]  # there are RSA and DSA certificates; cater for both
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
                    malware.result = "benign"
                    logger.info("%s is benign", app.package)
                    break
            if not a:
                malware.result = "malicious"
                logger.info("%s is malicious", app.package)

            malware.insert()

def chunkify(lst,n):
    return [ lst[i::n] for i in xrange(n) ]


def do():
    """
    splitting the list of apps to analyze and start in multiple threads
    :return:
    """
    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    threads = []
    for list in chunkify(appsList, 4):
        p = Process(target=explaindroid, args=(list,))
        logger.info("starting mallodroid thread %s", p)
        threads += [p]
        p.start()

    for t in threads:
        t.join()