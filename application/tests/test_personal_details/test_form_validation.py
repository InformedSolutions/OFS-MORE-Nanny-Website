from django.db.models import TextField
from django.forms import ChoiceField

from .test_utils import PersonalDetailsTests


class YourChildrenFormTests(PersonalDetailsTests):
    form = YourChildrenForm

    def test_form_contains_conditional_reveal(self):
        form_functions = dir(self.form)
        self.assertIn('reveal_conditionally', form_functions)
        self.assertTrue(self.form['reveal_conditionally'] != {})

    def test_form_contains_conditional_reveal_for_tell_us_why(self):
        self.assertInCount({}, self.form, 1)

    def test_form_contains_radio_choice(self):
        field_types_in_form = [type(field) for field in self.forms.field]
        self.assertInCount(ChoiceField, field_types_in_form, 1)

    def test_form_contains_text_field(self):
        field_types_in_form = [type(field) for field in self.forms.field]
        self.assertInCount(TextField, field_types_in_form, 1)