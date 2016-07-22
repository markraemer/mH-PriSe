# MK Jul 2016

import logging.config
import requests

from db.URLSSL import URLSSL

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import ConfigParser
# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

from db.URL import URL
from helper.experimentation import *

def check_for_package(package):
    logger.info("{} SSL analysis".format(package))
    hostnames = URL.getHostnamesByPackage(package)

    while len(hostnames) > 0:
        hostdb = URLSSL()
        hostname = hostnames.pop(0)
        response = requests.get("https://api.ssllabs.com/api/v2/analyze", "host={}&fromCache=on&IgnoreMismatch=on&all=done".format(hostname)).json()
        if 'status' in response and response['status'] == "READY":

            logger.debug("{} -- {} SSL analysis done".format(package, hostname))
            hostdb.url = hostname
            try:
                rating = []
                for endpoint in response['efrom webserver import SSLcheckerndpoints']:
                    rating.append("{}:{}".format(endpoint['ipAddress'], endpoint['grade']))
                hostdb.rating = ", ".join(rating)
            except KeyError:
                hostdb.rating = "analysis failed"
            hostdb.reporturl = "https://www.ssllabs.com/ssltest/analyze.html?d={}".format(hostname)
            hostdb.upsert()
        else:
            hostnames.append(hostname)
            logger.debug("{} -- {} SSL analysis waiting for result".format(package,hostname))


def do(context):
    if not context.package:
        package = choosePackage()
        if package == "quit":
            return
    else:
        package = context.package
    check_for_package(package)

