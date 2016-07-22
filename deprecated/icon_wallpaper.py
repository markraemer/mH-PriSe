#!/usr/bin/python
# KK, November 2014

# The script extracts the app icon 
# all apps in a given apk dir
# and creates a nice HTML table
# Prerequisite: Icons must be availbale
# => USe extract_title_version_pix_from_APK-Dir.py


import os
import commands
import re
import zipfile
import sys
#sys.path.append("./HTML.py-0.04")
#import HTML
import datetime

# Settings
APK_DIR = "/home/labits/APKs/top/" # dir where apks reside
RPDIR = "/tmp/" # home/labits/svn/kk/medical/" # dir where list and pix will be stored in new html dir
os.system("mkdir -p "+RPDIR+"/html")
# ANALYSIS_DIR = "/home/labits/svn/kk/medical/analysis/"

counter = 0

#t = HTML.Table(header_row=['Title',   'Package Name',   'File Name', 'VersionName', 'VersionCode', 'Icon'])
##
##for apk in sorted(os.listdir(APK_DIR)):
##    p = apk.replace("-1.apk", "")
##
##    command = "cp " + ANALYSIS_DIR + p + "/*.png /tmp/icons/" + str(counter)+ ".png"
##    out = commands.getstatusoutput(command)
##    print out, command
##    counter += 1

    
t = "<HTML><HEAD></HEAD>"
pix = []
for i in os.listdir("/tmp/icons/"):
    pix.append("/tmp/icons/" + i)

#print pix

t += "<TABLE>"
count = 0
for x in range(5):
    t += "<TR>"
    for y in range(4):
        print x,y
        t += "<TD><img src='" + pix[count] +"'  height='50' width='50'></TD>" 
    
        count += 1
    t += "</TR>"
t += "</TABLE></BODY></HTML>"

f= open("/tmp/wallpaper.html", "w")
f.write(t)
f.close()
        
