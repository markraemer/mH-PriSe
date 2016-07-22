# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import json

from db.Apps import Apps
from db.Addons import Addons
import deviceHelper
import glob
import time
import os


data_dir = "/storage/emulated/0/addons_detector/"



def parseJson():

    apps = Apps.getAllApps()
    appList = []
    for app in apps:
        appList.append(app[0])


    file = glob.glob('/tmp/dummy/*')
    docs = json.loads(open(file[0]).read())

    for i in range(0,len(docs)):
        ad = Addons()
        ad.package =  docs[i]['appPackageName']
        if ad.package not in appList:
            continue
        logger.info("%s adding addins", ad.package)
        for addon in docs[i]['addons']:
            ad.addon_type = addon['addon_type']
            ad.name = addon['name']
            ad.insert()
            logger.debug("%s adding %s", ad.package, ad.name)

    os.remove(file[0])


def do():
    app = Apps()
    app.package = "com.denper.addonsdetector"
    # this will only work on a Nexus 5 with Android 6
    if deviceHelper.checkInstall(app):
        logger.debug("Addons detector found on device")
        deviceHelper.startApp(app,"com.denper.addonsdetector.ui.Dashboard")
        deviceHelper.tapScreem("540", "940")
        time.sleep(5)
        deviceHelper.tapScreem("360", "600")
        deviceHelper.tapScreem("330", "1700")
        deviceHelper.tapScreem("730", "1200")
        deviceHelper.tapScreem("550", "1200")

        deviceHelper.copyFile(data_dir, "/tmp/dummy")
        deviceHelper.deleteFile(data_dir + "*")
        parseJson()

    else:
        logger.warning("Addons Detector Application not found")

