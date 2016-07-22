#!/usr/bin/python
# KK, December 2014

# The script extracts crypto classes from smale

import os
import sys

sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *
#sys.path.append("/home/labits/androguard")
#from androguard.core.bytecodes import apk
#from androguard.core.bytecodes import dvm
# from androguard.decompiler.dad import decompile

# Settings
APK_DIR = "/home/labits/APKs/Twins/" # dir where apks reside
SMALI_DIR = "/home/labits/smali/"
RPDIR = "/tmp/"
TEMPFILE = "/tmp/dummy_file_crypt"


##conn = MySQLdb.connect(host="localhost", user="root", passwd="Vot3Yes4Scotland", db='twins')
##c = conn.cursor()

##            print "Trying to execute " + sql
##            c.execute(sql)
##            conn.commit()
##            print 'Added an application to the database : {0}'.format(docid)       

def insert_classes(p, cc, keyword):
    # get id for package name
    c.execute("SELECT id FROM apps WHERE package = '%s';" % (p))
    s = c.fetchone()
    if s is None:
        print p + " does not exist in DB"
        return
##    else:
##        app_id = s[0]
    sql =  "INSERT INTO crypto (`package` , `class` , `keyword` ) VALUES \
            ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE package = '%s', class = '%s', keyword = '%s' " \
            % (p, cc, keyword, p, cc, keyword)
    print sql
    c.execute(sql)
    conn.commit()
    return

keywords = ["crypt", "passw",  "bouncycastle", "java/security", "ssl", "tls", "security", "random", "salt"]
    # "signature" produces too many hits


filenames = get_filenames()
f2p = filename2package()

for apk in filenames:

    p = f2p[apk]
    print "APK = " + apk, " ", p
    # p = apk.replace("-1.apk", "")
    
    # extract smali
    command = "apktool d '"+APK_DIR+apk+ "' " + SMALI_DIR + p
    try:
        os.system(command)
    except:
        print command + " FAILED"

    # grep smali code for URLs
    
       
    #ppath = p.split(".")
    #path = ppath[0]+"/"+ppath[1]
    for keyword in keywords:

        try:
            command1 = "rm " + TEMPFILE
            os.system(command1)
            command2 = "touch " + TEMPFILE
            os.system(command2)
        except:
            print "Error in " + command1 + " or " + command2

        command = "grep -r -i " + keyword + " " + SMALI_DIR + p + "/smali/* > " +  TEMPFILE
        try:
            os.system(command)
        except:
            print command + " FAILED"

        f = open(TEMPFILE, "r")
        for line in f:
            cl = line.split(":")
            cll = cl[0].split("/")
            del cll[-1]
            del cll[0]
            del cll[0]
            del cll[0]
            del cll[0]
            del cll[0]
            del cll[0]
           
            cc = ""
            for cs in cll:
                cc +=  cs + "/"
            print p, cc , keyword
            insert_classes(p, cc, keyword)
        f.close()
    

