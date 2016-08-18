"""
holds functions for traffic analysis of MITMproxy and tShark
captured files

MK Jul 2016
"""

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from helper.experimentation import *

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import mitm_extractURLs
from db.URL import URL
from db.Location import Location


def analysePCAP(context):
    """
    extracts IP addresses from tShark captured files to complement results from MITMproxy analysis
    while MITMproxy only covers HTTP traffic tShark includes TCP based connections
    IP addresses captured by tShark but not MITMproxy will be printed out on console
    :param context: the runners context
    :return:
    """
    if not context.package:
        package = choosePackage()
        if package == "quit":
            return
    else:
        package = context.package
    device = chooseDevice(package)
    record, index = select_recorded_experiment(package, device)
    print record
    if record:
        exp = Experiments()
        exp.id = record[0]
        exp.package = record[1]
        exp.time = record[2]
        exp.test_case = record[3]
        exp.log_folder = record[4]
        logger.info("%s %s %s analyzing", record[0], record[1], record[2])
        logger.debug("%s extracting IPs from pcap", record[0])
        # get all IPs in DB
        ips = URL.getIps(exp.package)

        # rename file - otherwise not working on ubuntu
        command = ["mv", exp.log_folder + "/tshark.pncap", exp.log_folder + "/tshark.pcap"]
        cmd = " ".join(command)
        os.system(cmd)

        # filter by IP address
        command = ["tcpdump", "-r", exp.log_folder + "/tshark.pcap","-w", exp.log_folder + "/tshark-filtered.pcap","'src 10.0.0.35 or dst 10.0.0.35'"]
        cmd = " ".join(command)
        logger.debug(cmd)
        os.system(cmd)

        # filter by IP address
        command = ["tshark", "-r", exp.log_folder + "/tshark-filtered.pcap", "-Y \"tcp.flags==2\" -T fields -e ip.dst |  sort |  uniq |  awk '{printf(\"%s\\n\",$1)}' > dummy.txt"]
        cmd = " ".join(command)
        logger.debug(cmd)
        os.system(cmd)

        with open("dummy.txt") as out:
            iplist = [line.rstrip('\n') for line in out]


            for ip in iplist:

                if ip is not "" and ip not in ips:
                    logger.debug("location ip {}".format(ip))
                    location = Location.getIP(ip)
                    if location is None:
                        mitm_extractURLs.getIpLocation(ip)
                        location = Location.getIP(ip)
                    logger.info("{} {}".format(ip, location))
                else:
                    logger.info("{} {}".format(ip, " already on record"))



def extractURLs(exp):
    """
    extracts IP addresses recorded for a specific experiment run
    calls MITMproxy with custom script to extract and save them
    :param exp: the experiment run to analyse
    :return:
    """
    command = ["mitmdump", "-q", "-ns", "\"traffic/mitm_extractURLs.py", exp.package, exp.test_case, "'" + str(exp.time) + "'" + "\"", "-r", "\"" + exp.log_folder + "/mitm.out\"", "-w", "/dev/null"]
    cmd = " ".join(command)
    logger.debug(cmd)
    os.system(cmd)

def prep_generate_map(exp):
    """
    loads ips from database to generate traffic map
    :param exp: the experiment to generate map for
    :return:
    """
    logger.info("%s generating traffic map", exp.package)
    rows = Location.getCoordinates(exp.test_case, exp.package, exp.time)
    lats = [float(x[0]) for x in rows]
    longs = [float(x[1]) for x in rows]
    generate_map(exp.log_folder + "/traffic-map.png", lats, longs)


def generate_map(output, lats=[], lons=[], wesn=None):
    """
    creates a traffic map for a specific experiment
    :param output:
    :param lats:
    :param lons:
    :param wesn:
    :return:
    """
    "see http://matplotlib.org/basemap/users/examples.html"
    m = Basemap(llcrnrlon=-180., llcrnrlat=-60., urcrnrlon=190., urcrnrlat=80., \
                rsphere=(6378137.00, 6356752.3142), \
                resolution='l', projection='merc', \
                lat_0=40., lon_0=-20., lat_ts=20.)

    for i in range(0, len(lats), 1):
        centerlat = 55.95
        centerlon = -3.2
        m.drawgreatcircle(lons[i], lats[i], centerlon, centerlat, linewidth=2, color='b')

    m.drawcoastlines()
    m.fillcontinents()
    m.drawparallels(np.arange(-60, 90, 20))
    m.drawmeridians(np.arange(-200, 200, 30))
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

def do(createMap=False):
    experimentLog = Experiments.getExperimentLog()
    for log in experimentLog:
        exp = Experiments()
        exp.package = log[0]
        exp.time = log[1]
        exp.test_case = log[2]
        exp.log_folder = log[3]
        logger.info("%s %s %s analyzing", log[0], log[1], log[2])
        logger.debug("%s extracting URLs", log[0])
        extractURLs(exp)
        if createMap:
            prep_generate_map(exp)

def for_rec_experiment(context, createMap=False):
    if not context.package:
        package = choosePackage()
        if package == "quit":
            return
    else:
        package = context.package
    device = chooseDevice(package)
    record, index = select_recorded_experiment(package,device)
    print record
    if record:
        exp = Experiments()
        exp.id = record[0]
        exp.package = record[1]
        exp.time = record[2]
        exp.test_case = record[3]
        exp.log_folder = record[4]
        logger.info("%s %s %s analyzing", record[0], record[1], record[2])
        logger.debug("%s extracting URLs", record[0])
        extractURLs(exp)
        if createMap:
            prep_generate_map(exp)


