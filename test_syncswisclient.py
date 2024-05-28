from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import IPAM, SubnetType


def main(**connection_parameters) -> None:
    with IPAM(**connection_parameters) as my_session:

        uri = my_session.node.get_uri(ip_address='10.22.10.65')
        if uri:
            # Get the IP address info
            result = my_session.node.read(uri)
            ip_address, alias = result['IPAddress'], result['Alias']
            print(f"Start:    IP Node {ip_address} has alias {result['Alias']!r}")

            # Change alias for node
            my_session.node.update(uri, Alias='Test Alias')

            # Check to see if it is indeed different
            result = my_session.node.read(uri)
            print(f"Updated:  IP Node {ip_address} has alias {result['Alias']!r}")

            # Change alias back to previous
            my_session.node.update(uri, Alias=alias)

            # Check to see if it is indeed back to before
            result = my_session.node.read(uri)
            print(f"Restored: IP Node {ip_address} has alias {result['Alias']!r}")


        id = my_session.node.get_id(ip_address='10.136.82.2')
        if id:
            print(f"Found ID {id} for node 10.136.82.2")    

            uri = my_session.node.get_uri_from_id(id)
            print(f"Uri for this node is {uri}")

            id = my_session.node.get_id_from_uri(uri)
            print(f"And back to ID: {id}")

        parent = my_session.node.get_parent(ip_address='10.136.82.2')
        if parent:
            print(f"Parent subnet for node is {parent}")
            result = my_session.node.get_nodes_in_subnet(parent)
            print(f"Other nodes in this subnet:")
            print(result)
        

        uri, id = my_session.node.get_uri_and_id(ip_address='10.136.82.2')
        if uri and id:
            print(f"URI and ID in a single call: {uri}, {id}")

        # todo: tests for 
        #       node.delete, node.create, 


        print(f"\n--- Find a subnet 10.136.82.64")
        uri = my_session.subnet.get_uri(subnet_address='10.136.82.64')
        if uri:
            print(f"Found. {uri=}")
            subnet = my_session.subnet.read(uri)
            print(subnet)
        else:
            print('Not Found')


        print(f"\n--- Find parent subnet ID of subnet 10.136.82.64")
        id = my_session.subnet.get_parent(subnet_address='10.136.82.64')
        if id:
            print(f"Found. {id=}")
            subnet = my_session.subnet.get_subnet_address(id)
            print(f"Subnet info for ID {id} is {subnet}")
        else:
            print('Not Found')


        print(f"\n--- Find a subnet 10.136.82.0")
        # Note that this will find the SUBnet. 
        # There is also a SUPERnet with the same name.
        uri = my_session.subnet.get_uri(subnet_address='10.136.82.0')
        if uri:
            print(f"Found. {uri=}")
        else:
            print('Not Found')


        print(f"\n--- Find a supernet 10.136.82.0")
        # Note that this will find the SUPERnet. 
        # There is also a SUBnet with the same name.
        uri = my_session.subnet.get_uri(subnet_address='10.136.82.0', subnet_type=SubnetType.Supernet)
        if uri:
            print(f"Found. {uri=}")
        else:
            print('Not Found')

 
        print(f"\n--- Find a subnet 10.16.0.0 with an explicid mask length of /26")
        uri = my_session.subnet.get_uri(subnet_address='10.16.0.0', subnet_cidr=26)
        if uri:
            print(f"Found, {uri=}")
            print(f"Note that you can use read(uri) only on subnets, not on supernets")
            print(my_session.subnet.read(uri))
        else:
            print('Not Found')



        print(f"\n--- Find Uri and ID for subnet 10.136.82.0")
        # Note that this will find the SUBnet. 
        # There is also a SUPERnet with the same name.
        uri, id = my_session.subnet.get_uri_and_id(subnet_address='10.136.82.0')
        if uri and id:
            print(f"Found. {uri=} {id=}")

            print('Uri from ID:', my_session.subnet.get_uri_from_id(id))

            print('ID from Uri:',my_session.subnet.get_id_from_uri(uri))

        else:
            print('Not Found')


        print(f"\n*** Testing C/R/U/D")
        # Delete subnet if it already exists from previous tests
        uri = my_session.subnet.get_uri(subnet_address='10.99.10.0', subnet_cidr=24)
        if uri:
            my_session.subnet.delete(uri)
            print(f"\n*!!! Existing subnet 10.99.10.0/24 deleted")
        else:
            print(f"\n*--- No Existing subnet 10.99.10.0/24, nothing to deleted")


        # Test by creating a subnet below 
        # supernet 10.16.0.0/13, 
        # change its properties, 
        # then delete the subnet
        print(f"\n--- Search for subnet 10.16.0.0 of type supernet")
        parent_id = my_session.subnet.get_id(subnet_address='10.16.0.0', subnet_type=SubnetType.Supernet)
        if parent_id:
            print(f"Parent ID (ID of subnet 10.16.0.0/13) is {parent_id}")

            # Create a new subnet
            uri=my_session.subnet.create('10.99.10.0', 24, parent_id=parent_id, Comments='test')
            print(f"Created a new subnet, subnet uri is {uri}")
            print(f"Subnet: {my_session.subnet.read(uri).get('FriendlyName')}")


            id = my_session.subnet.get_id_from_uri(uri)
            print(f"ID for this subnet is {id}")

            subnet_id = my_session.subnet.get_id(subnet_address='10.99.10.0', subnet_cidr=24)
            if subnet_id:
                print(f"Should be the same: {id} == {subnet_id}: {id==subnet_id}")

                # subnet = my_session.node.get_nodes_in_subnet(id)
                # print(subnet)

                # uri = my_session.node.get_uri(ip_address='10.99.10.250')
                # my_session.node.delete(uri)

                # subnet = my_session.node.get_nodes_in_subnet(id)
                # print(subnet)


            # Update subnet
            print(f"Update: VLAN ID of Subnet before update: {my_session.subnet.read(uri).get('VLAN')}")
            r=my_session.subnet.update(uri, VLAN=10)
            print(f"Update: VLAN ID of Subnet after update: {my_session.subnet.read(uri).get('VLAN')}")


            # delete subnet
            r = my_session.subnet.delete(uri)


        # Retrieve address info and return to caller
        uri = my_session.node.get_uri(ip_address='10.136.82.2')
        if uri:
            return my_session.node.read(uri)


if __name__ == '__main__':
    load_dotenv()
    connection_parameters = {
        'server':   getenv('SERVER') or '',
        'port':     getenv('PORT') or 17778,
        'username': getenv('USERNAME') or '',
        'password': getenv('PASSWORD') or '',
        'verify':   False
    }
    r = main(**connection_parameters)
    print(r)

