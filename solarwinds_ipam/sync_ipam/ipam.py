from solarwinds_ipam.sync_ipam.swis_api import SwisApi
from solarwinds_ipam.sync_ipam import ipaddress
from solarwinds_ipam.sync_ipam import ipsubnet
import re

class IPAM(SwisApi):

    def __init__(self, *, server='', port=17778, username='', password='', verify=False):

        super().__init__(server=server, port=port, username=username, password=password, verify=verify)
        #
        # Some weird things going on here :)
        # We make the 'ipaddress' and 'ipsubnet' modules imported above available in this class, so we can
        # use the functions in these modules as methods from this class.
        # ipam = IPAM(...)
        # ipam.ipaddress.* -> functions is 'ipaddress' module, i.e. ipam.ipaddress.get(...)
        # ipam.ipsubnet.* -> functions is 'ipsubnet' module, i.e. ipam.ipsubnet.get_uri(...)
        #
        # The basic methods are inherited from the 'swisclient' superclass
        #
        self.monkeypatch('ipaddress')
        self.monkeypatch('ipsubnet')

    def monkeypatch(self, module_name):
        #
        # Make the imported module <module_name> as "self.<module_name>"
        # or "<class_instance>.<module_name>" after instantiation.
        #
        module = globals()[module_name]
        setattr(self, module_name, module)
        #
        # Patch all methods in this class that start with a single "_" into the new module
        #
        for method_name in dir(self):
            if re.match(r'^_[^_]', method_name):
                function = getattr(super(), method_name)
                if callable(function):
                    setattr(module, method_name, function)
