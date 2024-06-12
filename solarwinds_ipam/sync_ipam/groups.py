from solarwinds_ipam.classes import IpNodeStatus


# dummy functions to keed the IDE happy. Will be overridden later
# fmt: off
def _create(): pass
def _read(): pass
def _update(): pass
def _delete(): pass
def _query(): pass
def _invoke(): pass
def _build_query(): pass
# fmt: on


#
# Nodes C/R/U/D
#
def create(Caption: str, IPAddress: str, **properties: dict) -> str:
    properties["Caption"] = Caption
    properties["IPAddress"] = IPAddress
    return _create("Orion.Container", **properties)


def read(uri: str) -> dict:
    return _read(uri)


def update(uri: str, **properties: dict) -> None:
    return _update(uri, **properties)


def delete(uri: str) -> None:
    return _delete(uri)


#
# Nodes helper methods
#


# "SELECT ContainerID FROM Orion.Container WHERE Name = @group_name"
def get_uri(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Container", "Uri", kwargs)
    if result:
        return result[0].get("Uri")


def get_id(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Container", "ContainerID", kwargs)
    if result:
        return result[0].get("ContainerID")


def get_uri_and_id(**kwargs: dict) -> str:
    result: list = _build_query("Orion.Container", ["Uri", "ContainerID"], kwargs)
    if result:
        return result[0].get("Uri"), result[0].get("ContainerID")


def get_uri_from_id(ContainerID: int) -> str:
    params = {"ContainerID": ContainerID}
    result: list = _build_query("Orion.Container", "Uri", params)
    if result:
        return result[0].get("Uri")


def get_id_from_uri(uri: str) -> int:
    result: dict = _read(uri)
    if result:
        return result.get("ContainerID")


def exist(**kwargs: dict) -> bool:
    return get_id(**kwargs) is not None


def is_node_in_group(node_name, group_id):
    parameters = {"ContainerID": group_id, "FullName": node_name}
    result: list = _build_query("Orion.ContainerMembers", "Name", parameters)
    if result:
        return result[0].get("Name") is not None


def add_node_to_group(self, node_name, node_uri, group_id):
    member_definition = {"Name": node_name, "Definition": node_uri}
    return _invoke("Orion.Container", "AddDefinition", group_id, member_definition)


def add_group(
    group_name,
    owner="Core",
    refresh_frequency=60,
    status_rollup=0,  # 0 = Mixed status shows warning 1 = Show worst status 2 = Show best status
    group_description="",
    polling_enabled=True,
    group_members=None,
):

    return _invoke(
        "Orion.Container",
        "CreateContainer",
        group_name,
        owner,
        refresh_frequency,
        status_rollup,
        group_description,
        polling_enabled,
        group_members or [],
    )


def delete_group(group_id: int):
    _invoke("Orion.Container", "DeleteContainer", int(group_id))


def add_group_custom_property(self, property_name, description, value_type, size):
    """Add a new group custom property with the specified name and details.

    Args:
        property_name(string): Name of the new group property.
        description(string): Description for the new group property.
        value_type(string): Value type for the new group property (string, integer, datetime, single, double, boolean)
        size(integer): The maximum length for string value types.  Ignored for other value types.

    Returns:
        None.

    """

    return _invoke(
        "Orion.GroupCustomProperties",
        "CreateCustomProperty",
        property_name,
        description,
        value_type,
        size,
        "",
        "",
        "",
        "",
        "",
        "",
    )


def set_group_custom_property(group_uri, custom_property_name, custom_property_value):
    custom_property = {custom_property_name: custom_property_value}
    _update(group_uri + "/CustomProperties", **custom_property)
