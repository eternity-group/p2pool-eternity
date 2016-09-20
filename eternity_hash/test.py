import x11_hash
from binascii import unhexlify, hexlify

import unittest

# eternity block #1
# moo@b1:~/.eternity$ eternity-cli getblockhash 1
# 00000f1f233096f9ae76b9524237388a9046b1470b933a430203e5d25044a838
# moo@b1:~/.eternity$ eternityd getblock 00000f1f233096f9ae76b9524237388a9046b1470b933a430203e5d25044a838
# {
    # "hash" : "00000f1f233096f9ae76b9524237388a9046b1470b933a430203e5d25044a838",
    # "confirmations" : 2646,
    # "size" : 179,
    # "height" : 1,
    # "version" : 3,
    # "merkleroot" : "c68bba1a02984ff56e5cef1b272137914f3c7f5699f748a7d7fa3ff8e0733028",
    # "tx" : [
    # "c68bba1a02984ff56e5cef1b272137914f3c7f5699f748a7d7fa3ff8e0733028"
    # ],
    # "time" : 1470517202,
    # "nonce" : 1560750,
    # "bits" : "1e0fffff",
    # "difficulty" : 0.00024414,
    # "chainwork" : "0000000000000000000000000000000000000000000000000000000000200011",
    # "previousblockhash" : "00000f39e7fdff2d6025511f525bf1dce2f705c15d098d7f31c824a1785a254a",
    # "nextblockhash" : "00000fda23f15d2c64a58e06af47572b9ae76a1b687ddf93cafd997be54ae945"
# }

header_hex = ("02000000" +
    "b67a40f3cd5804437a108f105533739c37e6229bc1adcab385140b59fd0f0000" +
    "a71c1aade44bf8425bec0deb611c20b16da3442818ef20489ca1e2512be43eef"
    "814cdb52" +
    "f0ff0f1e" +
    "dbf70100")

best_hash = '434341c0ecf9a2b4eec2644cfadf4d0a07830358aed12d0ed654121dd9070000'

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.block_header = unhexlify(header_hex)
        self.best_hash = best_hash

    def test_x11_hash(self):
        self.pow_hash = hexlify(x11_hash.getPoWHash(self.block_header))
        self.assertEqual(self.pow_hash, self.best_hash)


if __name__ == '__main__':
    unittest.main()

