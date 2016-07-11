#!/usr/bin/python
# KK, December 2014

# The script extracts the permissions from APK and stores them in DB

import sys

sys.path.append("/home/labits/androguard")
from androguard.core.bytecodes import apk

sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *
# from androguard.decompiler.dad import decompile

# Settings
APK_DIR = "/home/labits/APKs/Twins/" # dir where apks reside

counter = 1
filenames = get_filenames()
f2p = filename2package()

##conn = MySQLdb.connect(host="localhost", user="root", passwd="Vot3Yes4Scotland", db='twins')
##c = conn.cursor()
# No changes from here necessary

##            print "Trying to execute " + sql
##            c.execute(sql)
##            conn.commit()
##            print 'Added an application to the database : {0}'.format(docid)       
def insert_perms(permissions, apk):
    # get id for package name
    c.execute("SELECT id FROM apps WHERE package = '%s';" % (apk))
    s = c.fetchone()
    if s is None:
        print apk + " does not exist in DB"
        return
    else:
        app_id = s[0]
    for perm in permissions:
        c.execute("SELECT * FROM permissions WHERE name='%s';" % (perm))
        if c.fetchone() is None:
                c.execute("INSERT INTO permissions (name) VALUES (%s);", (perm))
                # print 'Add a permission to the database : {0} '.format(perm)
        c.execute("SELECT id FROM permissions WHERE name='%s';" % (perm))
        id_perm = c.fetchone()[0]
        sql = "SELECT * FROM app_perm WHERE id_app=%s AND id_perm=%s;" % (app_id, id_perm)
        c.execute(sql)
        s = c.fetchone()
        if (s is None):
                c.execute("INSERT INTO app_perm VALUES (%s, %s);", (app_id, id_perm))
                # print 'Add a permission to the database : {0} for the version :{2} of the application {1}'.format(perm, docid, version)
    conn.commit()
    return

for file in filenames:
    package = f2p[file]
    print "APK = " + package
    a = apk.APK(APK_DIR + file)
    # vm = dvm.DalvikVMFormat(open("myfile.dex", "r").read())
    # vmx = analysis.VMAnalysis(vm)

    # print a.get_permissions()
    # package = file.replace("-1.apk", "")
    insert_perms(a.get_permissions(), package)
    # show_Path(d, dx.tainted_packages.search_crypto_packages())

