"""
this script is read by mimtproxy and will write information about the recorded requests into the database
"""
import json
import os
import requests
import sys

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path + "/../")
sys.path.insert(0,path + "/../")

from db.URL import URL
from db.Location import Location
import ConfigParser
# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

def start(ctx, argv):
    global package, test_case, time, payload_map
    package = argv[1]
    test_case = argv[2]
    time = argv[3]
    payload_map = {}

    print package


def getIpLocation(ip):
    loc = Location()
    loc.ip_address = ip
    #jsondata = requests.get(config.get("traffic","traffic.ipdatabase.url") + ip).json()
    jsondata = requests.get("http://ipinfo.io/" + ip).json()
    loc.city = jsondata['city']
    loc.country_code = jsondata['country']
    loc.lat = jsondata['loc'].split(',')[0]
    loc.long = jsondata['loc'].split(',')[1]
    if 'region' in jsondata:
        loc.state = jsondata['region']
    if 'postal' in jsondata:
        loc.zip_code = jsondata['postal']
    loc.upsert()
    return jsondata['org']


def request(ctx, flow):
    url = URL()
    url.organization = getIpLocation(flow.request.host)
    url.package=package
    url.analysis="d"
    url.host=flow.request.host # ip address
    url.url=flow.request.url
    url.test_case = test_case
    url.time = time
    if 'host' in flow.request.headers:
        url.hostname = flow.request.headers['host'] # host name
    url.upsert()
    if url.host not in payload_map.keys():
        payload_map[url.host]=[]
    payload_map[url.host].append(len(flow.request.content))

def response(ctx, flow):
    if flow.repsonse.host not in payload_map.keys():
        payload_map[flow.repsonse.host]=[]
    payload_map[flow.repsonse.host].append(len(flow.response.body))


def done(ctx):
    f = open('workfile.out', 'w')
    for host in payload_map.keys():
        sum = 0
        for msg_len in payload_map[host]:
            sum = sum + msg_len
        f.write("{} {}\n".format(host,sum))
    f.close()