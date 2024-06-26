from solarwinds_ipam.classes import SubnetType


# dummy functions to keed the IDE happy. Will be overridden later
# fmt: off
def _create(): pass
def _read(): pass
def _update(): pass
def _delete(): pass
def _query(): pass
def _build_query(): pass
# fmt: on


#
# IP Group C/R/U/D
#
def create(FriendlyName: str = "", ParentId: int = 0, GroupType: SubnetType = SubnetType.Group, **properties: dict) -> str:  # fmt: skip
    properties.setdefault("Address", "0.0.0.0")
    properties.setdefault("CIDR", 32)
    properties.setdefault("ParentId", ParentId)
    properties.setdefault("FriendlyName", FriendlyName)
    if GroupType != SubnetType.Subnet:
        uri = _create("IPAM.Subnet", **properties)
        # print(f"Change GroupType to {GroupType} ({int(GroupType)})")
        _update(uri, GroupType=int(GroupType))
        return uri
    else:
        return _create("IPAM.Subnet", **properties)


def read(uri: str) -> dict:
    return _read(uri)


def update(uri: str, **properties: dict) -> None:
    return _update(uri, **properties)


def delete(uri: str) -> None:
    return _delete(uri)


#
# # Group helper methods
#
def get_uri(**kwargs: dict) -> str:
    kwargs = {"GroupType": int(SubnetType.Group), **kwargs}
    result: list = _build_query("IPAM.Subnet", "Uri", kwargs)
    if result:
        return result[0].get("Uri")


def get_id(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.Subnet", "SubnetID", kwargs)
    if result:
        return result[0].get("SubnetID")


def get_uri_and_id(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.Subnet", ["Uri", "SubnetID"], kwargs)
    if result:
        return result[0].get("Uri"), result[0].get("SubnetID")


def get_parent(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.Subnet", "ParentID", kwargs)
    if result:
        return result[0].get("ParentID")


def get_uri_from_id(subnet_id: int) -> str:
    params = {"SubnetID": subnet_id}
    result: list = _build_query("IPAM.Subnet", "Uri", params)
    if result:
        return result[0].get("Uri")


def get_id_from_uri(uri: str) -> int:
    result: dict = _read(uri)
    if result:
        return result.get("SubnetId")


def get_comment(FriendlyName: str = None) -> str:
    params: dict = {"FriendlyName": FriendlyName}
    result: list = _build_query("IPAM.Subnet", "Comments", params)
    if result:
        return result[0].get("Comments")
