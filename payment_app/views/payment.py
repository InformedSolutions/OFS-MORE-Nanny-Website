import datetime
import logging
import os
import re
import requests
import time

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache

from nanny.db_gateways import NannyGatewayActions, IdentityGatewayActions

from ..services import payment_service
from ..forms.payment import PaymentDetailsForm
from ..messaging.sqs_handler import SQSHandler

logger = logging.getLogger()
sqs_handler = SQSHandler(settings.PAYMENT_QUEUE_NAME)

@never_cache
def card_payment_details(request):
    """
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Card payment details template
    """
    if request.method == 'GET':
        return card_payment_get_handler(request)

    if request.method == 'POST':
        return card_payment_post_handler(request)


def card_payment_get_handler(request):
    """
    GET handler for card payment details page
    :param request: inbound HTTP request
    :return: A page for capturing card payment details
    """
    application_id = request.GET["id"]
    application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
    paid = application_record['application_reference']

    # Call out to payment service API
    prior_payment_record_exists = payment_service.payment_record_exists(application_id)

    if not prior_payment_record_exists:
        form = PaymentDetailsForm()
        variables = {
            'form': form,
            'application_id': application_id
        }

        return render(request, 'payment-details.html', variables)

    # If a previous attempt has been made, fetch payment record
    payment_record = payment_service.get_payment_record(application_id)

    # If payment has been fully authorised show fee paid page
    if payment_record['payment_authorised']:
        variables = {
            'application_id': application_id,
            'order_code': paid
        }
        return render(request, 'paid.html', variables)

    # If none of the above have resulted in a yield, show payment page
    form = PaymentDetailsForm()
    variables = {
        'form': form,
        'application_id': application_id
    }

    return render(request, 'payment-details.html', variables)


def card_payment_post_handler(request):
    """
    Handler for managing card payment POST requests
    :param request: inbound HTTP POST request
    :return: confirmation of payment or error page based on payment processing outcome
    """
    application_id = request.POST["id"]
    form = PaymentDetailsForm(request.POST)

    # If form is erroneous due to an invalid form, simply return form to user as an early return
    if not form.is_valid():
        variables = {
            'form': form,
            'application_id': application_id
        }
        return render(request, 'payment-details.html', variables)

    application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record

    application_reference = __assign_application_reference(application_record)

    # Boolean flag for managing logic gates
    prior_payment_record_exists = payment_service.payment_record_exists(application_id)

    payment_reference = __create_payment_record(application_record, application_reference)

    payment_record = payment_service.get_payment_record(application_id)

    payment_record_submitted = payment_record['payment_submitted']

    # If no prior payment record exists, request to capture the payment
    if not prior_payment_record_exists \
            or (prior_payment_record_exists
                and not payment_record_submitted):

        # Attempt to lodge payment by pulling form POST details
        card_number = re.sub('[ -]+', '', request.POST["card_number"])
        cardholders_name = request.POST["cardholders_name"]
        card_security_code = str(request.POST["card_security_code"])
        expiry_month = request.POST["expiry_date_0"]
        expiry_year = '20' + request.POST["expiry_date_1"]

        # Invoke Payment Gateway API
        create_payment_response = payment_service.make_payment(10300, cardholders_name, card_number, card_security_code,
                                                               expiry_month, expiry_year, 'GBP', payment_reference,
                                                               'Ofsted Fees')

        if create_payment_response.status_code == 201:

            # Mark payment submission flag to show an initial request has been lodged
            # if response status indicates success
            __mark_payment_record_as_submitted(application_id)

            # Parse JSON response
            parsed_payment_response = create_payment_response.json()

            if parsed_payment_response.get('lastEvent') == "AUTHORISED":
                # If payment response is immediately authorised, yield success page
                return __handle_authorised_payment(application_id)

            if parsed_payment_response.get('lastEvent') == "REFUSED":
                # If payment has been marked as a REFUSED by Worldpay then payment has
                # been attempted but was not successful in which case a new order should be attempted.
                __rollback_payment_submission_status(application_id)
                return __yield_general_processing_error_to_user(request, form, application_id)

            if parsed_payment_response.get('lastEvent') == "ERROR":
                return __yield_general_processing_error_to_user(request, form, application_id)

        else:
            # If non-201 return status, this indicates a Payment gateway or Worldpay failure
            return __yield_general_processing_error_to_user(request, form, application_id)

    # If above logic gates have not been triggered, this indicates a form re-submission whilst processing
    # was taking place
    return resubmission_handler(request, payment_reference, form, application_id)


def resubmission_handler(request, payment_reference, form, application):
    """
    Handling logic for managing page re-submissions to avoid duplicate payments being created
    :param request: Inbound HTTP post request
    :param payment_reference: the payment reference number allocated to an application payment attempt
    :param form: the Django form for the card details page
    :param application: the user's childminder application
    :return: HTTP response redirect based on payment status check outcome
    """

    # All logic below acts as a handler for page re-submissions
    time.sleep(int(settings.PAYMENT_STATUS_QUERY_INTERVAL_IN_SECONDS))

    # Check at this point whether Worldpay has marked the payment as authorised
    payment_status_response_raw = payment_service.check_payment(payment_reference)

    # If no record of the payment could be found, yield error
    if payment_status_response_raw.status_code == 404:
        return __yield_general_processing_error_to_user(request, form, application.application_id)

    # Deserialize Payment Gateway API response
    parsed_payment_response = payment_status_response_raw.json()

    if parsed_payment_response.get('lastEvent') == "AUTHORISED":
        # If payment has been marked as a AUTHORISED by Worldpay then payment has been captured
        # meaning user can be safely progressed to confirmation page
        return __handle_authorised_payment(application)
    if parsed_payment_response.get('lastEvent') == "REFUSED":
        # If payment has been marked as a REFUSED by Worldpay then payment has
        # been attempted but was not successful in which case a new order should be attempted.
        __rollback_payment_submission_status(application)
        return __yield_general_processing_error_to_user(request, form, application.application_id)
    if parsed_payment_response.get('lastEvent') == "ERROR":
        return __yield_general_processing_error_to_user(request, form, application.application_id)
    else:
        if 'processing_attempts' in request.META:
            processing_attempts = int(request.META.get('processing_attempts'))

            # If 3 attempts to process the payment have already been made without success
            # yield error to user
            if processing_attempts >= settings.PAYMENT_PROCESSING_ATTEMPTS:
                form.add_error(None, 'There has been a problem when trying to process your payment. '
                                     'Please contact Ofsted for assistance.', )
                form.error_summary_template_name = 'error-summary.html'

                variables = {
                    'form': form,
                    'application_id': application.application_id,
                }

                return HttpResponseRedirect(
                    reverse('Payment-Details-View') + '?id=' + application.application_id, variables)

            # Otherwise increment processing attempt count
            request.META['processing_attempts'] = processing_attempts + 1
        else:
            request.META['processing_attempts'] = 1

        # Retry processing of payment
        return resubmission_handler(request, payment_reference, form, application)


def __assign_application_reference(application):
    """
    Private helper function for calling out to the nanny gateway method for assigning an application reference
    :param application: the application for which a reference is to be assigned
    :returns application reference number
    """
    # Call out to Nanny Gateway method
    application_id = application['application_id']

    get_request_endpoint = os.environ.get('APP_NANNY_GATEWAY_URL') \
                           + '/api/v1/application/application_reference/' + application_id

    response = requests.get(get_request_endpoint)

    logger.debug('Received application reference number: ' + str(response.content) + ' from gateway API')

    if response.status_code == 200:
        response_body = response.json()
        return response_body['reference']
    else:
        # Raise up exception to caller if could not allocate reference
        raise Exception


def __create_payment_record(application, application_reference):
    """
    Private helper function for creating a payment record in the event one does not previously exist.
    If a previous record is already present, a payment reference is returned
    :param application: the application for which a new payment record is to be created
    :param application_reference: the reference number assigned to an application
    :return: a payment reference number for an application (either new or)
    """
    application_id = application['application_id']
    prior_payment_record_exists = payment_service.payment_record_exists(application_id)

    # Lodge payment record if does not currently exist
    if not prior_payment_record_exists:
        logger.info('Creating new payment record '
                    'for application with id: ' + application_id)

        # Create formatted payment reference for finance reconciliation purposes
        payment_reference = payment_service.create_formatted_payment_reference(application_reference)

        logger.info('Updating payment record with generated reference '
                    'for application with id: ' + application_id)

        NannyGatewayActions().create(
            'payment',
            params={
                'application_id': application_id,
                'payment_reference': payment_reference,
            }
        )
        return payment_reference

    else:
        logger.info('Fetching existing payment record '
                    'for application with id: ' + application_id)
        payment_record = payment_service.get_payment_record(application_id)
        return payment_record['payment_reference']


def __handle_authorised_payment(application_id):
    """
    Private helper function for managing a rejected payment
    :param application: application associated with the payment attempting to be made
    :return: redirect to payment confirmation page
    """

    # Update payment record to finalise approval of payment
    __mark_payment_record_as_authorised(application_id)

    # Transition application to submitted
    logger.info('Assigning SUBMITTED state for application with id: ' + str(application_id))

    application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
    application_record['date_submitted'] = datetime.datetime.today()
    application_record = NannyGatewayActions().put('application', params=application_record).record

    # Dispatch payment confirmation email to user
    __send_payment_confirmation_email(application_record)

    # Send ad-hoc payment to NOO
    app_cost_float = float(settings.APP_COST/100)
    msg_body = __build_message_body(application_record, format(app_cost_float, '.4f'))
    sqs_handler.send_message(msg_body)

    application_reference = application_record['application_reference']

    return __redirect_to_payment_confirmation(application_reference, application_id)


def __send_payment_confirmation_email(application_record):
    """
    Private helper for issuing a payment confirmation email to a user
    :param application_id: the unique identifier of the application
    """
    application_id = application_record['application_id']
    user_details = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
    applicant_details = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id}).record

    payment_service.payment_email(user_details['email'],
                                  applicant_details['first_name'],
                                  application_record['application_reference'],
                                  application_record['application_id'])


def __mark_payment_record_as_submitted(application_id):
    """
    Private helper function for marking a payment as submitted to Worldpay
    :param application_id: the unique identifier of the application for which a payment record is to be marked as submitted
    """
    logger.info('Marking payment as SUBMITTED for application with id: ' + str(application_id))
    payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id}).record
    payment_record['payment_submitted'] = True
    NannyGatewayActions().put('payment', params=payment_record)


def __mark_payment_record_as_authorised(application_id):
    """
    Private helper function for marking a payment as processed by Worldpay
    :param application_id: the unique identifier of the application for which a payment record is to be marked as authorised
    """
    logger.info('Marking payment as AUTHORISED for application with id: ' + str(application_id))
    payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id}).record
    payment_record['payment_authorised'] = True
    NannyGatewayActions().put('payment', params=payment_record)


def __yield_general_processing_error_to_user(request, form, app_id):
    """
    Private helper function to show a non-field relevant error on the payment details page
    :param request: inbound HTTP request
    :param form: the Django/GOV.UK form to which the error will be appended
    :param app_id: the user's application id
    :return: HTML template inclusive of a processing error
    """

    form.add_error(None, 'There has been a problem when trying to process your payment. '
                         'Your card has not been charged. '
                         'Please check your card details and try again.')
    form.error_summary_template_name = 'error-summary.html'

    # Payment failure path if server error encountered
    variables = {
        'form': form,
        'application_id': app_id,
    }

    return render(request, 'payment-details.html', variables)


def __rollback_payment_submission_status(application_id):
    """
    Method for rolling back a payment submission if card details have been declined
    :param application_id: the unique identifier of the application for which a payment is to be rolled back
    """
    logger.info('Rolling payment back in response to REFUSED status for application with id: '
                + str(application_id))
    payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id}).record
    payment_record['payment_submitted'] = False
    NannyGatewayActions().put('payment', params=payment_record)


def __redirect_to_payment_confirmation(application_reference, application_id):
    """
    Private helper function for redirecting to the payment confirmation page
    :return: payment confirmation page redirect
    """
    return HttpResponseRedirect(
        reverse('declaration:confirmation')
        + '?id=' + str(application_id)
        + '&orderCode=' + application_reference
    )


def payment_confirmation(request):
    """
    Method returning the template for the Payment confirmation page (for a given application)
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered Payment confirmation template
    """
    application_id_local = request.GET['id']
    conviction = NannyGatewayActions().read('dbs-check', params={'application_id': application_id_local}).record['cautions_convictions']
    local_app = NannyGatewayActions().read('application', params={'application_id': application_id_local}).record

    variables = {
        'application_id': application_id_local,
        'order_code': request.GET["orderCode"],
        'conviction': conviction,
        # 'health_status': local_app['health_status']  # Non-existent field in NannyApplication table.
    }

    local_app['declarations_status'] = 'COMPLETED'
    local_app['application_status'] = 'SUBMITTED'
    NannyGatewayActions().put('application', params=local_app)

    return render(request, 'payment-confirmation.html', variables)


def __build_message_body(application, amount):
    """
    Helper method to build an SQS request to be picked up by the Integration Adapter component
    for relay to NOO
    :param application: the application for which a payment request is to be generated
    :param amount: the amount that the payment was for
    :return: an SQS request that can be consumed up by the Integration Adapter component
    """

    application_reference = application['application_reference']
    applicant_details = NannyGatewayActions().read('applicant-personal-details',
                                                   params={'application_id': application['application_id']}).record

    if len(applicant_details['middle_names']):
        applicant_name = applicant_details['last_name'] + ', ' + applicant_details['first_name'] + " " + applicant_details['middle_names']
    else:
        applicant_name = applicant_details['last_name'] + ', ' + applicant_details['first_name']

    payment_record = NannyGatewayActions().read('payment', params={'application_id': application['application_id']}).record
    payment_reference = payment_record['payment_reference']

    return {
        "payment_action": "SC1",
        "payment_ref": payment_reference,
        "payment_amount": amount,
        "urn": str(settings.PAYMENT_URN_PREFIX) + application_reference,
        "setting_name": applicant_name
    }