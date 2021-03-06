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

from ....services.db_gateways import NannyGatewayActions, IdentityGatewayActions

from ....services import payment_service
from ..forms.payment import PaymentDetailsForm

logger = logging.getLogger()

application_cost = 10300


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


def check_tasks_completed(application_record, include_payment=False):
    """
    Checks if all tasks in an application are at the completed stage
    :param application_record: data from the application
    :return: boolean determining whether all tasks are completed
    """
    login_completed = application_record['login_details_status'] == "COMPLETED"
    pd_completed = application_record['personal_details_status'] == "COMPLETED"
    ca_completed = application_record['childcare_address_status'] == "COMPLETED"
    fa_completed = application_record['first_aid_status'] == "COMPLETED"
    ct_completed = application_record['childcare_training_status'] == "COMPLETED"
    dbs_completed = application_record['dbs_status'] == "COMPLETED"
    ic_completed = application_record['insurance_cover_status'] == "COMPLETED"
    info_declare = application_record['information_correct_declare']
    app_submitted = False
    payment_complete = True

    if include_payment:
        payment_record = NannyGatewayActions().read('payment', params={'application_id': application_record['application_id']})
        if payment_record.status_code != 200:
            payment_complete = False
            app_submitted = application_record['application_status'] == "SUBMITTED"

    if (login_completed and pd_completed and ca_completed and fa_completed and ct_completed and dbs_completed and
            ic_completed and info_declare and payment_complete):
        return True
    else:
        if app_submitted and include_payment:
            return True
        else:
            return False


def card_payment_get_handler(request):
    """
    GET handler for card payment details page
    :param request: inbound HTTP request
    :return: A page for capturing card payment details
    """
    application_id = request.GET["id"]
    application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record

    if check_tasks_completed(application_record):
        paid = application_record['application_reference']

        # Call out to payment service API
        prior_payment_record_exists = payment_service.payment_record_exists(application_id)

        if not prior_payment_record_exists:
            form = PaymentDetailsForm()
            variables = {
                'form': form,
                'id': application_id
            }

            return render(request, 'payment-details.html', variables)

        # If a previous attempt has been made, fetch payment record
        payment_record = payment_service.get_payment_record(application_id)

        # If payment has been fully authorised show fee paid page
        if payment_record['payment_authorised']:
            variables = {
                'id': application_id,
                'order_code': paid
            }
            return render(request, 'paid.html', variables)

        # If none of the above have resulted in a yield, show payment page
        form = PaymentDetailsForm()
        variables = {
            'form': form,
            'id': application_id
        }

        return render(request, 'payment-details.html', variables)
    else:
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)


def card_payment_post_handler(request):
    """
    Handler for managing card payment POST requests
    :param request: inbound HTTP POST request
    :return: confirmation of payment or error page based on payment processing outcome
    """
    logger.info('Received request to process card payment')

    application_id = request.POST["id"]
    form = PaymentDetailsForm(request.POST)

    # If form is erroneous due to an invalid form, simply return form to user as an early return
    if not form.is_valid():
        variables = {
            'form': form,
            'id': application_id
        }
        return render(request, 'payment-details.html', variables)

    application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record

    # Boolean flag for managing logic gates
    prior_payment_record_exists = payment_service.payment_record_exists(application_id)

    __create_payment_record(application_record)

    # If no prior payment record exists, request to capture the payment
    if not prior_payment_record_exists:

        # Assign the application reference - request goes to NOO to reserve this
        application_reference = __assign_application_reference(application_record)

        # Set the official payment reference (uses the application reference)
        payment_reference = __assign_payment_reference(application_record, application_reference)

        # Attempt to lodge payment by pulling form POST details
        card_number = re.sub('[ -]+', '', request.POST["card_number"])
        cardholders_name = request.POST["cardholders_name"]
        card_security_code = str(request.POST["card_security_code"])
        expiry_month = request.POST["expiry_date_0"]
        expiry_year = '20' + request.POST["expiry_date_1"]

        # Invoke Payment Gateway API
        create_payment_response = payment_service.make_payment(application_cost, cardholders_name, card_number,
                                                               card_security_code,
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
                __rollback_payment_submission_status(application_id)
                return __yield_general_processing_error_to_user(request, form, application_id)

        else:
            # If non-201 return status, this indicates a Payment gateway or Worldpay failure
            logger.info('Payment failed - rolling back payment status for application ' +
                        str(application_id))
            __rollback_payment_submission_status(application_id)
            return __yield_general_processing_error_to_user(request, form, application_id)
    else:
        logger.info('Previous payment record already exists - handling resubmission')
        # If above logic gates have not been triggered, this indicates a form re-submission whilst processing
        # was taking place
        return resubmission_handler(request, form, application_record)


def resubmission_handler(request, form, application):
    """
    Handling logic for managing page re-submissions to avoid duplicate payments being created
    :param request: Inbound HTTP post request
    :param payment_reference: the payment reference number allocated to an application payment attempt
    :param form: the Django form for the card details page
    :param application: the user's childminder application
    :return: HTTP response redirect based on payment status check outcome
    """
    logger.info('Resubmission handler triggered due to multiple payment requests')
    application_id = application['application_id']

    # All logic below acts as a handler for page re-submissions
    time.sleep(int(settings.PAYMENT_STATUS_QUERY_INTERVAL_IN_SECONDS))

    prior_payment_record_exists = payment_service.payment_record_exists(application_id)
    if prior_payment_record_exists:
        payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id}).record
        if payment_record['payment_reference'] is not None and payment_record['payment_reference'] != "PENDING":

            # Check at this point whether Worldpay has marked the payment as authorised
            payment_status_response_raw = payment_service.check_payment(payment_record['payment_reference'])

            # If no record of the payment could be found, yield error
            if payment_status_response_raw.status_code == 404:
                logger.info('Worldpay payment record does not exist for application ' + str(application_id))
                return __yield_general_processing_error_to_user(request, form, application_id)

            # Deserialize Payment Gateway API response
            parsed_payment_response = payment_status_response_raw.json()

            if parsed_payment_response.get('lastEvent') == "AUTHORISED":
                # If payment has been marked as a AUTHORISED by Worldpay then payment has been captured
                # meaning user can be safely progressed to confirmation page
                return __handle_authorised_payment(application_id)
            if parsed_payment_response.get('lastEvent') == "REFUSED":
                # If payment has been marked as a REFUSED by Worldpay then payment has
                # been attempted but was not successful in which case a new order should be attempted.
                __rollback_payment_submission_status(application_id)
                return __yield_general_processing_error_to_user(request, form, application_id)
            if parsed_payment_response.get('lastEvent') == "ERROR":
                return __yield_general_processing_error_to_user(request, form, application_id)
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
                            'id': application_id,
                        }

                        return HttpResponseRedirect(
                            reverse('Payment-Details-View') + '?id=' + application_id, variables)

                    # Otherwise increment processing attempt count
                    request.META['processing_attempts'] = processing_attempts + 1
                else:
                    request.META['processing_attempts'] = 1

                # Retry processing of payment
                return resubmission_handler(request, form, application)

        else:
            # No payment reference exists - clear the payment record so that applicant can try again
            __rollback_payment_submission_status(application_id)
            __yield_general_processing_error_to_user(request, form, application_id)

    else:
        # No payment record exists
        __yield_general_processing_error_to_user(request, form, application_id)


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

    logger.info('Received application reference number: ' + str(response.content) + ' from gateway API')

    if response.status_code == 200:
        response_body = response.json()
        return response_body['reference']
    else:
        # Raise up exception to caller if could not allocate reference
        raise Exception


def __assign_payment_reference(application, application_reference):
    """
    Private helper method to create formatted payment reference for finance reconciliation purposes
    :param application: the application for which a new payment reference is to be assigned
    :return: a payment reference number for an application (either new or existing)
    """
    application_id = application['application_id']
    payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id}).record
    if payment_record['payment_reference'] == "PENDING":
        logger.info('Assigning new payment reference for application with id ' + str(application_id))
        payment_reference = payment_service.create_formatted_payment_reference(application_reference)
        payment_record['payment_reference'] = payment_reference
        NannyGatewayActions().put('payment', params=payment_record)
        return payment_reference
    else:
        logger.info('Returning existing payment reference for application with id: ' + str(application.application_id))
        return payment_record['payment_reference']


def __create_payment_record(application):
    """
    Private helper function for creating a payment record in the event one does not previously exist.
    If a previous record is already present, a payment reference is returned
    :param application: the application for which a new payment record is to be created
    :param application_reference: the reference number assigned to an application
    """
    application_id = application['application_id']
    prior_payment_record_exists = payment_service.payment_record_exists(application_id)

    # Lodge payment record if does not currently exist
    if not prior_payment_record_exists:
        logger.info('Creating new payment record for application with id: ' + application_id)

        NannyGatewayActions().create(
            'payment',
            params={
                'application_id': application_id,
                'payment_reference': "PENDING",
            }
        )


def __handle_authorised_payment(application_id):
    """
    Private helper function for managing a rejected payment
    :param application: application associated with the payment attempting to be made
    :return: redirect to payment confirmation page
    """

    # Update payment record to finalise approval of payment
    __mark_payment_record_as_authorised(application_id)

    # Transition application to submitted
    logger.info('Assigning submitted date for application with id: ' + str(application_id))

    application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
    application_record['date_submitted'] = datetime.datetime.today()
    application_record = NannyGatewayActions().put('application', params=application_record).record

    # Dispatch payment confirmation email to user
    __send_payment_confirmation_email(application_record)

    application_reference = application_record['application_reference']

    # Dispatch payment notification to SQS for use by NOO
    payment_service.send_payment_notification(application_id, application_cost)

    return __redirect_to_payment_confirmation(application_reference, application_id)


def __send_payment_confirmation_email(application_record):
    """
    Private helper for issuing a payment confirmation email to a user
    :param application_id: the unique identifier of the application
    """
    application_id = application_record['application_id']
    user_details = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
    applicant_details = NannyGatewayActions().read('applicant-personal-details',
                                                   params={'application_id': application_id}).record

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
        'id': app_id,
    }

    return render(request, 'payment-details.html', variables)


def __rollback_payment_submission_status(application_id):
    """
    Method for rolling back a payment submission if card details have been declined
    :param application_id: the unique identifier of the application for which a payment is to be rolled back
    """
    logger.info('Rolling payment back for application with id: '
                + str(application_id))
    payment_record = NannyGatewayActions().read('payment', params={'application_id': application_id}).record
    if not payment_record['payment_authorised']:
        # Only delete the record if the payment is not authorised
        NannyGatewayActions().delete('payment', params=payment_record)
    else:
        logger.info('Rollback cancelled - payment has already been authorised')


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
