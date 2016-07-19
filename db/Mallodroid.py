# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Mallodroid():
    package = None
    mallo_text = None
    vuln_in = None
    vuln_package = None

    def upsert(self):
        data = []
        sql = []
        if self.package is not None:
            data.append(self.package)
            sql.append("package='%s'")
        if self.mallo_text is not None:
            data.append(self.mallo_text)
            sql.append("mallo_text='%s'")
        if self.vuln_in is not None:
            data.append(self.vuln_in)
            sql.append("vuln_in='%s'")
        if self.vuln_package is not None:
            data.append(self.vuln_package)
            sql.append("vuln_package='%s'")

        upsert = ["INSERT INTO mallodroid SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(query)

    @classmethod
    def getPackages(cls):
        sql = "select distinct package from mallodroid;"
        cur.execute(sql)
        rows = cur.fetchall()
        return [x[0] for x in rows]