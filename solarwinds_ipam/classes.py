from enum import IntEnum
from dataclasses import dataclass


class IpNodeStatus(IntEnum):
    Used        = 1
    Available   = 2
    Reserved    = 4
    Transient   = 8
    Blocked     = 16


class IpAllocPolicy(IntEnum):
    Static      = 1
    Dynamic     = 2


class SubnetType(IntEnum):
    Root        =  1
    Group       =  2
    Supernet    =  4
    Subnet      =  8
    Internal    = 16


@dataclass
class IpSubnet:
    SubnetId:int
    ParentId:int
    Address:str
    AddressN:str
    AddressMask:str
    CIDR:int
    AllocSize:int
    AllocSizeN:float
    FriendlyName:str
    Comments:str
    VLAN:str  # Or int?
    Location:str
    LastDiscovery:str           # '2024-04-27T14:13:29.193'
    Status:int
    ScanInterval:int
    PercentUsed:float
    TotalCount:int
    UsedCount:int
    AvailableCount:int
    ReservedCount:int
    TransientCount:int
    HasLicenceOverflow:bool
    GroupIconPrefix:str
    StatusName:str
    StatusShortDescription:str
    StatusRanking:int
    StatusIconPostfix:str
    GroupTypeText:str
    AccountID:str
    Role:str
    GroupType:int
    Distance:int
    SubnetStructureChanged:str          #'2024-03-26T14:03:51.393Z'
    DisplayName:str
    Description:str
    InstanceType:str
    Uri:str
    InstanceSiteId:int

    def __repr__(self):
        return f"<IpSubnet {self.Address}/{self.CIDR}>"



class IpNode:
    IpNodeId: int                       # Read-Only
    SubnetId: int                       # Read-Only, required
    IpOrdinal: int                      # required
    SubnetAddress: str                  # 
    SubnetMask: str                     # 
    SubnetCIDR: int                     # 
    IPAddress: str | None = None        # Read-Only, required
    IPMapped: str | None = None         # must be  None when Status is 'Available'
    Alias: str | None = None            # must be  None when Status is 'Available'
    MAC: str | None = None              # must be  None when Status is 'Available'
                                        # must be defined when DHCP Reservation is going to be created
                                        # MAC Address must follow this format: '00:00:00:00:00:00'
    DnsBackward: str | None = None      # Hostname, must be  None when Status is 'Available'
    DhcpClientName: str | None = None   # must be  None when Status is 'Available'
                                        # must be defined when DHCP Reservation is going to be created
    Comments: str | None = None         # must be  None when Status is 'Available'
    ResponseTime: int                   # Read-Only
    SkipScan: bool                      # Default: False
    Status: IpNodeStatus                # required, default: Available  
    AllocPolicy: IpAllocPolicy          # Default: Static
    Uri: str


    def __init__(self, **kwargs):
        self._raw = kwargs
        self.raw_to_attribs()


    def raw_to_attribs(self):
        self.IpNodeId =         self._raw.get('IpNodeId')
        self.SubnetId =         self._raw.get('SubnetId')
        self.IPAddress =        self._raw.get('IPAddress')
        self.IPMapped =         self._raw.get('IPMapped')
        self.Alias =            self._raw.get('Alias')
        self.MAC =              self._raw.get('MAC')
        self.DnsBackward =      self._raw.get('DnsBackward')
        self.DhcpClientName =   self._raw.get('DhcpClientName')
        self.Comments =         self._raw.get('Comments')
        self.ResponseTime =     self._raw.get('ResponseTime')
        self.SkipScan =         self._raw.get('SkipScan', False)
        self.Status =           IpNodeStatus(self._raw.get('Status',2))
        self.AllocPolicy =      IpAllocPolicy(self._raw.get('AllocPolicy', 1))
        self.Uri =              self._raw.get('Uri')


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
            print(f"{self._raw.get('Status', 2)} = {int(self.Status)}")
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