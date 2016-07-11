# MK Jul 2016
# runner application file
import os
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from playstore import apps_companion,apps_tools
from apk import extractBaseInfo, runMallodroid, manageOnDevice, signAnalysis, apkHelper, runEviCheck, runExplainDroid, checkObfuscation
from onDevice import runDrozer,addonDetector

from traffic import trafficAnalysis


from db.Location import Location
import requests


os.system("taskset -p 0xff %d" % os.getpid())
logger.info("Starting ...")

#apps_tools.do(True)
#apps_companion.do(False, True)
#extractBaseInfo.apkInfo()
#runMallodroid.do()
#manageOnDevice.doAll("INSTALL")
#runDrozer.do()
#signAnalysis.certInfo()
#addonDetector.do()

#apkHelper.allApksToSmali() #extracts all apks to smali code
#apkHelper.allApksToJar() #extracts all apks to jar

#runEviCheck.do()
#runExplainDroid.do()

#checkObfuscation.do()

### Traffic Analysis
trafficAnalysis.do(False) # true will automatically generate traffic maps



logger.info("... finished")