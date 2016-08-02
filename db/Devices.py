# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Devices():
    id = None
    vendor = None
    model = None
    package = None
    type = None
    android = None
    ios = None
    windows = None
    plugin = None
    wifi = None
    bluetooth = None
    ant = None
    url = None
    short_url = None


    @staticmethod
    def getDevices(package):
        sql = "select id, vendor, model from devices where package=%s;"
        cur.execute(sql,[package])
        rows = cur.fetchall()
        return rows

    @staticmethod
    def getDevicesNames(idlist):
        sql = "select concat_ws(' ', vendor, model), package from devices where id in (%s) order by id;"
        list = ", ".join([str(id) for id in idlist])
        query = sql % list
        cur.execute(query)
        rows = cur.fetchall()
        return rows










