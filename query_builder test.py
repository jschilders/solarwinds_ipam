from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import IPAM, SubnetType


def main(**connection_parameters) -> None:
    with IPAM(**connection_parameters) as my_session:

        table = "IPAM.Subnet"
        fields_to_return = [
            "ParentID",
            "SubnetID",
            #    'Uri',
            "CIDR",
            "GroupType",
        ]
        query_parameters = {
            "Address": "10.136.82.0",
            #'CIDR':      '24',
            #'GroupType': 4
        }
        order_by = {
            "CIDR": "DESC",
            #            'Address': 'ASC'
        }
        r = my_session._build_query(table, fields_to_return, query_parameters, order_by)

        print(r)


if __name__ == "__main__":
    load_dotenv()
    connection_parameters = {
        "server": getenv("SERVER") or "",
        "port": getenv("PORT") or 17778,
        "username": getenv("USERNAME") or "",
        "password": getenv("PASSWORD") or "",
        "verify": False,
    }
    r = main(**connection_parameters)
    print(r)
