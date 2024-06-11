from solarwinds_ipam.classes import IpNodeStatus


# dummy functions to keed the IDE happy. Will be overridden later
def _create():
    pass


def _read():
    pass


def _update():
    pass


def _delete():
    pass


def _query():
    pass


def _build_query():
    pass


#
# IP Address C/R/U/D
#
def create(
    IPAddress: str,
    SubnetId: str,
    IPOrdinal: int,
    Status=IpNodeStatus.Reserved,
    **properties: dict
) -> str:
    properties["IPAddress"] = IPAddress
    properties["SubnetId"] = SubnetId
    properties["IPOrdinal"] = IPOrdinal
    properties["Status"] = int(Status)
    return _create("IPAM.IPNode", **properties)


def read(uri: str) -> dict:
    return _read(uri)


def update(uri: str, **properties: dict) -> None:
    return _update(uri, **properties)


def delete(uri: str) -> None:
    return _delete(uri)


#
# IP Address helper methods
#
def get_uri(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.IPNode", "Uri", kwargs)
    if result:
        return result[0].get("Uri")


def get_id(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.IPNode", "IpNodeId", kwargs)
    if result:
        return result[0].get("IpNodeId")


def get_uri_and_id(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.IPNode", ["Uri", "IpNodeId"], kwargs)
    if result:
        return result[0].get("Uri"), result[0].get("IpNodeId")


def get_parent(**kwargs: dict) -> str:
    result: list = _build_query("IPAM.IPNode", "SubnetID", kwargs)
    if result:
        return result[0].get("SubnetID")


def get_uri_from_id(ipaddress_id: int) -> str:
    params = {"IpNodeId": ipaddress_id}
    result: list = _build_query("IPAM.IPNode", "Uri", params)
    if result:
        return result[0].get("Uri")


def get_id_from_uri(uri: str) -> int:
    result: dict = _read(uri)
    if result:
        return result.get("IpNodeId")


#
# Other helpers
#
def get_addresses_in_subnet(subnet_id: int = None) -> list[dict]:
    fields = [
        "IpNodeId",
        "SubnetId",
        "IPAddress",
        "IPMapped",
        "Alias",
        "MAC",
        "DnsBackward",
        "DhcpClientName",
        "Comments",
        "ResponseTime",
        "SkipScan",
        "Status",
        "AllocPolicy",
        "Uri",
    ]
    params = {"SubnetId": subnet_id}
    result: list = _build_query("IPAM.IPNode", fields, params)
    if result:
        return [ip_address for ip_address in result]
