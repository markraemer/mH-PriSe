#!/usr/bin/python
# KK, January 2015
# The script checks if an APK used Proguard obfuscation and outputs a probability

import re
import sys

sys.path.append("/home/labits/androguard")
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
# from androguard.decompiler.dad import decompile
from collections import defaultdict
sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *


# Loop over all methods and check if obfuscated
# score is number of obf. methods / all methods
def obfuscation_score(dct):
    # num_packages = len(dct)
    package_obfuscation_score = 0
    num_methods = 0
    num_obfuscated_methods = 0
    for c in dct: 
        # print "class = " + c
        num_methods += len(dct[c])
        # class_counter = 0
        for i in dct[c]: # loop over methods of class
            #print "Class = ", c, "Method = ",  i
            if len(i)<3 and re.match('[a-z]{1,2}', i):
                #print i, " Obfuscated"
                num_obfuscated_methods += 1
##            else:
##                print i, " Clear name"
        #class_obfuscation_score = class_counter/float(length) 
        #print "Obfuscation Score for package " + c + ": " + str(class_obfuscation_score)
        #package_obfuscation_score += class_obfuscation_score
    package_obfuscation_score =  num_obfuscated_methods / float(num_methods)
    #print "Total number of methods:", num_methods
    #print "Total number of obf. methods:", num_obfuscated_methods
    return package_obfuscation_score


##def native_obfuscation_score(dct, package):
##
##
##    length = len(dct[package])
##    class_counter = 0
##    for i in dct[package]:
##        # print "Class = " + i
##        if len(i)<3 and re.match('[a-z]{1,2}', i): class_counter += 1
##    class_obfuscation_score = class_counter/float(length) 
##    
##    return native_obfuscation_score

def insert_db(package, obf_score, obf_score_native):
    sql = "INSERT INTO obfuscation (package , obf_score , obf_score_native) \
            VALUES ('%s', %s, %s)" % (package, obf_score, obf_score_native)
    
    try:
        c.execute(sql)
        if DEBUG == 1: print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)
    return


# Settings
APK_DIR = "/home/labits/APKs/Twins/" # dir where apks reside

filenames = get_filenames()
f2p = filename2package()
counter = 1
# filenames = ["Wetter_3.2.5.apk", "com.kuriusgames.tractorcrew-1.apk", "SweetDrmzzz_1.0.apk", "Merry Larry_1.0.1.apk", "Christmas_1.5.apk"]
#for f in sorted(os.listdir(APK_DIR)):
for f in filenames:
    dct = defaultdict(list) # freh dict for each apk
    ndct = defaultdict(list) # freh dict for each apk
    
   
    # print "APK = " + f
    #package = f.replace("-1.apk", "")
    package = f2p[f]
    
    package = package.replace(".", "/")
    #print package
    print
    print
    print
    print str(counter) + " of " + str(len(filenames)) + ": Checking Obfuscation of file " + f + "/" + package
    counter += 1
    
    try:
        a = apk.APK(APK_DIR + f)
    except:
        print "Androguard Error. Skipping file."
        continue
    
    d = dvm.DalvikVMFormat(a.get_dex())
    dct = defaultdict(list)
##    for current_field in d.get_fields():
##        print current_field.get_name()
##    
    for current_class in d.get_classes():
        cl = current_class.get_name()
        # print cl
        cl = cl.strip(";")

        cl= cl.lstrip("L")

##        if cl==package:
##            native_obfuscation_score(dct, package)
        p = cl.split("/")
        cclass = p[-1]
        cl = "/".join(p[:-1])
        cl =  cl.strip(".")
        
        #print cl + " " +  cclass
        dct[cl].append(cclass)
    #print dct
    os = obfuscation_score(dct)
    print "Total Obfuscation score", os

    # now delete all non-native entries from dct and put them in ndct
    for i in dct:
        if package in i:
            print "IN" , i
            ndct[i] = dct[i]
            
##        else:
##            print "OUT", i
##            # del ndct[i]
    if len(ndct)>0:
        nos = obfuscation_score(ndct)
        
    else:
        nos = -1
    print "Native Obfuscation score", nos
    insert_db(f2p[f], os, nos)
