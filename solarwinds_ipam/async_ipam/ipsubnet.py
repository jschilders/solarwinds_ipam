from solarwinds_ipam.classes import SubnetType

#
# IP Subnet C/R/U/D
# 
async def create(connection, subnet_address, subnet_cidr, parent_id=0, **properties):
    properties['Address']   = subnet_address
    properties['CIDR']      = subnet_cidr
    properties['ParentId']  = parent_id
    result = await connection._create('IPAM.Subnet', **properties)
    return result

async def read(connection, uri):
    result = await connection._read(uri)
    #return IpSubnet(**result)
    return result

async def update(connection, uri, **properties):
    result = await connection._update(uri, **properties)
    return result

async def delete(connection, uri):
    result = await connection._delete(uri)
    return result

#
# IP subnet helper methods
#
async def get_uri(connection, **kwargs):
    result = await query_subnet(connection, **kwargs)
    return result['Uri']

async def get_id(connection, **kwargs):
    result = await query_subnet(connection, **kwargs)
    return result['SubnetID']

async def get_uri_and_id(connection, **kwargs):
    result = await query_subnet(connection, **kwargs)
    return result['Uri'], result['SubnetID']

async def get_parent(connection, **kwargs):
    result = await query_subnet(connection, **kwargs)
    return result['ParentID']

async def query_subnet(connection, subnet_address:str=None, subnet_cidr:int=None, subnet_type:SubnetType=SubnetType.Subnet):
    query = 'SELECT DISTINCT ParentID, SubnetID, Uri, CIDR  FROM IPAM.Subnet WHERE Address = @subnet_address'
    query_params = { 'subnet_address': subnet_address }
    if subnet_cidr:
        query += ' AND CIDR = @subnet_cidr'
        query_params |= { 'subnet_cidr': subnet_cidr }
    if subnet_type:
        query += ' AND GroupType = @subnet_type'
        query_params |= { 'subnet_type': int(subnet_type) }
    query += ' ORDER BY CIDR DESC'
    result = await connection._query(query, **query_params)
    return result['results'][0]

async def get_id_from_uri(connection, uri):
    subnet_id = await connection.read(uri)['SubnetId']
    return subnet_id

async def get_uri_from_id(connection, subnet_id):
    query = 'SELECT DISTINCT Uri FROM IPAM.Subnet WHERE SubnetId = @subnet_id'
    query_params = { 'subnet_id': subnet_id }
    result = await connection.query(query, **query_params)
    return result['result'][0]['Uri']



async def get_subnet_address(connection, subnet_id=None):
    query = 'SELECT DISTINCT Address, AddressMask, CIDR FROM IPAM.Subnet WHERE SubnetId = @subnet_id'
    query_params = { 'subnet_id': subnet_id or getattr(connection, 'SubnetId', None) }
    result = await connection._query(query, **query_params)
    return result['result'][0]['Address'],result[0]['AddressMask'],result[0]['CIDR']
