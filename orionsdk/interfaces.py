def get_list_of_interfaces(self, node_name):
    node_id = self.get_node_id(node_name)
    list_interfaces_names = self.swis.query(
        "SELECT Name FROM Orion.NPM.Interfaces WHERE NodeID " "= @node_id", node_id=node_id
    )
    if list_interfaces_names["results"]:
        return list_interfaces_names["results"]


def remove_interface(self, node_name, interface_name):
    interface_uri = self.get_interface_uri(node_name, interface_name)
    if self.does_interface_exist(node_name, interface_name):
        self.swis.delete(interface_uri)
        return True
    else:
        return False


def get_interface_uri(self, node_name, interface_name):
    node_id = self.get_node_id(node_name)
    interface_uri = self.swis.query(
        "SELECT Uri FROM Orion.NPM.Interfaces WHERE NodeID=@node_id AND " "InterfaceName=@interface_name",
        node_id=node_id,
        interface_name=interface_name,
    )
    if interface_uri["results"]:
        return interface_uri["results"][0]["Uri"]


def get_interface_id(self, node_name, interface_name):
    node_id = self.get_node_id(node_name)
    interface_id = self.swis.query(
        "SELECT InterfaceID FROM Orion.NPM.Interfaces WHERE NodeID=@node_id AND " "Name = @interface_name",
        node_id=node_id,
        interface_name=interface_name,
    )
    if interface_id["results"]:
        return interface_id["results"][0]["InterfaceID"]


def does_interface_exist(self, node_name, interface_name):
    if self.get_interface_id(node_name, interface_name):
        return True
    else:
        return False


def get_discovered_interfaces(self, node_name):
    node_id = self.get_node_id(node_name)
    discovered_interfaces = self.swis.invoke("Orion.NPM.Interfaces", "DiscoverInterfacesOnNode", node_id)
    return discovered_interfaces["DiscoveredInterfaces"]


def add_interface(self, node_name, interface_name):
    node_id = self.get_node_id(node_name)
    discovered_interfaces = self.get_discovered_interfaces(node_name)
    discovered_interface = [x for x in discovered_interfaces if x["Caption"].startswith(interface_name)]

    if discovered_interface:
        self.swis.invoke(
            "Orion.NPM.Interfaces", "AddInterfacesOnNode", node_id, discovered_interface, "AddDefaultPollers"
        )
