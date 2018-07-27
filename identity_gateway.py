import os

import coreapi


class IdentityGatewayActions:
    client = coreapi.Client()
    document = client.get(os.environ.get('APP_IDENTITY_URL') + 'schema/')
    target_url_prefix = os.environ.get('APP_IDENTITY_URL') + 'api/v1/'
    endpoints = list(document.data.keys())

    def list(self, endpoint, params):
        action = [endpoint, 'list']
        return self.client.action(self.document, action, params=params)

    def read(self, endpoint, params):
        action = [endpoint, 'read']
        return self.client.action(self.document, action, params, overrides={'url': self.target_url_prefix + endpoint + '/' + params['email'] + '/'})

    def create(self, endpoint, params):
        action = [endpoint, 'create']
        return self.client.action(self.document, action, params=params)

    def patch(self, endpoint, params):
        action = [endpoint, 'partial_update']
        return self.client.action(self.document, action, params=params, overrides={'url': self.target_url_prefix + endpoint + '/' + params['email'] + '/'})

    def put(self, endpoint, params):
        action = [endpoint, 'update']
        return self.client.action(self.document, action, params=params, overrides={'url': self.target_url_prefix + endpoint + '/' + params['email'] + '/'})

    def delete(self, endpoint, params):
        action = [endpoint, 'delete']
        return self.client.action(self.document, action, params=params, overrides={'url': self.target_url_prefix + endpoint + '/' + params['email'] + '/'})
