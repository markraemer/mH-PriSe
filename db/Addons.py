# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

from db.helper import *

class Addons():
    package = None
    name = None
    addon_type = None

    def insert(self):
        insert = "insert into addons (name, addon_type, package) values ('%s', '%s', '%s')" % (self.name, self.addon_type, self.package)

        update = []
        if self.addon_type is not None:
            update.append("addon_type = VALUES(addon_type)")
        if self.package is not None:
            update.append("package = VALUES(package)")

        if update:
            sql = [insert, "on duplicate key update"]
            sql.append(", ".join(update))
        else:
            sql = [insert]
        sql.append(";")
        logger.debug(" ".join(sql))
        cur.execute(" ".join(sql))

    @staticmethod
    def getAddons(package):
        sql = "SELECT name, addon_type FROM addons where package=%s;"
        cur.execute(sql, [package])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names