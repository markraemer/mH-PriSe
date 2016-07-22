#!/usr/bin/python
# KK, December 2014
# The script extracts certificate infos out of the APK file and stores it in DB

import os
import commands
import re
import MySQLdb
import sys
import datetime
import fnmatch
import time

# Settings
APK_DIR = "/home/labits/APKs/Twins/" # dir where apks reside
ANAL_DIR = "/home/labits/svn/kk/twins/analysis/" # where to store files
RPDIR = "/tmp" # dir where list and pix will be stored in new html dir
conn = MySQLdb.connect(host="localhost", user="root", passwd="Vot3Yes4Scotland", db='twins') # use correct db
# Do not change from here on 

c = conn.cursor()
conn.autocommit(True)


 
def put_in_db(r):
    sql = "INSERT INTO certificates \
            (package, cert_version,  \
            cert_sig_algo, cert_issuer, \
            cert_subject, cert_nb, cert_na, \
            cert_pka, cert_pkl, cert_sn) VALUES ('%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s') \
            ON DUPLICATE KEY UPDATE\
            cert_version = %s, \
            cert_sig_algo = '%s', \
            cert_issuer = '%s', \
            cert_subject= '%s', \
            cert_nb = '%s', \
            cert_na = '%s', \
            cert_pka = '%s', \
            cert_pkl = %s ,\
            cert_sn = '%s', \
            package = '%s'" \
            % (r["package"], r["cert_version"], r["cert_sig_algo"], r["cert_issuer"], \
               r["cert_subject"], r["cert_nb"], r["cert_na"], \
                r["cert_pka"], r["cert_pkl"], r["cert_sn"], \
               r["cert_version"], r["cert_sig_algo"], r["cert_issuer"], \
                r["cert_subject"], r["cert_nb"], r["cert_na"], \
                r["cert_pka"], r["cert_pkl"], r["cert_sn"], r["package"])
    # print sql
    try:
        c.execute(sql)
        print "SUCCESS !!! " + sql
    except:
        print "Something wrong" + sql
        sys.exit(1)    

    return



# get all package name
# global packages
sql = "SELECT package, filename FROM apps ORDER BY package"
c.execute(sql)
p = c.fetchall()

    
for index in range(len(p)):
    package = p[index][0]
    apk = p[index][1]

    r = {}
    r.setdefault("cert_version", None)

    # time.sleep(2)    
    print
    print
    print "Filename = " + apk
    command = "mkdir -p '/tmp/" + apk + "'"
    s = os.system(command)
    print "Status = ", s, command
    command = "unzip -o '"+APK_DIR +apk+"' -d '/tmp/" + apk + "/'"
    try:
        s = os.system(command)
        print "Status = ", s, command
    except:
        print command
        print "Error unzipping. Skipping this app"
        continue
    f_name = ""
    for file in os.listdir("/tmp/" + apk +"/META-INF/"):
        if fnmatch.fnmatch(file, '*.RSA'):
            f_name = file
##            # copy RSA file to ANAL_DIR
##            command = "cp '/tmp/" + apk +"/META-INF/" + f_name + "' " + ANAL_DIR + package
##            s = os.system(command)
##            print "Status = ", s, command

    if len(f_name)==0:
        print("No CERT File found")
        continue

    command = "openssl pkcs7 -in '/tmp/" + apk + "/META-INF/"+f_name+"' -inform DER -print_certs | openssl x509 -text -noout > /tmp/temp_cert"
    s = os.system(command)
    print "Status = ", s, command
    f = open("/tmp/temp_cert", "r")
    for line in f:
            # print line    
            p_v = re.compile(".*Version: (.*) \(")
            p_sa = re.compile(".*Signature Algorithm: (.*)")
            p_issuer = re.compile(".*Issuer: (.*)")
            p_subj = re.compile(".*Subject: (.*)")
            p_nb= re.compile(".*Not Before: (.*)")
            p_na = re.compile(".*Not After : (.*)")
            p_pka = re.compile(".*Public Key Algorithm: (.*)")
            p_pkl = re.compile(".*Public-Key: \((.*) bit")
            p_sn = re.compile(".*Serial Number: (.*)")
            a= p_v.match(line)
            if a: r["cert_version"]=a.group(1) 
            a= p_sa.match(line)
            if a: r["cert_sig_algo"]=a.group(1)
            a= p_issuer.match(line)
            if a: r["cert_issuer"]=a.group(1)
            a= p_subj.match(line)
            if a: r["cert_subject"]=a.group(1)
            a= p_nb.match(line)
            if a: r["cert_nb"]=a.group(1)
            a= p_na.match(line)
            if a: r["cert_na"]=a.group(1)
            a= p_pka.match(line)
            if a: r["cert_pka"]=a.group(1)
            a= p_pkl.match(line)
            if a: r["cert_pkl"]=a.group(1)
            a= p_sn.match(line)
            if a: r["cert_sn"]=a.group(1)
    r["package"]=package
    print r
    put_in_db(r)
    f.close()
    # copy RSA file to ANAL_DIR
    command = "cp /tmp/temp_cert " + ANAL_DIR + package
    s = os.system(command)
    print "Status = ", s, command
    
c.close()
       
            

    
