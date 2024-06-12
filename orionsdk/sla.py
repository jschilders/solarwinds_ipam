def add_node_to_ip_vnqm(self, node_name):

    properties = {
        "NodeID": self.get_node_id(node_name),
        "Name": node_name,
        "IsHub": False,
        "IsAutoConfigured": True,
    }
    results = self.swis.create("Orion.IpSla.Sites", **properties)


def add_icmp_echo_ip_sla_operation_to_node(self, node_name, ip_sla_operation_number, ip_sla_name):

    properties = {
        "NodeID": self.get_node_id(node_name),
        "OperationTypeID": 5,
        "OperationType": "ICMP Echo",
        "IsAutoConfigured": False,
        "Frequency": 10,
        "IpSlaOperationNumber": ip_sla_operation_number,
        "OperationName": ip_sla_name,
    }
    results = self.swis.create("Orion.IpSla.Operations", **properties)
