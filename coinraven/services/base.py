class NetworkAPI(object):
    supported_netcodes = []

    def __init__(self, netcode=None, *args, **kwargs):
        if netcode not in self.supported_netcodes:
            raise ValueError("Netcode %s is not supported by this network API" % netcode)

    def get_transactions(self, address):
        raise NotImplementedError("Method to fetch transactions is not implemented!")

    def get_unpents(self, address):
        raise NotImplementedError("Method to fetch unspents is not implemented!")

    def send(self, tx):
        raise NotImplementedError("Method to broadcast tranasaction is not implemented!")
