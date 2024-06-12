from solarwinds_ipam.classes import IpNodeStatus


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
# Nodes C/R/U/D
#
def create(Caption: str, IPAddress: str, **properties: dict) -> str:
    properties["Caption"] = Caption
    properties["IPAddress"] = IPAddress
    return _create("Orion.Nodes", **properties)


def read(uri: str) -> dict:
    return _read(uri)


def update(uri: str, **properties: dict) -> None:
    return _update(uri, **properties)


def delete(uri: str) -> None:
    return _delete(uri)


#
# Nodes helper methods
#
def get_uri(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Nodes", "Uri", kwargs)
    if result:
        return result[0].get("Uri")


def get_id(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Nodes", "NodeID", kwargs)
    if result:
        return result[0].get("NodeID")


def get_uri_and_id(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Nodes", ["Uri", "NodeID"], kwargs)
    if result:
        return result[0].get("Uri"), result[0].get("NodeID")


def get_uri_from_id(NodeID: int) -> str:
    params = {"NodeID": NodeID}
    result: list = _build_query("Orion.Nodes", "Uri", params)
    if result:
        return result[0].get("Uri")


def get_id_from_uri(uri: str) -> int:
    result: dict = _read(uri)
    if result:
        return result.get("NodeID")


def exist(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Nodes", "NodeID", kwargs)
    if result:
        return result[0].get("NodeID")


def exist(**kwargs: dict) -> bool:
    return get_id(**kwargs) is not None
