# MK Jul 2016
# runner application file
import os
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from playstore import apps_companion
from apk import extractBaseInfo, runMallodroid, installToDevice
from onDevice import runDrozer


os.system("taskset -p 0xff %d" % os.getpid())
logger.info("Starting ...")

#apps_companion.do()
#extractBaseInfo.apkInfo()
#runMallodroid.do()
#installToDevice.do()
runDrozer.do()

logger.info("... finished")