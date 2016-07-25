# Load the jinja library's namespace into the current module.
import jinja2
import sys
import csv

from db.Certificates import Certificates
from db.AppDetails import AppDetails
from db.Pripol import Pripol
from db.AppPerm import AppPerm
from db import ExperimentsOverview

# initialize configuration parser
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.prop')
# get configuration parameter
path = config.get('tools','path.doc.tabledata')

whitelist = ["com.activ8rlives.mobile","com.hapiconnect","com.medm.medmwt.diary","com.stabxtom.thomson","com.withings.wiscale2"]

# In this case, we will load templates off the filesystem.
# This means we must construct a FileSystemLoader object.
#
# The search path can be used to make finding templates by
#   relative paths much easier.  In this case, we are using
#   absolute paths and thus set it to the filesystem root.
def generate_table(outfile, keys, name):
	templateLoader = jinja2.FileSystemLoader( searchpath="." )

	# An environment provides the data necessary to read and
	#   parse our templates.  We pass in the loader object here.
	templateEnv = jinja2.Environment( loader=templateLoader, variable_start_string='\VAR{',
					 variable_end_string='}')

	# This constant string specifies the template file we will use.
	TEMPLATE_FILE = "helper/templates/template_datatool_table.tex"

	# Read the template file using the environment object.
	# This also constructs our Template object.
	template = templateEnv.get_template( TEMPLATE_FILE )

	# Specify any input variables to the template as a dictionary.
	collayout = []
	[collayout.append("X") for i in range(0,len(keys),1)]
	collayout = "|".join(collayout)

	headers=[]
	[headers.append("\\bfseries " + header.replace("_", "")) for header in keys]
	headers = " & ".join(headers)

	colkeys = []
	[colkeys.append("\\" + colkey.replace("_", "") + "=" + colkey.replace("_", " ")) for colkey in keys]
	colkeys = ", ".join(colkeys)

	rowkeys = []
	[rowkeys.append("\\" + rowkey.replace("_", "")) for rowkey in keys]
	rowkeys = " & ".join(rowkeys)

	templateVars = {"caption":"", "col_layout":collayout, "headers":headers, "tablename":name, "colkeys":colkeys, "rowkeys":rowkeys}

	# Finally, process the template to produce our final text.
	outputText = template.render( templateVars )
	out = open(outfile,'w')
	out.write(outputText)
	out.close()


def permission():
    perms, keys = AppPerm.getAllPerm()
    rows, keys = AppPerm.getAppPerm()

    header = []
    for row in rows:
        if row[0] not in whitelist:
            continue
        header.append(row[0])
    header.insert(0, "permission")

    dict = {}
    for perm in perms:
        dict[perm[1]] = []
    for row in rows:
        if row[0] not in whitelist:
            continue
        for perm in perms:
            if perm[1] in row[1].split():
                dict[perm[1]].append('X')
            else:
                dict[perm[1]].append('-')

    f = open(path + "permissions.csv", 'wt')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(header)
        for i in dict.keys():
            dict[i].insert(0,i)
            writer.writerow(dict[i])
    finally:
        f.close()


def experiment_overview_export():

    cases = ExperimentsOverview.getTestCases()
    for case in cases:
        steps = ExperimentsOverview.getTestSteps(case[0])
        header = ["test step", "rating", "desc"]
        for package in whitelist:
            header.append(package)

        body={}
        for step in steps:
            body[step[0]] = []
            body[step[0]].extend([step[1], step[2]])
            ratings = ExperimentsOverview.getRating(step[0])
            for rating in ratings:
                if rating[1] in whitelist:
                    body[step[0]].append(rating[0])

        body['sum']=["",""]
        sums = ExperimentsOverview.getSumRatings(case[0])
        for sum in sums:
            if sum[0] in whitelist:
                body['sum'].append(str(sum[1]))

        # generate csv file
        f = open(path + case[0] +".csv", 'wt')
        try:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(header)
            for i in body.keys():
                body[i].insert(0, i)
                writer.writerow(body[i])
        finally:
            f.close()

        # generate latex template
        generate_table(path + case[0] + ".tex", header, case[0])



def do():
    permission()

    experiment_overview_export()

    rows, keys = Certificates.getCerts()
    generate_table(path + "certificates.tex", keys, "certificates")

    rows, keys = AppDetails.getDetails()
    generate_table(path + "app-details.tex", keys, "appdetails")

    rows, keys = Pripol.getDetails()
    generate_table(path + "pripol.tex", keys, "pripol")
