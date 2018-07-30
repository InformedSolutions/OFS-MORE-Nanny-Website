from django.shortcuts import render
from django.views import View

from identity_models.user_details import UserDetails

from nanny import notify, utilities


class ResendEmail(View):
    """
    Class containing the methods for handling requests to the 'Resend-Email' page.
    """
    def get(self, request):
        email_address = request.GET['email_address']
        api_response = UserDetails.api.get_record(email=email_address)
        record = api_response.record
        validation_link, email_expiry_date = utilities.generate_email_validation_link(email_address)

        record['magic_link_email'] = validation_link.split('/')[-1]
        record['email_expiry_date'] = email_expiry_date
        UserDetails.api.put(record)

        # Send a Nannies email
        notify.send_email(email=email_address,
                          personalisation={"link": validation_link},
                          template_id='5d983266-7efa-4978-9d4c-9099ed6ece28')

        return render(request, template_name='email-resent.html', context={'email_address': email_address})
