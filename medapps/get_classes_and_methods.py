#!/usr/bin/python
# KK, December 2014

# The script extracts the permissions from APK and stores them in DB

import os
import commands
import re
import MySQLdb
import sys
import datetime
sys.path.append("/home/labits/androguard")
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
# from androguard.decompiler.dad import decompile
from collections import defaultdict


# Settings
APK_DIR = "/home/labits/APKs/Test/" # dir where apks reside


##conn = MySQLdb.connect(host="localhost", user="root", passwd="Vot3Yes4Scotland", db='med_apps')
##c = conn.cursor()

##            print "Trying to execute " + sql
##            c.execute(sql)
##            conn.commit()
##            print 'Added an application to the database : {0}'.format(docid)       

##def insert_classes(p, cl, keyword):
##    # get id for package name
##    c.execute("SELECT id FROM apps WHERE package = '%s';" % (p))
##    s = c.fetchone()
##    if s is None:
##        print p + " does not exist in DB"
##        return
####    else:
####        app_id = s[0]
##    sql =  "INSERT INTO `med_apps`.`crypto` (`package` , `class` , `keyword` ) VALUES \
##            ('%s', '%s', '%s') ON DUPLICATE KEY UPDATE package = '%s', class = '%s', keyword = '%s' " \
##            % (p, cl, keyword, p, cl, keyword)
##    # print sql
##    c.execute(sql)
##    conn.commit()
##    return

# keywords = ["crypt", "passw", "signat", "bouncycastle", "java/security", "ssl", "tls", "security", "random", "salt"]

dct = defaultdict(list)

for f in sorted(os.listdir(APK_DIR)):
    p=f.replace("-1.apk", "")
    print "APK = " + p
    a = apk.APK(APK_DIR + f)
   
    d = dvm.DalvikVMFormat(a.get_dex())
    obf = {}
##    for current_field in d.get_fields():
##        print current_field.get_name()
##    
    for current_class in d.get_classes():
        cl = current_class.get_name()
        
        cl = cl.strip(";")
        p = cl.split("/")
        cclass = p[-1]
        cl = cl.strip(cclass)
        cl =  cl.strip("/")
        
        print cl + " " +  cclass
        dct(cl).append(cclass)
#        print cl
##        for keyword in keywords:
##            if keyword.lower() in cl.lower():
##                print keyword, "usage in \t", p, "\t", cl
##                insert_classes(p, cl,j/ keyword)
##                if p in cl.replace("/", "."):
##                    print "USAGE OF NATIVE CRYPTO/Password"


