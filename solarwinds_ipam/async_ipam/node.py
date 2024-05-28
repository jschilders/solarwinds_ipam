from solarwinds_ipam.classes import IpNodeStatus

#
# IP Node C/R/U/D 
# 
async def create(connection, ip_address, subnet_id, ordinal, status=IpNodeStatus.Reserved, **properties):
    properties['IPAddress'] = ip_address
    properties['SubnetId']  = subnet_id
    properties['IPOrdinal'] = ordinal
    properties['Status']    = int(status)
    return await connection._create('IPAM.IPNode', **properties)

async def read(connection, uri):
    result = await connection._read(uri)
    return result

async def update(connection, uri, **properties):
    result = await connection._update(uri, **properties)
    return result

async def delete(connection, uri):
    result = await connection._delete(uri)
    return result

#
# IP Node helper methods
#
async def get_uri(connection, **kwargs):
    result = await connection.query_node(**kwargs)
    return result.get('Uri')
    
async def get_id(connection, **kwargs):
    result = await connection.query_node(**kwargs)
    return result.get('IpNodeId')

async def get_uri_and_id(connection, **kwargs):
    result = await query_node(connection, **kwargs)
    return result['Uri'], result['IpNodeId']

async def get_parent(connection, **kwargs):
    result = await query_node(connection, **kwargs)
    return result['SubnetID']

async def query_node(connection, ip_address, subnet_id=None):
    query = 'SELECT DISTINCT IpNodeId, SubnetID, Uri FROM IPAM.IPNode WHERE IPAddress = @ip_address'
    query_params = { 'ip_address': ip_address }
    if subnet_id:
        query += ' AND SubnetId = @subnet_id'
        query_params |= { 'subnet_id': subnet_id }
    result = await connection._query(query, **query_params)
    return result['results'][0]

#
#
#
async def get_id_from_uri(connection, uri):
    node_id = await connection._read(uri)['IpNodeId']
    return node_id

async def get_uri_from_id(connection, subnet_id):
    query = 'SELECT DISTINCT Uri FROM IPAM.Subnet WHERE SubnetId = @subnet_id'
    query_params = { 'subnet_id': subnet_id }
    result = await connection._query(query, **query_params)
    return result['result'][0]['Uri']

#
#
#
async def get_nodes_in_subnet(connection, subnet_id=None):
    query = 'SELECT DISTINCT IpNodeId, SubnetId, IPAddress, IPMapped, Alias, MAC, DnsBackward, DhcpClientName, Comments, ResponseTime, SkipScan, Status, AllocPolicy, Uri FROM IPAM.IPNode WHERE SubnetId = @subnet_id'
    query_params = { 'subnet_id': subnet_id or getattr(connection, 'SubnetId', None)}
    result = await connection._query(query, **query_params)
    return [ ip_node for ip_node in result ]
    #return [ IpNode(**ip_node) for ip_node in result ]
