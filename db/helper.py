# MK Jun 2016
# helper class for DB

import MySQLdb
import ConfigParser

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

# connect to database
db = MySQLdb.connect(host=config.get('db','db.host'),
                     user=config.get('db','db.user'),
                      passwd=config.get('db','db.passwd'),
                      db=config.get('db','db.name'))

#cursor for db queries
global cur
cur = db.cursor()
db.autocommit(True)

