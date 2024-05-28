import httpx


class SwisClient:

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
        response = self.session.request(method, self.api_path + uri, json=data)
        response.raise_for_status()
        return response.json()

    def _query(self, query, **params):
        return self._request("POST", "Query", {'query': query, 'parameters': params}).get('results')

    def _invoke(self, entity, verb, *args):
        return self._request("POST", f"Invoke/{entity}/{verb}", args).get('results')

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
