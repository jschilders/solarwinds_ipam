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

s: IPAM = IPAM(**connection_parameters)
print(s.ipaddress.read("swis://Qpark500.q-park.com/Orion/IPAM.IPNode/IpNodeId=1259109"))

print(s.ipaddress.get_uri_from_id(1259109))

print(s.ipaddress.get_uri(IPAddress="10.22.10.65"))

print(s.ipaddress.get_id(IPAddress="10.136.82.2"))

p = s.ipaddress.get_parent(IPAddress="10.136.82.2")
print(p)

print(s.ipaddress.get_addresses_in_subnet(p))
