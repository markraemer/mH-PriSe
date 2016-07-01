# MK Jun 2016
# downloads apk files from play store
# requires gplaycli and ghost python packages
# stores basic app information from playstore in database

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import os

import pdfkit

from db.Apps import Apps
from db.Pripol import Pripol
from gplay.config import *
from gplay.googleplay import GooglePlayAPI
from gplay.helpers import sizeof_fmt

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')



# takes a screenshot of the appstore page and saves it
def sreenshotplaystore(appId, path):
    if not os.path.exists(path + appId):
        os.makedirs(path + appId)

    # save a screenshot as pdf file
    try:
        pdfkit.from_url("https://play.google.com/store/apps/details?id=" + appId, path + appId + '/playstore.pdf')
    except IOError:
        print("Issue taking screenshot... Proceeding \r")

# downloads the apk file
def downloadapk(appId, path, app, pripol):
    # Connect
    api = GooglePlayAPI(ANDROID_ID)
    api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

    # get some details to store in the database
    m = api.details(appId)
    doc = m.docV2
    # privacy policy
    pripol.URL = doc.annotations.privacyPolicyUrl
    pripol.package = doc.docid
    # app name, package and path to apk
    app.label = doc.title
    app.package = doc.docid
    app.path_to_apk = path + appId + "/" + appId + ".apk"
    app.type = doc.offer[0].offerType
    vc = doc.details.appDetails.versionCode

    # Download
    print "Downloading %s..." % sizeof_fmt(doc.details.appDetails.installationSize),
    try:
        app.insert()
        pripol.insert()
        data = api.download(appId, vc, app.type)
        open(app.path_to_apk, "wb").write(data)

    except IndexError:
        print(appId + " is not available from play store")


def downloadApps(pathToStore, appListFile):
    with open(appListFile) as f:
        for appId in f:
            print(appId.strip())
            if appId.startswith('#') <> True:
                # create app object
                app = Apps()
                pripol = Pripol()
                sreenshotplaystore(appId.strip(),pathToStore)
                downloadapk(appId.strip(), pathToStore, app, pripol)

