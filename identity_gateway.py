import os
import json

import requests


class IdentityGatewayActions:
    target_url_prefix = os.environ.get('APP_IDENTITY_URL') + 'api/v1/'

    def list(self, endpoint, params):
        response = requests.get(self.target_url_prefix + endpoint + '/', data=params)

        if response.status_code == 200:
            response.record = json.loads(requests.get(self.target_url_prefix + endpoint + '/', data=params).text)

        return response

    def read(self, endpoint, params):
        return json.loads(requests.get(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params).text)

    def create(self, endpoint, params):
        return json.loads(requests.get(self.target_url_prefix + endpoint + '/', data=params).text)

    def patch(self, endpoint, params):
        return json.loads(requests.get(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params).text)

    def put(self, endpoint, params):
        return json.loads(requests.get(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params).text)

    def delete(self, endpoint, params):
        return json.loads(requests.get(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params).text)
