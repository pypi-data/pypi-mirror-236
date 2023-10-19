import json

from deepgram_api_client.utils import urljoin, swap_headers


class ResourcePool:
    def __init__(self, endpoint, session):
        self._endpoint = endpoint
        self._session = session

    def get_url(self):
        return self._endpoint

class CreatableResource:
    @swap_headers
    def create_item(self, item, params=None, files=None, custom_headers={}):
        if files:
            res = self._session.post(self._endpoint, data=item, params=params, files=files)
        else:
            res = self._session.post(self._endpoint, data=json.dumps(item), params=params)
        return res

class GettableResource:
    @swap_headers
    def fetch_item(self, code, params=None, custom_headers={}):
        url = urljoin(self._endpoint, code)
        res = self._session.get(url, params=params)
        return res

class ListableResource:
    @swap_headers
    def fetch_list(self, params=None, custom_headers={}):
        res = self._session.get(self._endpoint, params=params)
        return res

class UpdatableResource:
    @swap_headers
    def update_item(self, code, item, params=None, custom_headers={}):
        url = urljoin(self._endpoint, code)
        res = self._session.patch(url, data=json.dumps(item), params=params)
        return res

class DeletableResource:
    def delete_item(self, code, params=None):
        url = urljoin(self._endpoint, code)
        res = self._session.delete(url, params=params)
        return res