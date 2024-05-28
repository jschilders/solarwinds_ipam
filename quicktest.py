from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import IPAM


load_dotenv()

connection_parameters = {
    'server':   getenv('SERVER') or '',
    'port':     getenv('PORT') or 17778,
    'username': getenv('USERNAME') or '',
    'password': getenv('PASSWORD') or '',
    'verify':   False
}

s = IPAM(**connection_parameters)
r = s.node.read('swis://Qpark500.q-park.com/Orion/IPAM.IPNode/IpNodeId=1259108')
print(r)


