from db.helper import *

class CodeAnalysis():
    package = None,
    debuggable = None,
    contentprovider_used = None,
    contentprovider_accessible = None,
    contentprovider_gives_medical_app = None,
    malware = None

    def insert(self):
        sql = """insert into code_analysis (package, debuggable, contentprovider_used, contentprovider_accessible,
        contentprovider_gives_medical_app, malware) values ( %s, %s, %s, %s, %s, %s);"""
        data = (self.package, self.debuggable, self.contentprovider_used, self.contentprovider_accessible,
                self.contentprovider_gives_medical_app, self.malware)
        cur.execute(sql,data)