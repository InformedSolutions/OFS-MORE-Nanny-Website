import datetime

from application.presentation.base_views import NannyFormView
from application.services.notify import send_email
from application.presentation.utilities import app_id_finder
from ..forms.declaration import DeclarationForm

from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions


def generate_list_of_updated_tasks(application):
    """
    Method to generate a list of flagged tasks that have been updated
    :param application: a dictionary representing an application record
    :return: a list of updated tasks
    """
    # Determine which tasks have been updated
    updated_list = []

    if application['login_details_arc_flagged'] is True:
        updated_list.append('Your sign in details')
    if application['personal_details_arc_flagged'] is True:
        updated_list.append('Your personal details')
    if application['childcare_address_arc_flagged'] is True:
        updated_list.append('Childcare address')
    if application['first_aid_arc_flagged'] is True:
        updated_list.append('First aid training')
    if application['dbs_arc_flagged'] is True:
        updated_list.append('Criminal record (DBS) check')
    if application['childcare_training_arc_flagged'] is True:
        updated_list.append('Childcare training')
    if application['insurance_cover_arc_flagged'] is True:
        updated_list.append('Insurance cover')

    return updated_list


def resubmission_confirmation_email(email, application_reference, first_name, updated_tasks):
    """
    Method to send a magic link email, using notify.py, to allow applicant to log in
    """
    personalisation = {
        'ref': application_reference,
        'firstName': first_name,
    }

    all_tasks = [
        'Your sign in details',
        'Your personal details',
        'Childcare address',
        'First aid training',
        'Criminal record (DBS) check',
        'Childcare training',
        'Insurance cover'
    ]

    for task in all_tasks:
        personalisation[task] = task in updated_tasks

    # Remove parentheses from 'Criminal record (DBS) check' - Notify cannot format such variables.
    personalisation['Criminal record DBS check'] = personalisation.pop('Criminal record (DBS) check')

    template_id = '6858af6a-a731-4a93-8e16-5db4a61c9f8d'

    send_email(email, personalisation, template_id)


def clear_arc_flagged_statuses(application):
    """
    Method to clear flagged statues from Application fields.
    """
    
    flagged_fields_to_check = (
        "login_details_arc_flagged",
        "personal_details_arc_flagged",
        "childcare_address_arc_flagged",
        "first_aid_arc_flagged",
        "childcare_training_arc_flagged",
        "dbs_arc_flagged",
        "insurance_cover_arc_flagged"
    )

    for field in flagged_fields_to_check:
        application[field] = False

    return NannyGatewayActions().put('application', params=application)


class FinalDeclaration(NannyFormView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "final-declaration.html"
    success_url = None
    form_class = DeclarationForm

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        record['information_correct_declare'] = form.cleaned_data['confirm_declare']
        record['date_updated'] = datetime.datetime.today()
        NannyGatewayActions().put('application', params=record)

        if record['application_status'] == 'FURTHER_INFORMATION':
            # TODO: create a list of updated tasks
            updated_list = generate_list_of_updated_tasks(record)
            # TODO: send a re-submission email
            pd_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id}).record
            user_record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
            resubmission_confirmation_email(user_record['email'], record['application_reference'], pd_record['first_name'], updated_list)
            # TODO: clear statuses against Nanny application
            clear_arc_flagged_statuses(record)
            # TODO: redirect to resubmitted page
            self.success_url = 'declaration:confirmation'

        else:
            self.success_url = 'payment:payment-details'

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['fields'] = [context['form'].render_field(name, field) for name, field in context['form'].fields.items()]
        return context

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('declaration', params={'application_id': app_id})
        if api_response.status_code == 200:
            record = api_response.record
            initial['confirm_declare'] = record['confirm_declare']
        return initial
