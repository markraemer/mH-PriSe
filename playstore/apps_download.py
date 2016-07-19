# MK Jun 2016
# downloads apk files from play store
# requires gplaycli and ghost python packages
# stores basic app information from playstore in database

# Do not remove
import time

GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import os

import pdfkit

from onDevice import deviceHelper

from db.Apps import Apps
from db.AppDetails import AppDetails
from db.Pripol import Pripol
from playstore.gplay.googleplay import GooglePlayAPI
from playstore.gplay.helpers import sizeof_fmt
from playstore.gplay.config import *

import ConfigParser

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
def downloadapk(appId, path, app, pripol, writeToDb):
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
    # more details from appstore page
    appdetail = AppDetails()
    appdetail.package = doc.docid
    appdetail.asin
    appdetail.category = doc.details.appDetails.appCategory[0]
    appdetail.company = doc.creator
    appdetail.mom
    appdetail.popularity = doc.details.appDetails.numDownloads
    if doc.offer[0].formattedAmount == 'Free':
        appdetail.price = 0.0
    else:
        appdetail.price = float(doc.offer[0].formattedAmount)
    appdetail.pripol = doc.annotations.privacyPolicyUrl
    appdetail.rating = doc.aggregateRating.starRating
    if doc.details.appDetails.uploadDate != '':
        appdetail.release_date = time.strftime("%Y-%m-%d",time.strptime(doc.details.appDetails.uploadDate, "%d %b %Y"))
    appdetail.title = doc.title
    appdetail.version = doc.details.appDetails.versionString
    if writeToDb:
        app.upsert()
        appdetail.upsert()

    # Download
    print "Downloading %s..." % sizeof_fmt(doc.details.appDetails.installationSize),
    try:
        if writeToDb:
            app.upsert()
            pripol.upsert()
        data = api.download(appId, vc, app.type)
        open(app.path_to_apk, "wb").write(data)

    except IndexError:
        print(appId + " is not available from play store")


def downloadApps(pathToStore, appListFile, install, writeToDb):
    with open(appListFile) as f:
        for appId in f:
            print(appId.strip())
            if appId.startswith('#') <> True:
                # create app object
                app = Apps()
                pripol = Pripol()
                sreenshotplaystore(appId.strip(),pathToStore)
                downloadapk(appId.strip(), pathToStore, app, pripol, writeToDb)
                if install:
                    deviceHelper.installapk(app)


def downloadApp(pathToStore, package, install, writeToDb):

    # create app object
    app = Apps()
    pripol = Pripol()
    sreenshotplaystore(package.strip(),pathToStore)
    downloadapk(package.strip(), pathToStore, app, pripol, writeToDb)
    if install:
        deviceHelper.installapk(app)
