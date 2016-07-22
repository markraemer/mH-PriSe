import lxml
from lxml.html import builder as E
from lxml import etree
from db.Apps import Apps
from db.Addons import Addons
from db.AppDetails import AppDetails
from db.AppPerm import AppPerm
from db.Certificates import Certificates
from db.Experiments import Experiments
from db.ExperimentsDetails import ExperimentsDetails

def print_single(parent, row, fields):
    r1 = etree.SubElement(parent, "tr")
    r2 = etree.SubElement(parent, "tr")
    for i in range(0, len(row), 1):
        c1 = etree.SubElement(r1, "td")
        b = etree.SubElement(c1, "b")
        b.text = str(fields[i])
        c2 = etree.SubElement(r2, "td")
        c2.text = str(row[i])

def print_multi(parent, rows, fields):
    adr = []
    adr.append(etree.SubElement(parent, "tr"))
    for i in range(0, len(fields), 1):
        c1 = etree.SubElement(adr[0], "td")
        b = etree.SubElement(c1, "b")
        b.text = str(fields[i])

    for i in range(0, len(rows), 1):
        adr.append(etree.SubElement(parent, "tr"))
        for j in range(0, len(fields), 1):
            c2 = etree.SubElement(adr[i + 1], "td")
            pre = etree.SubElement(c2, "pre")
            pre.text = str(rows[i][j])


package = "com.activ8rlives.mobile"

html = etree.Element("html")
body = etree.SubElement(html, "body")


row, fields = Apps.getRow(package)
app = etree.SubElement(body, "table")
print_single(app,row,fields)




rows, fields = AppDetails.getDetails(package)
details = etree.SubElement(body, "table")
print_multi(details,rows,fields)


rows, fields = Addons.getAddons(package)
addons = etree.SubElement(body, "table")
print_multi(addons,rows,fields)

rows, fields = AppPerm.getPerm(package)
perm = etree.SubElement(body, "table")
print_multi(perm,rows,fields)

rows, fields = Certificates.getCerts(package)
cert = etree.SubElement(body, "table")
print_multi(cert,rows,fields)


rows, fields = Experiments.getExperiments(package)
for i in range (0, len(rows), 1):
    exp = etree.SubElement(body, "table")
    print_single(exp,rows[i],fields)

    r, f = ExperimentsDetails.getExpermimentDetails(rows[i][0])
    det = etree.SubElement(exp, "table")
    print_multi(det, r, f)



lxml.html.open_in_browser(html)
