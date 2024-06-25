from solarwinds_ipam.classes.enums import SubnetType, IpSubnetStatus


class IPSubnet:
    # fmt: off

    #
    # Fields according to documentation
    #
    SubnetId: int			                        # Read-Only
    ParentId: int = 0
    Address: str = ""	                            # Required
    AddressMask: str = ""	                        # Read-Only
    CIDR: int		                                # Read-Only, required
                                                    # Address CIDR must be greater than 21 and less than or equal to 32.
    FriendlyName: str = ""                          # Required. "Address"/"CIDR". Auto-created?
    Comments: str =""
    VLAN: str =""
    Location: str =""
    ScanInterval: int = 240
    Status: IpSubnetStatus = IpSubnetStatus.Up      # Extra field
    GroupType: SubnetType = SubnetType.Subnet       # Extra field
    Uri: str =""                                    # Extra field

    # fmt: on

    #
    # Extra fields returned with a standard "read" operation
    #
    AddressN: str
    AllocSize: int
    AllocSizeN: float
    LastDiscovery: str

    PercentUsed: float
    TotalCount: int
    UsedCount: int
    AvailableCount: int
    ReservedCount: int
    TransientCount: int
    HasLicenceOverflow: bool
    GroupIconPrefix: str
    StatusName: str
    StatusShortDescription: str
    StatusRanking: int
    StatusIconPostfix: str
    GroupTypeText: str
    AccountID: str
    Role: str
    Distance: int
    SubnetStructureChanged: str
    #
    DisplayName: str
    Description: str
    InstanceType: str
    InstanceSiteId: int

    def __init__(self, **kwargs):
        self._raw = kwargs
        self.raw_to_attribs()

    def __repr__(self):
        return f"<IPSubnet {self.Address}/{self.CIDR}>"

    def as_dict(self):
        return {keyname: getattr(self, keyname) for keyname in self.__annotations__ if keyname in vars(self)}

    def raw_to_attribs(self):
        for i in self.__annotations__:
            print(i)
            setattr(self, i, self._raw.get(i))

        # self.Status = IpSubnetStatus(self._raw.get("Status",2))
        # self.GroupType = SubnetType(self._raw.get("SubnetType", 1))

    def prepare_updates(self):
        updates = {}
        ...
        return updates

    # def refresh(self):
    #     self._raw = self._read(self._raw["Uri"])
    #     self.raw_to_attribs()
    #     return self

    # def save(self):
    #     updates = self.prepare_updates()

    #     if self.SubnetId and self.Uri:
    #         self.update(self.Uri, **updates)
    #         return self
    #     else:
    #         # assert Address is valid
    #         # assert SubnetId is valid
    #         # Check if the subnet address already exist
    #         # overwrite if it exists
    #         # create a new IP if it doesn't
    #         # self.Uri = self.create(self.IPAddress, self.SubnetId, self.IpOrdinal, status=self.Status, **updates)
    #         return self


_raw = {
    "SubnetId": 3790,
    "ParentId": 3788,
    "Address": "10.136.82.64",
    "AddressN": None,
    "AddressMask": "255.255.255.192",
    "CIDR": 26,
    "AllocSize": 64,
    "AllocSizeN": 100.0,
    "FriendlyName": "10.136.82.64/26",
    "Comments": "PMS",
    "VLAN": "102",
    "Location": "BETOCE",
    "LastDiscovery": "2024-04-29T13:13:29.04",
    "Status": 1,
    "ScanInterval": 60,
    "PercentUsed": 10.9375,
    "TotalCount": 64,
    "UsedCount": 5,
    "AvailableCount": 57,
    "ReservedCount": 2,
    "TransientCount": 0,
    "HasLicenceOverflow": False,
    "GroupIconPrefix": "subnet",
    "StatusName": "Up",
    "StatusShortDescription": "Up",
    "StatusRanking": 500,
    "StatusIconPostfix": "up",
    "GroupTypeText": "Subnet",
    "AccountID": "api_user",
    "Role": "SiteAdmin",
    "GroupType": 8,
    "Distance": 1,
    "SubnetStructureChanged": "2024-03-26T14:03:51.393Z",
    "DisplayName": "10.136.82.64/26",
    "Description": None,
    "InstanceType": "IPAM.Subnet",
    "Uri": "swis://Qpark500.q-park.com/Orion/IPAM.Subnet/SubnetId=3790,ParentId=3788",
    "InstanceSiteId": 0,
}
