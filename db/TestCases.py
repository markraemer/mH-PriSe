# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class TestCases():
    name = None
    short_desc = None
    long_desc = None

    @classmethod
    def getCases(self):
        sql = "select name from experiment_test_cases;"
        cur.execute(sql)
        rows = cur.fetchall()
        return [x[0] for x in rows]