import asyncio
from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import AsyncIPAM, SubnetType


async def main(**connection_parameters) -> None:
    async with AsyncIPAM(**connection_parameters) as my_session:

        uri = await my_session.ipaddress.get_uri(IPAddress="10.22.10.65")
        if uri:
            # Get the IP address info
            result = await my_session.ipaddress.read(uri)
            ip_address, alias = result["IPAddress"], result["Alias"]
            print(f"Start:    IP address {ip_address} has alias {result['Alias']!r}")

            # Change alias for IP Address
            await my_session.ipaddress.update(uri, Alias="Test Alias")

            # Check to see if it is indeed different
            result = await my_session.ipaddress.read(uri)
            print(f"Updated:  IP address {ip_address} has alias {result['Alias']!r}")

            # Change alias back to previous
            await my_session.ipaddress.update(uri, Alias=alias)

            # Check to see if it is indeed back to before
            result = await my_session.ipaddress.read(uri)
            print(f"Restored: IP address {ip_address} has alias {result['Alias']!r}")

        print(f"\n--- Find a subnet 10.136.82.64")
        uri = await my_session.ipsubnet.get_uri(Address="10.136.82.64")
        if uri:
            print(f"Found. {uri=}")
            subnet = await my_session.ipsubnet.read(uri)
            print(subnet)
        else:
            print("Not Found")

        # Retrieve address info and return to caller
        uri = await my_session.ipaddress.get_uri(IPAddress="10.136.82.2")
        if uri:
            return await my_session.ipaddress.read(uri)


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
