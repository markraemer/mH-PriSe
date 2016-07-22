# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class TestSteps():
    name = None
    order = None
    test_case = None
    short_desc = None
    rating = None
    long_desc = None

    @staticmethod
    def getByName(name):
        sql = "select ts.name, ts.test_case, ts.short_desc, ts.long_desc, ts.rating from experiment_test_steps ts where name = '{}';".format(name)
        cur.execute(sql)
        row = cur.fetchone()
        ts = TestSteps()
        ts.name = row[0]
        ts.test_case = row[1]
        ts.short_desc = row[2]
        ts.long_desc = row[3]
        ts.rating = row[4]
        return ts

    @staticmethod
    def getStepsForCase(test_case):
        sql = "select name from experiment_test_steps where test_case='{}';".format(test_case)
        cur.execute(sql)
        rows = cur.fetchall()
        return [x[0] for x in rows]



