from django.test import Client, modify_settings, SimpleTestCase, TestCase
from django.forms import ValidationError
from application.presentation.dbs import forms as dbs_forms, views


class CriminalRecordFormsTest(SimpleTestCase):
    def test_less_than_12_digit_dbs_raises_error(self):
        form = dbs_forms.CaptiaDBSDetailsForm(data={'dbs_number': '1'})

        with self.assertRaisesMessage(ValidationError, 'Check your certificate: the number should be 12 digits long'):
            form.clean_dbs_number()

    def test_more_than_12_digit_dbs_raises_error(self):
        form = dbs_forms.CaptiaDBSDetailsForm(data={'dbs_number': '0000000000013'})

        with self.assertRaisesMessage(ValidationError, 'Check your certificate: the number should be 12 digits long'):
            form.clean_dbs_number()

    def test_not_entering_a_dbs_number_rasies_error(self):
        form = dbs_forms.CaptiaDBSDetailsForm(data={'dbs_number': ''})

        with self.assertRaisesMessage(ValidationError, 'Please enter your DBS certificate number'):
            form.fields['dbs_number'].clean('')

    def test_not_entering_an_option_for_lived_abroad_raises_error(self):
        form = dbs_forms.LivedAbroadForm(data={'lived_abroad': ''})

        with self.assertRaisesMessage(ValidationError, 'Please say if you have lived outside of the UK in the last 5 years'):
            form.fields['lived_abroad'].clean('')






