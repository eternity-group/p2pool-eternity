import sys
import time

from twisted.internet import defer

import p2pool
from p2pool.eternity import data as eternity_data
from p2pool.util import deferral, jsonrpc

@deferral.retry('Error while checking eternity connection:', 1)
@defer.inlineCallbacks
def check(eternityd, net):
    if not (yield net.PARENT.RPC_CHECK(eternityd)):
        print >>sys.stderr, "    Check failed! Make sure that you're connected to the right eternityd with --eternityd-rpc-port!"
        raise deferral.RetrySilentlyException()
    if not net.VERSION_CHECK((yield eternityd.rpc_getinfo())['version']):
        print >>sys.stderr, '    eternity version too old! Upgrade to 0.11.2.17 or newer!'
        raise deferral.RetrySilentlyException()

@deferral.retry('Error getting work from eternityd:', 3)
@defer.inlineCallbacks
def getwork(eternityd, net, use_getblocktemplate=False):
    def go():
        if use_getblocktemplate:
            return eternityd.rpc_getblocktemplate(dict(mode='template'))
        else:
            return eternityd.rpc_getmemorypool()
    try:
        start = time.time()
        work = yield go()
        end = time.time()
    except jsonrpc.Error_for_code(-32601): # Method not found
        use_getblocktemplate = not use_getblocktemplate
        try:
            start = time.time()
            work = yield go()
            end = time.time()
        except jsonrpc.Error_for_code(-32601): # Method not found
            print >>sys.stderr, 'Error: eternity version too old! Upgrade to v0.11.2.17 or newer!'
            raise deferral.RetrySilentlyException()
    packed_transactions = [(x['data'] if isinstance(x, dict) else x).decode('hex') for x in work['transactions']]
    packed_votes = [(x['data'] if isinstance(x, dict) else x).decode('hex') for x in work['votes']]
    if 'height' not in work:
        work['height'] = (yield eternityd.rpc_getblock(work['previousblockhash']))['height'] + 1
    elif p2pool.DEBUG:
        assert work['height'] == (yield eternityd.rpc_getblock(work['previousblockhash']))['height'] + 1
    defer.returnValue(dict(
        version=work['version'],
        previous_block=int(work['previousblockhash'], 16),
        transactions=map(eternity_data.tx_type.unpack, packed_transactions),
        transaction_hashes=map(eternity_data.hash256, packed_transactions),
        transaction_fees=[x.get('fee', None) if isinstance(x, dict) else None for x in work['transactions']],
        subsidy=work['coinbasevalue'],
        time=work['time'] if 'time' in work else work['curtime'],
        bits=eternity_data.FloatingIntegerType().unpack(work['bits'].decode('hex')[::-1]) if isinstance(work['bits'], (str, unicode)) else eternity_data.FloatingInteger(work['bits']),
        coinbaseflags=work['coinbaseflags'].decode('hex') if 'coinbaseflags' in work else ''.join(x.decode('hex') for x in work['coinbaseaux'].itervalues()) if 'coinbaseaux' in work else '',
        height=work['height'],
        last_update=time.time(),
        use_getblocktemplate=use_getblocktemplate,
        latency=end - start,
        votes=map(eternity_data.vote_type.unpack, packed_votes),
        payee=eternity_data.address_to_pubkey_hash(work['payee'], net.PARENT) if (work['payee'] != '') else None,
        payee_address=work['payee'].strip() if (work['payee'] != '') else None,
        eternitynode_payments=work['eternitynode_payments'],
        payee_amount=work['payee_amount'] if (work['payee_amount'] != '') else work['coinbasevalue'] / 5,
    ))

@deferral.retry('Error submitting primary block: (will retry)', 10, 10)
def submit_block_p2p(block, factory, net):
    if factory.conn.value is None:
        print >>sys.stderr, 'No eternityd connection when block submittal attempted! %s%064x' % (net.PARENT.BLOCK_EXPLORER_URL_PREFIX, eternity_data.hash256(eternity_data.block_header_type.pack(block['header'])))
        raise deferral.RetrySilentlyException()
    factory.conn.value.send_block(block=block)

@deferral.retry('Error submitting block: (will retry)', 10, 10)
@defer.inlineCallbacks
def submit_block_rpc(block, ignore_failure, eternityd, eternityd_work, net):
    if eternityd_work.value['use_getblocktemplate']:
        try:
            result = yield eternityd.rpc_submitblock(eternity_data.block_type.pack(block).encode('hex'))
        except jsonrpc.Error_for_code(-32601): # Method not found, for older litecoin versions
            result = yield eternityd.rpc_getblocktemplate(dict(mode='submit', data=eternity_data.block_type.pack(block).encode('hex')))
        success = result is None
    else:
        result = yield eternityd.rpc_getmemorypool(eternity_data.block_type.pack(block).encode('hex'))
        success = result
    success_expected = net.PARENT.POW_FUNC(eternity_data.block_header_type.pack(block['header'])) <= block['header']['bits'].target
    if (not success and success_expected and not ignore_failure) or (success and not success_expected):
        print >>sys.stderr, 'Block submittal result: %s (%r) Expected: %s' % (success, result, success_expected)

def submit_block(block, ignore_failure, factory, eternityd, eternityd_work, net):
    submit_block_p2p(block, factory, net)
    submit_block_rpc(block, ignore_failure, eternityd, eternityd_work, net)
