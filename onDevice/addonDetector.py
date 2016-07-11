# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import json

from db.Apps import Apps
from db.Addons import Addons

from helper import helper
helper = helper()

data_dir = "/storage/emulated/0/addons_detector/"



def parseJson():

    apps = Apps.getAllApps()
    appList = []
    for app in apps:
        appList.append(app[0])
    docs = json.loads(open("/tmp/healthanalysis/dummy").read())
    for i in range(0,len(docs)):
        ad = Addons()
        ad.package =  docs[i]['appPackageName']
        if ad.package not in appList:
            continue
        for addon in docs[i]['addons']:
            ad.addon_type = addon['addon_type']
            ad.name = addon['name']
            ad.insert()

def do():
    app = Apps()
    app.package = "com.denper.addonsdetector"
    if helper.checkInstall(app):
        logger.debug("Addons detector found on device")
        #helper.startApp(app,"com.denper.addonsdetector.ui.Dashboard")
        #helper.tapScreem("540", "940")
        #time.sleep(5)
        #helper.tapScreem("360", "600")
        #helper.tapScreem("330", "1700")
        #helper.tapScreem("730", "1200")
        #helper.tapScreem("550", "1200")

        #helper.copyFile(data_dir, "/tmp/healthanalysis/dummy")
        #helper.deleteFile(data_dir + "*")
        parseJson()

    else:
        logger.warning("Addons Detector Application not found")

