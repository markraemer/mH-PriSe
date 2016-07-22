import os
from pick import pick

from playstore import apps_download

import ConfigParser

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

# get configuration parameter
path = config.get('apps','tool.apk.fs.dir')
app_list = config.get('apps','tool.apk.tools.list')
deviceId = config.get('dev','dev.adb.id')

# downloads apps from playstore
def do(install):
    with open(app_list) as lines:
        packages = [line.rstrip('\n') for line in lines]
        packages.insert(0,"ALL")
        packages.append("quit")
        package, index = pick(packages, "choose package")
        if package == "ALL":
            apps_download.downloadApps(path, app_list, install, False)
        else:
            apps_download.downloadApp(path, package, install, False)





