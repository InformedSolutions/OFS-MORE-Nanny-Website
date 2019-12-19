from django.test import TestCase, tag


class AccountSelectionRoutingTests(TestCase):
    from application.presentation.login.forms.account_selection import AcccountSelectionForm
    form = AcccountSelectionForm

    ERROR_MESSAGE_EMPTY = 'Please select one'

    @tag('unit')
    def test_invalid_enter_empty_data(self):
        data = {}

        form = self.form(data)

        self.assertFalse(form.is_valid())

        # Check error messages
        self.assertEqual(form.errors, {
            'account_selection': [self.ERROR_MESSAGE_EMPTY]
        })

    @tag('unit')
    def test_invalid_enter_blank_data(self):
        data = {'account_selection': None}

        form = self.form(data)

        self.assertFalse(form.is_valid())

        # Check error messages
        self.assertEqual(form.errors, {
            'account_selection': [self.ERROR_MESSAGE_EMPTY]
        })

    @tag('unit')
    def test_valid_enter_true(self):
        data = {'account_selection': 'new'}

        form = self.form(data)

        self.assertTrue(form.is_valid())

    @tag('unit')
    def test_valid_enter_false(self):
        data = {'account_selection': 'existing'}

        form = self.form(data)

        self.assertTrue(form.is_valid())
