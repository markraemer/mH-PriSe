#!/usr/bin/python
# KK, Jan. 2015

# The script searches XML Findbugs reports and
# puts them in DB

import re
import sys

sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *

# Settings
APK_DIR = "/home/labits/APKs/Twins/" # dir where apks reside
#SMALI_DIR = "/home/labits/smali/"
#RPDIR = "/tmp/"
# TEMPFILE = "/tmp/dummy_file_URLS"
BASE_DIR = "/home/labits/svn/kk/twins/analysis/"
#BASE_DIR = "/tmp/"

### get all package name
##global packages
##sql = "SELECT package FROM apps ORDER BY package"
##cur.execute(sql)
##p = cur.fetchall()
packages = get_packages()


def db_insert_summary(r):

    sql = "INSERT INTO findbugs \
            (`package`, `total_classes`, total_size, `total_bugs`, `priority_2`, `priority_1`, \
            `native_total_bugs`, native_total_size, `native_priority_2`, `native_priority_1`) \
            VALUES ('%s', %s, %s, %s, %s, %s, %s, %s, %s, %s) \
            ON DUPLICATE KEY UPDATE package = '%s'"\
            % (r["package"], r["total_classes"], r["total_size"], r["total_bugs"], r["priority_2"], r["priority_1"],\
               r["native_total_bugs"], r["native_total_size"], r["native_priority_2"], r["native_priority_1"], r["package"])

    try:
        # Execute the SQL command
        c.execute(sql)
        # Commit your changes in the database
        print "Successfully executed: " + sql
        # cur.close()
    except:
        # Rollback in case there is any error
        conn.rollback()
        print "Something wrong" + sql
        # sys.exit(1)
    return

def db_insert_details(s):

    sql = "INSERT INTO findbugs_details \
            (`package`, `type`, `priority`, `abbrev`, `category`) \
            VALUES ('%s', '%s', %s, '%s', '%s') \
            ON DUPLICATE KEY UPDATE package = '%s'" \
            % (s["package"], s["type"], s["priority"], s["abbrev"], s["category"], s["package"])
    try:
        # Execute the SQL command
        c.execute(sql)
        conn.commit()
        # Commit your changes in the database
        # print "Successfully executed: " + sql
        # cur.close()
    except:
        # Rollback in case there is any error
        db.rollback()
        print "Something wrong" + sql
        # sys.exit(1)
    return

###################################################################
## Start main part
###################################################################
counter = 1
np = len(packages)

for p in packages:

    print counter, "/", np, "Dealing with " + p
    counter += 1  
    try:
        f = open(BASE_DIR + p + "/findbugs/findbugs.xml", "r")
    except:
        print "Could not open XML file."
        continue
        
    r = {}
    r["package"] = p
    r["native_total_bugs"] = -1
    r["native_priority_2"] = -1
    r["native_priority_1"] = -1
    r["total_types"] = -1
    r["total_size"] = -1
    r["native_total_size"] = -1
    r["total_classes"] = -1
    r["total_bugs"] = -1
    r["priority_1"] = -1
    r["priority_2"] = -1

    u = re.compile(".*<FindBugsSummary.*total_classes=\"(.*?)\" (.*)")
    #u = re.compile(".*<FindBugsSummary.*total_classes=\"(.*?)\".* total_bugs=\"(.*?)\" total_size=\"(.*?)\".*priority_2=\"(.*?)\" priority_1=\"(.*?)\"")
##  #  reg_exp = ".*<PackageStats package=\"" + p + "\" total_bugs=\"(.*?)\" total_types=\"(.*?)\" total_size=\"(.*?)\" priority_2=\"(.*?)\"(.*)"
    #    print reg_exp
    u2 = re.compile(".*<BugInstance type=\"(.*?)\" priority=\"(.*?)\" abbrev=\"(.*?)\" category=\"(.*?)\">")
    # u3 = re.compile(".*<PackageStats package=\"" + p + ".*\" total_bugs=.*")
    u3 = re.compile(".*<PackageStats package=\"" + p + "\" total_bugs=.*")    
    for line in f:
        s = {}
        s["package"] = p
        
        # print line
        ## Extract Summary Info
        
        url = u.match(line)
        if url:
            # print line
            r["total_classes"] = url.group(1)
            a = url.group(2)
            aa = a.split(" ")
            #print aa
            for p in aa:
                pp = p.split("=")
                v = pp[1].replace('\"', '')
                v = v.replace('>', '')

                r[pp[0]] = v
                
##            r["total_classes"] = url.group(1) # Needed to be fixed to includes apps with no prio 1 or 2 vulns
##            r["total_bugs"] = url.group(2)
##            r["total_size"] = url.group(3)
##            r["priority_2"] = url.group(4)
##            r["priority_1"] = url.group(5)
            # print r
            

        ## Extract Summary Native Findings:
        url3 = u3.match(line)
        
        if url3:
            print "Found native match: " + line
            parts = line.split(" ")
            for part in parts:
                subparts = part.split("=")
                if subparts[0].strip('"\n') == "total_bugs": r["native_total_bugs"] += int(subparts[1].strip('"\n>'))
                if subparts[0].strip('"\n') == "total_size": r["native_total_size"] += int(subparts[1].strip('"\n>'))
                if subparts[0].strip('"\n') == "priority_2": r["native_priority_2"] += int(subparts[1].strip('"\n>'))
                if subparts[0].strip('"\n') == "priority_1": r["native_priority_1"] += int(subparts[1].strip('"\n>'))

        
        url2 = u2.match(line)
        if url2:
            #print url2
            s["type"] = url2.group(1)
            s["priority"] = url2.group(2)
            s["abbrev"] = url2.group(3)
            s["category"] = url2.group(4)
            # print s
            db_insert_details(s)
            

    # print r
    #
    if len(r) > 0: db_insert_summary(r)
    else: print "Nothing found"
    
    f.close()
    # sys.exit(1)



## Summary Info
##<FindBugsSummary timestamp="Tue, 13 Jan 2015 11:41:33 +0000" total_classes="1215" referenced_classes="1491"
##total_bugs="298" total_size="43280" num_packages="88" vm_version="24.65-b04"
##cpu_seconds="87.20" clock_seconds="28.38" peak_mbytes="416.60" alloc_mbytes="682.75" gc_seconds="1.47" priority_2="227" priority_1="71">

## Native FIndings:    
##<PackageStats package="com.bloodpressure.record.log.AR" total_bugs="28" total_types="69" total_size="2242" priority_2="21" priority_1="7">

## Individual Findings:
##<BugInstance type="NP_NULL_ON_SOME_PATH" priority="1" abbrev="NP" category="CORRECTNESS">



