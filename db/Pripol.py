# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Pripol():
    package = None
    URL = None
    NumWords = 0
    NumChars = 0
    version = None
    Country = None
    AP = None
    SSP = None
    OP = None
    PSP = None
    IPP = None
    intUsage = None
    thirdPartyStorage = None
    Merger = None
    thirdPartyForward = None
    quotes = None
    comments = None

    def upsert(self):

        sql = []
        data = []
        if self.package is not None:

            data.append(self.package)
            sql.append("package= '%s' ")
        if self.URL is not None:

            data.append(self.URL)
            sql.append("URL=  '%s' ")
        if self.NumWords <> 0:

            data.append(self.NumWords)
            sql.append("NumWords=  '%s' ")
        if self.NumChars <> 0:

            data.append(self.NumChars)
            sql.append("NumChars=  '%s' ")
        if self.version is not None:

            data.append(self.version)
            sql.append("version=  '%s' ")
        if self.Country is not None:

            data.append(self.Country)
            sql.append("Country=  '%s' ")
        if self.AP is not None:

            data.append(self.AP)
            sql.append("AP=  '%s' ")
        if self.SSP is not None:

            data.append(self.SSP)
            sql.append("SSP=  '%s' ")
        if self.OP is not None:

            data.append(self.OP)
            sql.append("OP=  '%s' ")
        if self.PSP is not None:

            data.append(self.PSP)
            sql.append("PSP=  '%s' ")
        if self.IPP is not None:

            data.append(self.IPP)
            sql.append("IPP=  '%s' ")
        if self.intUsage is not None:

            data.append(self.intUsage)
            sql.append("intUsage=  '%s' ")
        if self.thirdPartyStorage is not None:

            data.append(self.thirdPartyStorage)
            sql.append("3rdPartyStorage=  '%s' ")
        if self.Merger is not None:

            data.append(self.Merger)
            sql.append("Merger=  '%s' ")
        if self.thirdPartyForward is not None:

            data.append(self.thirdPartyForward)
            sql.append("3rdPartyForward=  '%s' ")
        if self.quotes is not None:

            data.append(self.quotes)
            sql.append("quotes=  '%s' ")
        if self.comments is not None:

            data.append(self.comments)
            sql.append("comments=  '%s' ")

        upsert = ["INSERT INTO pripol SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(query)

    @staticmethod
    def getDetails():
        sql = "SELECT * FROM pripol;"
        cur.execute(sql, [])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names