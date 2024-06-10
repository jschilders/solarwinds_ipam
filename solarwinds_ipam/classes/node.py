from dataclasses import dataclass
from solarwinds_ipam.classes.enums import IpNodeStatus, IpAllocPolicy
class Node:
    #
    # Fields according to documentation
    #
    IpNodeId:int = 0                                    # Read-Only
    SubnetId:int = 0                                    # Read-Only, required
    #  IpOrdinal: int                                   # required
    ## SubnetAddress: str                               #
    ## SubnetMask: str                                  #
    ## SubnetCIDR: int                                  #
    IPAddress:str  = ''                                 # Read-Only, required
    IPMapped:str = ''                                   # must be None when Status is 'Available'
    Alias:str = ''                                      # must be None when Status is 'Available'
    MAC:str = ''                                        # must be None when Status is 'Available'
                                                        # must be defined when DHCP Reservation is going to be created
                                                        # MAC Address must follow this format: '00:00:00:00:00:00'
    DnsBackward:str = ''                                # Hostname, must be  None when Status is 'Available'
    test1:str
    DhcpClientName:str = ''                             # must be None when Status is 'Available'
                                                        # must be defined when DHCP Reservation is going to be created
    Comments:str = ''                                   # must be None when Status is 'Available'
    ResponseTime:int = 0                                # Read-Only
    SkipScan:bool = False                               # Default: False
    Status:IpNodeStatus =IpNodeStatus.Available         # required, default: Available
    AllocPolicy:IpAllocPolicy = IpAllocPolicy.Static    # Default: Static
    Uri:str = ''


    def __init__(self, **kwargs):
        self._raw = kwargs
        self.raw_to_attribs()


    def raw_to_attribs(self):

        for i in self.__annotations__:
            print(i)
            setattr(self, i, self._raw.get(i))

        ##self.Status =           IpNodeStatus(self._raw.get('Status',2))
        ##self.AllocPolicy =      IpAllocPolicy(self._raw.get('AllocPolicy', 1))


    def prepare_updates(self):
        updates = {}

        if self.Status == IpNodeStatus.Available:
            self.IPMapped = self.Alias = self.MAC = self.DnsBackward = self.DhcpClientName = self.Comments = None

        if self.IPMapped != self._raw.get('IPMapped'):
            updates['IPMapped'] = self.IPMapped

        if self.Alias != self._raw.get('Alias'):
            updates['Alias'] = self.Alias

        if self.MAC != self._raw.get('MAC'):
            updates['MAC'] = self.MAC

        if self.DnsBackward != self._raw.get('DnsBackward'):
            updates['DnsBackward'] = self.DnsBackward

        if self.DhcpClientName != self._raw.get('DhcpClientName'):
            updates['DhcpClientName'] = self.DhcpClientName

        if self.Comments != self._raw.get('Comments'):
            updates['Comments'] = self.Comments

        if self.SkipScan != self._raw.get('SkipScan', False):
            updates['SkipScan'] = self.SkipScan

        if int(self.Status) != self._raw.get('Status', 2):
            updates['Status'] = int(self.Status)

        if int(self.AllocPolicy) != self._raw.get('AllocPolicy', 1):
            updates['AllocPolicy'] = int(self.AllocPolicy)

        return updates


    def __repr__(self):
        return f"<IpNode {self.IPAddress}>"

    def as_dict(self):
        return { keyname:getattr(self,keyname) for keyname in self.__annotations__ if keyname in vars(self) }


    #
    #
    #
    def refresh(self):
        self._raw = self._read(self._raw['Uri'])
        self.raw_to_attribs()
        return self


    def save(self):
        updates = self.prepare_updates()

        if self.IpNodeId and self.Uri:
            self.update(self.Uri, **updates)
            return self
        else:
            # assert IPAddress is valid
            # assert SubnetId is valid
            # assign a value to ordinal somehow
            # Check if the IP address already exist
            # force overwrite if it exists
            # create a new IP if it doesn't

            self.calculate_ordinal()

            #self.Uri = self.create(self.IPAddress, self.SubnetId, self.IpOrdinal, status=self.Status, **updates)
            return self


    def calculate_ordinal(self):
        def to_int(ip_address):
            return sum(int(octet)*256**counter for counter, octet in enumerate(reversed(ip_address.split('.'))))

        if not getattr(self, 'SubnetAddress', None):
            self.SubnetAddress, self.SubnetMask, self.SubnetCIDR = self.get_subnet_address()

        self.IpOrdinal = to_int(self.IPAddress) - to_int(self.SubnetAddress)
        return self.IpOrdinal



"""


>>> i.__annotations__.keys()

# All variables defined in class
['IpNodeId', 'SubnetId', 'IpOrdinal', 'SubnetAddress', 'SubnetMask', 'SubnetCIDR', 'IPAddress', 'IPMapped', 'Alias', 'MAC', 'DnsBackward', 'DhcpClientName', 'Comments', 'ResponseTime', 'SkipScan', 'Status', 'AllocPolicy', 'Uri']

>>> vars(i).keys()

['_raw', 'IpNodeId', 'SubnetId', 'IPAddress', 'IPMapped', 'Alias', 'MAC', 'DnsBackward', 'DhcpClientName', 'Comments', 'ResponseTime', 'SkipScan', 'Status', 'AllocPolicy', 'Uri']


[ IpOrdinal, IPMapped, Alias, MAC, DnsBackward, test1, DhcpClientName, Comments, SkipScan, Status, AllocPolicy, Uri ] 




    [ IpOrdinal, IPMapped, Alias, MAC, DnsBackward, test1, DhcpClientName, Comments, SkipScan, Status, AllocPolicy, Uri ] 
    
    raw = {
    'IpNodeId': 1259108,
    'SubnetId': 3789,
    'IPOrdinal': 2,
    'IPAddress': '10.136.82.2',
    'IPAddressN': '0252880a-0000-0000-0000-000000000000',
    'IPMapped': None,
    'IPMappedN': None,
    'Alias': 'Changed Alias',
    'MAC': '',
    'DnsBackward': 'PGW-1',
    'DhcpClientName': '',
    'SysName': '',
    'Description': '',
    'Contact': '',
    'Location': '',
    'SysObjectID': '',
    'Vendor': '',
    'VendorIcon': None,
    'MachineType': '',
    'Comments': 'PGW-1',
    'ResponseTime': 29,
    'LastBoot': None,
    'LastSync': '2024-04-29T15:56:22.073',
    'LastCredential': '00000000-0000-0000-0000-000000000000',
    'Status': 1,
    'AllocPolicy': 1,
    'SkipScan': False,
    'LeaseExpires': None,
    'DnsBy': 12288,
    'MacBy': 0,
    'StatusBy': 0,
    'SystemDataBy': 0,
    'DisplayName': '10.136.82.2',
    'InstanceType': 'IPAM.IPNode',
    'Uri': 'swis://Qpark500.q-park.com/Orion/IPAM.IPNode/IpNodeId=1259108',
    'InstanceSiteId': 0
}

"""