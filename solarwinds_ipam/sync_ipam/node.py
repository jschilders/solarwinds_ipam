from solarwinds_ipam.classes import IpNodeStatus



def _create(): pass
def _read(): pass
def _update(): pass
def _delete(): pass
def _query(): pass

#
# IP Node C/R/U/D 
# 
def create(ip_address:str, subnet_id:str, ordinal:int, status=IpNodeStatus.Reserved, **properties:dict)->str:
    properties['IPAddress'] = ip_address
    properties['SubnetId']  = subnet_id
    properties['IPOrdinal'] = ordinal
    properties['Status']    = int(status)
    return _create('IPAM.IPNode', **properties)

def read(uri:str)->dict:
    return _read(uri)

def update(uri:str, **properties:dict)->None:
    return _update(uri, **properties)

def delete(uri:str)->None:
    return _delete(uri)

#
# IP Node helper methods
#
def get_uri(**kwargs:dict)->str:
    result:dict = query_node(**kwargs)
    if result:
        return result.get('Uri')
     
def get_id(**kwargs:dict)->int:
    result:dict = query_node(**kwargs)
    if result:
        return result.get('IpNodeId')

def get_uri_and_id(**kwargs:dict)->tuple[str, int]:
    result:dict = query_node(**kwargs)
    if result:
        return result.get('Uri'), result.get('IpNodeId')

def get_parent(**kwargs:dict)->str:
    result:dict = query_node(**kwargs)
    if result:
        return result.get('SubnetID')

def query_node(ip_address:str, subnet_id:int=None)->dict:
    query:str = 'SELECT DISTINCT IpNodeId, SubnetID, Uri FROM IPAM.IPNode WHERE IPAddress = @ip_address'
    query_params:dict = { 'ip_address': ip_address }
    if subnet_id:
        query += ' AND SubnetId = @subnet_id'
        query_params |= { 'subnet_id': subnet_id }
    result:list = _query(query, **query_params)
    if result:
        return result[0]

def get_id_from_uri(uri:str)->int:
    result:dict = _read(uri)
    if result:
        return result.get('IpNodeId')

def get_uri_from_id(node_id:int)->str:
    query:str = 'SELECT DISTINCT Uri FROM IPAM.IPNode WHERE IpNodeId = @node_id'
    query_params:dict = { 'node_id': node_id }
    result:list = _query(query, **query_params)
    if result:
        return result[0].get('Uri')

#
# Other helpers
#
def get_nodes_in_subnet(subnet_id:int=None)->list[dict]:
    query:str = 'SELECT DISTINCT IpNodeId, SubnetId, IPAddress, IPMapped, Alias, MAC, DnsBackward, DhcpClientName, Comments, ResponseTime, SkipScan, Status, AllocPolicy, Uri FROM IPAM.IPNode WHERE SubnetId = @subnet_id'
    query_params:dict = { 'subnet_id': subnet_id or getattr('SubnetId', None)}
    result:dict = _query(query, **query_params)
    if result:
        return [ ip_node for ip_node in result ]


