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
    sql = "select rating, package, device, c2 from experiment_overview where test_step=%s order by device;"
    cur.execute(sql, [test_step])
    rows = cur.fetchall()
    return rows

def getTestCaseComments(test_case):
    sql = "select e.package, d.id, concat_ws(' ', d.vendor, d.model), group_concat(e.comment separator '\n') from experiments e join devices d on e.device = d.id where e.test_case=%s group by e.device order by e.device;"
    cur.execute(sql, [test_case])
    rows = cur.fetchall()
    return rows

def getSumRatings(test_case):
    sql = "select package, device, IFNULL(sum(rating),0) from experiment_overview where test_case=%s group by device,package order by device,package;"
    cur.execute(sql, [test_case])
    rows = cur.fetchall()
    return rows

def getSolArch():
    sql = "SELECT d.package, concat_ws(' ', d.vendor, d.model), e.c1 FROM mhealth_apps.experiment_overview e join devices d on e.device=d.id where e.test_case='sol_arch' order by e.device;"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows
