import logging
import os
import json
from unittest.mock import MagicMock

import requests


logger = logging.getLogger()


class DBGatewayActions:
    """
    Base class for handling all requests to Database gateway services at specified target_url_prefix.
    """
    target_url_prefix = None
    event_list = None

    endpoint_pk_dict = {
        'childcare-address': 'childcare_address_id',
        'arc-comments': 'review_id',
        'applicant-home-address': 'application_id',
        'applicant-personal-details': 'application_id',
        'application': 'application_id',
        'childcare-training': 'application_id',
        'dbs-check': 'application_id',
        'declaration': 'application_id',
        'first-aid': 'application_id',
        'insurance-cover': 'application_id',
        'payment': 'application_id',
        'summary': 'application_id'
    }

    def __init__(self):
        self.event_list = [getattr(self, func) for func in dir(self) if callable(getattr(self, func)) and func[0] != '_']
        self.__register_events()

    def __register_events(self):
        if any([isinstance(event, MagicMock) for event in self.event_list]):
            return None

        for event in self.event_list:
            setattr(self, event.__name__, self.__dispatch(event))

    def __dispatch(self, func):
        def log_wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            if response.status_code not in (200, 201, 404):

                verb_name = func.__name__
                endpoint_name = args[0]
                endpoint_lookup_field = self.endpoint_pk_dict[endpoint_name]

                if func.__name__ == 'list':
                    logger.error(
                        '!GATEWAY ERROR! "{}" request to API endpoint "{}" with {}: {} returned {} status code - see the Gateway logs for traceback'.format(
                            verb_name, endpoint_name, list(kwargs['params'].keys()), list(kwargs['params'].values()),
                            response.status_code))
                    logger.info('!GATEWAY ERROR! Targeted url: {}'.format(response.url))

                else:
                    logger.error(
                        '!GATEWAY ERROR! "{}" request to API endpoint "{}" with {}: {} returned {} status code - see the Gateway logs for traceback'.format(
                            verb_name, args[0], endpoint_lookup_field, kwargs['params'][endpoint_lookup_field],
                            response.status_code))
                    logger.info('!GATEWAY ERROR! Targeted url: {}'.format(response.url))

            return response

        return log_wrapper

    def list(self, endpoint, params):
        query_params = ''.join(['&' + key + '=' + value for key, value in params.items()])

        response = requests.get(self.target_url_prefix + endpoint + '/?' + query_params)

        if response.status_code == 200:
            response.record = json.loads(response.text)

        return response

    def read(self, endpoint, params):
        endpoint_lookup_field = self.endpoint_pk_dict[endpoint]
        response = requests.get(self.target_url_prefix + endpoint + '/' + params[endpoint_lookup_field] + '/', data=params)

        if response.status_code == 200:
            response.record = json.loads(response.text)

        response.status_code = 500

        return response

    def create(self, endpoint, params):
        response = requests.post(self.target_url_prefix + endpoint + '/', data=params)

        if response.status_code == 201:
            response.record = json.loads(response.text)

        return response

    def patch(self, endpoint, params):
        response = requests.patch(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params)

        if response.status_code == 200:
            response.record = json.loads(response.text)

        return response

    def put(self, endpoint, params):
        endpoint_lookup_field = self.endpoint_pk_dict[endpoint]
        response = requests.put(self.target_url_prefix + endpoint + '/' + params[endpoint_lookup_field] + '/', data=params)

        if response.status_code == 200:
            response.record = json.loads(response.text)

        return response

    def delete(self, endpoint, params):
        endpoint_lookup_field = self.endpoint_pk_dict[endpoint]
        return requests.delete(self.target_url_prefix + endpoint + '/' + params[endpoint_lookup_field] + '/', data=params)


class IdentityGatewayActions(DBGatewayActions):
    """
    Class for handling all requests to the Identity Gateway service.
    """
    target_url_prefix = os.environ.get('APP_IDENTITY_URL') + 'api/v1/'


class NannyGatewayActions(DBGatewayActions):
    """
    Class for handling all requests to the Nanny Gateway service.
    """
    target_url_prefix = os.environ.get('APP_NANNY_GATEWAY_URL') + '/api/v1/'
