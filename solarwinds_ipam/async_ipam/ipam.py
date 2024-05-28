from solarwinds_ipam.async_ipam.swisclient import AsyncSwisClient
from solarwinds_ipam.async_ipam import node
from solarwinds_ipam.async_ipam import subnet

class AsyncIPAM(AsyncSwisClient):

    def __init__(self, *, server='', port=17778, username='', password='', verify=False):

        super().__init__(server=server, port=port, username=username, password=password, verify=verify)

        # Monkey patch to link functions in the imported 'node' module to the methods in this class
        self.node = node
        for f in ['_create', '_read', '_update', '_delete', '_invoke', '_query', '_request']:
            setattr(self.node, f, getattr(self, f))

        # Monkey patch to link functions in the imported 'subnet' module to the methods in this class
        self.subnet = subnet
        for f in ['_create', '_read', '_update', '_delete', '_invoke', '_query', '_request']:
            setattr(self.subnet, f, getattr(self, f))

