# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

from db.helper import *

class Certificates():
    package = None
    cert_version = None
    cert_sig_algo = None
    cert_issuer = None
    cert_subject = None
    cert_nb = None
    cert_na = None
    cert_pka = None
    cert_pkl = None
    cert_sn = None

    def insert(self):
        insert = "insert into certificates (package, cert_version, cert_sig_algo, cert_issuer, cert_subject, cert_nb, cert_na, cert_pka, cert_pkl, cert_sn) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (self.package, self.cert_version, self.cert_sig_algo, self.cert_issuer, self.cert_subject, self.cert_nb, self.cert_na, self.cert_pka, self.cert_pkl, self.cert_sn)


        update = []
        if self.cert_version is not None:
            update.append("cert_version = VALUES(cert_version)")
        if self.cert_sig_algo is not None:
            update.append("cert_sig_algo = VALUES(cert_sig_algo)")
        if self.cert_issuer is not None:
            update.append("cert_issuer = VALUES(cert_issuer)")
        if self.cert_subject is not None:
            update.append("cert_subject = VALUES(cert_subject)")
        if self.cert_nb is not None:
            update.append("cert_nb = VALUES(cert_nb)")
        if self.cert_na is not None:
            update.append("cert_na = VALUES(cert_na)")
        if self.cert_pka is not None:
            update.append("cert_pka = VALUES(cert_pka)")
        if self.cert_pkl is not None:
            update.append("cert_pkl = VALUES(cert_pkl)")
        if self.cert_sn is not None:
            update.append("cert_sn = VALUES(cert_sn)")

        if update:
            sql = [insert, "on duplicate key update"]
            sql.append(", ".join(update))
        else:
            sql = [insert]
        sql.append(";")
        logger.debug(" ".join(sql))
        cur.execute(" ".join(sql))

    @staticmethod
    def getCerts(package):
        sql = "SELECT * FROM certificates where package=%s;"
        cur.execute(sql, [package])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names

    @staticmethod
    def getCerts():
        sql = "SELECT package, cert_sig_algo, cert_issuer, cert_subject, cert_nb, cert_na, cert_pka, cert_pkl, cert_sn FROM certificates;"
        cur.execute(sql, [])
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return rows, field_names