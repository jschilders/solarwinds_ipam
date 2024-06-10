import httpx


class SwisApi:

    def __init__(self, *, server='', port=17778, username='', password='', verify=False):
      
        self.base_url = f"https://{server}:{port}/"
        self.api_path = "SolarWinds/InformationService/v3/Json/"
        self.headers = {'Content-Type': 'application/json'}
        self.auth = (username, password)
        self.verify = verify
        
        self.session = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            auth = self.auth,
            verify=self.verify
        )

    def __enter__(self):
        return self

    def __exit__(self, *exception):
        self.session.close()
        self.session = None

    # -----------------------------------------------------------------------

    def _request(self, method, uri, data=None):
        #print(self.base_url + self.api_path + uri)
        response = self.session.request(method, self.api_path + uri, json=data)
        response.raise_for_status()
        return response.json()
 
    def _create(self, entity, **properties):
        return self._request("POST", f"Create/{entity}", properties)
    
    def _read(self, uri):
        return self._request("GET", uri)

    def _update(self, uri, **properties):
        self._request("POST", uri, properties)

    def _delete(self, uri):
        self._request("DELETE", uri)

    def _bulkupdate(self, uris, **properties):
        self._request("POST", "BulkUpdate", {'uris': uris, 'properties': properties})

    def _bulkdelete(self, uris):
        self._request("POST", "BulkDelete", {'uris': uris})

    def _invoke(self, entity, verb, *args):
        return self._request("POST", f"Invoke/{entity}/{verb}", args).get('results')

    def _query(self, query, **params):
        return self._request("POST", "Query", {'query': query, 'parameters': params}).get('results')

    def _build_query(self, table_name:str, fields_to_return:list|str, query_parameters:dict=None, order_by:dict=None):
        fields = ', '.join(fields_to_return) if isinstance(fields_to_return, list) else fields_to_return
        select = ' WHERE ' + ' AND '.join(f'{param} = @{param}' for param  in query_parameters) if query_parameters else ''
        order =  ' ORDER BY ' + ', '.join(f'{fieldname} {direction}' for fieldname, direction in order_by.items()) if order_by else ''
        query = f"SELECT DISTINCT {fields} FROM {table_name}{select}{order};"
        return self._query(query, **query_parameters)
