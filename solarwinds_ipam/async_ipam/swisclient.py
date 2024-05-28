import httpx

class AsyncSwisClient:
    def __init__(self, *, server='', port=17778, username='', password='', verify=False):
        self.base_url = f"https://{server}:{port}/"
        self.api_path = "SolarWinds/InformationService/v3/Json/"
        self.headers = {'Content-Type': 'application/json'}
        self.auth = (username, password)
        self.verify = verify
        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            auth = self.auth,
            verify=self.verify
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exception):
        await self.session.aclose()
        self.session = None

    # -----------------------------------------------------------------------

    async def _request(self, method, uri, data=None):
        response = await self.session.request(method, self.api_path + uri, json=data)
        response.raise_for_status()
        return response.json()

    async def _query(self, query, **params):
        return await self._request("POST", "Query", {'query': query, 'parameters': params})

    async def _invoke(self, entity, verb, *args):
        return await self._request("POST", f"Invoke/{entity}/{verb}", args)

    async def _create(self, entity, **properties):
        return await self._request("POST", f"Create/{entity}", properties)

    async def _read(self, uri):
        return await self._request("GET", uri)

    async def _update(self, uri, **properties):
        await self._request("POST", uri, properties)

    async def _delete(self, uri):
        await self._request("DELETE", uri)

    async def _bulkupdate(self, uris, **properties):
        await self._request("POST", "BulkUpdate", {'uris': uris, 'properties': properties})

    async def _bulkdelete(self, uris):
        await self._request("POST", "BulkDelete", {'uris': uris})

