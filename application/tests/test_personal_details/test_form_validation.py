from django.forms import ChoiceField, CharField

from application.presentation.personal_details.forms.your_children import PersonalDetailsYourChildrenForm
from .test_utils import PersonalDetailsTests


class YourChildrenFormTests(PersonalDetailsTests):
    form = PersonalDetailsYourChildrenForm

    def test_form_contains_conditional_reveal(self):
        form_functions = dir(self.form)
        self.assertIn('reveal_conditionally', form_functions)
        self.assertTrue(self.form.reveal_conditionally != {})

    def test_form_contains_conditional_reveal_for_tell_us_why(self):
        self.assertIn(('known_to_social_services', {True: 'reasons_known_to_social_services'}), self.form.reveal_conditionally.items())

    def test_form_contains_radio_choice(self):
        field_types_in_form = [type(field[1]) for field in self.form.base_fields.items()]
        print(field_types_in_form)
        self.assertInCount(ChoiceField, field_types_in_form, 1)

    def test_form_contains_text_field(self):
        field_types_in_form = [type(field[1]) for field in self.form.base_fields.items()]
        print(field_types_in_form)
        self.assertInCount(CharField, field_types_in_form, 1)
