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
# IP Subnet C/R/U/D
#
async def create(Address: str, CIDR: str, ParentId: int = 0, **properties: dict) -> str:
    properties["Address"] = Address
    properties["CIDR"] = CIDR
    properties["ParentId"] = ParentId
    return await _create("IPAM.Subnet", **properties)


async def read(uri: str) -> dict:
    return await _read(uri)


async def update(uri: str, **properties: dict) -> None:
    return await _update(uri, **properties)


async def delete(uri: str) -> None:
    return await _delete(uri)


#
# IP subnet helper methods
#
async def get_uri(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.Subnet", "Uri", kwargs)
    if result:
        return result[0].get("Uri")


async def get_id(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.Subnet", "SubnetID", kwargs)
    if result:
        return result[0].get("SubnetID")


async def get_uri_and_id(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.Subnet", ["Uri", "SubnetID"], kwargs)
    if result:
        return result[0].get("Uri"), result[0].get("SubnetID")


async def get_parent(**kwargs: dict) -> str:
    result: list = await _build_query("IPAM.Subnet", "ParentID", kwargs)
    if result:
        return result[0].get("ParentID")


async def get_uri_from_id(subnet_id: int) -> str:
    params = {"SubnetID": subnet_id}
    result: list = await _build_query("IPAM.Subnet", "Uri", params)
    if result:
        return result[0].get("Uri")


async def get_id_from_uri(uri: str) -> int:
    result: dict = await _read(uri)
    if result:
        return result.get("SubnetId")


async def get_subnet_address(subnet_id: int) -> str:
    fields: list = ["Address", "AddressMask", "CIDR"]
    params: dict = {"SubnetID": subnet_id}
    result: list = await _build_query("IPAM.Subnet", fields, params)
    if result:
        return (
            result[0].get("Address"),
            result[0].get("AddressMask"),
            result[0].get("CIDR"),
        )
