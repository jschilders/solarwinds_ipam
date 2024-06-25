from solarwinds_ipam.classes import IpNodeStatus


# dummy functions to keed the IDE happy. Will be overridden later
# fmt: off
async def _create(): pass
async def _read(): pass
async def _update(): pass
async def _delete(): pass
async def _query(): pass
async def _build_query(): pass
# fmt: on


#
# IP Address C/R/U/D
#
async def create(IPAddress: str, SubnetId: str, IPOrdinal: int, Status=IpNodeStatus.Reserved, **properties: dict) -> str:  # fmt: skip
    properties["IPAddress"] = IPAddress
    properties["SubnetId"] = SubnetId
    properties["IPOrdinal"] = IPOrdinal
    properties["Status"] = int(Status)
    return await _create("IPAM.IPNode", **properties)


async def read(uri: str) -> dict:
    return await _read(uri)


async def update(uri: str, **properties: dict) -> None:
    return await _update(uri, **properties)


async def delete(uri: str) -> None:
    return await _delete(uri)


#
# IP Node helper methods
#
async def get_uri(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.IPNode", "Uri", kwargs)
    if result:
        return result[0].get("Uri")


async def get_id(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.IPNode", "IpNodeId", kwargs)
    if result:
        return result[0].get("IpNodeId")


async def get_uri_and_id(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.IPNode", ["Uri", "IpNodeId"], kwargs)
    if result:
        return result[0].get("Uri"), result[0].get("IpNodeId")


async def get_parent(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.IPNode", "SubnetID", kwargs)
    if result:
        return result[0].get("SubnetID")


async def get_uri_from_id(IpNodeId: int) -> str:
    params = {"IpNodeId": IpNodeId}
    result: list = await _build_query("IPAM.IPNode", "Uri", params)
    if result:
        return result[0].get("Uri")


async def get_id_from_uri(uri: str) -> int:
    result: dict = await _read(uri)
    if result:
        return result.get("IpNodeId")


#
# Other helpers
#
async def get_addresses_in_subnet(SubnetId: int = None) -> list[dict]:
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
    params = {"SubnetId": SubnetId}
    result: list = await _build_query("IPAM.IPNode", fields, params)
    if result:
        return [ip_address for ip_address in result]  # noqa: C416
