from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import IPAM

load_dotenv()


connection_parameters = {
    "server": getenv("SERVER") or "",
    "port": getenv("PORT") or 17778,
    "username": getenv("USERNAME") or "",
    "password": getenv("PASSWORD") or "",
    "verify": False,
}

conn: IPAM = IPAM(**connection_parameters)

pf_uid = conn.ncm_nodes.get_pfuid(NodeCaption="UKSHRS-SW-1")
print(f"{pf_uid=}")


uri = conn.ncm_nodes.get_uri(NodeCaption="UKSHRS-SW-1")
print(f"{uri=}")

node_id = conn.ncm_nodes.get_id(NodeCaption="UKSHRS-SW-1")
print(f"{node_id=}")

uri_and_id = conn.ncm_nodes.get_uri_and_id(NodeCaption="UKSHRS-SW-1")
print(f"{uri_and_id=}")

new_uri = conn.ncm_nodes.get_uri_from_id(node_id)
print(f"{new_uri=}")

new_id = conn.ncm_nodes.get_id_from_uri(uri)
print(f"{new_id=}")

print(f"(uri, id) == uri_and_id {(uri, node_id) == uri_and_id}")
print(f"uri == new_uri {uri==new_uri}")
print(f"id  == new_id  {node_id==new_id}")

print(conn.ncm_nodes.read(uri))
