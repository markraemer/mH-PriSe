from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode
import M2Crypto

def verify_sign(public_key, signature, data):
    '''
    Verifies with a public key from whom the data came that it was indeed
    signed by their private key
    param: public_key_loc Path to public key
    param: signature String signature to be verified
    return: Boolean. True if the signature is valid; False otherwise.
    '''

    pub_key = public_key
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    # Assumes the data is base64 encoded to begin with
    digest.update(b64decode(data))
    print digest.hexdigest()
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

key = """c586630fd0c0fefcfd98
6bf909832561c86d994fee8caa0d9af00cc9b7aa28e356eb86983dba286e520168298ac20f839929d264b1fb730484edd551b30e
a4412423b5bd88edf2665a2598c41fa199d08f894299797b0f50fc5f7dd1fc032c7d3c5b4dff36f41850cb3dfd8dd8e20d44d87c
d011584eb78c9ca7c8477cfd3b3dfb38409278f2e4a13cef0485496c94666ff0ff9155f9d4479335a70515ccb18cab6e2fb4f1a5
d45ac823abc89e2999b1fc91ffc984dd422b2fbb1eaa980e49ea47d932ce1dd431793a7b4b1764aa4c1d1e18f0b5991091799d27
aa07c94dba86a4883a466f7555e70218c4ffc465200e8067bff387aa4878c048796a24dd14ff"""

digest = """ba4b173a68e647918e7bf3404dd3b2b48c990b63d94840d510b4cada5ca7adc9b4da9c0bb3568586c021a7ff34c8c925
cf5965e16acbc4d039c1bd33ca402fa583c1d77383f1a90e41d20b2ebb08c5b8d5200f1700dd14eadad3226d74f707a5b7dbd324
4f90468f2c0d108b14215c13a5fe34c61555e4741991f02528d9c026da7451898abc2f9beadd8aabb2360f4345b7041cdd58a144
58dd43a5e123e2e9633d0e971795c7481a9e2ad4d28c2279473311cf9b813ea77cfe54e03912112d670bfbbb8746cb9e9f876b10
d71c98370274b6bf2efce11bd0073d41ccd54c04ce4fa2bb52531e8ebd17afd556a0ae62207d8d42775cd62c1964dd20ddf42565"""

time = """1470129359"""

challenge = """GKBNEDVRHTGSRSYA"""

verify_sign(key,digest,challenge)

with open("/media/exthdd/experiments/com.withings.wiscale2/device-16/withings_net.der") as derfile:
    c = derfile.read()

pubKeyObj =  RSA.importKey(c)