#!/usr/bin/python
"""
Copyright (C) 2016, Martin Kraemer. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS-IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions
and limitations under the License.
"""


import logging.config
import os
import ConfigParser

from playstore import apps_companion,apps_tools
from apk import extractBaseInfo, runMallodroid, signAnalysis, apkHelper, runEviCheck, runExplainDroid, checkObfuscation
from onDevice import runDrozer,addonDetector,deviceHelper
from helper import checkLogFolders, experimentation, experiment_export_overview, experiment_export_latex
from traffic import trafficAnalysis
from pick import pick, Picker
from bash import bashHelper
from webserver import SSLchecker

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

config = ConfigParser.RawConfigParser()
config.read('config.prop')

os.system("taskset -p 0xff %d" % os.getpid())
dir_path = os.path.dirname(os.path.realpath(__file__))

logger.info("Starting ...")
logger.info("Log file is {}/log.out".format(dir_path))

# context object to pass parameters
class runner:
    current_menu = "main"
    package = ""
    device= ""
    action = ""
    android_sdk = ""
    log = ""
    chg_pkg = False
    chg_dev = False
context = runner()

context.log = dir_path + "/log.out"

def change_package(dest_menu):
    context.package = experimentation.choosePackage()
    context.current_menu = dest_menu


# using curses-menu by Paul Barrett
# https://github.com/pmbarrett314/curses-menu
menu_tree = {
    'prepare': {
        'menu': {
            "1 - maintain apps list": (bashHelper.runProgram, ["gedit", config.get("apps","apps.companion.list")]),
            "2 - maintain tools apps list": (bashHelper.runProgram, ["gedit", config.get("apps","tool.apk.tools.list")]),
            "3 - download and install tools": (apps_tools.do,[True]),
            "4 - download all companion apks": (apps_companion.download, []),
            "5 - install companion apks": (apps_companion.install, []),
            "quit": None
        },
        'title': 'steps to prepare the experiments',
        'parent_menu': 'main'
    },
    'main' : {
        'menu': {
            "1 - toggle hotspot": (bashHelper.toggleHostpot, None),
            "2 - PREPARE analysis": ('menu', ['prepare']),
            "3 - STATIC analysis": ('menu', ['static']),
            "4 - DYNAMIC analysis": ('menu', ['dynamic']), # should choose package first
            "5 - POST experiment analysis": ('menu', ['post']),  # should choose packge -> test case first
            "6 - export results": ('menu', ['export']),
            "7 - tools and helper": ('menu', ['tools']),
            "8 - open log file": (bashHelper.open_log, [context]),
            "quit": None
        },
        'title': "Main Menu - see logs in {}/log.out".format(dir_path),
        'parent_menu': None
    },
    'static' : {
        'menu': {
            "1 - extract base info": (extractBaseInfo.apkInfo,[]),
            "2 - run mallodroid": (runMallodroid.do,[]),
            "3 - intents, broadcasts, activities, services exports (Drozer)": (runDrozer.do,[]),
            "4 - signature certificate info (developer certificate": (signAnalysis.certInfo,[]),
            "5 - detect addons": (addonDetector.do,[]),
            "6 - check obfuscation": (checkObfuscation.do,[]),
            "7 - Malware / Evicheck": (runEviCheck.do,[]),
            "8 - Malware / ExplainDroid": (runExplainDroid.do,[]),
            "quit": None
        },
        'title': "Static analysis",
        'parent_menu': 'main'
    },
    'dynamic' : {
        'menu': {
            "1 - run test case": (experimentation.do,['start', context]),
            "2 - document recorded test case": (experimentation.do,['document', context]),
            "3 - show missing cases and steps": (experimentation.do,['missing', context]),
            "quit": None
        },
        'title': "Dynamic analysis - manually record test cases",
        'parent_menu': 'main'
    },
    'post' : {
        'menu': {
            "1 - extract URLs": (trafficAnalysis.for_rec_experiment,[context, True]),
            "2 - scan PCAP files": (trafficAnalysis.analysePCAP,[context]),
            "3 - check server SSL": (SSLchecker.do,[context]),
            "4 - show recording": ('menu', ['show']),
            "quit": None
        },
        'title': "post experiments analysis",
        'parent_menu': 'main'
    },
    'show' : {
        'menu': {
            "1 - show network traffic": (experimentation.show_traces, [context]),
            "2 - open log folder": (experimentation.open_log_folder, [context]),
            "quit": None
        },
        'title': "show test case details",
        'parent_menu': 'post'
    },
    'tools' : {
        'menu': {
            "1 - convert apk to smali": (apkHelper.apkToSmali,[context]),
            "2 - reassemble from smali and install": (apkHelper.assemble_and_install,[context]),
            "3 - convert apk to jar": (apkHelper.apkTorJar, [context]),
            "4 - open apk in jd-gui": (apkHelper.openJarInJdGui, [context]),
            "5 - stop all 3rd party apps": (deviceHelper.stopAllApps,None),
            "6 - kill running tools (if program crashed previously)": None,
            "7 - validate log folder structure": (checkLogFolders,[]),
            "quit": None
        },
        'title': "tools and helper",
        'parent_menu': 'main'
    },
    'export' : {
        'menu': {
            "1 - static analysis - tables to csv": (bashHelper.dump_tables, []),
            "2 - static analysis - generate latex exports": (experiment_export_latex.do, []),
            "3 - dynamic analysis - results (PDF, HTML)": (experiment_export_overview.do, []),
            "quit": None
        },
        'title': "show test case details",
        'parent_menu': 'post'
    }


}


# helper to set flags for device or package change
def choose_package(args):
    context.chg_pkg = True
    return "pass", 0

def choose_device(args):
    context.chg_dev = True
    return "pass", 0

def show_menu(startid='main'):
    """
    shows the menu on screen
    :param startid: the id of the menu to start with (used to find parrent)
    :return:
    """

    # check if package or device are to be changed
    # just working around stacking curses menus
    if context.chg_pkg:
        context.package = experimentation.choosePackage()
        context.chg_pkg = False
        return
    if context.chg_dev:
        context.device = experimentation.chooseDevice(context.package)
        context.chg_dev = False


    context.current_menu = startid
    menu = menu_tree[startid]
    options = menu['menu'].keys()

    options.sort()

    if context.package:
        subtitle = "Package: {}, Device: {}".format(context.package, context.device)
    else:
        subtitle = ""

    hotkeys = "Press 'p' to change the package, 'd' to change the device"
    title = "{}\n{}\n{}".format(menu['title'], hotkeys, subtitle)
    picker = Picker(options=options,title=title)
    picker.register_custom_handler(ord('p'), choose_package)
    picker.register_custom_handler(ord('d'), choose_device)
    action, idx = picker.start()

    context.action = action
    if action == "pass":
        # used to change package or device
        # will simply do nothing and reload the menu
        return
    if action == "quit":
        if menu['parent_menu'] != None:
            show_menu(menu['parent_menu'])
        else:
            logger.info("... finished")
            exit()
    else:
        func = menu['menu'][action][0]
        if func == 'menu':
            func = globals()['show_menu']
        if menu['menu'][action][1] is not None:
            args = menu['menu'][action][1]
            func(*args) # calling with arguments
        else:
            func()  # calling without arguments

# start the menu and loop
while True:
    context.android_sdk = deviceHelper.android_version()
    show_menu(context.current_menu)
