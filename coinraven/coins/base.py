from pycoin.key import Key


class BaseCoin(object):
    mainnet_necode = None
    testnet_netcode = None

    def __init__(self, key, network_apis=None, testnet=False, **kwargs):
        self.key = Key.from_text(key)
        self.netcode = self.testnet_netcode if testnet else self.mainnet_netcode
        if network_apis:
            self.network_apis = network_apis

    @property
    def address(self):
        return self.key.address()

    def get_unspents(self):
        raise NotImplementedError("Method to get list of unspents for this coins is not implemented!")

    def get_balance(self):
        raise NotImplementedError("Method to get balance value or this coins is not implemented!")

    def get_transactions(self):
        raise NotImplementedError("Method to get list of transactions for this coin is not implemented!")

    def send(self, payables, fee, change_address=None):
        raise NotImplementedError("Method to spend transactions for this coin is not implemented!")
