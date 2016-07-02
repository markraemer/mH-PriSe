# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from mallodroid import mallodroid
from db.Apps import Apps
from db.Mallodroid import Mallodroid

from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.decompiler.dad import decompile
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.bytecodes.apk import APK
from androguard.core.analysis.analysis import uVMAnalysis
from androguard.core.analysis.ganalysis import GVMAnalysis

from bs4 import BeautifulSoup
from multiprocessing import Process





import os

# this is based on mallodroid coding and simplified
def runMallodroid(app):
    assert isinstance(app, Apps), "app is not type Apps: %r" % app
    logger.info("%s running Mallodroid ", app.package)
    _a = apk.APK(app.path_to_apk)

    _vm = dvm.DalvikVMFormat(_a.get_dex())
    _vmx = uVMAnalysis(_vm)

    if 'android.permission.INTERNET' in _vmx.get_permissions([]):
        logger.debug('%s requires INTERNET permission. Continue analysis', app.package)


        _vm.create_python_export()
        _gx = GVMAnalysis(_vmx, None)

        _vm.set_vmanalysis(_vmx)
        _vm.set_gvmanalysis(_gx)
        _vm.create_dref(_vmx)
        _vm.create_xref(_vmx)

        _result = {'trustmanager': [], 'hostnameverifier': [], 'onreceivedsslerror': []}
        _result = mallodroid._check_all(_vm, _vmx, _gx)

        try:
            return mallodroid._xml_result(_a, _result)
        except TypeError:
            logger.error("error .. proceeding")
        #    print "Store decompiled Java code in {:s}".format(_args.dir)
        #   _store_java(_vm, _args)

    else:
        logger.info("%s does not require INTERNET permission. No need to worry about SSL misuse... Abort!", app.package)

def parseXML(xml, app):
    mallo = Mallodroid()

    doc = BeautifulSoup(xml, "xml")


    trustmanager = doc.trustmanagers.find("trustmanager")
    if trustmanager:
        mallo.package = app.package
        for m in doc.trustmanagers.find_all("trustmanager"):
            mallo.mallo_text = m
            mallo.vuln_package = m.xref['class']
            if (mallo.vuln_package).startswith(app.package):
                mallo.vuln_in = 1
            else:
                mallo.vuln_in = 2
            mallo.insert()

    insecuresslsocket = doc.trustmanagers.find_all("insecuresslsocket")
    if len(list(insecuresslsocket)) > 1:
        mallo.package = app.package
        for m in doc.trustmanagers.find_all("insecuresslsocket"):
            mallo.mallo_text = m
            mallo.vuln_package = m.xref['class']
            if (mallo.vuln_package).startswith(app.package):
                mallo.vuln_in = 1
            else:
                mallo.vuln_in = 2
            mallo.insert()

    hostnameverifier = doc.hostnameverifiers.find("hostnameverifier")
    if hostnameverifier:
        mallo.package = app.package
        for m in doc.hostnameverifiers.find_all("hostnameverifier"):
            mallo.mallo_text = m
            mallo.vuln_package = m.xref['class']
            if (mallo.vuln_package).startswith(app.package):
                mallo.vuln_in = 1
            else:
                mallo.vuln_in = 2
            mallo.insert()

    sslerror = doc.onreceivedsslerrors.find("sslerror")
    if sslerror:
        mallo.package = app.package
        for m in doc.onreceivedsslerrors.find_all("sslerror"):
            mallo.mallo_text = m
            mallo.vuln_package = m.xref['class']
            if (mallo.vuln_package).startswith(app.package):
                mallo.vuln_in = 1
            else:
                mallo.vuln_in = 2
            mallo.insert()

def chunkify(lst,n):
    return [ lst[i::n] for i in xrange(n) ]

def callMallodroid(appsList):

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]

        res = runMallodroid(app)
        # result will be empty if app doesn't require internet permission
        if res:
            parseXML(res.strip(), app)

def do():
    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getApks()

    threads = []
    for list in chunkify(appsList, 2):
        p = Process(target=callMallodroid, args=(list,))
        logger.info("starting mallodroid thread %s", p)
        threads += [p]
        p.start()



    for t in threads:
        t.join()












