#!/usr/bin/python
# KK, December 2014
# MK, June 2016

# The script extracts the app title, version and other base info
# from all apps in a given apk dir
# and puts them into or updates them in DB

# extracts permission and stores in database

import os
import re
from db.AppPerm import AppPerm
from db.Apps import Apps


RPDIR = "/tmp/"
KIND = "fad"
perm = AppPerm()

#////////////////////////////


def apkInfo():

    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getApks()

    for apk in appsList:
        app = Apps()
        app.filesize = os.path.getsize(apk[1])
        app.package = apk[0]

        # run android build tool aapt and write into temp file
        f = open(RPDIR + "dummy_file", "w")
        command = "aapt dump badging '" + apk[1] + "' > " + RPDIR + "dummy_file"
        s = os.system(command)
        print  command, " Status: ", s
        f.close()

        # read information from temp file
        f = open(RPDIR + "dummy_file", "r")
        for line in f:
            # print line
            p_versionname = re.compile(".*versionName='(.*?)'.*")
            p_versioncode = re.compile(".*versionCode='(.*?)'.*")
            p_icon = re.compile("application.*icon='(.*?)'.*")
            p_permission = re.compile("uses-permission.*'(.*?)'.*")

    ##        if "debuggable" in line:
    ##            print "DEBUG FLAG set for " + apk + "!!!"
    ##            r["debugging_flag_set_in_manifest"] = 1
    ##        else:
    ##            r["debugging_flag_set_in_manifest"] = 0
    ##        if "intent" in line:
    ##            print "INTENT FILTER used in " + apk + "!!!"

            a = p_versionname.match(line)
            if a:
                app.version = a.group(1)
                #break

            a = p_versioncode.match(line)
            if a:
                app.versioncode = a.group(1)
                #break

            a = p_icon.match(line)
            if a:
                app.path_to_icon = a.group(1)
                #break

            a = p_permission.match(line)
            if a:
                perm.id_app = app.id
                perm.id_perm = a.group(1)
                perm.insert()
                #break

        app.update()