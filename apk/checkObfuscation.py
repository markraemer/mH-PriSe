#!/usr/bin/python
# KK, January 2015
# MK Jul 2016
# The script checks if an APK used Proguard obfuscation and outputs a probability


from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
# from androguard.decompiler.dad import decompile
from collections import defaultdict

from db.Apps import Apps
from db.Obfuscation import Obfuscation

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import re

# initialize configuration parser
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.prop')



####
# Loop over all methods and check if obfuscated
# score is number of obf. methods / all methods
####
def obfuscation_score(dct):

    # num_packages = len(dct)
    package_obfuscation_score = 0
    num_methods = 0
    num_obfuscated_methods = 0
    for c in dct:
        # print "class = " + c
        num_methods += len(dct[c])
        # class_counter = 0
        for i in dct[c]:  # loop over methods of class
            # print "Class = ", c, "Method = ",  i
            if len(i) < 3 and re.match('[a-z]{1,2}', i):
                # print i, " Obfuscated"
                num_obfuscated_methods += 1
                ##            else:
                ##                print i, " Clear name"
                # class_obfuscation_score = class_counter/float(length)
                # print "Obfuscation Score for package " + c + ": " + str(class_obfuscation_score)
                # package_obfuscation_score += class_obfuscation_score
    package_obfuscation_score = num_obfuscated_methods / float(num_methods)
    # print "Total number of methods:", num_methods
    # print "Total number of obf. methods:", num_obfuscated_methods
    return package_obfuscation_score



def do():
    apps = Apps.getAllApps()
    #f2p = filename2package()

    counter = 1


    for app in apps:
        obf = Obfuscation()
        obf.package = app[0]
        dct = defaultdict(list)  # freh dict for each apk
        ndct = defaultdict(list)  # freh dict for each apk
        app[0] = app[0].replace(".", "/")

        logger.info(str(counter) + " of " + str(len(apps)) + ": Checking Obfuscation of file " + app[1])
        counter += 1

        try:
            a = apk.APK(app[1])
        except:
            print "Androguard Error. Skipping file."
            continue

        d = dvm.DalvikVMFormat(a.get_dex())
        dct = defaultdict(list)

        for current_class in d.get_classes():
            cl = current_class.get_name()
            # print cl
            cl = cl.strip(";")

            cl = cl.lstrip("L")


            p = cl.split("/")
            cclass = p[-1]
            cl = "/".join(p[:-1])
            cl = cl.strip(".")

            # print cl + " " +  cclass
            dct[cl].append(cclass)
        # print dct
        os = obfuscation_score(dct)
        logger.info("Total Obfuscation score " + os)

        # now delete all non-native entries from dct and put them in ndct
        for i in dct:
            if app[0] in i:
                print "IN", i
                ndct[i] = dct[i]

        if len(ndct) > 0:
            nos = obfuscation_score(ndct)

        else:
            nos = -1
        logger.info("Native Obfuscation score" + nos)
        obf.native_score = nos
        obf.score = os
        obf.insert()
