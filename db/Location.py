# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Location():
    ip_address = None
    country_code = None
    state = None
    city = None
    zip_code = None
    long = 0.0
    lat = 0.0

    def upsert(self):
        data=[]
        sql=[]
        if self.ip_address is not None:
            data.append(self.ip_address)
            sql.append("ip_address=%s")
        if self.country_code is not None:
            data.append(self.country_code)
            sql.append("country_code=%s")
        if self.state is not None:
            data.append(self.state)
            sql.append("state=%s")
        if self.city is not None:
            data.append(self.city)
            sql.append("city=%s")
        if self.zip_code is not None:
            data.append(self.zip_code)
            sql.append("zip_code=%s")
        if self.long is not None:
            data.append(self.long)
            sql.append("log=%s")
        if self.lat is not None:
            data.append(self.lat)
            sql.append("lat=%s")

        upsert = ["INSERT INTO location SET", ", ".join(sql), "on duplicate key update", ", ".join(sql), ";"]
        data.extend(copy(data))
        sql = " ".join(upsert)

        query = sql % tuple(data)
        logger.debug(query)
        cur.execute(sql, tuple(data))
        self.id = cur.lastrowid

    @staticmethod
    def getCoordinates(testcase, package, time):
        sql = "SELECT DISTINCT location.lat, location.log FROM urls inner join location on urls.host = location.ip_address where urls.test_case=%s and urls.package=%s and urls.time=%s;"
        data = (testcase, package, time)

        logger.debug(sql.format(data))
        cur.execute(sql, data)
        rows = cur.fetchall()
        return rows

    @staticmethod
    def getIP(ip):
        sql = "SELECT concat_ws(', ', country_code, state, city, zip_code) FROM location where ip_address='%s';"
        data = (ip)

        logger.debug(sql % data)
        cur.execute(sql % data)
        rows = cur.fetchone()
        return rows