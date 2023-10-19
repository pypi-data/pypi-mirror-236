import requests as rq

from deepgram_api_client import utils, resources


class Client:
    BASE_URL = 'https://api.deepgram.com'

    def __init__(self, token, version='v1'):
        
        self._session = rq.Session()
        self._session.headers = {
            'Authorization': f'Token {token}',
        }

        self._base_url = utils.urljoin(
            self.BASE_URL, version
        )

        self._resources = {
            'listen': resources.ListenPool(
                utils.urljoin(self._base_url, 'listen'), self._session
            )
        }

    @property
    def resources(self):
        return self._resources
    
    @property
    def listen(self):
        return self._resources['listen']
