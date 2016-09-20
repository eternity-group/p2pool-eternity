from p2pool.eternity import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    eternity=math.Object(
        PARENT=networks.nets['eternity'],
        SHARE_PERIOD=20, # seconds
        CHAIN_LENGTH=24*60*60//20, # shares
        REAL_CHAIN_LENGTH=24*60*60//20, # shares
        TARGET_LOOKBEHIND=100, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=10, # blocks
        IDENTIFIER='493A4A3F8049B800'.decode('hex'),
        PREFIX='24625DE68C76EE00'.decode('hex'),
        P2P_PORT=9219,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=9208,
        BOOTSTRAP_ADDRS='144.76.33.134'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-eternity',
        VERSION_CHECK=lambda v: v >= 120058,
    ),
    eternity_testnet=math.Object(
        PARENT=networks.nets['eternity_testnet'],
        SHARE_PERIOD=20, # seconds
        CHAIN_LENGTH=24*60*60//20, # shares
        REAL_CHAIN_LENGTH=24*60*60//20, # shares
        TARGET_LOOKBEHIND=100, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=10, # blocks
        IDENTIFIER='73D5B4F4533A7400'.decode('hex'),
        PREFIX='3476AF2B93F3CE00'.decode('hex'),
        P2P_PORT=19219,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=19208,
        BOOTSTRAP_ADDRS='144.76.33.134'.split(' '),
        ANNOUNCE_CHANNEL='',
        VERSION_CHECK=lambda v: True,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
