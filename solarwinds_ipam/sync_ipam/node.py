from solarwinds_ipam.classes import IpNodeStatus


# dummy functions to keed the IDE happy. Will be overridden later
def _create(): pass
def _read(): pass
def _update(): pass
def _delete(): pass
def _query(): pass
def _build_query(): pass

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
    result:list = _build_query('IPAM.IPNode', 'Uri', kwargs )
    if result:
        return result[0].get('Uri')

def get_id(**kwargs:dict)->str:
    result:list = _build_query('IPAM.IPNode', 'IpNodeId', kwargs )
    if result:
        return result[0].get('IpNodeId')

def get_parent(**kwargs:dict)->str:
    result:list = _build_query('IPAM.IPNode', 'SubnetID', kwargs )
    if result:
        return result[0].get('SubnetID')

def get_uri_from_id(node_id:int)->str:
    params = {'IpNodeId': node_id}
    result:list = _build_query('IPAM.IPNode', 'Uri', params )
    if result:
        return result[0].get('Uri')

def get_id_from_uri(uri:str)->int:
    result:dict = _read(uri)
    if result:
        return result.get('IpNodeId')

#
# Other helpers
#
def get_nodes_in_subnet(subnet_id:int=None)->list[dict]:
    fields = [ 
        'IpNodeId', 'SubnetId', 'IPAddress', 'IPMapped', 'Alias', 'MAC', 'DnsBackward', 
        'DhcpClientName', 'Comments', 'ResponseTime', 'SkipScan', 'Status', 'AllocPolicy', 'Uri'
     ]
    params = {'SubnetId': subnet_id}
    result:list = _build_query('IPAM.IPNode', fields, params )
    if result:
        return [ ip_node for ip_node in result ]
