#!/usr/bin/python
# KK, January 2015
# 
# The script produces finbug reports
# INPUT: apk files
# Output: findbugs report in xml


import os
import sys

sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *

#BASE_DIR = "/home/labits/svn/kk/twins/analysis/"
BASE_DIR= "/home/labits/svn/kk/twins/analysis/"
APK_DIR = "/home/labits/APKs/Twins/"
TMP_DIR = "/tmp/"

counter = 1
filenames = get_filenames()
f2p = filename2package()

##filenames = ["com.example.multinvers-2.apk", "com.bitdefender.clueful-1.apk"]
##f2p["com.example.multinvers-2.apk"]="mi"
##f2p["com.bitdefender.clueful-1.apk"]="bitdefender"

# Perform dex2jar for all APKs
for apk in filenames:

    f = f2p[apk]
     
    print
    print
    print
    print "Treating " + f + " which is " + str(counter) + " of " + str(len(filenames)) +" apps"
    counter += 1
    
    # move
    command = "cp '" + APK_DIR + apk + "' '" + TMP_DIR + f + ".zip'"
    print command
    s = os.system(command)
    print  command, " Status: ", s

    # unzip
    command = "unzip -o '" + TMP_DIR + f + "' -d '" + TMP_DIR + f + "'"
    s = os.system(command)
    print  command, " Status: ", s 

    # dex2jar
    command = "~/dex2jar-0.0.9.15/d2j-dex2jar.sh " + TMP_DIR + f + "/classes.dex -o " + TMP_DIR + f + "/classes.jar"
    s = os.system(command)
    print  command, " Status: ", s

    # findbugs
    command = "findbugs -xml '" + TMP_DIR + f + "/classes.jar' > '" + BASE_DIR + f + "/findbugs/findbugs.xml'"
    s = os.system(command)
    print  command, " Status: ", s
