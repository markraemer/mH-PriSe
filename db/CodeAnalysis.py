import logging.config
from copy import copy

from db.helper import *

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

class CodeAnalysis():
    package = None,
    debuggable = None,
    contentprovider_used = None,
    contentprovider_accessible = None,
    contentprovider_gives_medical_app = None,
    malware = None

    def insert(self):

        sql=[]
        data=[]
        if self.package is not None:
            data.append(self.package)
            sql.append("package=%s")
        if self.debuggable is not None:
            data.append(self.debuggable)
            sql.append("debuggable=%s")
        if self.contentprovider_used is not None:
            data.append(self.contentprovider_used)
            sql.append("contentprovider_used=%s")
        if self.contentprovider_accessible is not None:
            data.append(self.contentprovider_accessible)
            sql.append("contentprovider_accessible=%s")
        if self.contentprovider_gives_medical_app is not None:
            data.append(self.contentprovider_gives_medical_app)
            sql.append("contentprovider_gives_medical_app=%s")
        if self.malware is not None:
            data.append(self.malware)
            sql.append("malware=%s")

        upsert = ["INSERT INTO code_analysis SET", ", ".join(sql), "on duplicate key update", ", ".join(sql), ";"]
        data.extend(copy(data))
        sql = " ".join(upsert)
        query = sql % tuple(data)

        logger.debug(query)
        cur.execute(sql, tuple(data))