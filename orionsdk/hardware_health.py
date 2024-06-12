def enable_hardware_health_on_node(self, node_name):
    net_object_id = str(self.get_node_id(node_name))
    net_object = "N:" + net_object_id
    results = self.swis.invoke("Orion.HardwareHealth.HardwareInfo", "EnableHardwareHealth", net_object, 9)
