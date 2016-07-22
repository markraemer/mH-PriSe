# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class AppDetails():

    package = None
    title = None
    version = None
    asin = None
    category = None
    company = None
    price = None
    rating = None
    popularity = None
    release_date = None
    mom = None
    pripol = None
    timestamp = None

    def upsert(self):
        data=[]
        sql=[]
        if self.package is not None:
            data.append(self.package)
            sql.append("package=%s")
        if self.title is not None:
            data.append(self.title.encode("UTF-8"))
            sql.append("title=%s")
        if self.version is not None:
            data.append(self.version)
            sql.append("version=%s")
        if self.asin is not None:
            data.append(self.asin)
            sql.append("asin=%s")
        if self.category is not None:
            data.append(self.category)
            sql.append("category=%s")
        if self.company is not None:
            data.append(self.company)
            sql.append("company=%s")
        if self.price is not None:
            data.append(self.price)
            sql.append("price=%s")
        if self.rating is not None:
            data.append(self.rating)
            sql.append("rating=%s")
        if self.popularity is not None:
            data.append(self.popularity)
            sql.append("popularity=%s")
        if self.release_date is not None:
            data.append(self.release_date)
            sql.append("release_date=%s")
        if self.mom is not None:
            data.append(self.mom)
            sql.append("mom=%s")
        if self.pripol is not None:
            data.append(self.pripol)
            sql.append("pripol=%s")

        upsert = ["INSERT INTO am SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(sql, tuple(data))

    @staticmethod
    def getDetails(package):
        sql = "SELECT * FROM am where package=%s;"
        cur.execute(sql, [package])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names

    @staticmethod
    def getDetails():
        sql = "SELECT * FROM am;"
        cur.execute(sql, [])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names