from django.views.generic import FormView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from login_app.forms import DBSSecurityQuestionForm, DoBSecurityQuestionForm, MobileNumberSecurityQuestionForm


class SecurityQuestionFormView(FormView):
    """
    Class for handling requests to the 'Security-Question' page.
    """
    template_name = 'security-question.html'
    form_class = None
    success_url = 'Service-Unavailable'

    def form_valid(self, form):
        return HttpResponseRedirect(reverse(self.get_success_url()))

    def get_security_question_form(self, application):
        """
        Pseudo-code for getting the security question for a given applicant, depending upon the status of their
        application.
        """

        # TODO: Add API calls to execute the below.

        acc = application.user_details
        if application.criminal_record_check_status == 'COMPLETED':
            form = DBSSecurityQuestionForm
        elif application.personal_details_status == 'COMPLETED':
            form = PostCodeForm
        elif len(acc.mobile_number) != 0:
            form = MobileNumberSecurityQuestionForm
        return form

    def get_security_question_answer(self):
        # TODO: Make API call to grab the correct answer to the security question.
        pass

    def __init__(self, *args, **kwargs):
        # self.form_class = self.get_security_question_form()
        self.form_class = DBSSecurityQuestionForm
        super(SecurityQuestionFormView, self).__init__(*args, **kwargs)
