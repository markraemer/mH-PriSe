#!/usr/bin/python
# KK, January 2015
# 
# The script produces androsim reports
# INPUT: apk files
# Output: findbugs report in xml


import os
import commands
import re
import sys
import time
import MySQLdb
##import dbconnect

BASE_DIR = "/home/labits/svn/kk/twins/analysis/"
APK_DIR = "/home/labits/APKs/Twins/"
TMP_DIR = "/tmp/"

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="Vot3Yes4Scotland", # your password
                      db="twins") # name of the data base

global cur
cur = db.cursor()
sql = "SELECT a.package, b.package \
        FROM pairs as p, apps as a, apps as b \
        WHERE p.p1 = a.id AND p.p2 = b.id \
        ORDER by p1"
# sql = "SELECT p1, p2 FROM pairs order by p1"
cur.execute(sql)
pairs = cur.fetchall()
counter = 1
for p in pairs:
    

    print
    print
    print
    print "Treating " + p[0] + " and " + p[1] + " which is " + str(counter) + " of " + str(len(pairs)) +" pairs"
    counter += 1
    
    # cd to androsim dir
    command = "cd /home/labits/androguard"
    s = os.system(command)
    print  command, " Status: ", s
    
    # androsim
    command = "python /home/labits/androguard/androdiff.py -i " + \
              APK_DIR + p[0] + "-1.apk " + APK_DIR + p[1] + "-1.apk > " \
              + BASE_DIR + p[0] + "/androsim/androsim.txt"
    s = os.system(command)
    print  command, " Status: ", s

    # cp result to other twins dir
    command = "cp " + BASE_DIR + p[0] + "/androsim/androsim.txt " + BASE_DIR + p[1] + "/androsim"
    s = os.system(command)
    print  command, " Status: ", s
