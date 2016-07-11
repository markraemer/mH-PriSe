# MK Jul 2016

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('runner')

import subprocess
import re
from db.Certificates import Certificates
from db.Apps import Apps

#////////////////////////////


def certInfo():

    # get all apks which are linked in the database
    # will come with [0] package [1] path_to_apk
    appsList = Apps().getAllApps()

    p_version = re.compile(".*Version: (.*) \(.*")
    p_signalgo = re.compile(".*Signature Algorithm: (.*).*")
    p_cert_issuer = re.compile(".*Issuer: (.*) .*")
    p_cert_subject = re.compile(".*Subject: (.*) .*")
    p_cert_nb = re.compile(".*Not Before: (.*) .*")
    p_cert_na = re.compile(".*Not After : (.*) .*")
    p_cert_pka = re.compile(".*Public Key Algorithm: (.*).*")
    p_cert_pkl = re.compile(".*Public-Key: \((.*) bit\).*")
    p_cert_sn = re.compile(".*Serial Number: (.*)")



    for apk in appsList:
        cert = Certificates()
        app = Apps()
        app.path_to_apk = apk[1]
        app.package = apk[0]
        cert.package = app.package

        logger.info("%s starting certificate analysis", app.package)

        cmd = ["unzip", "-p",  app.path_to_apk, "META-INF/*.*SA"] # there are RSA and DSA certificates; cater for both
        cmd2 = ["openssl", "pkcs7", "-inform", "DER", "-noout", "-print_certs", "-text" ]
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p = subprocess.Popen(cmd2, stdin=ps.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        if err:
            logger.error(err)
            continue
        else:
            lines = out.splitlines()
            for line in lines:

                a = p_version.match(line)
                if a:
                    cert.cert_version = a.group(1)
                    continue

                a = p_signalgo.match(line)
                if a:
                    cert.cert_sig_algo = a.group(1)
                    continue

                a = p_cert_issuer.match(line)
                if a:
                    cert.cert_issuer = a.group(1)
                    continue

                a = p_cert_subject.match(line)
                if a:
                    cert.cert_subject = a.group(1)
                    continue

                a = p_cert_nb.match(line)
                if a:
                    cert.cert_nb = a.group(1)
                    continue

                a = p_cert_na.match(line)
                if a:
                    cert.cert_na = a.group(1)
                    continue

                a = p_cert_pka.match(line)
                if a:
                    cert.cert_pka = a.group(1)
                    continue

                a = p_cert_pkl.match(line)
                if a:
                    cert.cert_pkl = a.group(1)
                    continue

                a = p_cert_sn.match(line)
                if a:
                    cert.cert_sn = a.group(1)

            cert.insert()