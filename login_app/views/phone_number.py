from django.views.generic import FormView

from login_app.forms import PhoneNumbersForm


class PhoneNumbersFormView(FormView):
    """
    Class for handling requests to the 'Phone-Number' page.
    """
    template_name = 'phone-number.html'
    form_class = PhoneNumbersForm
    success_url = 'Phone-Number'

    def get_context_data(self, **kwargs):
        """
        Override base FormView method to add 'fields' key to context for rendering in template.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        return super(PhoneNumbersFormView, self).get_context_data(**kwargs)
