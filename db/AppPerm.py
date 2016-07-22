import _mysql_exceptions

from db.helper import *

class AppPerm():
    id_app = None
    id_perm = None

    def insert(self):

        sql = "select id from permissions where name=%s;"

        cur.execute(sql,[self.id_perm])
        if cur.rowcount == 0:
            sql = "insert into permissions (name) values (%s);"
            cur.execute(sql, [self.id_perm])
            id = cur.lastrowid
        else:
            row = cur.fetchone()
            id = row[0]

        sql = "insert ignore into app_perm (id_app, id_perm) values (%s, %s);"
        perm_data = (self.id_app,id)

        cur.execute(sql,perm_data)

    @staticmethod
    def getPerm(package):
        sql = "SELECT * FROM mhealth_apps.view_app_perm where package=%s;"
        cur.execute(sql, [package])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names

    @staticmethod
    def getAppPerm():
        sql = "SELECT * FROM mhealth_apps.view_app_perm;"
        cur.execute(sql, [])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names

    @staticmethod
    def getAllPerm():
        sql = "SELECT * FROM mhealth_apps.permissions;"
        cur.execute(sql, [])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names
