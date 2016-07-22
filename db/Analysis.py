from db.helper import *

class Analysis():
    package = None,
    Type = None,
    pripol_in_app = None,
    path_to_exports = None,
    safety_check_bp = None,
    safety_check_gl = None,
    safety_check_pulse = None,
    export_SD = None,
    export_mail = None,
    export_web_native = None,
    export_other = None,
    authentication = None,
    wipe = None,
    comment = None

    def insert(self):
        sql = """insert into analysis (package, Type, pripol_in_app, path_to_exports, safety_check_bp,
        safety_check_gl, safety_check_pulse, export_SD, export_mail, export_web_native,
        export_other, authentication, wipe, comment) values (%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s, ,%s);"""
        data = (self.package, self.Type, self.pripol_in_app, self.path_to_exports, self.safety_check_bp,
                self.safety_check_gl, self.safety_check_pulse, self.export_SD, self.export_mail,
                self.export_web_native, self.export_other, self.authentication, self.wipe, self.comment)

        cur.execute(sql,data)