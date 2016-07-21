# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

import sys

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

def getTestSteps(test_case):
    sql = "select name, rating, short_desc from experiment_test_steps where test_case=%s order by name;"
    cur.execute(sql,[test_case])
    rows = cur.fetchall()
    return rows

def getTestCases():
    sql = "select name from experiment_test_cases where name <> 'sol_arch' order by name ;"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def getRating(test_step):
    sql = "select rating, package, c2 from experiment_overview where test_step=%s order by package;"
    cur.execute(sql, [test_step])
    rows = cur.fetchall()
    return rows

def getSumRatings(test_case):
    sql = "select package, sum(rating) from experiment_overview where test_case=%s group by package order by package;"
    cur.execute(sql, [test_case])
    rows = cur.fetchall()
    return rows

def getSolArch():
    sql = "SELECT package, c1 FROM mhealth_apps.experiment_overview where test_case='sol_arch';"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows
