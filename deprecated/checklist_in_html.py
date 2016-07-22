#!/usr/bin/python
# The scripts prints out all the details about an app
# on a HTML site and allow input of data over HTML form
# in database

import MySQLdb
import sys
import pprint
import os
import string
from mod_python import apache

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="Vot3Yes4Scotland", # your password
                      db="twins") # name of the data base

global cur
cur = db.cursor()

def get_icon_name(apk):
    sql = "SELECT path_to_icon FROM apps WHERE package = '" + apk + "'"
    cur.execute(sql)
    data = cur.fetchall()
    if len(data)>0:
        d = data[0]
        d=d[0].split("/")
        return d[-1]
    else:
        return -1

global apk

###################################################
apk = "com.alt12.pinkpadfree"
###################################################



path_to_files = "/home/labits/svn/kk/twins/analysis/"
icon = get_icon_name(apk)
try:
    command = "cp " + path_to_files + apk + "/" + icon + " /var/www/py/pix/"+icon
    os.system(command)
except:
    print "Error in copying icon"
    print apk
    print icon

def check_status(apk):
    sql = "SELECT * FROM analysis WHERE package LIKE '" + apk + "'"
    cur.execute(sql)
    data = cur.fetchall()
    if len(data) == 1:
        return "UPDATE"
    else:
        return "INSERT"


# Check if package has already been analyzed
def check_analzed(apk):
    sql    = "SELECT * FROM analysis WHERE package = '" + apk + "'" 
    cur.execute(sql)
    data = cur.fetchall()
    if len(data)>0:
        return 1
    else:
        return 0

def base_info(apk):
    sql = "SELECT id, package, label, version, versioncode FROM apps WHERE package = '" + apk + "'" 
    cur.execute(sql)
    data = cur.fetchall()
    return data

def gp(apk):
        sql = "SELECT pripol, numDownload, creator, avRating, price FROM gp WHERE package = '" + apk + "'" 
        cur.execute(sql)
        data = cur.fetchall()
        return data


def cert_details(apk):
    sql = "SELECT cert_sig_algo, cert_issuer, cert_subject, cert_pkl FROM certificates WHERE package = '" + apk + "'" 
    cur.execute(sql)
    return cur.fetchall()

def permissions(apk):
    sql = "SELECT p.name \
        FROM permissions as p, apps as a, app_perm as ap \
        WHERE a.package = '%s' AND a.id = ap.id_app AND ap.id_perm = p.id" % (apk)
    cur.execute(sql)
    perms = "<ul>"
    for p in cur.fetchall():
        perms += "<li>" + p[0] + "</li>"
    perms +="</ul>"
    return perms

def addons(apk):
    sql = "SELECT name, addon_type  FROM `addons` WHERE `package` LIKE '%s'" % (apk)
    cur.execute(sql)
    perms = "<ul>"
    for p in cur.fetchall():
        perms += "<li>" + p[0] + " <==>  " + p[1] + "</li>"
    perms +="</ul>"
    return perms

def crypto_usage(apk):
    sql = "SELECT class, keyword FROM crypto WHERE `package` LIKE '%s'" % (apk)
    cur.execute(sql)
    perms = "<ul>"
    for p in cur.fetchall():
        perms += "<li>" + p[0] + " <==>  " + p[1] + "</li>"
    perms +="</ul>"
    return perms

def urls(apk):
    sql = "SELECT url FROM urls WHERE package = '" + apk + "'" 
    cur.execute(sql)
    return cur.fetchall()
        
def make_radio(name, text, d):
    r = "<B>"+text+"</B>"
    for k in d:
        r += "<INPUT type='radio' name='" + name + "' value='" + d[k] + "'>" + k
    r += "<BR>"
    return r

def make_text_input(name, text):
    r = "<B>"+text+"</B>"
    r += "<textarea cols=80 rows=20 name='" + name + "'></textarea>"
    return r
    
def make_form():
    form = "<FORM value='form' action='index2.py/store_data' method='post'>"
    t = {"DIABETES": "DIAB", "BLOOD PRESSURE": "BP", "BOTH": "BOTH"}
    form += make_radio("type", "What is the type of the app", t)
    bb = {"Yes": "1", "No": "0", "NA": "2"}
    b = {"Yes": "1", "No": "0"}
    form += make_radio("safety_check_bp", "BP > 200 / 120 possible", bb)
    form += make_radio("safety_check_gl", "Glucose > 111 possible", bb)
    form += make_radio("safety_check_pulse", "Pulse > 333 possible", bb)
    form += make_radio("export_SD", "Export to SD card possible", b)
    form += "<BR>Path to exports on SD card<input type='text' name='path_to_exports'><BR>"
    form += make_radio("export_mail", "Export to Mail possible", b)
    form += make_radio("export_web_native", "Export to Web account possible", b)
    form += "<BR>Export to others<input type='text' name='export_other'><BR>"
 
    form += make_radio("authentication", "Authentication to app provided", b)
    form += make_radio("wipe", "Wipe of data provided", b)
    form += make_radio("pripol_in_app", "Link or Statement of pripol given in app", b)
    form += make_text_input("comment", "General Comments")
    form += "<INPUT type='submit' value='Send'> <INPUT type='reset'></P></FORM>"
    return form

def index2():
    analyzedtext = ""
    if check_analzed(apk)==1:
        analyzedtext = "<FONT COLOR='RED'>App has already been analyted</FONT>"
    return """
<html><head>
<title>Privacy Analysis four %s</title>
</head>
<body>
<Table>
<TR>
<TD>
<H1>Base data for %s</H1>
<H2>Image</H2>
<IMG SRC = '%s'>
<A HREF='https://play.google.com/store/apps/details?id=%s'>Link to Google Play</A>
<H2>Data from APK file</H2>
id, package, label, version, versioncode<BR>
%s
<H2>Data from Google Play</H2>
pripol, numDownload, creator, avRating, price<BR>
%s
<H2>Permissions</H2>
%s
<H2>Addons</H2>
%s
<H2>Certificate Details</H2>
cert_sig_algo, cert_issuer, cert_subject, cert_pkl<BR>
%s
<H2>Crypto Code in APK</H2>
%s
<H2>URLS</H2>
%s
</TD>
<TD>
%s
%s
</TD>
</TR><TABLE>
</body>
</html>
""" %(apk, apk, "pix/"+icon, apk, str(base_info(apk)), str(gp(apk)), permissions(apk), addons(apk), str(cert_details(apk)), crypto_usage(apk), urls(apk), analyzedtext, make_form())


def store_data(req): 

    info = req.form
    status = check_status(apk)
    if status == "INSERT":

        sql = "INSERT INTO `analysis`(`package`, `Type`, `pripol_in_app`, `path_to_exports`, `safety_check_bp`, \
                `safety_check_gl`, `safety_check_pulse`, `export_SD`, `export_mail`, \
                `export_web_native`, `export_other`, `authentication`, `wipe`, `comment`) VALUES \
                ('%s', '%s', %s, '%s', %s, \
                %s, %s, %s,  %s, %s, \
                '%s', %s, %s, '%s') "\
                % (apk, info['type'], info['pripol_in_app'], info['path_to_exports'], info['safety_check_bp'], \
                 info['safety_check_gl'], info['safety_check_pulse'], info['export_SD'], info['export_mail'], \
                 info['export_web_native'], info['export_other'], info['authentication'], info['wipe'], info['comment'])
    else:
        sql = "UPDATE `analysis` SET `Type` = '%s', `pripol_in_app` = %s, `path_to_exports` = '%s', `safety_check_bp` = %s, \
                `safety_check_gl` = %s, `safety_check_pulse` = %s, `export_SD` = %s, `export_mail` = %s, \
                `export_web_native` = %s, `export_other` = '%s', `authentication` = %s, `wipe` = %s , `comment` = '%s' \
                WHERE package = '%s'"\
                 % (info['type'], info['pripol_in_app'], info['path_to_exports'], info['safety_check_bp'], \
                 info['safety_check_gl'], info['safety_check_pulse'], info['export_SD'], info['export_mail'], \
                 info['export_web_native'], info['export_other'], info['authentication'], info['wipe'], info['comment'], apk    )    
    cur.execute(sql)
    db.commit()
    return """
<html><head>
<title>Results</title>
</head>
<body>
<h1>Data for %s</h1>
<hr><br>
Your Data %s has been received and is stored in DB.<br>
SQL = %s
<BR>
<BR>
<a HREF='../index2.py'>Next entry</A>
</body>
</html>
""" %(apk, str(info), sql)
        
