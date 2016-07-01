# MK Jun 2016

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

    def insert(self):
        sql = "INSERT INTO pripol (package, URL, NumWords, NumChars, version, Country, AP, SSP," \
            "OP, PSP, IPP, intUsage, 3rdPartyStorage, Merger, 3rdPartyForward, quotes, comments)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        data_pripol = [self.package, self.URL, self.NumWords, self.NumChars, self.version, self.Country, self.AP, self.SSP, self.OP, self.PSP, self.IPP, self.intUsage, self.thirdPartyStorage, self.Merger, self.thirdPartyForward, self.quotes, self.comments]

        cur.execute(sql, data_pripol)