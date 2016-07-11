# This script stores common database operations

import sys
import MySQLdb

global DEBUG
DEBUG = 1
global c, conn
conn = MySQLdb.connect(host="localhost", \
                       user="root", \
                       passwd="Vot3Yes4Scotland", \
                       db='twins') # use correct db
c = conn.cursor()
conn.autocommit(True)


# get all package name
# global packages
def get_packages():
    sql = "SELECT package FROM apps ORDER BY package"
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

def get_filenames():
    sql = "SELECT filename FROM apps ORDER BY package"
    try:
        c.execute(sql)
        if DEBUG == 1: print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)    
    filenames = []
    for p in c.fetchall():
        filenames.append(p[0])
    if DEBUG == 1: print "Found " + str(len(filenames)) + " filenames."
    return filenames

def package2filename():
    sql = "SELECT package, filename FROM apps ORDER BY package"
    try:
        c.execute(sql)
        if DEBUG == 1: print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)    
    p2f = {}
    for p in c.fetchall():
        p2f[p[0]]=p[1]
    return p2f

def filename2package():
    sql = "SELECT package, filename FROM apps ORDER BY package"
    try:
        c.execute(sql)
        if DEBUG == 1: print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)    
    f2p = {}
    for f in c.fetchall():
        f2p[f[1]]=f[0]
    return f2p


