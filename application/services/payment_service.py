"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- payment_service.py --

@author: Informed Solutions
"""

import json
import logging
import time
from urllib.parse import quote

from ..presentation.utilities import get_confirmation_status, get_confirmation_email_template
from .notify import send_email

import requests

from django.conf import settings

from ..services.db_gateways import NannyGatewayActions


logger = logging.getLogger()


def make_payment(amount, name, number, cvc, expiry_m, expiry_y, currency, customer_order_code, desc):
    """
    Function used to send a WorldPay card payment request to the payment gateway, all validation is done by the gateway,
    appropriate error response will be sent in JSON
    :param amount: amount of money to be charged, send as an integer. Done in pence, so £35 would be 3500
    :param name: name of the card holder, send as a string. This should be what is written on the card
    :param number: card number, sent as an integer. This should be what is written on the card
    :param cvc: cvc number on back of card. This should be sent as an integer
    :param expiry_m: expiry month on the card, sent as an integer. This should be what is written on the card
    :param expiry_y: expiry year on the card, sent as an integer. This should be what is written on the card
    :param currency: Currency code that should be charged, sent as a string, see below for full list:
    https://developer.worldpay.com/jsonapi/faq/articles/what-currencies-can-i-accept-payments-in
    :param customer_order_code: This is the order code the customer will be provided with on the confirmation page
    :param desc: This is the order description the user will see attached to their payment when on PayPal, this should
    be a string
    :return: returns a full http response object containing either order details on success or an error message on
    failure
    """
    base_url = settings.PAYMENT_URL
    header = {'content-type': 'application/json'}
    payload = {
        "amount": amount,
        "cardHolderName": name,
        "cardNumber": number,
        "cvc": cvc,
        "expiryMonth": expiry_m,
        "expiryYear": expiry_y,
        "currencyCode": currency,
        "customerOrderCode": customer_order_code,
        "orderDescription": desc
    }

    logger.debug('Issuing call to payment gateway for payment reference: ' + customer_order_code)

    response = requests.post(base_url + "/api/v1/payments/card/", json.dumps(payload),
                             headers=header, timeout=int(settings.PAYMENT_HTTP_REQUEST_TIMEOUT))
    return response


def check_payment(payment_reference):
    """
    A function to confirm a worldpay order code exists in Worldpay's records
    :param payment_reference: the order code of the payment that needs to be checked
    :return: a status code to confirm whether this payment exists or not, these responses are defined in swagger
    """
    base_url = settings.PAYMENT_URL
    header = {'content-type': 'application/json'}
    query_path = base_url + "/api/v1/payments/" + quote(payment_reference)
    response = requests.get(query_path, headers=header, timeout=int(settings.PAYMENT_HTTP_REQUEST_TIMEOUT))
    return response


def payment_email(email, name, application_reference, application_id):
    """
    A function to send an email through the notify gateway with a payment template, currently used to confirm a Worldpay
    card order has been successful
    :param email: The address to send the email to, sent as a string
    :param name: The name to be placed on the email template to be sent to the user
    :param application_reference
    :param application_id
    :return: Returns the response object obtained from the PayPal gateway method, as defined in swagger
    """
    logger.debug('Dispatching payment confirmation email for application with identifier: ' + application_id)

    # Check for cautions and convictions, and whether the applicant has lived abroad

    dbs_record = NannyGatewayActions().read('dbs-check', params={'application_id': application_id}).record

    capita = dbs_record['is_ofsted_dbs']
    certificate_information = dbs_record['certificate_information']
    lived_abroad = dbs_record['lived_abroad']

    # Get the email template_id to send
    confirmation_status = get_confirmation_status(capita, certificate_information, lived_abroad)
    confirmation_email_template_id = get_confirmation_email_template(confirmation_status)
    logger.debug('Attempting send of email with template_id: {0}'.format(confirmation_email_template_id))

    response = send_email(email, {"firstName": name, "ref": application_reference}, confirmation_email_template_id)
    return response


def create_formatted_payment_reference(application_reference):
    """
    Function for formatting a payment reference to be issued to the payment provider
    :param application_reference: a unique application reference
    :return: a formatted payment reference
    """
    prefix = settings.PAYMENT_REFERENCE_PREFIX
    payment_urn_prefix = settings.PAYMENT_URN_PREFIX
    timestamp = time.strftime("%Y%m%d%H%M%S")
    formatted_payment_reference = str(prefix + ':' + payment_urn_prefix + application_reference + ':' + timestamp)
    return formatted_payment_reference


def payment_record_exists(application_id):
    """
    Service layer implementation for testing whether a payment record has previously been lodged
    :param application_id: the UUID of the application
    :return: a boolean indicator detailing whether a payment record exists or not
    """
    logger.debug('Testing for presence of payment record for application with identifier: ' + application_id)
    payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id})
    return payment_record.status_code == 200


def get_payment_record(application_id):
    """
    Service layer implementation for attempting to fetch a payment record from the Nanny Gateway API
    :param application_id: the UUID of the application
    :return: a payment record instance or a 404 status code if not found
    """
    logger.debug('Fetching payment record for application with identifier: ' + application_id)
    return NannyGatewayActions().read('payment', params={'application_id': application_id}).record
