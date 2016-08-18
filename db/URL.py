# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class URL():
    package = None
    url = None
    host = None
    hostname = None
    organization = None
    analysis = None
    time = None
    test_case = None


    def upsert(self):

        sql = []
        data = []

        if self.package is not None:
            data.append(self.package)
            sql.append("package=%s")
        if self.url is not None:
            data.append(self.url)
            sql.append("url=%s")
        if self.host is not None:
            data.append(self.host)
            sql.append("host=%s")
        if self.analysis is not None:
            data.append(self.analysis)
            sql.append("analysis=%s")
        if self.time is not None:
            data.append(self.time)
            sql.append("time=%s")
        if self.test_case is not None:
            data.append(self.test_case)
            sql.append("test_case=%s")
        if self.hostname is not None:
            data.append(self.hostname)
            sql.append("hostname=%s")
        if self.organization is not None:
            data.append(self.organization)
            sql.append("organization=%s")

        upsert = ["INSERT INTO urls SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(sql, tuple(data))

    @staticmethod
    def getHostnamesByPackage(package):
        sql = "select distinct hostname from urls where package=%s"
        data = [package]
        cur.execute(sql,data)
        query =  sql % tuple(data)

        logger.debug(query)
        rows = cur.fetchall()
        return [x[0] for x in rows]

    @staticmethod
    def getIps(package):
        sql = "select distinct host from urls where package=%s"
        data = [package]
        cur.execute(sql,data)
        query =  sql % tuple(data)

        logger.debug(query)
        rows = cur.fetchall()
        return [x[0] for x in rows]