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
