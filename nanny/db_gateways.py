import logging
import os
import json

import requests


logger = logging.getLogger()


class DBGatewayActions:
    """
    Base class for handling all requests to Database gateway services at specified target_url_prefix.
    """
    target_url_prefix = None
    event_list = None

    def __init__(self):
        self.event_list = [getattr(self, func) for func in dir(self) if callable(getattr(self, func)) and func[0] != '_']
        self._register_events()

    def _register_events(self):
        for event in self.event_list:
            setattr(self, event.__name__, self._dispatch(event))

    def _dispatch(self, func):

        def log_wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            if response.status_code not in (200, 201, 404):

                verb_name = func.__name__

                if verb_name == 'list':
                    logger.error(
                        '!GATEWAY ERROR! "{}" request to API endpoint "{}" with {}: {} returned {} status code - see the Gateway logs for traceback'.format(
                            verb_name, args[0], list(kwargs['params'].keys()), list(kwargs['params'].values()),
                            response.status_code))
                    logger.info('!GATEWAY ERROR! Targeted url: {}'.format(response.url))

                elif verb_name == 'childcare_address':
                    logger.error(
                        '!GATEWAY ERROR! "{}" request to API endpoint "{}" with {}: {} returned {} status code - see the Gateway logs for traceback'.format(
                            verb_name, args[0], 'childcare_address_id', kwargs['params']['childcare_address_id'],
                            response.status_code))
                    logger.info('!GATEWAY ERROR! Targeted url: {}'.format(response.url))

                elif verb_name == 'arc-comments':
                    logger.error(
                        '!GATEWAY ERROR! "{}" request to API endpoint "{}" with {}: {} returned {} status code - see the Gateway logs for traceback'.format(
                            verb_name, args[0], 'review_id', kwargs['params']['review_id'],
                            response.status_code))
                    logger.info('!GATEWAY ERROR! Targeted url: {}'.format(response.url))

                else:
                    logger.error(
                        '!GATEWAY ERROR! "{}" request to API endpoint "{}" with {}: {} returned {} status code - see the Gateway logs for traceback'.format(
                            verb_name, args[0], 'application_id', kwargs['params']['application_id'],
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
        if endpoint == 'childcare-address':
            response = requests.get(self.target_url_prefix + endpoint + '/' + params['childcare_address_id'] + '/', data=params)
        elif endpoint == 'arc-comments':
            response = requests.get(self.target_url_prefix + endpoint + '/' + params['review_id'] + '/', data=params)
        else:
            response = requests.get(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params)

        if response.status_code == 200:
            response.record = json.loads(response.text)

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
        if endpoint == 'childcare-address':
            response = requests.put(self.target_url_prefix + endpoint + '/' + params['childcare_address_id'] + '/', data=params)
        elif endpoint == 'arc-comments':
            response = requests.put(self.target_url_prefix + endpoint + '/' + params['review_id'] + '/', data=params)
        else:
            response = requests.put(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params)

        if response.status_code == 200:
            response.record = json.loads(response.text)

        return response

    def delete(self, endpoint, params):
        if endpoint == 'arc-comments':
            return requests.delete(self.target_url_prefix + endpoint + '/' + params['review_id'] + '/', data=params)
        else:
            return requests.delete(self.target_url_prefix + endpoint + '/' + params['application_id'] + '/', data=params)


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
