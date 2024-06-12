def get_list_of_custom_pollers_for_node(self, node_name):
    node_id = self.get_node_id(node_name)
    custom_pollers = self.swis.query(
        "SELECT CustomPollerName FROM Orion.NPM.CustomPollerAssignment WHERE NodeID " "= @node_id",
        node_id=node_id,
    )
    return custom_pollers["results"]


def remove_custom_poller_by_name(self, node_name, poller_name):
    node_id = self.get_node_id(node_name)

    custom_poller_id = self.swis.query(
        "SELECT CustomPollerID FROM Orion.NPM.CustomPollers WHERE UniqueName = " "@poller_name",
        poller_name=poller_name,
    )

    custom_poller_uri = self.swis.query(
        "SELECT Uri FROM Orion.NPM.CustomPollerAssignmentOnNode WHERE NodeID=@node_id AND CustomPollerID=@custom_poller_id",
        node_id=node_id,
        custom_poller_id=custom_poller_id["results"][0]["CustomPollerID"],
    )
    self.swis.delete(custom_poller_uri["results"][0]["Uri"])


def add_custom_poller_by_name(self, node_name, poller_name):
    node_id = self.get_node_id(node_name)
    custom_poller_id = self.swis.query(
        "SELECT CustomPollerID FROM Orion.NPM.CustomPollers WHERE UniqueName = @poller_name",
        poller_name=poller_name,
    )
    properties = {"NodeID": node_id, "customPollerID": custom_poller_id["results"][0]["CustomPollerID"]}
    self.swis.create("Orion.NPM.CustomPollerAssignmentOnNode", **properties)
