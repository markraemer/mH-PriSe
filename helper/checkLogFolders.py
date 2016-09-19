# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')


import ConfigParser
# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')
deviceId = config.get("dev","dev.adb.id")

import os
from db.Experiments import Experiments

def doAll():

    experiments = Experiments.getExperimentLog()
    for experiment in experiments:
        if not os.path.exists(experiment[3]):
            print experiment
