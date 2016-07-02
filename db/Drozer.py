from db.helper import *

class Drozer():
    package = None
    type_name = None
    class_name = None
    permission = None

    def insert(self):
        sql = "insert into app_attsuf (package, type_name, class, permission) values (%s, %s, %s, %s);"
        data = (self.package, self.type_name, self.class_name, self.permission)
        cur.execute(sql, data)