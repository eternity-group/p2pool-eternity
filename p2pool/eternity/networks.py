import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack

nets = dict(
    eternity=math.Object(
        P2P_PREFIX='8ff74d2e'.decode('hex'),
        P2P_PORT=4855,
        ADDRESS_VERSION=33,
        SCRIPT_ADDRESS_VERSION=8,
        RPC_PORT=4854,
        RPC_CHECK=defer.inlineCallbacks(lambda eternityd: defer.returnValue(
            'eternityaddress' in (yield eternityd.rpc_help()) and
            not (yield eternityd.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: __import__('eternity_subsidy').GetBlockBaseValue(nBits, height),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('x11_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('x11_hash').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='ENT',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Dash') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dash/') if platform.system() == 'Darwin' else os.path.expanduser('~/.eternity'), 'eternity.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.eternity.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.eternity.org/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.eternity.org/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000000 - 1, 2**256//2**22 - 1),
        DUST_THRESHOLD=0.001e8,
    ),
    eternity_testnet=math.Object(
        P2P_PREFIX='2a2c2c2d'.decode('hex'),
        P2P_PORT=14855,
        ADDRESS_VERSION=93,
        SCRIPT_ADDRESS_VERSION=10,
        RPC_PORT=14854,
        RPC_CHECK=defer.inlineCallbacks(lambda eternityd: defer.returnValue(
            'eternityaddress' in (yield eternityd.rpc_help()) and
            (yield eternityd.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: __import__('eternity_subsidy').GetBlockBaseValue_testnet(nBits, height),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('x11_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('x11_hash').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='tARC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Dash') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dash/') if platform.system() == 'Darwin' else os.path.expanduser('~/.eternity'), 'eternity.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://test.explorer.eternity.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://test.explorer.eternity.org/address/',
        TX_EXPLORER_URL_PREFIX='http://test.explorer.eternity.org/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000000 - 1, 2**256//2**20 - 1),
        DUST_THRESHOLD=0.001e8,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
