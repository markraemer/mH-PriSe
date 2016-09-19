from Crypto.Hash import MD5
import crc16
import re
import base64
import hashlib

pwd = MD5.new()
print pwd.new("123A456").hexdigest()

hash = MD5.new()
print hash.new(pwd.new("AAAAAA").hexdigest()+"inf.hapi@gmail.com").hexdigest()

###########
# fitbit protocol engineering
###########


def big2little_endian(str):
    return "".join(reversed(re.findall(r'.{1,2}', str, re.DOTALL)))

weight_g = 99999000

weight_bigendian = format(weight_g,'08X')

weight_littleendian = big2little_endian(weight_bigendian)

print weight_littleendian

hexstr = '030000006400000020F85ECB765DE301'\
         '8001FE617EA50289626B394304C82700'\
         '00002100000009909B57010000000200'\
         '000000000000' + weight_littleendian + '00FE8F9B570000'\
         '0000000000000000000000000000'


crc_bigendian = format(crc16.crc16xmodem((hexstr.decode("hex"))),'04X')
crc_littleendian = big2little_endian(crc_bigendian)

print crc_littleendian


post_weight = "weight=400.0&date=2016-07-31&time=23%3A59%3A59"

tracking_body = """W3siZXZlbnQiOiJTb2NpYWw6IFZpZXcgUHJvZmlsZSIsInByb3BlcnRpZXMiOnsibXBfbGliIjoiYW5kcm9pZCIsIiRsaWJfdm
Vyc2lvbiI6IjQuOC41IiwiJG9zIjoiQW5kcm9pZCIsIiRvc192ZXJzaW9uIjoiNi4wIiwiJG1hbnVmYWN0dXJlciI6IkxHRSIsIiRicm
FuZCI6Imdvb2dsZSIsIiRtb2RlbCI6Ik5leHVzIDUiLCIkZ29vZ2xlX3BsYXlfc2VydmljZXMiOiJhdmFpbGFibGUiLCIkc2NyZWVuX2
RwaSI6NDgwLCIkc2NyZWVuX2hlaWdodCI6MTc3NiwiJHNjcmVlbl93aWR0aCI6MTA4MCwiJGFwcF92ZXJzaW9uIjoiMi4yOSIsIiRhcH
BfdmVyc2lvbl9zdHJpbmciOiIyLjI5IiwiJGFwcF9yZWxlYXNlIjoyMTgzMDAyLCIkYXBwX2J1aWxkX251bWJlciI6MjE4MzAwMiwiJG
hhc19uZmMiOnRydWUsIiRoYXNfdGVsZXBob25lIjp0cnVlLCIkY2FycmllciI6IkVFIiwiJHdpZmkiOnRydWUsIiRibHVldG9vdGhfZW
5hYmxlZCI6dHJ1ZSwiJGJsdWV0b290aF92ZXJzaW9uIjoiYmxlIiwidG9rZW4iOiI4MmQxOTg0NWIyOThmY2M4Yjg3MTM4NjFjOWNmNj
djMCIsIlBsYXRmb3JtIjoiQW5kcm9pZCIsIkFuZHJvaWQgQXBwIFZlcnNpb24iOiIyLjI5ICgyMTgzMDAyKSIsIkJsdWV0b290aCBMaW
JyYXJ5IjoiR29vZ2xlIiwiRW52aXJvbm1lbnQiOiJwcm9kIiwiUGFpcmVkIERldmljZXMiOlsiQVJJQSJdLCJ0aW1lIjoxNDY5OTY3OD
Q1LCJkaXN0aW5jdF9pZCI6IjU3NTY5MDc5IiwiIVR5cGUiOiJQZXJzb25hbCIsIkxvY2FsZSI6ImVuX0dCIiwiTG9jYWxlTGFuZyI6Ik
dCIiwiTG9jYWxlUmVhbCI6ImVuX0dCIn19XQ=="""

engage = """W3siJGFkZCI6eyJBcHA6IExpZmV0aW1lIEFwcGxpY2F0aW9uIExhdW5jaGVzIjoxfSwiJHRva2VuIjoiODJkMTk4NDViMjk4Zm
NjOGI4NzEzODYxYzljZjY3YzAiLCIkdGltZSI6MTQ2OTk2Nzc4MjY3OSwiJGRpc3RpbmN0X2lkIjoiNTc1NjkwNzkifSx7IiRhZGQiOn
siQXBwOiBWZXJzaW9uLVNwZWNpZmljIEFwcCBPcGVucyI6MX0sIiR0b2tlbiI6IjgyZDE5ODQ1YjI5OGZjYzhiODcxMzg2MWM5Y2Y2N2
MwIiwiJHRpbWUiOjE0Njk5Njc3ODI2NzksIiRkaXN0aW5jdF9pZCI6IjU3NTY5MDc5In1d"""

print base64.decodestring(tracking_body)
print base64.decodestring(engage)




#########
# withings protocol engineering
#########


from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join

CERT_FILE = "myapp.crt"
KEY_FILE = "myapp.key"

# https://gist.github.com/ril3y/1165038

def create_self_signed_cert(cert_dir):
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    if not exists(join(cert_dir, CERT_FILE)) \
            or not exists(join(cert_dir, KEY_FILE)):
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "UK"
        cert.get_subject().ST = "UK"
        cert.get_subject().L = "UK"
        cert.get_subject().O = "UK"
        cert.get_subject().OU = "UK"
        cert.get_subject().CN = "wbs04-ws.withings.net"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        open(join(cert_dir, CERT_FILE), "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wt").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k))




hash = MD5.new()

once = "00e04956-d78742a9"
secret = "tmfozZCeTcc9jm6R2Miv7ldqEHgFggvp"
mac = "00:24:e4:35:c7:34"

# see .class public Lcom/withings/device/ws/DeviceSessionFactory
# and password util for further information
# <mac>:<secret>:<once>

print hash.new("{}:{}:{}".format(mac,secret,once)).hexdigest()
#b26e02358696be7bf57a3c6bf5987bf5

pwd = MD5.new()
print pwd.new("AAAAAA").hexdigest()


## withings body cardio



pbkey = """c586630fd0c0fefcfd986bf909832561c86d994fee8caa0d9af00cc9b7aa28e356eb86983dba286e520168298ac20f839929d264b1fb730484edd551b30e
a4412423b5bd88edf2665a2598c41fa199d08f894299797b0f50fc5f7dd1fc032c7d3c5b4dff36f41850cb3dfd8dd8e20d44d87c
d011584eb78c9ca7c8477cfd3b3dfb38409278f2e4a13cef0485496c94666ff0ff9155f9d4479335a70515ccb18cab6e2fb4f1a5
d45ac823abc89e2999b1fc91ffc984dd422b2fbb1eaa980e49ea47d932ce1dd431793a7b4b1764aa4c1d1e18f0b5991091799d27
aa07c94dba86a4883a466f7555e70218c4ffc465200e8067bff387aa4878c048796a24dd14ff"""

print hashlib.sha1(pbkey).hexdigest()

digest = """0bcae3abbc3a67494942e9c4b597a9302b6ec9204606f302e23725e9fb44605033b559402b112dc8df85d2b41a995116
606cc7a09722b8c388e84ab2c003ab29d4943a864e267ee3996f80fe7c892644c5ee3acab76fd9d916c00f380a136eec9cf7aa35
21a4d63c2c28cf4f00f97327579bc028a2ffb4e328cad44c180662b4a1a636dbac93b6d062cc2736054b7f7be457d9a122a3b558
f995d0e9de1f3eeba42402ed05a0982b192fd6ccca7df680cb09cbcc2f3be49ea57c81f6343e694d0cc83b2d0a24031cee1e22de
a253ee7764741029eb226027c9e8bb554bad940db659c48b742b77d3287e16eec98651b4a032c1c887d72204828b11f87fc7a8bf"""

get_certificate = """{"status":0,"body":{"date":1469966749,"keyscount":1,"keys":[{"size":2048,"modulus":"%s","exponent":"00010001"}],"digest":"%s"}}""" % (pbkey,digest)


print hashlib.sha256(pbkey).hexdigest()

from OpenSSL.crypto import load_certificate, FILETYPE_PEM
cert_file_string = open("/media/exthdd/experiments/com.withings.wiscale2/device-16/withings_net.pem", "rb").read()
cert = load_certificate(FILETYPE_PEM, cert_file_string)
sha1_fingerprint = cert.digest("sha1")
print "Cert SHA1 finger print ", sha1_fingerprint