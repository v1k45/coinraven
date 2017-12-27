from pycoin.tx.tx_utils import create_signed_tx

from coinraven.exceptions import NetworkAPIError
from coinraven.tx import Payable

from .base import BaseCoin


class Bitcoin(BaseCoin):
    mainnet_netcode = "BTC"
    testnet_netcode = "XTN"

    def get_unspents(self):
        """
        List all UTXOs for the given address
        returns: List of spendable objects
        """
        for network_api in self.network_apis:
            try:
                return network_api.get_unspents(self.address)
            except NetworkAPIError:
                continue
        raise NetworkAPIError("All network calls for this method failed!")

    def get_transactions(self):
        """
        List all transactions for a given address
        return: List of Transaction objects
        """
        for network_api in self.network_apis:
            try:
                return network_api.get_transactions(self.address)
            except NetworkAPIError:
                continue
        raise NetworkAPIError("All network calls for this method failed!")

    def send(self, payables, fee, change_address=None):
        """
        Send coins list of payees with a fee and return the remaining coins
        to the change address (defaults to sender address)

        Payables should have their coin value in satoshis
        """
        spendables = self.get_unspents()

        # calculate leftover coins
        total_in = sum([s.coin_value for s in spendables])
        total_out = sum([p.value for p in payables])
        leftover = total_in - (total_out + fee)

        if leftover > 0:
            payables.append(Payable(change_address or self.address, leftover))

        # create a signed transaction
        signed_tx = create_signed_tx(spendables, payables, [self.key.wif(), ],
                                     netcode=self.netcode)

        # broadcast transaction to bitcoin network
        for network_api in self.network_apis:
            try:
                return network_api.send(signed_tx)
            except NetworkAPIError:
                continue
        raise NetworkAPIError("All network calls for this method failed!")
