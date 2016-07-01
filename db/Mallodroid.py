from db.helper import *

class Mallodroid():
    package = None
    mallo_text = None
    vuln_in = None
    vuln_package = None

    def insert(self):
        sql = "insert into mallodroid (package, mallo_text, vuln_in, vuln_package) values (%s, %s, %s, %s);"
        data =(self.package, self.mallo_text, self.vuln_in, self.vuln_package)
        cur.execute(sql,data)