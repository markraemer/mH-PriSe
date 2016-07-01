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
    def insert(self):
        sql = "INSERT INTO apps (label, package, version, versioncode, filesize, timestamp, path_to_icon, Type,path_to_exports, path_to_internal_data, comment, path_to_apk) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
        data_apps = (self.label.encode("UTF-8"), self.package, self.version, self.versioncode, self.filesize, self.timestamp, self.path_to_icon, self.type, self.path_to_exports, self.path_to_internal_data, self.comment, self.path_to_apk )
        cur.execute(sql,data_apps)
        self.id = cur.lastrowid

    @classmethod
    def getApks(cls):
        sql = "SELECT package, path_to_apk FROM apps;"
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    # used by aapt tool to insert additional information
    def update(self):
        # this should be implemented some point in time
        # boilerplate coding....
        usql = "update apps set "
        fields = []
        udata = []

        if self.filesize <> None:
            fields.append("filesize = %s")
            udata.append(self.filesize)

        if self.version <> None:
            fields.append("version = %s")
            udata.append(self.version)

        if self.versioncode <> None:
            fields.append("versioncode = %s")
            udata.append(self.versioncode)

        if self.path_to_icon <> None:
            fields.append("path_to_icon = %s")
            udata.append(self.path_to_icon)

        udata.append(self.package)
        usql = usql + ", ".join(fields) + "where package=%s"
        cur.execute(usql,udata)
        self.id = cur.lastrowid


