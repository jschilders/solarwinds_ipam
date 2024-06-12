def add_node_using_snmp_v3(
    self,
    node_name,
    ip_address,
    snmpv3_username,
    snmpv3_priv_method,
    snmpv3_priv_pwd,
    snmpv3_auth_method,
    snmpv3_auth_pwd,
):

    if not self.does_node_exist(node_name):
        # set up property bag for the new node
        properties = {
            "IPAddress": ip_address,
            "EngineID": 1,
            "ObjectSubType": "SNMP",
            "SNMPVersion": 3,
            "SNMPV3Username": snmpv3_username,
            "SNMPV3PrivMethod": snmpv3_priv_method,
            "SNMPV3PrivKeyIsPwd": True,
            "SNMPV3PrivKey": snmpv3_priv_pwd,
            "SNMPV3AuthMethod": snmpv3_auth_method,
            "SNMPV3AuthKeyIsPwd": True,
            "SNMPV3AuthKey": snmpv3_auth_pwd,
            "DNS": "",
            "SysName": "",
            "Caption": node_name,
        }

        # Create base node object.
        results = self.swis.create("Orion.Nodes", **properties)

        # Assign pollers to node.
        self.attach_poller_to_node(node_name, "N.Status.ICMP.Native")
        self.attach_poller_to_node(node_name, "N.Status.SNMP.Native", False)
        self.attach_poller_to_node(node_name, "N.ResponseTime.ICMP.Native")
        self.attach_poller_to_node(node_name, "N.ResponseTime.SNMP.Native", False)
        self.attach_poller_to_node(node_name, "N.Details.SNMP.Generic")
        self.attach_poller_to_node(node_name, "N.Uptime.SNMP.Generic")


def set_node_custom_property(self, node_name, custom_property_name, custom_property_value):
    node_uri = self.get_node_uri(node_name)
    custom_property = {custom_property_name: custom_property_value}
    self.swis.update(node_uri + "/CustomProperties", **custom_property)


def get_node_custom_properties(self, node_name):
    node_uri = self.get_node_uri(node_name)
    custom_properties = self.swis.read(node_uri + "/CustomProperties")
    return custom_properties
