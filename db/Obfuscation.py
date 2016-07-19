# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Obfuscation():
    package = None
    score = None
    native_score = None
    time = None

    def insert(self):
        data = []
        sql = []
        if self.package is not None:
            data.append(self.package)
            sql.append("package='%s'")
        if self.score is not None:
            data.append(self.score)
            sql.append("score='%s'")
        if self.native_score is not None:
            data.append(self.native_score)
            sql.append("native_score='%s'")
        if self.time is not None:
            data.append(self.time)
            sql.append("time='%s'")

        upsert = ["INSERT INTO obfuscation SET", ", ".join(sql), "on duplicate key update", ", ".join(sql), ";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query = sql % tuple(data)

        logger.debug(query)
        cur.execute(query)

    @classmethod
    def getPackages(cls):
        sql = "select distinct package from obfuscation;"
        cur.execute(sql)
        rows = cur.fetchall()
        return [x[0] for x in rows]
