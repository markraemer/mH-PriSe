import os

from playstore import apps_download

import ConfigParser

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

# get configuration parameter
path = config.get('tools','apk.fs.dir')
appList = config.get('tools','apk.tools.list')
deviceId = config.get('dev','dev.adb.id')

# downloads apps from playstore
def do(install):
    apps_download.downloadApps(path, appList, install, False)