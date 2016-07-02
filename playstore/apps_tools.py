import subprocess

path = "/media/exthdd/tools/Android/apps/"
appsList = "../apps_tools.prop"

def installapk(appId):
    #subprocess.call(["adb","devices"])
    subprocess.call(["adb", "-s" , "037dc31f093b0ada", "install", "-r", "-d", path + appId + "/" + appId + ".apk"])

#def wipeDevice():
# subprocess.call(["adb", "-s" , "037dc31f093b0ada", "shell", "am", "broadcast", "-a", "android.intent.action.MASTER_CLEAR"])

#apps_download.downloadApps(path,appsList)
with open(appsList) as f:
    for appId in f:
        print(appId.strip())
        #wipeDevice()
        installapk(appId.strip())