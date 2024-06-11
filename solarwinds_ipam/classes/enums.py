from enum import IntEnum


class IpNodeStatus(IntEnum):
    Used = 1
    Available = 2
    Reserved = 4
    Transient = 8
    Blocked = 16


class IpAllocPolicy(IntEnum):
    Static = 1
    Dynamic = 2


class SubnetType(IntEnum):
    Root = 1
    Group = 2
    Supernet = 4
    Subnet = 8
    Internal = 16
