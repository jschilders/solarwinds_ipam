def does_dependency_exist(self, dependency_name):
    return self.get_dependency_id(dependency_name) is not None


def get_dependency_id(self, dependency_name):
    dependency_id = self.swis.query(
        "SELECT DependencyId FROM Orion.Dependencies WHERE Name = @dependency_name",
        dependency_name=dependency_name,
    )

    if dependency_id["results"]:
        return dependency_id["results"][0]["DependencyId"]


def add_dependency(self, dependency_name, parent_name, child_name):

    if not self.does_dependency_exist(dependency_name):
        if self.does_node_exist(parent_name):
            # The parent is a node.
            parent_id = self.get_node_id(parent_name)
            parent_uri = self.get_node_uri(parent_name)
            parent_entity_type = "Orion.Nodes"
        elif self.does_group_exist(parent_name):
            # The parent is a group.
            parent_id = self.get_group_id(parent_name)
            parent_uri = self.get_group_uri(parent_name)
            parent_entity_type = "Orion.Groups"
        else:
            return False

        if self.does_node_exist(child_name):
            # The child is a node.")
            child_id = self.get_node_id(child_name)
            child_uri = self.get_node_uri(child_name)
            child_entity_type = "Orion.Nodes"
        elif self.does_group_exist(child_name):
            # The child is a group.")
            child_id = self.get_group_id(child_name)
            child_uri = self.get_group_uri(child_name)
            child_entity_type = "Orion.Groups"
        else:
            return False

        properties = {
            "Name": dependency_name,
            "ParentUri": parent_uri,
            "ParentEntityType": parent_entity_type,
            "ParentNetObjectId": parent_id,
            "ChildUri": child_uri,
            "ChildEntityType": child_entity_type,
            "ChildNetObjectId": child_id,
        }

        self.swis.create("Orion.Dependencies", **properties)
