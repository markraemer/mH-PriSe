# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Experiments():

    id = None
    package = None
    time = None
    test_case = None
    comment = None
    log_folder = None

    def upsert(self):
        data = []
        sql = []

        if self.package is not None:
            data.append(self.package)
            sql.append("package='%s'")
        if self.time is not None:
            data.append(self.time)
            sql.append("time='%s'")
        if self.test_case is not None:
            data.append(self.test_case)
            sql.append("test_case='%s'")
        if self.comment is not None:
            data.append(self.comment)
            sql.append("comment='%s'")
        if self.log_folder is not None:
            data.append(self.log_folder)
            sql.append("log_folder='%s'")

        upsert = ["INSERT INTO experiments SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(query)
        self.id = cur.lastrowid

    @classmethod
    def getExperimentLog(cls):
        sql = "SELECT package, time, test_case, log_folder FROM experiments;"
        cur.execute(sql)
        rows = cur.fetchall()
        return rows