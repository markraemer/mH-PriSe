# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class ExperimentsDetails():


    experiment = None
    test_step = None
    comment = None
    rating = None

    def upsert(self):
        data=[]
        sql=[]

        if self.experiment is not None:
            data.append(self.experiment)
            sql.append("experiment=%s")
        if self.test_step is not None:
            data.append(self.test_step)
            sql.append("test_step=%s")
        if self.comment is not None:
            data.append(self.comment)
            sql.append("comment=%s")
        if self.rating is not None:
            data.append(self.rating)
            sql.append("rating=%s")

        upsert = ["INSERT INTO experiments_details SET", ", ".join(sql),"on duplicate key update", ", ".join(sql),";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query =  sql % tuple(data)

        logger.debug(query)
        cur.execute(sql, tuple(data))

    @staticmethod
    def getExpermimentDetails(experiment):
        sql = "SELECT * FROM experiments_details where experiment='{}' order by test_step;".format(experiment)
        cur.execute(sql)
        rows = list(cur.fetchall())
        field_names = [i[0] for i in cur.description]
        return rows, field_names

