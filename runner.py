#!/usr/bin/python
# MK Jul 2016
# runner application file
import os
import logging.config

import curses

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

# to construct the menu
from cursesmenu import *
from cursesmenu.items import *

from subprocess import call

from playstore import apps_companion,apps_tools
from apk import extractBaseInfo, runMallodroid, signAnalysis, apkHelper, runEviCheck, runExplainDroid, checkObfuscation
from onDevice import runDrozer,addonDetector,deviceHelper
from helper import checkLogFolders, experimentation, experiment_overview
from traffic import trafficAnalysis
from pick import pick
from bash import bashHelper
from webserver import SSLchecker

import sys


from db.Location import Location
import requests

os.system("taskset -p 0xff %d" % os.getpid())
logger.info("Starting ...")

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.prop')

class runner:
    current_menu = "main"
    package = ""
    action = ""
    android_sdk = ""

context = runner()

def change_package(dest_menu):
    context.package = experimentation.choosePackage()
    context.current_menu = dest_menu

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
            "4 - DYNAMIC analysis": (change_package, ['dynamic']), # should choose package first
            "5 - data analysis": (change_package, ['post']),  # should choose packge -> test case first
            "6 - tools and helper": ('menu', ['tools']),
            "7 - show results": (experiment_overview.do, []),
            "quit": None
        },
        'title': "Main Menu",
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
            "1 - extract URLs (requried for following)": (trafficAnalysis.for_rec_experiment,[context, True]),
            "2 - create traffic map": None,
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
            "8 - export tables to csv": (bashHelper.dump_tables, []),
            "quit": None
        },
        'title': "tools and helper",
        'parent_menu': 'main'
    }


}

import time

def show_menu(startid='main'):
    context.current_menu = startid
    menu = menu_tree[startid]
    options = menu['menu'].keys()
    options.sort()
    if context.package:
        subtitle = context.package
    else:
        subtitle = ""
    title = "{} \n {}".format(menu['title'], subtitle)
    action, idx = pick(options, title)
    context.action = action
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
            func(*args) # this will call the linked function
        else:
            func()  # this will call the linked function





while True:
    context.android_sdk = deviceHelper.android_version()
    show_menu(context.current_menu)
