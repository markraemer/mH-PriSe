## just a helper

import subprocess
import os
import logging.config
import time
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

def toggleHostpot():
    cmd = "pgrep -a hotspot | awk '{print $1}'"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out, err

    if out:
        cmd = "kill -2 {}".format(out)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        cmd = "kill -2 `pgrep -a hostapd | awk '{print $1}'`"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logger.info("stopped access point")
        time.sleep(2)
    else:

        cmd = "`pwd`/bash/hotspot.sh > /dev/null &"
        os.system(cmd)
        logger.info("started access point")
        time.sleep(2)

def runProgram(program, args=None):
    os.system("{} {}".format(program,args))

def dump_tables():
    tables = ['devices','view_addons','am', 'view_app_perm','apps','certificates','experiment_overview','pripol','view_malware','view_obfuscation']
    path = "doc/tabledata"
    for table in tables:
        cmd = "sh bash/dump_table_to_csv.sh {} {}".format(table, path)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()


def open_log(context):
    cmd = ["gnome-terminal","-e","\"tail","-f",context.log,"\""]
    os.system(" ".join(cmd))
