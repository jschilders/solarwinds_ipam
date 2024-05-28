from solarwinds_ipam.classes import SubnetType


def _create(): pass
def _read(): pass
def _update(): pass
def _delete(): pass
def _query(): pass

#
# IP Subnet C/R/U/D
# 
def create(subnet_address:str, subnet_cidr:str, parent_id:int=0, **properties:dict)->str:
    properties['Address']   = subnet_address
    properties['CIDR']      = subnet_cidr
    properties['ParentId']  = parent_id
    return _create('IPAM.Subnet', **properties)

def read(uri:str)->dict:
    return _read(uri)

def update(uri:str, **properties:dict)->None:
    return _update(uri, **properties)

def delete(uri:str)->None:
    return _delete(uri)

#
# IP subnet helper methods
#
def get_uri(**kwargs:dict)->str:
    result:dict = query_subnet(**kwargs)
    if result:
        return result.get('Uri')

def get_id(**kwargs:dict)->int:
    result:dict = query_subnet(**kwargs)
    if result:
        return result.get('SubnetID')

def get_uri_and_id(**kwargs:dict)->tuple[str, int]:
    result:dict = query_subnet(**kwargs)
    if result:
        return result.get('Uri'), result.get('SubnetID')

def get_parent(**kwargs:dict)->str:
    result:dict = query_subnet(**kwargs)
    if result:
        return result.get('ParentID')

def query_subnet(subnet_address:str=None, subnet_cidr:int=None, subnet_type:SubnetType=SubnetType.Subnet)->dict:
    query = 'SELECT DISTINCT ParentID, SubnetID, Uri, CIDR  FROM IPAM.Subnet WHERE Address = @subnet_address'
    query_params = { 'subnet_address': subnet_address }
    if subnet_cidr:
        query += ' AND CIDR = @subnet_cidr'
        query_params |= { 'subnet_cidr': subnet_cidr }
    if subnet_type:
        query += ' AND GroupType = @subnet_type'
        query_params |= { 'subnet_type': int(subnet_type) }
    query += ' ORDER BY CIDR DESC'
    result:list = _query(query, **query_params)
    if result:
        return result[0]

def get_id_from_uri(uri:str)->int:
    result:dict = _read(uri)
    if result:
        return result.get('SubnetId')

def get_uri_from_id(subnet_id:int)->str:
    query:str = 'SELECT DISTINCT Uri FROM IPAM.Subnet WHERE SubnetId = @subnet_id'
    query_params:dict = { 'subnet_id': subnet_id }
    result:list = _query(query, **query_params)
    if result:
        return result[0].get('Uri')

#
# Other helpers
#
def get_subnet_address(subnet_id:int=None)->tuple[str, str, int]:
    query:str = 'SELECT DISTINCT Address, AddressMask, CIDR FROM IPAM.Subnet WHERE SubnetId = @subnet_id'
    query_params:dict = { 'subnet_id': subnet_id or getattr('SubnetId', None) }
    result:list = _query(query, **query_params)
    if result:
        return result[0].get('Address'), result[0].get('AddressMask'), result[0].get('CIDR')
