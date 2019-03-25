from django.test import TestCase, tag


class YourLocationRoutingTests(TestCase):
    from application.presentation.login.forms.your_location import YourLocationForm
    form = YourLocationForm

    ERROR_MESSAGE_EMPTY = 'Please say if you live in Greater London'

    @tag('unit')
    def test_invalid_enter_empty_data(self):
        data = {}

        form = self.form(data)

        self.assertFalse(form.is_valid())

        # Check error messages
        self.assertEqual(form.errors, {
            'your_location': [self.ERROR_MESSAGE_EMPTY]
        })

    @tag('unit')
    def test_invalid_enter_blank_data(self):
        data = {'your_location': None}

        form = self.form(data)

        self.assertFalse(form.is_valid())

        # Check error messages
        self.assertEqual(form.errors, {
            'your_location': [self.ERROR_MESSAGE_EMPTY]
        })

    @tag('unit')
    def test_valid_enter_true(self):
        data = {'your_location': True}

        form = self.form(data)

        self.assertTrue(form.is_valid())

    @tag('unit')
    def test_valid_enter_false(self):
        data = {'your_location': False}

        form = self.form(data)

        self.assertTrue(form.is_valid())
