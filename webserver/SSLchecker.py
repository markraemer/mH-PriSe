"""
MK Jul 2016

queries SSLlabs.com for a complete check on a server SSL configuration
"""


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
    """
    requests SSLlabs check for all hosts on record for a specific package;
    results are written to the database
    :param package: the package to check all hosts for
    :return: None
    """

    logger.info("{} SSL analysis".format(package))
    hostnames = URL.getHostnamesByPackage(package)

    while len(hostnames) > 0:
        hostdb = URLSSL()
        hostname = hostnames.pop(0) # get first element from stack and check
        response = requests.get("https://api.ssllabs.com/api/v2/analyze", "host={}&fromCache=on&IgnoreMismatch=on&all=done".format(hostname)).json()
        if 'status' in response and response['status'] == "READY":

            logger.debug("{} -- {} SSL analysis done".format(package, hostname))
            hostdb.url = hostname
            try:
                rating = []
                for endpoint in response['endpoints']:
                    rating.append("{}:{}".format(endpoint['ipAddress'], endpoint['grade']))
                hostdb.rating = ", ".join(rating)
            except KeyError:
                hostdb.rating = "analysis failed"
            hostdb.reporturl = "https://www.ssllabs.com/ssltest/analyze.html?d={}".format(hostname)
            hostdb.upsert()
        else:
            hostnames.append(hostname) # not successful, so add element back to the stack
            logger.debug("{} -- {} SSL analysis waiting for result".format(package,hostname))


def do(context):
    """
    starts the check for a package; if no package specficied a new package is selected
    :param context: the runners context
    :return:
    """
    if not context.package:
        package = choosePackage()
        if package == "quit":
            return
    else:
        package = context.package
    check_for_package(package)

