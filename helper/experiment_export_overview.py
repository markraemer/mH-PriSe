# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from db import ExperimentsOverview

import pdfkit
from lxml import etree
from StringIO import *
from db.Devices import Devices
import ConfigParser
# initialize configuration parser
config = ConfigParser.RawConfigParser()
config.read('config.prop')

doc_folder = config.get("export","doc.folder")


devices = [1,2,5,6,9,10]

packages = ["com.activ8rlives.mobile", "com.hapiconnect",
            "com.medm.medmwt.diary", "com.stabxtom.thomson", "com.withings.wiscale2"]


packages.sort()


import os
path = os.path.dirname(os.path.abspath(__file__))

def create_doc(file_name, details=False):
    doctype = "<!DOCTYPE html><html></html>"
    tree = etree.parse(StringIO(doctype))
    header = etree.SubElement(tree.getroot(), "head")

    if details:
        meta = etree.SubElement(header, "meta")
        meta.set("name","pdfkit-orientation")
        meta.set("content", "Landscape")

    link = etree.SubElement(header, "link")
    link.set("rel","stylesheet")
    link.set("href", "../helper/style.css")
    body = etree.SubElement(tree.getroot(), "body")
    script = etree.SubElement(body, "script")
    script.set("src", "https://s3-us-west-2.amazonaws.com/s.cdpn.io/3/modernizr-2.7.1.js")


    cases = ExperimentsOverview.getTestCases()

    for case in cases:
        if details:
            table = etree.SubElement(body, "table")
            table.set("class", "table")
            table.set("width", "1024px")
            caption = etree.SubElement(table,"caption")
            h1 = etree.SubElement(caption, "h1")
            h1.text = case[0]
            thead = etree.SubElement(table, "thead")
            comments = ExperimentsOverview.getTestCaseComments(case[0])

            tr = etree.SubElement(thead, "tr")
            th = etree.SubElement(tr, "th")
            th.text = "device"
            br = etree.SubElement(th,"br")
            br.tail = "package"
            th = etree.SubElement(tr, "th")
            th.text = "comment"
            for comment in comments:
                if int(comment[1]) in devices:
                    tr = etree.SubElement(table, "tr")
                    th = etree.SubElement(tr, "th")
                    th.text = comment[2]
                    br = etree.SubElement(th, "br")
                    br.tail = comment[0]
                    th.set("class","row-header")
                    td = etree.SubElement(tr, "td")
                    td.text = comment[3]

        table = etree.SubElement(body, "table")
        if not details:
            table.set("class","table table-header-rotated")
        else:
            table.set("class", "table")
        caption = etree.SubElement(table,"caption")
        h1 = etree.SubElement(caption, "h1")
        h1.text = case[0]
        thead = etree.SubElement(table, "thead")
        steps = ExperimentsOverview.getTestSteps(case[0])
        tr = etree.SubElement(thead, "tr")
        th = etree.SubElement(tr, "th")
        th.text = "test step"
        th = etree.SubElement(tr, "th")
        th.text = "rating"
        th.set("width", "200px")
        th = etree.SubElement(tr, "th")
        th.text = "desc"
        th.set("width", "200px")
        devicenames = Devices.getDevicesNames(devices)
        for device in devicenames:
            th = etree.SubElement(tr, "th")
            div = etree.SubElement(th, "div")
            span = etree.SubElement(div, "span")
            span.text = device[0]
            br = etree.SubElement(span, "br")
            br.tail = device[1]
            th.set("class","rotate")
        tbody = etree.SubElement(table, "tbody")
        for step in steps:
            tr = etree.SubElement(tbody, "tr")
            th = etree.SubElement(tr, "th")
            th.text = step[0]
            th.set("class","row-header")
            td2 = etree.SubElement(tr, "td")
            td2.text = step[1]
            td2.set("style", "font-size: small;")
            td3 = etree.SubElement(tr, "td")
            td3.text = step[2]
            td3.set("style", "font-size: small;")
            ratings = ExperimentsOverview.getRating(step[0])
            for rating in ratings:
                if int(rating[2]) in devices:
                    td = etree.SubElement(tr, "td")
                    td.set("style", "font-size: small;text-align: left; vertical-align: top;")
                    p = etree.SubElement(td, "p")
                    p.set("style","font-style: bold;")
                    p.text = rating[0]
                    if details:
                        p2 = etree.SubElement(td, "p")
                        p2.text = rating[3]


        # add sums
        tr = etree.SubElement(tbody, "tr")
        td = etree.SubElement(tr, "td")
        td = etree.SubElement(tr, "td")
        td = etree.SubElement(tr, "td")
        sums = ExperimentsOverview.getSumRatings(case[0])
        for sum in sums:
            if int(sum[1]) in devices:
                td = etree.SubElement(tr, "td")
                td.text = str(sum[2])



    h1 = etree.SubElement(body,"h1")
    h1.text = "sol_arch"

    table = etree.SubElement(body, "table")
    table.set("border","1 px")
    table.set("width", "1024px")
    comments = ExperimentsOverview.getSolArch()
    tr = etree.SubElement(table, "tr")
    td = etree.SubElement(tr, "td")
    td.text = "device\npackage"
    td2 = etree.SubElement(tr, "td")
    td2.text = "comment"
    for comment in comments:
        tr = etree.SubElement(table, "tr")
        td = etree.SubElement(tr, "td")
        td.text = comment[0]
        br = etree.SubElement(td, "br")
        br.tail = comment[1]
        td2 = etree.SubElement(tr, "td")
        td2.text = comment[2]

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'orientation': 'Landscape'
    }

    file = open("doc/{}.html".format(file_name),'w')
    tree.write(file, pretty_print=True, encoding="us-ascii", xml_declaration=None, method="html")
    pdfkit.from_file("doc/{}.html".format(file_name),"doc/{}.pdf".format(file_name), options=options)


def do():
    create_doc("overview",False)
    create_doc("details", True)