# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import sys
from copy import copy

reload(sys)
sys.setdefaultencoding('latin-1')

from db.helper import *

class Apps():
    id = None
    label = None
    package = None
    version = None
    versioncode = None
    filesize = None
    timestamp = None
    path_to_icon = None
    type = None
    path_to_exports = None
    path_to_internal_data = None
    comment = None
    path_to_apk = None

    # used when downloading the apk file initially
    def upsert(self):
        data = []
        sql = []
        if self.label is not None:
            data.append(self.label.encode("UTF-8"))
            sql.append("label='%s'")
        if self.package is not None:
            data.append(self.package)
            sql.append("package='%s'")
        if self.version is not None:
            data.append(self.version)
            sql.append("version='%s'")
        if self.versioncode is not None:
            data.append(self.versioncode)
            sql.append("versioncode='%s'")
        if self.filesize is not None:
            data.append(self.filesize)
            sql.append("filesize='%s'")
        if self.path_to_icon is not None:
            data.append(self.path_to_icon)
            sql.append("path_to_icon='%s'")
        if self.type is not None:
            data.append(self.type)
            sql.append("Type='%s'")
        if self.path_to_exports is not None:
            data.append(self.path_to_exports)
            sql.append("path_to_exports='%s'")
        if self.path_to_apk is not None:
            data.append(self.path_to_apk)
            sql.append("path_to_apk='%s'")
        if self.comment is not None:
            data.append(self.comment)
            sql.append("comment='%s'")

        upsert = ["INSERT INTO apps SET", ", ".join(sql), "on duplicate key update", ", ".join(sql), ";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query = sql % tuple(data)

        logger.debug(query)
        cur.execute(query)
        self.id = cur.lastrowid

    @classmethod
    def getAllApps(cls):
        sql = "SELECT package, path_to_apk, id FROM apps;"
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    @classmethod
    def getApks(cls):
        sql = "select distinct path_to_apk from apps;"
        cur.execute(sql)
        rows = cur.fetchall()
        return [x[0] for x in rows]

