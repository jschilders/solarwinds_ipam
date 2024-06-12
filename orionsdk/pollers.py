def is_poller_attached_to_node(self, node_name, poller_name):

    net_object_id = str(self.get_node_id(node_name))
    net_object = "N:" + net_object_id

    results = self.swis.query(
        "SELECT PollerType FROM Orion.Pollers WHERE NetObject = @net_object AND PollerType " "= @poller_name",
        net_object=net_object,
        poller_name=poller_name,
    )

    return results["results"] is not None


def attach_poller_to_node(self, node_name, poller_name, enabled=True):

    net_object_id = str(self.get_node_id(node_name))
    net_object = "N:" + net_object_id

    properties = {
        "PollerType": poller_name,
        "NetObject": net_object,
        "NetObjectType": "N",
        "NetObjectID": net_object_id,
        "Enabled": enabled,
    }

    results = self.swis.create("Orion.Pollers", **properties)
