from unittest import mock

from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import reverse
from django.test import Client, modify_settings, SimpleTestCase, TestCase
from django.urls import resolve

from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions
from application.services import payment_service
from application.presentation.payment.forms import PaymentDetailsForm
from application.presentation.payment.views import payment as payment_views
from application.presentation.declaration.views import Confirmation
from application.tests.test_utils import side_effect


valid_payment_data ={
    'id': '',
    'card_type': 'visa',
    'card_number': '4545454545454545',
    'expiry_date_0': '10',
    'expiry_date_1': '22',
    'cardholders_name': 'AUTHORISED',
    'card_security_code' : '123'
}


@modify_settings(MIDDLEWARE={
        'remove': [
            'nanny.middleware.CustomAuthenticationHandler',
        ]
    })
@mock.patch.object(payment_service, 'make_payment')
@mock.patch.object(payment_views, '__assign_application_reference')
@mock.patch.object(payment_views, '__create_payment_record', side_effect={'payment_reference': 'fairlyOddReference'})
@mock.patch.object(IdentityGatewayActions, 'read',   side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'create', side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'read',   side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'list',   side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'patch',  side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'put',    side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'delete', side_effect=side_effect)
class PaymentTests(TestCase):
    """
    Tests for asserting payment functionality
    """
    def setUp(self):
        self.client = Client()
        self.test_app_id = ''

    def test_get_to_payment_page_renders_payment_details_if_no_prior_payment_record_exists(self, *args):
        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x: False):

            response = self.client.get(
                reverse('payment:payment-details'),
                data={
                    'id': self.test_app_id
                }
            )

            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'payment-details.html')

    def test_get_to_payment_page_renders_paid_page_if_prior_payment_previously_authorised(self, *args):
        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x: True):

            response = self.client.get(
                reverse('payment:payment-details'),
                data={
                    'id': self.test_app_id
                }
            )

            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'paid.html')

    def test_get_to_payment_page_redirects_renders_payment_details_if_payment_not_previously_authorised(self, *args):
        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : True), \
                mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_authorised': False}):

            response = self.client.get(
                reverse('payment:payment-details'),
                data={
                    'id': self.test_app_id
                }
            )

            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'payment-details.html')

    def test_post_to_payment_page_renders_payment_details_if_form_invalid(self, *args):
        response = self.client.post(reverse('payment:payment-details'), data={'id': self.test_app_id})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment-details.html')

    def test_payment_attempted_if_no_prior_payment_exists(self, *args):
        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : False), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': None}), \
            mock.patch.object(payment_service, 'make_payment') as make_payment_mock:

            self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertTrue(make_payment_mock.called)

    def test_payment_attempted_if_prior_payment_record_but_not_submitted(self, *args):
        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : True), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': False}), \
            mock.patch.object(payment_service, 'make_payment') as make_payment_mock:

            self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertTrue(make_payment_mock.called)

    def test_redirect_to_payment_success_page_if_201_worldpay_response_and_lastevent_authorised(self, *args):
        payment_response = HttpResponse(status=201)
        payment_response.json = lambda: {'lastEvent': 'AUTHORISED'}

        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : False), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': False}), \
            mock.patch.object(payment_service, 'make_payment', return_value=payment_response):

            response = self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertEqual(response.status_code, 302)
            self.assertEqual(resolve(response.url).func.__name__, Confirmation.__name__)

    def test_payment_details_page_rendered_if_201_worldpay_response_and_lastevent_refused(self, *args):
        payment_response = HttpResponse(status=201)
        payment_response.json = lambda: {'lastEvent': 'REFUSED'}

        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : False), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': False}), \
            mock.patch.object(payment_service, 'make_payment', return_value=payment_response):

            response = self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'payment-details.html')

    def test_payment_details_page_rendered_if_201_worldpay_response_and_lastevent_error(self, *args):
        payment_response = HttpResponse(status=201)
        payment_response.json = lambda: {'lastEvent': 'ERROR'}

        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : False), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': False}), \
            mock.patch.object(payment_service, 'make_payment', return_value=payment_response):

            response = self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'payment-details.html')

    def test_payment_details_page_rendered_called_if_not_201_worldpay_response(self, *args):
        payment_response = HttpResponse(status=404)

        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : False), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': False}), \
            mock.patch.object(payment_service, 'make_payment', return_value=payment_response):

            response = self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'payment-details.html')

    def test_resubmission_handler_called_if_payment_submitted(self, *args):
        self.skipTest('NotImplemented')

    def test_payment_marked_as_authorised_if_successful(self, *args):
        self.skipTest('NotImplemented')

    def test_payment_email_sent_if_payment_successful(self, *args):
        payment_response = HttpResponse(status=201)
        payment_response.json = lambda: {'lastEvent': 'AUTHORISED'}

        with mock.patch.object(payment_service, 'payment_record_exists', side_effect=lambda x : False), \
            mock.patch.object(payment_service, 'get_payment_record', side_effect=lambda x : {'payment_submitted': False}), \
            mock.patch.object(payment_service, 'make_payment', return_value=payment_response), \
            mock.patch.object(payment_service, 'payment_email') as payment_email_mock:

            self.client.post(
                reverse('payment:payment-details'),
                data=valid_payment_data
            )

            self.assertTrue(payment_email_mock.called)


class PaymentFormValidation(SimpleTestCase):
    def test_valid_card_details_does_not_raise_exception(self):
        form = PaymentDetailsForm(data=valid_payment_data)

        self.assertTrue(form.is_valid())

    def test_entering_no_card_type_raises_error(self):
        form = PaymentDetailsForm(data={})

        with self.assertRaisesMessage(ValidationError, 'Please select the type of card'):
            form.fields['card_type'].clean('')

    def test_entering_invalid_card_number_raises_error(self):
        invalid_card_numbers = {  # Card numbers with an invalid first number for each provider.
            'visa': '5462030000000000',
            'mastercard': '6555555555554444',
            'maestro': '‎1759649826438453'
        }

        for key, value in invalid_card_numbers.items():
            form = PaymentDetailsForm(data={'card_type': key, 'card_number': value})
            form.cleaned_data = form.data  # Manually set cleaned_data so that clean method can be tested - else failure is caught by forms.Form

            with self.assertRaisesMessage(ValidationError, 'Please check the number on your card'):
                form.clean_card_number()

    def test_entering_no_card_number_raises_error(self):
        form = PaymentDetailsForm(data={})

        with self.assertRaisesMessage(ValidationError, 'Please enter the number on your card'):
            form.fields['card_number'].clean('')

    def test_expiry_date_in_the_past_raises_error(self):
        form = PaymentDetailsForm(data={'expiry_date_0': 10, 'expiry_date_1': 10})
        form.cleaned_data = {'expiry_date': [form.data['expiry_date_0'], form.data['expiry_date_1']]}

        with self.assertRaisesMessage(ValidationError, 'Check the expiry date or use a new card'):
            form.clean_expiry_date()

    def test_entering_no_expiry_date_raises_error(self):
        form = PaymentDetailsForm(data={})

        with self.assertRaisesMessage(ValidationError, 'Please enter the expiry date on the card'):
            form.fields['expiry_date'].clean('')

    def test_entering_more_than_50_character_cardholder_name_raises_error(self):
        form = PaymentDetailsForm(data={'cardholders_name': '012345678901234567890123456789012345678901234567890'})
        form.cleaned_data = form.data

        with self.assertRaisesMessage(ValidationError, 'Please enter 50 characters or less'):
            form.clean_cardholders_name()

    def test_entering_no_cardholder_name_raises_error(self):
        form = PaymentDetailsForm(data={})

        with self.assertRaisesMessage(ValidationError, 'Please enter the name of the cardholder'):
            form.fields['cardholders_name'].clean('')

    def test_security_code_must_be_three_or_four_digits_long(self):
        test_values = [0, 12, 12345]

        for v in test_values:
            form = PaymentDetailsForm(data={'card_security_code': v})
            form.cleaned_data = form.data

            with self.assertRaisesMessage(ValidationError, 'The code should be 3 or 4 digits long'):
                form.clean_card_security_code()

    def test_entering_no_security_code_raises_error(self):
        form = PaymentDetailsForm(data={})

        with self.assertRaisesMessage(ValidationError, 'Please enter the 3 or 4 digit card security code'):
            form.fields['card_security_code'].clean('')
