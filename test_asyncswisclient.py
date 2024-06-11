import asyncio
from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import AsyncIPAM, SubnetType


async def main(**connection_parameters) -> None:
    print(connection_parameters)
    async with AsyncIPAM(**connection_parameters) as my_session:
        result = await my_session._query_node(ip_address="10.136.82.2")
        if result:
            uri = result.get("Uri")
            return await my_session._read(uri)


if __name__ == "__main__":
    load_dotenv()
    connection_parameters = {
        "server": getenv("SERVER") or "",
        "port": getenv("PORT") or 17778,
        "username": getenv("USERNAME") or "",
        "password": getenv("PASSWORD") or "",
        "verify": False,
    }
    r = asyncio.run(main(**connection_parameters))
    print(r)
