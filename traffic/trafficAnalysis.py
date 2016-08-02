# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from db.Location import Location

from helper.experimentation import *

# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

# extract URLs and run script which will insert them into database
def extractURLs(exp):
    print exp
    command = ["mitmdump", "-q", "-ns", "\"traffic/mitm_extractURLs.py", exp.package, exp.test_case, "'" + str(exp.time) + "'" + "\"", "-r", "\"" + exp.log_folder + "/mitm.out\"", "-w", "/dev/null"]
    cmd = " ".join(command)
    logger.debug(cmd)
    os.system(cmd)

def prep_generate_map(exp):
    logger.info("%s generating traffic map", exp.package)
    rows = Location.getCoordinates(exp.test_case, exp.package, exp.time)
    lats = [float(x[0]) for x in rows]
    longs = [float(x[1]) for x in rows]
    generate_map(exp.log_folder + "/traffic-map.png", lats, longs)

def generate_map(output, lats=[], lons=[], wesn=None):
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
    m.drawparallels(np.arange(-60, 90, 20), labels=[1, 1, 0, 1])
    m.drawmeridians(np.arange(-200, 200, 30), labels=[1, 1, 0, 1])
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


