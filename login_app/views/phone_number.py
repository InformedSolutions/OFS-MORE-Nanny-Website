from identity_models.user_details import UserDetails

from login_app.forms import PhoneNumbersForm

from .base import BaseFormView


class PhoneNumbersFormView(BaseFormView):
    """
    Class for handling requests to the 'Phone-Number' page.
    """
    template_name = 'phone-number.html'
    form_class = PhoneNumbersForm
    success_url = 'Contact-Details-Summary'

    def form_valid(self, form):
        application_id = self.request.GET['id']
        api_response = UserDetails.api.get_record(application_id=application_id)

        record = api_response.record
        record['mobile_number'] = form.cleaned_data['mobile_number']
        record['add_phone_number'] = form.cleaned_data['other_phone_number']

        UserDetails.api.put(record)  # Update entire record.

        return super(PhoneNumbersFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        return super(PhoneNumbersFormView, self).get_context_data(**kwargs)
