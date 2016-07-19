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

