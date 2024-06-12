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
print(conn.ipaddress.read("swis://Qpark500.q-park.com/Orion/IPAM.IPNode/IpNodeId=1259109"))

print(conn.ipsubnet.read("swis://Qpark500.q-park.com/Orion/IPAM.Subnet/SubnetId=3790,ParentId=3788"))
