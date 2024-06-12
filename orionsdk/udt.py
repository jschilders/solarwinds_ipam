def add_node_to_udt(self, node_name):

    # add node at l2 to udt
    properties = {"NodeID": self.get_node_id(node_name), "Capability": "2", "Enabled": True}
    results = self.swis.create("Orion.UDT.NodeCapability", **properties)

    # add node at l3
    properties = {"NodeID": self.get_node_id(node_name), "Capability": "3", "Enabled": True}
    results = self.swis.create("Orion.UDT.NodeCapability", **properties)
