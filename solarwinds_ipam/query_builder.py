from dotenv import load_dotenv
from os import getenv
from rich import print
from solarwinds_ipam import IPAM, SubnetType

#
# This is only for testing an idea at the moment
#

def query_builder(table, fields_to_return=None, query_parameters=None, order_by=None):

    if fields_to_return:
        fields = ', '.join(fields_to_return)
    else:
        fields = '*'
        # Will not work with swql

    if query_parameters:
        select = ' WHERE ' + ' AND '.join(f'{param} = @{param}' for param  in query_parameters)
    else:
        select = ''

    if order_by:
        order = ' ORDER BY ' + ', '.join(f'{fieldname} {direction}' for fieldname, direction in order_by.items())
    else:
        order = ''

    query = f"SELECT DISTINCT {fields} FROM {table}{select}{order};"
    if select:
        params = { parameter: value for parameter, value in query_parameters.items() }
    else:
        params = {}

    return query, params



def main(**connection_parameters) -> None:
    with IPAM(**connection_parameters) as my_session:

        table = 'IPAM.Subnet'
        fields_to_return = [ 
            'ParentID', 
            'SubnetID', 
        #    'Uri', 
            'CIDR',
            'GroupType'
        ]
        query_parameters = {
            'Address':   '10.136.82.0',
            #'CIDR':      '24',
            #'GroupType': 4
            
        }
        order_by = {
            'CIDR': 'DESC',
#            'Address': 'ASC'
        }
        query, params = query_builder(table, fields_to_return, query_parameters, order_by)

        print()
        print(query)
        print(params)
        print()

        return my_session._query(query, **params)






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

