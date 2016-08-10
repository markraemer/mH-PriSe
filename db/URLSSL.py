# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class URLSSL():
    url = None
    rating = None
    reporturl = None
    timestamp = None


    def upsert(self):

        sql = []
        data = []

        if self.url is not None:
            data.append(self.url)
            sql.append("url=%s")
        if self.rating is not None:
            data.append(self.rating)
            sql.append("rating=%s")
        if self.reporturl is not None:
            data.append(self.reporturl)
            sql.append("report_url=%s")
        if self.timestamp is not None:
            data.append(self.timestamp)
            sql.append("timestamp=%s")

        upsert = ["INSERT INTO urls_ssl SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(sql, tuple(data))

    @staticmethod
    def get_rating(package):
        sql = """SELECT distinct u.hostname, s.rating FROM urls u join urls_ssl s on u.hostname = s.url where u.package=%s;"""
        cur.execute(sql,[package])
        rows = cur.fetchall()
        return rows

