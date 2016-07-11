import os

from playstore import apps_download

import ConfigParser

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

# get configuration parameter
path = config.get('apps','apps.fs.dir')
appList = config.get('apps','apps.companion.list')
deviceId = config.get('dev','dev.adb.id')

# downloads apps from playstore
def do(install, writeToDb):
    apps_download.downloadApps(path, appList, install, writeToDb)
