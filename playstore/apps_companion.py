import ConfigParser

from pick import pick

from playstore import apps_download
from onDevice import deviceHelper
from db.Apps import Apps
# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

# get configuration parameter
path = config.get('apps','apps.fs.dir')
app_list = config.get('apps','apps.companion.list')
deviceId = config.get('dev','dev.adb.id')

# downloads apps from playstore
def download():
    with open(app_list) as lines:
        packages = [line.rstrip('\n') for line in lines]
        packages.insert(0,"ALL")
        packages.append("quit")
        package, index = pick(packages, "choose package")
        if package == "ALL":
            apps_download.downloadApps(path, app_list, False, True)
        else:
            apps_download.downloadApp(path, package, False, True)


# downloads apps from playstore
def install():
    with open(app_list) as lines:
        packages = [line.rstrip('\n') for line in lines]
        packages.insert(0,"ALL")
        packages.append("quit")
        package, index = pick(packages, "choose package")
        if package == "ALL":
            apps = Apps.getAllApps()
            for a in apps:
                app = Apps()
                app.package = a[0]
                app.path_to_apk = a[1]
                deviceHelper.installapk(app)
        else:
            app = Apps.getApp(package)
            deviceHelper.installapk(app)
