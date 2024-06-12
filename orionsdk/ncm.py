def ncm_download_nodes_running_config(self, node_name):
    results = self.swis.query("SELECT NodeID FROM Cirrus.Nodes WHERE NodeCaption = @node_name", node_name=node_name)[
        "results"
    ]
    cirrus_node_id = results[0]["NodeID"]
    self.swis.invoke("Cirrus.ConfigArchive", "DownloadConfig", [cirrus_node_id], "Running")


def ncm_run_compliance_report(self, report_name):
    results = self.swis.query(
        "SELECT PolicyReportID FROM Cirrus.PolicyReports WHERE Name = @report_name", report_name=report_name
    )
    report_id = results["results"][0]["PolicyReportID"]
    self.swis.invoke("Cirrus.PolicyReports", "StartCaching", [report_id])


def add_node_to_ncm(self, node_name):
    results = self.swis.invoke("Cirrus.Nodes", "AddNodeToNCM", self.get_node_id(node_name))
