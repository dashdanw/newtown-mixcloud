import os
import requests
import settings

from urllib import parse

from requests_toolbelt.multipart.encoder import MultipartEncoder


class MixcloudAPI():
    BASE_URL = 'https://www.mixcloud.com/'

    AUTHORIZE_PATH = 'oauth/authorize'
    ACCESS_TOKEN_PATH = 'oauth/access_token'

    API_URL = 'https://api.mixcloud.com/'
    UPLOAD_PATH = 'upload/'

    def __init__(self, client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET):
        self.client_id = client_id
        self.client_secret = client_secret

    def authorize(self, redirect_uri=settings.REDIRECT_URI):
        auth_url = f'{self.BASE_URL}/{self.AUTHORIZE_PATH}?client_id={parse.quote(self.client_id)}&redirect_uri={parse.quote(redirect_uri)}'
        code = input(f'Follow {auth_url} and paste the returned code in query params here:')

        token_url = f'{self.BASE_URL}/{self.ACCESS_TOKEN_PATH}'
        token_params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': settings.REDIRECT_URI
        }

        response = requests.get(url=token_url, params=token_params)

        self.access_token = response.json()['access_token']

        return response

    def upload(self, filename, name, tags):
        tags = { f'tags-{i}-tag': tag for i, tag in enumerate(tags) }
        mp_encoder = MultipartEncoder(
            fields={
                'name': name,
                # plain file object, no filename or mime type produces a
                # Content-Disposition header with just the part name
                'mp3': (os.path.basename(filename), open(filename, 'rb'), 'audio/mp3'),
                **tags,
            }
        )
        response = requests.post(
            f'{self.API_URL}/{self.UPLOAD_PATH}?access_token={self.access_token}',
            data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
            # The MultipartEncoder provides the content-type header with the boundary:
            headers={'Content-Type': mp_encoder.content_type}
        )
        return response
