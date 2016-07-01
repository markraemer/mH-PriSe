# MK Jul 2016

from mallodroid import mallodroid
from db.Apps import Apps

from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.decompiler.dad import decompile
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.bytecodes.apk import APK
from androguard.core.analysis.analysis import uVMAnalysis
from androguard.core.analysis.ganalysis import GVMAnalysis

from bs4 import BeautifulSoup


# this is based on mallodroid coding and simplified
def runMallodroid(app):
    assert isinstance(app, Apps), "app is not type Apps: %r" % app
    print "running mallodroid on %s" % app.package
    _a = apk.APK(app.path_to_apk)

    _vm = dvm.DalvikVMFormat(_a.get_dex())
    _vmx = uVMAnalysis(_vm)

    if 'android.permission.INTERNET' in _vmx.get_permissions([]):
        print "App requires INTERNET permission. Continue analysis..."

        _vm.create_python_export()
        _gx = GVMAnalysis(_vmx, None)

        _vm.set_vmanalysis(_vmx)
        _vm.set_gvmanalysis(_gx)
        _vm.create_dref(_vmx)
        _vm.create_xref(_vmx)

        _result = {'trustmanager': [], 'hostnameverifier': [], 'onreceivedsslerror': []}
        _result = mallodroid._check_all(_vm, _vmx, _gx)

        return mallodroid._xml_result(_a, _result)

        #    print "Store decompiled Java code in {:s}".format(_args.dir)
        #   _store_java(_vm, _args)

    else:
        print "App does not require INTERNET permission. No need to worry about SSL misuse... Abort!"

def parseXML(xml):
    doc = BeautifulSoup(xml, "lxml")

    print len(list(doc.trustmanagers.children))




def do():
    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getApks()

    for apk in appsList:
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]

        #res = runMallodroid(app)

        res = """
        <?xml version="1.0" ?>
<result package="com.fitbit.FitbitMobile">
	<trustmanagers>
		<trustmanager broken="True" class="com.amazonaws.http.g$c">
			<xref class="com.amazonaws.http.g$b" method="&lt;init&gt;"/>
		</trustmanager>
		<trustmanager broken="True" class="com.amazonaws.http.s$b">
			<xref class="com.amazonaws.http.s" method="a"/>
		</trustmanager>
		<insecuresslsocket/>
	</trustmanagers>
	<hostnameverifiers>
		<hostnameverifier broken="True" class="com.amazonaws.http.s$a">
			<xref class="com.amazonaws.http.s" method="a"/>
		</hostnameverifier>
		<allowhostnames/>
	</hostnameverifiers>
	<onreceivedsslerrors>
		<sslerror broken="Maybe" class="com.facebook.internal.ab$b">
			<xref class="com.facebook.internal.ab" method="a"/>
		</sslerror>
	</onreceivedsslerrors>
</result>
        """
        parseXML(res.strip())









