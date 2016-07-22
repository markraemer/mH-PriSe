#!/usr/bin/python
# KK, November 2014

# The script extracts the app title, version and icon for
# all apps in a given apk dir
# and puts them in a HTML file and in analysis dir

import os
import re
import sys
import zipfile

##sys.path.append("./HTML.py-0.04")
##import HTML
import datetime
sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *

# Settings
APK_DIR = "/home/labits/APKs/Twins/" # dir where apks reside
RPDIR = "/tmp/" # home/labits/svn/kk/medical/" # dir where list and pix will be stored in new html dir
os.system("mkdir -p "+RPDIR+"/html")
ANALYSIS_DIR = "/home/labits/svn/kk/twins/analysis/"

counter = 0

# t = HTML.Table(header_row=['Title',   'Package Name',   'File Name', 'VersionName', 'VersionCode', 'Icon'])
# t = HTML.Table(header_row=['Title',   'Package Name', 'VersionCode', 'Icon'])
t = "Test"
filenames = get_filenames()
f2p = filename2package()

for apk in filenames:
# for apk in sorted(os.listdir(APK_DIR)):
    
    print "APK = " + apk
    p = f2p[apk]
    
    f = open(RPDIR + "dummy_file", "w")
    
    command = "aapt dump badging '" + APK_DIR+apk + "' > " + RPDIR + "dummy_file"
    print command
    os.system(command)

    # apk = apk.replace(" ", "_")
    f.close()
    f = open(RPDIR + "dummy_file", "r")

    for line in f:
            # print line    
            p_packagename = re.compile("package: name='(.*?)'.*")
            p_versionname = re.compile(".*versionName='(.*?)'.*")
            p_versioncode = re.compile(".*versionCode='(.*?)'.*")
            p_label= re.compile("application-label:'(.*?)'.*")
            p_icon = re.compile("application.*icon='(.*?)'.*")

            if "debuggable" in line:
                print "DEBUG FLAG set for " + apk + "!!!"
            if "intent" in line:
                print "INTENT FILTER used in " + apk + "!!!"
                
            a = p_packagename.match(line)
            if a:
                packagename = a.group(1)
                #print "Packagename = " + packagename
                
            a = p_versionname.match(line)
            if a:
                versionname = a.group(1)
                #print "Versionname = " + versionname

            a = p_versioncode.match(line)
            if a:
                versioncode = a.group(1)
                #print "Version Code = " + versioncode

            a = p_label.match(line)
            if a:
                label = a.group(1)
                #print "Label= " + label

            a = p_icon.match(line)
            if a:
                icon = a.group(1)
                #print "Icon = " + icon

    # Make directory
    command = "mkdir -p '"+RPDIR+"html/" + apk + "'"
    out = os.system(command)
    print out, command

    with zipfile.ZipFile(APK_DIR + apk) as z:
        print z, "xxx", os.path.basename(icon)
        with open(os.path.join(RPDIR+"html/"+apk+"/", os.path.basename(icon)), 'wb') as ff:
            ff.write(z.read(icon))
    ff.close

    # This part copies icon in analysis dir
    command = "cp " + RPDIR + "html/" + apk +"/* " + ANALYSIS_DIR + p + "/"
    # command = "cp " + RPDIR + "html/" + apk +"/* " + ANALYSIS_DIR + apk.replace("-1.apk", "") + "/"
    # command = "cp '" + RPDIR + "html/" + apk +"/" + os.path.basename(icon)+ "' " + ANALYSIS_DIR + "icon" + str(counter) + ".png"
    out = os.system(command)
    print out, command
    
 
    pixs = icon.split("/")
    print pixs
    pix =  "<img src='" + apk + "/" + pixs[-1] +"'  height='42' width='42'>" 

    if counter % 2 == 0:
        color = "Silver"
    else:
        color = "White"
    counter += 1
    
##    colored_cell = HTML.TableCell(' ', bgcolor=color)
##    # t.rows.append([colorname, colored_cell])
##    t.rows.append([HTML.TableCell(label, bgcolor=color), \
##                   HTML.TableCell(packagename, bgcolor=color), \
##                   # HTML.TableCell(apk, bgcolor=color), \
##                   HTML.TableCell(versionname, bgcolor=color), \
##                   # HTML.TableCell(versioncode, bgcolor=color), \
##                   pix])
    
    f.close()

now = datetime.datetime.now()
# t.rows.append(["List Generated: ", now])

htmlcode = str(t)
g = open(RPDIR+"html/list.html","w")
# print htmlcode
g.write(htmlcode)
g.close()
