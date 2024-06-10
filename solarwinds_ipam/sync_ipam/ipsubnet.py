from solarwinds_ipam.classes import SubnetType


# dummy functions to keed the IDE happy. Will be overridden later
def _create(): pass
def _read(): pass
def _update(): pass
def _delete(): pass
def _query(): pass
def _build_query(): pass

#
# IP Subnet C/R/U/D
# 
def create(Address:str, CIDR:str, ParentId:int=0, **properties:dict)->str:
    properties['Address']   = Address
    properties['CIDR']      = CIDR
    properties['ParentId']  = ParentId
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
    result:list = _build_query('IPAM.Subnet', 'Uri', kwargs )
    if result:
        return result[0].get('Uri')

def get_id(**kwargs:dict)->str:
    result:list = _build_query('IPAM.Subnet', 'SubnetID', kwargs )
    if result:
        return result[0].get('SubnetID')

def get_uri_and_id(**kwargs:dict)->str:
    result:list = _build_query('IPAM.Subnet', ['Uri', 'SubnetID'], kwargs )
    if result:
        return result[0].get('Uri'), result[0].get('SubnetID')

def get_parent(**kwargs:dict)->str:
    result:list = _build_query('IPAM.Subnet', 'ParentID', kwargs )
    if result:
        return result[0].get('ParentID')

def get_uri_from_id(subnet_id:int)->str:
    params = {'SubnetID': subnet_id}
    result:list = _build_query('IPAM.Subnet', 'Uri', params )
    if result:
        return result[0].get('Uri')

def get_id_from_uri(uri:str)->int:
    result:dict = _read(uri)
    if result:
        return result.get('SubnetId')



# def query_subnet(subnet_address:str=None, subnet_cidr:int=None, subnet_type:SubnetType=SubnetType.Subnet)->dict:
#     query = 'SELECT DISTINCT ParentID, SubnetID, Uri, CIDR  FROM IPAM.Subnet WHERE Address = @subnet_address'
#     query_params = { 'subnet_address': subnet_address }
#     if subnet_cidr:
#         query += ' AND CIDR = @subnet_cidr'
#         query_params |= { 'subnet_cidr': subnet_cidr }
#     if subnet_type:
#         query += ' AND GroupType = @subnet_type'
#         query_params |= { 'subnet_type': int(subnet_type) }
#     query += ' ORDER BY CIDR DESC'
#     result:list = _query(query, **query_params)
#     if result:
#         return result[0]


#
# Other helpers
#
# def get_subnet_address(subnet_id:int=None)->tuple[str, str, int]:
#     query:str = ' WHERE SubnetId = @subnet_id'
#     query_params:dict = { 'subnet_id': subnet_id or getattr('SubnetId', None) }
#     result:list = _query(query, **query_params)
#     if result:
#         return result[0].get('Address'), result[0].get('AddressMask'), result[0].get('CIDR')


def get_subnet_address(subnet_id:int)->str:
    fields:list = ['Address', 'AddressMask', 'CIDR']
    params:dict = {'SubnetID': subnet_id}
    result:list = _build_query('IPAM.Subnet', fields, params )
    if result:
        return result[0].get('Address'), result[0].get('AddressMask'), result[0].get('CIDR')
