import logging.config
from copy import copy
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('db')

from db.helper import *

class Drozer():
    package = None
    type_name = None
    class_name = None
    permission = None

    def insert(self):
        data=[]
        sql=[]

        if self.package is not None:
            data.append(self.package)
            sql.append("package=%s")
        if self.type_name is not None:
            data.append(self.type_name)
            sql.append("type_name=%s")
        if self.class_name is not None:
            data.append(self.class_name)
            sql.append("class=%s")
        if self.permission is not None:
            data.append(self.permission)
            sql.append("permission=%s")

            upsert = ["INSERT INTO app_attsuf SET", ", ".join(sql), "on duplicate key update", ", ".join(sql), ";"]
            data.extend(copy(data))
            sql = " ".join(upsert)
            query = sql % tuple(data)

            logger.debug(query)
            cur.execute(sql,tuple(data))