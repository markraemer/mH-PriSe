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
    def getStepsForCase(test_case):
        sql = "select name from experiment_test_steps where test_case='{}';".format(test_case)
        cur.execute(sql)
        rows = cur.fetchall()
        return [x[0] for x in rows]

