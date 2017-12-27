import decimal
import io

import requests

from pycoin.convention import btc_to_satoshi
from pycoin.serialize import b2h, h2b, h2b_rev
from pycoin.tx.script import tools
from pycoin.tx.Tx import Spendable, Tx, TxIn, TxOut

from .base import NetworkAPI

# TODO: Refactor, this class taken from pycoin. Needs some cleanup.


class InsightAPI(NetworkAPI):
    supported_netcodes = ["BTC", "XTN"]
    NETCODE_API_MAP = {
        "BTC": "https://insight.bitpay.com/api",
        "XTN": "https://test-insight.bitpay.com/api"
    }

    def __init__(self, netcode=None):
        super(InsightAPI, self).__init__(netcode)
        self.base_url = self.NETCODE_API_MAP[netcode]

    def get_unspents(self, address):
        """
        Return a list of Spendable objects for the given bitcoin address.
        """
        URL = "%s/addr/%s/utxo" % (self.base_url, address)
        r = requests.get(URL)
        r.raise_for_status()
        spendables = []
        for u in r.json():
            coin_value = btc_to_satoshi(str(u.get("amount")))
            script = h2b(u.get("scriptPubKey"))
            previous_hash = h2b_rev(u.get("txid"))
            previous_index = u.get("vout")
            spendables.append(Spendable(coin_value, script, previous_hash, previous_index))
        return spendables

    def get_transactions(self, address):
        """
        Return a list of transaction objects for the given bitcoin address
        """
        URL = "%s/txs" % self.base_url
        res = requests.get(URL, params={"address": address})
        res.raise_for_status()
        transactions = []
        for transaction in res.json()["txs"]:
            transactions.append(self._tx_from_json_dict(transaction))
        return transactions

    def send(self, tx):
        """
        Broadcast a signed transaction to the network
        """
        s = io.BytesIO()
        tx.stream(s)
        tx_as_hex = b2h(s.getvalue())
        URL = "%s/tx/send" % self.base_url
        r = requests.post(URL, data={"rawtx": tx_as_hex})
        r.raise_for_status()
        print(r.text)
        return r.text

    @staticmethod
    def _tx_from_json_dict(r):
        """
        Convert a transaction dictionary to a Transaction object.
        Taken from pycoin.services.insight
        """
        version = r.get("version")
        lock_time = r.get("locktime")
        txs_in = []
        for vin in r.get("vin"):
            if "coinbase" in vin:
                previous_hash = b'\0' * 32
                script = h2b(vin.get("coinbase"))
                previous_index = 4294967295
            else:
                previous_hash = h2b_rev(vin.get("txid"))
                scriptSig = vin.get("scriptSig")
                if "hex" in scriptSig:
                    script = h2b(scriptSig.get("hex"))
                else:
                    script = tools.compile(scriptSig.get("asm"))
                previous_index = vin.get("vout")
            sequence = vin.get("sequence")
            txs_in.append(TxIn(previous_hash, previous_index, script, sequence))
        txs_out = []
        for vout in r.get("vout"):
            coin_value = btc_to_satoshi(decimal.Decimal(vout.get("value")))
            script = tools.compile(vout.get("scriptPubKey").get("asm"))
            txs_out.append(TxOut(coin_value, script))
        tx = Tx(version, txs_in, txs_out, lock_time)
        bh = r.get("blockhash")
        if bh:
            bh = h2b_rev(bh)
        tx.confirmation_block_hash = bh
        return tx
