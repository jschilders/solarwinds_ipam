from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import IPAM, SubnetType


def main(**connection_parameters) -> None:
    with IPAM(**connection_parameters) as my_session:

        uri = my_session.ipaddress.get_uri(IPAddress="10.22.10.65")
        if uri:
            # Get the IP address info
            result = my_session.ipaddress.read(uri)
            ip_address, alias = result["IPAddress"], result["Alias"]
            print(f"Start:    IP address {ip_address} has alias {result['Alias']!r}")

            # Change alias for IP Address
            my_session.ipaddress.update(uri, Alias="Test Alias")

            # Check to see if it is indeed different
            result = my_session.ipaddress.read(uri)
            print(f"Updated:  IP address {ip_address} has alias {result['Alias']!r}")

            # Change alias back to previous
            my_session.ipaddress.update(uri, Alias=alias)

            # Check to see if it is indeed back to before
            result = my_session.ipaddress.read(uri)
            print(f"Restored: IP address {ip_address} has alias {result['Alias']!r}")

        id = my_session.ipaddress.get_id(IPAddress="10.136.82.2")
        if id:
            print(f"Found ID {id} for address 10.136.82.2")

            uri = my_session.ipaddress.get_uri_from_id(id)
            print(f"Uri for this address is {uri}")

            id = my_session.ipaddress.get_id_from_uri(uri)
            print(f"And back to ID: {id}")

        parent = my_session.ipaddress.get_parent(IPAddress="10.136.82.2")
        if parent:
            print(f"Parent subnet for address is {parent}")
            result = my_session.ipaddress.get_addresses_in_subnet(parent)
            print(f"Other address in this subnet:")
            print(result[:3])

        # todo: tests for
        #       ipaddress.delete, ipaddress.create,

        print(f"\n--- Find a subnet 10.136.82.64")
        uri = my_session.ipsubnet.get_uri(Address="10.136.82.64")
        if uri:
            print(f"Found. {uri=}")
            subnet = my_session.ipsubnet.read(uri)
            print(subnet)
        else:
            print("Not Found")

        print(f"\n--- Find parent subnet ID of subnet 10.136.82.64")
        id = my_session.ipsubnet.get_parent(Address="10.136.82.64")
        if id:
            print(f"Found. {id=}")
            subnet = my_session.ipsubnet.get_subnet_address(id)
            print(f"Subnet info for ID {id} is {subnet}")
        else:
            print("Not Found")

        print(f"\n--- Find a subnet 10.136.82.0")
        # Note that this will find the SUBnet.
        # There is also a SUPERnet with the same name.
        uri = my_session.ipsubnet.get_uri(Address="10.136.82.0")
        if uri:
            print(f"Found. {uri=}")
        else:
            print("Not Found")

        print(f"\n--- Find a supernet 10.136.82.0")
        # Note that this will find the SUPERnet.
        # There is also a SUBnet with the same name.
        uri = my_session.ipsubnet.get_uri(Address="10.136.82.0", GroupType=SubnetType.Supernet)
        if uri:
            print(f"Found. {uri=}")
        else:
            print("Not Found")

        print(f"\n--- Find a subnet 10.16.0.0 with an explicid mask length of /26")
        uri = my_session.ipsubnet.get_uri(Address="10.16.0.0", CIDR=26)
        if uri:
            print(f"Found, {uri=}")
            print(f"Note that you can use read(uri) only on subnets, not on supernets")
            print(my_session.ipsubnet.read(uri))
        else:
            print("Not Found")

        print(f"\n--- Find Uri and ID for subnet 10.136.82.64")
        # Note that this will find the SUBnet.
        # There is also a SUPERnet with the same name.
        uri, id = my_session.ipsubnet.get_uri_and_id(Address="10.136.82.64")
        if uri and id:
            print(f"Found. {uri=} {id=}")

            print("Uri from ID:", my_session.ipsubnet.get_uri_from_id(id))
            print("Uri from ID:", my_session.ipsubnet.get_uri_from_id(id) == uri)

            print("ID from Uri:", my_session.ipsubnet.get_id_from_uri(uri))
            print("ID from Uri:", my_session.ipsubnet.get_id_from_uri(uri) == id)

        else:
            print("Not Found")

        print(f"\n*** Testing C/R/U/D")
        # Delete subnet if it already exists from previous tests
        uri = my_session.ipsubnet.get_uri(Address="10.99.10.0", CIDR=24)
        if uri:
            my_session.ipsubnet.delete(uri)
            print(f"\n*!!! Existing subnet 10.99.10.0/24 deleted")
        else:
            print(f"\n*--- No Existing subnet 10.99.10.0/24, nothing to deleted")

        # Test by creating a subnet below
        # supernet 10.16.0.0/13,
        # change its properties,
        # then delete the subnet
        print(f"\n--- Search for subnet 10.16.0.0 of type supernet")
        parent_id = my_session.ipsubnet.get_id(Address="10.16.0.0", GroupType=SubnetType.Supernet)
        if parent_id:
            print(f"Parent ID (ID of subnet 10.16.0.0/13) is {parent_id}")

            # Create a new subnet
            uri = my_session.ipsubnet.create("10.99.10.0", 24, parent_id=parent_id, Comments="test")
            print(f"Created a new subnet, subnet uri is {uri}")
            print(f"Subnet: {my_session.ipsubnet.read(uri).get('FriendlyName')}")

            id = my_session.ipsubnet.get_id_from_uri(uri)
            print(f"ID for this subnet is {id}")

            subnet_id = my_session.ipsubnet.get_id(Address="10.99.10.0", CIDR=24)
            if subnet_id:
                print(f"Should be the same: {id} == {subnet_id}: {id==subnet_id}")

                # my_subnet = my_session.ipaddress.get_addresses_in_subnet(id)
                # print(my_subnet)

                # my_uri = my_session.ipaddress.get_uri(IPAddress="10.99.10.250")
                # 403 FORBIDDEN?
                # my_session.ipaddress.delete(my_uri)

                # my_subnet = my_session.ipaddress.get_addresses_in_subnet(id)
                # print(my_subnet)

            # Update subnet
            print(f"Update: VLAN ID of Subnet before update: {my_session.ipsubnet.read(uri).get('VLAN')}")
            r = my_session.ipsubnet.update(uri, VLAN=10)
            print(f"Update: VLAN ID of Subnet after update: {my_session.ipsubnet.read(uri).get('VLAN')}")

            # delete subnet
            r = my_session.ipsubnet.delete(uri)

        # Retrieve address info and return to caller
        uri = my_session.ipaddress.get_uri(IPAddress="10.136.82.2")
        if uri:
            return my_session.ipaddress.read(uri)


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
