#!/usr/bin/python
# KK, January 2015

# The script downloads the pripol for each package name
# and stores the pripols data in the DB
# Sources: http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/

import sys
import urllib2
from bs4 import BeautifulSoup
sys.path.append("/home/labits/svn/kk")
from deprecated.db_functions import *

# Settings
ANALYSIS_DIR = "/home/labits/svn/kk/twins/analysis/" # dir where apks reside
#SMALI_DIR = "/home/labits/smali/"
RPDIR = "/tmp/"
#TEMPFILE = "/tmp/dummy_file_crypt"

##conn = MySQLdb.connect(host="localhost", user="root", passwd="Vot3Yes4Scotland", db='med_apps')
##c = conn.cursor()

# Get all packages
##sql = "SELECT package FROM apps ORDER BY package"
##c.execute(sql)
##p = []
##for pp in c.fetchall():
##        p.append(pp)

def strip_url(url):
    
    html = urllib2.urlopen(url, timeout = 5).read()
    #urllib2.urlopen("http://example.com", timeout = 1)
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # print(text)
    return text

def create_url_shortcut_text(p, url):
    return """    
    [Desktop Entry]
    Encoding=UTF-8
    Name=Pripol of %s
    Type=Link
    URL=%s
    Icon=text-html
    """ % (p, url)

def check_text(keyword, text):
        if keyword.upper() in text.upper():
            return 1
        else:
            return 0
def insert_db(package, url, http_code, privacyinHTML, P3PinHTML, NumWords, NumChars):
    sql = "INSERT INTO pripol (`package`, `URL`, `http_code`, `privacyinHTML`, `P3PinHTML`, `NumWords`, `NumChars`) \
            VALUES ('%s', '%s', %s, %s, %s, %s, %s)" % (package, url, http_code, privacyinHTML, P3PinHTML, NumWords, NumChars);
    
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

def insert_error_db(package, http_code):
    sql = "INSERT INTO pripol (`package`, `http_code`) \
            VALUES ('%s', %s)" % (package, http_code)
    
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

#################################################################



sql = "SELECT package, pripol FROM `gp` WHERE pripol != '' AND pripol !='None'\
        UNION SELECT package, pripol FROM `am` WHERE pripol != '' AND pripol !='None'"

        
c.execute(sql)
for url in c.fetchall():
    p = url[0]
    print
    print
    print "Dealing with " + p + " at '" + url[1] + "'"
    
##req = urllib2.Request('http://www.pretend_server.org')
##>>> try: urllib2.urlopen(req)
##... except URLError as e:
##...    print e.reason  



    print "Trying to open url"
    try:
#        response = urllib2.urlopen(url[1], timeout = 5)
        req = urllib2.Request(url[1], headers={ 'User-Agent': 'Mozilla/5.0' })
        response = urllib2.urlopen(req, timeout = 5)
    except urllib2.HTTPError as e:
        http_code = e.code
        print e
        insert_error_db(p, http_code)
        # print e.read() 
        continue
    except:
        insert_error_db(p, 444)
        # print e.read() 
        continue
    html = response.read()
    print "Get the length :", len(html)
    http_code = response.code
    print "This gets the code: ", response.code
    # print "Success"

    #open the entire file for writing
    print "Trying Download HTML to file: ", 
    file = ANALYSIS_DIR + p + "/pripol/pripol_g_orig_" + p + ".html"
    try:
        
        fh = open(file, "w")
        fh.write(html)
        fh.close()
        print "Success"
    except:
        print "Failure"
        continue
    
    # Write only text, no tags, no scripts
    file = ANALYSIS_DIR + p + "/pripol/pripol_g_plain_" + p + ".html"
    fh = open(file, "w")
    print "Trying Stripping of HTML: ", 
    try:
        text = strip_url(url[1])
        print "Length: " + str(len(text))
        fh.write(text.encode('utf-8'))
        print "Success"
    except:
        print "Failure"
    fh.close()

    # Write url
    file = ANALYSIS_DIR + p + "/pripol/url.desktop"
    print "Creating Shortcut: ", 
    fh = open(file, "w")
    try:
        
        fh.write(create_url_shortcut_text(p, url[1]))
        print "Success"
    except:
        print "Failure"
    fh.close()

        
    # database insert
    insert_db(p, url[1], http_code, check_text("privacy", html), check_text("P3P", html), len(text.split( )), len(text))
##
##    sql = "INSERT INTO pripol (`package`, `URL`, `http_code`, `privacyinHTML`, `P3PinHTML`, `NumWords`, `NumChars`) \
##            VALUES ('%s', '%s', %s, %s, %s, %s, %s);   
