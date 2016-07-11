#!/usr/bin/python
# KK, February 2015
# The script gets APKs out of DB and stores them in file system
import os
import sys

sys.path.append("/home/labits/androguard")
# from androguard.decompiler.dad import decompile
sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *

SOURCE_DIR = "/home/labits/APKs/Twins/"

TARGET_DIR = "/tmp/twins/"

def get_filenames():
    sql = "SELECT filename FROM `apps` WHERE kind like '%pair%'"
    try:
        c.execute(sql)
        if DEBUG == 1: print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)    
    packages = []
    for p in c.fetchall():
        packages.append(p[0])
    if DEBUG == 1: print "Found " + str(len(packages)) + " packages."
    return packages

def get_packages():
    sql = "SELECT package FROM `apps` WHERE kind like '%pair%'"
    try:
        c.execute(sql)
        if DEBUG == 1: print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)    
    packages = []
    for p in c.fetchall():
        packages.append(p[0])
    if DEBUG == 1: print "Found " + str(len(packages)) + " packages."
    return packages



filenames = get_filenames()

for f in filenames:
    # copy apks in TARGET_DIR
    command = "cp '" + SOURCE_DIR+f + "'  '" + TARGET_DIR + f + "'"
    s = os.system(command)
    print  command, " Status: ", s
    # Install on device - connect before
    command = "adb install '" + TARGET_DIR + f + "'"
    s = os.system(command)
    print  command, " Status: ",  s

# packages = get_packages()

##for p in packages:
##    # Uninstall
##    command = "adb uninstall '" + p + "'"
##    s = os.system(command)
##    print  command, " Status: ", s
