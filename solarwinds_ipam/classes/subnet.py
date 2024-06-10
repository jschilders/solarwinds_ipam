from dataclasses import dataclass

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




