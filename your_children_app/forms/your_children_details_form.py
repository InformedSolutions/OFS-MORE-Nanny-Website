import re
from .base import BaseFormView, BaseTemplateView
from django import forms
from django.conf import settings

from nanny.db_gateways import NannyGatewayActions


class YourChildrenDetailsForm(BaseFormView):
    """
    GOV.UK form for entering own children under 16 details
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = "There was a problem with your children's details"
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode', error_messages={'required': 'Please enter your postcode'})

    def __init__(self, *args, **kwargs):
        """
        Method to configure the initialisation of the childcare address postcode search
        :param args: arguments passed to the form
        :param kwargs: keyword arguments passed to the form, e.g. application ID
        """

        # extract the application id from the 'initial' or 'data' dictionaries.
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        # extract the childcare address id from the 'initial' dictionary.
        if 'childcare_address_id' in kwargs['initial']:
            self.childcare_address_id = kwargs['initial']['childcare_address_id']

        super(ChildcareAddressForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        postcode = None
        if 'childcare_address_id' in self:
            response = NannyGatewayActions().list('childcare-address', params={'childcare_address_id': self.childcare_address_id})
            if response.status_code == 200:
                postcode = response.record[0]['postcode']
            self.pk = self.childcare_address_id

        self.fields['postcode'].initial = postcode
        self.field_list = ['postcode']



    # def clean_postcode(self):
    #     """
    #     Postcode validation
    #     :return: string
    #     """
    #     postcode = self.cleaned_data['postcode']
    #     postcode_no_space = postcode.replace(" ", "")
    #     postcode_uppercase = postcode_no_space.upper()
    #     if re.match(settings.REGEX['POSTCODE_UPPERCASE'], postcode_uppercase) is None:
    #         raise forms.ValidationError('Please enter a valid postcode')
    #     return postcode

